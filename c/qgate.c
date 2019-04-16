/*
 *  qgate.c
 */

#include "qlazy.h"

void qgate_get_symbol(char* symbol, Kind kind)
{
  switch (kind) {
  case INIT:
    strcpy(symbol,"%");
    break;
  case CIRC:
    strcpy(symbol,"&");
    break;
  case GATES:
    strcpy(symbol,"!");
    break;
  case SHOW:
    strcpy(symbol,"-");
    break;
  case ECHO:
    strcpy(symbol,"@");
    break;
  case OUTPUT:
    strcpy(symbol,">");
    break;
  case HELP:
    strcpy(symbol,"?");
    break;
  case QUIT:
    strcpy(symbol,".");
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
  case ROTATION_X:
    strcpy(symbol,"RX");
    break;
  case ROTATION_Y:
    strcpy(symbol,"RY");
    break;
  case ROTATION_Z:
    strcpy(symbol,"RZ");
    break;
  case CONTROLLED_X:
    strcpy(symbol,"CX");
    break;
  case CONTROLLED_Z:
    strcpy(symbol,"CZ");
    break;
  case TOFFOLI:
    strcpy(symbol,"CCX");
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
    break;
  }
}

Kind qgate_get_kind(char* symbol)
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
  else if (strcmp(symbol,"RX")    == 0) kind = ROTATION_X;
  else if (strcmp(symbol,"rx")    == 0) kind = ROTATION_X;
  else if (strcmp(symbol,"RY")    == 0) kind = ROTATION_Y;
  else if (strcmp(symbol,"ry")    == 0) kind = ROTATION_Y;
  else if (strcmp(symbol,"RZ")    == 0) kind = ROTATION_Z;
  else if (strcmp(symbol,"rz")    == 0) kind = ROTATION_Z;
  else if (strcmp(symbol,"CX")    == 0) kind = CONTROLLED_X;
  else if (strcmp(symbol,"cx")    == 0) kind = CONTROLLED_X;
  else if (strcmp(symbol,"CZ")    == 0) kind = CONTROLLED_Z;
  else if (strcmp(symbol,"cz")    == 0) kind = CONTROLLED_Z;
  else if (strcmp(symbol,"CCX")   == 0) kind = TOFFOLI;
  else if (strcmp(symbol,"ccx")   == 0) kind = TOFFOLI;
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

  return kind;
}
