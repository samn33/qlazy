/*
 *  init.c
 */

#define GLOBAL_VALUE_DEFINE
#include "qlazy.h"

void init_qlazy(unsigned int seed)
{
  g_Errno = SUCCESS;
  srand(seed);
}
