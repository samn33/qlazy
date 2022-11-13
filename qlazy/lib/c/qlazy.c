/*
 *  qlazy.c
 */

#include "qlazy.h"

int clock_gettime();

static void _qlazy_print_help()
{
  fprintf(stderr,"\
== qlazy - quantum computer simulator ==\n\
  [option]\n\
  -qc FILE : quantum circuit file name \n\
  -i       : quantum circuit file from stdin \n\
  -sd SEED : seed of randam generation for measurement (default:time)\n\
  -tm      : output CPU time \n\
  -etm     : output elapsed time \n\
  -pr      : print circuit and exit (don't run) \n\
  -h       : print this usage and exit\n\
  -v       : print this version and exit\n\
  [example]\n\
  $ cat foo.qc \n\
  init 2       \n\
  h 0          \n\
  cx 0 1       \n\
  m            \n\
  $ qlazy -qc foo.qc \n\
  => execute circuit \n\
  $ qlazy -i < foo.qc \n\
  => execute circuit \n\
  $ qlazy -qc foo.qc -pr \n\
  => print circuit \n\
  $ qlazy \n\
  => interactive mode \n\
");
}

static void _qlazy_print_version()
{
  char cuda_str[16];

  if (is_gpu_supported_lib() == true) {
    strcpy(cuda_str, "-cuda");
  }
  else {
    strcpy(cuda_str, "");
  }

#ifdef DEV
  const char date[] = __DATE__;
  const char time[] = __TIME__;
  fprintf(stderr,"* Version: %s%s (build: %s - %s)\n", VERSION, cuda_str, date, time);
#else
  fprintf(stderr,"* Version: %s%s\n", VERSION, cuda_str);
#endif  
}

int main(int argc, char** argv)
{
  char*		fname_qc	     = NULL;
  unsigned int  seed		     = (unsigned int)time(NULL);
  int           pr		     = OFF;
  int           tm		     = OFF;
  int           etm		     = OFF;
  int           interactive	     = OFF;
  int           stdinput	     = OFF;
  QC*           qc		     = NULL;
  QSystem*      qsystem		     = NULL;
  char          fname_ini[FNAME_LEN] = DEF_QLAZYINIT;
  int           n;
  
  clock_t	  c_start	     = 0;
  clock_t	  c_end		     = 0;
  double          cpu_time           = 0.0;
  double          elapsed_time       = 0.0;
  int		  sec, nsec;
  struct timespec e_start, e_end;

  bool            use_gpu = false;
  
  /* get command line arguments */

  if (argc == 1) { interactive = ON; }
  else {
    interactive = OFF;
    for (n=1; n<argc; n++) {
      if (strcmp(argv[n],"-v") == 0) {
	_qlazy_print_version();
	exit(0);
      }
      else if (strcmp(argv[n],"-h") == 0) {
	_qlazy_print_help();
	exit(0);
      }
      else if (strcmp(argv[n],"-sd") == 0) {
	seed = (unsigned int)strtol(argv[++n],NULL,10);
      }
      else if (strcmp(argv[n],"-qc") == 0) {
	fname_qc = argv[++n];
      }
      else if (strcmp(argv[n],"-i") == 0) {
	stdinput = ON;
	fname_qc = NULL;
      }
      else if (strcmp(argv[n],"-pr") == 0) {
	pr = ON;
      }
      else if (strcmp(argv[n],"-tm") == 0) {
	tm = ON;
      }
      else if (strcmp(argv[n],"-etm") == 0) {
	etm = ON;
      }
      else {
	ERR_RETURN(ERROR_INVALID_ARGUMENT,1);
      }
    }
  }
  if ((interactive == OFF) && (stdinput == OFF) && (fname_qc == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,1);
  
  init_genrand(seed);

  if (!qsystem_init((void**)&qsystem)) ERR_RETURN(ERROR_QSYSTEM_INIT,1);
  
  if (pr == ON) {  /* print quantum circuit only */
    if (!(qc_read_file(fname_qc, (void**)&qc)))
      ERR_RETURN(ERROR_QC_READ_FILE,1);
    qc_print_qc(qc);
    qc_free(qc); qc = NULL;
  }
  else if (interactive == ON) {  /* execute in interactive mode */
    printf("interactive mode\n");
    if (!(qsystem_intmode(qsystem, fname_ini, use_gpu)))
      ERR_RETURN(ERROR_QSYSTEM_INTMODE,1);
  }
  else {  /* execute quantum circuit file */
    c_start = clock();
    clock_gettime(CLOCK_REALTIME, &e_start);
    if (!(qsystem_execute(qsystem, fname_qc, use_gpu)))
      ERR_RETURN(ERROR_QSYSTEM_EXECUTE,1);
    c_end = clock();
    clock_gettime(CLOCK_REALTIME, &e_end);
    cpu_time = (double)(c_end-c_start)/CLOCKS_PER_SEC;
    sec	= e_end.tv_sec - e_start.tv_sec;
    nsec = e_end.tv_nsec - e_start.tv_nsec;
    elapsed_time = (double)sec + (double)nsec / (1000 * 1000 * 1000);
    if (tm == ON) printf("* CPU time = %f sec\n", cpu_time);
    if (etm == ON) printf("* elapsed time = %f sec\n", elapsed_time);
  }
  
  qsystem_free(qsystem);
  qsystem = NULL;
  
  return 0;
}
