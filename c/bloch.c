/*
 *  bloch.c
 */

#include "qlazy.h"

int bloch_get_angle(COMPLEX alpha, COMPLEX beta, double* theta, double* phi)
{
  COMPLEX	b_tmp, c_tmp;
  double	norm;

  g_Errno = NO_ERROR;

  /* in the case of north or south pole */
  if (cabs(alpha) < MIN_DOUBLE) {  /* south pole */
    *theta = 1.0;
    *phi = 0.0;
    return TRUE;
  }
  else if (cabs(beta) < MIN_DOUBLE) {  /* north pole */
    *theta = 0.0;
    *phi = 0.0;
    return TRUE;
  }
    
  /* eliminate phase factor */
  if (complex_division(beta, alpha, &b_tmp) == FALSE) goto ERROR_EXIT;
  alpha = 1.0 + 0.0j;
  beta	= b_tmp;
  
  /* normailzation */
  norm = sqrt(1.0 + beta * conj(beta));
  alpha /= norm;      /* alpha -> positive real, 0.0 <= alpha <= 1.0 */
  beta /= norm;       /* beta  -> complex */

  /* get (theta,phi) from (alpha,beta) */
  *theta = 2.0 * acos(creal(alpha));  /* 0.0 <= theta <= pi */
  if (complex_division((sin(*theta/2.0)+0.0j), beta, &c_tmp) == FALSE)
    goto ERROR_EXIT;
  *phi = -1.0 * carg(c_tmp);

  /* unit transform (unit=pi(radian)) */
  *theta /= M_PI;
  *phi /= M_PI;

  return TRUE;
  
 ERROR_EXIT:
  g_Errno = ERROR_BLOCH_GET_ANGLE;
  return FALSE;
}

