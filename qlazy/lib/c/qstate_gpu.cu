/*
 *  qstate_gpu.cu
 */
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"

#ifdef __cplusplus
extern "C" {
#endif

#include "qlazy.h"

#define BLOCKSIZE 32
#define STREAM_NUM 4

__constant__ cuDoubleComplex d_U[16];

__global__ void cuda_qstate_operate_unitary2(cuDoubleComplex* d_camp_out, cuDoubleComplex* d_camp_in,
					     int qubit_num, int state_size, int state_offset, int n)
{
  unsigned int	ix, iy, nx;
  int		nn, i, p, pp, sign, offset;

  nn = qubit_num - n - 1;
  
  ix = blockIdx.x * blockDim.x + threadIdx.x;
  iy = blockIdx.y * blockDim.y + threadIdx.y;
  nx = gridDim.x * blockDim.x;
  i = (int)(iy * nx + ix);

  if (i < state_size) {
    i += state_offset;
    p = (i >> nn) % 2;
    pp = p ^ 1;
    sign = (pp << 1) - 1; // pp=0 -> -1, pp=1 -> +1
    offset = sign * (1 << nn);

    d_camp_out[i] = cuCadd(cuCmul(d_U[IDX2(p,p)], d_camp_in[i]), cuCmul(d_U[IDX2(p,pp)], d_camp_in[i + offset]));
  }
}

__global__ void cuda_qstate_operate_unitary4(cuDoubleComplex* d_camp_out, cuDoubleComplex* d_camp_in,
					     int qubit_num, int state_size, int state_offset, int m, int n)
{
  unsigned int		ix, iy, nx;
  int			mm, nn, i, p, pp, q, qq;
  int			l, sign_p, sign_q, off_p, off_q;
  cuDoubleComplex	camp;
  
  mm = qubit_num - m - 1;
  nn = qubit_num - n - 1;

  ix = blockIdx.x * blockDim.x + threadIdx.x;
  iy = blockIdx.y * blockDim.y + threadIdx.y;
  nx = gridDim.x * blockDim.x;
  i = (int)(iy * nx + ix);

  if (i < state_size) {
    i += state_offset;
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
    camp = cuCadd(camp, cuCmul(d_U[IDX4(l, (l^3))], d_camp_in[i + off_q + off_p]));
    d_camp_out[i] = camp;
  }
}

static bool _qstate_operate_unitary_gpu_stream(QState* qstate, int dim, int m, int n,
					       cudaStream_t* streams)
{
  int			 qubit_num  = qstate->qubit_num;
  cuDoubleComplex*	 d_buffer_0 = qstate->d_buffer_0;
  cuDoubleComplex*	 d_buffer_1 = qstate->d_buffer_1;
  int			 i;
  int                    stream_num = STREAM_NUM;
  int			 size	    = qstate->state_num / stream_num;
  int			 offset	    = 0;

  if ((qstate == NULL) || (qstate->use_gpu == false) || (dim < 0))
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (size == 0) {
    size = 1;
    stream_num = qstate->state_num;
  }

  int	blocksize = BLOCKSIZE;
  dim3	block (blocksize, 1, 1);
  dim3	grid ((size + block.x - 1) / block.x, 1, 1);

  if (dim == 2) {
    /* 0 -> 1 */
    if (qstate->d_buf_id == 0) {
      for (i=0; i<stream_num; i++) {
	offset = i * size;
	cuda_qstate_operate_unitary2<<< grid, block, 0, streams[i] >>>(d_buffer_1, d_buffer_0,
								       qubit_num, size, offset, m);
      }
      qstate->d_buf_id = 1;
      qstate->d_camp = qstate->d_buffer_1;
    }
    /* 1 -> 0 */
    else {
      for (i=0; i<stream_num; i++) {
	offset = i * size;
	cuda_qstate_operate_unitary2<<< grid, block, 0, streams[i] >>>(d_buffer_0, d_buffer_1,
								       qubit_num, size, offset, m);
      }
      qstate->d_buf_id = 0;
      qstate->d_camp = qstate->d_buffer_0;
    }
  }
  else if (dim == 4) {
    /* 0 -> 1 */
    if (qstate->d_buf_id == 0) {
      for (i=0; i<stream_num; i++) {
	offset = i * size;
	cuda_qstate_operate_unitary4<<< grid, block, 0, streams[i] >>>(d_buffer_1, d_buffer_0,
								       qubit_num, size, offset,
								       m, n);
      }
      qstate->d_buf_id = 1;
      qstate->d_camp = qstate->d_buffer_1;
    }
    /* 1 -> 0 */
    else {
      for (i=0; i<stream_num; i++) {
	offset = i * size;
	cuda_qstate_operate_unitary4<<< grid, block, 0, streams[i] >>>(d_buffer_0, d_buffer_1,
								       qubit_num, size, offset,
								       m, n);
      }
      qstate->d_buf_id = 0;
      qstate->d_camp = qstate->d_buffer_0;
    }
  }
  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }

  for (i=0; i<STREAM_NUM; i++) {
    checkCudaErrors(cudaStreamSynchronize(streams[i]));
  }

  SUC_RETURN(true);
}

bool qstate_operate_unitary_gpu(QState* qstate, COMPLEX* U, int dim, int m, int n)
{
  int			i;
  cuDoubleComplex*	h_U = NULL;
  cudaStream_t*         streams = NULL;

  if ((qstate == NULL) || (qstate->use_gpu == false) || (U == NULL) || (dim < 0))
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (!(streams = (cudaStream_t*)malloc(sizeof(cudaStream_t) * STREAM_NUM)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  for (i=0; i<STREAM_NUM; i++) {
    checkCudaErrors(cudaStreamCreate(&streams[i]));
  }

  checkCudaErrors(cudaMallocHost((void**)&h_U, sizeof(cuDoubleComplex) * 16));

  for (i=0; i<dim*dim; i++) {
    h_U[i] = make_cuDoubleComplex(creal(U[i]), cimag(U[i]));
  }
  checkCudaErrors(cudaMemcpyToSymbol(d_U, h_U, sizeof(cuDoubleComplex) * dim * dim));

  _qstate_operate_unitary_gpu_stream(qstate, dim, m, n, streams);

  checkCudaErrors(cudaFreeHost(h_U));

  for (i=0; i<STREAM_NUM; i++) {
    checkCudaErrors(cudaStreamDestroy(streams[i]));
  }

  free(streams); streams = NULL;

  SUC_RETURN(true);
}

bool qstate_operate_qcirc_gpu(QState* qstate, CMem* cmem, QCirc* qcirc)
{
  QGate*		qgate = NULL;	/* quantum gate in quantum circuit */
  double		angle = 0.0;	/* measurement angle */
  double		phase = 0.0;	/* measurement phase */
  int			qubit_id[MAX_QUBIT_NUM];
  int			mes_id;
  int                   i;
  int			dim   = 0;
  COMPLEX*		U     = NULL;
  cuDoubleComplex*	h_U   = NULL;
  int                   q0 = -1;
  int                   q1 = -1;
  cudaStream_t*         streams = NULL;

  /* error check */
  if ((qstate == NULL || qcirc == NULL) ||
      (qstate->qubit_num < qcirc->qubit_num) ||
      (cmem != NULL && cmem->cmem_num < qcirc->cmem_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(streams = (cudaStream_t*)malloc(sizeof(cudaStream_t) * STREAM_NUM)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  for (i=0; i<STREAM_NUM; i++) {
    checkCudaErrors(cudaStreamCreate(&streams[i]));
  }
  
  checkCudaErrors(cudaMallocHost((void**)&h_U, sizeof(cuDoubleComplex) * 16));

  qgate = qcirc->first;
  while (qgate != NULL) {

    if ((qgate->ctrl == -1) ||
	((qgate->ctrl != -1) && (cmem->bit_array[qgate->ctrl] == 1))) {

      /* unitary gate */
      if (kind_is_unitary(qgate->kind) == true) {

	if (!(qgate_get_next_unitary((void**)&qgate, qstate->gbank, &dim, &q0, &q1, (void**)&U, true))) {
	  ERR_RETURN(ERROR_GBANK_GET_UNITARY,false);
	}
	
	for (i=0; i<dim*dim; i++) {
	  h_U[i] = make_cuDoubleComplex(creal(U[i]), cimag(U[i]));
	}
	checkCudaErrors(cudaMemcpyToSymbol(d_U, h_U, sizeof(cuDoubleComplex) * dim * dim));

	if (!(_qstate_operate_unitary_gpu_stream(qstate, dim, q0, q1, streams))) {
	  ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
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
      	qubit_id[0] = qgate->qid[0];
      	if (!(qstate_measure(qstate, angle, phase, 1, qubit_id, &mes_id)))
      	  ERR_RETURN(ERROR_QSTATE_MEASURE, false);
      	if (mes_id < 0 || mes_id > 1) ERR_RETURN(ERROR_QSTATE_MEASURE, false);
      	if (qgate->c != -1) cmem->bit_array[qgate->c] = (BYTE)mes_id; /* measured value is stored to classical register */
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

  for (i=0; i<STREAM_NUM; i++) {
    checkCudaErrors(cudaStreamDestroy(streams[i]));
  }

  free(streams); streams = NULL;

  SUC_RETURN(true);
}

bool qstate_init_gpu(int qubit_num, void** qstate_out)
{
  QState		*qstate	   = NULL;
  int			 state_num = (1 << qubit_num);
  int			 blocksize = BLOCKSIZE;
  dim3			 block (blocksize, 1, 1);
  dim3			 grid ((state_num + block.x - 1) / block.x, 1, 1);
  cuDoubleComplex	 h_buf[1];

  if ((qubit_num < 1) || (qubit_num > MAX_QUBIT_NUM))
    ERR_RETURN(ERROR_OUT_OF_BOUND,false);
  
  if (!(qstate = (QState*)malloc(sizeof(QState))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  qstate->qubit_num = qubit_num;
  qstate->state_num = state_num;
  qstate->use_gpu = true;

  /* host memory */
  qstate->buf_id = 0;
  if (!(qstate->buffer_0 = (COMPLEX*)malloc(sizeof(COMPLEX) * state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  if (!(qstate->buffer_1 = (COMPLEX*)malloc(sizeof(COMPLEX) * state_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  qstate->camp = qstate->buffer_0;

  /* allocatie device memory */
  qstate->d_buf_id = 0;
  checkCudaErrors(cudaMalloc((void**)&(qstate->d_buffer_0), sizeof(cuDoubleComplex) * state_num));
  
  checkCudaErrors(cudaMalloc((void**)&(qstate->d_buffer_1), sizeof(cuDoubleComplex) * state_num));
  qstate->d_camp = qstate->d_buffer_0;

  /* initialize device memory */
  checkCudaErrors(cudaMemset(qstate->d_buffer_0, 0, sizeof(cuDoubleComplex) * state_num));
  h_buf[0] = make_cuDoubleComplex(1.0, 0.0);
  checkCudaErrors(cudaMemcpy(qstate->d_buffer_0, h_buf, sizeof(cuDoubleComplex),
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
