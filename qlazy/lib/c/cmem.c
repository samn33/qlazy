/*
 *  cmem.c
 */

#include "qlazy.h"

bool cmem_init(int cmem_num, void** cmem_out)
{
  CMem* cmem = NULL;
  int	i;

  if (cmem_num < 1) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(cmem = (CMem*)malloc(sizeof(CMem))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);
    
  cmem->cmem_num = cmem_num;
  if (!(cmem->bit_array = (BYTE*)malloc(sizeof(BYTE) * cmem_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);
  for (i=0; i<cmem_num; i++) cmem->bit_array[i] = 0;

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

  memcpy(cmem->bit_array, cmem_in->bit_array, sizeof(BYTE) * cmem_in->cmem_num);
    
  *cmem_out = cmem;
  
  SUC_RETURN(true);
}

bool cmem_get_bits(CMem* cmem, void** bits_out)
{
  BYTE* bits = NULL;
  
  if (cmem == NULL)
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (!(bits = (BYTE*)malloc(sizeof(BYTE) * cmem->cmem_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  memcpy(bits, cmem->bit_array, sizeof(BYTE) * cmem->cmem_num);

  *bits_out = bits;
  
  SUC_RETURN(true);
}

bool cmem_set_bits(CMem* cmem, BYTE* bits, int num)
{
  if ((cmem == NULL) || (cmem->cmem_num != num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  memcpy(cmem->bit_array, bits, sizeof(BYTE) * cmem->cmem_num);
  
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
