/*
 *  qgate.c
 */

#include "qlazy.h"

static bool _composite_unitary(COMPLEX* U, int* dim, int* q0, int* q1,
			       COMPLEX* U_A, int dim_A, int q0_A, int q1_A)
/* U <= U_A x U */
  
{
  int		i, j, k, l, m, n, p, q, r, s;
  int           jj, kk;
  COMPLEX       U_B[16];
  int           dim_B;
  int           q0_B;
  int           q1_B;

  /* set dim_B, q0_B, q1_B, U_B, and reset U to zero */
  dim_B = *dim;
  q0_B = *q0;
  q1_B = *q1;
  for (i=0; i<dim_B*dim_B; i++) {
    U_B[i] = U[i];
  }
  for (i=0; i<16; i++) {
    U[i] = 0.0;
  }

  /* 1-qubit(B) --> 1-qubit(A) */
  if (dim_B == 2 && dim_A == 2) {
    if (q0_B == q0_A) {

      for (i=0; i<2; i++) {
	for (j=0; j<2; j++) {
	  for (k=0; k<2; k++) {
	    U[IDX2(i, j)] += U_A[IDX2(i, k)] * U_B[IDX2(k, j)];
	  }
	}
      }
      *dim = 2;

    }
    else {

      for (i=0; i<4; i++) {
	k = i % 2;
	m = i / 2;
	for (j=0; j<4; j++) {
	  l = j % 2;
	  n = j / 2;
	  U[IDX4(i, j)] = U_A[IDX2(k, l)] * U_B[IDX2(m, n)];
	}
      }
      *q0 = q0_B;
      *q1 = q0_A;
      *dim = 4;
    }
  }

  /* 1-qubit(B) --> 2-qubit(A) */
  else if (dim_B == 2 && dim_A == 4) {

    if (q0_B == q0_A) {

      m = 0;
      r = 1;
      for (i=0; i<4; i++) {
	k = i;
	p = i;
	for (j=0; j<4; j++) {
	  l = j % 2;
	  n = j / 2;
	  q = j % 2 + 2;
	  s = j / 2;
	  U[IDX4(i, j)] = U_A[IDX4(k, l)] * U_B[IDX2(m, n)] + U_A[IDX4(p, q)] * U_B[IDX2(r, s)];
	}
      }
      *q0 = q0_A;
      *q1 = q1_A;
      *dim = 4;
    }

    else if (q0_B == q1_A) {

      m = 0;
      r = 1;
      for (i=0; i<4; i++) {
	k = i;
	p = i;
	for (j=0; j<4; j++) {
	  l = (j / 2) * 2;
	  n = j % 2;
	  q = (j / 2) * 2 + 1;
	  s = j % 2;
	  U[IDX4(i, j)] = U_A[IDX4(k, l)] * U_B[IDX2(m, n)] + U_A[IDX4(p, q)] * U_B[IDX2(r, s)];
	}
      }
      *q0 = q0_A;
      *q1 = q1_A;
      *dim = 4;
    }
    else {
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    }

  /* 2-qubit(B) --> 1-qubit(A) */
  }
  else if (dim_B == 4 && dim_A == 2) {

    if (q0_B == q0_A) {

      l = 0;
      q = 1;
      for (i=0; i<4; i++) {
	k = i / 2;
	m = i % 2;
	p = i / 2;
	r = (i % 2) + 2;
	for (j=0; j<4; j++) {
	  n = j;
	  s = j;
	  U[IDX4(i, j)] = U_A[IDX2(k, l)] * U_B[IDX4(m, n)] + U_A[IDX2(p, q)] * U_B[IDX4(r, s)];
	}
      }
      *q0 = q0_B;
      *q1 = q1_B;
      *dim = 4;
    }
    else if (q1_B == q0_A) {

      l = 0;
      q = 1;
      for (i=0; i<4; i++) {
	k = i % 2;
	m = (i / 2) * 2;
	p = i % 2;
	r = (i / 2) * 2 + 1;
	for (j=0; j<4; j++) {
	  n = j;
	  s = j;
	  U[IDX4(i, j)] = U_A[IDX2(k, l)] * U_B[IDX4(m, n)] + U_A[IDX2(p, q)] * U_B[IDX4(r, s)];
	}
      }
      *q0 = q0_B;
      *q1 = q1_B;
      *dim = 4;
    }
    else {
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    }

  /* 2-qubit --> 2-qubit */
  }
  else if (dim_B == 4 && dim_A == 4) {

    if ((q0_B == q0_A) && (q1_B == q1_A)) {

      for (i=0; i<4; i++) {
	for (j=0; j<4; j++) {
	  for (k=0; k<4; k++) {
	    U[IDX4(i, j)] += U_A[IDX4(i, k)] * U_B[IDX4(k, j)];
	  }
	}
      }
      *q0 = q0_A;
      *q1 = q1_A;
      *dim = 4;
    }
    else if ((q0_B == q1_A) && (q1_B == q0_A)) {

      for (i=0; i<4; i++) {
	for (j=0; j<4; j++) {
	  if (j == 1) jj = 2;
	  else if (j == 2) jj = 1;
	  else jj = j;
	  for (k=0; k<4; k++) {
	    if (k == 1) kk = 2;
	    else if (k == 2) kk = 1;
	    else kk = k;
	    U[IDX4(i, j)] += U_A[IDX4(i, k)] * U_B[IDX4(kk, jj)];
	  }
	}
      }
      *q0 = q0_A;
      *q1 = q1_A;
      *dim = 4;
    }
    else {
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    }
  }

  /* error */
  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }
  
  SUC_RETURN(true);
}

static bool _composite_or_not(int dim, int q0, int q1, QGate* qgate_next, bool* ans)
{
  int dim_next;
  int q0_next = qgate_next->qid[0];
  int q1_next = qgate_next->qid[1];

  if (kind_get_qid_size(qgate_next->kind) == 1) dim_next = 2;
  else dim_next = 4;
  
  /* 1-qubit -> 1-qubit */
  if ((dim == 2) && (dim_next == 2)) {
    if (q0 == q0_next) {
      *ans = true;
    }
    else {
      *ans = false;
    }
  }
  /* 1-qubit -> 2-qubit */
  else if ((dim == 2) && (dim_next == 4)) {
    if ((q0 != q0_next) && (q0 != q1_next)) {
      *ans = false;
    }
    else {
      *ans = false;
    }
  }
  /* 2-qubit -> 1-qubit */
  else if ((dim == 4) && (dim_next == 2)) {
    if ((q0 != q0_next) && (q1 != q0_next)) {
      *ans = false;
    }
    else {
      *ans = false;
    }
  }
  /* 2-qubit -> 2-qubit */
  else if ((dim == 4) && (dim_next == 4)) {
    if ((q0 == q0_next) && (q1 == q1_next)) {
      *ans = false;
    }
    else if ((q0 == q1_next) && (q1 == q0_next)) {
      *ans = false;
    }
    else {
      *ans = false;
    }
  }
  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }

  SUC_RETURN(true);
}

bool qgate_get_next_unitary(void** qgate_inout, GBank* gbank, int* dim, int* q0, int* q1,
			    void** matrix_out, bool* compo)
{
  COMPLEX*      U	= NULL;
  COMPLEX*	U_tmp	= NULL;
  int		dim_tmp	= 2;
  int           q0_tmp	= -1;
  int           q1_tmp	= -1;
  int           i;
  bool          ans	= false;
  QGate*        qgate = (QGate*)(*qgate_inout);

  /* malloc for output unitary matrix */
  if (!(U = (COMPLEX*)malloc(sizeof(COMPLEX) * 16)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  /* get 1st unitary matrix */
  if (!(gbank_get_unitary(gbank, qgate->kind, qgate->para[0], qgate->para[1],
			  qgate->para[2], &dim_tmp, (void**)&U_tmp))) {
    ERR_RETURN(ERROR_GBANK_GET_UNITARY, false);
  }

  /* set U, dim, q0, q1 */
  for (i=0; i<dim_tmp*dim_tmp; i++) {
    U[i] = U_tmp[i];
  }
  *dim = dim_tmp;
  *q0 = qgate->qid[0];
  *q1 = qgate->qid[1];
  free(U_tmp); U_tmp = NULL;

  *compo = false;
  while ((qgate->next != NULL) && (kind_is_unitary(qgate->next->kind) == true)) {

    if (!(_composite_or_not(*dim, *q0, *q1, qgate->next, &ans)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

    if (ans == true) *compo = true;
    else break;
  
    qgate = qgate->next;
    if (!(gbank_get_unitary(gbank, qgate->kind, qgate->para[0], qgate->para[1], qgate->para[2],
			    &dim_tmp, (void**)&U_tmp))) {
      ERR_RETURN(ERROR_GBANK_GET_UNITARY, false);
    }

    q0_tmp = qgate->qid[0];
    q1_tmp = qgate->qid[1];
    if (!(_composite_unitary(U, dim, q0, q1, U_tmp, dim_tmp, q0_tmp, q1_tmp))) {
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    }
    free(U_tmp); U_tmp = NULL;
  }

  *qgate_inout = qgate;
  *matrix_out = U;

  SUC_RETURN(true);
}

bool qgate_get_measurement_attributes(void** qgate_inout, GBank* gbank,
				      int* mnum_out, int* qid_out, int* cid_out, bool* last_out)
{
  int		count = 0;
  QGate*	qgate = (QGate*)(*qgate_inout);

  *last_out = false;

  qid_out[count] = qgate->qid[0];
  cid_out[count] = qgate->c;
  count++;

  while (true) {
    if (qgate->next == NULL) {
      *last_out = true;
      break;
    }
    else if (kind_is_measurement(qgate->next->kind) == true) {
      qgate = qgate->next;
      qid_out[count] = qgate->qid[0];
      cid_out[count] = qgate->c;
      count++;
    }
    else {
      break;
    }
  }

  *mnum_out = count;
  *qgate_inout = qgate;

  SUC_RETURN(true);
}
