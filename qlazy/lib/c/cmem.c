/*
 *  cmem.c
 */

#include "qlazy.h"

bool cmem_init(int cmem_num, void** cmem_out)
{
  CMem* cmem = NULL;
  
  if (cmem_num < 0) {
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }

  if (!(cmem = (CMem*)malloc(sizeof(CMem))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);

  cmem->cmem_num = cmem_num;
  if (!(cmem->bit_array = (int*)malloc(sizeof(int) * cmem_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);
  for (int i=0; i<cmem_num; i++) cmem->bit_array[i] = 0;

  *cmem_out = cmem;
  
  SUC_RETURN(true);
}

bool cmem_copy(CMem* cmem_in, void** cmem_out)
{
  CMem* cmem = NULL;

  if (cmem_in == NULL || cmem_in->cmem_num < 0)
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(cmem_init(cmem_in->cmem_num, (void**)&cmem)))
    ERR_RETURN(ERROR_CMEM_INIT, NULL);

  memcpy(cmem->bit_array, cmem_in->bit_array, sizeof(int) * cmem_in->cmem_num);
    
  *cmem_out = cmem;
  
  SUC_RETURN(true);
}

void cmem_free(CMem* cmem)
{
  if (cmem == NULL) return;

  if (cmem->bit_array != NULL) {
    free(cmem->bit_array); cmem->bit_array = NULL;
  }
  free(cmem); cmem = NULL;
}
