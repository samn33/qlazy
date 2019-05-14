/*
 *  qstate.c
 */

#include "qlazy.h"

static void qstate_set_none(QState* qstate)
{
  for (int i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = 0.0 + 0.0i;
  }
}

static void qstate_set_0(QState* qstate)
{
  for (int i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = 0.0 + 0.0i;
  }
  qstate->camp[0] = 1.0 + 0.0i;
}

static int qstate_normalize(QState* qstate)
{
  double	norm	    = 0.0;
  
  if (qstate == NULL) goto ERROR_EXIT;

  for (int i=0; i<qstate->state_num; i++) {
    norm += pow(cabs(qstate->camp[i]),2.0);
  }
  norm = sqrt(norm);

  if (norm == 0.0) goto ERROR_EXIT;

  /* normalization */
  for (int i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = qstate->camp[i] / norm;
  }

  return TRUE;
  
 ERROR_EXIT:
  return FALSE;
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

  qstate->gbank = gbank_init();

  qstate_set_0(qstate);

  return qstate;

 ERROR_EXIT:
  g_Errno = ERROR_QSTATE_INIT;
  return NULL;
}

QState* qstate_copy(QState* qstate_src)
{
  QState* qstate_dst = NULL;

  g_Errno = NO_ERROR;

  if (qstate_src == NULL) goto ERROR_EXIT;

  if (!(qstate_dst = qstate_init(qstate_src->qubit_num))) goto ERROR_EXIT;

  memcpy(qstate_dst->camp, qstate_src->camp, sizeof(CTYPE)*qstate_src->state_num);

  return qstate_dst;
  
 ERROR_EXIT:
  g_Errno = ERROR_QSTATE_COPY;
  return NULL;
}

static QState* qstate_mask(QState* qstate_in, int qubit_num, int qubit_id[MAX_QUBIT_NUM])
{
  MData*        mdata	    = NULL;	/* temporary in this function */
  QState*       mask_qstate = NULL;
  int           mask_qubit_num;
  int           mask_qubit_id[MAX_QUBIT_NUM];

  g_Errno = NO_ERROR;

  if (qstate_in == NULL) goto ERROR_EXIT;

  /* set temporal qstate */

  if (qstate_in->qubit_num == qubit_num) {
    mask_qstate = qstate_copy(qstate_in);
  }
  else {  /* in the case of extracting some qubit states */
    /* mask qstate by measurement */
    mask_qstate = qstate_copy(qstate_in);
    mask_qubit_num = qstate_in->qubit_num - qubit_num;
    int cnt = 0;
    for (int i=0; i<qstate_in->qubit_num; i++) {
      int flg = OFF;
      for (int j=0; j<qubit_num; j++) {
	if (i == qubit_id[j]) { flg = ON; break; }
      }
      if (flg == OFF) {
	mask_qubit_id[cnt++] = i;
      }
    }
    if (!(mdata = qstate_measure(mask_qstate, 1, 0.0, 0.0,
				 mask_qubit_num, mask_qubit_id))) goto ERROR_EXIT;
  }

  /* free temporal mdata */

  mdata_free(mdata); mdata = NULL;
  
  return mask_qstate;

 ERROR_EXIT:
  return NULL;
}

double* qstate_get_camp(QState* qstate, int qubit_num, int qubit_id[MAX_QUBIT_NUM])
{
  QState*	mask_qstate = NULL;
  double*	out	    = NULL;

  g_Errno = NO_ERROR;

  if (qstate == NULL) goto ERROR_EXIT;

  if (!(mask_qstate = qstate_mask(qstate, qubit_num, qubit_id))) goto ERROR_EXIT;

  if (!(out = (double*)malloc(sizeof(double)*2*mask_qstate->state_num)))
    goto ERROR_EXIT;

  for (int i=0; i<mask_qstate->state_num; i++) {
    out[2*i] = creal(qstate->camp[i]);
    out[2*i+1] = cimag(qstate->camp[i]);
  }

  qstate_free(mask_qstate); mask_qstate = NULL;
  
  return out;
  
 ERROR_EXIT:
  g_Errno = ERROR_QSTATE_GET_CAMP;
  return NULL;
}

#ifdef REMOVE_PHASE_FACTOR
static int qstate_remove_phase_factor(QState* qstate, CTYPE* phase_factor)
{
  CTYPE exp_i_phase = 1.0 + 0.0i;

  if (qstate == NULL) goto ERROR_EXIT;

  /* remove phase factor from whole state */
  if (fabs(cimag(qstate->camp[0])) > MIN_DOUBLE) {
    exp_i_phase = qstate->camp[0] / cabs(qstate->camp[0]);
    if (creal(qstate->camp[0]/exp_i_phase) < 0.0) {
      exp_i_phase = -exp_i_phase;
    }
  }
  else if (creal(qstate->camp[0]) < 0.0) {
    exp_i_phase = -exp_i_phase;
  }
  for (int i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = qstate->camp[i] / exp_i_phase;
  }

  *phase_factor = exp_i_phase;

  return TRUE;
  
 ERROR_EXIT:
  return FALSE;
}
#endif

int qstate_print(QState* qstate_in, int qubit_num, int qubit_id[MAX_QUBIT_NUM])
{
  double	qreal,qimag,prob;
  int		prob_level = 0;
  char		state[MAX_QUBIT_NUM+1];

  /* for extracting phase factor */
#ifdef REMOVE_PHASE_FACTOR
  CTYPE         phase_factor;
#endif

  /* for selecting some qubit id */
  int           x;
  QState*       qstate	    = NULL;	/* temporary in this function */
  MData*        mdata	    = NULL;	/* temporary in this function */
  QState*       mask_qstate = NULL;	/* temporary in this function */

  g_Errno = NO_ERROR;

  if (qstate_in == NULL) goto ERROR_EXIT;

  /* set temporal qstate */

  if (qstate_in->qubit_num == qubit_num) {
    qstate = qstate_copy(qstate_in);
  }
  else {  /* in the case of extracting some qubit states */
    mask_qstate = qstate_mask(qstate_in, qubit_num, qubit_id);

    /* selected qubits state (qstate) */
    if (!(qstate = qstate_init(qubit_num))) goto ERROR_EXIT;
    qstate_set_none(qstate);
    for (int i=0; i<mask_qstate->state_num; i++) {
      select_bits(&x, i, qubit_num, qstate_in->qubit_num, qubit_id);
      qstate->camp[x] += mask_qstate->camp[i];
    }
  }
  if (qstate_normalize(qstate) == FALSE) goto ERROR_EXIT;

  /* print qstate */

#ifdef REMOVE_PHASE_FACTOR
  if (qstate_remove_phase_factor(qstate, &phase_factor) == FALSE)
    goto ERROR_EXIT;
  
#ifdef SHOW_PHASE_FACTOR
  if (fabs(cimag(phase_factor)) > MIN_DOUBLE) {
    printf("phase factor = exp(%+.4f*PI*i)\n",carg(phase_factor)/M_PI);
  }
  else if (creal(qstate->camp[0]) < 0.0) {
    printf("phase factor = %+.4f\n",creal(phase_factor));
  }
#endif

#endif
  
  for (int i=0; i<qstate->state_num; i++) {
    qreal = creal(qstate->camp[i]);
    qimag = cimag(qstate->camp[i]);

    get_binstr_from_decimal(state, qstate->qubit_num, i, ON);

    prob = pow(cabs(qstate->camp[i]),2.0);
    if (fabs(prob) < MIN_DOUBLE) prob_level = 0;
    else prob_level = (int)(prob/0.1 + 1.5);
    
    printf("c[%s] = %+.4f%+.4f*i : %.4f |", state, qreal, qimag, prob);
    for (int k=0; k<prob_level; k++) printf("+");
    printf("\n");
  }

  /* free temporal qstate and mdata */

  qstate_free(mask_qstate); mask_qstate = NULL;
  qstate_free(qstate); qstate = NULL;
  mdata_free(mdata); mdata = NULL;
  
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

static int qstate_transform_basis(QState* qstate, double angle, double phase, int n)
{
  /*
     This function operate U+ to the qstate
     - |p> = U |0> = cos(theta/2) |0> + exp(i phi) sin(theta/2) |1>
     - U = Rz(PI/2 + phi) H Rz(theta) H
     - U+ = H Rz(-theta) H Rz(-PI/2 - phi)
   */
  double phs = -0.5 - phase;
  double ang = -angle;

  if (qstate == NULL) goto ERROR_EXIT;
  
  if (qstate_operate_qgate_1_rot(qstate, Z_AXIS, phs, M_PI, n) == FALSE)
    goto ERROR_EXIT;
  if (qstate_operate_qgate_1(qstate, HADAMARD, n) == FALSE)
    goto ERROR_EXIT;
  if (qstate_operate_qgate_1_rot(qstate, Z_AXIS, ang, M_PI, n) == FALSE)
    goto ERROR_EXIT;
  if (qstate_operate_qgate_1(qstate, HADAMARD, n) == FALSE)
    goto ERROR_EXIT;

  return TRUE;

 ERROR_EXIT:
  return FALSE;
}

static int qstate_transform_basis_inv(QState* qstate, double angle, double phase, int n)
{
  /* 
     This function operate U to the qstate
     - |p> = U |0> = cos(theta/2) |0> + exp(i phi) sin(theta/2) |1>
     - U = Rz(PI/2 + phi) H Rz(theta) H
     - U+ = H Rz(-theta) H Rz(-PI/2 - phi)
   */
  double phs = 0.5 + phase;
  double ang = angle;

  if (qstate == NULL) goto ERROR_EXIT;
  
  if (qstate_operate_qgate_1(qstate, HADAMARD, n) == FALSE)
    goto ERROR_EXIT;
  if (qstate_operate_qgate_1_rot(qstate, Z_AXIS, ang, M_PI, n) == FALSE)
    goto ERROR_EXIT;
  if (qstate_operate_qgate_1(qstate, HADAMARD, n) == FALSE)
    goto ERROR_EXIT;
  if (qstate_operate_qgate_1_rot(qstate, Z_AXIS, phs, M_PI, n) == FALSE)
    goto ERROR_EXIT;

  return TRUE;

 ERROR_EXIT:
  return FALSE;
}

static int qstate_measure_one_time_without_change_state(QState* qstate_in, double angle,
							double phase, int qubit_num,
							int qubit_id[MAX_QUBIT_NUM])
{
  double	r      = rand()/(double)RAND_MAX;
  double	prob_s = 0.0;
  double	prob_e = 0.0;
  int		value  = qstate_in->state_num - 1;
  QState*	qstate = NULL;

  /* copy qstate for measurement */
  qstate = qstate_copy(qstate_in);

  /* unitary transform, if measuremment base is not {|0><0|,|1><1|} */
  if ((angle != 0.0) || (phase != 0.0)) {
    for (int i=0; i<qubit_num; i++) {
      qstate_transform_basis(qstate, angle, phase, qubit_id[i]);
    }
  }

  for (int i=0; i<qstate->state_num; i++) {
    prob_s = prob_e;
    prob_e += pow(cabs(qstate->camp[i]),2.0);
    if (r >= prob_s && r < prob_e) value = i;
  }

  qstate_free(qstate);

  return value;
}

static int qstate_measure_one_time(QState* qstate, double angle, double phase,
				   int qubit_num, int qubit_id[MAX_QUBIT_NUM])
{
  double	r      = rand()/(double)RAND_MAX;
  double	prob_s = 0.0;
  double	prob_e = 0.0;
  int		value  = qstate->state_num - 1;
  int mes_id,x;

  /* change basis, if measurement axis isn't Z */
  if ((angle != 0.0) || (phase != 0.0)) {
    for (int i=0; i<qubit_num; i++) {
      qstate_transform_basis(qstate, angle, phase, qubit_id[i]);
    }
  }

  for (int i=0; i<qstate->state_num; i++) {
    prob_s = prob_e;
    prob_e += pow(cabs(qstate->camp[i]),2.0);
    if (r >= prob_s && r < prob_e) value = i;
  }

  /* update quantum state by measurement (projection,normalize and change basis) */

  /* projection*/
  select_bits(&mes_id, value, qubit_num, qstate->qubit_num, qubit_id);
  for (int i=0; i<qstate->state_num; i++) {
    select_bits(&x, i, qubit_num, qstate->qubit_num, qubit_id);
    if (x != mes_id) qstate->camp[i] = 0.0;
  }
  /* normalize */
  qstate_normalize(qstate);
  /* change basis (inverse), if measurement axis isn't Z */
  if ((angle != 0.0) || (phase != 0.0)) {
    for (int i=0; i<qubit_num; i++) {
      qstate_transform_basis_inv(qstate, angle, phase, qubit_id[i]);
    }
  }
  
  return value;
}

MData* qstate_measure(QState* qstate, int shot_num, double angle, double phase,
		      int qubit_num, int qubit_id[MAX_QUBIT_NUM])
{
  int		state_id;
  int		mes_id;
  int		mes_num = (1<<qubit_num);
  MData*	mdata	= NULL;
  
  g_Errno = NO_ERROR;

  if (qstate == NULL) goto ERROR_EXIT;
  if (shot_num < 1) goto ERROR_EXIT;
  if ((qubit_num < 0) || (qubit_num > qstate->qubit_num)) goto ERROR_EXIT;

  /* measure all bits, if no parameter set */
  if (qubit_num == 0) {
    qubit_num = qstate->qubit_num;
    mes_num = (1<<qubit_num);
    for (int i=0; i<qstate->qubit_num; i++) {
      qubit_id[i] = i;
    }
  }
  

  /* initialize mdata */
  if (!(mdata = mdata_init(qubit_num, mes_num, shot_num, angle, phase, qubit_id)))
    goto ERROR_EXIT;

  /* execute mesurement */
  for (int i=0; i<shot_num; i++) {
    if (i == shot_num - 1) {  /* if last measurement -> change state */
      state_id = qstate_measure_one_time(qstate, angle, phase, qubit_num, qubit_id);
    }
    else {  /* if not last measurement -> not change state */
      state_id = qstate_measure_one_time_without_change_state(qstate, angle, phase,
							      qubit_num, qubit_id);
    }
    if (select_bits(&mes_id, state_id, qubit_num, qstate->qubit_num, qubit_id) == FALSE)
      goto ERROR_EXIT;
    mdata->freq[mes_id]++;
  }
  mdata->last = mes_id;

  return mdata;

 ERROR_EXIT:
  g_Errno = ERROR_QSTATE_MEASURE;
  return NULL;
}

MData* qstate_measure_bell(QState* qstate, int shot_num, int qubit_num,
			   int qubit_id[MAX_QUBIT_NUM])
{
  MData*	mdata  = NULL;
  int		q0     = qubit_id[0];
  int		q1     = qubit_id[1];
  
  g_Errno = NO_ERROR;

  if (qstate == NULL) goto ERROR_EXIT;
  if (shot_num < 1) goto ERROR_EXIT;
  if (qubit_num != 2) goto ERROR_EXIT;

  /* equivalent transform to bell-basis */
  /* CX 0 1 */
  if (qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q1) == FALSE)
    goto ERROR_EXIT;
  /* H 0 */
  if (qstate_operate_qgate_1(qstate, HADAMARD, q0) == FALSE)
    goto ERROR_EXIT;
  /* CX 0 1 */
  if (qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q1) == FALSE)
    goto ERROR_EXIT;

  /* execute Bell-mesurement */
  if (!(mdata = qstate_measure(qstate, shot_num, 0.0, 0.0, qubit_num, qubit_id)))
    goto ERROR_EXIT;

  /* equivalent transform to bell-basis (inverse) */
  /* CX 0 1 */
  if (qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q1) == FALSE)
    goto ERROR_EXIT;
  /* H 0 */
  if (qstate_operate_qgate_1(qstate, HADAMARD, q0) == FALSE)
    goto ERROR_EXIT;
  /* CX 0 1 */
  if (qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q1) == FALSE)
    goto ERROR_EXIT;

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
  case MEASURE_X:
  case MEASURE_Y:
  case MEASURE_Z:
  case MEASURE_BELL:
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
    if (qstate_operate_qgate_1(qstate, kind, q0) == FALSE)
      goto ERROR_EXIT;
    break;
  case ROTATION_X:
    if (qstate_operate_qgate_1_rot(qstate, X_AXIS, phase, M_PI, q0) == FALSE)
      goto ERROR_EXIT;
    break;
  case ROTATION_Y:
    if (qstate_operate_qgate_1_rot(qstate, Y_AXIS, phase, M_PI, q0) == FALSE)
      goto ERROR_EXIT;
    break;
  case ROTATION_Z:
    if (qstate_operate_qgate_1_rot(qstate, Z_AXIS, phase, M_PI, q0) == FALSE)
      goto ERROR_EXIT;
    break;
  case CONTROLLED_X:
  case CONTROLLED_Z:
    if (qstate_operate_qgate_2(qstate, kind, q0, q1) == FALSE)
      goto ERROR_EXIT;
    break;
  case TOFFOLI:
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
  case MEASURE_X:
  case MEASURE_Y:
  case MEASURE_Z:
    if (!(mdata = qstate_measure(qstate, para->mes.shots,
				 para->mes.angle, para->mes.phase, terminal_num,
				 qubit_id))) goto ERROR_EXIT;
    mdata_print(mdata);
    mdata_free(mdata); mdata = NULL;
    break;
  case MEASURE_BELL:
    if (!(mdata = qstate_measure_bell(qstate, para->mes.shots, terminal_num, qubit_id)))
      goto ERROR_EXIT;
    mdata_print_bell(mdata);
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

static int qstate_evolve_spro(QState* qstate, SPro* spro, double time)
{
  int pre,now;
  
  if (qstate == NULL) return FALSE;
  if (spro == NULL) return FALSE;

  pre = -1; now = 0;
  while (now < spro->spin_num) {
    /* operate nothing */
    if (spro->spin_type[now] == NONE) {
      now++;
      continue;
    }
    /* operate G: G=H (if PauliX), G=Rx(-0.5) (if PauliY), G=I (if PauliZ) */
    if (spro->spin_type[now] == SIGMA_X) {
      if (qstate_operate_qgate_1(qstate, HADAMARD, now) == FALSE)
	return FALSE;
    }
    else if (spro->spin_type[now] == SIGMA_Y) {
      if (qstate_operate_qgate_1_rot(qstate, X_AXIS, -0.5, M_PI, now) == FALSE)
	return FALSE;
    }
    else if (spro->spin_type[now] == SIGMA_Z) {
      ;
    }
    else {
      return FALSE;
    }
    /* operate CX */
    if (pre >= 0) {
      if ((spro->spin_type[pre] != NONE) && (spro->spin_type[now] != NONE)) {
	if (qstate_operate_qgate_2(qstate, CONTROLLED_X, pre, now) == FALSE)
	  return FALSE;
      }
    }
    pre = now; now++;
  }
  
  /* operate Rz(-2.0*t) */
  now = spro->spin_num-1;
  if (qstate_operate_qgate_1_rot(qstate, Z_AXIS, -2.0*time, M_PI, now) == FALSE)
    //  if (qstate_operate_qgate_1_rot(qstate, Z_AXIS, 2.0*time, M_PI, now) == FALSE)
    //  if (qstate_operate_qgate_1_rot(qstate, Z_AXIS, time, M_PI, now) == FALSE)
    return FALSE;

  pre = now; now--;
  while (pre >= 0) {
    /* operate nothing */
    if ((now >= 0) && (spro->spin_type[now] == NONE)) {
      now--;
      if (now >= 0) continue;
    }
    /* operate CX */
    if (now >= 0) {
      if ((spro->spin_type[pre] != NONE) && (spro->spin_type[now] != NONE)) {
	if (qstate_operate_qgate_2(qstate, CONTROLLED_X, now, pre) == FALSE)
	  return FALSE;
      }
    }
    /* operate G+: G+=H (if PauliX), G+=Rx(+0.5) (if PauliY), G+=I (if PauliZ) */
    if (spro->spin_type[pre] == SIGMA_X) {
      if (qstate_operate_qgate_1(qstate, HADAMARD, pre) == FALSE)
	return FALSE;
    }
    else if (spro->spin_type[pre] == SIGMA_Y) {
      if (qstate_operate_qgate_1_rot(qstate, X_AXIS, 0.5, M_PI, pre) == FALSE)
	return FALSE;
    }
    else if (spro->spin_type[pre] == SIGMA_Z) {
      ;
    }
    else {
      return FALSE;
    }
    pre = now; now--;
  }
  
  return TRUE;
}

int qstate_evolve(QState* qstate, Observable* observ, double time, int iter)
{
  double t = time / iter;
  
  g_Errno = NO_ERROR;

  if (qstate == NULL) goto ERROR_EXIT;
  if (observ == NULL) goto ERROR_EXIT;
  if (iter < 1) goto ERROR_EXIT;

  for (int i=0; i<iter; i++) {
    for (int j=0; j<observ->array_num; j++) {
      if (qstate_evolve_spro(qstate, observ->spro_array[j], t) == FALSE)
	goto ERROR_EXIT;
    }
  }

  return TRUE;

 ERROR_EXIT:
  g_Errno = ERROR_QSTATE_EVOLVE;
  return FALSE;
}

static int qstate_add(QState* qstate, QState* qstate_add)
{
  if (qstate == NULL) return FALSE;
  if (qstate_add == NULL) return FALSE;

  if (qstate->state_num != qstate_add->state_num) return FALSE;
  for (int i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = qstate->camp[i] + qstate_add->camp[i];
  }

  return TRUE;
}

static int qstate_mul(QState* qstate, double mul)
{
  if (qstate == NULL) return FALSE;

  for (int i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = mul * qstate->camp[i];
  }

  return TRUE;
}

static QState* qstate_apply_spro(QState* qstate, SPro* spro)
{
  QState* qstate_ob = NULL;
  
  if (qstate == NULL) return NULL;
  if (spro == NULL) return NULL;

  if (!(qstate_ob = qstate_copy(qstate))) return NULL;

  for (int i=0; i<spro->spin_num; i++) {
    if (spro->spin_type[i] == NONE) {
      ;
    }
    else if (spro->spin_type[i] == SIGMA_X) {
      if (qstate_operate_qgate_1(qstate_ob, PAULI_X, i) == FALSE)
	return FALSE;
    }
    else if (spro->spin_type[i] == SIGMA_Y) {
      if (qstate_operate_qgate_1(qstate_ob, PAULI_Y, i) == FALSE)
	return FALSE;
    }
    else if (spro->spin_type[i] == SIGMA_Z) {
      if (qstate_operate_qgate_1(qstate_ob, PAULI_Z, i) == FALSE)
	return FALSE;
    }
    else {
      return NULL;
    }
  }

  if (qstate_mul(qstate_ob, spro->coef) == FALSE) return FALSE;
  
  return qstate_ob;
}

static QState* qstate_apply_observable(QState* qstate, Observable* observ)
{
  QState* qstate_ob = NULL;
  QState* qstate_tmp = NULL;

  if (qstate == NULL) return NULL;
  
  for (int i=0; i<observ->array_num; i++) {
    if (!(qstate_tmp = qstate_apply_spro(qstate, observ->spro_array[i])))
      return NULL;
    if (qstate_ob == NULL) {
      if (!(qstate_ob = qstate_init(qstate_tmp->qubit_num))) return NULL;
      qstate_set_none(qstate_ob);
    }
    if (qstate_add(qstate_ob, qstate_tmp) == FALSE) return NULL;

    qstate_free(qstate_tmp);
    qstate_tmp = NULL;
  }

  return qstate_ob;
}

int qstate_inner_product(QState* qstate_0, QState* qstate_1,
			 double* real, double* imag)
{
  CTYPE out = 0.0 + 0.0i;
  
  g_Errno = NO_ERROR;

  if ((qstate_0 == NULL) || (qstate_1 == NULL)) goto ERROR_EXIT;
  if (qstate_0->qubit_num != qstate_1->qubit_num) goto ERROR_EXIT;
  if (qstate_0->state_num != qstate_1->state_num) goto ERROR_EXIT;
  
  for (int i=0; i<qstate_0->state_num; i++) {
    out = out + conj(qstate_0->camp[i]) * qstate_1->camp[i];
  }
  *real = creal(out);
  *imag = cimag(out);

  return TRUE;

 ERROR_EXIT:
  g_Errno = ERROR_QSTATE_INNER_PRODUCT;
  return FALSE;
}

int qstate_expect_value(QState* qstate, Observable* observ, double* value)
{
  QState*	qstate_ob = NULL;
  double	real	  = 0.0;
  double	imag	  = 0.0;

  if (qstate == NULL) goto ERROR_EXIT;
  if (observ == NULL) goto ERROR_EXIT;
  
  if (!(qstate_ob = qstate_apply_observable(qstate, observ))) goto ERROR_EXIT;
      
  if (qstate_inner_product(qstate, qstate_ob, &real, &imag) == FALSE)
    goto ERROR_EXIT;
  
  if (fabs(imag) > MIN_DOUBLE) goto ERROR_EXIT;

  qstate_free(qstate_ob);
  qstate_ob = NULL;

  *value = real;

  return TRUE;
  
 ERROR_EXIT:
  g_Errno = ERROR_QSTATE_EXPECT_VALUE;
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
