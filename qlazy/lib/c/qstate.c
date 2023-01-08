/*
 *  qstate.c
 */
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"

#include "qlazy.h"

#define METHOD_0

static void _qstate_set_none(QState* qstate)
{
  int i;
  
  for (i=0; i<qstate->state_num; i++) {
    qstate->buffer_0[i] = 0.0 + 0.0 * COMP_I;
  }
  for (i=0; i<qstate->state_num; i++) {
    qstate->buffer_1[i] = 0.0 + 0.0 * COMP_I;
  }
}

static void _qstate_set_0(QState* qstate)
{
  int i;
  
  for (i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = 0.0 + 0.0 * COMP_I;
  }
  qstate->camp[0] = 1.0 + 0.0 * COMP_I;
}

bool qstate_normalize(QState* qstate)
{
  double	norm = 0.0;
  int		i;
  
  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  for (i=0; i<qstate->state_num; i++) {
    norm += pow(cabs(qstate->camp[i]),2.0);
  }
  norm = sqrt(norm);

  /*
  if (norm == 0.0) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  for (int i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = qstate->camp[i] / norm;
  }
  */

  /* normalization */
  if (norm != 0.0) {
    for (i=0; i<qstate->state_num; i++) {
      qstate->camp[i] = qstate->camp[i] / norm;
    }
  }
  else {
    for (i=0; i<qstate->state_num; i++) {
      qstate->camp[i] = 0.0;
    }
    qstate->camp[0] = 1.0;
  }

  SUC_RETURN(true);
}

static QState* _qstate_mask(QState* qstate_in, int qubit_num, int* qubit_id)
{
  MData*        mdata	    = NULL;	/* temporary in this function */
  QState*       mask_qstate = NULL;
  int           mask_qubit_num;
  int           mask_qubit_id[MAX_QUBIT_NUM];
  int		i,j;

  if (qstate_in == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);;

  /* wave function collapse by mesurement */

  if (qstate_in->qubit_num == qubit_num) {
    if (!(qstate_copy(qstate_in, (void**)&mask_qstate)))
      ERR_RETURN(ERROR_QSTATE_COPY,NULL);
  }
  else {  /* in the case of extracting some qubit states */
    /* mask qstate by measurement */
    if (!(qstate_copy(qstate_in, (void**)&mask_qstate)))
      ERR_RETURN(ERROR_QSTATE_COPY,NULL);
    mask_qubit_num = qstate_in->qubit_num - qubit_num;
    int cnt = 0;
    for (i=0; i<qstate_in->qubit_num; i++) {
      int flg = OFF;
      for (j=0; j<qubit_num; j++) {
	if (i == qubit_id[j]) { flg = ON; break; }
      }
      if (flg == OFF) {
	mask_qubit_id[cnt++] = i;
      }
    }
    if (!(qstate_measure_stats(mask_qstate, 1, 0.0, 0.0, mask_qubit_num,
			       mask_qubit_id, (void**)&mdata)))
      ERR_RETURN(ERROR_QSTATE_MEASURE_STATS,NULL);
  }

  /* free temporal mdata */

  mdata_free(mdata); mdata = NULL;

  SUC_RETURN(mask_qstate);
}

static QState* _qstate_pickup(QState* qstate_in, int qubit_num, int* qubit_id)
{
  QState*	qstate	    = NULL;
  QState*	mask_qstate = NULL;
  int		x;
  int		i;

  if (!(mask_qstate = _qstate_mask(qstate_in, qubit_num, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);

  /* selected qubits state (qstate) */
  if (!(qstate_init(qubit_num, (void**)&qstate, qstate_in->use_gpu)))
    ERR_RETURN(ERROR_QSTATE_INIT,NULL);
  _qstate_set_none(qstate);
  for (i=0; i<mask_qstate->state_num; i++) {
    if (!(select_bits(&x, i, qubit_num, qstate_in->qubit_num, qubit_id)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
    qstate->camp[x] += mask_qstate->camp[i];
  }
  if (!(qstate_normalize(qstate)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);

  qstate_free(mask_qstate); mask_qstate = NULL;

  SUC_RETURN(qstate);
}

#ifdef REMOVE_PHASE_FACTOR

static bool _qstate_remove_phase_factor(QState* qstate, COMPLEX* phase_factor)
{
  COMPLEX	exp_i_phase = 1.0 + 0.0 * COMP_I;
  int		i;

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

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
  for (i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = qstate->camp[i] / exp_i_phase;
  }

  *phase_factor = exp_i_phase;

  SUC_RETURN(true);
}

#endif

static bool _complex_division(COMPLEX a, COMPLEX b, COMPLEX* c)
{
  /* c = a / b */
  COMPLEX	denom;
  double	numer;

  denom = a * conj(b);	                /* denom = a b* */
  numer = cabs(b); numer *= numer;	/* numer = b b* */

  if (fabs(numer) < MIN_DOUBLE) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  *c = denom/numer;

  SUC_RETURN(true);
}

static bool _bloch_get_angle(COMPLEX alpha, COMPLEX beta, double* theta, double* phi)
{
  COMPLEX	b_tmp, c_tmp;
  double	norm;

  /* in the case of north or south pole */
  if (cabs(alpha) < MIN_DOUBLE) {  /* south pole */
    *theta = 1.0;
    *phi = 0.0;
    SUC_RETURN(true);
  }
  else if (cabs(beta) < MIN_DOUBLE) {  /* north pole */
    *theta = 0.0;
    *phi = 0.0;
    SUC_RETURN(true);
  }
    
  /* eliminate phase factor */
  if (!(_complex_division(beta, alpha, &b_tmp)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  alpha = 1.0 + 0.0 * COMP_I;
  beta	= b_tmp;
  
  /* normailzation */
  //  norm = sqrt(1.0 + beta * conj(beta));
  norm = sqrt(1.0 + creal(beta * conj(beta)));
  alpha /= norm;      /* alpha -> positive real, 0.0 <= alpha <= 1.0 */
  beta /= norm;       /* beta  -> complex */

  /* get (theta,phi) from (alpha,beta) */
  *theta = 2.0 * acos(creal(alpha));  /* 0.0 <= theta <= pi */
  if (!(_complex_division((sin(*theta/2.0)+0.0*COMP_I), beta, &c_tmp)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  *phi = -1.0 * carg(c_tmp);

  /* unit transform (unit=pi(radian)) */
  *theta /= M_PI;
  *phi /= M_PI;

  SUC_RETURN(true);
}

bool _qstate_init_cpu(int qubit_num, void** qstate_out)
{
  QState	*qstate = NULL;
  int		 state_num;

  if ((qubit_num < 1) || (qubit_num > MAX_QUBIT_NUM))
    ERR_RETURN(ERROR_OUT_OF_BOUND,false);
  
  if (!(qstate = (QState*)malloc(sizeof(QState))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  qstate->qubit_num = qubit_num;
  state_num = (1 << qubit_num);
  qstate->state_num = state_num;

  qstate->buf_id = 0;

  if (!(qstate->buffer_0 = (COMPLEX*)malloc(sizeof(COMPLEX)*state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  if (!(qstate->buffer_1 = (COMPLEX*)malloc(sizeof(COMPLEX)*state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  qstate->camp = qstate->buffer_0;

  if (!(qstate->prob_array = (double*)malloc(sizeof(double) * state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  qstate->prob_updated = false;

  if (!(gbank_init((void**)&(qstate->gbank))))
      ERR_RETURN(ERROR_GBANK_INIT,false);

  qstate->use_gpu = false;

  _qstate_set_0(qstate);

  *qstate_out = qstate;
  
  SUC_RETURN(true);
}

bool qstate_init(int qubit_num, void** qstate_out, bool use_gpu)
{
  QState	*qstate = NULL;

  if (qubit_num < 1) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (use_gpu == false) {
    if (!(_qstate_init_cpu(qubit_num, (void**)&qstate)))
      ERR_RETURN(ERROR_QSTATE_INIT, false);
  }

#ifdef USE_GPU
  else if (use_gpu == true) {
    if (!(qstate_init_gpu(qubit_num, (void**)&qstate)))
      ERR_RETURN(ERROR_QSTATE_INIT, false);
  }
#endif

  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }

  *qstate_out = qstate;

  SUC_RETURN(true);
}

bool qstate_init_with_vector(double* real, double* imag, int dim, void** qstate_out, bool use_gpu)
{
  QState	*qstate	   = NULL;
  int            state_num = dim;
  int		 qubit_num;
  int		 i;

  if ((real == NULL) || (imag == NULL) || (dim <= 0) || (!(is_power_of_2(dim))))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  qubit_num = (int)log2((double)dim);
  if (!(qstate_init(qubit_num, (void**)&qstate, use_gpu)))
    ERR_RETURN(ERROR_QSTATE_INIT, false);

  for (i=0; i<state_num; i++) {
    qstate->camp[i] = real[i] + 1.0 * COMP_I * imag[i];
  }

#ifdef USE_GPU
  if (!(qstate_update_device_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_DEVICE_MEMORY, false);
#endif

  *qstate_out = qstate;
  
  SUC_RETURN(true);
}

static bool _qstate_copy_host_memory(QState* qstate_in, void** qstate_out)
{
  QState* qstate = NULL;

  if (qstate_in == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(qstate_init(qstate_in->qubit_num, (void**)&qstate, qstate_in->use_gpu)))
    ERR_RETURN(ERROR_QSTATE_INIT,false);

  memcpy(qstate->camp, qstate_in->camp, sizeof(COMPLEX)*qstate_in->state_num);

  *qstate_out = qstate;

  SUC_RETURN(true);
}

bool qstate_copy(QState* qstate_in, void** qstate_out)
{
  QState* qstate = NULL;

  if (qstate_in == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate_in)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, false);
#endif

  if (!(_qstate_copy_host_memory(qstate_in, (void**)&qstate)))
    ERR_RETURN(ERROR_QSTATE_COPY,false);

  
#ifdef USE_GPU
  if (!(qstate_update_device_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_DEVICE_MEMORY, false);
#endif

  *qstate_out = qstate;

  SUC_RETURN(true);
}

bool qstate_reset(QState* qstate_in, int qubit_num, int* qubit_id)
{
  QState*	qstate = NULL;
  int		mask   = 0;
  int           shift  = 0;
  int           idx    = 0;
  int		i,k;
  
  if (qstate_in == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate_in)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY,false);
#endif

  /* copy to temporary qstate */
  if (!(_qstate_copy_host_memory(qstate_in, (void**)&qstate)))
    ERR_RETURN(ERROR_QSTATE_COPY,false);

  /* make mask */
  mask = (1 << qstate_in->qubit_num) - 1;
  for (k=0; k<qubit_num; k++) {
    shift = qstate_in->qubit_num - qubit_id[k] - 1;
    mask = mask ^ (1 << shift);
  }

  /* apply mask operation to qubit index (= reset |0>) */
  for (i=0; i<qstate_in->state_num; i++) {
    qstate_in->camp[i] = 0.0;
  }
  if (qubit_num == qstate_in->qubit_num) {
    qstate_in->camp[0] = 1.0;
  }
  else {
    for (i=0; i<qstate->state_num; i++) {
      idx = i & mask;
      qstate_in->camp[idx] += qstate->camp[i];
    }
  }

  /* normalize the qstate */
  if (!(qstate_normalize(qstate_in)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);

  qstate->prob_updated = false;
  
#ifdef USE_GPU
  if (!(qstate_update_device_memory(qstate_in)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_DEVICE_MEMORY,false);
#endif
  
  /* free temporary qstate */
  qstate_free(qstate); qstate = NULL;
  
  SUC_RETURN(true);
}

bool qstate_get_camp(QState* qstate, int qubit_num, int* qubit_id,
		     void** camp_out)
{
  QState*	mask_qstate = NULL;
  double*	camp	    = NULL;
  int		i;

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, false);
#endif

  if (!(mask_qstate = _qstate_pickup(qstate, qubit_num, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(camp = (double*)malloc(sizeof(double)*2*mask_qstate->state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  for (i=0; i<mask_qstate->state_num; i++) {
    camp[2*i] = creal(mask_qstate->camp[i]);
    camp[2*i+1] = cimag(mask_qstate->camp[i]);
  }

  qstate_free(mask_qstate); mask_qstate = NULL;

  *camp_out = camp;
  
  SUC_RETURN(true);
}

bool qstate_print(QState* qstate_in, int qubit_num, int* qubit_id, bool nonzero)
{
  double	qreal,qimag,prob;
  int		prob_level = 0;
  char		state[MAX_QUBIT_NUM+1];
  int		i,k;

  /* for extracting phase factor */
#ifdef REMOVE_PHASE_FACTOR
  COMPLEX       phase_factor;
#endif

  /* for picking up some qubit id */
  QState*       qstate	    = NULL;	/* temporary in this function */
  MData*        mdata	    = NULL;	/* temporary in this function */

  if (qstate_in == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate_in)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, false);
#endif

  if (!(qstate = _qstate_pickup(qstate_in, qubit_num, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* print qstate */

#ifdef REMOVE_PHASE_FACTOR
  if (!(_qstate_remove_phase_factor(qstate, &phase_factor)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
#ifdef SHOW_PHASE_FACTOR
  if (fabs(cimag(phase_factor)) > MIN_DOUBLE) {
    printf("phase factor = exp(%+.4f*PI*i)\n",carg(phase_factor)/M_PI);
  }
  else if (creal(qstate->camp[0]) < 0.0) {
    printf("phase factor = %+.4f\n",creal(phase_factor));
  }
#endif

#endif
  
  for (i=0; i<qstate->state_num; i++) {
    qreal = creal(qstate->camp[i]);
    qimag = cimag(qstate->camp[i]);

    if (!(binstr_from_decimal(state, qstate->qubit_num, i, ON)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    
    prob = pow(cabs(qstate->camp[i]),2.0);
    if (fabs(prob) < MIN_DOUBLE) prob_level = 0;
    else prob_level = (int)(prob/0.1 + 1.5);
    
    if ((nonzero == false) || (nonzero == true && prob > MIN_DOUBLE)) {
      printf("c[%s] = %+.4f%+.4f*i : %.4f |", state, qreal, qimag, prob);
      for (k=0; k<prob_level; k++) printf("+");
      printf("\n");
    }
  }

  /* free temporal qstate and mdata */

  qstate_free(qstate); qstate = NULL;
  mdata_free(mdata); mdata = NULL;
  
  SUC_RETURN(true);
}

bool qstate_bloch(QState* qstate, int qid, double* theta, double* phi)
{
  int           qubit_num;
  int           qubit_id[MAX_QUBIT_NUM];
  QState*	qstate_tmp = NULL;
  COMPLEX	alpha, beta;
  
  if ((qstate == NULL) || (qid < 0))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, false);
#endif

  /* qstate of qid-th qubit -> qstate_mask */
  qubit_num = 1;
  qubit_id[0] = qid;

  if (!(qstate_tmp = _qstate_pickup(qstate, qubit_num, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* get theta and phi from alpha and beta */
  alpha = qstate_tmp->camp[0];
  beta = qstate_tmp->camp[1];

  if (!(_bloch_get_angle(alpha, beta, theta, phi)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  qstate_free(qstate_tmp);
  qstate_tmp = NULL;
  
  SUC_RETURN(true);
}

bool qstate_print_bloch(QState* qstate, int qid)
{
  double theta, phi;
  
  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, false);
#endif

  if (!(qstate_bloch(qstate, qid, &theta, &phi)))
    ERR_RETURN(ERROR_QSTATE_BLOCH,false);

  printf("theta = %+.4f, phi = %+.4f\n", theta, phi);

  SUC_RETURN(true);
}

#ifdef METHOD_0

static bool _qstate_operate_unitary2(COMPLEX* camp_out, COMPLEX* camp_in, COMPLEX* U2,
				     int qubit_num, int state_num, int n)
{
  int		nn   = qubit_num - n - 1;
  int		i;
  COMPLEX	u_00 = U2[IDX2(0,0)];
  COMPLEX	u_01 = U2[IDX2(0,1)];
  COMPLEX	u_10 = U2[IDX2(1,0)];
  COMPLEX	u_11 = U2[IDX2(1,1)];

# pragma omp parallel for shared(camp_out)
  for (i=0; i<state_num; i++) {
    if ((i >> nn) %2 == 0) {
      camp_out[i]
	= u_00 * camp_in[i]
	+ u_01 * camp_in[i + (1 << nn)];
    }
    else {
      camp_out[i]
	= u_10 * camp_in[i - (1 << nn)]
	+ u_11 * camp_in[i];
    }
  }
  
  SUC_RETURN(true);
}

static bool _qstate_operate_unitary4(COMPLEX* camp_out, COMPLEX* camp_in, COMPLEX* U4,
				     int qubit_num, int state_num, int m, int n)
{
  int		mm   = qubit_num - m - 1;
  int		nn   = qubit_num - n - 1;
  int		i;
  COMPLEX	u_00 = U4[IDX4(0,0)];
  COMPLEX	u_01 = U4[IDX4(0,1)];
  COMPLEX	u_02 = U4[IDX4(0,2)];
  COMPLEX	u_03 = U4[IDX4(0,3)];
  COMPLEX	u_10 = U4[IDX4(1,0)];
  COMPLEX	u_11 = U4[IDX4(1,1)];
  COMPLEX	u_12 = U4[IDX4(1,2)];
  COMPLEX	u_13 = U4[IDX4(1,3)];
  COMPLEX	u_20 = U4[IDX4(2,0)];
  COMPLEX	u_21 = U4[IDX4(2,1)];
  COMPLEX	u_22 = U4[IDX4(2,2)];
  COMPLEX	u_23 = U4[IDX4(2,3)];
  COMPLEX	u_30 = U4[IDX4(3,0)];
  COMPLEX	u_31 = U4[IDX4(3,1)];
  COMPLEX	u_32 = U4[IDX4(3,2)];
  COMPLEX	u_33 = U4[IDX4(3,3)];

# pragma omp parallel for shared(camp_out)
  for (i=0; i<state_num; i++) {
    if (((i >> mm) % 2 == 0) && ((i >> nn) % 2 == 0)) {
      camp_out[i]
	= u_00 * camp_in[i]
	+ u_01 * camp_in[i + (1 << nn)]
	+ u_02 * camp_in[i + (1 << mm)]
	+ u_03 * camp_in[i + (1 << nn) + (1 << mm)];
    }
    else if (((i >> mm) % 2 == 0) && ((i >> nn) % 2 == 1)) {
      camp_out[i]
	= u_10 * camp_in[i - (1 << nn)]
	+ u_11 * camp_in[i]
	+ u_12 * camp_in[i - (1 << nn) + (1 << mm)]
	+ u_13 * camp_in[i + (1 << mm)];
    }
    else if (((i >> mm) % 2 == 1) && ((i >> nn) % 2 == 0)) {
      camp_out[i]
	= u_20 * camp_in[i - (1 << mm)]
	+ u_21 * camp_in[i + (1 << nn) - (1 << mm)]
	+ u_22 * camp_in[i]
	+ u_23 * camp_in[i + (1 << nn)];
    }
    else {
      camp_out[i]
	= u_30 * camp_in[i - (1 << nn) - (1 << mm)]
	+ u_31 * camp_in[i - (1 << mm)]
	+ u_32 * camp_in[i - (1 << nn)]
	+ u_33 * camp_in[i];
    }
  }
  
  SUC_RETURN(true);
}

#endif

#ifdef METHOD_1

static bool _qstate_operate_unitary2(COMPLEX* camp_out, COMPLEX* camp_in, COMPLEX* U2,
				     int qubit_num, int state_num, int n)
{
  int flg[4];  // flag represent whether matrix element is zero or non-zero (0:zero, 1:non-zero)
  int nn = qubit_num - n - 1;

  /* set flags */
  for (int i=0; i<4; i++) {
    if (U2[i] == 0.0) flg[i] = 0;
    else flg[i] = 1;
  }
  
# pragma omp parallel for shared(camp_out)
  for (int i=0; i<state_num; i++) {
    camp_out[i] = 0.0;
    if ((i >> nn) %2 == 0) {
      int a = IDX2(0,0);
      int b = IDX2(0,1);
      if (flg[a] == 1) camp_out[i] += U2[a] * camp_in[i];
      if (flg[b] == 1) camp_out[i] += U2[b] * camp_in[i + (1 << nn)];
    }
    else {
      int a = IDX2(1,0);
      int b = IDX2(1,1);
      if (flg[a] == 1) camp_out[i] += U2[a] * camp_in[i - (1 << nn)];
      if (flg[b] == 1) camp_out[i] += U2[b] * camp_in[i];
    }
  }
  
  SUC_RETURN(true);
}

static bool _qstate_operate_unitary4(COMPLEX* camp_out, COMPLEX* camp_in, COMPLEX* U4,
				     int qubit_num, int state_num, int m, int n)
{
  int flg[16];  // flag represent whether matrix element is zero or non-zero (0:zero, 1:non-zero)
  int mm = qubit_num - m - 1;
  int nn = qubit_num - n - 1;

  /* set flags */
  for (int i=0; i<16; i++) {
    if (U4[i] == 0.0) flg[i] = 0;
    else flg[i] = 1;
  }
  
  # pragma omp parallel for
  for (int i=0; i<state_num; i++) {

    camp_out[i] = 0.0;
    if (((i >> mm) % 2 == 0) && ((i >> nn) % 2 == 0)) {
      int a = IDX4(0,0);
      int b = IDX4(0,1);
      int c = IDX4(0,2);
      int d = IDX4(0,3);
      if (flg[a] == 1) camp_out[i] += U4[a] * camp_in[i];
      if (flg[b] == 1) camp_out[i] += U4[b] * camp_in[i + (1 << nn)];
      if (flg[c] == 1) camp_out[i] += U4[c] * camp_in[i + (1 << mm)];
      if (flg[d] == 1) camp_out[i] += U4[d] * camp_in[i + (1 << nn) + (1 << mm)];
    }
    else if (((i >> mm) % 2 == 0) && ((i >> nn) % 2 == 1)) {
      int a = IDX4(1,0);
      int b = IDX4(1,1);
      int c = IDX4(1,2);
      int d = IDX4(1,3);
      if (flg[a] == 1) camp_out[i] += U4[a] * camp_in[i - (1 << nn)];
      if (flg[b] == 1) camp_out[i] += U4[b] * camp_in[i];
      if (flg[c] == 1) camp_out[i] += U4[c] * camp_in[i - (1 << nn) + (1 << mm)];
      if (flg[c] == 1) camp_out[i] += U4[d] * camp_in[i + (1 << mm)];
    }
    else if (((i >> mm) % 2 == 1) && ((i >> nn) % 2 == 0)) {
      int a = IDX4(2,0);
      int b = IDX4(2,1);
      int c = IDX4(2,2);
      int d = IDX4(2,3);
      if (flg[a] == 1) camp_out[i] += U4[a] * camp_in[i - (1 << mm)];
      if (flg[b] == 1) camp_out[i] += U4[b] * camp_in[i + (1 << nn) - (1 << mm)];
      if (flg[c] == 1) camp_out[i] += U4[c] * camp_in[i];
      if (flg[d] == 1) camp_out[i] += U4[d] * camp_in[i + (1 << nn)];
    }
    else {
      int a = IDX4(3,0);
      int b = IDX4(3,1);
      int c = IDX4(3,2);
      int d = IDX4(3,3);
      if (flg[a] == 1) camp_out[i] += U4[a] * camp_in[i - (1 << nn) - (1 << mm)];
      if (flg[b] == 1) camp_out[i] += U4[b] * camp_in[i - (1 << mm)];
      if (flg[c] == 1) camp_out[i] += U4[c] * camp_in[i - (1 << nn)];
      if (flg[d] == 1) camp_out[i] += U4[d] * camp_in[i];
    }
  }
  
  SUC_RETURN(true);
}

#endif

#ifdef METHOD_2

static bool _qstate_operate_unitary2(COMPLEX* camp_out, COMPLEX* camp_in, COMPLEX* U2,
				     int qubit_num, int state_num, int n)
{
  int nn = qubit_num - n - 1;

# pragma omp parallel for shared(camp_out)
  for (int i=0; i<state_num; i++) {
    int p = (i >> nn) % 2;
    int pp = p ^ 1;
    int sign = (pp << 1) - 1; // b=0 -> -1, b=1 -> +1
    int offset = sign * (1 << nn);
    camp_out[i] = U2[IDX2(p,p)] * camp_in[i] + U2[IDX2(p,pp)] * camp_in[i + offset];
  }
  
  SUC_RETURN(true);
}

static bool _qstate_operate_unitary4(COMPLEX* camp_out, COMPLEX* camp_in, COMPLEX* U4,
				     int qubit_num, int state_num, int m, int n)
{
  int mm = qubit_num - m - 1;
  int nn = qubit_num - n - 1;

# pragma omp parallel for shared(camp_out)
  for (int i=0; i<state_num; i++) {

    int p = (i >> mm) % 2;
    int pp = p ^ 1;
    int q = (i >> nn) % 2;
    int qq = q ^ 1;

    int l = (p << 1) + q;

    int sign_p = (pp << 1) - 1;
    int sign_q = (qq << 1) - 1;

    int off_p = sign_p * (1 << mm);
    int off_q = sign_q * (1 << nn);

    camp_out[i]
      = U4[IDX4(l, l)] * camp_in[i]
      + U4[IDX4(l, (l^1))] * camp_in[i + off_q]
      + U4[IDX4(l, (l^2))] * camp_in[i + off_p]
      + U4[IDX4(l, (l^3))] * camp_in[i + off_q + off_p];
  }
  
  SUC_RETURN(true);
}

#endif

static bool _qstate_operate_controlled_gate_core(COMPLEX* camp_out, COMPLEX* camp_in, COMPLEX* U,
						 int qubit_num, int state_num, int m, int n)
{
  int		mm   = qubit_num - m - 1;
  int		nn   = qubit_num - n - 1;
  int		i;
  COMPLEX	u_00 = U[IDX4(0,0)];
  COMPLEX	u_11 = U[IDX4(1,1)];
  COMPLEX	u_22 = U[IDX4(2,2)];
  COMPLEX	u_23 = U[IDX4(2,3)];
  COMPLEX	u_32 = U[IDX4(3,2)];
  COMPLEX	u_33 = U[IDX4(3,3)];

# pragma omp parallel for shared(camp_out)
  for (i=0; i<state_num; i++) {
    if (((i >> mm) % 2 == 0) && ((i >> nn) % 2 == 0)) {
      camp_out[i] = u_00 * camp_in[i];
    }
    else if (((i >> mm) % 2 == 0) && ((i >> nn) % 2 == 1)) {
      camp_out[i] = u_11 * camp_in[i];
    }
    else if (((i >> mm) % 2 == 1) && ((i >> nn) % 2 == 0)) {
      camp_out[i]
	= u_22 * camp_in[i]
	+ u_23 * camp_in[i + (1 << nn)];
    }
    else {
      camp_out[i]
	= u_32 * camp_in[i - (1 << nn)]
	+ u_33 * camp_in[i];
    }
  }
  
  SUC_RETURN(true);
}

static bool _qstate_operate_controlled_gate_cpu(QState* qstate, COMPLEX* U, int m, int n)
{
  if (qstate == NULL)
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (qstate->buf_id == 0) {
    if (!(_qstate_operate_controlled_gate_core(qstate->buffer_1, qstate->buffer_0, U,
					       qstate->qubit_num, qstate->state_num, m, n))) {
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
    qstate->buf_id = 1;
    qstate->camp = qstate->buffer_1;
  }
  else {
    if (!(_qstate_operate_controlled_gate_core(qstate->buffer_0, qstate->buffer_1, U,
					       qstate->qubit_num, qstate->state_num, m, n))) {
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
    qstate->buf_id = 0;
    qstate->camp = qstate->buffer_0;
  }

  SUC_RETURN(true);
}

static bool _qstate_operate_unitary_cpu(QState* qstate, COMPLEX* U, int dim, int m, int n)
{
  if (qstate == NULL)
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (dim == 2) {

    if (qstate->buf_id == 0) {
      if (!(_qstate_operate_unitary2(qstate->buffer_1, qstate->buffer_0, U,
                                     qstate->qubit_num, qstate->state_num, m))) {
      	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      }
      qstate->buf_id = 1;
      qstate->camp = qstate->buffer_1;
    }
    else {
      if (!(_qstate_operate_unitary2(qstate->buffer_0, qstate->buffer_1, U,
				     qstate->qubit_num, qstate->state_num, m))) {
      	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      }
      qstate->buf_id = 0;
      qstate->camp = qstate->buffer_0;
    }
  }

  else if (dim == 4) {

    if (qstate->buf_id == 0) {
      if (!(_qstate_operate_unitary4(qstate->buffer_1, qstate->buffer_0, U,
				     qstate->qubit_num, qstate->state_num, m, n))) {
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      }
      qstate->buf_id = 1;
      qstate->camp = qstate->buffer_1;
    }
    else {
      if (!(_qstate_operate_unitary4(qstate->buffer_0, qstate->buffer_1, U,
				     qstate->qubit_num, qstate->state_num, m, n))) {
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      }
      qstate->buf_id = 0;
      qstate->camp = qstate->buffer_0;
    }
  }
  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }

  SUC_RETURN(true);
}

static bool _qstate_operate_controlled_gate(QState* qstate, COMPLEX* U, int m, int n)
{
  if (qstate->use_gpu == false) {
    if (!(_qstate_operate_controlled_gate_cpu(qstate, U, m, n)))
      ERR_RETURN(ERROR_QSTATE_OPERATE_UNITARY, false);
  }

#ifdef USE_GPU
  else if (qstate->use_gpu == true) {
    if (!(qstate_operate_controlled_gate_gpu(qstate, U, m, n)))
      ERR_RETURN(ERROR_QSTATE_OPERATE_UNITARY, false);
  }
#endif

  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }
  
  SUC_RETURN(true);
}

static bool _qstate_operate_unitary(QState* qstate, COMPLEX* U, int dim, int m, int n)
{
  if (qstate->use_gpu == false) {
    if (!(_qstate_operate_unitary_cpu(qstate, U, dim, m, n)))
      ERR_RETURN(ERROR_QSTATE_OPERATE_UNITARY, false);
  }

#ifdef USE_GPU
  else if (qstate->use_gpu == true) {
    if (!(qstate_operate_unitary_gpu(qstate, U, dim, m, n)))
      ERR_RETURN(ERROR_QSTATE_OPERATE_UNITARY, false);
  }
#endif

  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }
  
  SUC_RETURN(true);
}

static bool _qstate_transform_basis(QState* qstate, double angle, double phase, int n)
{
  /*
     This function operate U+ to the qstate
     - |p> = U |0> = cos(theta/2) |0> + exp(i phi) sin(theta/2) |1>
     - U = Rz(PI/2 + phi) H Rz(theta) H
     - U+ = H Rz(-theta) H Rz(-PI/2 - phi)
   */
  double	phs = -0.5 - phase;
  double	ang = -angle;
  int		qubit_id[MAX_QUBIT_NUM];

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  qubit_id[0] = n;
  if (!(qstate_operate_qgate(qstate, ROTATION_Z, phs, 0.0, 1.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 1.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(qstate_operate_qgate(qstate, ROTATION_Z, ang, 0.0, 1.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, false);
#endif

  SUC_RETURN(true);
}

static bool _qstate_transform_basis_inv(QState* qstate, double angle, double phase, int n)
{
  /* 
     This function operate U to the qstate
     - |p> = U |0> = cos(theta/2) |0> + exp(i phi) sin(theta/2) |1>
     - U = Rz(PI/2 + phi) H Rz(theta) H
     - U+ = H Rz(-theta) H Rz(-PI/2 - phi)
   */
  double	phs = 0.5 + phase;
  double	ang = angle;
  int		qubit_id[MAX_QUBIT_NUM];

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  qubit_id[0] = n;
  if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 1.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(qstate_operate_qgate(qstate, ROTATION_Z, ang, 0.0, 1.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 1.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(qstate_operate_qgate(qstate, ROTATION_Z, phs, 0.0, 1.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, false);
#endif

  SUC_RETURN(true);
}

static bool _qstate_update_prob_array(QState* qstate)
{
  int		i;
  double	prob;

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  for (i=0; i<qstate->state_num; i++) qstate->prob_array[i] = 0.0;

  qstate->prob_array[0] = 0.0;
  for (i=1; i<qstate->state_num; i++) {
    prob = pow(cabs(qstate->camp[i-1]), 2.0);
    qstate->prob_array[i] = qstate->prob_array[i-1] + prob;
  }

  SUC_RETURN(true);
}

static bool _qstate_get_measured_char(QState* qstate, int mnum, int* qid, char* mchar)
{
  double	r;
  int           i, idx, up;

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (qstate->prob_updated == false) {
    _qstate_update_prob_array(qstate);
    qstate->prob_updated = true;
  }

  r = genrand_real1();
  idx = 0;
  for (i=0; i<qstate->qubit_num; i++) {
    up = 1 << (qstate->qubit_num - 1 - i);
    if (r >= qstate->prob_array[idx + up]) {
      idx = idx + up;
    }
  }

  for (i=0; i<mnum; i++) {
    mchar[i] = (idx >> (qstate->qubit_num - qid[i] - 1)) % 2;
  }

  SUC_RETURN(true);
}

bool qstate_measure(QState* qstate, int mnum, int* qid, char* measured_char,
		    bool measure_update)
{
  int	i, x;
  int   mval_qid = 0;

  if ((qstate == NULL) || (mnum < 1) ||
      (qid == NULL) || (measured_char == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    
#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, false);
#endif

  _qstate_get_measured_char(qstate, mnum, qid, measured_char);

  /* get measured value for target qubits */
  /* update qstate (projection and normalize) */
  if (measure_update == true) {
    for (i=0; i<mnum; i++) {
      mval_qid += ((int)measured_char[i] << (mnum - 1 - i));
    }
    for (i=0; i<qstate->state_num; i++) {
      if (!(select_bits(&x, i, mnum, qstate->qubit_num, qid)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
      if (x != mval_qid) qstate->camp[i] = 0.0;
    }
    if (!(qstate_normalize(qstate))) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

#ifdef USE_GPU
    if (!(qstate_update_device_memory(qstate)))
      ERR_RETURN(ERROR_QSTATE_UPDATE_DEVICE_MEMORY, false);
#endif

    qstate->prob_updated = false;
  }

  SUC_RETURN(true);
}

bool qstate_measure_stats(QState* qstate, int shot_num, double angle, double phase,
			  int qubit_num, int* qubit_id, void** mdata_out)
{
  int		mes_id	       = 0;
  MData*	mdata	       = NULL;
  bool		measure_update = false;
  char*		measured_char  = NULL;
  int		i, j;

  if ((qstate == NULL) ||
      (shot_num < 1) || (qubit_num < 0) ||
      (qubit_num > qstate->qubit_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, false);
#endif

  /* initialize mdata */
  if (!(mdata_init(qubit_num, shot_num, angle, phase, qubit_id,
		   (void**)&mdata))) ERR_RETURN(ERROR_MDATA_INIT,false);

  /* change basis, if measurement axis isn't Z */
  if ((angle != 0.0) || (phase != 0.0)) {
    for (i=0; i<qubit_num; i++) {
      if (!(_qstate_transform_basis(qstate, angle, phase, qubit_id[i])))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,-1);
    }
  }

  /* get measurement data */
  if (!(measured_char = (char*)malloc(sizeof(char) * qstate->qubit_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  for (i=0; i<shot_num; i++) {
    if (i < shot_num - 1) measure_update = false;
    else measure_update = true;

    if (!(qstate_measure(qstate, qubit_num, qubit_id, measured_char, measure_update)))
      ERR_RETURN(ERROR_QSTATE_MEASURE, false);

    mes_id = 0;
    for (j=0; j<qubit_num; j++) {
      mes_id += ((int)measured_char[j] << (qubit_num - j - 1));
    }
    mdata->freq[mes_id]++;
  }
  mdata->last_val = mes_id;

  /* change basis (inverse), if measurement axis isn't Z */
  if ((angle != 0.0) || (phase != 0.0)) {
    for (i=0; i<qubit_num; i++) {
      if (!(_qstate_transform_basis_inv(qstate, angle, phase, qubit_id[i])))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,-1);
    }
  }

#ifdef USE_GPU
  if (!(qstate_update_device_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_DEVICE_MEMORY, false);
#endif

  qstate->prob_updated = false;

  free(measured_char); measured_char = NULL;
  
  *mdata_out = mdata;
  SUC_RETURN(true);
}

bool qstate_measure_bell_stats(QState* qstate, int shot_num, int qubit_num,
			       int* qubit_id, void** mdata_out)
{
  MData*	mdata  = NULL;
  
  if ((qstate == NULL) || (shot_num < 1) || (qubit_num != 2))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* equivalent transform to bell-basis */
  /* CX 0 1 */
  if (!(qstate_operate_qgate(qstate, CONTROLLED_X, 0.0, 0.0, 1.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* H 0 */
  if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 1.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* CX 0 1 */
  if (!(qstate_operate_qgate(qstate, CONTROLLED_X, 0.0, 0.0, 1.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* execute Bell-mesurement */
  if (!(qstate_measure_stats(qstate, shot_num, 0.0, 0.0, qubit_num, qubit_id, (void**)&mdata)))
    ERR_RETURN(ERROR_QSTATE_MEASURE_STATS,false);

  /* equivalent transform to bell-basis (inverse) */
  /* CX 0 1 */
  if (!(qstate_operate_qgate(qstate, CONTROLLED_X, 0.0, 0.0, 1.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* H 0 */
  if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 1.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* CX 0 1 */
  if (!(qstate_operate_qgate(qstate, CONTROLLED_X, 0.0, 0.0, 1.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

#ifdef USE_GPU
  if (!(qstate_update_device_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_DEVICE_MEMORY, false);
#endif

  qstate->prob_updated = false;

  *mdata_out = mdata;
  SUC_RETURN(true);
}

bool qstate_operate_qgate(QState* qstate, Kind kind, double phase, double gphase,
			  double factor, int* qubit_id)
{
  int		q0  = qubit_id[0];
  int		q1  = qubit_id[1];
  int		dim = 0;
  COMPLEX*	U   = NULL;

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if ((kind == INIT) || (kind == MEASURE) || (kind ==MEASURE_X) ||
      (kind == MEASURE_Y) || (kind == MEASURE_Z) || (kind == MEASURE_BELL) ||
      (kind == RESET)) {
    SUC_RETURN(true);
  }

  if (!(gbank_get_unitary(qstate->gbank, kind, phase, gphase, factor, &dim, (void**)&U)))
    ERR_RETURN(ERROR_GBANK_GET_UNITARY,false);
  
  if (kind_is_controlled(kind) == true) {
    if (!(_qstate_operate_controlled_gate(qstate, U, q0, q1)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }
  else {
    if (!(_qstate_operate_unitary(qstate, U, dim, q0, q1)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }

  qstate->prob_updated = false;

  free(U); U = NULL;
  SUC_RETURN(true);
}

static bool _qstate_evolve_spro(QState* qstate, SPro* spro, double time)
{
  int	pre,now;
  int	qubit_id[MAX_QUBIT_NUM];
  
  if ((qstate == NULL) || (spro == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  pre = -1; now = 0;
  while (now < spro->spin_num) {
    /* operate nothing */
    if (spro->spin_type[now] == NONE) {
      now++;
      continue;
    }
    /* operate G: G=H (if PauliX), G=Rx(-0.5) (if PauliY), G=I (if PauliZ) */
    if (spro->spin_type[now] == SIGMA_X) {
      qubit_id[0] = now;
      if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 1.0, qubit_id)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
    else if (spro->spin_type[now] == SIGMA_Y) {
      qubit_id[0] = now;
      if (!(qstate_operate_qgate(qstate, ROTATION_X, -0.5, 0.0, 1.0, qubit_id)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
    else if (spro->spin_type[now] == SIGMA_Z) {
      ;
    }
    else {
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
    /* operate CX */
    if (pre >= 0) {
      if ((spro->spin_type[pre] != NONE) && (spro->spin_type[now] != NONE)) {
	qubit_id[0] = pre;
	qubit_id[1] = now;
	if (!(qstate_operate_qgate(qstate, CONTROLLED_X, 0.0, 0.0, 1.0, qubit_id)))
	  ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      }
    }
    pre = now; now++;
  }
  
  /* operate Rz(-2.0*t) */
  now = spro->spin_num-1;
  qubit_id[0] = now;
  if (!(qstate_operate_qgate(qstate, ROTATION_Z, -2.0*time, 0.0, 1.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

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
	qubit_id[0] = now;
	qubit_id[1] = pre;
	if (!(qstate_operate_qgate(qstate, CONTROLLED_X, 0.0, 0.0, 1.0, qubit_id)))
	  ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      }
    }
    /* operate G+: G+=H (if PauliX), G+=Rx(+0.5) (if PauliY), G+=I (if PauliZ) */
    if (spro->spin_type[pre] == SIGMA_X) {
      qubit_id[0] = pre;
      if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 1.0, qubit_id)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
    else if (spro->spin_type[pre] == SIGMA_Y) {
      qubit_id[0] = pre;
      if (!(qstate_operate_qgate(qstate, ROTATION_X, 0.5, 0.0, 1.0, qubit_id)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
    else if (spro->spin_type[pre] == SIGMA_Z) {
      ;
    }
    else if (spro->spin_type[pre] == NONE) {
      ;
    }
    else {
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
    pre = now; now--;
  }
  
  SUC_RETURN(true);
}

bool qstate_evolve(QState* qstate, ObservableBase* observ, double time, int iter)
{
  double	t = time / iter;
  int		i,j;
  
  if ((qstate == NULL) || (observ == NULL) || (iter < 1))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  for (i=0; i<iter; i++) {
    for (j=0; j<observ->array_num; j++) {
      if (!(_qstate_evolve_spro(qstate, observ->spro_array[j], t)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
  }

  SUC_RETURN(true);
}

static bool _qstate_add(QState* qstate, QState* qstate_add)
{
  int i;

  if ((qstate == NULL) || (qstate_add == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (qstate->state_num != qstate_add->state_num)
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  for (i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = qstate->camp[i] + qstate_add->camp[i];
  }

  qstate->prob_updated = false;

  SUC_RETURN(true);
}

static bool _qstate_mul(QState* qstate, double mul)
{
  int i;
  
  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  for (i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = mul * qstate->camp[i];
  }

  qstate->prob_updated = false;

  SUC_RETURN(true);
}

static QState* _qstate_apply_spro(QState* qstate, SPro* spro)
{
  QState*	qstate_ob = NULL;
  int		qubit_id[MAX_QUBIT_NUM];
  int		i;

  if ((qstate == NULL) || (spro == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT, NULL);

  if (!(qstate_copy(qstate, (void**)&qstate_ob)))
    ERR_RETURN(ERROR_QSTATE_COPY, NULL);

  for (i=0; i<spro->spin_num; i++) {
    qubit_id[0] = i;
    if (spro->spin_type[i] == NONE) {
      ;
    }
    else if (spro->spin_type[i] == SIGMA_X) {
      if (!(qstate_operate_qgate(qstate_ob, PAULI_X, 0.0, 0.0, 1.0, qubit_id))) {
	qstate_free(qstate_ob); qstate_ob = NULL;
	ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
      }
    }
    else if (spro->spin_type[i] == SIGMA_Y) {
      if (!(qstate_operate_qgate(qstate_ob, PAULI_Y, 0.0, 0.0, 1.0, qubit_id))) {
	qstate_free(qstate_ob); qstate_ob = NULL;
	ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
      }
    }
    else if (spro->spin_type[i] == SIGMA_Z) {
      if (!(qstate_operate_qgate(qstate_ob, PAULI_Z, 0.0, 0.0, 1.0, qubit_id))) {
	qstate_free(qstate_ob); qstate_ob = NULL;
	ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
      }
    }
    else {
      qstate_free(qstate_ob); qstate_ob = NULL;
      ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
    }
  }

#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate_ob)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, NULL);
#endif

  if (!(_qstate_mul(qstate_ob, spro->coef))) {
    qstate_free(qstate_ob); qstate_ob = NULL;
    ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
  }
  

  SUC_RETURN(qstate_ob);
}

static QState* _qstate_apply_observable(QState* qstate, ObservableBase* observ)
{
  QState*	qstate_ob  = NULL;
  QState*	qstate_tmp = NULL;
  int		i;

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, NULL);
  
  for (i=0; i<observ->array_num; i++) {
    if (!(qstate_tmp = _qstate_apply_spro(qstate, observ->spro_array[i])))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, NULL);
    if (qstate_ob == NULL) {
      if (!(qstate_init(qstate_tmp->qubit_num, (void**)&qstate_ob, qstate->use_gpu)))
	ERR_RETURN(ERROR_QSTATE_INIT, NULL);
      _qstate_set_none(qstate_ob);
    }
    if (!(_qstate_add(qstate_ob, qstate_tmp)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, NULL);

    qstate_free(qstate_tmp);
    qstate_tmp = NULL;
  }

#ifdef USE_GPU
  if (!(qstate_update_device_memory(qstate_ob)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_DEVICE_MEMORY, NULL);
#endif

  SUC_RETURN(qstate_ob);
}

bool qstate_inner_product(QState* qstate_0, QState* qstate_1,
			  double* real, double* imag)
{
  COMPLEX	out = 0.0 + 0.0 * COMP_I;
  int		i;

  if ((qstate_0 == NULL) || (qstate_1 == NULL) ||
      (qstate_0->qubit_num != qstate_1->qubit_num) ||
      (qstate_0->state_num != qstate_1->state_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate_0)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY,false);
  if (!(qstate_update_host_memory(qstate_1)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY,false);
#endif

  for (i=0; i<qstate_0->state_num; i++) {
    out = out + conj(qstate_0->camp[i]) * qstate_1->camp[i];
  }
  *real = creal(out);
  *imag = cimag(out);

  SUC_RETURN(true);
}

bool qstate_tensor_product(QState* qstate_0, QState* qstate_1, void** qstate_out)
{
  int		qubit_num;
  QState*	qstate = NULL;
  int		i,j;

  if ((qstate_0 == NULL) || (qstate_1 == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (qstate_0->use_gpu != qstate_1->use_gpu)
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate_0)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, false);
  if (!(qstate_update_host_memory(qstate_1)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, false);
#endif

  qubit_num = qstate_0->qubit_num + qstate_1->qubit_num;
  if (!(qstate_init(qubit_num, (void**)&qstate, qstate_0->use_gpu)))
    ERR_RETURN(ERROR_QSTATE_INIT, false);

  int cnt = 0;
  for (i=0; i<qstate_0->state_num; i++) {
    for (j=0; j<qstate_1->state_num; j++) {
      qstate->camp[cnt++] = qstate_0->camp[i] * qstate_1->camp[j];
    }
  }

#ifdef USE_GPU
  if (!(qstate_update_device_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_DEVICE_MEMORY, false);
#endif

  *qstate_out = qstate;

  SUC_RETURN(true);
}

bool qstate_expect_value(QState* qstate, ObservableBase* observ, double* value)
{
  QState*	qstate_ob = NULL;
  double	real	  = 0.0;
  double	imag	  = 0.0;

  if ((qstate == NULL) || (observ == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, false);
#endif
  
  if (!(qstate_ob = _qstate_apply_observable(qstate, observ)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      
#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate_ob)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, false);
#endif

  if (!(qstate_inner_product(qstate, qstate_ob, &real, &imag)))
    ERR_RETURN(ERROR_QSTATE_INNER_PRODUCT,false);
  
  if (fabs(imag) > MIN_DOUBLE) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  qstate_free(qstate_ob);
  qstate_ob = NULL;

  *value = real;

  SUC_RETURN(true);
}

bool qstate_apply_matrix(QState* qstate, int qnum_part, int* qid,
			 double* real, double *imag, int row, int col)
{
  QState*	qstate_tmp = NULL;
  int*		index	   = NULL;
  int*		inv_index  = NULL;
  COMPLEX	coef	   = 0.0 + 0.0 * COMP_I;
  int		shift	   = 0;
  int           N	   = 0;
  int		ii,iii,jj,jjj;
  int           i,k,n;

  if ((qstate == NULL) || (real == NULL) || (imag == NULL) ||
      (qstate->state_num < row) || (1<<qnum_part != row) || (row != col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

#ifdef USE_GPU
  if (!(qstate_update_host_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY,false);
#endif

  if (!(_qstate_copy_host_memory(qstate, (void**)&qstate_tmp)))
    ERR_RETURN(ERROR_QSTATE_COPY,false);

  index = bit_permutation_array(qstate->state_num, qstate->qubit_num, qnum_part, qid);

  if (!(inv_index = (int*)malloc(sizeof(int)*qstate->state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  for (n=0; n<qstate->state_num; n++) inv_index[index[n]] = n; 

  shift = qstate->qubit_num-qnum_part;
  N = 1<<(qstate->qubit_num-shift);
  
  for (i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = 0.0 + 0.0 * COMP_I;
    ii = index[i]>>shift;
    iii = index[i]%(1<<shift);

    for (k=0; k<N; k++) {
      int j = inv_index[(k<<shift)+iii];
      jj = index[j]>>shift;
      jjj = index[j]%(1<<shift);
      coef = real[ii*col+jj] + 1.0 * COMP_I * imag[ii*col+jj];
      qstate->camp[i] += (coef * qstate_tmp->camp[j]);
    }
  }

#ifdef USE_GPU
  if (!(qstate_update_device_memory(qstate)))
    ERR_RETURN(ERROR_QSTATE_UPDATE_DEVICE_MEMORY,false);
#endif

  free(index); index = NULL;
  free(inv_index); inv_index = NULL;
  qstate_free(qstate_tmp); qstate_tmp = NULL;

  qstate->prob_updated = false;

  SUC_RETURN(true);
}

static bool _qstate_operate_qcirc_cpu(QState* qstate, CMem* cmem, QCirc* qcirc,
				      bool measure_update)
/* one shot execution */
{
  QGate*        qgate = NULL;   /* quantum gate in quantum circuit */
  int		dim   = 0;
  int           q0    = -1;
  int           q1    = -1;
  COMPLEX*	U     = NULL;
  bool          compo = false;  /* U is composite or not */
  int		mnum  = 0;
  int*		qid   = NULL;
  int*		cid   = NULL;
  bool		last  = false;
  char*		measured_char = NULL;
  int i;

  /* error check */
  if ((qstate == NULL || qcirc == NULL) ||
      (qstate->qubit_num < qcirc->qubit_num) ||
      (cmem != NULL && cmem->cmem_num < qcirc->cmem_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* malloc */
  if (cmem != NULL) {
    if (!(cid = (int*)malloc(sizeof(int) * cmem->cmem_num)))
      ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

    if (!(measured_char = (char*)malloc(sizeof(int) * cmem->cmem_num)))
      ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
  }
  if (!(qid = (int*)malloc(sizeof(int) * qstate->qubit_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  /* execute quantum circuit */
  qgate = qcirc->first;
  while (qgate != NULL) {

    if ((qgate->ctrl == -1) ||
	((qgate->ctrl != -1) && (cmem->bit_array[qgate->ctrl] == 1))) {

      /* unitary gate */
      if (kind_is_unitary(qgate->kind) == true) {

	if (!(qgate_get_next_unitary((void**)&qgate, qstate->gbank, &dim, &q0, &q1, (void**)&U, &compo))) {
	  ERR_RETURN(ERROR_QGATE_GET_NEXT_UNITARY, false);
	}

	/* operate unitary matrix */
	if (compo == false && kind_is_controlled(qgate->kind) == true) {
	  if (!(_qstate_operate_controlled_gate(qstate, U, q0, q1))) {
	    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
	  }
	}
	else {
	  if (!(_qstate_operate_unitary(qstate, U, dim, q0, q1))) {
	    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
	  }
	}
	free(U); U = NULL;
	
	qgate = qgate->next;
      }
      /* reset */
      else if (kind_is_reset(qgate->kind) == true) {
	if (!(qstate_reset(qstate, 1, qgate->qid)))
	  ERR_RETURN(ERROR_CANT_RESET, false);
	qgate = qgate->next;
      }
      /* measurement */
      else if (kind_is_measurement(qgate->kind) == true) {

	if (!(qgate_get_measurement_attributes((void**)&qgate, qstate->gbank, &mnum, qid, cid, &last))) {
	  ERR_RETURN(ERROR_QGATE_GET_NEXT_UNITARY, false);
	}
	if (!(qstate_measure(qstate, mnum, qid, measured_char, measure_update)))
	  ERR_RETURN(ERROR_QSTATE_MEASURE, false);
	for (i=0; i<mnum; i++) {
	  cmem->bit_array[cid[i]] = measured_char[i];
	}
	qgate = qgate->next;
      }
      else {
	ERR_RETURN(ERROR_QSTATE_OPERATE_QCIRC, false);
      }
    }
    else {
      qgate = qgate->next;
    }
  }

  /* free */
  if (cmem != NULL) {
    free(cid); cid = NULL;
    free(measured_char); measured_char = NULL;
  }
  free(qid); qid = NULL;

  qstate->prob_updated = false;

  SUC_RETURN(true);
}

bool qstate_operate_qcirc(QState* qstate, CMem* cmem, QCirc* qcirc, int shots, char* mchar_shots,
			  bool out_state)
/* shots times execution */
{
  int		i, j, k;
  QCirc*	qcirc_uonly    = NULL;
  QCirc*	qcirc_mixed    = NULL;
  QCirc*	qcirc_monly    = NULL;
  QState*	qstate_tmp     = NULL;
  bool		measure_update = true;
  QGate*        qgate	       = NULL;
  int		mnum	       = 0;
  int*		qid	       = NULL;
  int*		cid	       = NULL;
  bool		last	       = false;
  char*		measured_char  = NULL;

  if (!(qcirc_decompose(qcirc, (void**)&qcirc_uonly, (void**)&qcirc_mixed, (void**)&qcirc_monly)))
    ERR_RETURN(ERROR_QCIRC_DECOMPOSE, false);
  
  if (qstate->use_gpu == false) {

    if (qcirc_uonly != NULL) { /* unitary only */
      measure_update = true; /* not efficient because of including no measurements */
      if (!(_qstate_operate_qcirc_cpu(qstate, cmem, qcirc_uonly, measure_update)))
	ERR_RETURN(ERROR_QSTATE_OPERATE_QCIRC, false);
      qcirc_free(qcirc_uonly); qcirc_uonly = NULL;
    }
    
    if (qcirc_mixed != NULL) { /* unitary and non-unitary mixed */
      measure_update = true;
      for (i=0; i<shots-1; i++) {
	if (!(qstate_copy(qstate, (void**)&qstate_tmp)))
	  ERR_RETURN(ERROR_QSTATE_COPY, false);
	if (!(_qstate_operate_qcirc_cpu(qstate_tmp, cmem, qcirc_mixed, measure_update)))
	  ERR_RETURN(ERROR_QSTATE_OPERATE_QCIRC, false);
	for (j=0; j<cmem->cmem_num; j++) {
	  mchar_shots[i * cmem->cmem_num + j] = cmem->bit_array[j];
	}
	qstate_free(qstate_tmp); qstate_tmp = NULL;
      }
      if (!(_qstate_operate_qcirc_cpu(qstate, cmem, qcirc_mixed, measure_update)))
	ERR_RETURN(ERROR_QSTATE_OPERATE_QCIRC, false);
      for (j=0; j<cmem->cmem_num; j++) {
	mchar_shots[(shots - 1) * cmem->cmem_num + j] = cmem->bit_array[j];
      }
      qcirc_free(qcirc_mixed); qcirc_mixed = NULL;
    }
    
    else if (qcirc_monly != NULL) { /* measurement only */

      if (!(measured_char = (char*)malloc(sizeof(char) * qstate->qubit_num)))
	ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
      if (!(cid = (int*)malloc(sizeof(int) * cmem->cmem_num)))
	ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
      if (!(qid = (int*)malloc(sizeof(int) * qstate->qubit_num)))
	ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

      qgate = qcirc_monly->first;
      if (!(qgate_get_measurement_attributes((void**)&qgate, qstate->gbank, &mnum, qid, cid, &last))) {
	ERR_RETURN(ERROR_QGATE_GET_NEXT_UNITARY, false);
      }

      measure_update = false;
      for (i=0; i<shots; i++) {
	if (out_state == false || i < shots - 1) measure_update = false;
	else measure_update = false;

	if (!(qstate_measure(qstate, mnum, qid, measured_char, measure_update)))
	  ERR_RETURN(ERROR_QSTATE_MEASURE, false);
	for (k=0; k<mnum; k++) {
	  cmem->bit_array[cid[k]] = measured_char[k];
	}
	for (j=0; j<cmem->cmem_num; j++) {
	  mchar_shots[i * cmem->cmem_num + j] = cmem->bit_array[j];
	}
      }

      free(cid); cid = NULL;
      free(measured_char); measured_char = NULL;
      free(qid); qid = NULL;

      qcirc_free(qcirc_monly); qcirc_monly = NULL;
    }
  }

#ifdef USE_GPU
  else if (qstate->use_gpu == true) {

    if (qcirc_uonly != NULL) { /* unitary only */
      measure_update = true; /* not efficient because of including no measurements */
      if (!(qstate_operate_qcirc_gpu(qstate, cmem, qcirc_uonly, measure_update)))
	ERR_RETURN(ERROR_QSTATE_OPERATE_QCIRC, false);
      qcirc_free(qcirc_uonly); qcirc_uonly = NULL;
    }

    if (qcirc_mixed != NULL) { /* unitary and non-unitary mixed */
      measure_update = true;
      for (i=0; i<shots-1; i++) {
	if (!(qstate_copy(qstate, (void**)&qstate_tmp)))
	  ERR_RETURN(ERROR_QSTATE_COPY, false);
	if (!(qstate_operate_qcirc_gpu(qstate_tmp, cmem, qcirc_mixed, measure_update)))
	  ERR_RETURN(ERROR_QSTATE_OPERATE_QCIRC, false);
	for (j=0; j<cmem->cmem_num; j++) {
	  mchar_shots[i * cmem->cmem_num + j] = cmem->bit_array[j];
	}
	qstate_free(qstate_tmp); qstate_tmp = NULL;
      }
      if (!(qstate_operate_qcirc_gpu(qstate, cmem, qcirc_mixed, measure_update)))
	ERR_RETURN(ERROR_QSTATE_OPERATE_QCIRC, false);
      for (j=0; j<cmem->cmem_num; j++) {
	mchar_shots[(shots - 1) * cmem->cmem_num + j] = cmem->bit_array[j];
      }
      qcirc_free(qcirc_mixed); qcirc_mixed = NULL;
    }

    else if (qcirc_monly != NULL) { /* measurement only */
      /* shots times meaurements */
      if (!(qstate_operate_measure_gpu(qstate, cmem, qcirc_monly, shots, mchar_shots, out_state)))
	ERR_RETURN(ERROR_QSTATE_OPERATE_MEASURE, false);
      qcirc_free(qcirc_monly); qcirc_monly = NULL;
    }
  }
#endif

  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }
    
  qstate->prob_updated = false;

  SUC_RETURN(true);
}

static void _qstate_free_cpu(QState* qstate)
{
  if (qstate == NULL) return;
  
  if (qstate->buffer_0 != NULL) {
    free(qstate->buffer_0); qstate->buffer_0 = NULL;
  }
  if (qstate->buffer_1 != NULL) {
    free(qstate->buffer_1); qstate->buffer_1 = NULL;
  }
  if (qstate->gbank != NULL) {
    free(qstate->gbank); qstate->gbank = NULL;
  }
  free(qstate);
}

void qstate_free(QState* qstate)
{
  if (qstate->use_gpu == false) {
    _qstate_free_cpu(qstate);
  }

#ifdef USE_GPU
  else if (qstate->use_gpu == true) {
    qstate_free_gpu(qstate);
  }
#endif

  else {
    return;
  }
}
