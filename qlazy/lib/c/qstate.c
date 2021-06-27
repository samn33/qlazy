/*
 *  qstate.c
 */
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"

#include "qlazy.h"

#define METHOD_0

static bool _select_bits(int* bits_out, int bits_in, int digits_out, int digits_in,
			int digit_array[MAX_QUBIT_NUM])
{
  /*
    [description]
    - bits_out:     after selecting bits (ex: '01') <- output of this function
    - bits_in:      before selecting bits = whole bits (ex: '111010')
    - digits_out:   number of output digits (ex: 2)
    - digits_in:    number of whole digits (ex: 6)
    - digits_array: qubits array you want to output (ex: {3,4})
   */
  
  if ((digits_in < 1) || (digits_in > MAX_QUBIT_NUM) ||
      (digits_out < 1) || (digits_out > MAX_QUBIT_NUM) || (bits_in < 0))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  int bits = 0;
  int count = 0;
  for (int i=digits_out-1; i>=0; i--) {
    if (digit_array[i] >= digits_in) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    bits += (((bits_in>>(digits_in-1-digit_array[i]))%2) << count);
    count++;
  }
  
  *bits_out = bits;
  
  SUC_RETURN(true);
}

static void _qstate_set_none(QState* qstate)
{
  for (int i=0; i<qstate->state_num; i++) {
    qstate->buffer_0[i] = 0.0 + 0.0i;
  }
  for (int i=0; i<qstate->state_num; i++) {
    qstate->buffer_1[i] = 0.0 + 0.0i;
  }
}

static void _qstate_set_0(QState* qstate)
{
  for (int i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = 0.0 + 0.0i;
  }
  qstate->camp[0] = 1.0 + 0.0i;
}

static bool _qstate_normalize(QState* qstate)
{
  double	norm	    = 0.0;
  
  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  for (int i=0; i<qstate->state_num; i++) {
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
    for (int i=0; i<qstate->state_num; i++) {
      qstate->camp[i] = qstate->camp[i] / norm;
    }
  }
  else {
    for (int i=0; i<qstate->state_num; i++) {
      qstate->camp[i] = 0.0;
    }
    qstate->camp[0] = 1.0;
  }

  SUC_RETURN(true);
}

static QState* _qstate_mask(QState* qstate_in, int qubit_num, int qubit_id[MAX_QUBIT_NUM])
{
  MData*        mdata	    = NULL;	/* temporary in this function */
  QState*       mask_qstate = NULL;
  int           mask_qubit_num;
  int           mask_qubit_id[MAX_QUBIT_NUM];

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
    for (int i=0; i<qstate_in->qubit_num; i++) {
      int flg = OFF;
      for (int j=0; j<qubit_num; j++) {
	if (i == qubit_id[j]) { flg = ON; break; }
      }
      if (flg == OFF) {
	mask_qubit_id[cnt++] = i;
      }
    }
    if (!(qstate_measure(mask_qstate, 1, 0.0, 0.0, mask_qubit_num,
			 mask_qubit_id, (void**)&mdata)))
      ERR_RETURN(ERROR_QSTATE_MEASURE,NULL);
  }

  /* free temporal mdata */

  mdata_free(mdata); mdata = NULL;

  SUC_RETURN(mask_qstate);
}

static QState* _qstate_pickup(QState* qstate_in, int qubit_num, int qubit_id[MAX_QUBIT_NUM])
{
  QState*	qstate	    = NULL;
  QState*	mask_qstate = NULL;
  int		x;

  if (!(mask_qstate = _qstate_mask(qstate_in, qubit_num, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);

  /* selected qubits state (qstate) */
  if (!(qstate_init(qubit_num, (void**)&qstate)))
    ERR_RETURN(ERROR_QSTATE_INIT,NULL);
  _qstate_set_none(qstate);
  for (int i=0; i<mask_qstate->state_num; i++) {
    if (!(_select_bits(&x, i, qubit_num, qstate_in->qubit_num, qubit_id)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
    qstate->camp[x] += mask_qstate->camp[i];
  }
  if (!(_qstate_normalize(qstate)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);

  qstate_free(mask_qstate); mask_qstate = NULL;

  SUC_RETURN(qstate);
}

#ifdef REMOVE_PHASE_FACTOR

static bool _qstate_remove_phase_factor(QState* qstate, COMPLEX* phase_factor)
{
  COMPLEX exp_i_phase = 1.0 + 0.0i;

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
  for (int i=0; i<qstate->state_num; i++) {
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
  alpha = 1.0 + 0.0j;
  beta	= b_tmp;
  
  /* normailzation */
  norm = sqrt(1.0 + beta * conj(beta));
  alpha /= norm;      /* alpha -> positive real, 0.0 <= alpha <= 1.0 */
  beta /= norm;       /* beta  -> complex */

  /* get (theta,phi) from (alpha,beta) */
  *theta = 2.0 * acos(creal(alpha));  /* 0.0 <= theta <= pi */
  if (!(_complex_division((sin(*theta/2.0)+0.0j), beta, &c_tmp)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  *phi = -1.0 * carg(c_tmp);

  /* unit transform (unit=pi(radian)) */
  *theta /= M_PI;
  *phi /= M_PI;

  SUC_RETURN(true);
}

bool qstate_init(int qubit_num, void** qstate_out)
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

  if (!(gbank_init((void**)&(qstate->gbank))))
      ERR_RETURN(ERROR_GBANK_INIT,false);

  _qstate_set_0(qstate);

  *qstate_out = qstate;
  
  SUC_RETURN(true);
}

bool qstate_init_with_vector(double* real, double* imag, int dim, void** qstate_out)
{
  QState	*qstate = NULL;
  int            state_num = dim;
  int		 qubit_num;

  if ((real == NULL) || (imag == NULL) || (dim <= 0) || (!(is_power_of_2(dim))))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  qubit_num = log2(dim);
  if (!(qstate_init(qubit_num, (void**)&qstate)))
    ERR_RETURN(ERROR_QSTATE_INIT,false);

  for (int i=0; i<state_num; i++)
    qstate->camp[i] = real[i] + 1.0i * imag[i];

  *qstate_out = qstate;
  
  SUC_RETURN(true);
}

bool qstate_reset(QState* qstate_in, int qubit_num, int qubit_id[MAX_QUBIT_NUM])
{
  QState*	qstate = NULL;
  int		mask   = 0;
  int           shift  = 0;
  int           idx    = 0;
  
  if (qstate_in == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* copy to temporary qstate */
  if (!(qstate_copy(qstate_in, (void**)&qstate)))
    ERR_RETURN(ERROR_QSTATE_COPY,false);

  /* make mask */
  mask = (1 << qstate_in->qubit_num) - 1;
  for (int k=0; k<qubit_num; k++) {
    shift = qstate_in->qubit_num - qubit_id[k] - 1;
    mask = mask ^ (1 << shift);
  }

  /* apply mask operation to qubit index (= reset |0>) */
  for (int i=0; i<qstate_in->state_num; i++) {
    qstate_in->camp[i] = 0.0;
  }
  if (qubit_num == qstate_in->qubit_num) {
    qstate_in->camp[0] = 1.0;
  }
  else {
    for (int i=0; i<qstate->state_num; i++) {
      idx = i & mask;
      qstate_in->camp[idx] += qstate->camp[i];
    }
  }

  /* normalize the qstate */
  if (!(_qstate_normalize(qstate_in)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);

  /* free temporary qstate */
  qstate_free(qstate); qstate = NULL;
  
  SUC_RETURN(true);
}

bool qstate_copy(QState* qstate_in, void** qstate_out)
{
  QState* qstate = NULL;

  if (qstate_in == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(qstate_init(qstate_in->qubit_num, (void**)&qstate)))
    ERR_RETURN(ERROR_QSTATE_INIT,false);

  memcpy(qstate->camp, qstate_in->camp, sizeof(COMPLEX)*qstate_in->state_num);

  *qstate_out = qstate;

  SUC_RETURN(true);
}

bool qstate_get_camp(QState* qstate, int qubit_num, int qubit_id[MAX_QUBIT_NUM],
		     void** camp_out)
{
  QState*	mask_qstate = NULL;
  double*	camp	    = NULL;

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(mask_qstate = _qstate_pickup(qstate, qubit_num, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(camp = (double*)malloc(sizeof(double)*2*mask_qstate->state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  for (int i=0; i<mask_qstate->state_num; i++) {
    camp[2*i] = creal(mask_qstate->camp[i]);
    camp[2*i+1] = cimag(mask_qstate->camp[i]);
  }

  qstate_free(mask_qstate); mask_qstate = NULL;

  *camp_out = camp;
  
  SUC_RETURN(true);
}

bool qstate_print(QState* qstate_in, int qubit_num, int qubit_id[MAX_QUBIT_NUM], bool nonzero)
{
  double	qreal,qimag,prob;
  int		prob_level = 0;
  char		state[MAX_QUBIT_NUM+1];

  /* for extracting phase factor */
#ifdef REMOVE_PHASE_FACTOR
  COMPLEX       phase_factor;
#endif

  /* for picking up some qubit id */
  QState*       qstate	    = NULL;	/* temporary in this function */
  MData*        mdata	    = NULL;	/* temporary in this function */

  if (qstate_in == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

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
  
  for (int i=0; i<qstate->state_num; i++) {
    qreal = creal(qstate->camp[i]);
    qimag = cimag(qstate->camp[i]);

    if (!(binstr_from_decimal(state, qstate->qubit_num, i, ON)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    
    prob = pow(cabs(qstate->camp[i]),2.0);
    if (fabs(prob) < MIN_DOUBLE) prob_level = 0;
    else prob_level = (int)(prob/0.1 + 1.5);
    
    if ((nonzero == false) || (nonzero == true && prob > MIN_DOUBLE)) {
      printf("c[%s] = %+.4f%+.4f*i : %.4f |", state, qreal, qimag, prob);
      for (int k=0; k<prob_level; k++) printf("+");
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

  if (!(qstate_bloch(qstate, qid, &theta, &phi)))
    ERR_RETURN(ERROR_QSTATE_BLOCH,false);

  printf("theta = %+.4f, phi = %+.4f\n", theta, phi);

  SUC_RETURN(true);
}

#ifdef METHOD_0

static bool _qstate_operate_unitary2(COMPLEX* camp_out, COMPLEX* camp_in, COMPLEX* U2,
				     int qubit_num, int state_num, int n)
{
  int nn = qubit_num - n - 1;
  COMPLEX u_00 = U2[IDX2(0,0)];
  COMPLEX u_01 = U2[IDX2(0,1)];
  COMPLEX u_10 = U2[IDX2(1,0)];
  COMPLEX u_11 = U2[IDX2(1,1)];

  # pragma omp parallel for
  for (int i=0; i<state_num; i++) {
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
  int mm = qubit_num - m - 1;
  int nn = qubit_num - n - 1;
  COMPLEX u_00 = U4[IDX4(0,0)];
  COMPLEX u_01 = U4[IDX4(0,1)];
  COMPLEX u_02 = U4[IDX4(0,2)];
  COMPLEX u_03 = U4[IDX4(0,3)];
  COMPLEX u_10 = U4[IDX4(1,0)];
  COMPLEX u_11 = U4[IDX4(1,1)];
  COMPLEX u_12 = U4[IDX4(1,2)];
  COMPLEX u_13 = U4[IDX4(1,3)];
  COMPLEX u_20 = U4[IDX4(2,0)];
  COMPLEX u_21 = U4[IDX4(2,1)];
  COMPLEX u_22 = U4[IDX4(2,2)];
  COMPLEX u_23 = U4[IDX4(2,3)];
  COMPLEX u_30 = U4[IDX4(3,0)];
  COMPLEX u_31 = U4[IDX4(3,1)];
  COMPLEX u_32 = U4[IDX4(3,2)];
  COMPLEX u_33 = U4[IDX4(3,3)];

  # pragma omp parallel for
  for (int i=0; i<state_num; i++) {
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
  
  # pragma omp parallel for
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

  # pragma omp parallel for
  for (int i=0; i<state_num; i++) {
    int p = (i >> nn) % 2;
    int pp = p ^ 1;
    int sign = (pp << 1) - 1; // b=0 -> -1, b=1 -> +1 (bを2倍して1を引く)
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

  # pragma omp parallel for
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

static bool _qstate_operate_unitary(QState* qstate, COMPLEX* U, int dim, int m, int n)
{
  if ((qstate == NULL) || (dim < 0))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (dim == 2) {

    if (qstate->buf_id == 0) {
      if (!(_qstate_operate_unitary2(qstate->buffer_1, qstate->buffer_0, U,
				     qstate->qubit_num, qstate->state_num, m)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      qstate->buf_id = 1;
      qstate->camp = qstate->buffer_1;
    }
    else {
      if (!(_qstate_operate_unitary2(qstate->buffer_0, qstate->buffer_1, U,
				     qstate->qubit_num, qstate->state_num, m)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      qstate->buf_id = 0;
      qstate->camp = qstate->buffer_0;
    }
  }

  else if (dim == 4) {

    if (qstate->buf_id == 0) {
      if (!(_qstate_operate_unitary4(qstate->buffer_1, qstate->buffer_0, U,
				     qstate->qubit_num, qstate->state_num, m, n)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      qstate->buf_id = 1;
      qstate->camp = qstate->buffer_1;
    }
    else {
      if (!(_qstate_operate_unitary4(qstate->buffer_0, qstate->buffer_1, U,
				     qstate->qubit_num, qstate->state_num, m, n)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      qstate->buf_id = 0;
      qstate->camp = qstate->buffer_0;
    }
  }
  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
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
  if (!(qstate_operate_qgate(qstate, ROTATION_Z, phs, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(qstate_operate_qgate(qstate, ROTATION_Z, ang, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

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
  if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(qstate_operate_qgate(qstate, ROTATION_Z, ang, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(qstate_operate_qgate(qstate, ROTATION_Z, phs, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  SUC_RETURN(true);
}

static int _qstate_measure_one_time_without_change_state(QState* qstate_in, double angle,
							 double phase, int qubit_num,
							 int qubit_id[MAX_QUBIT_NUM])
{
  double	r      = rand()/(double)RAND_MAX;
  double	prob_s = 0.0;
  double	prob_e = 0.0;
  int		value  = qstate_in->state_num - 1;
  QState*	qstate = NULL;

  if (qstate_in == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,-1);
  
  /* copy qstate for measurement */
  if (!(qstate_copy(qstate_in, (void**)&qstate)))
    ERR_RETURN(ERROR_QSTATE_COPY,-1);

  /* unitary transform, if measuremment base is not {|0><0|,|1><1|} */
  if ((angle != 0.0) || (phase != 0.0)) {
    for (int i=0; i<qubit_num; i++) {
      if (!(_qstate_transform_basis(qstate, angle, phase, qubit_id[i])))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,-1);
    }
  }

  for (int i=0; i<qstate->state_num; i++) {
    prob_s = prob_e;
    prob_e += pow(cabs(qstate->camp[i]),2.0);
    if (r >= prob_s && r < prob_e) value = i;
  }

  qstate_free(qstate);

  SUC_RETURN(value);
}

static int _qstate_measure_one_time(QState* qstate, double angle, double phase,
				    int qubit_num, int qubit_id[MAX_QUBIT_NUM])
{
  double	r      = rand()/(double)RAND_MAX;
  double	prob_s = 0.0;
  double	prob_e = 0.0;
  int		value  = qstate->state_num - 1;
  int mes_id,x;

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,-1);

  /* change basis, if measurement axis isn't Z */
  if ((angle != 0.0) || (phase != 0.0)) {
    for (int i=0; i<qubit_num; i++) {
      if (!(_qstate_transform_basis(qstate, angle, phase, qubit_id[i])))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,-1);
    }
  }

  for (int i=0; i<qstate->state_num; i++) {
    prob_s = prob_e;
    prob_e += pow(cabs(qstate->camp[i]),2.0);
    if (r >= prob_s && r < prob_e) value = i;
  }

  /* update quantum state by measurement (projection,normalize and change basis) */

  /* projection*/
  if (!(_select_bits(&mes_id, value, qubit_num, qstate->qubit_num, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,-1);
  for (int i=0; i<qstate->state_num; i++) {
    if (!(_select_bits(&x, i, qubit_num, qstate->qubit_num, qubit_id)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,-1);
    if (x != mes_id) qstate->camp[i] = 0.0;
  }
  /* normalize */
  if (!(_qstate_normalize(qstate))) ERR_RETURN(ERROR_INVALID_ARGUMENT,-1);
  /* change basis (inverse), if measurement axis isn't Z */
  if ((angle != 0.0) || (phase != 0.0)) {
    for (int i=0; i<qubit_num; i++) {
      if (!(_qstate_transform_basis_inv(qstate, angle, phase, qubit_id[i])))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,-1);
    }
  }
  
  SUC_RETURN(value);
}

bool qstate_measure(QState* qstate, int shot_num, double angle, double phase,
		    int qubit_num, int qubit_id[MAX_QUBIT_NUM], void** mdata_out)
{
  int		state_id;
  int		mes_id;
  int		mes_num = (1<<qubit_num);
  MData*	mdata	= NULL;

  if ((qstate == NULL) ||
      (shot_num < 1) || (qubit_num < 0) ||
      (qubit_num > qstate->qubit_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* measure all bits, if no parameter set */
  if (qubit_num == 0) {
    qubit_num = qstate->qubit_num;
    mes_num = (1<<qubit_num);
    for (int i=0; i<qstate->qubit_num; i++) {
      qubit_id[i] = i;
    }
  }

  /* initialize mdata */
  if (!(mdata_init(qubit_num, mes_num, shot_num, angle, phase, qubit_id,
		   (void**)&mdata))) ERR_RETURN(ERROR_MDATA_INIT,false);

  /* execute mesurement */
  for (int i=0; i<shot_num; i++) {
    if (i == shot_num - 1) {  /* if last measurement -> change state */
      state_id = _qstate_measure_one_time(qstate, angle, phase, qubit_num, qubit_id);
    }
    else {  /* if not last measurement -> not change state */
      state_id = _qstate_measure_one_time_without_change_state(qstate, angle, phase,
							       qubit_num, qubit_id);
    }
    if (!(_select_bits(&mes_id, state_id, qubit_num, qstate->qubit_num, qubit_id)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    mdata->freq[mes_id]++;
  }
  mdata->last = mes_id;

  *mdata_out = mdata;
  SUC_RETURN(true);
}

bool qstate_measure_bell(QState* qstate, int shot_num, int qubit_num,
			 int qubit_id[MAX_QUBIT_NUM], void** mdata_out)
{
  MData*	mdata  = NULL;
  
  if ((qstate == NULL) || (shot_num < 1) || (qubit_num != 2))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* equivalent transform to bell-basis */
  /* CX 0 1 */
  if (!(qstate_operate_qgate(qstate, CONTROLLED_X, 0.0, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* H 0 */
  if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* CX 0 1 */
  if (!(qstate_operate_qgate(qstate, CONTROLLED_X, 0.0, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* execute Bell-mesurement */
  if (!(qstate_measure(qstate, shot_num, 0.0, 0.0, qubit_num, qubit_id, (void**)&mdata)))
    ERR_RETURN(ERROR_QSTATE_MEASURE,false);

  /* equivalent transform to bell-basis (inverse) */
  /* CX 0 1 */
  if (!(qstate_operate_qgate(qstate, CONTROLLED_X, 0.0, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* H 0 */
  if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* CX 0 1 */
  if (!(qstate_operate_qgate(qstate, CONTROLLED_X, 0.0, 0.0, 0.0, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  *mdata_out = mdata;
  SUC_RETURN(true);
}

bool qstate_operate_qgate(QState* qstate, Kind kind, double alpha, double beta,
			  double gamma, int qubit_id[MAX_QUBIT_NUM])
{
  int		q0  = qubit_id[0];
  int		q1  = qubit_id[1];
  int		dim = 0;
  COMPLEX*	U   = NULL;

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if ((kind == INIT) || (kind ==MEASURE) || (kind ==MEASURE_X) ||
      (kind == MEASURE_Y) || (kind == MEASURE_Z) || (kind == MEASURE_BELL))
    SUC_RETURN(true);
  else {
    if (!(gbank_get_unitary(qstate->gbank, kind, alpha, beta, gamma, &dim, (void**)&U)))
      ERR_RETURN(ERROR_GBANK_GET_UNITARY,false);
#ifdef TEST_NEW_VERSION
    if (!(_qstate_operate_unitary_new(qstate, U, dim, q0, q1)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
#else
    if (!(_qstate_operate_unitary(qstate, U, dim, q0, q1)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
#endif
    free(U); U = NULL;
    SUC_RETURN(true);
  }
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
      if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 0.0, qubit_id)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
    else if (spro->spin_type[now] == SIGMA_Y) {
      qubit_id[0] = now;
      if (!(qstate_operate_qgate(qstate, ROTATION_X, -0.5, 0.0, 0.0, qubit_id)))
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
	if (!(qstate_operate_qgate(qstate, CONTROLLED_X, 0.0, 0.0, 0.0, qubit_id)))
	  ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      }
    }
    pre = now; now++;
  }
  
  /* operate Rz(-2.0*t) */
  now = spro->spin_num-1;
  qubit_id[0] = now;
  if (!(qstate_operate_qgate(qstate, ROTATION_Z, -2.0*time, 0.0, 0.0, qubit_id)))
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
	if (!(qstate_operate_qgate(qstate, CONTROLLED_X, 0.0, 0.0, 0.0, qubit_id)))
	  ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      }
    }
    /* operate G+: G+=H (if PauliX), G+=Rx(+0.5) (if PauliY), G+=I (if PauliZ) */
    if (spro->spin_type[pre] == SIGMA_X) {
      qubit_id[0] = pre;
      if (!(qstate_operate_qgate(qstate, HADAMARD, 0.0, 0.0, 0.0, qubit_id)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
    else if (spro->spin_type[pre] == SIGMA_Y) {
      qubit_id[0] = pre;
      if (!(qstate_operate_qgate(qstate, ROTATION_X, 0.5, 0.0, 0.0, qubit_id)))
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

bool qstate_evolve(QState* qstate, Observable* observ, double time, int iter)
{
  double t = time / iter;
  
  if ((qstate == NULL) || (observ == NULL) || (iter < 1))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  for (int i=0; i<iter; i++) {
    for (int j=0; j<observ->array_num; j++) {
      if (!(_qstate_evolve_spro(qstate, observ->spro_array[j], t)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
  }

  SUC_RETURN(true);
}

static bool _qstate_add(QState* qstate, QState* qstate_add)
{
  if ((qstate == NULL) || (qstate_add == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (qstate->state_num != qstate_add->state_num)
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  for (int i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = qstate->camp[i] + qstate_add->camp[i];
  }

  SUC_RETURN(true);
}

static bool _qstate_mul(QState* qstate, double mul)
{
  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  for (int i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = mul * qstate->camp[i];
  }

  SUC_RETURN(true);
}

static QState* _qstate_apply_spro(QState* qstate, SPro* spro)
{
  QState*	qstate_ob = NULL;
  int		qubit_id[MAX_QUBIT_NUM];

  if ((qstate == NULL) || (spro == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(qstate_copy(qstate, (void**)&qstate_ob)))
    ERR_RETURN(ERROR_QSTATE_COPY,NULL);

  for (int i=0; i<spro->spin_num; i++) {
    qubit_id[0] = i;
    if (spro->spin_type[i] == NONE) {
      ;
    }
    else if (spro->spin_type[i] == SIGMA_X) {
      if (!(qstate_operate_qgate(qstate_ob, PAULI_X, 0.0, 0.0, 0.0, qubit_id))) {
	qstate_free(qstate_ob); qstate_ob = NULL;
	ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
      }
    }
    else if (spro->spin_type[i] == SIGMA_Y) {
      if (!(qstate_operate_qgate(qstate_ob, PAULI_Y, 0.0, 0.0, 0.0, qubit_id))) {
	qstate_free(qstate_ob); qstate_ob = NULL;
	ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
      }
    }
    else if (spro->spin_type[i] == SIGMA_Z) {
      if (!(qstate_operate_qgate(qstate_ob, PAULI_Z, 0.0, 0.0, 0.0, qubit_id))) {
	qstate_free(qstate_ob); qstate_ob = NULL;
	ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
      }
    }
    else {
      qstate_free(qstate_ob); qstate_ob = NULL;
      ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
    }
  }

  if (!(_qstate_mul(qstate_ob, spro->coef))) {
    qstate_free(qstate_ob); qstate_ob = NULL;
    ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
  }
  
  SUC_RETURN(qstate_ob);
}

static QState* _qstate_apply_observable(QState* qstate, Observable* observ)
{
  QState* qstate_ob = NULL;
  QState* qstate_tmp = NULL;

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
  
  for (int i=0; i<observ->array_num; i++) {
    if (!(qstate_tmp = _qstate_apply_spro(qstate, observ->spro_array[i])))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
    if (qstate_ob == NULL) {
      if (!(qstate_init(qstate_tmp->qubit_num, (void**)&qstate_ob)))
	ERR_RETURN(ERROR_QSTATE_INIT,NULL);
      _qstate_set_none(qstate_ob);
    }
    if (!(_qstate_add(qstate_ob, qstate_tmp)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);

    qstate_free(qstate_tmp);
    qstate_tmp = NULL;
  }

  SUC_RETURN(qstate_ob);
}

bool qstate_inner_product(QState* qstate_0, QState* qstate_1,
			  double* real, double* imag)
{
  COMPLEX out = 0.0 + 0.0i;

  if ((qstate_0 == NULL) || (qstate_1 == NULL) ||
      (qstate_0->qubit_num != qstate_1->qubit_num) ||
      (qstate_0->state_num != qstate_1->state_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  for (int i=0; i<qstate_0->state_num; i++) {
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

  if ((qstate_0 == NULL) || (qstate_1 == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  qubit_num = qstate_0->qubit_num + qstate_1->qubit_num;
  if (!(qstate_init(qubit_num, (void**)&qstate)))
    ERR_RETURN(ERROR_QSTATE_INIT,false);

  int cnt = 0;
  for (int i=0; i<qstate_0->state_num; i++) {
    for (int j=0; j<qstate_1->state_num; j++) {
      qstate->camp[cnt++] = qstate_0->camp[i] * qstate_1->camp[j];
    }
  }

  *qstate_out = qstate;

  SUC_RETURN(true);
}

bool qstate_expect_value(QState* qstate, Observable* observ, double* value)
{
  QState*	qstate_ob = NULL;
  double	real	  = 0.0;
  double	imag	  = 0.0;

  if ((qstate == NULL) || (observ == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  if (!(qstate_ob = _qstate_apply_observable(qstate, observ)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      
  if (!(qstate_inner_product(qstate, qstate_ob, &real, &imag)))
    ERR_RETURN(ERROR_QSTATE_INNER_PRODUCT,false);
  
  if (fabs(imag) > MIN_DOUBLE) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  qstate_free(qstate_ob);
  qstate_ob = NULL;

  *value = real;

  SUC_RETURN(true);
}

bool qstate_apply_matrix(QState* qstate, int qnum_part, int qid[MAX_QUBIT_NUM],
			 double* real, double *imag, int row, int col)
{
  QState*	qstate_tmp = NULL;
  int*		index	   = NULL;
  int*		inv_index  = NULL;
  COMPLEX	coef	   = 0.0 + 0.0i;
  int		shift	   = 0;
  int           N	   = 0;
  int		ii,iii,jj,jjj;

  if ((qstate == NULL) || (real == NULL) || (imag == NULL) ||
      (qstate->state_num < row) || (1<<qnum_part != row) || (row != col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(qstate_copy(qstate, (void**)&qstate_tmp)))
    ERR_RETURN(ERROR_QSTATE_COPY,false);

  index = bit_permutation_array(qstate->state_num, qstate->qubit_num, qnum_part, qid);

  if (!(inv_index = (int*)malloc(sizeof(int)*qstate->state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  for (int n=0; n<qstate->state_num; n++) inv_index[index[n]] = n; 

  shift = qstate->qubit_num-qnum_part;
  N = 1<<(qstate->qubit_num-shift);
  
  for (int i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = 0.0 + 0.0i;
    ii = index[i]>>shift;
    iii = index[i]%(1<<shift);

    for (int k=0; k<N; k++) {
      int j = inv_index[(k<<shift)+iii];
      jj = index[j]>>shift;
      jjj = index[j]%(1<<shift);
      coef = real[ii*col+jj] + 1.0i * imag[ii*col+jj];
      qstate->camp[i] += (coef * qstate_tmp->camp[j]);
    }
  }

  free(index); index = NULL;
  free(inv_index); inv_index = NULL;
  qstate_free(qstate_tmp); qstate_tmp = NULL;

  SUC_RETURN(true);
}

bool qstate_operate_qcirc(QState* qstate, CMem* cmem, QCirc* qcirc, int shots, void** mdata_out)
{
  QGate*        qgate                   = NULL;   /* quantum gate in quantum circuit */
  QState*       qstate_tmp              = NULL;   /* quantum state (temporary) */
  CMem*         cmem_tmp                = NULL;   /* classical register (temporary) */
  int*          freq                    = NULL;   /* array for storing measurement frequency */
  bool		ugate_after_measurement = false;  /* exist unitary gate after measurement */
  bool		last_measurements	= false;  /* exist last measurements */
  double        angle                   = 0.0;    /* measurement angle */
  double        phase                   = 0.0;    /* measurement phase */
  int		meas_num                = 0;      /* measurement qubit number */
  int*		meas_qid		= NULL;   /* measurement qubit id */
  int           operation_gate_num      = 0;      /* number of gates without last measurements */
  MData*	mdata			= NULL;   /* output measurement data */

  /* error check */
  if ((qstate == NULL || qcirc == NULL) ||
      (qstate->qubit_num < qcirc->qubit_num) ||
      (cmem->cmem_num < qcirc->cmem_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  /* exist some mesurements before last measurements or not */
  /* (set 'ugate_after_measurement' true or false)        */
  qgate = qcirc->first;
  Kind kind_pre = NOT_A_GATE;
  ugate_after_measurement = false;
  while (qgate != NULL) {
    Kind kind_now = qgate->kind;
    if ((kind_is_measurement(kind_pre) == true) && (kind_is_unitary(kind_now) == true)) {
      ugate_after_measurement = true;
      break;
    }
    qgate = qgate->next;
    kind_pre = kind_now;
  }

  /* number of last measurements */
  meas_num = 0;
  qgate = qcirc->last;
  while (qgate != NULL && kind_is_measurement(qgate->kind) == true) {
    meas_num++;
    last_measurements = true;
    qgate = qgate->prev;
  }
  operation_gate_num = qcirc->gate_num - meas_num;

  /* set measurement qubit id */
  if (!(meas_qid = (int*)malloc(sizeof(int) * meas_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  qgate = qcirc->last;
  int cnt = meas_num;
  while (qgate != NULL && kind_is_measurement(qgate->kind) == true) {
    meas_qid[--cnt] = qgate->qid[0];
    qgate = qgate->prev;
  }
  
  /* 
     operate quantum gates 
  */
  if (ugate_after_measurement == true) {  /* exist some mesurements before last measurements */

    /* allocate memory for storing measurement frequency */
    int state_num = (int)pow(2.0, meas_num);
    if (!(freq = (int*)malloc(sizeof(int) * state_num)))
      ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
    for (int i=0; i<state_num; i++) freq[i] = 0;

    /* execute the quantum circuit iteratively */
    for (int n=0; n<shots; n++) {

      /* initial quantum state */
      if (!(qstate_copy(qstate, (void**)&qstate_tmp)))
	ERR_RETURN(ERROR_QSTATE_COPY,NULL);

      /* initial classical register */
      if (!(cmem_copy(cmem, (void**)&cmem_tmp)))
	ERR_RETURN(ERROR_CMEM_COPY,NULL);

      /* operations before last measurements */
      qgate = qcirc->first;
      for (int i=0; i<operation_gate_num; i++) {

	if ((qgate->ctrl == -1) ||
	    ((qgate->ctrl != -1) && (cmem_tmp->bit_array[qgate->ctrl] == 1))) {

	  if (kind_is_measurement(qgate->kind) == true) {  /* mesurement */
	    if (qgate->kind == MEASURE_X) { angle = 0.5; phase = 0.0; }
	    else if (qgate->kind == MEASURE_Y) { angle = 0.5; phase = 0.5; }
	    else { angle = phase = 0.0; }
	    if (!(qstate_measure(qstate_tmp, 1, angle, phase, 1, qgate->qid, (void**)&mdata)))
	      ERR_RETURN(ERROR_QSTATE_MEASURE, false);
	    if (qgate->c != -1) cmem_tmp->bit_array[qgate->c] = mdata->last;  /* measured value is stored to classical register */
	    mdata_free(mdata); mdata = NULL;
	  }
	  else {  /* unitary gate */
	    if (!(qstate_operate_qgate(qstate_tmp, qgate->kind, qgate->para[0], qgate->para[1], qgate->para[2], qgate->qid)))
	      ERR_RETURN(ERROR_QSTATE_OPERATE_QGATE, false);
	  }
	}
	qgate = qgate->next;
      }

      /* last measurements */
      if (operation_gate_num != qcirc->gate_num) {
	if (qgate->kind == MEASURE_X) { angle = 0.5; phase = 0.0; }
	else if (qgate->kind == MEASURE_Y) { angle = 0.5; phase = 0.5; }
	else { angle = phase = 0.0; }
	if (!(qstate_measure(qstate, 1, angle, phase, meas_num, meas_qid, (void**)&mdata)))
	  ERR_RETURN(ERROR_QSTATE_MEASURE, false);
	freq[mdata->last] += 1;
      }

      /* this time is last or not */
      if (n < shots - 1) {  /* not last */
	qstate_free(qstate_tmp); qstate_tmp = NULL;
	cmem_free(cmem_tmp); cmem_tmp = NULL;
      }
      else {  /* last */
	memcpy(qstate->buffer_0, qstate_tmp->buffer_0, sizeof(COMPLEX) * qstate->state_num);
	memcpy(qstate->buffer_1, qstate_tmp->buffer_1, sizeof(COMPLEX) * qstate->state_num);
	qstate_free(qstate_tmp); qstate_tmp = NULL;
      }
    }

    if (operation_gate_num != qcirc->gate_num) {
      free(mdata->freq);
      mdata->freq = freq;
    }
    else {
      free(freq);
      mdata_free(mdata); mdata = NULL;
    }
  }
  
  else {  /* exist some mesurements before last measurements */

    /* operations before last measurements */
    qgate = qcirc->first;
    for (int i=0; i<operation_gate_num; i++) {
      if ((qgate->ctrl == -1) || ((qgate->ctrl != -1) && (cmem->bit_array[qgate->ctrl] == 1))) {
	if (!(qstate_operate_qgate(qstate, qgate->kind, qgate->para[0], qgate->para[1], qgate->para[2], qgate->qid)))
	  ERR_RETURN(ERROR_QSTATE_OPERATE_QGATE, false);
	qgate = qgate->next;
      }
    }

    /* last measurements */
    if (operation_gate_num != qcirc->gate_num) {
      if (qgate->kind == MEASURE_X) { angle = 0.5; phase = 0.0; }
      else if (qgate->kind == MEASURE_Y) { angle = 0.5; phase = 0.5; }
      else { angle = phase = 0.0; }
      if (!(qstate_measure(qstate, shots, angle, phase, meas_num, meas_qid, (void**)&mdata)))
	ERR_RETURN(ERROR_QSTATE_MEASURE, false);
    }
  }

  free(meas_qid); meas_qid = NULL;

  *mdata_out = mdata;
  
  SUC_RETURN(true);
}

void qstate_free(QState* qstate)
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
