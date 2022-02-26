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

#define VERSION "0.2.4"

//#define TEST_NEW_VERSION

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
#define DEF_QC_STEPS       100
#define DEF_QCIRC_DEPTH    100
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

#ifndef S_SPLINT_S
#define COMP_I 1.0i
#else
#define COMP_I 1.0
#endif

#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))

#define IDX2(i,j) ((i<<1)+j)
#define IDX4(i,j) ((i<<2)+j)

#define SUC_RETURN(ret) do {						\
    return ret;								\
  } while(0)

#ifdef DEV

#define ERR_RETURN(err,ret) do {					\
    fprintf(stderr, "%s,%s,%d - ", __FILE__, __FUNCTION__, __LINE__);	\
    error_msg(err);							\
    return ret;								\
  } while(0)

#else

#define ERR_RETURN(err,ret) do {					\
    error_msg(err);							\
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
  ERROR_QG_GET_SYMBOL,
  ERROR_QG_GET_KIND,
  ERROR_QC_INIT,
  ERROR_QC_APPEND_QGATE,
  ERROR_QC_SET_CIMAGE,
  ERROR_QC_PRINT_QC,
  ERROR_QC_PRINT_QGATES,
  ERROR_QC_READ_FILE,
  ERROR_QC_WRITE_FILE,
  ERROR_GBANK_INIT,
  ERROR_GBANK_GET_UNITARY,
  ERROR_QSTATE_INIT,
  ERROR_QSTATE_INIT_WITH_VECTOR,
  ERROR_QSTATE_COPY,
  ERROR_QSTATE_GET_CAMP,
  ERROR_QSTATE_PRINT,
  ERROR_QSTATE_BLOCH,
  ERROR_QSTATE_PRINT_BLOCH,
  ERROR_QSTATE_MEASURE,
  ERROR_QSTATE_MEASURE_STATS,
  ERROR_QSTATE_MEASURE_BELL_STATS,
  ERROR_QSTATE_OPERATE_QGATE,
  ERROR_QSTATE_EVOLVE,
  ERROR_QSTATE_INNER_PRODUCT,
  ERROR_QSTATE_EXPECT_VALUE,
  ERROR_QSTATE_APPLY_MATRIX,
  ERROR_QSTATE_OPERATE_QCIRC,
  ERROR_MDATA_INIT,
  ERROR_MDATA_PRINT,
  ERROR_MDATA_PRINT_BELL,
  ERROR_QSYSTEM_INIT,
  ERROR_QSYSTEM_EXECUTE,
  ERROR_QSYSTEM_INTMODE,
  ERROR_SPRO_INIT,
  ERROR_OBSERVABLE_INIT,
  ERROR_DENSOP_INIT,
  ERROR_DENSOP_INIT_WITH_MATRIX,
  ERROR_DENSOP_COPY,
  ERROR_DENSOP_GET_ELM,
  ERROR_DENSOP_PRINT,
  ERROR_DENSOP_ADD,
  ERROR_DENSOP_MUL,
  ERROR_DENSOP_TRACE,
  ERROR_DENSOP_SQTRACE,
  ERROR_DENSOP_PATRACE,
  ERROR_DENSOP_APPLY_MATRIX,
  ERROR_DENSOP_PROBABILITY,
  ERROR_DENSOP_TENSOR_PRODUCT,
  ERROR_STABILIZER_INIT,
  ERROR_STABILIZER_COPY,
  ERROR_STABILIZER_SET_PAULI_OP,
  ERROR_STABILIZER_GET_PAULI_OP,
  ERROR_STABILIZER_SET_PAULI_FAC,
  ERROR_STABILIZER_GET_PAULI_FAC,
  ERROR_STABILIZER_OPERATE_QGATE,
  ERROR_STABILIZER_MEASURE,
  ERROR_STABILIZER_OPERATE_QCIRC,
  ERROR_QCIRC_INIT,
  ERROR_QCIRC_APPEND_GATE,
  ERROR_CMEM_INIT,
  ERROR_CMEM_COPY,

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
  ERROR_CANT_RESET,
} ErrCode;

typedef enum _Kind {
  CIRC  	 = 1,	 	/* symbol: '&','circ'  */
  GATES  	 = 2,	 	/* symbol: '!','gates' */
  SHOW   	 = 3,	 	/* symbol: '-','show'   */
  BLOCH   	 = 4,	 	/* symbol: '|','bloch' */
  ECHO   	 = 5,	 	/* symbol: '@','echo'  */
  OUTPUT	 = 6,	 	/* symbol: '>','output' */
  HELP    	 = 7,	 	/* symbol: '?','help'   */
  QUIT	         = 8,	 	/* symbol: '.','quit'   */
  INIT  	 = 9,	 	/* symbol: '%','init'   */
  PAULI_X	 = 120,		/* symbol: 'x'          */
  PAULI_Y	 = 121,		/* symbol: 'y'          */
  PAULI_Z	 = 122,		/* symbol: 'z'          */
  ROOT_PAULI_X	 = 123,		/* symbol: 'xr'         */
  ROOT_PAULI_X_	 = 124,		/* symbol: 'xr'         */
  HADAMARD	 = 130,		/* symbol: 'h'          */
  PHASE_SHIFT_S	 = 140,		/* symbol: 's'          */
  PHASE_SHIFT_S_ = 141,		/* symbol: 's_dg'       */
  PHASE_SHIFT_T	 = 142,		/* symbol: 't'          */
  PHASE_SHIFT_T_ = 143,		/* symbol: 'tdg'        */
  PHASE_SHIFT    = 144,		/* symbol: 'p'          */
  ROTATION_X	 = 150,		/* symbol: 'rx'         */
  ROTATION_Y	 = 151,		/* symbol: 'ry'         */
  ROTATION_Z	 = 152,		/* symbol: 'rz'         */
  ROTATION_U1	 = 153,		/* symbol: 'u1'         */
  ROTATION_U2	 = 154,		/* symbol: 'u2'         */
  ROTATION_U3	 = 155,		/* symbol: 'u3'         */
  CONTROLLED_X	 = 160,		/* symbol: 'cx'         */
  CONTROLLED_Y	 = 161,		/* symbol: 'cx'         */
  CONTROLLED_Z	 = 162,		/* symbol: 'cz'         */
  CONTROLLED_XR	 = 163,		/* symbol: 'cxr'        */
  CONTROLLED_XR_ = 164,		/* symbol: 'cxr_dg'     */
  CONTROLLED_H	 = 165,		/* symbol: 'ch'         */
  CONTROLLED_S	 = 166,		/* symbol: 'cs'         */
  CONTROLLED_S_	 = 167,		/* symbol: 'cs_dg'      */
  CONTROLLED_T	 = 168,		/* symbol: 'ct'         */
  CONTROLLED_T_	 = 169,		/* symbol: 'ct_dg'      */
  CONTROLLED_P	 = 170,		/* symbol: 'cp'         */
  CONTROLLED_RX	 = 171,		/* symbol: 'crx'        */
  CONTROLLED_RY	 = 172,		/* symbol: 'cry'        */
  CONTROLLED_RZ	 = 173,		/* symbol: 'crz'        */
  CONTROLLED_U1  = 174,		/* symbol: 'cu1'        */
  CONTROLLED_U2  = 175,		/* symbol: 'cu1'        */
  CONTROLLED_U3  = 176,		/* symbol: 'cu1'        */
  SWAP_QUBITS	 = 180,		/* symbol: 'sw'         */
  MEASURE	 = 200,	 	/* symbol: 'm'          */
  MEASURE_X	 = 201,	 	/* symbol: 'mx'         */
  MEASURE_Y	 = 202,	 	/* symbol: 'my'         */
  MEASURE_Z	 = 203,	 	/* symbol: 'mz'         */
  MEASURE_BELL	 = 204,	 	/* symbol: 'mb'         */
  RESET	         = 205,	 	/* symbol: '>','reset'  */
  NOT_A_GATE	 = 1000,
  IDENTITY       = 2000,
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

typedef enum _ApplyDir {
  LEFT  = 0,
  RIGHT = 1,
  BOTH  = 2,
} ApplyDir;

typedef enum _MatrixType {
  KRAUS = 1,
  POVM  = 2,
} MatrixType;

typedef double _Complex COMPLEX;

typedef struct _ParaPhase {
  double	alpha;
  double	beta;
  double	gamma;
} ParaPhase;
  
typedef struct _ParaMes {
  int		shots;
  double	angle;
  double	phase;
} ParaMes;
  
typedef union _Para {
  ParaPhase	phase;		/* phase angle under unit PI (for RX,RY,RZ) */
  ParaMes	mes;		/* measurement parameter (for M) */
} Para;
  
typedef struct _QG {
  Kind	        kind;
  Para          para;
  int		terminal_num;
  int		qubit_id[MAX_QUBIT_NUM];
} QG;

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
  COMPLEX ControlledXR[16];
  COMPLEX ControlledXR_[16];
  COMPLEX ControlledH[16];
  COMPLEX ControlledS[16];
  COMPLEX ControlledS_[16];
  COMPLEX ControlledT[16];
  COMPLEX ControlledT_[16];
  COMPLEX Swap[16];
} GBank;

typedef struct _QC {
  int		qubit_num;
  int		step_num;
  int           buf_length;
  QG*	        qgate;
  CImage*       cimage;
} QC;

typedef struct _QGate {
  Kind			kind;    /* kind of qgate */
  int			qid[2];	 /* array of qubit id */
  double		para[3]; /* array of gate parameters (ex: phases of rotation gate)*/
  int			c;       /* classical register id for storing measurement result (0 or 1) */
  int			ctrl;    /* classical register id for controlling quantum gate */
  struct _QGate*        prev;
  struct _QGate*        next;
} QGate;

typedef struct _QCirc {
  int           qubit_num;
  int           cmem_num;
  int           gate_num;
  QGate*        first;
  QGate*        last;
} QCirc;

typedef struct _CMem {
  int	        cmem_num;
  int*	        bit_array;
} CMem;

typedef struct _QState {
  int		qubit_num;	/* number of qubits */
  int		state_num;	/* number of quantum state (dim = 2^num) */
  int           buf_id;         /* official buffer id (0: buffer_0, 1: buffer_1)*/
  COMPLEX*	camp;           /* complex amplitude of the quantum state (pointer to buffer #0 or #1) */
  COMPLEX*	buffer_0;       /* complex amplitude of the quantum state (buffer #0) */
  COMPLEX*	buffer_1;       /* complex amplitude of the quantum state (buffer #1) */
  GBank*        gbank;
} QState;

typedef struct _MData {
  int		qubit_num;
  int		shot_num;
  double	angle;
  double	phase;
  int*		qubit_id;
  int*		freq;
  int		last_val;
} MData;

typedef struct _QSystem {
  QC*	qc;
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

typedef struct _DensOp {
  int		row;
  int		col;
  int           buf_id;
  COMPLEX*	elm;
  COMPLEX*	buffer_0;
  COMPLEX*	buffer_1;
  GBank*        gbank;
} DensOp;

typedef enum _ComplexAxis {
  REAL_PLUS  = 0,
  IMAG_PLUS  = 1,
  REAL_MINUS = 2,
  IMAG_MINUS = 3,
} ComplexAxis;

typedef struct _Stabilizer {
  int		gene_num;
  int		qubit_num;
  ComplexAxis*	pauli_factor;	/* number of array = gene_num */
  int*		check_matrix;	/* number of array = 2 * qubit_num * gene_num */
} Stabilizer;

/*====================================================================*/
/*  Functions                                                         */
/*====================================================================*/

/* complex.h */
double	 cabs(double _Complex);
double	 carg(double _Complex);
double	 creal(double _Complex);
double	 cimag(double _Complex);
double _Complex conj(double _Complex);
double _Complex cexp(double _Complex);

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
int      bit_permutation(int bits_in, int qnum, int qnum_part, int* qid);
int*     bit_permutation_array(int length, int qnum, int qnum_part, int* qid);
bool     is_power_of_2(int n);
int      kind_get_qid_size(Kind kind);
int      kind_get_para_size(Kind kind);
bool     kind_is_measurement(Kind kind);
bool     kind_is_reset(Kind kind);
bool     kind_is_unitary(Kind kind);

/* message.c */
void	 error_msg(ErrCode err);

/* help.c */
bool	 help_print(char* item);

/* qg.c */
bool	 qg_get_symbol(Kind kind, char* symbol_out);
bool	 qg_get_kind(char* symbol, Kind* kind_out);

/* qc.c */
bool	 qc_init(int qubit_num, int buf_length, void** qc_out);
bool	 qc_append_qgate(QC* qc, Kind kind, int terminal_num,
			 Para* para, int* qubit_id);
bool	 qc_set_cimage(QC* qc);
bool	 qc_print_qc(QC* qc);
bool	 qc_print_qgates(QC* qc);
bool	 qc_read_file(char* fname, void** qc_out);
bool	 qc_write_file(QC* qc, char* fname);
void	 qc_free(QC* qc);

/* gbank.c */
bool	 gbank_init(void** gbank_out);
bool     gbank_get_unitary(GBank* gbank, Kind kind, double phase, double phase1,
			   double phase2, int* dim_out, void** matrix_out);

/* qstate.c */
bool	 qstate_init(int qubit_num, void** qstate_out);
bool	 qstate_init_with_vector(double* real, double* imag, int dim, void** qstate_out);
bool	 qstate_reset(QState* qstate, int qubit_num, int* qubit_id);
bool	 qstate_copy(QState* qstate, void** qstate_out);
bool     qstate_get_camp(QState* qstate, int qubit_num, int* qubit_id,
			 void** camp_out);
bool	 qstate_print(QState* qstate, int qubit_num, int* qubit_id, bool nonzero);
bool     qstate_bloch(QState* qstate, int qid, double* theta, double* phi);
bool     qstate_print_bloch(QState* qstate, int qid);
bool     qstate_measure(QState* qstate, double angle, double phase,
			int qubit_num, int* qubit_id, int* mval_out);
bool	 qstate_measure_stats(QState* qstate, int shot_num, double angle, double phase,
			      int qubit_num, int* qubit_id, void** mdata_out);
bool     qstate_measure_bell_stats(QState* qstate, int shot_num, int qubit_num,
				   int* qubit_id, void** mdata_out);
bool	 qstate_operate_qgate(QState* qstate, Kind kind, double alpha, double beta,
			      double gamma, int* qubit_id);
bool     qstate_evolve(QState* qstate, Observable* observ, double time, int iter);
bool     qstate_inner_product(QState* qstate_0, QState* qstate_1, double* real,
			      double* imag);
bool     qstate_tensor_product(QState* qstate_0, QState* qstate_1, void** qstate_out);
bool     qstate_expect_value(QState* qstate, Observable* observ, double* value);
bool     qstate_apply_matrix(QState* qstate, int qnum, int* qid,
			     double* real, double *imag, int row, int col);
bool     qstate_operate_qcirc(QState* qstate, CMem* cmem, QCirc* qcirc);
void	 qstate_free(QState* qstate);

/* mdata.c */
bool     mdata_init(int qubit_num, int shot_num,
		    double angle, double phase, int* qubit_id, void** mdata_out);
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

/* densop.c */
bool     densop_init(QState* qstate, double* prob, int num, void** densop_out);
bool     densop_init_with_matrix(double* real, double* imag, int row, int col,
				 void** densop_out);
bool	 densop_reset(DensOp* densop, int qubit_num, int* qubit_id);
bool	 densop_copy(DensOp* densop_in, void** densop_out);
bool     densop_get_elm(DensOp* densop, void** densop_out);
bool     densop_print(DensOp* densop, bool nonzero);
bool     densop_add(DensOp* densop, DensOp* densop_add);
bool     densop_mul(DensOp* densop, double factor);
bool     densop_trace(DensOp* densop, double* real, double* imag);
bool     densop_sqtrace(DensOp* densop, double* real, double* imag);
bool     densop_patrace(DensOp* densop_in, int qubit_num, int* qubit_id,
			void** densop_out);
bool     densop_apply_matrix(DensOp* densop, int qnum_part, int* qid,
			     ApplyDir adir, double* real, double* imag, int row, int col);
bool     densop_probability(DensOp* densop, int qnum_part, int* qid,
			    MatrixType mtype, double* real, double* imag, int row, int col,
			    double* prob_out);
bool     densop_operate_qgate(DensOp* densop, Kind kind, double alpha, double beta,
			      double gamma, int* qubit_id);
bool     densop_tensor_product(DensOp* densop_0, DensOp* densop_1, void** densop_out);
void     densop_free(DensOp* densop);

/* stabilizer.c */
bool	stabilizer_init(int gene_num, int qubit_num, unsigned int seed, void** stab_out);
bool	stabilizer_copy(Stabilizer* stab, void** stab_out);
bool	stabilizer_set_pauli_op(Stabilizer* stab, int gene_id, int qubit_id, Kind pauli_op);
bool	stabilizer_get_pauli_op(Stabilizer* stab, int gene_id, int qubit_id, Kind* pauli_op);
bool	stabilizer_set_pauli_fac(Stabilizer* stab, int gene_id, ComplexAxis pauli_fac);
bool	stabilizer_get_pauli_fac(Stabilizer* stab, int gene_id, ComplexAxis* pauli_fac);
bool	stabilizer_operate_qgate(Stabilizer* stab, Kind kind, int q0, int q1);
bool    stabilizer_get_rank(Stabilizer* stab, int* rank_out);
bool	stabilizer_measure(Stabilizer* stab, int q, double* prob_out, int* mval_out);
bool    stabilizer_operate_qcirc(Stabilizer* stab, CMem* cmem, QCirc* qcirc);
void	stabilizer_free(Stabilizer* stab);

/* qcirc.c */
bool qcirc_init(void** qcirc_out);
bool qcirc_copy(QCirc* qcirc, void** qcirc_out);
bool qcirc_merge(QCirc* qcirc_L, QCirc* qcirc_R, void** qcirc_out);
bool qcirc_is_equal(QCirc* qcirc_L, QCirc* qcirc_R, bool* ans);
bool qcirc_kind_first(QCirc* qcirc, Kind* kind);
bool qcirc_append_gate(QCirc* qcirc, Kind kind, int* qid, double* para, int c, int ctrl);
bool qcirc_pop_gate(QCirc* qcirc, Kind* kind, int* qid, double* para, int* c, int* ctrl);
void qcirc_free(QCirc* qcirc);

/* cmem.c */
bool cmem_init(int cmem_num, void** cmem_out);
bool cmem_copy(CMem* cmem_in, void** cmem_out);
void cmem_free(CMem* cmem);

#endif
