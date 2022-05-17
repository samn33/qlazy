/*
 *  gpu.cu
 */

#include "qlazy.h"

#ifdef __cplusplus
extern "C" {
#endif

bool gpu_preparation(void)
{
  int *dummy;
  checkCudaErrors(cudaMalloc((void**)&dummy,sizeof(int)*1));
  checkCudaErrors(cudaFree(dummy));

  SUC_RETURN(true);
}

#ifdef __cplusplus
}
#endif
