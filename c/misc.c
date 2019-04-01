/*
 *  misc.c
 */

#include "qlazy.h"

int get_binstr_from_decimal(char* binstr, int qubit_num, int decimal)
{
  int d = decimal;
  int max_decimal = (1<<MAX_QUBIT_NUM) - 1;
  int pos = 0;

  g_Errno = NO_ERROR;
  
  if (d >= max_decimal) return FALSE;

  for (int i=0; i<qubit_num; i++) binstr[i] = '0';
  binstr[qubit_num] = '\0';

  while (d > 0) {
    if (d%2 == 0) binstr[qubit_num-pos-1] = '0';
    else binstr[qubit_num-pos-1] = '1';
    d = d/2;
    pos++;
  }
  
  return TRUE;
}

int select_bits(int* bits_out, int bits_in, int digits_out, int digits_in,
		int digit_array[MAX_QUBIT_NUM])
{
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
