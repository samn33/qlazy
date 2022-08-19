/*
 *  observable.c
 */

#include "qlazy.h"

static int _get_term_num(char* str)
{
  int pos = 1;
  int num = 1;

  while (str[pos]!='\0') {
    if ((str[pos]=='+') || (str[pos]=='-')) num++;
    pos++;
  }
  SUC_RETURN(num);
}

bool observable_base_init(char* str, void** observ_out)
/*
  [input string format (example)]
  "5.0+2.0*Z_0*X_1*Y_3+3.0*X_0*Z_1-Y_1"
 */
{
  ObservableBase*	observ	= NULL;
  int		str_len;
  char*		exp_str = NULL;
  char*		token[TOKEN_NUM];
  int		term_num = 0;
  int           spin_num = 0;
  int           i;

  /* expand string buffer: str -> exp_str */
  if (!line_check_length(str)) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!line_chomp(str)) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if (!line_remove_space(str)) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  str_len = (int)strlen(str);
  str_len += _get_term_num(str);
  if (!(exp_str = (char*)malloc(sizeof(char)*str_len)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

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
  if (!line_split(exp_str, ",", token, &term_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
    
  /* set observ */
  if (!(observ = (ObservableBase*)malloc(sizeof(ObservableBase))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  observ->array_num = term_num;
  if (!(observ->spro_array = (SPro**)malloc(sizeof(SPro*)*observ->array_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  for (i=0; i<observ->array_num; i++) {
    if (!(spro_init(token[i], (void**)&(observ->spro_array[i]))))
      ERR_RETURN(ERROR_SPRO_INIT,false);
    
    spin_num = MAX(spin_num, observ->spro_array[i]->spin_num);
  }
  observ->spin_num = spin_num;
  
  free(exp_str);
  exp_str = NULL;

  *observ_out = observ;

  SUC_RETURN(true);
}

void observable_base_free(ObservableBase* observ)
{
  int i;
  
  if (observ != NULL) {
    if (observ->spro_array != NULL) {
      for (i=0; i<observ->array_num; i++) {
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
