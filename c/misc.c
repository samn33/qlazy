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

  for (int i=ini; i<fin; i++) {
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

  if (d >= max_decimal) return false;

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
  
  return true;
}
