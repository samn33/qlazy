/*
 *  qlazy.c
 */

#include "qlazy.h"

static void qlazy_print_help()
{
  fprintf(stderr,"\
== qlazy - quantum computer simulator ==\n\
  [option]\n\
  -qc FILE : quantum circuit file name (default:interactive mode)\n\
  -sd SEED : seed of randam generation for measurement (default:time)\n\
  -tm      : output processing time \n\
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
  $ qlazy -qc foo.qc -pr \n\
  => print circuit \n\
  $ qlazy \n\
  => interactive mode \n\
");
}

static void qlazy_print_version()
{
  const char date[] = __DATE__;
  const char time[] = __TIME__;
  
  fprintf(stderr,"\
* Version: %s (build: %s - %s)\n", VERSION,date,time);
}

int main(int argc, char** argv)
{
  char*		fname_qc	     = NULL;
  unsigned int  seed		     = (unsigned int)time(NULL);
  int           pr		     = OFF;
  int           tm		     = OFF;
  int           im		     = ON;
  clock_t	c_start		     = 0;
  clock_t	c_end		     = 0;
  double        proc_time            = 0.0;
  QCirc*        qcirc		     = NULL;
  QSystem*      qsystem		     = NULL;
  char          fname_ini[FNAME_LEN] = DEF_QLAZYINIT;

  g_Errno = NO_ERROR;

  /* get command line arguments */

  for (int n=1; n<argc; n++) {
    if (strcmp(argv[n],"-v") == 0) {
      qlazy_print_version();
      exit(0);
    }
    else if (strcmp(argv[n],"-h") == 0) {
      qlazy_print_help();
      exit(0);
    }
    else if (strcmp(argv[n],"-sd") == 0) {
      seed = (unsigned int)strtol(argv[++n],NULL,10);
    }
    else if (strcmp(argv[n],"-qc") == 0) {
      im = OFF;
      fname_qc = argv[++n];
    }
    else if (strcmp(argv[n],"-pr") == 0) {
      pr = ON;
    }
    else if (strcmp(argv[n],"-tm") == 0) {
      tm = ON;
    }
    else {
      g_Errno = INVALID_ARGUMENT;
      goto ERROR_EXIT;
    }
  }

  init_qlazy(seed);

  qsystem = qsystem_init();
  
  if (pr == ON) {  /* print quantum circuit only */
    if (!(qcirc = qcirc_read_file(fname_qc))) goto ERROR_EXIT;
    qcirc_print_qcirc(qcirc);
    qcirc_free(qcirc); qcirc = NULL;
  }
  else if (im == ON) {  /* execute in interactive mode */
    printf("interactive mode\n");
    if (qsystem_intmode(qsystem, fname_ini) == FALSE) goto ERROR_EXIT;
  }
  else {  /* execute quantum circuit file */
    c_start = clock();
    if (qsystem_execute(qsystem, fname_qc) == FALSE) goto ERROR_EXIT;
    c_end = clock();
    proc_time = (double)(c_end-c_start)/CLOCKS_PER_SEC;
    if (tm == ON) printf("[[ time = %f sec ]]\n", proc_time);
  }
  
  qsystem_free(qsystem);
  qsystem = NULL;
  
  return 0;

 ERROR_EXIT:
  error_msg(g_Errno); exit(1);
}
