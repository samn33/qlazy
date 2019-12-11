/*
 *  qgate.c
 */

#include "qlazy.h"

bool qgate_get_symbol(Kind kind, char* symbol)
{
  switch (kind) {
  case INIT:
    strcpy(symbol,"init");
    break;
  case CIRC:
    strcpy(symbol,"circ");
    break;
  case GATES:
    strcpy(symbol,"gates");
    break;
  case SHOW:
    strcpy(symbol,"show");
    break;
  case BLOCH:
    strcpy(symbol,"bloch");
    break;
  case ECHO:
    strcpy(symbol,"echo");
    break;
  case OUTPUT:
    strcpy(symbol,"output");
    break;
  case HELP:
    strcpy(symbol,"help");
    break;
  case QUIT:
    strcpy(symbol,"quit");
    break;
  case PAULI_X:
    strcpy(symbol,"X");
    break;
  case PAULI_Y:
    strcpy(symbol,"Y");
    break;
  case PAULI_Z:
    strcpy(symbol,"Z");
    break;
  case ROOT_PAULI_X:
    strcpy(symbol,"XR");
    break;
  case ROOT_PAULI_X_:
    strcpy(symbol,"XR+");
    break;
  case HADAMARD:
    strcpy(symbol,"H");
    break;
  case PHASE_SHIFT_S:
    strcpy(symbol,"S");
    break;
  case PHASE_SHIFT_S_:
    strcpy(symbol,"S+");
    break;
  case PHASE_SHIFT_T:
    strcpy(symbol,"T");
    break;
  case PHASE_SHIFT_T_:
    strcpy(symbol,"T+");
    break;
  case PHASE_SHIFT:
    strcpy(symbol,"P");
    break;
  case ROTATION_X:
    strcpy(symbol,"RX");
    break;
  case ROTATION_Y:
    strcpy(symbol,"RY");
    break;
  case ROTATION_Z:
    strcpy(symbol,"RZ");
    break;
  case ROTATION_U1:
    strcpy(symbol,"U1");
    break;
  case ROTATION_U2:
    strcpy(symbol,"U2");
    break;
  case ROTATION_U3:
    strcpy(symbol,"U3");
    break;
  case CONTROLLED_X:
    strcpy(symbol,"CX");
    break;
  case CONTROLLED_Y:
    strcpy(symbol,"CY");
    break;
  case CONTROLLED_Z:
    strcpy(symbol,"CZ");
    break;
  case CONTROLLED_XR:
    strcpy(symbol,"CXR");
    break;
  case CONTROLLED_XR_:
    strcpy(symbol,"CXR+");
    break;
  case CONTROLLED_H:
    strcpy(symbol,"CH");
    break;
  case CONTROLLED_S:
    strcpy(symbol,"CS");
    break;
  case CONTROLLED_S_:
    strcpy(symbol,"CS+");
    break;
  case CONTROLLED_T:
    strcpy(symbol,"CT");
    break;
  case CONTROLLED_T_:
    strcpy(symbol,"CT+");
    break;
  case CONTROLLED_P:
    strcpy(symbol,"CP");
    break;
  case CONTROLLED_RX:
    strcpy(symbol,"CRX");
    break;
  case CONTROLLED_RY:
    strcpy(symbol,"CRY");
    break;
  case CONTROLLED_RZ:
    strcpy(symbol,"CRZ");
    break;
  case CONTROLLED_U1:
    strcpy(symbol,"CU1");
    break;
  case CONTROLLED_U2:
    strcpy(symbol,"CU2");
    break;
  case CONTROLLED_U3:
    strcpy(symbol,"CU3");
    break;
  case SWAP:
    strcpy(symbol,"SW");
    break;
  case MEASURE:
    strcpy(symbol,"M");
    break;
  case MEASURE_X:
    strcpy(symbol,"MX");
    break;
  case MEASURE_Y:
    strcpy(symbol,"MY");
    break;
  case MEASURE_Z:
    strcpy(symbol,"MZ");
    break;
  case MEASURE_BELL:
    strcpy(symbol,"MB");
    break;
  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }

  SUC_RETURN(true);
}

bool qgate_get_kind(char* symbol, Kind* kind_out)
{
  Kind kind;

  if (strcmp(symbol,"%")          == 0) kind = INIT;
  else if (strcmp(symbol,"init")  == 0) kind = INIT;
  else if (strcmp(symbol,"&")     == 0) kind = CIRC;
  else if (strcmp(symbol,"circ")  == 0) kind = CIRC;
  else if (strcmp(symbol,"!")     == 0) kind = GATES;
  else if (strcmp(symbol,"gates") == 0) kind = GATES;
  else if (strcmp(symbol,"-")     == 0) kind = SHOW;
  else if (strcmp(symbol,"show")  == 0) kind = SHOW;
  else if (strcmp(symbol,"|")     == 0) kind = BLOCH;
  else if (strcmp(symbol,"bloch") == 0) kind = BLOCH;
  else if (strcmp(symbol,"@")     == 0) kind = ECHO;
  else if (strcmp(symbol,"echo")  == 0) kind = ECHO;
  else if (strcmp(symbol,">")     == 0) kind = OUTPUT;
  else if (strcmp(symbol,"output")== 0) kind = OUTPUT;
  else if (strcmp(symbol,"?")     == 0) kind = HELP;
  else if (strcmp(symbol,"help")  == 0) kind = HELP;
  else if (strcmp(symbol,".")     == 0) kind = QUIT;
  else if (strcmp(symbol,"quit")  == 0) kind = QUIT;
  else if (strcmp(symbol,"X")     == 0) kind = PAULI_X;
  else if (strcmp(symbol,"x")     == 0) kind = PAULI_X;
  else if (strcmp(symbol,"Y")     == 0) kind = PAULI_Y;
  else if (strcmp(symbol,"y")     == 0) kind = PAULI_Y;
  else if (strcmp(symbol,"Z")     == 0) kind = PAULI_Z;
  else if (strcmp(symbol,"z")     == 0) kind = PAULI_Z;
  else if (strcmp(symbol,"XR")    == 0) kind = ROOT_PAULI_X;
  else if (strcmp(symbol,"xr")    == 0) kind = ROOT_PAULI_X;
  else if (strcmp(symbol,"XR+")   == 0) kind = ROOT_PAULI_X_;
  else if (strcmp(symbol,"xr+")   == 0) kind = ROOT_PAULI_X_;
  else if (strcmp(symbol,"H")     == 0) kind = HADAMARD; 
  else if (strcmp(symbol,"h")     == 0) kind = HADAMARD; 
  else if (strcmp(symbol,"S")     == 0) kind = PHASE_SHIFT_S; 
  else if (strcmp(symbol,"s")     == 0) kind = PHASE_SHIFT_S; 
  else if (strcmp(symbol,"S+")    == 0) kind = PHASE_SHIFT_S_; 
  else if (strcmp(symbol,"s+")    == 0) kind = PHASE_SHIFT_S_; 
  else if (strcmp(symbol,"T")     == 0) kind = PHASE_SHIFT_T; 
  else if (strcmp(symbol,"t")     == 0) kind = PHASE_SHIFT_T; 
  else if (strcmp(symbol,"T+")    == 0) kind = PHASE_SHIFT_T_; 
  else if (strcmp(symbol,"t+")    == 0) kind = PHASE_SHIFT_T_; 
  else if (strcmp(symbol,"P")     == 0) kind = PHASE_SHIFT; 
  else if (strcmp(symbol,"p")     == 0) kind = PHASE_SHIFT; 
  else if (strcmp(symbol,"RX")    == 0) kind = ROTATION_X;
  else if (strcmp(symbol,"rx")    == 0) kind = ROTATION_X;
  else if (strcmp(symbol,"RY")    == 0) kind = ROTATION_Y;
  else if (strcmp(symbol,"ry")    == 0) kind = ROTATION_Y;
  else if (strcmp(symbol,"RZ")    == 0) kind = ROTATION_Z;
  else if (strcmp(symbol,"rz")    == 0) kind = ROTATION_Z;
  else if (strcmp(symbol,"U1")    == 0) kind = ROTATION_U1;
  else if (strcmp(symbol,"u1")    == 0) kind = ROTATION_U1;
  else if (strcmp(symbol,"U2")    == 0) kind = ROTATION_U2;
  else if (strcmp(symbol,"u2")    == 0) kind = ROTATION_U2;
  else if (strcmp(symbol,"U3")    == 0) kind = ROTATION_U3;
  else if (strcmp(symbol,"u3")    == 0) kind = ROTATION_U3;
  else if (strcmp(symbol,"CX")    == 0) kind = CONTROLLED_X;
  else if (strcmp(symbol,"cx")    == 0) kind = CONTROLLED_X;
  else if (strcmp(symbol,"CY")    == 0) kind = CONTROLLED_Y;
  else if (strcmp(symbol,"cy")    == 0) kind = CONTROLLED_Y;
  else if (strcmp(symbol,"CZ")    == 0) kind = CONTROLLED_Z;
  else if (strcmp(symbol,"cz")    == 0) kind = CONTROLLED_Z;
  else if (strcmp(symbol,"CXR")   == 0) kind = CONTROLLED_XR;
  else if (strcmp(symbol,"cxr")   == 0) kind = CONTROLLED_XR;
  else if (strcmp(symbol,"CXR+")  == 0) kind = CONTROLLED_XR_;
  else if (strcmp(symbol,"cxr+")  == 0) kind = CONTROLLED_XR_;
  else if (strcmp(symbol,"CH")    == 0) kind = CONTROLLED_H;
  else if (strcmp(symbol,"ch")    == 0) kind = CONTROLLED_H;
  else if (strcmp(symbol,"CS")    == 0) kind = CONTROLLED_S;
  else if (strcmp(symbol,"cs")    == 0) kind = CONTROLLED_S;
  else if (strcmp(symbol,"CS+")   == 0) kind = CONTROLLED_S_;
  else if (strcmp(symbol,"cs+")   == 0) kind = CONTROLLED_S_;
  else if (strcmp(symbol,"CT")    == 0) kind = CONTROLLED_T;
  else if (strcmp(symbol,"ct")    == 0) kind = CONTROLLED_T;
  else if (strcmp(symbol,"CT+")   == 0) kind = CONTROLLED_T_;
  else if (strcmp(symbol,"ct+")   == 0) kind = CONTROLLED_T_;
  else if (strcmp(symbol,"CP")    == 0) kind = CONTROLLED_P;
  else if (strcmp(symbol,"cp")    == 0) kind = CONTROLLED_P;
  else if (strcmp(symbol,"CRX")   == 0) kind = CONTROLLED_RX;
  else if (strcmp(symbol,"crx")   == 0) kind = CONTROLLED_RX;
  else if (strcmp(symbol,"CRY")   == 0) kind = CONTROLLED_RY;
  else if (strcmp(symbol,"cry")   == 0) kind = CONTROLLED_RY;
  else if (strcmp(symbol,"CRZ")   == 0) kind = CONTROLLED_RZ;
  else if (strcmp(symbol,"crz")   == 0) kind = CONTROLLED_RZ;
  else if (strcmp(symbol,"CU1")   == 0) kind = CONTROLLED_U1;
  else if (strcmp(symbol,"cu1")   == 0) kind = CONTROLLED_U1;
  else if (strcmp(symbol,"CU2")   == 0) kind = CONTROLLED_U2;
  else if (strcmp(symbol,"cu2")   == 0) kind = CONTROLLED_U2;
  else if (strcmp(symbol,"CU3")   == 0) kind = CONTROLLED_U3;
  else if (strcmp(symbol,"cu3")   == 0) kind = CONTROLLED_U3;
  else if (strcmp(symbol,"SW")    == 0) kind = SWAP;
  else if (strcmp(symbol,"sw")    == 0) kind = SWAP;
  else if (strcmp(symbol,"M")     == 0) kind = MEASURE;
  else if (strcmp(symbol,"m")     == 0) kind = MEASURE;
  else if (strcmp(symbol,"MX")    == 0) kind = MEASURE_X;
  else if (strcmp(symbol,"mx")    == 0) kind = MEASURE_X;
  else if (strcmp(symbol,"MY")    == 0) kind = MEASURE_Y;
  else if (strcmp(symbol,"my")    == 0) kind = MEASURE_Y;
  else if (strcmp(symbol,"MZ")    == 0) kind = MEASURE_Z;
  else if (strcmp(symbol,"mz")    == 0) kind = MEASURE_Z;
  else if (strcmp(symbol,"MB")    == 0) kind = MEASURE_BELL;
  else if (strcmp(symbol,"mb")    == 0) kind = MEASURE_BELL;
  else kind = NOT_A_GATE;

  *kind_out = kind;
  
  SUC_RETURN(true);
}
