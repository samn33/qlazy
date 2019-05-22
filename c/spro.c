/*
 *  spro.c
 */

#include "qlazy.h"

int spro_init(char* str, void** spro_out)
/*
  [input string format (example)]
  "3.0-2.0*Z_0*X_1*Y_3"
 */
{
  SPro*		spro = NULL;
  char*		token[TOKEN_NUM];
  char*		args[TOKEN_NUM];
  double	sign;
  int		tnum;
  int		anum;
  int		spin_id;
  int           flg[MAX_QUBIT_NUM];

  g_Errno = NO_ERROR;

  for (int i=0; i<MAX_QUBIT_NUM; i++) flg[i] = OFF;

  if (line_check_length(str) == FALSE) goto ERROR_EXIT;
  line_chomp(str);
  line_remove_space(str);

  /* eliminate 1st '+/-' character and set sign */
  if (str[0]=='+') { sign = 1.0; str++; }
  else if (str[0]=='-') { sign = -1.0; str++; }
  else { sign = 1.0; }

  tnum = line_split(str, "*", token);
  
  if (!(spro = (SPro*)malloc(sizeof(SPro)))) goto ERROR_EXIT;
  for (int i=0; i<MAX_QUBIT_NUM; i++) spro->spin_type[i] = NONE;

  spro->coef = 1.0;
  spro->spin_num = 0;
  for (int i=0; i<tnum; i++) {
    if ((i==0) && (is_number(token[i])==TRUE)) {
      spro->coef = strtod(token[0], NULL);
    }
    else {
      anum = line_split(token[i], "_", args);
      if (anum != 2) goto ERROR_EXIT;

      if (strcmp(args[0], "X") == 0) {
	if (is_decimal(args[1]) == FALSE) goto ERROR_EXIT;
	spin_id = strtol(args[1], NULL, 10);
	if (spin_id >= MAX_QUBIT_NUM) goto ERROR_EXIT;
	if (flg[spin_id] == ON) goto ERROR_EXIT;
	flg[spin_id] = ON;
	spro->spin_type[spin_id] = SIGMA_X;
      }
      else if (strcmp(args[0], "x") == 0) {
	if (is_decimal(args[1]) == FALSE) goto ERROR_EXIT;
	spin_id = strtol(args[1], NULL, 10);
	if (spin_id >= MAX_QUBIT_NUM) goto ERROR_EXIT;
	if (flg[spin_id] == ON) goto ERROR_EXIT;
	flg[spin_id] = ON;
	spro->spin_type[spin_id] = SIGMA_X;
      }
      else if (strcmp(args[0], "Y") == 0) {
	if (is_decimal(args[1]) == FALSE) goto ERROR_EXIT;
	spin_id = strtol(args[1], NULL, 10);
	if (spin_id >= MAX_QUBIT_NUM) goto ERROR_EXIT;
	if (flg[spin_id] == ON) goto ERROR_EXIT;
	flg[spin_id] = ON;
	spro->spin_type[spin_id] = SIGMA_Y;
      }
      else if (strcmp(args[0], "y") == 0) {
	if (is_decimal(args[1]) == FALSE) goto ERROR_EXIT;
	spin_id = strtol(args[1], NULL, 10);
	if (spin_id >= MAX_QUBIT_NUM) goto ERROR_EXIT;
	if (flg[spin_id] == ON) goto ERROR_EXIT;
	flg[spin_id] = ON;
	spro->spin_type[spin_id] = SIGMA_Y;
      }
      else if (strcmp(args[0], "Z") == 0) {
	if (is_decimal(args[1]) == FALSE) goto ERROR_EXIT;
	spin_id = strtol(args[1], NULL, 10);
	if (spin_id >= MAX_QUBIT_NUM) goto ERROR_EXIT;
	if (flg[spin_id] == ON) goto ERROR_EXIT;
	flg[spin_id] = ON;
	spro->spin_type[spin_id] = SIGMA_Z;
      }
      else if (strcmp(args[0], "z") == 0) {
	if (is_decimal(args[1]) == FALSE) goto ERROR_EXIT;
	spin_id = strtol(args[1], NULL, 10);
	if (spin_id >= MAX_QUBIT_NUM) goto ERROR_EXIT;
	if (flg[spin_id] == ON) goto ERROR_EXIT;
	flg[spin_id] = ON;
	spro->spin_type[spin_id] = SIGMA_Z;
      }
      else {
	goto ERROR_EXIT;
      }
      spro->spin_num = MAX(spro->spin_num, spin_id);
    }
  }
  spro->coef *= sign;
  spro->spin_num += 1;

  *spro_out = spro;
  
  return TRUE;

 ERROR_EXIT:
  g_Errno = ERROR_SPRO_INIT;
  return FALSE;
}

void spro_free(SPro* spro)
{
  if (spro != NULL) free(spro);
}
