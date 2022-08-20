/*
 *  spro.c
 */

#include "qlazy.h"

bool spro_init(char* str, void** spro_out)
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
  int           flg[MAX_MPS_QUBIT_NUM];
  int		i;

  for (i=0; i<MAX_MPS_QUBIT_NUM; i++) flg[i] = OFF;

  if (!line_check_length(str)) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!line_chomp(str)) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!line_remove_space(str)) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* eliminate 1st '+/-' character and set sign */
  if (str[0]=='+') { sign = 1.0; str++; }
  else if (str[0]=='-') { sign = -1.0; str++; }
  else { sign = 1.0; }

  if (!line_split(str, "*", token, &tnum))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  if (!(spro = (SPro*)malloc(sizeof(SPro))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  for (i=0; i<MAX_MPS_QUBIT_NUM; i++) spro->spin_type[i] = NONE;

  spro->coef = 1.0;
  spro->spin_num = 0;
  for (i=0; i<tnum; i++) {
    if ((i==0) && (is_number(token[i])==true)) {
      spro->coef = strtod(token[0], NULL);
    }
    else {
      if (!line_split(token[i], "_", args, &anum))
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      if (anum != 2) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

      if (strcmp(args[0], "X") == 0) {
	if (!(is_decimal(args[1]))) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	spin_id = strtol(args[1], NULL, 10);
	if (spin_id >= MAX_MPS_QUBIT_NUM) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	if (flg[spin_id] == ON) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	flg[spin_id] = ON;
	spro->spin_type[spin_id] = SIGMA_X;
      }
      else if (strcmp(args[0], "x") == 0) {
	if (!(is_decimal(args[1]))) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	spin_id = strtol(args[1], NULL, 10);
	if (spin_id >= MAX_MPS_QUBIT_NUM) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	if (flg[spin_id] == ON) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	flg[spin_id] = ON;
	spro->spin_type[spin_id] = SIGMA_X;
      }
      else if (strcmp(args[0], "Y") == 0) {
	if (!(is_decimal(args[1]))) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	spin_id = strtol(args[1], NULL, 10);
	if (spin_id >= MAX_MPS_QUBIT_NUM) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	if (flg[spin_id] == ON) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	flg[spin_id] = ON;
	spro->spin_type[spin_id] = SIGMA_Y;
      }
      else if (strcmp(args[0], "y") == 0) {
	if (!(is_decimal(args[1]))) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	spin_id = strtol(args[1], NULL, 10);
	if (spin_id >= MAX_MPS_QUBIT_NUM) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	if (flg[spin_id] == ON) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	flg[spin_id] = ON;
	spro->spin_type[spin_id] = SIGMA_Y;
      }
      else if (strcmp(args[0], "Z") == 0) {
	if (!(is_decimal(args[1]))) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	spin_id = strtol(args[1], NULL, 10);
	if (spin_id >= MAX_MPS_QUBIT_NUM) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	if (flg[spin_id] == ON) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	flg[spin_id] = ON;
	spro->spin_type[spin_id] = SIGMA_Z;
      }
      else if (strcmp(args[0], "z") == 0) {
	if (!(is_decimal(args[1]))) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	spin_id = strtol(args[1], NULL, 10);
	if (spin_id >= MAX_MPS_QUBIT_NUM) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	if (flg[spin_id] == ON) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
	flg[spin_id] = ON;
	spro->spin_type[spin_id] = SIGMA_Z;
      }
      else {
	ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
      }
      spro->spin_num = MAX(spro->spin_num, spin_id);
    }
  }
  spro->coef *= sign;
  spro->spin_num += 1;

  *spro_out = spro;
  
  SUC_RETURN(true);
}

void spro_free(SPro* spro)
{
  if (spro != NULL) free(spro);
}
