/*
 *  line.c
 */

#include "qlazy.h"

int line_check_length(char* str)
{
  int pos = 0;

  while (1) {
    if (str[pos] == '\0') { pos++; break; }
    else pos++;
  }

  if (pos > LINE_STRLEN) return FALSE;
  else return TRUE;
}

int line_is_blank(char* str)
{
  char* p = str;
  while ((*p==' ') || (*p=='\t') || (*p=='\n') ||
	 (*p=='\v') || (*p=='\f')|| (*p=='\r')) p++;
  if (*p == '\0') return TRUE;
  else return FALSE;
}

int line_is_comment(char* str)
{
  if (str[0] == '#') return TRUE;
  else return FALSE;
}

int line_chomp(char* str)
{
  if (str == NULL) return FALSE;
  char* p;
  p = strchr(str,'\n');
  if (p != NULL) {
    *p = '\0';
  }
  return TRUE;
}

int line_split(char* str, const char* delim, char* outlist[])
{
  char* tk;
  int cnt = 0;
  tk = strtok(str,delim);
  while (tk!=NULL && cnt<TOKEN_NUM) {
    outlist[cnt++] = tk;
    tk = strtok(NULL,delim);
  }
  return cnt;
}

int line_getargs(char* str, char* args[])
/* "Func(foo,bar)" => "Func","foo","bar" */
{
  int	cnt = 0;
  int   anum;
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
  anum = line_split(str, " ", args);
  return anum;
}

int line_join_token(char* dst, char* token[], int ini, int fin)
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

  return TRUE;
}
