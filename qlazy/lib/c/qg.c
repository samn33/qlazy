/*
 *  qg.c
 */

#include "qlazy.h"

bool qg_get_symbol(Kind kind, char* symbol)
{
  switch (kind) {
  case INIT:
    strcpy(symbol, "init");
    break;
  case CIRC:
    strcpy(symbol, "circ");
    break;
  case GATES:
    strcpy(symbol, "gates");
    break;
  case SHOW:
    strcpy(symbol, "show");
    break;
  case BLOCH:
    strcpy(symbol, "bloch");
    break;
  case ECHO:
    strcpy(symbol, "echo");
    break;
  case OUTPUT:
    strcpy(symbol, "output");
    break;
  case HELP:
    strcpy(symbol, "help");
    break;
  case QUIT:
    strcpy(symbol, "quit");
    break;
  case PAULI_X:
    strcpy(symbol, "x");
    break;
  case PAULI_Y:
    strcpy(symbol, "y");
    break;
  case PAULI_Z:
    strcpy(symbol, "z");
    break;
  case ROOT_PAULI_X:
    strcpy(symbol, "xr");
    break;
  case ROOT_PAULI_X_:
    strcpy(symbol, "xr_dg");
    break;
  case HADAMARD:
    strcpy(symbol, "h");
    break;
  case PHASE_SHIFT_S:
    strcpy(symbol, "s");
    break;
  case PHASE_SHIFT_S_:
    strcpy(symbol, "s_dg");
    break;
  case PHASE_SHIFT_T:
    strcpy(symbol, "t");
    break;
  case PHASE_SHIFT_T_:
    strcpy(symbol, "t_dg");
    break;
  case PHASE_SHIFT:
    strcpy(symbol, "p");
    break;
  case ROTATION_X:
    strcpy(symbol, "rx");
    break;
  case ROTATION_Y:
    strcpy(symbol, "ry");
    break;
  case ROTATION_Z:
    strcpy(symbol, "rz");
    break;
  case ROTATION_U1:
    strcpy(symbol, "u1");
    break;
  case ROTATION_U2:
    strcpy(symbol, "u2");
    break;
  case ROTATION_U3:
    strcpy(symbol, "u3");
    break;
  case CONTROLLED_X:
    strcpy(symbol, "cx");
    break;
  case CONTROLLED_Y:
    strcpy(symbol, "cy");
    break;
  case CONTROLLED_Z:
    strcpy(symbol, "cz");
    break;
  case CONTROLLED_XR:
    strcpy(symbol, "cxr");
    break;
  case CONTROLLED_XR_:
    strcpy(symbol, "cxr_dg");
    break;
  case CONTROLLED_H:
    strcpy(symbol, "ch");
    break;
  case CONTROLLED_S:
    strcpy(symbol, "cs");
    break;
  case CONTROLLED_S_:
    strcpy(symbol, "cs_dg");
    break;
  case CONTROLLED_T:
    strcpy(symbol, "ct");
    break;
  case CONTROLLED_T_:
    strcpy(symbol, "ct_dg");
    break;
  case CONTROLLED_P:
    strcpy(symbol,"cp");
    break;
  case CONTROLLED_RX:
    strcpy(symbol, "crx");
    break;
  case CONTROLLED_RY:
    strcpy(symbol, "cry");
    break;
  case CONTROLLED_RZ:
    strcpy(symbol, "crz");
    break;
  case CONTROLLED_U1:
    strcpy(symbol, "cu1");
    break;
  case CONTROLLED_U2:
    strcpy(symbol, "cu2");
    break;
  case CONTROLLED_U3:
    strcpy(symbol, "cu3");
    break;
  case ROTATION_XX:
    strcpy(symbol, "rxx");
    break;
  case ROTATION_YY:
    strcpy(symbol, "ryy");
    break;
  case ROTATION_ZZ:
    strcpy(symbol, "rzz");
    break;
  case SWAP_QUBITS:
    strcpy(symbol, "sw");
    break;
  case MEASURE:
    strcpy(symbol, "m");
    break;
  case MEASURE_X:
    strcpy(symbol, "mx");
    break;
  case MEASURE_Y:
    strcpy(symbol, "my");
    break;
  case MEASURE_Z:
    strcpy(symbol, "mz");
    break;
  case MEASURE_BELL:
    strcpy(symbol, "mb");
    break;
  case RESET:
    strcpy(symbol, ">");
    break;
  default:
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }

  SUC_RETURN(true);
}

bool qg_get_kind(char* symbol, Kind* kind_out)
{
  Kind kind;

  if (strcmp(symbol, "%")          == 0) kind = INIT;
  else if (strcmp(symbol, "init")  == 0) kind = INIT;
  else if (strcmp(symbol, "&")     == 0) kind = CIRC;
  else if (strcmp(symbol, "circ")  == 0) kind = CIRC;
  else if (strcmp(symbol, "!")     == 0) kind = GATES;
  else if (strcmp(symbol, "gates") == 0) kind = GATES;
  else if (strcmp(symbol, "-")     == 0) kind = SHOW;
  else if (strcmp(symbol, "show")  == 0) kind = SHOW;
  else if (strcmp(symbol, "|")     == 0) kind = BLOCH;
  else if (strcmp(symbol, "bloch") == 0) kind = BLOCH;
  else if (strcmp(symbol, "@")     == 0) kind = ECHO;
  else if (strcmp(symbol, "echo")  == 0) kind = ECHO;
  else if (strcmp(symbol, ">")     == 0) kind = OUTPUT;
  else if (strcmp(symbol, "output")== 0) kind = OUTPUT;
  else if (strcmp(symbol, "?")     == 0) kind = HELP;
  else if (strcmp(symbol, "help")  == 0) kind = HELP;
  else if (strcmp(symbol, ".")     == 0) kind = QUIT;
  else if (strcmp(symbol, "quit")  == 0) kind = QUIT;
  else if (strcmp(symbol, "x")     == 0) kind = PAULI_X;
  else if (strcmp(symbol, "y")     == 0) kind = PAULI_Y;
  else if (strcmp(symbol, "z")     == 0) kind = PAULI_Z;
  else if (strcmp(symbol, "xr")    == 0) kind = ROOT_PAULI_X;
  else if (strcmp(symbol, "xr_dg")   == 0) kind = ROOT_PAULI_X_;
  else if (strcmp(symbol, "h")     == 0) kind = HADAMARD; 
  else if (strcmp(symbol, "s")     == 0) kind = PHASE_SHIFT_S; 
  else if (strcmp(symbol, "s_dg")    == 0) kind = PHASE_SHIFT_S_; 
  else if (strcmp(symbol, "t")     == 0) kind = PHASE_SHIFT_T; 
  else if (strcmp(symbol, "t_dg")    == 0) kind = PHASE_SHIFT_T_; 
  else if (strcmp(symbol, "p")     == 0) kind = PHASE_SHIFT; 
  else if (strcmp(symbol, "rx")    == 0) kind = ROTATION_X;
  else if (strcmp(symbol, "ry")    == 0) kind = ROTATION_Y;
  else if (strcmp(symbol, "rz")    == 0) kind = ROTATION_Z;
  else if (strcmp(symbol, "u1")    == 0) kind = ROTATION_U1;
  else if (strcmp(symbol, "u2")    == 0) kind = ROTATION_U2;
  else if (strcmp(symbol, "u3")    == 0) kind = ROTATION_U3;
  else if (strcmp(symbol, "cx")    == 0) kind = CONTROLLED_X;
  else if (strcmp(symbol, "cy")    == 0) kind = CONTROLLED_Y;
  else if (strcmp(symbol, "cz")    == 0) kind = CONTROLLED_Z;
  else if (strcmp(symbol, "cxr")   == 0) kind = CONTROLLED_XR;
  else if (strcmp(symbol, "cxr_dg")  == 0) kind = CONTROLLED_XR_;
  else if (strcmp(symbol, "ch")    == 0) kind = CONTROLLED_H;
  else if (strcmp(symbol, "cs")    == 0) kind = CONTROLLED_S;
  else if (strcmp(symbol, "cs_dg")   == 0) kind = CONTROLLED_S_;
  else if (strcmp(symbol, "ct")    == 0) kind = CONTROLLED_T;
  else if (strcmp(symbol, "ct_dg")   == 0) kind = CONTROLLED_T_;
  else if (strcmp(symbol, "cp")    == 0) kind = CONTROLLED_P;
  else if (strcmp(symbol, "crx")   == 0) kind = CONTROLLED_RX;
  else if (strcmp(symbol, "cry")   == 0) kind = CONTROLLED_RY;
  else if (strcmp(symbol, "crz")   == 0) kind = CONTROLLED_RZ;
  else if (strcmp(symbol, "cu1")   == 0) kind = CONTROLLED_U1;
  else if (strcmp(symbol, "cu2")   == 0) kind = CONTROLLED_U2;
  else if (strcmp(symbol, "cu3")   == 0) kind = CONTROLLED_U3;
  else if (strcmp(symbol, "rxx")   == 0) kind = ROTATION_XX;
  else if (strcmp(symbol, "ryy")   == 0) kind = ROTATION_YY;
  else if (strcmp(symbol, "rzz")   == 0) kind = ROTATION_ZZ;
  else if (strcmp(symbol, "sw")    == 0) kind = SWAP_QUBITS;
  else if (strcmp(symbol, "m")     == 0) kind = MEASURE;
  else if (strcmp(symbol, "mx")    == 0) kind = MEASURE_X;
  else if (strcmp(symbol, "my")    == 0) kind = MEASURE_Y;
  else if (strcmp(symbol, "mz")    == 0) kind = MEASURE_Z;
  else if (strcmp(symbol, "mb")    == 0) kind = MEASURE_BELL;
  else if (strcmp(symbol, "reset") == 0) kind = RESET;
  else kind = NOT_A_GATE;

  *kind_out = kind;
  
  SUC_RETURN(true);
}
