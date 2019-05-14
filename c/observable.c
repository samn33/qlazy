/*
 *  observable.c
 */

#include "qlazy.h"

static int get_term_num(char* str)
{
  int pos = 1;
  int num = 1;

  while (str[pos]!='\0') {
    if ((str[pos]=='+') || (str[pos]=='-')) num++;
    pos++;
  }
  return num;
}

Observable* observable_init(char* str)
/*
  [input string format (example)]
  "-2.0*Z_0*X_1*Y_3+3.0*X_0*Z_1-Y_1"
 */
{
  Observable*	observ	= NULL;
  int		str_len;
  char*		exp_str = NULL;
  char*		token[TOKEN_NUM];
  int		term_num = 0;
  int           spin_num = 0;

  g_Errno = NO_ERROR;

  /* expand string buffer: str -> exp_str */
  if (line_check_length(str) == FALSE) goto ERROR_EXIT;
  line_chomp(str);
  line_remove_space(str);
  str_len = strlen(str);
  str_len += get_term_num(str);
  if (!(exp_str = (char*)malloc(sizeof(char)*str_len))) goto ERROR_EXIT;

  /* insert ',' to the end of terms except last term */
  int pos = 0;
  int cnt = 0;
  exp_str[cnt++] = str[pos++];
  while (str[pos]!='\0') {
    if ((str[pos]=='+') || (str[pos]=='-')) {
      exp_str[cnt++] = ',';
      exp_str[cnt++] = str[pos++];
    }
    else {
      exp_str[cnt++] = str[pos++];
    }
  }
  exp_str[cnt] = '\0';

  /* split terms */
  term_num = line_split(exp_str, ",", token);

  /* set observ */
  if (!(observ = (Observable*)malloc(sizeof(Observable)))) goto ERROR_EXIT;
  observ->array_num = term_num;
  if (!(observ->spro_array = (SPro**)malloc(sizeof(SPro*)*observ->array_num)))
    goto ERROR_EXIT;

  for (int i=0; i<observ->array_num; i++) {
    if (!(observ->spro_array[i] = spro_init(token[i]))) goto ERROR_EXIT;
    spin_num = MAX(spin_num, observ->spro_array[i]->spin_num);
  }
  observ->spin_num = spin_num;
  
  free(exp_str);
  exp_str = NULL;
  
  return observ;

 ERROR_EXIT:
  g_Errno = ERROR_OBSERVABLE_INIT;
  return NULL;
}

void observable_free(Observable* observ)
{
  if (observ != NULL) {
    if (observ->spro_array != NULL) {
      for (int i=0; i<observ->array_num; i++) {
	if (observ->spro_array[i] != NULL) {
	  spro_free(observ->spro_array[i]);
	  observ->spro_array[i] = NULL;
	}
      }
      free(observ->spro_array);
      observ->spro_array = NULL;
    }
    free(observ);
  }
}
