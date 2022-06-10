#include "qlazy.h"

static int _key_to_hash(HashTable* ht, char* key)
{
  int   i    = 0;
  int	hash = 0;

  while (key[i] != '\0') {
    hash += key[i];
    i++;
  }
  hash = hash % ht->table_size;;

  return hash;
}

bool hashtable_create(int table_size, void** ht_out)
{
  HashTable* ht;

  if (!(ht = (HashTable*)malloc(sizeof(HashTable))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, NULL);

  ht->table_size = table_size;
  if (!(ht->table = (Element**)malloc(sizeof(Element*) * ht->table_size)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, NULL);
  
  for (int i=0; i<ht->table_size; i++) {
    if (!(ht->table[i] = (Element*)malloc(sizeof(Element))))
      ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, NULL);

    ht->table[i]->active = false;
    strcpy(ht->table[i]->key, "0");
    ht->table[i]->value = 0;
    ht->table[i]->next = NULL;
  }

  ht->data_num = 0;
  
  *ht_out = ht;

  SUC_RETURN(true);
}

bool hashtable_set_value(HashTable* ht, char* key, int value)
{
  int		hash = 0;
  Element*	pos  = NULL;

  hash = _key_to_hash(ht, key);
  
  pos = ht->table[hash];
  while (pos->active == true) {
    if (strcmp(pos->key, key) == 0) {
      pos->value = value; /* overwrite */
      SUC_RETURN(true);
    }
    pos = pos->next;
  }
  pos->active = true;
  strcpy(pos->key, key);
  pos->value = value;
  if (!(pos->next = (Element*)malloc(sizeof(Element))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, NULL);

  pos->next->active = false;
  strcpy(pos->next->key, "0");
  pos->next->value = 0;
  pos->next->next = NULL;

  ht->data_num++;

  SUC_RETURN(true);
}

bool hashtable_add_value(HashTable* ht, char* key, int value)
{
  int		hash = 0;
  Element*	pos  = NULL;

  hash = _key_to_hash(ht, key);
  
  pos = ht->table[hash];
  while (pos->active == true) {
    if (strcmp(pos->key, key) == 0) {
      pos->value += value; /* overwrite */
      SUC_RETURN(true);
    }
    pos = pos->next;
  }

  ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
}

bool hashtable_get_value(HashTable* ht, char* key, int* value)
{
  int 	hash = 0;
  Element*	pos  = NULL;

  hash = _key_to_hash(ht, key);
  
  pos = ht->table[hash];

  while (pos != NULL) {
    if (strcmp(key, pos->key) == 0) {
      *value = pos->value;
      SUC_RETURN(true);
    }
    pos = pos->next;
  }

  ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
}

void hashtable_free(HashTable* ht)
{
  Element*	pos  = NULL;
  Element*	prev = NULL;
  
  if (ht != NULL) {
    for (int i=0; i<ht->table_size; i++) {
      pos = ht->table[i];
      while (pos != NULL) {
	prev = pos;
	pos = pos->next;
	free(prev); prev = NULL;
      }
    }
  }
}

void hashtable_print_shape(HashTable* ht)
{
  Element* now = NULL;
  
  for (int i=0; i<ht->table_size; i++) {
    now = ht->table[i];
    printf("-");
    while (now->active == true) {
      printf("*");
      now = now->next;
    }
    printf("\n");
  }
}

void hashtable_print_data(HashTable* ht)
{
  Element* now = NULL;
  
  for (int i=0; i<ht->table_size; i++) {
    now = ht->table[i];
    while (now->active == true) {
      printf("key, value = %s, %d\n", now->key, now->value);
      now = now->next;
    }
  }
}

bool hashtable_get_data(HashTable* ht, void** key_array_out, void** value_array_out)
{
  int		i;
  int		k_pos;
  Element*	now	    = NULL;
  char**	key_array   = NULL;
  char*		buff	    = NULL;
  int*		value_array = NULL;
  int		counter	    = 0;

  if (!(key_array = (char**)malloc(sizeof(char*) * ht->data_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, NULL);

  if (!(buff = (char*)malloc(sizeof(char) * KEY_STRLEN * ht->data_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, NULL);

  k_pos = 0;
  for (i=0; i<ht->data_num; i++) {
    key_array[i] = &buff[k_pos];
    k_pos += KEY_STRLEN;
  }
    
  if (!(value_array = (int*)malloc(sizeof(int) * ht->data_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, NULL);
  
  for (i=0; i<ht->table_size; i++) {
    now = ht->table[i];
    while (now->active == true) {
      strcpy(key_array[counter], now->key);
      value_array[counter] = now->value;
      now = now->next;
      counter++;
    }
  }

  *key_array_out = key_array;
  *value_array_out = value_array;
  
  SUC_RETURN(true);
}
