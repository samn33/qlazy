/*
 *  densop.c
 */

#include "qlazy.h"

bool densop_init(QState* qstate, double* prob, int num, void** densop_out)
{
  DensOp*	densop = NULL;
  int		state_num;

  if ((qstate == NULL) || (prob == NULL)) {
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }
  else {
    for (int i=0; i<num; i++) {
      /* qstate dimensions must be same */
      if (i==0) state_num = qstate[i].state_num;
      else if (qstate[i].state_num != state_num)
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    }
  }

  if (!(densop = (DensOp*)malloc(sizeof(DensOp))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  densop->row = densop->col = state_num;
  if (!(densop->elm = (COMPLEX*)malloc(sizeof(COMPLEX)*state_num*state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  int idx = 0;
  for (int k=0; k<state_num; k++) {
    for (int l=0; l<state_num; l++) {
      for (int i=0; i<num; i++) {
	densop->elm[idx] += (prob[i] * conj(qstate[i].camp[k]) * qstate[i].camp[l]);
      }
      idx++;
    }
  }

  *densop_out = densop;

  SUC_RETURN(true);
}

bool densop_print(DensOp* densop)
{
  int idx = 0;

  if ((densop == NULL) || (densop->row != densop->col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  for (int i=0; i<densop->row; i++) {
    for (int j=0; j<densop->col; j++) {
      double	dreal  = creal(densop->elm[idx]);
      double	dimag  = cimag(densop->elm[idx]);
      double	absval = pow(cabs(densop->elm[idx]),2.0);
      int	absval_level;

      if (fabs(absval) < MIN_DOUBLE) absval_level = 0;
      else absval_level = (int)(absval/0.1 + 1.5);
      
      printf("elm[%d][%d] = %+.4f%+.4f*i : %.4f |", i, j, dreal, dimag, absval);
      for (int k=0; k<absval_level; k++) printf("+");
      printf("\n");
      idx++;
    }
  }
  
  SUC_RETURN(true);
}

bool densop_trace(DensOp* densop, double* real, double* imag)
{
  COMPLEX	out = 0.0 + 0.0i;
  int		idx = 0;

  if ((densop == NULL) || (densop->row != densop->col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  for (int i=0; i<densop->row; i++) {
    out += densop->elm[idx];
    idx += (densop->col + 1);
  }
  
  *real = creal(out);
  *imag = cimag(out);

  SUC_RETURN(true);
}

static DensOp* _densop_copy(DensOp* densop_in)
{
  DensOp*	densop_out = NULL;
  int		dim;
  
  if ((densop_in == NULL) || (densop_in->row != densop_in->col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(densop_out = (DensOp*)malloc(sizeof(DensOp))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  densop_out->row = densop_in->row;
  densop_out->col = densop_in->col;
  dim = densop_in->row;
  if (!(densop_out->elm = (COMPLEX*)malloc(sizeof(COMPLEX)*dim*dim)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  memcpy(densop_out->elm, densop_in->elm, sizeof(COMPLEX)*dim*dim);

  return densop_out;
}

/* trace of the square of density operator */
bool densop_sqtrace(DensOp* densop, double* real, double* imag)
{
  DensOp*	densop_tmp = NULL;
  int		dim;
  COMPLEX	tmp;

  if ((densop == NULL) || (densop->row != densop->col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  dim = densop->row;

  /* square of the density operators */
  densop_tmp = _densop_copy(densop);
  for (int i=0; i<dim; i++) {
    for (int j=0; j<dim; j++) {
      tmp = 0.0 + 0.0i;
      for (int k=0; k<dim; k++) {
	tmp += (densop_tmp->elm[i*dim+k] * densop_tmp->elm[k*dim+j]);
      }
      densop->elm[i*dim+j] = tmp;
    }
  }

  /* trace of the matrix */
  tmp = 0.0 + 0.0i;
  for (int i=0; i<dim; i++) {
    tmp += densop->elm[i*dim+i];
  }
  
  *real = creal(tmp);
  *imag = cimag(tmp);

  densop_free(densop_tmp);
  densop_tmp = NULL;

  SUC_RETURN(true);
}

static int _cmp_for_sort(const void* p, const void* q)
{
  return *(int*)p - *(int*)p;
}


static int _get_id_remained(int in, int total_qubit_num,
			    int qubit_num, int qubit_id[MAX_QUBIT_NUM])
{
  int out = in;
  int shift,left,right;
  int qid;
  
  for (int i=0; i<qubit_num; i++) {
    qid = total_qubit_num - 1 - qubit_id[i];
    shift = qid;
    left = (out>>(shift+1))<<shift;
    right = in%(1<<shift);
    out = left + right;
  }
  return out;
}

static int _get_id_traced(int in, int total_qubit_num,
			  int qubit_num, int qubit_id[MAX_QUBIT_NUM])
{
  int out = 0;
  int qid,ii;
  for (int i=0; i<qubit_num; i++) {
    qid = total_qubit_num - 1 - qubit_id[i];
    ii = qubit_num - 1 - i;
    out += ((in>>qid)%2<<ii);
  }
  return out;
}

/* partial trace */
bool densop_patrace(DensOp* densop_in, int qubit_num, int qubit_id[MAX_QUBIT_NUM],
		     void** densop_out)
{
  DensOp*	densop = NULL;
  int           total_qubit_num;
  int		dim_in, dim_tr, dim;

  if ((densop_in == NULL) || (densop_in->row != densop_in->col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  dim_in = densop_in->row;
  total_qubit_num = (int)log2(dim_in);
  dim_tr = 1<<qubit_num;
  dim = 1<<(total_qubit_num-qubit_num);
  
#ifdef DEV
  printf("* total_qubit_num = %d\n", total_qubit_num);
#endif

  if (!(densop = (DensOp*)malloc(sizeof(DensOp))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  densop->row = densop->col = dim;
  if (!(densop->elm = (COMPLEX*)malloc(sizeof(COMPLEX)*dim*dim)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  for (int n=0; n<dim*dim; n++) densop->elm[n] = 0.0+0.0i;

  qsort(qubit_id, qubit_num, sizeof(int), _cmp_for_sort);
  
//#ifdef DEV
//  printf("* qubit_id: ");
//  for (int i=0; i<qubit_num; i++) printf("%d ", qubit_id[i]);
//  printf("\n");
//#endif

  int k,kk,l,ll;
  for (int i=0; i<dim_in; i++) {
    k = _get_id_remained(i, total_qubit_num, qubit_num, qubit_id);
    kk = _get_id_traced(i, total_qubit_num, qubit_num, qubit_id);
//#ifdef DEV
//    printf("i,k,kk = %d, %d, %d\n", i,k,kk);
//#endif
    for (int j=0; j<dim_in; j++) {
      l = _get_id_remained(j, total_qubit_num, qubit_num, qubit_id);
      ll = _get_id_traced(j, total_qubit_num, qubit_num, qubit_id);
//#ifdef DEV
//      printf("j,l,ll = %d, %d, %d\n", j,l,ll);
//#endif
      if (kk == ll) {
	densop->elm[k*dim+l] += densop_in->elm[i*dim_in+j];
      }
    }
  }
  
  *densop_out = densop;

  SUC_RETURN(true);
}

bool densop_apply_matrix(DensOp* densop, double* real, double* imag, int row, int col)
/*
  densop' = matrix * densop * matrix+ 
*/
{
  DensOp* densop_tmp = NULL;
  COMPLEX tmp;
  
  if ((densop == NULL) ||
      (densop->row != row) || (densop->col != col) || (row != col))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* allocate temporary */
  if (!(densop_tmp = (DensOp*)malloc(sizeof(DensOp))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  densop_tmp->row = densop_tmp->col = row;
  if (!(densop_tmp->elm = (COMPLEX*)malloc(sizeof(COMPLEX)*row*col)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  for (int n=0; n<row*col; n++) densop_tmp->elm[n] = 0.0+0.0i;

  /* Densop_tmp = Matrix * Densop */
  for (int i=0; i<row; i++) {
    for (int j=0; j<col; j++) {
      tmp = 0.0 + 0.0i;
      for (int k=0; k<row; k++) {
	tmp += (real[i*col+k]+1.0i*imag[i*col+k]) * densop->elm[k*col+j];
      }
      densop_tmp->elm[i*col+j] = tmp;
    }
  }

  /* Densop = Densop_tmp * Matrix+ */
  for (int i=0; i<row; i++) {
    for (int j=0; j<col; j++) {
      tmp = 0.0 + 0.0i;
      for (int k=0; k<row; k++) {
	tmp += conj(densop->elm[i*col+k]) * (real[k*col+j]+1.0i*imag[k*col+j]);
      }
      densop->elm[i*col+j] = tmp;
    }
  }

  densop_free(densop_tmp); densop_tmp = NULL;
  
  SUC_RETURN(true);
}

void densop_free(DensOp* densop)
{
  if (densop != NULL) {
    if (densop->elm != NULL) {
      free(densop->elm); densop->elm = NULL;
    }
    free(densop); densop = NULL;
  }
}
