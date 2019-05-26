/*
 *  cimage.c
 */

#include "qlazy.h"

bool cimage_init(int qubit_num, int step_num, void** cimage_out)
{
  CImage* cimage = NULL;
  int     glen = 20;

  if (!(cimage = (CImage*)malloc(sizeof(CImage))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  
  cimage->qubit_num = qubit_num;
  if (!(cimage->ch = (char**)malloc(sizeof(char*)*qubit_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  
  for (int i=0; i<qubit_num; i++) {
    if (!(cimage->ch[i] = (char*)malloc(sizeof(char)*step_num*glen)))
      ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
    for (int j=0; j<step_num*glen; j++) cimage->ch[i][j] = '-';
    cimage->ch[i][step_num*glen] = '\0';
  }

  *cimage_out = cimage;

  SUC_RETURN(true);
}

void cimage_free(CImage* cimage)
{
  if (cimage != NULL) {
    if (cimage->ch != NULL) {
      for (int i=0; i<cimage->qubit_num; i++) {
	free(cimage->ch[i]);
	cimage->ch[i] = NULL;
      }
      free(cimage->ch); cimage->ch = NULL;
    }
    free(cimage);
  }
}
