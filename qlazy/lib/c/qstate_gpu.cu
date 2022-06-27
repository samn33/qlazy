/*
 *  qstate_gpu.cu
 */
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"

#ifdef __cplusplus
extern "C" {
#endif

#include "qlazy.h"

#define BLOCKSIZE 32

__constant__ cuDoubleComplex d_U[16];

__global__ void cuda_qstate_operate_unitary2(cuDoubleComplex* d_camp_out, cuDoubleComplex* d_camp_in,
					     int qubit_num, int state_num, int n)
{
  int		nn, i, p, pp, sign, off;
  cuDoubleComplex	camp;

  nn = qubit_num - n - 1;
  
  i = blockIdx.x * blockDim.x + threadIdx.x;

  if (i < state_num) {
    
    p = (i >> nn) % 2;
    pp = p ^ 1;
    sign = (pp << 1) - 1; // pp=0 -> -1, pp=1 -> +1
    off = sign * (1 << nn);

    camp = cuCmul(d_U[IDX2(p,p)], d_camp_in[i]);
    d_camp_out[i] = cuCadd(camp, cuCmul(d_U[IDX2(p,pp)], d_camp_in[i + off]));
  }
}

__global__ void cuda_qstate_operate_unitary4(cuDoubleComplex* d_camp_out, cuDoubleComplex* d_camp_in,
					     int qubit_num, int state_num, int m, int n)
{
  int			mm, nn, i, p, pp, q, qq;
  int			l, sign_p, sign_q, off_p, off_q;
  cuDoubleComplex	camp;
  
  mm = qubit_num - m - 1;
  nn = qubit_num - n - 1;

  i = blockIdx.x * blockDim.x + threadIdx.x;

  if (i < state_num) {

    p = (i >> mm) % 2;
    pp = p ^ 1;
    q = (i >> nn) % 2;
    qq = q ^ 1;

    l = (p << 1) + q;

    sign_p = (pp << 1) - 1;
    sign_q = (qq << 1) - 1;

    off_p = sign_p * (1 << mm);
    off_q = sign_q * (1 << nn);

    camp = cuCmul(d_U[IDX4(l, l)], d_camp_in[i]);
    camp = cuCadd(camp, cuCmul(d_U[IDX4(l, (l^1))], d_camp_in[i + off_q]));
    camp = cuCadd(camp, cuCmul(d_U[IDX4(l, (l^2))], d_camp_in[i + off_p]));
    d_camp_out[i] = cuCadd(camp, cuCmul(d_U[IDX4(l, (l^3))], d_camp_in[i + off_q + off_p]));
  }
}

__global__ void cuda_qstate_operate_controlled_gate(cuDoubleComplex* d_camp_out, cuDoubleComplex* d_camp_in,
						    int qubit_num, int state_num, int m, int n)
{
  int			mm, nn, i, p, q, qq;
  int			l, sign_q, off_q;
  cuDoubleComplex	camp;
  
  mm = qubit_num - m - 1;
  nn = qubit_num - n - 1;

  i = blockIdx.x * blockDim.x + threadIdx.x;

  if (i < state_num) {

    p = (i >> mm) % 2;
    q = (i >> nn) % 2;
    qq = q ^ 1;

    l = (p << 1) + q;

    sign_q = (qq << 1) - 1;
    off_q = sign_q * (1 << nn);

    camp = cuCmul(d_U[IDX4(l, l)], d_camp_in[i]);
    d_camp_out[i] = cuCadd(camp, cuCmul(d_U[IDX4(l, (l^1))], d_camp_in[i + off_q]));
  }
}

static bool _qstate_operate_unitary_gpu_static(QState* qstate, int dim, int m, int n)
{
  int			qubit_num  = qstate->qubit_num;
  int			state_num  = qstate->state_num;
  cuDoubleComplex*	d_buffer_0 = qstate->d_buffer_0;
  cuDoubleComplex*	d_buffer_1 = qstate->d_buffer_1;
  int			blocksize  = BLOCKSIZE;
  dim3			block (blocksize, 1, 1);
  dim3			grid ((state_num + block.x - 1) / block.x, 1, 1);

  if ((qstate == NULL) || (qstate->use_gpu == false) || (dim < 0))
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (dim == 2) {
    /* 0 -> 1 */
    if (qstate->d_buf_id == 0) {
      cuda_qstate_operate_unitary2<<< grid, block >>>(d_buffer_1, d_buffer_0,
      						      qubit_num, state_num, m);
      qstate->d_buf_id = 1;
      qstate->d_camp = qstate->d_buffer_1;
    }
    /* 1 -> 0 */
    else {
      cuda_qstate_operate_unitary2<<< grid, block >>>(d_buffer_0, d_buffer_1,
						      qubit_num, state_num, m);
      qstate->d_buf_id = 0;
      qstate->d_camp = qstate->d_buffer_0;
    }
  }
  else if (dim == 4) {
    /* 0 -> 1 */
    if (qstate->d_buf_id == 0) {
      cuda_qstate_operate_unitary4<<< grid, block >>>(d_buffer_1, d_buffer_0,
      						      qubit_num, state_num, m, n);
      qstate->d_buf_id = 1;
      qstate->d_camp = qstate->d_buffer_1;
    }
    /* 1 -> 0 */
    else {
      cuda_qstate_operate_unitary4<<< grid, block >>>(d_buffer_0, d_buffer_1,
						      qubit_num, state_num, m, n);
      qstate->d_buf_id = 0;
      qstate->d_camp = qstate->d_buffer_0;
    }
  }
  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }

  qstate->d_prob_updated = false;

  SUC_RETURN(true);
}

static bool _qstate_operate_controlled_gate_gpu_static(QState* qstate, int m, int n)
{
  int			qubit_num  = qstate->qubit_num;
  int			state_num  = qstate->state_num;
  cuDoubleComplex*	d_buffer_0 = qstate->d_buffer_0;
  cuDoubleComplex*	d_buffer_1 = qstate->d_buffer_1;
  int			blocksize  = BLOCKSIZE;
  dim3			block (blocksize, 1, 1);
  dim3			grid ((state_num + block.x - 1) / block.x, 1, 1);

  if ((qstate == NULL) || (qstate->use_gpu == false))
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  /* 0 -> 1 */
  if (qstate->d_buf_id == 0) {
    cuda_qstate_operate_controlled_gate<<< grid, block >>>(d_buffer_1, d_buffer_0,
							   qubit_num, state_num, m, n);
    qstate->d_buf_id = 1;
    qstate->d_camp = qstate->d_buffer_1;
  }
  /* 1 -> 0 */
  else {
    cuda_qstate_operate_controlled_gate<<< grid, block >>>(d_buffer_0, d_buffer_1,
							   qubit_num, state_num, m, n);
    qstate->d_buf_id = 0;
    qstate->d_camp = qstate->d_buffer_0;
  }

  qstate->d_prob_updated = false;

  SUC_RETURN(true);
}

bool qstate_operate_controlled_gate_gpu(QState* qstate, COMPLEX* U, int m, int n)
{
  int			i;
  cuDoubleComplex*	h_U = NULL;

  if ((qstate == NULL) || (qstate->use_gpu == false) || (U == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  checkCudaErrors(cudaMallocHost((void**)&h_U, sizeof(cuDoubleComplex) * 16));

  for (i=0; i<16; i++) {
    h_U[i] = make_cuDoubleComplex(creal(U[i]), cimag(U[i]));
  }
  checkCudaErrors(cudaMemcpyToSymbol(d_U, h_U, sizeof(cuDoubleComplex) * 16));

  _qstate_operate_controlled_gate_gpu_static(qstate, m, n);

  checkCudaErrors(cudaFreeHost(h_U));

  SUC_RETURN(true);
}

bool qstate_operate_unitary_gpu(QState* qstate, COMPLEX* U, int dim, int m, int n)
{
  int			i;
  cuDoubleComplex*	h_U = NULL;

  if ((qstate == NULL) || (qstate->use_gpu == false) || (U == NULL) || (dim < 0))
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  checkCudaErrors(cudaMallocHost((void**)&h_U, sizeof(cuDoubleComplex) * 16));

  for (i=0; i<dim*dim; i++) {
    h_U[i] = make_cuDoubleComplex(creal(U[i]), cimag(U[i]));
  }
  checkCudaErrors(cudaMemcpyToSymbol(d_U, h_U, sizeof(cuDoubleComplex) * dim * dim));

  _qstate_operate_unitary_gpu_static(qstate, dim, m, n);

  checkCudaErrors(cudaFreeHost(h_U));

  SUC_RETURN(true);
}

__global__ void cuda_qstate_update_prob_array(cuDoubleComplex* d_camp, double* d_prob_array,
					      int state_num)
{
  double p = 0.0;
  int i = blockIdx.x * blockDim.x + threadIdx.x;

  if (i < state_num) {
    p = cuCabs(d_camp[i]);
    d_prob_array[i] = p * p;
  }
}

static bool _qstate_get_measured_char_gpu(QState* qstate, int mnum, int* qid, char* mchar)
/* not update qstate, get measured char only */
{
  cuDoubleComplex*	d_buffer_0   = qstate->d_buffer_0;
  cuDoubleComplex*	d_buffer_1   = qstate->d_buffer_1;
  cuDoubleComplex*      d_camp	     = NULL;
  double*		d_prob_array = qstate->d_prob_array;
  double		r	     = 0.0;
  double		prob_s	     = 0.0;
  double		prob_e	     = 0.0;
  int			value	     = 0;
  int			bit	     = 0;
  int			blocksize    = BLOCKSIZE;
  dim3			block (blocksize, 1, 1);
  dim3			grid ((qstate->state_num + block.x - 1) / block.x, 1, 1);
  int			i;

  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  /* update prob_array, qstate */
  if (qstate->d_prob_updated == false) {
    if (qstate->d_buf_id == 0) d_camp = d_buffer_0;
    else d_camp = d_buffer_1;

    cuda_qstate_update_prob_array<<< grid, block >>>(d_camp, d_prob_array,
						     qstate->state_num);
    qstate->d_prob_updated = true;

    if (!(qstate_update_host_memory(qstate)))
      ERR_RETURN(ERROR_QSTATE_UPDATE_HOST_MEMORY, false);
  }
  
  r = rand() / (double)RAND_MAX;
  for (i=0; i<qstate->state_num; i++) {
    prob_s = prob_e;
    //prob_e = qstate->prob_array[i];
    prob_e = prob_s + qstate->prob_array[i];
    if (r >= prob_s && r < prob_e) {
      value = i;
      break;
    }
  }

  for (i=0; i<mnum; i++) {
    bit = (value >> (qstate->qubit_num - qid[i] - 1)) % 2;
    if (bit == 0) mchar[i] = 0;
    else mchar[i] = 1;
  }

  SUC_RETURN(true);
}

static bool _qstate_measure_gpu(QState* qstate, int mnum, int* qid,
				char* measured_char, bool measure_update)
/* ececute one shot measurement and update qstate according to measure_update flag */
{
  int			i, x;
  int			mval_qid     = 0;

  if (measure_update == true) { /* measure and update qstate */
    _qstate_get_measured_char_gpu(qstate, mnum, qid, measured_char);

    /* update qstate */
    for (i=0; i<mnum; i++) {
      mval_qid += ((int)measured_char[i] << (mnum - 1 - i));
    }
    for (i=0; i<qstate->state_num; i++) {
      if (!(select_bits(&x, i, mnum, qstate->qubit_num, qid)))
	ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
      if (x != mval_qid) qstate->camp[i] = 0.0;
    }
    if (!(qstate_normalize(qstate))) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

    if (!(qstate_update_device_memory(qstate)))
      ERR_RETURN(ERROR_QSTATE_UPDATE_DEVICE_MEMORY, false);

    qstate->prob_updated = false;
    qstate->d_prob_updated = false;
  }

  else { /* measure but not update qstate */
    _qstate_get_measured_char_gpu(qstate, mnum, qid, measured_char);
  }

  SUC_RETURN(true);
}

bool qstate_operate_qcirc_gpu(QState* qstate, CMem* cmem, QCirc* qcirc, bool measure_update)
/* one shot qcirc execution */
{
  QGate*		qgate	      = NULL;	/* quantum gate in quantum circuit */
  int                   i;
  int			dim	      = 0;
  COMPLEX*		U	      = NULL;
  cuDoubleComplex*	h_U	      = NULL;
  int                   q0	      = -1;
  int                   q1	      = -1;
  bool                  compo	      = false;	/* U is composite or not */
  int			mnum;
  int*			qid	      = NULL;
  int*			cid	      = NULL;
  bool			last;
  char*			measured_char = NULL;

  /* error check */
  if ((qstate == NULL || qcirc == NULL) ||
      (qstate->qubit_num < qcirc->qubit_num) ||
      (cmem != NULL && cmem->cmem_num < qcirc->cmem_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  checkCudaErrors(cudaMallocHost((void**)&h_U, sizeof(cuDoubleComplex) * 16));

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
	  ERR_RETURN(ERROR_GBANK_GET_UNITARY,false);
	}
	
	for (i=0; i<dim*dim; i++) {
	  h_U[i] = make_cuDoubleComplex(creal(U[i]), cimag(U[i]));
	}
	checkCudaErrors(cudaMemcpyToSymbol(d_U, h_U, sizeof(cuDoubleComplex) * dim * dim));

	if (compo == false && kind_is_controlled(qgate->kind) == true) {
	  if (!(_qstate_operate_controlled_gate_gpu_static(qstate, q0, q1))) {
	    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	  }
	}
	else {
	  if (!(_qstate_operate_unitary_gpu_static(qstate, dim, q0, q1))) {
	    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
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
	if (!(_qstate_measure_gpu(qstate, mnum, qid, measured_char, measure_update)))
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

  checkCudaErrors(cudaFreeHost(h_U));

  SUC_RETURN(true);
}

bool qstate_operate_measure_gpu(QState* qstate, CMem* cmem, QCirc* qcirc, int shots, char* mchar_shots)
/* qcirc execution and get measurement data (suppose that qcirc includes only measurements) */
{
  char*		measured_char = NULL;
  int*		qid	      = NULL;
  int*		cid	      = NULL;
  QGate*	qgate	      = NULL;
  int		mnum;
  bool		last;
  bool		measure_update;
  bool		ans;
  int		i,j,k;

  if ((qstate == NULL) || (cmem == NULL) || (qcirc == NULL) ||
      (shots < 1) || (mchar_shots == NULL) )
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  qcirc_is_measurement_only(qcirc, &ans);
  if (ans == false) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  
  if (!(measured_char = (char*)malloc(sizeof(char) * qstate->qubit_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
  if (!(cid = (int*)malloc(sizeof(int) * cmem->cmem_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
  if (!(qid = (int*)malloc(sizeof(int) * qstate->qubit_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  qgate = qcirc->first;
  if (!(qgate_get_measurement_attributes((void**)&qgate, qstate->gbank, &mnum, qid, cid, &last))) {
    ERR_RETURN(ERROR_QGATE_GET_NEXT_UNITARY, false);
  }

  // TODO: -> kernel function
  measure_update = false;
  for (i=0; i<shots; i++) {
    if (i < shots - 1) measure_update = false;
    else measure_update = true;

    if (!(_qstate_measure_gpu(qstate, mnum, qid, measured_char, measure_update)))
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

  SUC_RETURN(true);
}

bool qstate_init_gpu(int qubit_num, void** qstate_out)
{
  QState		*qstate	   = NULL;
  int			 state_num = (1 << qubit_num);
  int			 blocksize = BLOCKSIZE;
  dim3			 block (blocksize, 1, 1);
  dim3			 grid ((state_num + block.x - 1) / block.x, 1, 1);
  cuDoubleComplex	 h_buf;

  if ((qubit_num < 1) || (qubit_num > MAX_QUBIT_NUM))
    ERR_RETURN(ERROR_OUT_OF_BOUND,false);
  
  if (!(qstate = (QState*)malloc(sizeof(QState))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  qstate->qubit_num = qubit_num;
  qstate->state_num = state_num;
  qstate->use_gpu = true;

  /* allocate host memory */
  qstate->buf_id = 0;
  if (!(qstate->buffer_0 = (COMPLEX*)malloc(sizeof(COMPLEX) * state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
  if (!(qstate->buffer_1 = (COMPLEX*)malloc(sizeof(COMPLEX) * state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
  qstate->camp = qstate->buffer_0;

  if (!(qstate->prob_array = (double*)malloc(sizeof(double) * state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
  qstate->prob_updated = false;

  /* allocatie device memory */
  qstate->d_buf_id = 0;
  checkCudaErrors(cudaMalloc((void**)&(qstate->d_buffer_0), sizeof(cuDoubleComplex) * state_num));
  
  checkCudaErrors(cudaMalloc((void**)&(qstate->d_buffer_1), sizeof(cuDoubleComplex) * state_num));
  qstate->d_camp = qstate->d_buffer_0;

  checkCudaErrors(cudaMalloc((void**)&(qstate->d_prob_array), sizeof(double) * state_num));
  qstate->d_prob_updated = false;

  /* initialize device memory */
  checkCudaErrors(cudaMemset(qstate->d_buffer_0, 0, sizeof(cuDoubleComplex) * state_num));
  h_buf = make_cuDoubleComplex(1.0, 0.0);
  checkCudaErrors(cudaMemcpy(qstate->d_buffer_0, &h_buf, sizeof(cuDoubleComplex),
			     cudaMemcpyHostToDevice));

  /* set gbank */
  if (!(gbank_init((void**)&(qstate->gbank))))
      ERR_RETURN(ERROR_GBANK_INIT,false);

  *qstate_out = qstate;
  
  SUC_RETURN(true);
}

bool qstate_update_host_memory(QState* qstate)
{
  cuDoubleComplex*	h_camp = NULL;
  int			i;
  
  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  if (qstate->use_gpu == false) SUC_RETURN(true);

  checkCudaErrors(cudaMallocHost((void**)&h_camp, sizeof(cuDoubleComplex) * qstate->state_num));

  checkCudaErrors(cudaMemcpy(h_camp, qstate->d_camp, sizeof(cuDoubleComplex) * qstate->state_num,
			     cudaMemcpyDeviceToHost));

  checkCudaErrors(cudaMemcpy(qstate->prob_array, qstate->d_prob_array, sizeof(double) * qstate->state_num,
			     cudaMemcpyDeviceToHost));
  // qstate->prob_updated = true;
  // qstate->d_prob_updated = true;
  qstate->prob_updated = qstate->d_prob_updated;

  for (i=0; i<qstate->state_num; i++) {
    qstate->camp[i] = h_camp[i].x + h_camp[i].y * COMP_I;
  }

  checkCudaErrors(cudaFreeHost(h_camp));

  SUC_RETURN(true);
}
  
bool qstate_update_device_memory(QState* qstate)
{
  cuDoubleComplex*	h_camp = NULL;
  int			i;
  
  if (qstate == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  if (qstate->use_gpu == false) SUC_RETURN(true);

  checkCudaErrors(cudaMallocHost((void**)&h_camp, sizeof(cuDoubleComplex) * qstate->state_num));

  for (i=0; i<qstate->state_num; i++) {
    h_camp[i] = make_cuDoubleComplex(creal(qstate->camp[i]), cimag(qstate->camp[i]));
  }

  checkCudaErrors(cudaMemcpy(qstate->d_camp, h_camp, sizeof(cuDoubleComplex) * qstate->state_num,
			     cudaMemcpyHostToDevice));

  checkCudaErrors(cudaMemcpy(qstate->d_prob_array, qstate->prob_array, sizeof(double) * qstate->state_num,
			     cudaMemcpyHostToDevice));
  //qstate->prob_updated = true;
  //qstate->d_prob_updated = true;
  qstate->d_prob_updated = qstate->prob_updated;

  checkCudaErrors(cudaFreeHost(h_camp));

  SUC_RETURN(true);
}

void qstate_free_gpu(QState* qstate)
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

  checkCudaErrors(cudaFree(qstate->d_buffer_0)); qstate->d_buffer_0 = NULL;
  checkCudaErrors(cudaFree(qstate->d_buffer_1)); qstate->d_buffer_1 = NULL;
  
  free(qstate);
}
  
#ifdef __cplusplus
}
#endif
