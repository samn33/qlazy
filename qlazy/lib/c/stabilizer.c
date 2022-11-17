/*
 *  stabilizer.c
 */

#include "qlazy.h"

static ComplexAxis _mul_complex_axis(ComplexAxis a, ComplexAxis b)
{
  ComplexAxis out = REAL_PLUS;
  
  if (a == REAL_PLUS) { out = b; }

  else if (a == IMAG_PLUS) {
    if (b == REAL_PLUS) { out = a;}
    else if (b == IMAG_PLUS) { out = REAL_MINUS;}
    else if (b == REAL_MINUS) { out = IMAG_MINUS;}
    else { out = REAL_PLUS;}
  }

  else if (a == REAL_MINUS) {
    if (b == REAL_PLUS) { out = a;}
    else if (b == IMAG_PLUS) { out = IMAG_MINUS;}
    else if (b == REAL_MINUS) { out = REAL_PLUS;}
    else { out = IMAG_PLUS;}
  }

  else if (a == IMAG_MINUS) {
    if (b == REAL_PLUS) { out = a;}
    else if (b == IMAG_PLUS) { out = REAL_PLUS;}
    else if (b == REAL_MINUS) { out = IMAG_PLUS;}
    else { out = REAL_MINUS;}
  }

  return out;
}

bool stabilizer_init(int gene_num, int qubit_num, unsigned int seed, void** stab_out)
{
  Stabilizer*	stab	    = NULL;
  int		matrix_size = gene_num * qubit_num * 2;
  int		i;

  init_genrand(seed);

  if ((qubit_num < 1) || (gene_num < 1))
    ERR_RETURN(ERROR_OUT_OF_BOUND,false);

  if (!(stab = (Stabilizer*)malloc(sizeof(Stabilizer))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  stab->qubit_num = qubit_num;
  stab->gene_num = gene_num;

  if (!(stab->pauli_factor = (ComplexAxis*)malloc(sizeof(ComplexAxis)*stab->gene_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  for (i=0; i<stab->gene_num; i++) stab->pauli_factor[i] = REAL_PLUS;

  if (!(stab->check_matrix = (int*)malloc(sizeof(int)*matrix_size)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  for (i=0; i<matrix_size; i++) stab->check_matrix[i] = 0;

  *stab_out = stab;

  SUC_RETURN(true);
}

bool stabilizer_copy(Stabilizer* stab_in, void** stab_out)
{
  /* error check */
  if (stab_in == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if ((stab_in->gene_num < 1) || (stab_in->qubit_num < 1))
    ERR_RETURN(ERROR_OUT_OF_BOUND,false);

  Stabilizer* stab = NULL;
  if (!(stab = (Stabilizer*)malloc(sizeof(Stabilizer))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  stab->gene_num = stab_in->gene_num;
  stab->qubit_num = stab_in->qubit_num;
  int matrix_size = stab->gene_num * stab->qubit_num * 2;

  if (!(stab->pauli_factor = (ComplexAxis*)malloc(sizeof(ComplexAxis)*stab->gene_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  memcpy(stab->pauli_factor, stab_in->pauli_factor, sizeof(ComplexAxis)*stab->gene_num);

  if (!(stab->check_matrix = (int*)malloc(sizeof(int)*matrix_size)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  memcpy(stab->check_matrix, stab_in->check_matrix, sizeof(int)*matrix_size);

  *stab_out = stab;

  SUC_RETURN(true);
}

bool stabilizer_set_pauli_fac(Stabilizer* stab, int gene_id, ComplexAxis pauli_fac)
{
  int i;
  
  /* error check */
  if (stab == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if ((gene_id < 0) || (gene_id >= stab->gene_num))
    ERR_RETURN(ERROR_OUT_OF_BOUND,false);

  /* if generator have pauli-Ys */
  int col = 2 * stab->qubit_num;
  ComplexAxis pf = pauli_fac;
  for (i=0; i<stab->qubit_num; i++) {
    if ((stab->check_matrix[gene_id*col+i] == 1) &&
	(stab->check_matrix[gene_id*col+i+stab->qubit_num] == 1)) {
      pf = _mul_complex_axis(pf, IMAG_PLUS);
    }
  }

  stab->pauli_factor[gene_id] = pf;

  SUC_RETURN(true);
}

bool stabilizer_get_pauli_fac(Stabilizer* stab, int gene_id, ComplexAxis* pauli_fac)
{
  int i;
  
  /* error check */
  if (stab == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if ((gene_id < 0) || (gene_id >= stab->gene_num))
    ERR_RETURN(ERROR_OUT_OF_BOUND,false);

  /* if generator have pauli-Ys */
  int col = 2 * stab->qubit_num;
  ComplexAxis pf = stab->pauli_factor[gene_id];
  for (i=0; i<stab->qubit_num; i++) {
    if ((stab->check_matrix[gene_id*col+i] == 1) &&
	(stab->check_matrix[gene_id*col+i+stab->qubit_num] == 1)) {
      pf = _mul_complex_axis(pf, IMAG_MINUS);
    }
  }

  *pauli_fac = pf;

  SUC_RETURN(true);
}

bool stabilizer_set_pauli_op(Stabilizer* stab, int gene_id, int qubit_id, Kind pauli_op)
{
  /* error check */
  if (stab == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if ((qubit_id < 0) || (qubit_id >= stab->qubit_num) ||
      (gene_id < 0) || (gene_id >= stab->gene_num))
    ERR_RETURN(ERROR_OUT_OF_BOUND,false);

  int id_X = gene_id * stab->qubit_num * 2 + qubit_id;
  int id_Z = gene_id * stab->qubit_num * 2 + stab->qubit_num + qubit_id;
  
  switch (pauli_op) {
  case PAULI_X:
    /* if source is Y */
    if ((stab->check_matrix[id_X] == 1) && (stab->check_matrix[id_Z] == 1)) {
      stab->pauli_factor[gene_id]
	= _mul_complex_axis(stab->pauli_factor[gene_id], IMAG_MINUS);
    }
    stab->check_matrix[id_X] = 1;
    stab->check_matrix[id_Z] = 0;
    break;
  case PAULI_Y:
    /* if souce is X or Z or Identity */
    if ((stab->check_matrix[id_X] != 1) || (stab->check_matrix[id_Z] != 1)) {
      stab->pauli_factor[gene_id]
	= _mul_complex_axis(stab->pauli_factor[gene_id], IMAG_PLUS);
      stab->check_matrix[id_X] = 1;
      stab->check_matrix[id_Z] = 1;
    }
    /* if source is Y, do nothing */
    break;
  case PAULI_Z:
    /* if source is Y */
    if ((stab->check_matrix[id_X] == 1) && (stab->check_matrix[id_Z] == 1)) {
      stab->pauli_factor[gene_id]
	= _mul_complex_axis(stab->pauli_factor[gene_id], IMAG_MINUS);
    }
    stab->check_matrix[id_X] = 0;
    stab->check_matrix[id_Z] = 1;
    break;
  case IDENTITY:
    /* if source is Y */
    if ((stab->check_matrix[id_X] == 1) && (stab->check_matrix[id_Z] == 1)) {
      stab->pauli_factor[gene_id]
	= _mul_complex_axis(stab->pauli_factor[gene_id], IMAG_MINUS);
    }
    stab->check_matrix[id_X] = 0;
    stab->check_matrix[id_Z] = 0;
    break;
  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }

  SUC_RETURN(true);
}

bool stabilizer_get_pauli_op(Stabilizer* stab, int gene_id, int qubit_id, Kind* pauli_op)
{
  /* error check */
  if (stab == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if ((qubit_id < 0) || (qubit_id >= stab->qubit_num) ||
      (gene_id < 0) || (gene_id >= stab->gene_num))
    ERR_RETURN(ERROR_OUT_OF_BOUND,false);

  int id_X = gene_id * stab->qubit_num * 2 + qubit_id;
  int id_Z = gene_id * stab->qubit_num * 2 + stab->qubit_num + qubit_id;

  if ((stab->check_matrix[id_X] == 0) && (stab->check_matrix[id_Z] == 0)) {
    *pauli_op = IDENTITY;
  }
  else if ((stab->check_matrix[id_X] == 0) && (stab->check_matrix[id_Z] == 1)) {
    *pauli_op = PAULI_Z;
  }
  else if ((stab->check_matrix[id_X] == 1) && (stab->check_matrix[id_Z] == 0)) {
    *pauli_op = PAULI_X;
  }
  else if ((stab->check_matrix[id_X] == 1) && (stab->check_matrix[id_Z] == 1)) {
    *pauli_op = PAULI_Y;
  }
  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }
  
  SUC_RETURN(true);
}

static void _add_vector(int* vec_0, int* vec_1, int dim)
{
  int i;
  
  for (i=0; i<dim; i++) {
    vec_0[i] = (vec_0[i] + vec_1[i]) % 2;
  }
}

static int _row_reduction(int* coef, int row, int col)
/* output rank */
{
  int i = 0;
  int j = 0;
  int rank = 0;
  int k,l;

  /* row reducction */
  while (i < row) {
    while (j < col) {
      if (coef[i*col+j] == 0) {
	for (k=i+1; k<row; k++) {
	  if (coef[k*col+j] == 1) {
	    _add_vector(&coef[i*col], &coef[k*col], col);
	    break;
	  }
	}
      }
      if (coef[i*col+j] == 0) { j++; continue; }
      else { break; }
    }

    for (l=0; l<row; l++) {
      if ((l != i) && (coef[l*col+j] == 1)) {
    	_add_vector(&coef[l*col], &coef[i*col], col);
      }
    }
    i++; j++;
  }

  /* rank */
  for (i=0; i<row; i++) {
    for (j=0; j<col; j++) {
      if (coef[i*col+j] == 1) {
	rank++;
	break;
      }
    }
  }

  return rank;
}

bool stabilizer_get_rank(Stabilizer* stab, int* rank_out)
/* get rank of check matrix */
{
  int* coef = NULL;

  if (stab == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  int size = stab->gene_num * stab->qubit_num * 2;
  if (!(coef = (int*)malloc(sizeof(int)*size)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  memcpy(coef, stab->check_matrix, sizeof(int)*size);

  *rank_out = _row_reduction(coef, stab->gene_num, stab->qubit_num * 2);

  free(coef); coef = NULL;
  
  SUC_RETURN(true);
}

static bool _stabilizer_operate_x(Stabilizer* stab, int q)
{
  Kind	pauli_op;
  int	i;

  for (i=0; i<stab->gene_num; i++) {
    stabilizer_get_pauli_op(stab, i, q, &pauli_op);
    if ((pauli_op == PAULI_Y) || (pauli_op == PAULI_Z))
      stab->pauli_factor[i] = _mul_complex_axis(stab->pauli_factor[i], REAL_MINUS);
  }
  SUC_RETURN(true);
}

static bool _stabilizer_operate_y(Stabilizer* stab, int q)
{
  Kind	pauli_op;
  int	i;

  for (i=0; i<stab->gene_num; i++) {
    stabilizer_get_pauli_op(stab, i, q, &pauli_op);
    if ((pauli_op == PAULI_X) || (pauli_op == PAULI_Z))
      stab->pauli_factor[i] = _mul_complex_axis(stab->pauli_factor[i], REAL_MINUS);
  }
  SUC_RETURN(true);
}

static bool _stabilizer_operate_z(Stabilizer* stab, int q)
{
  Kind pauli_op;
  int  i;

  for (i=0; i<stab->gene_num; i++) {
    stabilizer_get_pauli_op(stab, i, q, &pauli_op);
    if ((pauli_op == PAULI_X) || (pauli_op == PAULI_Y))
      stab->pauli_factor[i] = _mul_complex_axis(stab->pauli_factor[i], REAL_MINUS);
  }
  SUC_RETURN(true);
}

static bool _stabilizer_operate_h(Stabilizer* stab, int q)
{
  Kind pauli_op;
  int  i;

  for (i=0; i<stab->gene_num; i++) {
    stabilizer_get_pauli_op(stab, i, q, &pauli_op);
    if (pauli_op == PAULI_X) {
      stabilizer_set_pauli_op(stab, i, q, PAULI_Z);
    }
    else if (pauli_op == PAULI_Y) {
      stabilizer_set_pauli_op(stab, i, q, PAULI_Y);
      stab->pauli_factor[i] = _mul_complex_axis(stab->pauli_factor[i], REAL_MINUS);
    }
    else if (pauli_op == PAULI_Z) {
      stabilizer_set_pauli_op(stab, i, q, PAULI_X);
    }
  }
  SUC_RETURN(true);
}

static bool _stabilizer_operate_s(Stabilizer* stab, int q)
{
  Kind pauli_op;
  int  i;

  for (i=0; i<stab->gene_num; i++) {
    stabilizer_get_pauli_op(stab, i, q, &pauli_op);
    if (pauli_op == PAULI_X) {
      stabilizer_set_pauli_op(stab, i, q, PAULI_Y);
    }
    else if (pauli_op == PAULI_Y) {
      stabilizer_set_pauli_op(stab, i, q, PAULI_X);
      stab->pauli_factor[i] = _mul_complex_axis(stab->pauli_factor[i], IMAG_PLUS);
    }
  }
  SUC_RETURN(true);
}

static bool _stabilizer_operate_s_dg(Stabilizer* stab, int q)
{
  Kind pauli_op;
  int  i;
  
  for (i=0; i<stab->gene_num; i++) {
    stabilizer_get_pauli_op(stab, i, q, &pauli_op);
    if (pauli_op == PAULI_X) {
      stabilizer_set_pauli_op(stab, i, q, PAULI_Y);
      stab->pauli_factor[i] = _mul_complex_axis(stab->pauli_factor[i], REAL_MINUS);
    }
    else if (pauli_op == PAULI_Y) {
      stabilizer_set_pauli_op(stab, i, q, PAULI_X);
      stab->pauli_factor[i] = _mul_complex_axis(stab->pauli_factor[i], IMAG_MINUS);
    }
  }
  SUC_RETURN(true);
}

static bool _stabilizer_operate_cx(Stabilizer* stab, int q_1, int q_2)
{
  Kind pop_1;
  Kind pop_2;
  int  i;

  for (i=0; i<stab->gene_num; i++) {
    stabilizer_get_pauli_op(stab, i, q_1, &pop_1);
    stabilizer_get_pauli_op(stab, i, q_2, &pop_2);
    /* X1 */
    if ((pop_1 == PAULI_X) && (pop_2 == IDENTITY)) {
      stabilizer_set_pauli_op(stab, i, q_2, PAULI_X);
    }
    /* X2 */
    else if ((pop_1 == IDENTITY) && (pop_2 == PAULI_X)) {
	;
    }
    /* Y1 */
    else if ((pop_1 == PAULI_Y) && (pop_2 == IDENTITY)) {
      stabilizer_set_pauli_op(stab, i, q_2, PAULI_X);
    }
    /* Y2 */
    else if ((pop_1 == IDENTITY) && (pop_2 == PAULI_Y)) {
      stabilizer_set_pauli_op(stab, i, q_1, PAULI_Z);
    }
    /* Z1 */
    else if ((pop_1 == PAULI_Z) && (pop_2 == IDENTITY)) {
	;
    }
    /* Z2 */
    else if ((pop_1 == IDENTITY) && (pop_2 == PAULI_Z)) {
      stabilizer_set_pauli_op(stab, i, q_1, PAULI_Z);
    }
    /* X1 X2 */
    else if ((pop_1 == PAULI_X) && (pop_2 == PAULI_X)) {
      stabilizer_set_pauli_op(stab, i, q_2, IDENTITY);
    }
    /* X1 Y2 */
    else if ((pop_1 == PAULI_X) && (pop_2 == PAULI_Y)) {
      stabilizer_set_pauli_op(stab, i, q_1, PAULI_Y);
      stabilizer_set_pauli_op(stab, i, q_2, PAULI_Z);
    }
    /* X1 Z2 */
    else if ((pop_1 == PAULI_X) && (pop_2 == PAULI_Z)) {
      stabilizer_set_pauli_op(stab, i, q_1, PAULI_Y);
      stabilizer_set_pauli_op(stab, i, q_2, PAULI_Y);
      stab->pauli_factor[i] = _mul_complex_axis(stab->pauli_factor[i], REAL_MINUS);
    }
    /* Y1 X2 */
    else if ((pop_1 == PAULI_Y) && (pop_2 == PAULI_X)) {
      stabilizer_set_pauli_op(stab, i, q_2, IDENTITY);
    }
    /* Y1 Y2 */
    else if ((pop_1 == PAULI_Y) && (pop_2 == PAULI_Y)) {
      stabilizer_set_pauli_op(stab, i, q_1, PAULI_X);
      stabilizer_set_pauli_op(stab, i, q_2, PAULI_Z);
      stab->pauli_factor[i] = _mul_complex_axis(stab->pauli_factor[i], REAL_MINUS);
    }
    /* Y1 Z2 */
    else if ((pop_1 == PAULI_Y) && (pop_2 == PAULI_Z)) {
      stabilizer_set_pauli_op(stab, i, q_1, PAULI_X);
      stabilizer_set_pauli_op(stab, i, q_2, PAULI_Y);
    }
    /* Z1 X2 */
    else if ((pop_1 == PAULI_Z) && (pop_2 == PAULI_X)) {
	;
    }
    /* Z1 Y2 */
    else if ((pop_1 == PAULI_Z) && (pop_2 == PAULI_Y)) {
      stabilizer_set_pauli_op(stab, i, q_1, IDENTITY);
    }
    /* Z1 Z2 */
    else if ((pop_1 == PAULI_Z) && (pop_2 == PAULI_Z)) {
      stabilizer_set_pauli_op(stab, i, q_1, IDENTITY);
    }
  }
  SUC_RETURN(true);
}

static bool _stabilizer_operate_cz(Stabilizer* stab, int q_1, int q_2)
{
  Kind pop_1;
  Kind pop_2;
  int  i;

  for (i=0; i<stab->gene_num; i++) {
    stabilizer_get_pauli_op(stab, i, q_1, &pop_1);
    stabilizer_get_pauli_op(stab, i, q_2, &pop_2);
    /* X1 */
    if ((pop_1 == PAULI_X) && (pop_2 == IDENTITY)) {
      stabilizer_set_pauli_op(stab, i, q_2, PAULI_Z);
    }
    /* X2 */
    else if ((pop_1 == IDENTITY) && (pop_2 == PAULI_X)) {
      stabilizer_set_pauli_op(stab, i, q_1, PAULI_Z);
    }
    /* Y1 */
    else if ((pop_1 == PAULI_Y) && (pop_2 == IDENTITY)) {
      stabilizer_set_pauli_op(stab, i, q_2, PAULI_Z);
    }
    /* Y2 */
    else if ((pop_1 == IDENTITY) && (pop_2 == PAULI_Y)) {
      stabilizer_set_pauli_op(stab, i, q_1, PAULI_Z);
    }
    /* Z1 */
    else if ((pop_1 == PAULI_Z) && (pop_2 == IDENTITY)) {
      ;
    }
    /* Z2 */
    else if ((pop_1 == IDENTITY) && (pop_2 == PAULI_Z)) {
      ;
    }
    /* X1 X2 */
    else if ((pop_1 == PAULI_X) && (pop_2 == PAULI_X)) {
      stabilizer_set_pauli_op(stab, i, q_1, PAULI_Y);
      stabilizer_set_pauli_op(stab, i, q_2, PAULI_Y);
    }
    /* X1 Y2 */
    else if ((pop_1 == PAULI_X) && (pop_2 == PAULI_Y)) {
      stabilizer_set_pauli_op(stab, i, q_1, PAULI_Y);
      stabilizer_set_pauli_op(stab, i, q_2, PAULI_X);
      stab->pauli_factor[i] = _mul_complex_axis(stab->pauli_factor[i], REAL_MINUS);
    }
    /* X1 Z2 */
    else if ((pop_1 == PAULI_X) && (pop_2 == PAULI_Z)) {
      stabilizer_set_pauli_op(stab, i, q_2, IDENTITY);
    }
    /* Y1 X2 */
    else if ((pop_1 == PAULI_Y) && (pop_2 == PAULI_X)) {
      stabilizer_set_pauli_op(stab, i, q_1, PAULI_X);
      stabilizer_set_pauli_op(stab, i, q_2, PAULI_Y);
      stab->pauli_factor[i] = _mul_complex_axis(stab->pauli_factor[i], REAL_MINUS);
    }
    /* Y1 Y2 */
    else if ((pop_1 == PAULI_Y) && (pop_2 == PAULI_Y)) {
      stabilizer_set_pauli_op(stab, i, q_1, PAULI_X);
      stabilizer_set_pauli_op(stab, i, q_2, PAULI_X);
    }
    /* Y1 Z2 */
    else if ((pop_1 == PAULI_Y) && (pop_2 == PAULI_Z)) {
      stabilizer_set_pauli_op(stab, i, q_2, IDENTITY);
    }
    /* Z1 X2 */
    else if ((pop_1 == PAULI_Z) && (pop_2 == PAULI_X)) {
      stabilizer_set_pauli_op(stab, i, q_1, IDENTITY);
    }
    /* Z1 Y2 */
    else if ((pop_1 == PAULI_Z) && (pop_2 == PAULI_Y)) {
      stabilizer_set_pauli_op(stab, i, q_1, IDENTITY);
    }
    /* Z1 Z2 */
    else if ((pop_1 == PAULI_Z) && (pop_2 == PAULI_Z)) {
      ;
    }
  }
  SUC_RETURN(true);
}

bool stabilizer_operate_qgate(Stabilizer* stab, Kind kind, int q0, int q1)
{
  /* error check */
  if (stab == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if ((q0 < 0) || (q0 >= stab->qubit_num))
    ERR_RETURN(ERROR_OUT_OF_BOUND,false);

  switch (kind) {
  case PAULI_X:
    _stabilizer_operate_x(stab, q0);
    break;
  case PAULI_Y:
    _stabilizer_operate_y(stab, q0);
    break;
  case PAULI_Z:
    _stabilizer_operate_z(stab, q0);
    break;
  case HADAMARD:
    _stabilizer_operate_h(stab, q0);
    break;
  case PHASE_SHIFT_S:
    _stabilizer_operate_s(stab, q0);
    break;
  case PHASE_SHIFT_S_:
    _stabilizer_operate_s_dg(stab, q0);
    break;
  case CONTROLLED_X:
    if ((q1 < 0) || (q1 >= stab->qubit_num)) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    _stabilizer_operate_cx(stab, q0, q1);
    break;
  case CONTROLLED_Z:
    if ((q1 < 0) || (q1 >= stab->qubit_num)) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    _stabilizer_operate_cz(stab, q0, q1);
    break;
  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }
  
  SUC_RETURN(true);
}

static bool _get_solution(Stabilizer* stab, int* measured_op, int* variables)
{
  /* error check */
  if ((stab == NULL) || (measured_op == NULL) || (variables == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  int*	coef   = NULL;  /* stab->check matrix + measured op */
  int*	coef_T = NULL;  /* transpose matrix of 'coef' */
  int	row    = stab->gene_num;
  int	col    = 2 * stab->qubit_num;
  int   size   = row * col;
  int   i,j;

  /* copy 'stab->check_matrix' + 'measured_op' to 'coef' */
  if (!(coef = (int*)malloc(sizeof(int)*(size+col))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  memcpy(coef, stab->check_matrix, sizeof(int)*size);
  for (i=0; i<col; i++) coef[row*col+i] = measured_op[i];

  /* transpose of 'coef' ('coef_T') */
  if (!(coef_T = (int*)malloc(sizeof(int)*(size+col))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  for (i=0; i<col; i++) {
    for (j=0; j<row+1; j++) {
      coef_T[i*(row+1)+j] = coef[j*col+i];
    }
  }

  /* solve (row reduction) */
  _row_reduction(coef_T, col, row+1);

  for (i=0; i<col; i++) {
    variables[i] = coef_T[i*(row+1)+row];
  }

  free(coef); coef = NULL;
  free(coef_T); coef_T = NULL;
  
  SUC_RETURN(true);
}

bool stabilizer_measure(Stabilizer* stab, int q, double* prob_out, int* mval_out)
{
  /* measured_op: binary vector corresponding to Z(q)   */
  /* ex) Z(0) for 3-qubit-system = (0,0,0,1,0,0)        */
  int*	measured_op = NULL;	/* dimension = 2*qubit_num  */
  bool* commute_flg = NULL;	/* dimention = gene_num     */
  int   i;
  
  /* error check */
  if (stab == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  if ((q < 0) || (q >= stab->qubit_num))
    ERR_RETURN(ERROR_OUT_OF_BOUND,false);

  int rank = 0;
  stabilizer_get_rank(stab, &rank);
  if (rank != stab->qubit_num)
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* set measured_op : Z(q) */
  if (!(measured_op = (int*)malloc(sizeof(int)*2*stab->qubit_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  for (i=0; i<2*stab->qubit_num; i++) measured_op[i] = 0;
  measured_op[stab->qubit_num + q] = 1;

  /* commute or not */
  if (!(commute_flg = (bool*)malloc(sizeof(bool)*stab->gene_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  int row = stab->gene_num;
  int col = 2 * stab->qubit_num;
  int commute = 0;
  for (i=0; i<row; i++) {
    if (stab->check_matrix[i*col+q] == 0) {
      commute_flg[i] = true; commute++;
    }
    else if (stab->check_matrix[i*col+q] == 1) {
      commute_flg[i] = false;
    }
    else {
      ERR_RETURN(ERROR_STABILIZER_MEASURE,false);
    }
  }

  int not_commute = row - commute;
  if (not_commute == 0) { /* commute */

    /* +Z(q) in S -> prob[0] = 1, prob[1] = 0 */
    /* -Z(q) in S -> prob[0] = 0, prob[1] = 1 */

    int* variables = NULL;
    if (!(variables = (int*)malloc(sizeof(int)*col)))
      ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
    if (!(_get_solution(stab, measured_op, variables)))
      ERR_RETURN(ERROR_STABILIZER_MEASURE,false);

    ComplexAxis sign = REAL_PLUS;
    for (i=0; i<row; i++) {
      if (variables[i] == 1) {
	sign = _mul_complex_axis(sign, stab->pauli_factor[i]);
      }
    }
    if (sign == REAL_PLUS) { /* Z(q) in S */
      prob_out[0] = 1.0; prob_out[1] = 0.0;
      *mval_out = 0;
    }
    else if (sign == REAL_MINUS) { /* -Z(q) in S */
      prob_out[0] = 0.0; prob_out[1] = 1.0;
      *mval_out = 1;
    }
    else {
      ERR_RETURN(ERROR_STABILIZER_MEASURE,false);
    }
    
    free(variables); variables = NULL;
  }
  
  else if (not_commute >= 1) {

    int not_commute_id = 0;
    for (i=0; i<row; i++) {
      if (commute_flg[i] == false) { not_commute_id = i; break; }
    }

    /* number of generators not commute will be only one */
    if (not_commute > 1) {
      for (i=not_commute_id+1; i<row; i++) {
	if (commute_flg[i] == false) {
	  _add_vector(&(stab->check_matrix[i*col]),
		       &(stab->check_matrix[not_commute_id*col]), col);
	  stab->pauli_factor[i] = _mul_complex_axis(stab->pauli_factor[i],
						    stab->pauli_factor[not_commute_id]);
	}
      }
    }

    /* replace generator to mesured operator (Z(q) of -Z(q)) */
    for (i=0; i<col; i++) {
      stab->check_matrix[not_commute_id*col+i] = measured_op[i];
    }
    
    //if (rand()%2 == 0) {
    if (genrand_int32()%2 == 0) {
      stab->pauli_factor[not_commute_id] = REAL_PLUS; /* Z(q) */
      *mval_out = 0;
    }
    else {
      stab->pauli_factor[not_commute_id] = REAL_MINUS; /* -Z(q) */
      *mval_out = 1;
    }
      
    /* set probabilities */
    prob_out[0] = 0.5; prob_out[1] = 0.5;
  }

  else {
    ERR_RETURN(ERROR_STABILIZER_MEASURE,false);
  }

  free(measured_op); measured_op = NULL;
  free(commute_flg); commute_flg = NULL;

  SUC_RETURN(true);
}

bool stabilizer_operate_qcirc(Stabilizer* stab, CMem* cmem, QCirc* qcirc)
{
  QGate*        qgate = NULL;   /* quantum gate in quantum circuit */
  MData*	mdata = NULL;   /* output measurement data */
  int		m;
  double	prob_out[2];

  /* error check */
  if ((stab == NULL || qcirc == NULL) ||
      (stab->qubit_num != stab->gene_num) ||
      (stab->qubit_num < qcirc->qubit_num) ||
      (cmem != NULL && cmem->cmem_num < qcirc->cmem_num))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  qgate = qcirc->first;
  while (qgate != NULL) {

    if ((qgate->ctrl == -1) ||
	((qgate->ctrl != -1) && (cmem->bit_array[qgate->ctrl] == 1))) {
    
      if (kind_is_unitary(qgate->kind) == true) {
	if (!(stabilizer_operate_qgate(stab, qgate->kind, qgate->qid[0], qgate->qid[1])))
	  ERR_RETURN(ERROR_STABILIZER_OPERATE_QGATE, false);
      }
      else if (kind_is_reset(qgate->kind) == true) {
	if (!(stabilizer_measure(stab, qgate->qid[0], prob_out, &m)))
	  ERR_RETURN(ERROR_STABILIZER_MEASURE, false);
	if (m < 0 || m > 1) ERR_RETURN(ERROR_STABILIZER_MEASURE, false);
	if (m == 1) {
	  if (!(stabilizer_operate_qgate(stab, PAULI_X, qgate->qid[0], qgate->qid[1])))
	    ERR_RETURN(ERROR_STABILIZER_OPERATE_QGATE, false);
	}
      }
      else if (kind_is_measurement(qgate->kind) == true) {
	if (!(stabilizer_measure(stab, qgate->qid[0], prob_out, &m)))
	  ERR_RETURN(ERROR_STABILIZER_MEASURE, false);
	if (m < 0 || m > 1) ERR_RETURN(ERROR_STABILIZER_MEASURE, false);
	if (qgate->c != -1) cmem->bit_array[qgate->c] = (BYTE)m;  /* measured value is stored to classical register */
	mdata_free(mdata); mdata = NULL;
      }
      else {
	ERR_RETURN(ERROR_QSTATE_OPERATE_QCIRC, false);
      }
    }
    
    qgate = qgate->next;
  }

  SUC_RETURN(true);
}

void stabilizer_free(Stabilizer* stab)
{
  if (stab != NULL) {
    if (stab->pauli_factor != NULL) {
      free(stab->pauli_factor);
      stab->pauli_factor = NULL;
    }
    if (stab->check_matrix != NULL) {
      free(stab->check_matrix);
      stab->check_matrix = NULL;
    }
    free(stab);
  }
}
