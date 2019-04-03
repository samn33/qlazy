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

#define VERSION "0.0.2"

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
  ERROR_QSTATE_GET_CAMP	      = 31,
  ERROR_QSTATE_PRINT	      = 32,
  ERROR_QSTATE_MEASURE        = 33,
  ERROR_QSTATE_OPERATE        = 34,
  ERROR_QSTATE_OPERATE_QGATE  = 35,
  ERROR_MDATA_INIT	      = 40,
  ERROR_MDATA_PRINT	      = 41,
  ERROR_GBANK_INIT	      = 50,
  ERROR_GBANK_GET	      = 51,
  ERROR_CIMAGE_INIT	      = 60,
  ERROR_LINE_OPERATE          = 70,
  ERROR_QSYSTEM_EXECUTE       = 80,
  ERROR_QSYSTEM_INTMODE       = 81,
  ERROR_HELP_PRINT_MESSAGE    = 90,
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
  WARN_CANT_PRINT_CIRC        = 9,
  WARN_CANT_PRINT_GATES       = 10,
  WARN_CANT_PRINT_HELP        = 11,
} WrnCode;

typedef enum _Kind {
  CIRC  	 = 1,	 	/* symbol: '&','circ'   */
  GATES  	 = 2,	 	/* symbol: '!','gates'  */
  SHOW   	 = 3,	 	/* symbol: '-','show'   */
  ECHO   	 = 4,	 	/* symbol: '@','echo'   */
  OUTPUT	 = 5,	 	/* symbol: '>','output' */
  HELP    	 = 6,	 	/* symbol: '?','help'   */
  QUIT	         = 7,	 	/* symbol: '.','quit'   */
  INIT  	 = 10,	 	/* symbol: '%','init'   */
  PAULI_X	 = 20,		/* symbol: 'X','x'      */
  PAULI_Y	 = 21,		/* symbol: 'Y','y'      */
  PAULI_Z	 = 22,		/* symbol: 'Z','z'      */
  ROOT_PAULI_X	 = 23,		/* symbol: 'XR','xr'    */
  ROOT_PAULI_X_	 = 24,		/* symbol: 'XR+','xr'   */
  HADAMARD	 = 30,		/* symbol: 'H','h'      */
  PHASE_SHIFT_S	 = 40,		/* symbol: 'S','s'      */
  PHASE_SHIFT_S_ = 41,		/* symbol: 'S+','s+'    */
  PHASE_SHIFT_T	 = 42,		/* symbol: 'T','t'      */
  PHASE_SHIFT_T_ = 43,		/* symbol: 'T+','t+'    */
  ROTATION_X	 = 50,		/* symbol: 'RX','rx'    */
  ROTATION_Y	 = 51,		/* symbol: 'RY','ry'    */
  ROTATION_Z	 = 52,		/* symbol: 'RZ','rz'    */
  CONTROLLED_X	 = 60,		/* symbol: 'CX','cx'    */
  CONTROLLED_Z	 = 61,		/* symbol: 'CZ','cz'    */
  TOFFOLI	 = 70,		/* symbol: 'CCX','ccx'  */
  MEASURE	 = 100,	 	/* symbol: 'M','m'      */
  NOT_A_GATE	 = 1000,
} Kind;

typedef enum _Axis {
  X_AXIS = 0,
  Y_AXIS = 1,
  Z_AXIS = 2,
} Axis;

typedef double _Complex CTYPE;

typedef union _Para {
  double	phase;  /* phase angle under unit PI (for RX,RY,RZ) */
  int		shots;	/* number of measurement (for M) */
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
  CTYPE PauliX[4];
  CTYPE PauliY[4];
  CTYPE PauliZ[4];
  CTYPE RootPauliX[4];
  CTYPE RootPauliX_[4];
  CTYPE Hadamard[4];
  CTYPE PhaseShiftS[4];
  CTYPE PhaseShiftS_[4];
  CTYPE PhaseShiftT[4];
  CTYPE PhaseShiftT_[4];
  CTYPE ControlledX[16];
  CTYPE ControlledZ[16];
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
  CTYPE*	camp;           /* complex amplitude of the quantum state */
  int           measured[MAX_QUBIT_NUM];	/* measured flag */
  GBank*        gbank;
} QState;

typedef struct _MData {
  int	qubit_num;
  int	state_num;
  int	shot_num;
  int	qubit_id[MAX_QUBIT_NUM];
  int*	freq;
  int   last;
} MData;

typedef struct _QSystem {
  QCirc*	qcirc;
  QState*	qstate;
  int           qubit_num;
} QSystem;

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
double	 cabs(double _Complex z);
double	 creal(double _Complex z);
double	 cimag(double _Complex z);

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

/* misc.c */
int	 get_binstr_from_decimal(char* binstr, int qubit_num, int decimal);
int      select_bits(int* bits_out, int bits_in, int digits_out, int digits_in,
		     int digit_array[MAX_QUBIT_NUM]);

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

/* qstate.c */
QState*	 qstate_init(int qubit_num);
double*  qstate_get_camp(QState* qstate);
int	 qstate_print(QState* qstate);
MData*	 qstate_measure(QState* qstate, int shot_num, int qubit_num,
			int qubit_id[MAX_QUBIT_NUM]);
int	 qstate_operate_qgate_param(QState* qstate, Kind kind, double phase,
				    int qubit_id[MAX_QUBIT_NUM]);
int	 qstate_operate_qgate(QState* qstate, QGate* qgate);
void	 qstate_free(QState* qstate);

/* mdata.c */
MData*	 mdata_init(int qubit_num, int state_num, int shot_num,
		    int qubit_id[MAX_QUBIT_NUM]);
int	 mdata_print(MData* mdata);
void	 mdata_free(MData* mdata);

/* gbank.c */
GBank*	 gbank_init(void);
CTYPE*	 gbank_get(GBank* gbank, Kind kind);
CTYPE*	 gbank_get_rotation(Axis axis, double phase, double unit);

/* cimage.c */
CImage*	 cimage_init(int qubit_num, int step_num);
void	 cimage_free(CImage* cimage);

/* qsystem.c */
QSystem* qsystem_init(void);
int	 qsystem_execute(QSystem* qsystem, char* fname);
int	 qsystem_intmode(QSystem* qsystem, char* fnmae_ini);
void	 qsystem_free(QSystem* qsystem);

#endif
