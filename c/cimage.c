/*
 *  cimage.c
 */

#include "qlazy.h"

CImage* cimage_init(int qubit_num, int step_num)
{
  CImage* cimage = NULL;
  int     glen = 20;

  g_Errno = NO_ERROR;
  
  if (!(cimage = (CImage*)malloc(sizeof(CImage)))) goto ERROR_EXIT;;
  cimage->qubit_num = qubit_num;
  if (!(cimage->ch = (char**)malloc(sizeof(char*)*qubit_num)))
    goto ERROR_EXIT;
  for (int i=0; i<qubit_num; i++) {
    if (!(cimage->ch[i] = (char*)malloc(sizeof(char)*step_num*glen)))
      goto ERROR_EXIT;
    for (int j=0; j<step_num*glen; j++) cimage->ch[i][j] = '-';
    cimage->ch[i][step_num*glen] = '\0';
  }

  return cimage;

 ERROR_EXIT:
  g_Errno = ERROR_CIMAGE_INIT;
  return NULL;
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
