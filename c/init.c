/*
 *  init.c
 */

#define GLOBAL_VALUE_DEFINE
#include "qlazy.h"

void init_qlazy(unsigned int seed)
{
  g_Errno = NO_ERROR;
  g_Wrnno = NO_WARN;
  
  srand(seed);
}
