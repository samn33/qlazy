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
  case CONTROLLED_XR:
    matrix = gbank->ControlledXR;
    break;
  case CONTROLLED_XR_:
    matrix = gbank->ControlledXR_;
    break;
  case CONTROLLED_H:
    matrix = gbank->ControlledH;
    break;
  case CONTROLLED_S:
    matrix = gbank->ControlledS;
    break;
  case CONTROLLED_S_:
    matrix = gbank->ControlledS_;
    break;
  case CONTROLLED_T:
    matrix = gbank->ControlledT;
    break;
  case CONTROLLED_T_:
    matrix = gbank->ControlledT_;
    break;
  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }

  *matrix_out = matrix;
  
  SUC_RETURN(true);
}
