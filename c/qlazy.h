/*
 *  qlazy.h
 */

#ifndef qlazy_h
#define qlazy_h

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>
#include <string.h>
#include <complex.h>
#include <readline/readline.h>
#include <readline/history.h>

#define VERSION "0.0.18"

/*====================================================================*/
/*  Definitions & Macros                                              */
/*====================================================================*/

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

#define SUC_RETURN(ret) do {						\
    g_Errno = SUCCESS;							\
    return ret;								\
  } while(0)

#ifdef DEV

#define ERR_RETURN(err,ret) do {					\
    fprintf(stderr, "%s,%s,%d - ", __FILE__, __FUNCTION__, __LINE__);	\
    error_msg(err);							\
    g_Errno = err;							\
    return ret;								\
  } while(0)

#else

#define ERR_RETURN(err,ret) do {					\
    g_Errno = err;							\
    return ret;								\
  } while(0)

#endif

/*====================================================================*/
/*  Structures                                                        */
/*====================================================================*/

typedef enum _ErrCode {
  SUCCESS,
  ERROR_INVALID_ARGUMENT,
  ERROR_CANT_ALLOC_MEMORY,
  ERROR_CANT_OPEN_FILE,
  ERROR_CANT_READ_LINE,

  /* qlazy functions */
  ERROR_HELP_PRINT,
  ERROR_QGATE_GET_SYMBOL,
  ERROR_QGATE_GET_KIND,
  ERROR_QCIRC_INIT,
  ERROR_QCIRC_APPEND_QGATE,
  ERROR_QCIRC_SET_CIMAGE,
  ERROR_QCIRC_PRINT_QCIRC,
  ERROR_QCIRC_PRINT_QGATES,
  ERROR_QCIRC_READ_FILE,
  ERROR_QCIRC_WRITE_FILE,
  ERROR_GBANK_INIT,
  ERROR_GBANK_GET,
  ERROR_GBANK_GET_ROTATION,
  ERROR_CIMAGE_INIT,
  ERROR_QSTATE_INIT,
  ERROR_QSTATE_COPY,
  ERROR_QSTATE_GET_CAMP,
  ERROR_QSTATE_PRINT,
  ERROR_QSTATE_BLOCH,
  ERROR_QSTATE_PRINT_BLOCH,
  ERROR_QSTATE_MEASURE,
  ERROR_QSTATE_MEASURE_BELL,
  ERROR_QSTATE_OPERATE_QGATE,
  ERROR_QSTATE_OPERATE_QGATE_PARAM,
  ERROR_QSTATE_EVOLVE,
  ERROR_QSTATE_INNER_PRODUCT,
  ERROR_QSTATE_EXPECT_VALUE,
  ERROR_QSTATE_APPLY_MATRIX,
  ERROR_MDATA_INIT,
  ERROR_MDATA_PRINT,
  ERROR_MDATA_PRINT_BELL,
  ERROR_QSYSTEM_INIT,
  ERROR_QSYSTEM_EXECUTE,
  ERROR_QSYSTEM_INTMODE,
  ERROR_SPRO_INIT,
  ERROR_OBSERVABLE_INIT,

  /* qlazy interactive mode */
  ERROR_NEED_TO_INITIALIZE,
  ERROR_UNKNOWN_GATE,
  ERROR_OUT_OF_BOUND,
  ERROR_SAME_QUBIT_ID,
  ERROR_TOO_MANY_ARGUMENTS,
  ERROR_NEED_MORE_ARGUMENTS,
  ERROR_CANT_INITIALIZE,
  ERROR_CANT_WRITE_FILE,
  ERROR_CANT_PRINT_QSTATE,
  ERROR_CANT_PRINT_BLOCH,
  ERROR_CANT_PRINT_CIRC,
  ERROR_CANT_PRINT_GATES,
  ERROR_CANT_PRINT_HELP,
} ErrCode;

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
  PHASE_SHIFT    = 144,		/* symbol: 'P','p'      */
  ROTATION_X	 = 150,		/* symbol: 'RX','rx'    */
  ROTATION_Y	 = 151,		/* symbol: 'RY','ry'    */
  ROTATION_Z	 = 152,		/* symbol: 'RZ','rz'    */
  CONTROLLED_X	 = 160,		/* symbol: 'CX','cx'    */
  CONTROLLED_Y	 = 161,		/* symbol: 'CX','cx'    */
  CONTROLLED_Z	 = 162,		/* symbol: 'CZ','cz'    */
  CONTROLLED_H	 = 163,		/* symbol: 'CH','ch'    */
  CONTROLLED_P	 = 164,		/* symbol: 'CP','cp'    */
  CONTROLLED_RX	 = 165,		/* symbol: 'CRX','crx'  */
  CONTROLLED_RY	 = 166,		/* symbol: 'CRY','cry'  */
  CONTROLLED_RZ	 = 167,		/* symbol: 'CRZ','crz'  */
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
  COMPLEX ControlledY[16];
  COMPLEX ControlledZ[16];
  COMPLEX ControlledH[16];
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

/*====================================================================*/
/*  Functions                                                         */
/*====================================================================*/

/* complex.h */
double	 cabs(double _Complex z);
double	 carg(double _Complex z);
double	 creal(double _Complex z);
double	 cimag(double _Complex z);
double _Complex conj(double _Complex z);

/* misc.c */
bool	 line_check_length(char* str);
bool	 line_is_blank(char* str);
bool	 line_is_comment(char* str);
bool	 line_chomp(char* str);
bool	 line_split(char* str, const char* delim, char* outlist[], int* tnum);
bool	 line_getargs(char* str, char* args[], int* anum);
bool	 line_join_token(char* dst, char* token[], int ini, int fin);
bool     line_remove_space(char* str);
bool     is_number(char* str);
bool     is_decimal(char* str);
bool	 binstr_from_decimal(char* binstr, int qubit_num, int decimal, int zflag);

/* init.c */
void	 init_qlazy(unsigned int seed);

/* message.c */
void	 error_msg(ErrCode err);

/* help.c */
bool	 help_print(char* item);

/* qgate.c */
bool	 qgate_get_symbol(char* symbol, Kind kind);
bool	 qgate_get_kind(char* symbol, Kind* kind_out);

/* qcirc.c */
bool	 qcirc_init(int qubit_num, int buf_length, void** qcirc_out);
bool	 qcirc_append_qgate(QCirc* qcirc, Kind kind, int terminal_num,
			    Para* para, int qubit_id[MAX_QUBIT_NUM]);
bool	 qcirc_set_cimage(QCirc* qcirc);
bool	 qcirc_print_qcirc(QCirc* qcirc);
bool	 qcirc_print_qgates(QCirc* qcirc);
bool	 qcirc_read_file(char* fname, void** qcirc_out);
bool	 qcirc_write_file(QCirc* qcirc, char* fname);
void	 qcirc_free(QCirc* qcirc);

/* gbank.c */
bool	 gbank_init(void** gbank_out);
bool     gbank_get(GBank* gbank, Kind kind, void** matrix_out);
bool     gbank_get_rotation(Axis axis, double phase, double unit, void** matrix_out);
bool     gbank_get_phase_shift(double phase, double unit, void** matrix_out);
bool     gbank_get_ctr_rotation(Axis axis, double phase, double unit, void** matrix_out);
bool     gbank_get_ctr_phase_shift(double phase, double unit, void** matrix_out);

/* cimage.c */
bool     cimage_init(int qubit_num, int step_num, void** cimage_out);
void	 cimage_free(CImage* cimage);

/* qstate.c */
bool	 qstate_init(int qubit_num, void** qstate_out);
bool	 qstate_copy(QState* qstate, void** qstate_out);
bool     qstate_get_camp(QState* qstate, int qubit_num, int qubit_id[MAX_QUBIT_NUM],
			 void** camp_out);
bool	 qstate_print(QState* qstate, int qubit_num, int qubit_id[MAX_QUBIT_NUM]);
bool     qstate_bloch(QState* qstate, int qid, double* theta, double* phi);
bool     qstate_print_bloch(QState* qstate, int qid);
bool	 qstate_measure(QState* qstate, int shot_num, double angle, double phase,
			int qubit_num, int qubit_id[MAX_QUBIT_NUM], void** mdata_out);
bool     qstate_measure_bell(QState* qstate, int shot_num, int qubit_num,
			     int qubit_id[MAX_QUBIT_NUM], void** mdata_out);
bool	 qstate_operate_qgate(QState* qstate, QGate* qgate);
bool	 qstate_operate_qgate_param(QState* qstate, Kind kind, double phase,
				    int qubit_id[MAX_QUBIT_NUM]);
bool     qstate_evolve(QState* qstate, Observable* observ, double time, int iter);
bool     qstate_inner_product(QState* qstate_0, QState* qstate_1, double* real,
			      double* imag);
bool     qstate_tensor_product(QState* qstate_0, QState* qstate_1, void** qstate_out);
bool     qstate_expect_value(QState* qstate, Observable* observ, double* value);
bool     qstate_apply_matrix(QState* qstate, double* matrix, int dim);
void	 qstate_free(QState* qstate);

/* mdata.c */
bool     mdata_init(int qubit_num, int state_num, int shot_num,
		    double angle, double phase, int qubit_id[MAX_QUBIT_NUM],
		    void** mdata_out);
bool	 mdata_print(MData* mdata);
bool	 mdata_print_bell(MData* mdata);
void	 mdata_free(MData* mdata);

/* qsystem.c */
bool     qsystem_init(void** qsystem_out);
bool	 qsystem_execute(QSystem* qsystem, char* fname);
bool	 qsystem_intmode(QSystem* qsystem, char* fnmae_ini);
void	 qsystem_free(QSystem* qsystem);

/* spro.c */
bool     spro_init(char* str, void** spro_out);
void     spro_free(SPro* spro);

/* observable.c */
bool     observable_init(char* str, void** observ_out);
void     observable_free(Observable* observ);

#endif
