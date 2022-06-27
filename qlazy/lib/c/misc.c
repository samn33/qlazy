/*
 *  misc.c
 */

#include "qlazy.h"

bool line_check_length(char* str)
{
  int pos = 0;

  while (1) {
    if (str[pos] == '\0') { pos++; break; }
    else pos++;
  }

  if (pos > LINE_STRLEN) return false;
  else return true;
}

bool line_is_blank(char* str)
{
  char* p = str;
  while ((*p==' ') || (*p=='\t') || (*p=='\n') ||
	 (*p=='\v') || (*p=='\f')|| (*p=='\r')) p++;
  if (*p == '\0') return true;
  else return false;
}

bool line_is_comment(char* str)
{
  if (str[0] == '#') return true;
  else return false;
}

bool line_chomp(char* str)
{
  if (str == NULL) return false;
  char* p;
  p = strchr(str,'\n');
  if (p != NULL) {
    *p = '\0';
  }
  return true;
}

bool line_split(char* str, const char* delim, char* outlist[], int* tnum)
{
  char* tk;
  int cnt = 0;
  tk = strtok(str,delim);
  while (tk!=NULL && cnt<TOKEN_NUM) {
    outlist[cnt++] = tk;
    tk = strtok(NULL,delim);
  }
  *tnum = cnt;
  
  return true;
}

bool line_getargs(char* str, char* args[], int* anum)
/* "Func(foo,bar)" => "Func","foo","bar" */
{
  int	cnt = 0;
  int   a;
  while (1) {
    if (str[cnt] == ')') {
      str[cnt] = '\0';
      break;
    }
    else if (str[cnt] == '(') {
      str[cnt] = ' ';
    }
    else if (str[cnt] == ',') {
      str[cnt] = ' ';
    }
    else if (str[cnt] == '\0') {
      break;
    }
    cnt++;
  }
  line_split(str, " ", args, &a);
  *anum = a;
  
  return true;
}

bool line_join_token(char* dst, char* token[], int ini, int fin)
{
  int dpos = 0;
  int tpos = 0;
  int i;

  for (i=ini; i<fin; i++) {
    tpos = 0;
    while (1) {
      if (token[i][tpos] == '\0') {
	dst[dpos++] = ' ';
	break;
      }
      else {
	dst[dpos++] = token[i][tpos++];
      }
    }
  }
  dst[dpos] = '\0';

  return true;
}

bool line_remove_space(char* str)
{
  int pos = 0;
  int cnt = 0;

  if (str == NULL) return false;

  while(str[pos] != '\0') {
    if (str[pos] != ' ') {
      str[cnt++] = str[pos++];
    }
    else {
      pos++;
      str[cnt++] = str[pos++];
    }
  }
  str[cnt] = '\0';

  return true;
}

bool is_number(char* str)
{
  int pos = 0;
  
  if (str == NULL) return false;

  /* 1st character */
  if (!(isdigit(str[pos])) && (str[pos]!='.') &&
      (str[pos]!='+') && (str[pos]!='-')) return false;
  /* 2nd and subsequent */
  pos++;
  while ((str[pos] != '\0') && (pos < TOKEN_STRLEN)) {
    if (!(isdigit(str[pos])) && (str[pos]!='.')) return false;
    pos++;
  }

  return true;
}

bool is_decimal(char* str)
{
  int pos = 0;
  
  if (str == NULL) return false;

  /* 1st character */
  if (!(isdigit(str[pos])) && (str[pos]!='+') && (str[pos]!='-'))
    return false;
  /* 2nd and subsequent */
  pos++;
  while ((str[pos] != '\0') && (pos < TOKEN_STRLEN)) {
    if (!(isdigit(str[pos]))) return false;
    pos++;
  }

  return true;
}

bool binstr_from_decimal(char* binstr, int qubit_num, int decimal, int zflag)
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
  int   i;

  if (d >= max_decimal) return false;

  if (zflag == ON) {
    up = '0';
    dn = '1';
  }
  else {
    up = 'u';
    dn = 'd';
  }
  
  for (i=0; i<qubit_num; i++) binstr[i] = up;
  binstr[qubit_num] = '\0';

  while (d > 0) {
    if (d%2 == 0) binstr[qubit_num-pos-1] = up;
    else binstr[qubit_num-pos-1] = dn;
    d = d/2;
    pos++;
  }
  
  return true;
}

int bit_permutation(int bits_in, int qnum, int qnum_part, int* qid)
/*
  [example]
  bits_in: abcdef (<-- binary array)
  qnum_part: 3
  qid: [4,0,2,...]
  --> bits_out: eacbdf
*/
{
  int	bits_out = 0;
  int	bit	 = 0;
  int	now	 = 0;
  bool	flg[MAX_QUBIT_NUM];
  int   i;

  for (i=0; i<MAX_QUBIT_NUM; i++) flg[i] = false;

  for (i=0; i<qnum_part; i++) {
    bit = (bits_in>>(qnum-1-qid[i]))&0x1;
    bits_out += (bit<<(qnum-1-i));
    flg[qid[i]] = true;
  }

  now = qnum_part;
  for (i=0; i<qnum; i++) {
    if (flg[i] == false) {
      bit = (bits_in>>(qnum-1-i))&0x1;
      bits_out += (bit<<(qnum-1-now));
      now++;
    }
  }
  
  return bits_out;
}

int* bit_permutation_array(int length, int qnum, int qnum_part, int* qid)
{
  int* index = NULL;
  int  i;

  if (!(index = (int*)malloc(sizeof(int)*length))) {
    printf("Error: can't alloc memory\n");
    exit(1);
  }  

  for (i=0; i<length; i++) {
    index[i] = bit_permutation(i, qnum, qnum_part, qid);
  }

  return index;
}

bool select_bits(int* bits_out, int bits_in, int digits_out, int digits_in, int* digit_array)
{
  /*
    [description]
    - bits_out:     after selecting bits (ex: '01') <- output of this function
    - bits_in:      before selecting bits = whole bits (ex: '111010')
    - digits_out:   number of output digits (ex: 2)
    - digits_in:    number of whole digits (ex: 6)
    - digits_array: qubits array you want to output (ex: {3,4})
   */
  int i;
  
  if ((digits_in < 1) || (digits_in > MAX_QUBIT_NUM) ||
      (digits_out < 1) || (digits_out > MAX_QUBIT_NUM) || (bits_in < 0))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  int bits = 0;
  int count = 0;
  for (i=digits_out-1; i>=0; i--) {
    if (digit_array[i] >= digits_in) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    bits += (((bits_in>>(digits_in-1-digit_array[i]))%2) << count);
    count++;
  }
  
  *bits_out = bits;
  
  SUC_RETURN(true);
}

bool is_power_of_2(int n)
{
  int log2_n;
  double diff;
  
  log2_n = (int)log2((double)n);
  diff = log2((double)n) - (double)log2_n;
  if (fabs(diff) < MIN_DOUBLE) return true;
  else return false;
}

int kind_get_qid_size(Kind kind)
{
  int qid_size;

  switch (kind) {
  case PAULI_X:
  case PAULI_Y:
  case PAULI_Z:
  case ROOT_PAULI_X:
  case ROOT_PAULI_X_:
  case HADAMARD:
  case PHASE_SHIFT_S:
  case PHASE_SHIFT_S_:
  case PHASE_SHIFT_T:
  case PHASE_SHIFT_T_:
  case PHASE_SHIFT:
  case ROTATION_X:
  case ROTATION_Y:
  case ROTATION_Z:
  case ROTATION_U1:
  case ROTATION_U2:
  case ROTATION_U3:
  case MEASURE:
  case MEASURE_X:
  case MEASURE_Y:
  case MEASURE_Z:
  case RESET:
    qid_size = 1;
    break;
  case CONTROLLED_X:
  case CONTROLLED_Y:
  case CONTROLLED_Z:
  case CONTROLLED_XR:
  case CONTROLLED_XR_:
  case CONTROLLED_H:
  case CONTROLLED_S:
  case CONTROLLED_S_:
  case CONTROLLED_T:
  case CONTROLLED_T_:
  case CONTROLLED_P:
  case CONTROLLED_RX:
  case CONTROLLED_RY:
  case CONTROLLED_RZ:
  case CONTROLLED_U1:
  case CONTROLLED_U2:
  case CONTROLLED_U3:
  case SWAP_QUBITS:
  case MEASURE_BELL:
  case IDENTITY:
    qid_size = 2;
    break;
  default:
    qid_size = -1; /* error */
    break;
  }
  
  return qid_size;
}

int kind_get_para_size(Kind kind)
{
  int para_size;

  switch (kind) {
  case PAULI_X:
  case PAULI_Y:
  case PAULI_Z:
  case ROOT_PAULI_X:
  case ROOT_PAULI_X_:
  case HADAMARD:
  case PHASE_SHIFT_S:
  case PHASE_SHIFT_S_:
  case PHASE_SHIFT_T:
  case PHASE_SHIFT_T_:
  case MEASURE:
  case MEASURE_X:
  case MEASURE_Y:
  case MEASURE_Z:
  case RESET:
  case CONTROLLED_X:
  case CONTROLLED_Y:
  case CONTROLLED_Z:
  case CONTROLLED_XR:
  case CONTROLLED_XR_:
  case CONTROLLED_H:
  case CONTROLLED_S:
  case CONTROLLED_S_:
  case CONTROLLED_T:
  case CONTROLLED_T_:
  case SWAP_QUBITS:
  case MEASURE_BELL:
  case IDENTITY:
    para_size = 0;
    break;
  case PHASE_SHIFT:
  case ROTATION_X:
  case ROTATION_Y:
  case ROTATION_Z:
  case ROTATION_U1:
  case CONTROLLED_P:
  case CONTROLLED_RX:
  case CONTROLLED_RY:
  case CONTROLLED_RZ:
  case CONTROLLED_U1:
    para_size = 1;
    break;
  case ROTATION_U2:
  case CONTROLLED_U2:
    para_size = 2;
    break;
  case ROTATION_U3:
  case CONTROLLED_U3:
    para_size = 3;
    break;
  default:
    para_size = -1;  /* error */
    break;
  }
  
  return para_size;
}

bool kind_is_measurement(Kind kind)
{
  bool is_measurement;
  
  switch (kind) {
  case MEASURE:
  case MEASURE_X:
  case MEASURE_Y:
  case MEASURE_Z:
  case MEASURE_BELL:
    is_measurement = true;
    break;
  default:
    is_measurement = false;
    break;
  }

  return is_measurement;
}

bool kind_is_reset(Kind kind)
{
  bool is_reset;
  
  switch (kind) {
  case RESET:
    is_reset = true;
    break;
  default:
    is_reset = false;
    break;
  }

  return is_reset;
}

bool kind_is_unitary(Kind kind)
{
  bool is_unitary;
  
  switch (kind) {
  case PAULI_X:
  case PAULI_Y:
  case PAULI_Z:
  case ROOT_PAULI_X:
  case ROOT_PAULI_X_:
  case HADAMARD:
  case PHASE_SHIFT_S:
  case PHASE_SHIFT_S_:
  case PHASE_SHIFT_T:
  case PHASE_SHIFT_T_:
  case CONTROLLED_X:
  case CONTROLLED_Y:
  case CONTROLLED_Z:
  case CONTROLLED_XR:
  case CONTROLLED_XR_:
  case CONTROLLED_H:
  case CONTROLLED_S:
  case CONTROLLED_S_:
  case CONTROLLED_T:
  case CONTROLLED_T_:
  case SWAP_QUBITS:
  case IDENTITY:
  case PHASE_SHIFT:
  case ROTATION_X:
  case ROTATION_Y:
  case ROTATION_Z:
  case ROTATION_U1:
  case CONTROLLED_P:
  case CONTROLLED_RX:
  case CONTROLLED_RY:
  case CONTROLLED_RZ:
  case CONTROLLED_U1:
  case ROTATION_U2:
  case CONTROLLED_U2:
  case ROTATION_U3:
  case CONTROLLED_U3:
    is_unitary = true;
    break;
  default:
    is_unitary = false;
    break;
  }
  
  return is_unitary;
}

bool kind_is_controlled(Kind kind)
{
  bool is_controlled;
  
  switch (kind) {
  case CONTROLLED_X:
  case CONTROLLED_Y:
  case CONTROLLED_Z:
  case CONTROLLED_XR:
  case CONTROLLED_XR_:
  case CONTROLLED_H:
  case CONTROLLED_S:
  case CONTROLLED_S_:
  case CONTROLLED_T:
  case CONTROLLED_T_:
  case CONTROLLED_P:
  case CONTROLLED_RX:
  case CONTROLLED_RY:
  case CONTROLLED_RZ:
  case CONTROLLED_U1:
  case CONTROLLED_U2:
  case CONTROLLED_U3:
    is_controlled = true;
    break;
  default:
    is_controlled = false;
    break;
  }
  
  return is_controlled;
}

bool is_gpu_supported_lib(void)
{
#ifdef USE_GPU
  return true;
#else
  return false;
#endif
}

bool is_gpu_available(void)
{
  const char* command = "nvidia-smi > /dev/null 2>&1";
  int res;

  res = system(command);
  if ((WIFEXITED(res) == true) && (WEXITSTATUS(res) == 0)){
    return true;
  }
  else {
    return false;
  }
}
