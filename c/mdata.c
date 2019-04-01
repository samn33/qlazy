/*
 *  mdata.c
 */

#include "qlazy.h"

MData* mdata_init(int qubit_num, int state_num, int shot_num,
		  int qubit_id[MAX_QUBIT_NUM])
{
  MData* mdata = NULL;

  g_Errno = NO_ERROR;
  
  if (!(mdata = (MData*)malloc(sizeof(MData)))) goto ERROR_EXIT;
  mdata->qubit_num = qubit_num;
  mdata->state_num = state_num;
  mdata->shot_num = shot_num;
  memcpy(mdata->qubit_id, qubit_id, sizeof(int)*MAX_QUBIT_NUM);

  if (!(mdata->freq = (int*)malloc(sizeof(int)*state_num))) goto ERROR_EXIT;
  for (int i=0; i<state_num; i++) mdata->freq[i] = 0;

  return mdata;

 ERROR_EXIT:
  g_Errno = ERROR_MDATA_INIT;
  return NULL;
}

int mdata_print(MData* mdata)
{
  char	state[MAX_QUBIT_NUM+1];
  char	last_state[MAX_QUBIT_NUM+1];

  if (mdata == NULL) goto ERROR_EXIT;

  for (int i=0; i<mdata->state_num; i++) {
    if (get_binstr_from_decimal(state, mdata->qubit_num, i) == FALSE)
      return FALSE;
    if (mdata->freq[i] > 0) {
      printf("frq[%s] = %d\n", state, mdata->freq[i]);
    }
  }

  if (get_binstr_from_decimal(last_state, mdata->qubit_num,
			      mdata->last) == FALSE) return FALSE;
  printf("last state => %s\n", last_state);

  return TRUE;

 ERROR_EXIT:
  g_Errno = ERROR_MDATA_PRINT;
  return FALSE;
}

void mdata_free(MData* mdata)
{
  if (mdata != NULL) {
    if (mdata->freq != NULL) {
      free(mdata->freq); mdata->freq = NULL;
    }
    free(mdata);
  }
}
