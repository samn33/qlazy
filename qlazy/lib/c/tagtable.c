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
