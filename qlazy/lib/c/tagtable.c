/*
 *  tagtable.c
 */

#include "qlazy.h"

static int _tag_to_hash(TagTable* tt, char* tag)
{
  int           i = 0;
  int		hash = 0;

  while (tag[i] != '\0') {
    hash += tag[i];
    i++;
  }
  hash = hash % tt->table_size;;

  return hash;
}

bool tagtable_init(int table_size, void** tt_out)
{
  TagTable* tt;

  if (!(tt = (TagTable*)malloc(sizeof(TagTable))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);

  tt->table_size = table_size;
  if (!(tt->table = (Element**)malloc(sizeof(Element*) * tt->table_size)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);
  
  for (int i=0; i<tt->table_size; i++) {
    if (!(tt->table[i] = (Element*)malloc(sizeof(Element))))
      ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);

    tt->table[i]->active = false;
    strcpy(tt->table[i]->tag, "0");
    tt->table[i]->phase = 0.0;
    tt->table[i]->next = NULL;
  }

  tt->data_num = 0;
  
  *tt_out = tt;

  SUC_RETURN(true);
}

bool tagtable_merge(TagTable* tt, TagTable* tt_in)
{
  Element* now = NULL;
  
  if ((tt == NULL) || (tt_in == NULL) ||
      (tt->table_size != tt_in->table_size)) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  
  for (int i=0; i<tt_in->table_size; i++) {
    now = tt_in->table[i];
    while (now->active == true) {
      if (!(tagtable_set_phase(tt, now->tag, now->phase))) {
	ERR_RETURN(ERROR_TAGTABLE_SET_PHASE, false);
      }
      now = now->next;
    }
  }

  SUC_RETURN(true);
}

bool tagtable_set_phase(TagTable* tt, char* tag, double phase)
{
  int		hash = 0;
  Element*	pos  = NULL;

  if (tt == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  hash = _tag_to_hash(tt, tag);
  
  pos = tt->table[hash];
  while (pos->active == true) {
    if (strcmp(pos->tag, tag) == 0) {
      pos->phase = phase; /* overwrite */
      SUC_RETURN(true);
    }
    pos = pos->next;
  }
  pos->active = true;
  strcpy(pos->tag, tag);
  pos->phase = phase;
  if (!(pos->next = (Element*)malloc(sizeof(Element))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);

  pos->next->active = false;
  strcpy(pos->next->tag, "0");
  pos->next->phase = 0;
  pos->next->next = NULL;

  tt->data_num++;

  SUC_RETURN(true);
}

bool tagtable_get_phase(TagTable* tt, char* tag, double* phase)
{
  int		hash = 0;
  Element*	pos  = NULL;

  if (tt == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  hash = _tag_to_hash(tt, tag);
  
  pos = tt->table[hash];

  while (pos != NULL) {
    if (strcmp(tag, pos->tag) == 0) {
      *phase = pos->phase;
      SUC_RETURN(true);
    }
    pos = pos->next;
  }

  ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
}

bool tagtable_get_tags(TagTable* tt, void** tag_array_out, int* tag_num, int* tag_strlen)
/*
  The tag_array_out is an array of pointers of char,
  and the tag_array_out[0] is allocated as an continuous 1-dim array buffer.
*/
{
  int		i;
  int		k_pos;
  Element*	now	  = NULL;
  char**	tag_array = NULL;
  char*		buff	  = NULL;
  int		counter	  = 0;

  if (tt == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  
  if (!(tag_array = (char**)malloc(sizeof(char*) * tt->data_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);

  if (!(buff = (char*)malloc(sizeof(char) * TAG_STRLEN * tt->data_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);

  k_pos = 0;
  for (i=0; i<tt->data_num; i++) {
    tag_array[i] = &buff[k_pos];
    k_pos += TAG_STRLEN;
  }
    
  for (i=0; i<tt->table_size; i++) {
    now = tt->table[i];
    while (now->active == true) {
      strcpy(tag_array[counter], now->tag);
      now = now->next;
      counter++;
    }
  }

  *tag_array_out = tag_array;
  *tag_num = tt->data_num;
  *tag_strlen = TAG_STRLEN;
  
  SUC_RETURN(true);
}

/* for debug */
void tagtable_print_data(TagTable* tt)
{
  Element* now = NULL;
  
  for (int i=0; i<tt->table_size; i++) {
    now = tt->table[i];
    while (now->active == true) {
      printf("tag, phase = %s, %f\n", now->tag, now->phase);
      now = now->next;
    }
  }
}

void tagtable_free(TagTable* tt)
{
  Element* pos = NULL;
  Element* prev = NULL;
  
  if (tt != NULL) {
    for (int i=0; i<tt->table_size; i++) {
      pos = tt->table[i];
      while (pos != NULL) {
	prev = pos;
	pos = pos->next;
	free(prev); prev = NULL;
      }
    }
  }
}
