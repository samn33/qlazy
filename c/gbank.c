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
  gbank->PauliY[1] = -1.0i;
  gbank->PauliY[2] = 1.0i;
  gbank->PauliY[3] =  0.0;

  gbank->PauliZ[0] =  1.0;
  gbank->PauliZ[1] =  0.0;
  gbank->PauliZ[2] =  0.0;
  gbank->PauliZ[3] = -1.0;

  gbank->RootPauliX[0] = (1.0+1.0i)/2.0;
  gbank->RootPauliX[1] = (1.0-1.0i)/2.0;
  gbank->RootPauliX[2] = (1.0-1.0i)/2.0;
  gbank->RootPauliX[3] = (1.0+1.0i)/2.0;

  gbank->RootPauliX_[0] = (1.0-1.0i)/2.0;
  gbank->RootPauliX_[1] = (1.0+1.0i)/2.0;
  gbank->RootPauliX_[2] = (1.0+1.0i)/2.0;
  gbank->RootPauliX_[3] = (1.0-1.0i)/2.0;

  gbank->Hadamard[0] =  1.0/sqrt(2.0);
  gbank->Hadamard[1] =  1.0/sqrt(2.0);
  gbank->Hadamard[2] =  1.0/sqrt(2.0);
  gbank->Hadamard[3] = -1.0/sqrt(2.0);

  gbank->PhaseShiftS[0] =  1.0;
  gbank->PhaseShiftS[1] =  0.0;
  gbank->PhaseShiftS[2] =  0.0;
  gbank->PhaseShiftS[3] =  1.0i;

  gbank->PhaseShiftS_[0] =   1.0;
  gbank->PhaseShiftS_[1] =   0.0;
  gbank->PhaseShiftS_[2] =   0.0;
  gbank->PhaseShiftS_[3] =  -1.0i;

  gbank->PhaseShiftT[0] =  1.0;
  gbank->PhaseShiftT[1] =  0.0;
  gbank->PhaseShiftT[2] =  0.0;
  gbank->PhaseShiftT[3] =  (1.0+1.0i)/sqrt(2.0);

  gbank->PhaseShiftT_[0] =  1.0;
  gbank->PhaseShiftT_[1] =  0.0;
  gbank->PhaseShiftT_[2] =  0.0;
  gbank->PhaseShiftT_[3] =  (1.0-1.0i)/sqrt(2.0);

  gbank->ControlledX[0] = 1.0;
  gbank->ControlledX[1] = 0.0;
  gbank->ControlledX[2] = 0.0;
  gbank->ControlledX[3] = 0.0;
  gbank->ControlledX[4] = 0.0;
  gbank->ControlledX[5] = 1.0;
  gbank->ControlledX[6] = 0.0;
  gbank->ControlledX[7] = 0.0;
  gbank->ControlledX[8] = 0.0;
  gbank->ControlledX[9] = 0.0;
  gbank->ControlledX[10] = 0.0;
  gbank->ControlledX[11] = 1.0;
  gbank->ControlledX[12] = 0.0;
  gbank->ControlledX[13] = 0.0;
  gbank->ControlledX[14] = 1.0;
  gbank->ControlledX[15] = 0.0;

  gbank->ControlledY[0] = 1.0;
  gbank->ControlledY[1] = 0.0;
  gbank->ControlledY[2] = 0.0;
  gbank->ControlledY[3] = 0.0;
  gbank->ControlledY[4] = 0.0;
  gbank->ControlledY[5] = 1.0;
  gbank->ControlledY[6] = 0.0;
  gbank->ControlledY[7] = 0.0;
  gbank->ControlledY[8] = 0.0;
  gbank->ControlledY[9] = 0.0;
  gbank->ControlledY[10] = 0.0;
  gbank->ControlledY[11] = -1.0i;
  gbank->ControlledY[12] = 0.0;
  gbank->ControlledY[13] = 0.0;
  gbank->ControlledY[14] = 1.0i;
  gbank->ControlledY[15] = 0.0;

  gbank->ControlledZ[0] =  1.0;
  gbank->ControlledZ[1] =  0.0;
  gbank->ControlledZ[2] =  0.0;
  gbank->ControlledZ[3] =  0.0;
  gbank->ControlledZ[4] =  0.0;
  gbank->ControlledZ[5] =  1.0;
  gbank->ControlledZ[6] =  0.0;
  gbank->ControlledZ[7] =  0.0;
  gbank->ControlledZ[8] =  0.0;
  gbank->ControlledZ[9] =  0.0;
  gbank->ControlledZ[10] =  1.0;
  gbank->ControlledZ[11] =  0.0;
  gbank->ControlledZ[12] =  0.0;
  gbank->ControlledZ[13] =  0.0;
  gbank->ControlledZ[14] =  0.0;
  gbank->ControlledZ[15] = -1.0;

  gbank->ControlledH[0] =  1.0;
  gbank->ControlledH[1] =  0.0;
  gbank->ControlledH[2] =  0.0;
  gbank->ControlledH[3] =  0.0;
  gbank->ControlledH[4] =  0.0;
  gbank->ControlledH[5] =  1.0;
  gbank->ControlledH[6] =  0.0;
  gbank->ControlledH[7] =  0.0;
  gbank->ControlledH[8] =  0.0;
  gbank->ControlledH[9] =  0.0;
  gbank->ControlledH[10] =  1.0/sqrt(2.0);
  gbank->ControlledH[11] =  1.0/sqrt(2.0);
  gbank->ControlledH[12] =  0.0;
  gbank->ControlledH[13] =  0.0;
  gbank->ControlledH[14] =  1.0/sqrt(2.0);
  gbank->ControlledH[15] = -1.0/sqrt(2.0);

  *gbank_out = gbank;
  
  SUC_RETURN(true);
}

bool gbank_get_rotation(Axis axis, double phase, double unit, void** matrix_out)
{
  COMPLEX* matrix = NULL;
  double theta = phase * unit;

  if (!(matrix = (COMPLEX*)malloc(sizeof(COMPLEX)*4)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  switch (axis) {
  case X_AXIS:
    matrix[IDX2(0,0)] = cos(theta/2.0);
    matrix[IDX2(0,1)] = - 1.0i * sin(theta/2.0);
    matrix[IDX2(1,0)] = - 1.0i * sin(theta/2.0);
    matrix[IDX2(1,1)] = cos(theta/2.0);
    break;
  case Y_AXIS:
    matrix[IDX2(0,0)] = cos(theta/2.0);
    matrix[IDX2(0,1)] = -sin(theta/2.0);
    matrix[IDX2(1,0)] = sin(theta/2.0);
    matrix[IDX2(1,1)] = cos(theta/2.0);
    break;
  case Z_AXIS:
    matrix[IDX2(0,0)] = cos(theta/2.0) - 1.0i * sin(theta/2.0);
    matrix[IDX2(0,1)] = 0.0 + 0.0i;
    matrix[IDX2(1,0)] = 0.0 + 0.0i;
    matrix[IDX2(1,1)] = cos(theta/2.0) + 1.0i * sin(theta/2.0);
    break;
  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }

  *matrix_out = matrix;

  SUC_RETURN(true);
}

bool gbank_get_ctr_rotation(Axis axis, double phase, double unit, void** matrix_out)
{
  COMPLEX* matrix = NULL;
  double theta = phase * unit;

  if (!(matrix = (COMPLEX*)malloc(sizeof(COMPLEX)*16)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  for (int i=0; i<16; i++) matrix[i] = 0.0 + 0.0i;
  
  switch (axis) {
  case X_AXIS:
    matrix[IDX4(0,0)] = 1.0 + 0.0i;
    matrix[IDX4(1,1)] = 1.0 + 0.0i;
    matrix[IDX4(2,2)] = cos(theta/2.0);
    matrix[IDX4(2,3)] = - 1.0i * sin(theta/2.0);
    matrix[IDX4(3,2)] = - 1.0i * sin(theta/2.0);
    matrix[IDX4(3,3)] = cos(theta/2.0);
    break;
  case Y_AXIS:
    matrix[IDX4(0,0)] = 1.0 + 0.0i;
    matrix[IDX4(1,1)] = 1.0 + 0.0i;
    matrix[IDX4(2,2)] = cos(theta/2.0);
    matrix[IDX4(2,3)] = -sin(theta/2.0);
    matrix[IDX4(3,2)] = sin(theta/2.0);
    matrix[IDX4(3,3)] = cos(theta/2.0);
    break;
  case Z_AXIS:
    matrix[IDX4(0,0)] = 1.0 + 0.0i;
    matrix[IDX4(1,1)] = 1.0 + 0.0i;
    matrix[IDX4(2,2)] = cos(theta/2.0) - 1.0i * sin(theta/2.0);
    matrix[IDX4(2,3)] = 0.0 + 0.0i;
    matrix[IDX4(3,2)] = 0.0 + 0.0i;
    matrix[IDX4(3,3)] = cos(theta/2.0) + 1.0i * sin(theta/2.0);
    break;
  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }

  *matrix_out = matrix;

  SUC_RETURN(true);
}

bool gbank_get_phase_shift(double phase, double unit, void** matrix_out)
{
  COMPLEX* matrix = NULL;
  double theta = phase * unit;

  if (!(matrix = (COMPLEX*)malloc(sizeof(COMPLEX)*4)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  matrix[IDX2(0,0)] = 1.0 + 0.0i;
  matrix[IDX2(0,1)] = 0.0 + 0.0i;
  matrix[IDX2(1,0)] = 0.0 + 0.0i;
  matrix[IDX2(1,1)] = cos(theta) + 1.0i * sin(theta);

  *matrix_out = matrix;

  SUC_RETURN(true);
}

bool gbank_get_ctr_phase_shift(double phase, double unit, void** matrix_out)
{
  COMPLEX* matrix = NULL;
  double theta = phase * unit;

  if (!(matrix = (COMPLEX*)malloc(sizeof(COMPLEX)*16)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  for (int i=0; i<16; i++) matrix[i] = 0.0 + 0.0i;
  matrix[IDX4(0,0)] = 1.0 + 0.0i;
  matrix[IDX4(1,1)] = 1.0 + 0.0i;
  matrix[IDX4(2,2)] = 1.0 + 0.0i;
  matrix[IDX4(3,3)] = cos(theta) + 1.0i * sin(theta);

  *matrix_out = matrix;

  SUC_RETURN(true);
}

bool gbank_get(GBank* gbank, Kind kind, void** matrix_out)
{
  COMPLEX* matrix = NULL;

  if (gbank == NULL)
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  switch (kind) {
  case PAULI_X:
    matrix = gbank->PauliX;
    break;
  case PAULI_Y:
    matrix = gbank->PauliY;
    break;
  case PAULI_Z:
    matrix = gbank->PauliZ;
    break;
  case ROOT_PAULI_X:
    matrix = gbank->RootPauliX;
    break;
  case ROOT_PAULI_X_:
    matrix = gbank->RootPauliX_;
    break;
  case PHASE_SHIFT_T:
    matrix = gbank->PhaseShiftT;
    break;
  case PHASE_SHIFT_T_:
    matrix = gbank->PhaseShiftT_;
    break;
  case PHASE_SHIFT_S:
    matrix = gbank->PhaseShiftS;
    break;
  case PHASE_SHIFT_S_:
    matrix = gbank->PhaseShiftS_;
    break;
  case HADAMARD:
    matrix = gbank->Hadamard;
    break;
  case CONTROLLED_X:
    matrix = gbank->ControlledX;
    break;
  case CONTROLLED_Y:
    matrix = gbank->ControlledY;
    break;
  case CONTROLLED_Z:
    matrix = gbank->ControlledZ;
    break;
  case CONTROLLED_H:
    matrix = gbank->ControlledH;
    break;
  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }

  *matrix_out = matrix;
  
  SUC_RETURN(true);
}
