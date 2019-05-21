/*
 *  qlazy.h
 */

#ifndef qlazy_h
#define qlazy_h

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>
#include <complex.h>
#include <readline/readline.h>
#include <readline/history.h>

#define VERSION "0.0.11"

/*====================================================================*/
/*  Definitions & Macros                                              */
/*====================================================================*/

#define TRUE  1
#define FALSE 0

#define ON  1
#define OFF 0

#define MIN_DOUBLE	   0.000001
#define MAX_DOUBLE	   1000000.0

#define FNAME_LEN          1024 
#define LINE_STRLEN	   1024     /* max length of each line of read/write file */
#define TOKEN_STRLEN	   1024     /* max token string length */
#define TOKEN_NUM	   100      /* max token number of each line */
#define MAX_ERR_MSG_LENGTH 1024	    /* max string length of err message  */

#define DEF_QUBIT_NUM      5
#define DEF_QCIRC_STEPS    100
#define MAX_QUBIT_NUM      30
#define DEF_QLAZYINIT       "./.qlazyinit"

#define DEF_SHOTS 100
#define DEF_PHASE  0.0

#define BELL_PHI_PLUS  0
#define BELL_PHI_MINUS 3
#define BELL_PSI_PLUS  1
#define BELL_PSI_MINUS 2

/* phase factor for 'show' command */
#define REMOVE_PHASE_FACTOR
//#define SHOW_PHASE_FACTOR

#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))

#define IDX2(i,j) ((i<<1)+j)
#define IDX4(i,j) ((i<<2)+j)

/*====================================================================*/
/*  Structures                                                        */
/*====================================================================*/

typedef enum _ErrCode {
  NO_ERROR		      = 0,
  INVALID_ARGUMENT	      = 1,
  CANT_ALLOC_MEMORY	      = 2,
  OUT_OF_QUBIT_NUM	      = 3,
  ERROR_QGATE_PRINT	      = 10,
  ERROR_QCIRC_INIT	      = 20,
  ERROR_QCIRC_APPEND_QGATE    = 21,
  ERROR_QCIRC_READ_FILE	      = 22,
  ERROR_QCIRC_WRITE_FILE      = 23,
  ERROR_QCIRC_PRINT_QCIRC     = 24,
  ERROR_QCIRC_PRINT_QGATES    = 25,
  ERROR_QSTATE_INIT	      = 30,
  ERROR_QSTATE_COPY	      = 31,
  ERROR_QSTATE_GET_CAMP	      = 32,
  ERROR_QSTATE_PRINT	      = 33,
  ERROR_QSTATE_MEASURE        = 34,
  ERROR_QSTATE_OPERATE        = 35,
  ERROR_QSTATE_OPERATE_QGATE  = 36,
  ERROR_QSTATE_EVOLVE         = 37,
  ERROR_QSTATE_INNER_PRODUCT  = 38,
  ERROR_QSTATE_EXPECT_VALUE   = 39,
  ERROR_QSTATE_BLOCH          = 40,
  ERROR_QSTATE_PRINT_BLOCH    = 41,
  ERROR_MDATA_INIT	      = 50,
  ERROR_MDATA_PRINT	      = 51,
  ERROR_GBANK_INIT	      = 60,
  ERROR_GBANK_GET	      = 61,
  ERROR_CIMAGE_INIT	      = 70,
  ERROR_LINE_OPERATE          = 80,
  ERROR_QSYSTEM_EXECUTE       = 90,
  ERROR_QSYSTEM_INTMODE       = 91,
  ERROR_SPRO_INIT             = 100,
  ERROR_OBSERVABLE_INIT       = 110,
  ERROR_BLOCH_GET_ANGLE       = 120,
  ERROR_HELP_PRINT_MESSAGE    = 130,
} ErrCode;

typedef enum _WrnCode {
  NO_WARN		      = 0,
  WARN_NEED_TO_INITIALIZE     = 1,
  WARN_UNKNOWN_GATE	      = 2,
  WARN_OUT_OF_BOUND	      = 3,
  WARN_SAME_QUBIT_ID	      = 4,
  WARN_TOO_MANY_ARGUMENTS     = 5,
  WARN_NEED_MORE_ARGUMENTS    = 6,
  WARN_CANT_INITIALIZE        = 7,
  WARN_CANT_WRITE_FILE        = 8,
  WARN_CANT_PRINT_QSTATE      = 9,
  WARN_CANT_PRINT_BLOCH       = 10,
  WARN_CANT_PRINT_CIRC        = 11,
  WARN_CANT_PRINT_GATES       = 12,
  WARN_CANT_PRINT_HELP        = 13,
} WrnCode;

typedef enum _Kind {
  CIRC  	 = 1,	 	/* symbol: '&','circ'   */
  GATES  	 = 2,	 	/* symbol: '!','gates'  */
  SHOW   	 = 3,	 	/* symbol: '-','show'   */
  BLOCH   	 = 4,	 	/* symbol: '|','bloch'  */
  ECHO   	 = 5,	 	/* symbol: '@','echo'   */
  OUTPUT	 = 6,	 	/* symbol: '>','output' */
  HELP    	 = 7,	 	/* symbol: '?','help'   */
  QUIT	         = 8,	 	/* symbol: '.','quit'   */
  INIT  	 = 9,	 	/* symbol: '%','init'   */
  PAULI_X	 = 120,		/* symbol: 'X','x'      */
  PAULI_Y	 = 121,		/* symbol: 'Y','y'      */
  PAULI_Z	 = 122,		/* symbol: 'Z','z'      */
  ROOT_PAULI_X	 = 123,		/* symbol: 'XR','xr'    */
  ROOT_PAULI_X_	 = 124,		/* symbol: 'XR+','xr'   */
  HADAMARD	 = 130,		/* symbol: 'H','h'      */
  PHASE_SHIFT_S	 = 140,		/* symbol: 'S','s'      */
  PHASE_SHIFT_S_ = 141,		/* symbol: 'S+','s+'    */
  PHASE_SHIFT_T	 = 142,		/* symbol: 'T','t'      */
  PHASE_SHIFT_T_ = 143,		/* symbol: 'T+','t+'    */
  ROTATION_X	 = 150,		/* symbol: 'RX','rx'    */
  ROTATION_Y	 = 151,		/* symbol: 'RY','ry'    */
  ROTATION_Z	 = 152,		/* symbol: 'RZ','rz'    */
  CONTROLLED_X	 = 160,		/* symbol: 'CX','cx'    */
  CONTROLLED_Z	 = 161,		/* symbol: 'CZ','cz'    */
  TOFFOLI	 = 170,		/* symbol: 'CCX','ccx'  */
  MEASURE	 = 200,	 	/* symbol: 'M','m'      */
  MEASURE_X	 = 201,	 	/* symbol: 'MX','mx'    */
  MEASURE_Y	 = 202,	 	/* symbol: 'MY','my'    */
  MEASURE_Z	 = 203,	 	/* symbol: 'MZ','mz'    */
  MEASURE_BELL	 = 204,	 	/* symbol: 'MB','mb'    */
  NOT_A_GATE	 = 1000,
} Kind;

typedef enum _Axis {
  X_AXIS = 0,
  Y_AXIS = 1,
  Z_AXIS = 2,
} Axis;

typedef enum _SpinType {
  NONE	  = 0, /* = Identity */
  SIGMA_X = 1,
  SIGMA_Y = 2,
  SIGMA_Z = 3,
} SpinType;

typedef double _Complex COMPLEX;

typedef struct _ParaMes {
  int		shots;
  double	angle;
  double	phase;
} ParaMes;
  
typedef union _Para {
  double	phase;		/* phase angle under unit PI (for RX,RY,RZ) */
  ParaMes	mes;		/* measurement parameter (for M) */
} Para;
  
typedef struct _QGate {
  Kind	        kind;
  Para          para;
  int		terminal_num;
  int		qubit_id[MAX_QUBIT_NUM];
} QGate;

typedef struct _CImage {
  int		qubit_num;
  char**	ch;
} CImage;

typedef struct _GBank {
  COMPLEX PauliX[4];
  COMPLEX PauliY[4];
  COMPLEX PauliZ[4];
  COMPLEX RootPauliX[4];
  COMPLEX RootPauliX_[4];
  COMPLEX Hadamard[4];
  COMPLEX PhaseShiftS[4];
  COMPLEX PhaseShiftS_[4];
  COMPLEX PhaseShiftT[4];
  COMPLEX PhaseShiftT_[4];
  COMPLEX ControlledX[16];
  COMPLEX ControlledZ[16];
} GBank;

typedef struct _QCirc {
  int		qubit_num;
  int		step_num;
  int           buf_length;
  QGate*	qgate;
  CImage*       cimage;
} QCirc;

typedef struct _QState {
  int		qubit_num;	/* number of qubits */
  int		state_num;	/* number of quantum state (dim = 2^num) */
  COMPLEX*	camp;           /* complex amplitude of the quantum state */
  GBank*        gbank;
} QState;

typedef struct _MData {
  int		qubit_num;
  int		state_num;
  int		shot_num;
  double	angle;
  double	phase;
  int		qubit_id[MAX_QUBIT_NUM];
  int*		freq;
  int		last;
} MData;

typedef struct _QSystem {
  QCirc*	qcirc;
  QState*	qstate;
  int           qubit_num;
} QSystem;

/* spin-product = tensor product of spins: [ex] "-2.0*X_0*Z_1*Y_2" */
typedef struct _SPro {
  double	coef;
  int		spin_num;	                /* max of spin id + 1 */
  SpinType	spin_type[MAX_QUBIT_NUM];	/* Pauli-X,Y,Z,or Identity*/
} SPro;

/* observable consist of pauli operators (= array of "SpinProduct") */
/* ex) 3.0-2.0*X_0*Z_1*Y_2 + Z_1*X_2 + 4.0*Z_3 ... */
typedef struct _Observable {
  int		spin_num;
  int		array_num;
  SPro**	spro_array;
} Observable;

/*====================================================================*/
/*  Global Variables                                                  */
/*====================================================================*/

#ifdef GLOBAL_VALUE_DEFINE
  #define GLOBAL
#else
  #define GLOBAL extern
#endif

GLOBAL ErrCode  g_Errno;
GLOBAL WrnCode  g_Wrnno;

/*====================================================================*/
/*  Functions                                                         */
/*====================================================================*/

/* complex.h */
double	cabs(double _Complex z);
double	carg(double _Complex z);
double	creal(double _Complex z);
double	cimag(double _Complex z);
double _Complex conj(double _Complex z);

/* init.c */
void	 init_qlazy(unsigned int seed);

/* message.c */
void	 error_msg(ErrCode err);
void	 warn_msg(WrnCode wrn);

/* help.c */
int	 help_print(char* item);

/* line.c */
int	 line_check_length(char* str);
int	 line_is_blank(char* str);
int	 line_is_comment(char* str);
int	 line_chomp(char* str);
int	 line_split(char* str, const char* delim, char* outlist[]);
int	 line_getargs(char* str, char* args[]);
int	 line_join_token(char* dst, char* token[], int ini, int fin);
int      line_remove_space(char* str);

/* misc.c */
int      is_number(char* str);
int      is_decimal(char* str);
int	 get_binstr_from_decimal(char* binstr, int qubit_num, int decimal, int zflag);
int      select_bits(int* bits_out, int bits_in, int digits_out, int digits_in,
		     int digit_array[MAX_QUBIT_NUM]);
int      complex_division(COMPLEX a, COMPLEX b, COMPLEX* c);

/* bloch.c */
int      bloch_get_angle(COMPLEX alpha, COMPLEX beta, double* theta, double* phi);

/* qgate.c */
void	 qgate_init(void);
void	 qgate_get_symbol(char* symbol, Kind kind);
Kind	 qgate_get_kind(char* symbol);

/* qcirc.c */
QCirc*	 qcirc_init(int qubit_num, int buf_length);
int	 qcirc_append_qgate(QCirc* qcirc, Kind kind, int terminal_num,
			    Para* para, int qubit_id[MAX_QUBIT_NUM]);
int	 qcirc_set_cimage(QCirc* qcirc);
int	 qcirc_print_qcirc(QCirc* qcirc);
int	 qcirc_print_qgates(QCirc* qcirc);
QCirc*	 qcirc_read_file(char* fname);
int	 qcirc_write_file(QCirc* qcirc, char* fname);
void	 qcirc_free(QCirc* qcirc);

/* spro.c */
SPro*    spro_init(char* str);
void     spro_free(SPro* spro);

/* observable.c */
Observable*  observable_init(char* str);
void         observable_free(Observable* observ);

/* qstate.c */
QState*	 qstate_init(int qubit_num);
QState*	 qstate_copy(QState* qstate);
double*  qstate_get_camp(QState* qstate, int qubit_num, int qubit_id[MAX_QUBIT_NUM]);
int	 qstate_print(QState* qstate, int qubit_num, int qubit_id[MAX_QUBIT_NUM]);
int      qstate_bloch(QState* qstate, int qid, double* theta, double* phi);
int      qstate_print_bloch(QState* qstate, int qid);
MData*	 qstate_measure(QState* qstate, int shot_num, double angle, double phase,
			int qubit_num, int qubit_id[MAX_QUBIT_NUM]);
MData*   qstate_measure_bell(QState* qstate, int shot_num, int qubit_num,
			     int qubit_id[MAX_QUBIT_NUM]);
int	 qstate_operate_qgate_param(QState* qstate, Kind kind, double phase,
				    int qubit_id[MAX_QUBIT_NUM]);
int	 qstate_operate_qgate(QState* qstate, QGate* qgate);
int      qstate_evolve(QState* qstate, Observable* observ, double time, int iter);
int      qstate_inner_product(QState* qstate_0, QState* qstate_1, double* real,
			      double* imag);
int      qstate_expect_value(QState* qstate, Observable* observ, double* value);
void	 qstate_free(QState* qstate);

/* mdata.c */
MData*	 mdata_init(int qubit_num, int state_num, int shot_num,
		    double angle, double phase, int qubit_id[MAX_QUBIT_NUM]);
int	 mdata_print(MData* mdata);
int	 mdata_print_bell(MData* mdata);
void	 mdata_free(MData* mdata);

/* gbank.c */
GBank*	 gbank_init(void);
COMPLEX* gbank_get(GBank* gbank, Kind kind);
COMPLEX* gbank_get_rotation(Axis axis, double phase, double unit);

/* cimage.c */
CImage*	 cimage_init(int qubit_num, int step_num);
void	 cimage_free(CImage* cimage);

/* qsystem.c */
QSystem* qsystem_init(void);
int	 qsystem_execute(QSystem* qsystem, char* fname);
int	 qsystem_intmode(QSystem* qsystem, char* fnmae_ini);
void	 qsystem_free(QSystem* qsystem);

#endif
