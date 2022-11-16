/*
 *  gbank.c
 */

#include "qlazy.h"

bool gbank_init(void** gbank_out)
{
  GBank* gbank = NULL;

  if (!(gbank = (GBank*)malloc(sizeof(GBank))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  gbank->PauliX[0] = 0.0;
  gbank->PauliX[1] = 1.0;
  gbank->PauliX[2] = 1.0;
  gbank->PauliX[3] = 0.0;

  gbank->PauliY[0] =  0.0;
  gbank->PauliY[1] = -1.0 * COMP_I;

  gbank->PauliY[2] = 1.0 * COMP_I;
  gbank->PauliY[3] =  0.0;

  gbank->PauliZ[0] =  1.0;
  gbank->PauliZ[1] =  0.0;
  gbank->PauliZ[2] =  0.0;
  gbank->PauliZ[3] = -1.0;

  gbank->RootPauliX[0] = (1.0 + 1.0 * COMP_I) / 2.0;
  gbank->RootPauliX[1] = (1.0 - 1.0 * COMP_I) / 2.0;
  gbank->RootPauliX[2] = (1.0 - 1.0 * COMP_I) / 2.0;
  gbank->RootPauliX[3] = (1.0 + 1.0 * COMP_I) / 2.0;

  gbank->RootPauliX_[0] = (1.0 - 1.0 * COMP_I) / 2.0;
  gbank->RootPauliX_[1] = (1.0 + 1.0 * COMP_I) / 2.0;
  gbank->RootPauliX_[2] = (1.0 + 1.0 * COMP_I) / 2.0;
  gbank->RootPauliX_[3] = (1.0 - 1.0 * COMP_I) / 2.0;

  gbank->Hadamard[0] =  1.0 / sqrt(2.0);
  gbank->Hadamard[1] =  1.0 / sqrt(2.0);
  gbank->Hadamard[2] =  1.0 / sqrt(2.0);
  gbank->Hadamard[3] = -1.0 / sqrt(2.0);

  gbank->PhaseShiftS[0] =  1.0;
  gbank->PhaseShiftS[1] =  0.0;
  gbank->PhaseShiftS[2] =  0.0;
  gbank->PhaseShiftS[3] =  1.0 * COMP_I;

  gbank->PhaseShiftS_[0] =   1.0;
  gbank->PhaseShiftS_[1] =   0.0;
  gbank->PhaseShiftS_[2] =   0.0;
  gbank->PhaseShiftS_[3] =  -1.0 * COMP_I;

  gbank->PhaseShiftT[0] =  1.0;
  gbank->PhaseShiftT[1] =  0.0;
  gbank->PhaseShiftT[2] =  0.0;
  gbank->PhaseShiftT[3] =  (1.0 + 1.0 * COMP_I) / sqrt(2.0);

  gbank->PhaseShiftT_[0] =  1.0;
  gbank->PhaseShiftT_[1] =  0.0;
  gbank->PhaseShiftT_[2] =  0.0;
  gbank->PhaseShiftT_[3] =  (1.0 - 1.0 * COMP_I) / sqrt(2.0);

  gbank->ControlledX[0]  = 1.0;
  gbank->ControlledX[1]  = 0.0;
  gbank->ControlledX[2]  = 0.0;
  gbank->ControlledX[3]  = 0.0;
  gbank->ControlledX[4]  = 0.0;
  gbank->ControlledX[5]  = 1.0;
  gbank->ControlledX[6]  = 0.0;
  gbank->ControlledX[7]  = 0.0;
  gbank->ControlledX[8]  = 0.0;
  gbank->ControlledX[9]  = 0.0;
  gbank->ControlledX[10] = gbank->PauliX[0];
  gbank->ControlledX[11] = gbank->PauliX[1];
  gbank->ControlledX[12] = 0.0;
  gbank->ControlledX[13] = 0.0;
  gbank->ControlledX[14] = gbank->PauliX[2];
  gbank->ControlledX[15] = gbank->PauliX[3];

  gbank->ControlledY[0]  = 1.0;
  gbank->ControlledY[1]  = 0.0;
  gbank->ControlledY[2]  = 0.0;
  gbank->ControlledY[3]  = 0.0;
  gbank->ControlledY[4]  = 0.0;
  gbank->ControlledY[5]  = 1.0;
  gbank->ControlledY[6]  = 0.0;
  gbank->ControlledY[7]  = 0.0;
  gbank->ControlledY[8]  = 0.0;
  gbank->ControlledY[9]  = 0.0;
  gbank->ControlledY[10] = gbank->PauliY[0];
  gbank->ControlledY[11] = gbank->PauliY[1];
  gbank->ControlledY[12] = 0.0;
  gbank->ControlledY[13] = 0.0;
  gbank->ControlledY[14] = gbank->PauliY[2];
  gbank->ControlledY[15] = gbank->PauliY[3];

  gbank->ControlledZ[0]  =  1.0;
  gbank->ControlledZ[1]  =  0.0;
  gbank->ControlledZ[2]  =  0.0;
  gbank->ControlledZ[3]  =  0.0;
  gbank->ControlledZ[4]  =  0.0;
  gbank->ControlledZ[5]  =  1.0;
  gbank->ControlledZ[6]  =  0.0;
  gbank->ControlledZ[7]  =  0.0;
  gbank->ControlledZ[8]  =  0.0;
  gbank->ControlledZ[9]  =  0.0;
  gbank->ControlledZ[10] =  gbank->PauliZ[0];
  gbank->ControlledZ[11] =  gbank->PauliZ[1];
  gbank->ControlledZ[12] =  0.0;
  gbank->ControlledZ[13] =  0.0;
  gbank->ControlledZ[14] =  gbank->PauliZ[2];
  gbank->ControlledZ[15] =  gbank->PauliZ[3];

  gbank->ControlledXR[0]  =  1.0;
  gbank->ControlledXR[1]  =  0.0;
  gbank->ControlledXR[2]  =  0.0;
  gbank->ControlledXR[3]  =  0.0;
  gbank->ControlledXR[4]  =  0.0;
  gbank->ControlledXR[5]  =  1.0;
  gbank->ControlledXR[6]  =  0.0;
  gbank->ControlledXR[7]  =  0.0;
  gbank->ControlledXR[8]  =  0.0;
  gbank->ControlledXR[9]  =  0.0;
  gbank->ControlledXR[10] =  gbank->RootPauliX[0];
  gbank->ControlledXR[11] =  gbank->RootPauliX[1];
  gbank->ControlledXR[12] =  0.0;
  gbank->ControlledXR[13] =  0.0;
  gbank->ControlledXR[14] =  gbank->RootPauliX[2];
  gbank->ControlledXR[15] =  gbank->RootPauliX[3];

  gbank->ControlledXR_[0]  =  1.0;
  gbank->ControlledXR_[1]  =  0.0;
  gbank->ControlledXR_[2]  =  0.0;
  gbank->ControlledXR_[3]  =  0.0;
  gbank->ControlledXR_[4]  =  0.0;
  gbank->ControlledXR_[5]  =  1.0;
  gbank->ControlledXR_[6]  =  0.0;
  gbank->ControlledXR_[7]  =  0.0;
  gbank->ControlledXR_[8]  =  0.0;
  gbank->ControlledXR_[9]  =  0.0;
  gbank->ControlledXR_[10] =  gbank->RootPauliX_[0];
  gbank->ControlledXR_[11] =  gbank->RootPauliX_[1];
  gbank->ControlledXR_[12] =  0.0;
  gbank->ControlledXR_[13] =  0.0;
  gbank->ControlledXR_[14] =  gbank->RootPauliX_[2];
  gbank->ControlledXR_[15] =  gbank->RootPauliX_[3];

  gbank->ControlledH[0]  =  1.0;
  gbank->ControlledH[1]  =  0.0;
  gbank->ControlledH[2]  =  0.0;
  gbank->ControlledH[3]  =  0.0;
  gbank->ControlledH[4]  =  0.0;
  gbank->ControlledH[5]  =  1.0;
  gbank->ControlledH[6]  =  0.0;
  gbank->ControlledH[7]  =  0.0;
  gbank->ControlledH[8]  =  0.0;
  gbank->ControlledH[9]  =  0.0;
  gbank->ControlledH[10] =  gbank->Hadamard[0];
  gbank->ControlledH[11] =  gbank->Hadamard[1];
  gbank->ControlledH[12] =  0.0;
  gbank->ControlledH[13] =  0.0;
  gbank->ControlledH[14] =  gbank->Hadamard[2];
  gbank->ControlledH[15] =  gbank->Hadamard[3];

  gbank->ControlledS[0]  =  1.0;
  gbank->ControlledS[1]  =  0.0;
  gbank->ControlledS[2]  =  0.0;
  gbank->ControlledS[3]  =  0.0;
  gbank->ControlledS[4]  =  0.0;
  gbank->ControlledS[5]  =  1.0;
  gbank->ControlledS[6]  =  0.0;
  gbank->ControlledS[7]  =  0.0;
  gbank->ControlledS[8]  =  0.0;
  gbank->ControlledS[9]  =  0.0;
  gbank->ControlledS[10] =  gbank->PhaseShiftS[0];
  gbank->ControlledS[11] =  gbank->PhaseShiftS[1];
  gbank->ControlledS[12] =  0.0;
  gbank->ControlledS[13] =  0.0;
  gbank->ControlledS[14] =  gbank->PhaseShiftS[2];
  gbank->ControlledS[15] =  gbank->PhaseShiftS[3];

  gbank->ControlledS_[0]  =  1.0;
  gbank->ControlledS_[1]  =  0.0;
  gbank->ControlledS_[2]  =  0.0;
  gbank->ControlledS_[3]  =  0.0;
  gbank->ControlledS_[4]  =  0.0;
  gbank->ControlledS_[5]  =  1.0;
  gbank->ControlledS_[6]  =  0.0;
  gbank->ControlledS_[7]  =  0.0;
  gbank->ControlledS_[8]  =  0.0;
  gbank->ControlledS_[9]  =  0.0;
  gbank->ControlledS_[10] =  gbank->PhaseShiftS_[0];
  gbank->ControlledS_[11] =  gbank->PhaseShiftS_[1];
  gbank->ControlledS_[12] =  0.0;
  gbank->ControlledS_[13] =  0.0;
  gbank->ControlledS_[14] =  gbank->PhaseShiftS_[2];
  gbank->ControlledS_[15] =  gbank->PhaseShiftS_[3];

  gbank->ControlledT[0]  =  1.0;
  gbank->ControlledT[1]  =  0.0;
  gbank->ControlledT[2]  =  0.0;
  gbank->ControlledT[3]  =  0.0;
  gbank->ControlledT[4]  =  0.0;
  gbank->ControlledT[5]  =  1.0;
  gbank->ControlledT[6]  =  0.0;
  gbank->ControlledT[7]  =  0.0;
  gbank->ControlledT[8]  =  0.0;
  gbank->ControlledT[9]  =  0.0;
  gbank->ControlledT[10] =  gbank->PhaseShiftT[0];
  gbank->ControlledT[11] =  gbank->PhaseShiftT[1];
  gbank->ControlledT[12] =  0.0;
  gbank->ControlledT[13] =  0.0;
  gbank->ControlledT[14] =  gbank->PhaseShiftT[2];
  gbank->ControlledT[15] =  gbank->PhaseShiftT[3];

  gbank->ControlledT_[0]  =  1.0;
  gbank->ControlledT_[1]  =  0.0;
  gbank->ControlledT_[2]  =  0.0;
  gbank->ControlledT_[3]  =  0.0;
  gbank->ControlledT_[4]  =  0.0;
  gbank->ControlledT_[5]  =  1.0;
  gbank->ControlledT_[6]  =  0.0;
  gbank->ControlledT_[7]  =  0.0;
  gbank->ControlledT_[8]  =  0.0;
  gbank->ControlledT_[9]  =  0.0;
  gbank->ControlledT_[10] =  gbank->PhaseShiftT_[0];
  gbank->ControlledT_[11] =  gbank->PhaseShiftT_[1];
  gbank->ControlledT_[12] =  0.0;
  gbank->ControlledT_[13] =  0.0;
  gbank->ControlledT_[14] =  gbank->PhaseShiftT_[2];
  gbank->ControlledT_[15] =  gbank->PhaseShiftT_[3];

  gbank->Swap[0]   =  1.0;
  gbank->Swap[1]   =  0.0;
  gbank->Swap[2]   =  0.0;
  gbank->Swap[3]   =  0.0;
  gbank->Swap[4]   =  0.0;
  gbank->Swap[5]   =  0.0;
  gbank->Swap[6]   =  1.0;
  gbank->Swap[7]   =  0.0;
  gbank->Swap[8]   =  0.0;
  gbank->Swap[9]   =  1.0;
  gbank->Swap[10]  =  0.0;
  gbank->Swap[11]  =  0.0;
  gbank->Swap[12]  =  0.0;
  gbank->Swap[13]  =  0.0;
  gbank->Swap[14]  =  0.0;
  gbank->Swap[15]  =  1.0;

  *gbank_out = gbank;
  
  SUC_RETURN(true);
}

static bool _gbank_get_rotation(Axis axis, double phase, double unit, void** matrix_out)
{
  COMPLEX* matrix = NULL;
  double theta = phase * unit;

  if (!(matrix = (COMPLEX*)malloc(sizeof(COMPLEX) * 4)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  switch (axis) {
  case X_AXIS:
    matrix[IDX2(0, 0)] = cos(theta/2.0);
    matrix[IDX2(0, 1)] = - 1.0 * COMP_I * sin(theta / 2.0);
    matrix[IDX2(1, 0)] = - 1.0 * COMP_I * sin(theta / 2.0);
    matrix[IDX2(1, 1)] = cos(theta / 2.0);
    break;
  case Y_AXIS:
    matrix[IDX2(0, 0)] = cos(theta / 2.0);
    matrix[IDX2(0, 1)] = -sin(theta / 2.0);
    matrix[IDX2(1, 0)] = sin(theta / 2.0);
    matrix[IDX2(1, 1)] = cos(theta / 2.0);
    break;
  case Z_AXIS:
    matrix[IDX2(0, 0)] = cos(theta/2.0) - 1.0 * COMP_I * sin(theta / 2.0);
    matrix[IDX2(0, 1)] = 0.0 + 0.0 * COMP_I;
    matrix[IDX2(1, 0)] = 0.0 + 0.0 * COMP_I;
    matrix[IDX2(1, 1)] = cos(theta/2.0) + 1.0 * COMP_I * sin(theta / 2.0);
    break;
  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }

  *matrix_out = matrix;

  SUC_RETURN(true);
}

static bool _gbank_get_ctr_rotation(Axis axis, double phase, double unit, void** matrix_out)
{
  COMPLEX*	matrix = NULL;
  double	theta;
  int		i;

  theta = phase * unit;

  if (!(matrix = (COMPLEX*)malloc(sizeof(COMPLEX) * 16)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  for (i=0; i<16; i++) matrix[i] = 0.0 + 0.0 * COMP_I;

  switch (axis) {
  case X_AXIS:
    matrix[IDX4(0, 0)] = 1.0 + 0.0 * COMP_I;
    matrix[IDX4(1, 1)] = 1.0 + 0.0 * COMP_I;
    matrix[IDX4(2, 2)] = cos(theta/2.0);
    matrix[IDX4(2, 3)] = - 1.0 * COMP_I * sin(theta / 2.0);
    matrix[IDX4(3, 2)] = - 1.0 * COMP_I * sin(theta / 2.0);
    matrix[IDX4(3, 3)] = cos(theta/2.0);
    break;
  case Y_AXIS:
    matrix[IDX4(0, 0)] = 1.0 + 0.0 * COMP_I;
    matrix[IDX4(1, 1)] = 1.0 + 0.0 * COMP_I;
    matrix[IDX4(2, 2)] = cos(theta / 2.0);
    matrix[IDX4(2, 3)] = -sin(theta / 2.0);
    matrix[IDX4(3, 2)] = sin(theta / 2.0);
    matrix[IDX4(3, 3)] = cos(theta / 2.0);
    break;
  case Z_AXIS:
    matrix[IDX4(0, 0)] = 1.0 + 0.0 * COMP_I;
    matrix[IDX4(1, 1)] = 1.0 + 0.0 * COMP_I;
    matrix[IDX4(2, 2)] = cos(theta / 2.0) - 1.0 * COMP_I * sin(theta / 2.0);
    matrix[IDX4(2, 3)] = 0.0 + 0.0 * COMP_I;
    matrix[IDX4(3, 2)] = 0.0 + 0.0 * COMP_I;
    matrix[IDX4(3, 3)] = cos(theta / 2.0) + 1.0 * COMP_I * sin(theta / 2.0);
    break;
  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }

  *matrix_out = matrix;

  SUC_RETURN(true);
}

static bool _gbank_get_phase_shift(double phase, double unit, void** matrix_out)
{
  COMPLEX*	matrix = NULL;
  double	theta;

  theta  = phase * unit;

  if (!(matrix = (COMPLEX*)malloc(sizeof(COMPLEX) * 4)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  matrix[IDX2(0, 0)] = 1.0 + 0.0 * COMP_I;
  matrix[IDX2(0, 1)] = 0.0 + 0.0 * COMP_I;
  matrix[IDX2(1, 0)] = 0.0 + 0.0 * COMP_I;
  matrix[IDX2(1, 1)] = cos(theta) + 1.0 * COMP_I * sin(theta);

  *matrix_out = matrix;

  SUC_RETURN(true);
}

static bool _gbank_get_ctr_phase_shift(double phase, double unit, void** matrix_out)
{
  COMPLEX*	matrix = NULL;
  double	theta;
  int		i;

  theta = phase * unit;

  if (!(matrix = (COMPLEX*)malloc(sizeof(COMPLEX) * 16)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  for (i=0; i<16; i++) matrix[i] = 0.0 + 0.0 * COMP_I;
  matrix[IDX4(0, 0)] = 1.0 + 0.0 * COMP_I;
  matrix[IDX4(1, 1)] = 1.0 + 0.0 * COMP_I;
  matrix[IDX4(2, 2)] = 1.0 + 0.0 * COMP_I;
  matrix[IDX4(3, 3)] = cos(theta) + 1.0 * COMP_I * sin(theta);

  *matrix_out = matrix;

  SUC_RETURN(true);
}

static bool _gbank_get_rotation_xx(double phase, double unit, void** matrix_out)
{
  COMPLEX*	matrix = NULL;
  double	theta;
  int           i;
  
  theta  = phase * unit;
  
  if (!(matrix = (COMPLEX*)malloc(sizeof(COMPLEX) * 16)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  for (i=0; i<16; i++) matrix[i] = 0.0 + 0.0 * COMP_I;
  matrix[IDX4(0, 0)] = cos(theta / 2.0) + 0.0 * COMP_I;
  matrix[IDX4(1, 1)] = cos(theta / 2.0) + 0.0 * COMP_I;
  matrix[IDX4(2, 2)] = cos(theta / 2.0) + 0.0 * COMP_I;
  matrix[IDX4(3, 3)] = cos(theta / 2.0) + 0.0 * COMP_I;
  matrix[IDX4(0, 3)] = 0.0 - 1.0 * COMP_I * sin(theta / 2.0);
  matrix[IDX4(1, 2)] = 0.0 - 1.0 * COMP_I * sin(theta / 2.0);
  matrix[IDX4(2, 1)] = 0.0 - 1.0 * COMP_I * sin(theta / 2.0);
  matrix[IDX4(3, 0)] = 0.0 - 1.0 * COMP_I * sin(theta / 2.0);
  
  *matrix_out = matrix;
  
  SUC_RETURN(true);
}

static bool _gbank_get_rotation_yy(double phase, double unit, void** matrix_out)
{
  COMPLEX*	matrix = NULL;
  double	theta;
  int           i;
  
  theta  = phase * unit;
  
  if (!(matrix = (COMPLEX*)malloc(sizeof(COMPLEX) * 16)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  for (i=0; i<16; i++) matrix[i] = 0.0 + 0.0 * COMP_I;
  matrix[IDX4(0, 0)] = cos(theta / 2.0) + 0.0 * COMP_I;
  matrix[IDX4(1, 1)] = cos(theta / 2.0) + 0.0 * COMP_I;
  matrix[IDX4(2, 2)] = cos(theta / 2.0) + 0.0 * COMP_I;
  matrix[IDX4(3, 3)] = cos(theta / 2.0) + 0.0 * COMP_I;
  matrix[IDX4(0, 3)] = 0.0 + 1.0 * COMP_I * sin(theta / 2.0);
  matrix[IDX4(1, 2)] = 0.0 - 1.0 * COMP_I * sin(theta / 2.0);
  matrix[IDX4(2, 1)] = 0.0 - 1.0 * COMP_I * sin(theta / 2.0);
  matrix[IDX4(3, 0)] = 0.0 + 1.0 * COMP_I * sin(theta / 2.0);
  
  *matrix_out = matrix;
  
  SUC_RETURN(true);
}

static bool _gbank_get_rotation_zz(double phase, double unit, void** matrix_out)
{
  COMPLEX*	matrix = NULL;
  double	theta;
  int           i;
  
  theta  = phase * unit;
  
  if (!(matrix = (COMPLEX*)malloc(sizeof(COMPLEX) * 16)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  for (i=0; i<16; i++) matrix[i] = 0.0 + 0.0 * COMP_I;
  matrix[IDX4(0, 0)] = cexp(-1.0 * COMP_I * theta / 2.0);
  matrix[IDX4(1, 1)] = cexp(1.0 * COMP_I * theta / 2.0);
  matrix[IDX4(2, 2)] = cexp(1.0 * COMP_I * theta / 2.0);
  matrix[IDX4(3, 3)] = cexp(-1.0 * COMP_I * theta / 2.0);

  *matrix_out = matrix;
  
  SUC_RETURN(true);
}

static bool _gbank_get(GBank* gbank, Kind kind, void** matrix_out)
{
  COMPLEX*	matrix = NULL;
  int		size   = 0;

  if (gbank == NULL)
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  /* get matrix size */

  switch (kind) {
  case PAULI_X:
  case PAULI_Y:
  case PAULI_Z:
  case ROOT_PAULI_X:
  case ROOT_PAULI_X_:
  case PHASE_SHIFT_T:
  case PHASE_SHIFT_T_:
  case PHASE_SHIFT_S:
  case PHASE_SHIFT_S_:
  case HADAMARD:
    size = 4;
    break;

  case CONTROLLED_X:
  case CONTROLLED_Y:
  case CONTROLLED_Z:
  case CONTROLLED_XR:
  case CONTROLLED_XR_:
  case CONTROLLED_H:
  case CONTROLLED_S:
  case CONTROLLED_S_:
  case CONTROLLED_T:
  case CONTROLLED_T_:
  case SWAP_QUBITS:
    size = 16;
    break;
    
  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }

  /* get unitary matrix */

  if (!(matrix = (COMPLEX*)malloc(sizeof(COMPLEX) * size)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  switch (kind) {
  case PAULI_X:
    memcpy(matrix, gbank->PauliX, sizeof(COMPLEX) * size);
    break;
  case PAULI_Y:
    memcpy(matrix, gbank->PauliY, sizeof(COMPLEX) * size);
    break;
  case PAULI_Z:
    memcpy(matrix, gbank->PauliZ, sizeof(COMPLEX) * size);
    break;
  case ROOT_PAULI_X:
    memcpy(matrix, gbank->RootPauliX, sizeof(COMPLEX) * size);
    break;
  case ROOT_PAULI_X_:
    memcpy(matrix, gbank->RootPauliX_, sizeof(COMPLEX) * size);
    break;
  case PHASE_SHIFT_T:
    memcpy(matrix, gbank->PhaseShiftT, sizeof(COMPLEX) * size);
    break;
  case PHASE_SHIFT_T_:
    memcpy(matrix, gbank->PhaseShiftT_, sizeof(COMPLEX) * size);
    break;
  case PHASE_SHIFT_S:
    memcpy(matrix, gbank->PhaseShiftS, sizeof(COMPLEX) * size);
    break;
  case PHASE_SHIFT_S_:
    memcpy(matrix, gbank->PhaseShiftS_, sizeof(COMPLEX) * size);
    break;
  case HADAMARD:
    memcpy(matrix, gbank->Hadamard, sizeof(COMPLEX) * size);
    break;
  case CONTROLLED_X:
    memcpy(matrix, gbank->ControlledX, sizeof(COMPLEX) * size);
    break;
  case CONTROLLED_Y:
    memcpy(matrix, gbank->ControlledY, sizeof(COMPLEX) * size);
    break;
  case CONTROLLED_Z:
    memcpy(matrix, gbank->ControlledZ, sizeof(COMPLEX) * size);
    break;
  case CONTROLLED_XR:
    memcpy(matrix, gbank->ControlledXR, sizeof(COMPLEX) * size);
    break;
  case CONTROLLED_XR_:
    memcpy(matrix, gbank->ControlledXR_, sizeof(COMPLEX) * size);
    break;
  case CONTROLLED_H:
    memcpy(matrix, gbank->ControlledH, sizeof(COMPLEX) * size);
    break;
  case CONTROLLED_S:
    memcpy(matrix, gbank->ControlledS, sizeof(COMPLEX) * size);
    break;
  case CONTROLLED_S_:
    memcpy(matrix, gbank->ControlledS_, sizeof(COMPLEX) * size);
    break;
  case CONTROLLED_T:
    memcpy(matrix, gbank->ControlledT, sizeof(COMPLEX) * size);
    break;
  case CONTROLLED_T_:
    memcpy(matrix, gbank->ControlledT_, sizeof(COMPLEX) * size);
    break;
  case SWAP_QUBITS:
    memcpy(matrix, gbank->Swap, sizeof(COMPLEX) * size);
    break;
  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }

  *matrix_out = matrix;
  
  SUC_RETURN(true);
}

bool gbank_get_unitary(GBank* gbank, Kind kind, double para_phase, double para_gphase,
		       double para_factor, int* dim_out, void** matrix_out)
{
  COMPLEX*	matrix = NULL;
  int		dim    = 0;
  double        phase = para_phase * para_factor;
  
  if (gbank == NULL)
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  switch (kind) {
    /*
     * 1-qubit
     */
  case PAULI_X:
  case PAULI_Y:
  case PAULI_Z:
  case ROOT_PAULI_X:
  case ROOT_PAULI_X_:
  case PHASE_SHIFT_T:
  case PHASE_SHIFT_T_:
  case PHASE_SHIFT_S:
  case PHASE_SHIFT_S_:
  case HADAMARD:
    /* 1-qubit gate */
    dim = 2;
    if (!(_gbank_get(gbank, kind, (void**)&matrix)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    break;
  case ROTATION_X:
    /* 1-qubit gate (1-parameter) */
    dim = 2;
    if (!(_gbank_get_rotation(X_AXIS, phase, M_PI, (void**)&matrix)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    break;
  case ROTATION_Y:
    /* 1-qubit gate (1-parameter) */
    dim = 2;
    if (!(_gbank_get_rotation(Y_AXIS, phase, M_PI, (void**)&matrix)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    break;
  case ROTATION_Z:
    /* 1-qubit gate (1-parameter) */
    dim = 2;
    if (!(_gbank_get_rotation(Z_AXIS, phase, M_PI, (void**)&matrix)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    break;
  case PHASE_SHIFT:
    /* 1-qubit gate (1-parameter) */
    dim = 2;
    if (!(_gbank_get_phase_shift(phase, M_PI, (void**)&matrix)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    break;

    /*
     * 2-qubit
     */
  case CONTROLLED_X:
  case CONTROLLED_Y:
  case CONTROLLED_Z:
  case CONTROLLED_XR:
  case CONTROLLED_XR_:
  case CONTROLLED_H:
  case CONTROLLED_S:
  case CONTROLLED_S_:
  case CONTROLLED_T:
  case CONTROLLED_T_:
  case SWAP_QUBITS:
    /* 2-qubit gate */
    dim = 4;
    if (!(_gbank_get(gbank, kind, (void**)&matrix)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    break;
  case CONTROLLED_RX:
    /* 2-qubit gate (1-parameter) */
    dim = 4;
    if (!(_gbank_get_ctr_rotation(X_AXIS, phase, M_PI, (void**)&matrix)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    break;
  case CONTROLLED_RY:
    /* 2-qubit gate (1-parameter) */
    dim = 4;
    if (!(_gbank_get_ctr_rotation(Y_AXIS, phase, M_PI, (void**)&matrix)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    break;
  case CONTROLLED_RZ:
    /* 2-qubit gate (1-parameter) */
    dim = 4;
    if (!(_gbank_get_ctr_rotation(Z_AXIS, phase, M_PI, (void**)&matrix)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    break;
  case CONTROLLED_P:
    /* 2-qubit gate (1-parameter) */
    dim = 4;
    if (!(_gbank_get_ctr_phase_shift(phase, M_PI, (void**)&matrix)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    break;
  case ROTATION_XX:
    /* 2-qubit gate (1-parameter) */
    dim = 4;
    if (!(_gbank_get_rotation_xx(phase, M_PI, (void**)&matrix)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    break;
  case ROTATION_YY:
    /* 2-qubit gate (1-parameter) */
    dim = 4;
    if (!(_gbank_get_rotation_yy(phase, M_PI, (void**)&matrix)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    break;
  case ROTATION_ZZ:
    /* 2-qubit gate (1-parameter) */
    dim = 4;
    if (!(_gbank_get_rotation_zz(phase, M_PI, (void**)&matrix)))
      ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
    break;

  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }

  *matrix_out = matrix;
  *dim_out = dim;

  SUC_RETURN(true);
}
