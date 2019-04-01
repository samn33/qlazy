/*
 *  qstate.c
 */

#include "qlazy.h"

static void qstate_set_0(QState* qstate)
{
  for (int i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = 0.0 + 0.0i;
  }
  qstate->camp[0] = 1.0 + 0.0i;
}

QState* qstate_init(int qubit_num)
{
  QState	*qstate = NULL;
  int		 state_num;

  g_Errno = NO_ERROR;

  if ((qubit_num < 1) || (qubit_num > MAX_QUBIT_NUM)) goto ERROR_EXIT;
  
  if (!(qstate = (QState*)malloc(sizeof(QState)))) goto ERROR_EXIT;

  qstate->qubit_num = qubit_num;
  state_num = (1 << qubit_num);
  qstate->state_num = state_num;

  if (!(qstate->camp = (CTYPE*)malloc(sizeof(CTYPE)*state_num))) goto ERROR_EXIT;

  for (int i=0; i<MAX_QUBIT_NUM; i++) qstate->measured[i] = OFF;

  qstate->gbank = gbank_init();

  qstate_set_0(qstate);

  return qstate;

 ERROR_EXIT:
  g_Errno = ERROR_QSTATE_INIT;
  return NULL;
}

double* qstate_get_camp(QState* qstate)
{
  double*  out = NULL;

  g_Errno = NO_ERROR;

  if (qstate == NULL) goto ERROR_EXIT;

  if (!(out = (double*)malloc(sizeof(double)*2*qstate->state_num)))
    goto ERROR_EXIT;

  for (int i=0; i<qstate->state_num; i++) {
    out[2*i] = creal(qstate->camp[i]);
    out[2*i+1] = cimag(qstate->camp[i]);
  }

  return out;
  
 ERROR_EXIT:
  g_Errno = ERROR_QSTATE_GET_CAMP;
  return NULL;
}

int qstate_print(QState* qstate)
{
  double	qreal,qimag,prob;
  int		prob_level = 0;
  char		state[MAX_QUBIT_NUM+1];

  g_Errno = NO_ERROR;

  if (qstate == NULL) goto ERROR_EXIT;

  for (int i=0; i<qstate->state_num; i++) {
    qreal = creal(qstate->camp[i]);
    qimag = cimag(qstate->camp[i]);

    get_binstr_from_decimal(state, qstate->qubit_num, i);

    prob = pow(cabs(qstate->camp[i]),2.0);
    if (fabs(prob) < MIN_DOUBLE) prob_level = 0;
    else prob_level = (int)(prob/0.1 + 1.0);
    
    printf("c[%s] = %+.4f%+.4f*i : %.4f |", state, qreal, qimag, prob);
    for (int k=0; k<prob_level; k++) printf("+");
    printf("\n");
  }

  return TRUE;

 ERROR_EXIT:
  g_Errno = ERROR_QSTATE_PRINT;
  return FALSE;
}

static int qstate_operate_qgate_1(QState* qstate, Kind kind, int n)
{
  int i;
  QState* qstate_tmp = NULL;
  int nn = qstate->qubit_num - n - 1;
  CTYPE* U = NULL;

  if (!(U = gbank_get(qstate->gbank, kind))) goto ERROR_EXIT;

  if (qstate == NULL) goto ERROR_EXIT;
  if (nn < 0 || nn >= qstate->qubit_num) goto ERROR_EXIT;
  
  if (!(qstate_tmp = qstate_init(qstate->qubit_num))) goto ERROR_EXIT;
  
  for (i=0; i<qstate->state_num; i++) {
    if ((i >> nn) %2 == 0) {
      qstate_tmp->camp[i]
	= U[IDX2(0,0)] * qstate->camp[i]
	+ U[IDX2(0,1)] * qstate->camp[i + (1 << nn)];
    }
    else {
      qstate_tmp->camp[i]
	= U[IDX2(1,0)] * qstate->camp[i - (1 << nn)]
	+ U[IDX2(1,1)] * qstate->camp[i];
    }
  }
  memcpy(qstate->camp, qstate_tmp->camp, sizeof(CTYPE)*qstate->state_num);
  qstate_free(qstate_tmp); qstate_tmp = NULL;

  return TRUE;

 ERROR_EXIT:
  return FALSE;
}

static int qstate_operate_qgate_1_rot(QState* qstate, Axis axis, double phase,
					  double unit, int n)
{
  int		i;
  QState*	qstate_tmp = NULL;
  int		nn	   = qstate->qubit_num - n - 1;
  CTYPE*	U	   = NULL;

  if (qstate == NULL) goto ERROR_EXIT;
  if (nn < 0 || nn >= qstate->qubit_num) goto ERROR_EXIT;
  
  /* set rotation matrix aroud the X,Y,Z-axis*/
  if (!(U = gbank_get_rotation(axis, phase, unit))) goto ERROR_EXIT;
 
  if (!(qstate_tmp = qstate_init(qstate->qubit_num))) goto ERROR_EXIT;
  
  for (i=0; i<qstate->state_num; i++) {
    if ((i >> nn) %2 == 0) {
      qstate_tmp->camp[i]
	= U[IDX2(0,0)] * qstate->camp[i]
	+ U[IDX2(0,1)] * qstate->camp[i + (1 << nn)];
    }
    else {
      qstate_tmp->camp[i]
	= U[IDX2(1,0)] * qstate->camp[i - (1 << nn)]
	+ U[IDX2(1,1)] * qstate->camp[i];
    }
  }
  memcpy(qstate->camp, qstate_tmp->camp, sizeof(CTYPE)*qstate->state_num);
  qstate_free(qstate_tmp); qstate_tmp = NULL;

  free(U); U = NULL;

  return TRUE;

 ERROR_EXIT:
  return FALSE;
}

static int qstate_operate_qgate_2(QState* qstate, Kind kind, int m, int n)
{
  int i;
  QState* qstate_tmp = NULL;
  int mm = qstate->qubit_num - m - 1;
  int nn = qstate->qubit_num - n - 1;
  CTYPE* U = NULL;

  if (!(U = gbank_get(qstate->gbank, kind))) goto ERROR_EXIT;

  if (qstate == NULL) goto ERROR_EXIT;
  if (m < 0 || m >= qstate->qubit_num) goto ERROR_EXIT;
  if (n < 0 || n >= qstate->qubit_num) goto ERROR_EXIT;
  
  if (!(qstate_tmp = qstate_init(qstate->qubit_num))) goto ERROR_EXIT;
  
  for (i=0; i<qstate->state_num; i++) {
    if (((i >> mm) % 2 == 0) && ((i >> nn) % 2 == 0)) {
      qstate_tmp->camp[i]
	= U[IDX4(0,0)] * qstate->camp[i]
	+ U[IDX4(0,1)] * qstate->camp[i + (1 << nn)]
	+ U[IDX4(0,2)] * qstate->camp[i + (1 << mm)]
	+ U[IDX4(0,3)] * qstate->camp[i + (1 << nn) + (1 << mm)];
    }
    else if (((i >> mm) % 2 == 0) && ((i >> nn) % 2 == 1)) {
      qstate_tmp->camp[i]
	= U[IDX4(1,0)] * qstate->camp[i - (1 << nn)]
	+ U[IDX4(1,1)] * qstate->camp[i]
	+ U[IDX4(1,2)] * qstate->camp[i - (1 << nn) + (1 << mm)]
	+ U[IDX4(1,3)] * qstate->camp[i + (1 << mm)];
    }
    else if (((i >> mm) % 2 == 1) && ((i >> nn) % 2 == 0)) {
      qstate_tmp->camp[i]
	= U[IDX4(2,0)] * qstate->camp[i - (1 << mm)]
	+ U[IDX4(2,1)] * qstate->camp[i + (1 << nn) - (1 << mm)]
	+ U[IDX4(2,2)] * qstate->camp[i]
	+ U[IDX4(2,3)] * qstate->camp[i + (1 << nn)];
    }
    else {
      qstate_tmp->camp[i]
	= U[IDX4(3,0)] * qstate->camp[i - (1 << nn) - (1 << mm)]
	+ U[IDX4(3,1)] * qstate->camp[i - (1 << mm)]
	+ U[IDX4(3,2)] * qstate->camp[i - (1 << nn)]
	+ U[IDX4(3,3)] * qstate->camp[i];
    }
  }
  memcpy(qstate->camp, qstate_tmp->camp, sizeof(CTYPE)*qstate->state_num);
  qstate_free(qstate_tmp); qstate_tmp = NULL;

  return TRUE;

 ERROR_EXIT:
  return FALSE;
}

static int qstate_operate_qgate_3_ccx(QState* qstate, int q0, int q1, int q2)
/* CCX = toffoli gate */
{
  if (qstate == NULL) goto ERROR_EXIT;
  
  /* H 2 */
  if (qstate_operate_qgate_1(qstate, HADAMARD, q2) == FALSE)
    goto ERROR_EXIT;
  /* CX 1 2 */
  if (qstate_operate_qgate_2(qstate, CONTROLLED_X, q1, q2) == FALSE)
    goto ERROR_EXIT;
  /* T+ 2 */
  if (qstate_operate_qgate_1(qstate, PHASE_SHIFT_T_, q2) == FALSE)
    goto ERROR_EXIT;
  /* CX 0 2 */
  if (qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q2) == FALSE)
    goto ERROR_EXIT;
  /* T 2 */
  if (qstate_operate_qgate_1(qstate, PHASE_SHIFT_T, q2) == FALSE)
    goto ERROR_EXIT;
  /* CX 1 2 */
  if (qstate_operate_qgate_2(qstate, CONTROLLED_X, q1, q2) == FALSE)
    goto ERROR_EXIT;
  /* T+ 2 */
  if (qstate_operate_qgate_1(qstate, PHASE_SHIFT_T_, q2) == FALSE)
    goto ERROR_EXIT;
  /* CX 0 2 */
  if (qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q2) == FALSE)
    goto ERROR_EXIT;
  /* T 1 */
  if (qstate_operate_qgate_1(qstate, PHASE_SHIFT_T, q1) == FALSE)
    goto ERROR_EXIT;
  /* T 2 */
  if (qstate_operate_qgate_1(qstate, PHASE_SHIFT_T, q2) == FALSE)
    goto ERROR_EXIT;
  /* H 2 */
  if (qstate_operate_qgate_1(qstate, HADAMARD, q2) == FALSE)
    goto ERROR_EXIT;
  /* CX 0 1 */
  if (qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q1) == FALSE)
    goto ERROR_EXIT;
  /* T 0 */
  if (qstate_operate_qgate_1(qstate, PHASE_SHIFT_T, q0) == FALSE)
    goto ERROR_EXIT;
  /* T+ 1 */
  if (qstate_operate_qgate_1(qstate, PHASE_SHIFT_T_, q1) == FALSE)
    goto ERROR_EXIT;
  /* CX 0 1 */
  if (qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q1) == FALSE)
    goto ERROR_EXIT;

  return TRUE;
  
 ERROR_EXIT:
  return FALSE;
}

static int qstate_measure_one_time(QState* qstate)
{
  double r = rand()/(double)RAND_MAX;
  double prob_s = 0.0;
  double prob_e = 0.0;
  int value = qstate->state_num - 1;

  for (int i=0; i<qstate->state_num; i++) {
    prob_s = prob_e;
    prob_e += pow(cabs(qstate->camp[i]),2.0);
    if (r >= prob_s && r < prob_e) value = i;
  }

  return value;
}

static int qstate_normalize(QState* qstate)
{
  double norm = 0.0;
  
  if (qstate == NULL) goto ERROR_EXIT;

  for (int i=0; i<qstate->state_num; i++) {
    norm += pow(cabs(qstate->camp[i]),2.0);
  }
  norm = sqrt(norm);

  if (norm == 0.0) goto ERROR_EXIT;

  for (int i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = qstate->camp[i] / norm;
  }

  return TRUE;
  
 ERROR_EXIT:
  return FALSE;
}

MData* qstate_measure(QState* qstate, int shot_num, int qubit_num,
		      int qubit_id[MAX_QUBIT_NUM])
{
  int		state_id;
  int		mes_id;
  int		mes_num = (1<<qubit_num);
  int           x;
  MData*	mdata	= NULL;
  
  g_Errno = NO_ERROR;

  if (qstate == NULL) goto ERROR_EXIT;
  if (shot_num < 1) goto ERROR_EXIT;
  if ((qubit_num < 0) || (qubit_num > qstate->qubit_num)) goto ERROR_EXIT;

  /* check if qubits already measured */
  for (int i=0; i<qubit_num; i++) {
    if (qstate->measured[qubit_id[i]] == ON) {
      printf("qubit:%d has already measured !\n",qubit_id[i]);
    }
  }

  /* measure all bits, if no parameter set */
  if (qubit_num == 0) {
    qubit_num = qstate->qubit_num;
    mes_num = (1<<qubit_num);
    for (int i=0; i<qstate->qubit_num; i++) {
      qubit_id[i] = i;
    }
  }

  /* initialize mdata */
  if (!(mdata = mdata_init(qubit_num, mes_num, shot_num, qubit_id))) goto ERROR_EXIT;

  /* execute mesurement */
  for (int i=0; i<shot_num; i++) {
    state_id = qstate_measure_one_time(qstate);
    if (select_bits(&mes_id, state_id, qubit_num, qstate->qubit_num, qubit_id) == FALSE)
      goto ERROR_EXIT;
    mdata->freq[mes_id]++;
  }
  mdata->last = mes_id;

  /* udate quantum state (by last measurement) */
  for (int i=0; i<qstate->state_num; i++) {
    if (select_bits(&x, i, qubit_num, qstate->qubit_num, qubit_id) == FALSE)
      goto ERROR_EXIT;
    if (x != mdata->last) qstate->camp[i] = 0.0;
  }
  if (qstate_normalize(qstate) == FALSE) goto ERROR_EXIT;
  
  /* set measured flag */
  for (int i=0; i<qubit_num; i++) {
    qstate->measured[qubit_id[i]] = ON;
  }

  return mdata;

 ERROR_EXIT:
  g_Errno = ERROR_QSTATE_MEASURE;
  return NULL;
}

int qstate_operate_qgate_param(QState* qstate, Kind kind, double phase,
			       int qubit_id[MAX_QUBIT_NUM])
{
  int q0 = qubit_id[0];
  int q1 = qubit_id[1];
  int q2 = qubit_id[2];
  
  g_Errno = NO_ERROR;

  switch (kind) {
  case INIT:
    break;
  case MEASURE:
    break;
  case PAULI_X:
  case PAULI_Y:
  case PAULI_Z:
  case ROOT_PAULI_X:
  case ROOT_PAULI_X_:
  case PHASE_SHIFT_T:
  case PHASE_SHIFT_T_:
  case PHASE_SHIFT_S:
  case PHASE_SHIFT_S_:
  case HADAMARD:
    if (qstate->measured[q0] == ON) goto ERROR_EXIT;
    if (qstate_operate_qgate_1(qstate, kind, q0) == FALSE)
      goto ERROR_EXIT;
    break;
  case ROTATION_X:
    if (qstate->measured[q0] == ON) goto ERROR_EXIT;
    if (qstate_operate_qgate_1_rot(qstate, X_AXIS, phase, M_PI, q0) == FALSE)
      goto ERROR_EXIT;
    break;
  case ROTATION_Y:
    if (qstate->measured[q0] == ON) goto ERROR_EXIT;
    if (qstate_operate_qgate_1_rot(qstate, Y_AXIS, phase, M_PI, q0) == FALSE)
      goto ERROR_EXIT;
    break;
  case ROTATION_Z:
    if (qstate->measured[q0] == ON) goto ERROR_EXIT;
    if (qstate_operate_qgate_1_rot(qstate, Z_AXIS, phase, M_PI, q0) == FALSE)
      goto ERROR_EXIT;
    break;
  case CONTROLLED_X:
  case CONTROLLED_Z:
    if (qstate->measured[q0] == ON) goto ERROR_EXIT;
    if (qstate->measured[q1] == ON) goto ERROR_EXIT;
    if (qstate_operate_qgate_2(qstate, kind, q0, q1) == FALSE)
      goto ERROR_EXIT;
    break;
  case TOFFOLI:
    if (qstate->measured[q0] == ON) goto ERROR_EXIT;
    if (qstate->measured[q1] == ON) goto ERROR_EXIT;
    if (qstate->measured[q2] == ON) goto ERROR_EXIT;
    if (qstate_operate_qgate_3_ccx(qstate, q0, q1, q2) == FALSE) goto ERROR_EXIT;
    break;
  default:
    goto ERROR_EXIT;
  }
  
  return TRUE;
  
 ERROR_EXIT:
  g_Errno = ERROR_QSTATE_OPERATE;
  return FALSE;
}

int qstate_operate_qgate(QState* qstate, QGate* qgate)
{
  Kind		kind	     = qgate->kind;
  Para*         para	     = &(qgate->para);
  int           terminal_num = qgate->terminal_num;
  int*          qubit_id     = qgate->qubit_id;
  MData*	mdata	     = NULL;
  
  g_Errno = NO_ERROR;

  switch (kind) {
  case INIT:
    break;
  case MEASURE:
    if (!(mdata = qstate_measure(qstate, para->shots, terminal_num,
				 qubit_id))) goto ERROR_EXIT;
    mdata_print(mdata);
    mdata_free(mdata); mdata = NULL;
    break;
  case PAULI_X:
  case PAULI_Y:
  case PAULI_Z:
  case ROOT_PAULI_X:
  case ROOT_PAULI_X_:
  case PHASE_SHIFT_T:
  case PHASE_SHIFT_T_:
  case PHASE_SHIFT_S:
  case PHASE_SHIFT_S_:
  case HADAMARD:
  case ROTATION_X:
  case ROTATION_Y:
  case ROTATION_Z:
  case CONTROLLED_X:
  case CONTROLLED_Z:
  case TOFFOLI:
    if (qstate_operate_qgate_param(qstate, kind, para->phase, qubit_id) == FALSE)
      goto ERROR_EXIT;
    break;
  default:
    goto ERROR_EXIT;
  }

  return TRUE;
  
 ERROR_EXIT:
  g_Errno = ERROR_QSTATE_OPERATE_QGATE;
  return FALSE;
}

void qstate_free(QState* qstate)
{
  if (qstate == NULL) return;
  
  if (qstate->camp != NULL) {
    free(qstate->camp); qstate->camp = NULL;
  }
  if (qstate->gbank != NULL) {
    free(qstate->gbank); qstate->gbank = NULL;
  }
  free(qstate);
}
