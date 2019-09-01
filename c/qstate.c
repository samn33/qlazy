/*
 *  qstate.c
 */

#include "qlazy.h"

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
    qstate->camp[i] = 0.0 + 0.0i;
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

  if (norm == 0.0) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* normalization */
  for (int i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = qstate->camp[i] / norm;
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

  if (!(qstate->camp = (COMPLEX*)malloc(sizeof(COMPLEX)*state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  if (!(gbank_init((void**)&(qstate->gbank))))
      ERR_RETURN(ERROR_GBANK_INIT,false);

  _qstate_set_0(qstate);

  *qstate_out = qstate;
  
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

  if (!(mask_qstate = _qstate_mask(qstate, qubit_num, qubit_id)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(camp = (double*)malloc(sizeof(double)*2*mask_qstate->state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  for (int i=0; i<mask_qstate->state_num; i++) {
    camp[2*i] = creal(qstate->camp[i]);
    camp[2*i+1] = cimag(qstate->camp[i]);
  }

  qstate_free(mask_qstate); mask_qstate = NULL;

  *camp_out = camp;
  
  SUC_RETURN(true);
}

bool qstate_print(QState* qstate_in, int qubit_num, int qubit_id[MAX_QUBIT_NUM])
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
    
    printf("c[%s] = %+.4f%+.4f*i : %.4f |", state, qreal, qimag, prob);
    for (int k=0; k<prob_level; k++) printf("+");
    printf("\n");
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

static bool _qstate_operate_qgate_1(QState* qstate, Kind kind, int n)
{
  int i;
  QState* qstate_tmp = NULL;
  int nn = qstate->qubit_num - n - 1;
  COMPLEX* U = NULL;

  if (!(gbank_get(qstate->gbank, kind, (void**)&U)))
      ERR_RETURN(ERROR_GBANK_GET,false);

  if ((qstate == NULL) || (nn < 0) || (nn >= qstate->qubit_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  if (!(qstate_init(qstate->qubit_num, (void**)&qstate_tmp)))
    ERR_RETURN(ERROR_QSTATE_INIT,false);
  
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
  memcpy(qstate->camp, qstate_tmp->camp, sizeof(COMPLEX)*qstate->state_num);
  qstate_free(qstate_tmp); qstate_tmp = NULL;

  SUC_RETURN(true);
}

static bool _qstate_operate_qgate_1_rot(QState* qstate, Axis axis, double phase,
					double unit, int n)
{
  int		i;
  QState*	qstate_tmp = NULL;
  int		nn	   = qstate->qubit_num - n - 1;
  COMPLEX*	U	   = NULL;

  if ((qstate == NULL) || (nn < 0) || (nn >= qstate->qubit_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  /* set rotation matrix aroud the X,Y,Z-axis*/
  if (!(gbank_get_rotation(axis, phase, unit, (void**)&U)))
    ERR_RETURN(ERROR_GBANK_GET_ROTATION,false);

  if (!(qstate_init(qstate->qubit_num, (void**)&qstate_tmp)))
    ERR_RETURN(ERROR_QSTATE_INIT,false);
  
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
  memcpy(qstate->camp, qstate_tmp->camp, sizeof(COMPLEX)*qstate->state_num);
  qstate_free(qstate_tmp); qstate_tmp = NULL;

  free(U); U = NULL;

  SUC_RETURN(true);
}

static bool _qstate_operate_qgate_1_phase_shift(QState* qstate, double phase,
						double unit, int n)
{
  int		i;
  QState*	qstate_tmp = NULL;
  int		nn	   = qstate->qubit_num - n - 1;
  COMPLEX*	U	   = NULL;

  if ((qstate == NULL) || (nn < 0) || (nn >= qstate->qubit_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  if (!(gbank_get_phase_shift(phase, unit, (void**)&U)))
    ERR_RETURN(ERROR_GBANK_GET_ROTATION,false);

  if (!(qstate_init(qstate->qubit_num, (void**)&qstate_tmp)))
    ERR_RETURN(ERROR_QSTATE_INIT,false);
  
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
  memcpy(qstate->camp, qstate_tmp->camp, sizeof(COMPLEX)*qstate->state_num);
  qstate_free(qstate_tmp); qstate_tmp = NULL;

  free(U); U = NULL;

  SUC_RETURN(true);
}

static bool _qstate_operate_qgate_2(QState* qstate, Kind kind, int m, int n)
{
  int i;
  QState* qstate_tmp = NULL;
  int mm = qstate->qubit_num - m - 1;
  int nn = qstate->qubit_num - n - 1;
  COMPLEX* U = NULL;

  if (!(gbank_get(qstate->gbank, kind, (void**)&U)))
    ERR_RETURN(ERROR_GBANK_GET,false);

  if ((qstate == NULL) ||
      (m < 0) || (m >= qstate->qubit_num) ||
      (n < 0) || (n >= qstate->qubit_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  if (!(qstate_init(qstate->qubit_num, (void**)&qstate_tmp)))
    ERR_RETURN(ERROR_QSTATE_INIT,false);
  
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
  memcpy(qstate->camp, qstate_tmp->camp, sizeof(COMPLEX)*qstate->state_num);
  qstate_free(qstate_tmp); qstate_tmp = NULL;

  SUC_RETURN(true);
}

static bool _qstate_operate_qgate_2_ctr_rot(QState* qstate, Axis axis, double phase,
					    double unit, int m, int n)
{
  int i;
  QState* qstate_tmp = NULL;
  int mm = qstate->qubit_num - m - 1;
  int nn = qstate->qubit_num - n - 1;
  COMPLEX* U = NULL;

  if (!(gbank_get_ctr_rotation(axis, phase, unit, (void**)&U)))
    ERR_RETURN(ERROR_GBANK_GET,false);

  if ((qstate == NULL) ||
      (m < 0) || (m >= qstate->qubit_num) ||
      (n < 0) || (n >= qstate->qubit_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  if (!(qstate_init(qstate->qubit_num, (void**)&qstate_tmp)))
    ERR_RETURN(ERROR_QSTATE_INIT,false);
  
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
  memcpy(qstate->camp, qstate_tmp->camp, sizeof(COMPLEX)*qstate->state_num);
  qstate_free(qstate_tmp); qstate_tmp = NULL;

  SUC_RETURN(true);
}

static bool _qstate_operate_qgate_2_ctr_phase_shift(QState* qstate, double phase,
						    double unit, int m, int n)
{
  int i;
  QState* qstate_tmp = NULL;
  int mm = qstate->qubit_num - m - 1;
  int nn = qstate->qubit_num - n - 1;
  COMPLEX* U = NULL;

  if (!(gbank_get_ctr_phase_shift(phase, unit, (void**)&U)))
    ERR_RETURN(ERROR_GBANK_GET,false);

  if ((qstate == NULL) ||
      (m < 0) || (m >= qstate->qubit_num) ||
      (n < 0) || (n >= qstate->qubit_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  if (!(qstate_init(qstate->qubit_num, (void**)&qstate_tmp)))
    ERR_RETURN(ERROR_QSTATE_INIT,false);
  
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
  memcpy(qstate->camp, qstate_tmp->camp, sizeof(COMPLEX)*qstate->state_num);
  qstate_free(qstate_tmp); qstate_tmp = NULL;

  SUC_RETURN(true);
}

static bool _qstate_operate_qgate_3_ccx(QState* qstate, int q0, int q1, int q2)
/* CCX = toffoli gate */
{
  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  /* H 2 */
  if (!(_qstate_operate_qgate_1(qstate, HADAMARD, q2)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* CX 1 2 */
  if (!(_qstate_operate_qgate_2(qstate, CONTROLLED_X, q1, q2)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* T+ 2 */
  if (!(_qstate_operate_qgate_1(qstate, PHASE_SHIFT_T_, q2)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* CX 0 2 */
  if (!(_qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q2)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* T 2 */
  if (!(_qstate_operate_qgate_1(qstate, PHASE_SHIFT_T, q2)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* CX 1 2 */
  if (!(_qstate_operate_qgate_2(qstate, CONTROLLED_X, q1, q2)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* T+ 2 */
  if (!(_qstate_operate_qgate_1(qstate, PHASE_SHIFT_T_, q2)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* CX 0 2 */
  if (!(_qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q2)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* T 1 */
  if (!(_qstate_operate_qgate_1(qstate, PHASE_SHIFT_T, q1)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* T 2 */
  if (!(_qstate_operate_qgate_1(qstate, PHASE_SHIFT_T, q2)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* H 2 */
  if (!(_qstate_operate_qgate_1(qstate, HADAMARD, q2)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* CX 0 1 */
  if (!(_qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q1)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* T 0 */
  if (!(_qstate_operate_qgate_1(qstate, PHASE_SHIFT_T, q0)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* T+ 1 */
  if (!(_qstate_operate_qgate_1(qstate, PHASE_SHIFT_T_, q1)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* CX 0 1 */
  if (!(_qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q1)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

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
  double phs = -0.5 - phase;
  double ang = -angle;

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  if (!(_qstate_operate_qgate_1_rot(qstate, Z_AXIS, phs, M_PI, n)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(_qstate_operate_qgate_1(qstate, HADAMARD, n)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(_qstate_operate_qgate_1_rot(qstate, Z_AXIS, ang, M_PI, n)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(_qstate_operate_qgate_1(qstate, HADAMARD, n)))
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
  double phs = 0.5 + phase;
  double ang = angle;

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  if (!(_qstate_operate_qgate_1(qstate, HADAMARD, n)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(_qstate_operate_qgate_1_rot(qstate, Z_AXIS, ang, M_PI, n)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(_qstate_operate_qgate_1(qstate, HADAMARD, n)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!(_qstate_operate_qgate_1_rot(qstate, Z_AXIS, phs, M_PI, n)))
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
  int		q0     = qubit_id[0];
  int		q1     = qubit_id[1];
  
  if ((qstate == NULL) || (shot_num < 1) || (qubit_num != 2))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* equivalent transform to bell-basis */
  /* CX 0 1 */
  if (!(_qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q1)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* H 0 */
  if (!(_qstate_operate_qgate_1(qstate, HADAMARD, q0)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* CX 0 1 */
  if (!(_qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q1)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* execute Bell-mesurement */
  if (!(qstate_measure(qstate, shot_num, 0.0, 0.0, qubit_num, qubit_id, (void**)&mdata)))
    ERR_RETURN(ERROR_QSTATE_MEASURE,false);

  /* equivalent transform to bell-basis (inverse) */
  /* CX 0 1 */
  if (!(_qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q1)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* H 0 */
  if (!(_qstate_operate_qgate_1(qstate, HADAMARD, q0)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  /* CX 0 1 */
  if (!(_qstate_operate_qgate_2(qstate, CONTROLLED_X, q0, q1)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  *mdata_out = mdata;
  SUC_RETURN(true);
}

bool qstate_operate_qgate_param(QState* qstate, Kind kind, double phase,
				int qubit_id[MAX_QUBIT_NUM])
{
  int q0 = qubit_id[0];
  int q1 = qubit_id[1];
  int q2 = qubit_id[2];

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
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
    if (!(_qstate_operate_qgate_1(qstate, kind, q0)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    break;
  case ROTATION_X:
    if (!(_qstate_operate_qgate_1_rot(qstate, X_AXIS, phase, M_PI, q0)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    break;
  case ROTATION_Y:
    if (!(_qstate_operate_qgate_1_rot(qstate, Y_AXIS, phase, M_PI, q0)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    break;
  case ROTATION_Z:
    if (!(_qstate_operate_qgate_1_rot(qstate, Z_AXIS, phase, M_PI, q0)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    break;
  case PHASE_SHIFT:
    if (!(_qstate_operate_qgate_1_phase_shift(qstate, phase, M_PI, q0)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    break;
  case CONTROLLED_X:
  case CONTROLLED_Y:
  case CONTROLLED_Z:
  case CONTROLLED_XR:
  case CONTROLLED_XR_:
  case CONTROLLED_H:
  case CONTROLLED_S:
  case CONTROLLED_S_:
  case CONTROLLED_T:
  case CONTROLLED_T_:
    if (!(_qstate_operate_qgate_2(qstate, kind, q0, q1)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    break;
  case CONTROLLED_RX:
    if (!(_qstate_operate_qgate_2_ctr_rot(qstate, X_AXIS, phase, M_PI, q0, q1)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    break;
  case CONTROLLED_RY:
    if (!(_qstate_operate_qgate_2_ctr_rot(qstate, Y_AXIS, phase, M_PI, q0, q1)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    break;
  case CONTROLLED_RZ:
    if (!(_qstate_operate_qgate_2_ctr_rot(qstate, Z_AXIS, phase, M_PI, q0, q1)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    break;
  case CONTROLLED_P:
    if (!(_qstate_operate_qgate_2_ctr_phase_shift(qstate, phase, M_PI, q0, q1)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    break;
  case TOFFOLI:
    if (!(_qstate_operate_qgate_3_ccx(qstate, q0, q1, q2)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    break;
  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }
  
  SUC_RETURN(true);
}

bool qstate_operate_qgate(QState* qstate, QGate* qgate)
{
  Kind		kind	     = qgate->kind;
  Para*         para	     = &(qgate->para);
  int           terminal_num = qgate->terminal_num;
  int*          qubit_id     = qgate->qubit_id;
  MData*	mdata	     = NULL;
  
  if ((qstate == NULL) || (qgate == NULL))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  switch (kind) {
  case INIT:
    break;
  case MEASURE:
  case MEASURE_X:
  case MEASURE_Y:
  case MEASURE_Z:
    if (!(qstate_measure(qstate, para->mes.shots,
			 para->mes.angle, para->mes.phase, terminal_num,
			 qubit_id, (void**)&mdata)))
      ERR_RETURN(ERROR_QSTATE_MEASURE,false);
    mdata_print(mdata);
    mdata_free(mdata); mdata = NULL;
    break;
  case MEASURE_BELL:
    if (!(qstate_measure_bell(qstate, para->mes.shots, terminal_num, qubit_id,
			      (void**)&mdata)))
      ERR_RETURN(ERROR_QSTATE_MEASURE_BELL,false);
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
  case PHASE_SHIFT:
  case HADAMARD:
  case ROTATION_X:
  case ROTATION_Y:
  case ROTATION_Z:
  case CONTROLLED_X:
  case CONTROLLED_Y:
  case CONTROLLED_Z:
  case CONTROLLED_XR:
  case CONTROLLED_XR_:
  case CONTROLLED_H:
  case CONTROLLED_S:
  case CONTROLLED_S_:
  case CONTROLLED_T:
  case CONTROLLED_T_:
  case CONTROLLED_RX:
  case CONTROLLED_RY:
  case CONTROLLED_RZ:
  case CONTROLLED_P:
  case TOFFOLI:
    if (!(qstate_operate_qgate_param(qstate, kind, para->phase, qubit_id)))
      ERR_RETURN(ERROR_QSTATE_OPERATE_QGATE_PARAM,false);
    break;
  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }

  SUC_RETURN(true);
}

static bool _qstate_evolve_spro(QState* qstate, SPro* spro, double time)
{
  int pre,now;
  
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
      if (!(_qstate_operate_qgate_1(qstate, HADAMARD, now)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
    else if (spro->spin_type[now] == SIGMA_Y) {
      if (!(_qstate_operate_qgate_1_rot(qstate, X_AXIS, -0.5, M_PI, now)))
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
	if (!(_qstate_operate_qgate_2(qstate, CONTROLLED_X, pre, now)))
	  ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      }
    }
    pre = now; now++;
  }
  
  /* operate Rz(-2.0*t) */
  now = spro->spin_num-1;
  if (!(_qstate_operate_qgate_1_rot(qstate, Z_AXIS, -2.0*time, M_PI, now)))
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
	if (!(_qstate_operate_qgate_2(qstate, CONTROLLED_X, now, pre)))
	  ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      }
    }
    /* operate G+: G+=H (if PauliX), G+=Rx(+0.5) (if PauliY), G+=I (if PauliZ) */
    if (spro->spin_type[pre] == SIGMA_X) {
      if (!(_qstate_operate_qgate_1(qstate, HADAMARD, pre)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
    else if (spro->spin_type[pre] == SIGMA_Y) {
      if (!(_qstate_operate_qgate_1_rot(qstate, X_AXIS, 0.5, M_PI, pre)))
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
  QState* qstate_ob = NULL;

  if ((qstate == NULL) || (spro == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(qstate_copy(qstate, (void**)&qstate_ob)))
    ERR_RETURN(ERROR_QSTATE_COPY,NULL);

  for (int i=0; i<spro->spin_num; i++) {
    if (spro->spin_type[i] == NONE) {
      ;
    }
    else if (spro->spin_type[i] == SIGMA_X) {
      if (!(_qstate_operate_qgate_1(qstate_ob, PAULI_X, i))) {
	qstate_free(qstate_ob); qstate_ob = NULL;
	ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
      }
    }
    else if (spro->spin_type[i] == SIGMA_Y) {
      if (!(_qstate_operate_qgate_1(qstate_ob, PAULI_Y, i))) {
	qstate_free(qstate_ob); qstate_ob = NULL;
	ERR_RETURN(ERROR_INVALID_ARGUMENT,NULL);
      }
    }
    else if (spro->spin_type[i] == SIGMA_Z) {
      if (!(_qstate_operate_qgate_1(qstate_ob, PAULI_Z, i))) {
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

bool qstate_apply_matrix(QState* qstate, double* real, double *imag, int row, int col)
{
  QState*	qstate_tmp = NULL;
  COMPLEX	coef	   = 0.0 + 0.0i;
  int		idx;

  if ((qstate == NULL) || (real == NULL) || (imag == NULL) ||
      (qstate->state_num != col) || (row != col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(qstate_copy(qstate, (void**)&qstate_tmp)))
    ERR_RETURN(ERROR_QSTATE_COPY,false);

  for (int i=0; i<row; i++) {
    qstate->camp[i] = 0.0 + 0.0i;
    idx = i*col;
    for (int j=0; j<col; j++) {
      coef = real[idx+j] + 1.0i * imag[idx+j];
      qstate->camp[i] += (coef * qstate_tmp->camp[j]);
    }
  }

  qstate_free(qstate_tmp);
  qstate_tmp = NULL;

  SUC_RETURN(true);
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
