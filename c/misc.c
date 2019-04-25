/*
 *  misc.c
 */

#include "qlazy.h"

int get_binstr_from_decimal(char* binstr, int qubit_num, int decimal, int zflag)
{
  /*
    [description]
    - binstr:    characters expression of state id (ex:'110') <- outut of this function
    - qubit_num: number of qubits (ex:3)
    - decimal:   state id (ex:6)
    - zflag:     ON -> character of the state is '0'/'1'
                 OFF->character of the state is 'u'/'d'
   */
  int	d	    = decimal;
  int	max_decimal = (1<<MAX_QUBIT_NUM) - 1;
  int	pos	    = 0;
  char	up,dn;

  g_Errno = NO_ERROR;

  if (d >= max_decimal) return FALSE;

  if (zflag == ON) {
    up = '0';
    dn = '1';
  }
  else {
    up = 'u';
    dn = 'd';
  }
  
  for (int i=0; i<qubit_num; i++) binstr[i] = up;
  binstr[qubit_num] = '\0';

  while (d > 0) {
    if (d%2 == 0) binstr[qubit_num-pos-1] = up;
    else binstr[qubit_num-pos-1] = dn;
    d = d/2;
    pos++;
  }
  
  return TRUE;
}

int select_bits(int* bits_out, int bits_in, int digits_out, int digits_in,
		int digit_array[MAX_QUBIT_NUM])
{
  /*
    [description]
    - bits_out:     after selecting bits (ex: '01') <- output of this function
    - bits_in:      before selecting bits = whole bits (ex: '111010')
    - digits_out:   number of output digits (ex: 2)
    - digits_in:    number of whole digits (ex: 6)
    - digits_array: qubits array you want to output (ex: {3,4})
   */
  
  if ((digits_in < 1) || (digits_in > MAX_QUBIT_NUM)) return FALSE;
  if ((digits_out < 1) || (digits_out > MAX_QUBIT_NUM)) return FALSE;
  if (bits_in < 0) return FALSE;

  int bits = 0;
  int count = 0;
  for (int i=digits_out-1; i>=0; i--) {
    if (digit_array[i] >= digits_in) return FALSE;
    bits += (((bits_in>>(digits_in-1-digit_array[i]))%2) << count);
    count++;
  }
  
  *bits_out = bits;
  
  return TRUE;
}
