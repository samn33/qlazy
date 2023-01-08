/*
 *  densop.c
 */
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"

#include "qlazy.h"

static DensOp* _create_densop(int row, int col)
{
  DensOp*	densop = NULL;
  int		size   = row * col;
  int i;

  if (!(densop = (DensOp*)malloc(sizeof(DensOp))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);
  densop->row = row;
  densop->col = col;
  densop->buf_id = 0;
  if (!(densop->buffer_0 = (COMPLEX*)malloc(sizeof(COMPLEX)*size)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);
  if (!(densop->buffer_1 = (COMPLEX*)malloc(sizeof(COMPLEX)*size)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);
  densop->elm = densop->buffer_0;

  for (i=0; i<size; i++) {
    densop->buffer_0[i] = 0.0 + 0.0 * COMP_I;
    densop->buffer_1[i] = 0.0 + 0.0 * COMP_I;
  }
  
  if (!(gbank_init((void**)&(densop->gbank))))
      ERR_RETURN(ERROR_GBANK_INIT,NULL);

  return densop;
}

bool densop_init(QState* qstate, double* prob, int num, void** densop_out)
{
  DensOp*	densop	  = NULL;
  int		state_num = 0;
  int		i,k,l,idx;

  if ((qstate == NULL) || (prob == NULL)) {
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }
  else {
    for (i=0; i<num; i++) {
      /* qstate dimensions must be same */
      if (i==0) state_num = qstate[i].state_num;
      else if (qstate[i].state_num != state_num)
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
  }

  if(!(densop = _create_densop(state_num, state_num)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  idx = 0;
  for (k=0; k<state_num; k++) {
    for (l=0; l<state_num; l++) {
      for (i=0; i<num; i++) {
	densop->elm[idx] += (prob[i] * qstate[i].camp[k] * conj(qstate[i].camp[l]));
      }
      idx++;
    }
  }

  *densop_out = densop;

  SUC_RETURN(true);
}

bool densop_init_with_matrix(double* real, double* imag, int row, int col,
			     void** densop_out)
{
  DensOp*	densop = NULL;
  int		size;

  size   = row * col;
  
  if ((real == NULL) || (imag == NULL) || (row != col) || (row < 1) ||
      (fabs(log2((double)row)-(int)log2((double)row)) > MIN_DOUBLE))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if(!(densop = _create_densop(row, col)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  int i;
  for (i=0; i<size; i++) {
    densop->elm[i] = real[i] + COMP_I * imag[i];
  }
  
  *densop_out = densop;

  SUC_RETURN(true);
}

bool densop_reset(DensOp* densop, int qubit_num, int* qubit_id)
{
  DensOp*	densop_A  = NULL;
  DensOp*	densop_B  = NULL;	/* |0><0| */
  DensOp*	densop_AB = NULL;
  int		row,col;
  int		row_B,col_B;
  int		i;
  
  if ((densop == NULL) || (densop->row != densop->col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  row = densop->row;
  col = densop->col;
  row_B = (int)(pow(2.0, (double)qubit_num) + 0.5);
  col_B = (int)(pow(2.0, (double)qubit_num) + 0.5);

  /* reset whole system */
  if ((row == row_B) && (col == col_B)) {
    for (i=0; i<row*col; i++) {
      densop->elm[i] = 0.0;
    }
    densop->elm[0] = 1.0;
  
    SUC_RETURN(true);
  }

  /* reset partial system */
  else if ((row > row_B) && (col > col_B)) {
    /* extract partial system (A) */
    if (!(densop_patrace(densop, qubit_num, qubit_id, (void**)&densop_A)))
      ERR_RETURN(ERROR_DENSOP_PATRACE,false);
  
    /* prepare |0><0| state (B) */
    if(!(densop_B = _create_densop(row_B, col_B)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    densop_B->elm[0] = 1.0;

    /* tensor product A and B */
    if (!(densop_tensor_product(densop_A, densop_B, (void**)&densop_AB)))
      ERR_RETURN(ERROR_DENSOP_TENSOR_PRODUCT,false);
    for (i=0; i<row*col; i++) {
      densop->elm[i] = densop_AB->elm[i];
    }

    densop_free(densop_A); densop_A = NULL;
    densop_free(densop_B); densop_B = NULL;
    densop_free(densop_AB); densop_AB = NULL;

    SUC_RETURN(true);
  }

  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }
}

bool densop_copy(DensOp* densop_in, void** densop_out)
{
  DensOp* densop = NULL;

  if (densop_in == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(densop = (DensOp*)malloc(sizeof(DensOp))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  densop->row = densop_in->row;
  densop->col = densop_in->col;
  densop->buf_id = 0;
  if (!(densop->buffer_0 = (COMPLEX*)malloc(sizeof(COMPLEX)*(densop->row)*(densop->col))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  if (!(densop->buffer_1 = (COMPLEX*)malloc(sizeof(COMPLEX)*(densop->row)*(densop->col))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  densop->elm = densop->buffer_0;

  memcpy(densop->elm, densop_in->elm, sizeof(COMPLEX)*(densop->row)*(densop->col));

  if (!(gbank_init((void**)&(densop->gbank))))
      ERR_RETURN(ERROR_GBANK_INIT,NULL);

  *densop_out = densop;

  SUC_RETURN(true);
}

bool densop_get_elm(DensOp* densop, void** elm_out)
{
  double*	elm = NULL;
  int		size;
  int		n   = 0;
  int		i;
  
  size = densop->row * densop->col;

  if (densop == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(elm = (double*)malloc(sizeof(double)*2*size)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  n = 0;
  for (i=0; i<size; i++) {
    elm[n++] = creal(densop->elm[i]);
    elm[n++] = cimag(densop->elm[i]);
  }

  *elm_out = elm;
  
  SUC_RETURN(true);
}

bool densop_print(DensOp* densop, bool nonzero)
{
  double	dreal;
  double	dimag;
  double	absval;
  int		absval_level;
  int		idx = 0;
  int		i,j,k;

  if ((densop == NULL) || (densop->row != densop->col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  for (i=0; i<densop->row; i++) {
    for (j=0; j<densop->col; j++) {
      dreal  = creal(densop->elm[idx]);
      dimag  = cimag(densop->elm[idx]);
      absval = pow(cabs(densop->elm[idx]),2.0);

      if (fabs(absval) < MIN_DOUBLE) absval_level = 0;
      else absval_level = (int)(absval/0.1 + 1.5);
      
      if ((nonzero == false) || (nonzero == true && fabs(absval) > MIN_DOUBLE)) {
	printf("elm[%d][%d] = %+.4f%+.4f*i : %.4f |", i, j, dreal, dimag, absval);
	for (k=0; k<absval_level; k++) printf("+");
	printf("\n");
      }
      idx++;
    }
  }
  
  SUC_RETURN(true);
}

bool densop_add(DensOp* densop, DensOp* densop_add)
{
  int size = 0;
  int i;
  
  if ((densop == NULL) || (densop->row != densop_add->row) ||
      (densop->col != densop_add->col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  size = densop->row * densop->col;

  for (i=0; i<size; i++) {
    densop->elm[i] += densop_add->elm[i];
  }
  
  SUC_RETURN(true);
}

bool densop_mul(DensOp* densop, double factor)
{
  int size = 0;
  int i;
  
  if (densop == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  size = densop->row * densop->col;

  for (i=0; i<size; i++) {
    densop->elm[i] *= factor;
  }

  SUC_RETURN(true);
}

bool densop_trace(DensOp* densop, double* real, double* imag)
{
  COMPLEX	out = 0.0 + 0.0 * COMP_I;
  int		idx = 0;
  int		i;

  if ((densop == NULL) || (densop->row != densop->col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  for (i=0; i<densop->row; i++) {
    out += densop->elm[idx];
    idx += (densop->col + 1);
  }
  
  *real = creal(out);
  *imag = cimag(out);
  
  SUC_RETURN(true);
}

/* trace of the square of density operator */
bool densop_sqtrace(DensOp* densop, double* real, double* imag)
{
  DensOp*	densop_tmp = NULL;
  int		dim;
  COMPLEX	tmp;
  int		i,j,k;

  if ((densop == NULL) || (densop->row != densop->col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  dim = densop->row;
  
  /* square of the density operators */
  if (!(densop_copy(densop, (void**)&densop_tmp)))
    ERR_RETURN(ERROR_DENSOP_COPY,false);
  for (i=0; i<dim; i++) {
    for (j=0; j<dim; j++) {
      tmp = 0.0 + 0.0 * COMP_I;
      for (k=0; k<dim; k++) {
	tmp += (densop->elm[i*dim+k] * densop->elm[k*dim+j]);
      }
      densop_tmp->elm[i*dim+j] = tmp;
    }
  }

  /* trace of the matrix */
  tmp = 0.0 + 0.0 * COMP_I;
  for (i=0; i<dim; i++) {
    tmp += densop_tmp->elm[i*dim+i];
  }
  
  *real = creal(tmp);
  *imag = cimag(tmp);

  densop_free(densop_tmp);
  densop_tmp = NULL;

  SUC_RETURN(true);
}

static int _cmp_for_sort(const void* p, const void* q)
{
  return *(int*)p - *(int*)q;
}

static int _get_id_remained(int in, int total_qubit_num,
			    int qubit_num, int* qubit_id)
{
  int out = in;
  int shift,left,right;
  int qid;
  int i;
  
  for (i=0; i<qubit_num; i++) {
    qid = total_qubit_num - 1 - qubit_id[i];
    shift = qid;
    left = (out>>(shift+1))<<shift;
    right = in%(1<<shift);
    out = left + right;
  }
  return out;
}

static int _get_id_traced(int in, int total_qubit_num,
			  int qubit_num, int* qubit_id)
{
  int out = 0;
  int qid,ii,i;
  
  for (i=0; i<qubit_num; i++) {
    qid = total_qubit_num - 1 - qubit_id[i];
    ii = qubit_num - 1 - i;
    out += ((in>>qid)%2<<ii);
  }
  return out;
}

/* partial trace */
bool densop_patrace(DensOp* densop_in, int qubit_num, int* qubit_id,
		     void** densop_out)
{
  DensOp*	densop = NULL;
  int           total_qubit_num;
  int		dim_in, dim_tr, dim;
  int		i,j,k,kk,l,ll;

  if ((densop_in == NULL) || (densop_in->row != densop_in->col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  dim_in = densop_in->row;
  total_qubit_num = (int)log2((double)dim_in);
  dim_tr = 1<<qubit_num;
  dim = 1<<(total_qubit_num-qubit_num);
  
  if(!(densop = _create_densop(dim, dim)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  qsort(qubit_id, (size_t)qubit_num, sizeof(int), _cmp_for_sort);
  
  for (i=0; i<dim_in; i++) {
    k = _get_id_remained(i, total_qubit_num, qubit_num, qubit_id);
    kk = _get_id_traced(i, total_qubit_num, qubit_num, qubit_id);

    for (j=0; j<dim_in; j++) {
      l = _get_id_remained(j, total_qubit_num, qubit_num, qubit_id);
      ll = _get_id_traced(j, total_qubit_num, qubit_num, qubit_id);

      if (kk == ll) {
	densop->elm[k*dim+l] += densop_in->elm[i*dim_in+j];
      }
    }
  }
  
  *densop_out = densop;

  SUC_RETURN(true);
}

static bool _hermitian_conj(double* real_in, double* imag_in, int row, int col,
			    void** real_out, void** imag_out)
{
  int		size;
  double*	real = NULL;
  double*	imag = NULL;
  int		i,j;

  size = row * col;

  if (!(real = (double*)malloc(sizeof(double)*size)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  if (!(imag = (double*)malloc(sizeof(double)*size)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  for (i=0; i<row; i++) {
    for (j=0; j<col; j++) {
      real[i*col+j] = real_in[j*col+i];
      imag[i*col+j] = -imag_in[j*col+i];
    }
  }

  *real_out = real;
  *imag_out = imag;
  
  SUC_RETURN(true);
}

static bool _densop_rapply_matrix(DensOp* densop, int qnum_part, int* qid,
				  double* real, double* imag, int row, int col)
/*
  densop' = densop * matrix
*/
{
  int*		index	   = NULL;
  int*		inv_index  = NULL;
  COMPLEX	coef	   = 0.0 + 0.0 * COMP_I;
  int		qnum	   = 0;
  int		shift	   = 0;
  int           N	   = 0;
  int		ii,iii,jj,jjj,kk,kkk;
  int           i,j,k,l,n;
  COMPLEX*      buffer_in;
  COMPLEX*      buffer_out;

  if ((densop == NULL) || (real == NULL) || (imag == NULL) ||
      (densop->row < row) || (densop->col < col) || (row != col) ||
      (1<<qnum_part != row))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (densop->buf_id == 0) {
    buffer_in = densop->buffer_0;
    buffer_out = densop->buffer_1;
  }
  else {
    buffer_in = densop->buffer_1;
    buffer_out = densop->buffer_0;
  }

  qnum = (int)log2((double)densop->row);
  index = bit_permutation_array(densop->row, qnum, qnum_part, qid);

  if (!(inv_index = (int*)malloc(sizeof(int)*densop->row)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  for (n=0; n<densop->row; n++) inv_index[index[n]] = n; 
  
  /* Densop = Densop * Matrix */
  shift = qnum-qnum_part;
  N = 1<<(qnum-shift);

# pragma omp parallel for private(ii,iii,jj,jjj,k,kk,kkk,coef), shared(buffer_out)
  for (i=0; i<densop->row; i++) {
    ii = index[i]>>shift;
    iii = index[i]%(1<<shift);
    for (j=0; j<densop->col; j++) {
      jj = index[j]>>shift;
      jjj = index[j]%(1<<shift);
      buffer_out[i*densop->col+j] = 0.0 + 0.0 * COMP_I;

      for (l=0; l<N; l++) {
	k = inv_index[(l<<shift)+jjj];
	kk = index[k]>>shift;
	kkk = index[k]%(1<<shift);
	coef = real[kk*col+jj] + 1.0 * COMP_I * imag[kk*col+jj];
	buffer_out[i*densop->col+j] += (buffer_in[i*densop->col+k] * coef);
      }
    }
  }

  if (densop->buf_id == 0) densop->buf_id = 1;
  else densop->buf_id = 0;
  densop->elm = buffer_out;

  free(index); index = NULL;
  free(inv_index); inv_index = NULL;

  SUC_RETURN(true);
}

static bool _densop_lapply_matrix(DensOp* densop, int qnum_part, int* qid,
				  double* real, double* imag, int row, int col)
/*
  densop' = matrix * densop
*/
{
  int*		index	   = NULL;
  int*		inv_index  = NULL;
  COMPLEX	coef	   = 0.0 + 0.0 * COMP_I;
  int		qnum	   = 0;
  int		shift	   = 0;
  int           N	   = 0;
  int		ii,iii,jj,jjj,kk,kkk;
  int           i,j,k,l,n;

  COMPLEX*      buffer_in;
  COMPLEX*      buffer_out;
  
  if ((densop == NULL) || (real == NULL) || (imag == NULL) ||
      (densop->row < row) || (densop->col < col) || (row != col) ||
      (1<<qnum_part != row))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (densop->buf_id == 0) {
    buffer_in = densop->buffer_0;
    buffer_out = densop->buffer_1;
  }
  else {
    buffer_in = densop->buffer_1;
    buffer_out = densop->buffer_0;
  }

  qnum = (int)log2((double)densop->row);
  index = bit_permutation_array(densop->row, qnum, qnum_part, qid);

  if (!(inv_index = (int*)malloc(sizeof(int)*densop->row)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  for (n=0; n<densop->row; n++) inv_index[index[n]] = n; 

  /* Densop = Matrix * Densop */
  shift = qnum-qnum_part;
  N = 1<<(qnum-shift);

# pragma omp parallel for private(ii,iii,jj,jjj,k,kk,kkk,coef), shared(buffer_out)
  for (i=0; i<densop->row; i++) {
    ii = index[i]>>shift;
    iii = index[i]%(1<<shift);
    for (j=0; j<densop->col; j++) {
      jj = index[j]>>shift;
      jjj = index[j]%(1<<shift);
      buffer_out[i*densop->col+j] = 0.0 + 0.0 * COMP_I;

      for (l=0; l<N; l++) {
	k = inv_index[(l<<shift)+iii];
	kk = index[k]>>shift;
	kkk = index[k]%(1<<shift);
	coef = real[ii*col+kk] + 1.0 * COMP_I * imag[ii*col+kk];
	buffer_out[i*densop->col+j] += (coef * buffer_in[k*densop->col+j]);
      }
    }
  }

  if (densop->buf_id == 0) densop->buf_id = 1;
  else densop->buf_id = 0;
  densop->elm = buffer_out;

  free(index); index = NULL;
  free(inv_index); inv_index = NULL;

  SUC_RETURN(true);
}

static bool _densop_bapply_matrix(DensOp* densop, int qnum_part, int* qid,
				  double* real, double* imag, int row, int col)
/*
  densop' = matrix * densop * matrix^{dagger}
*/
{
  double*	real_hc = NULL;
  double*	imag_hc = NULL;

  if (!(_densop_lapply_matrix(densop, qnum_part, qid, real, imag, row, col)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  _hermitian_conj(real, imag, row, col, (void**)&real_hc, (void**)&imag_hc);
  
  if (!(_densop_rapply_matrix(densop, qnum_part, qid, real_hc, imag_hc, row, col)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  free(real_hc); real_hc = NULL;
  free(imag_hc); imag_hc = NULL;

  SUC_RETURN(true);
}

bool densop_apply_matrix(DensOp* densop, int qnum_part, int* qid,
			 ApplyDir adir, double* real, double* imag, int row, int col)
{
  if (adir == LEFT) {
    if (!(_densop_lapply_matrix(densop, qnum_part, qid, real, imag, row, col)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }
  else if (adir == RIGHT) {
    if (!(_densop_rapply_matrix(densop, qnum_part, qid, real, imag, row, col)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }
  else if (adir == BOTH) {
    if (!(_densop_bapply_matrix(densop, qnum_part, qid, real, imag, row, col)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }
  else {
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }

  SUC_RETURN(true);
}

static bool _densop_probability_kraus(DensOp* densop, int qnum_part, int* qid,
				      double* real, double* imag, int row, int col,
				      double* prob_out)
{
  DensOp*	densop_tmp = NULL;
  double	prob_real  = 0.0;
  double	prob_imag  = 0.0;
  
  if (densop == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(densop_copy(densop, (void**)&densop_tmp)))
    ERR_RETURN(ERROR_DENSOP_COPY,false);

  if (!(_densop_bapply_matrix(densop_tmp, qnum_part, qid, real, imag, row, col)))
    ERR_RETURN(ERROR_DENSOP_APPLY_MATRIX,false);
  
  if (!(densop_trace(densop_tmp, &prob_real, &prob_imag)))
    ERR_RETURN(ERROR_DENSOP_TRACE,false);
  if (fabs(prob_imag) > MIN_DOUBLE) ERR_RETURN(ERROR_DENSOP_TRACE,false);
  *prob_out = prob_real;

  densop_free(densop_tmp); densop_tmp = NULL;
  
  SUC_RETURN(true);
}

static bool _densop_probability_povm(DensOp* densop, int qnum_part, int* qid,
				     double* real, double* imag, int row, int col,
				     double* prob_out)
{
  DensOp*	densop_tmp = NULL;
  double	prob_real  = 0.0;
  double	prob_imag  = 0.0;
  
  if (densop == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(densop_copy(densop, (void**)&densop_tmp)))
    ERR_RETURN(ERROR_DENSOP_COPY,false);

  if (!(_densop_lapply_matrix(densop_tmp, qnum_part, qid, real, imag, row, col)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  if (!(densop_trace(densop_tmp, &prob_real, &prob_imag)))
    ERR_RETURN(ERROR_DENSOP_TRACE,false);
  if (fabs(prob_imag) > MIN_DOUBLE) ERR_RETURN(ERROR_DENSOP_TRACE,false);
  *prob_out = prob_real;
    
  densop_free(densop_tmp); densop_tmp = NULL;
  
  SUC_RETURN(true);
}

bool densop_probability(DensOp* densop, int qnum_part, int* qid,
			MatrixType mtype, double* real, double* imag, int row, int col,
			double* prob_out)
{
  if (densop == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (mtype == KRAUS) {
    if (!(_densop_probability_kraus(densop, qnum_part, qid, real, imag, row, col, prob_out)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }
  else if (mtype == POVM) {
    if (!(_densop_probability_povm(densop, qnum_part, qid, real, imag, row, col, prob_out)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }
  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }

  SUC_RETURN(true);
}

static bool _densop_operate_unitary(DensOp* densop, COMPLEX* U, int dim, int m, int n)
{
  int		qnum_part;
  int		qid[2];
  ApplyDir	adir = BOTH;
  double	real[16];
  double	imag[16];
  int		row,col;
  int		i;

  if ((densop == NULL) || (densop->row != densop->col))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if ((m < 0) || (m >= densop->row))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  if (dim == 2) {
    qnum_part = 1;
    row = col = 2;
    qid[0] = m;
    for (i=0; i<dim*dim; i++) {
      real[i] = creal(U[i]);
      imag[i] = cimag(U[i]);
    }
    if (!(densop_apply_matrix(densop, qnum_part, qid, adir, real, imag, row, col)))
      ERR_RETURN(ERROR_DENSOP_APPLY_MATRIX,false);
  }

  else if (dim == 4) {
    if ((n < 0) || (n >= densop->row) || (m == n))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    qnum_part = 2;
    row = col = 4;
    qid[0] = m; qid[1] = n;
    for (i=0; i<dim*dim; i++) {
      real[i] = creal(U[i]);
      imag[i] = cimag(U[i]);
    }
    if (!(densop_apply_matrix(densop, qnum_part, qid, adir, real, imag, row, col)))
      ERR_RETURN(ERROR_DENSOP_APPLY_MATRIX,false);
  }

  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }
  
  SUC_RETURN(true);
}

bool densop_operate_qgate(DensOp* densop, Kind kind, double para_phase, double para_gphase,
			  double para_factor, int* qubit_id)
{
  int		q0  = qubit_id[0];
  int		q1  = qubit_id[1];
  int		dim = 0;
  COMPLEX*	U   = NULL;

  if (densop == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if ((kind == INIT) || (kind ==MEASURE) || (kind ==MEASURE_X) ||
      (kind == MEASURE_Y) || (kind == MEASURE_Z) || (kind == MEASURE_BELL))
    SUC_RETURN(true);
  else {
    if (!(gbank_get_unitary(densop->gbank, kind, para_phase, para_gphase, para_factor, &dim, (void**)&U)))
      ERR_RETURN(ERROR_GBANK_GET_UNITARY,false);
    if (!(_densop_operate_unitary(densop, U, dim, q0, q1)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    free(U); U = NULL;
    SUC_RETURN(true);
  }
}

bool densop_tensor_product(DensOp* densop_0, DensOp* densop_1, void** densop_out)
{
  int		row, row_0, row_1;
  int		col, col_0, col_1;
  int		idx, idx_0, idx_1;
  DensOp*	densop = NULL;
  int		i,j;

  if ((densop_0 == NULL) || (densop_1 == NULL) ||
      (densop_0->row != densop_0->col) || (densop_1->row != densop_1->col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  row_0 = densop_0->row;
  col_0 = densop_0->col;
  row_1 = densop_1->row;
  col_1 = densop_1->col;
  row = row_0 * row_1;
  col = col_0 * col_1;
  
  if(!(densop = _create_densop(row, col)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* Kronecker product */
  idx = 0;
  for (i=0; i<row; i++) {
    for (j=0; j<col; j++) {
      idx_0 = (i/row_1) * col_0 + (j/col_1);
      idx_1 = (i%row_1) * col_1 + (j%col_1);
      densop->elm[idx++] = densop_0->elm[idx_0] * densop_1->elm[idx_1];
    }
  }

  *densop_out = densop;

  SUC_RETURN(true);
}

void densop_free(DensOp* densop)
{
  if (densop != NULL) {
    if (densop->buffer_0 != NULL) {
      free(densop->buffer_0); densop->buffer_0 = NULL;
    }
    if (densop->buffer_1 != NULL) {
      free(densop->buffer_1); densop->buffer_1 = NULL;
    }
    free(densop); densop = NULL;
  }
}
