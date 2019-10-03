/*
 *  message.c
 */

#include "qlazy.h"

void error_msg(ErrCode err)
{
  switch (err) {
  case SUCCESS:
    fprintf(stderr, "No Error, OK!\n");
    break;
  case ERROR_INVALID_ARGUMENT:
    fprintf(stderr, "ERROR: invalid argument !\n");
    break;
  case ERROR_CANT_ALLOC_MEMORY:
    fprintf(stderr, "ERROR: can't alloc memory !\n");
    break;
  case ERROR_CANT_OPEN_FILE:
    fprintf(stderr, "ERROR: can't open file !\n");
    break;
  case ERROR_CANT_READ_LINE:
    fprintf(stderr, "ERROR: can't read line (syntax error?) !\n");
    break;

  case ERROR_HELP_PRINT:
    fprintf(stderr, "ERROR: help print failure !\n");
    break;

  case ERROR_QGATE_GET_SYMBOL:
    fprintf(stderr, "ERROR: qgate get symbol failure !\n");
    break;
  case ERROR_QGATE_GET_KIND:
    fprintf(stderr, "ERROR: qgate get kind failure !\n");
    break;

  case ERROR_QCIRC_INIT:
    fprintf(stderr, "ERROR: qcirc init failure !\n");
    break;
  case ERROR_QCIRC_APPEND_QGATE:
    fprintf(stderr, "ERROR: qcirc append qgate failure !\n");
    break;
  case ERROR_QCIRC_SET_CIMAGE:
    fprintf(stderr, "ERROR: qcirc set cimage failure !\n");
    break;
  case ERROR_QCIRC_PRINT_QCIRC:
    fprintf(stderr, "ERROR: qcirc print qcirc failure !\n");
    break;
  case ERROR_QCIRC_PRINT_QGATES:
    fprintf(stderr, "ERROR: qcirc print qgates failure !\n");
    break;
  case ERROR_QCIRC_READ_FILE:
    fprintf(stderr, "ERROR: qcirc read file failure !\n");
    break;
  case ERROR_QCIRC_WRITE_FILE:
    fprintf(stderr, "ERROR: qcirc write file failure !\n");
    break;

  case ERROR_GBANK_INIT:
    fprintf(stderr, "ERROR: gbank init failure !\n");
    break;

  case ERROR_GBANK_GET_UNITARY:
    fprintf(stderr, "ERROR: gbank get unitary failure !\n");
    break;

  case ERROR_QSTATE_INIT:
    fprintf(stderr, "ERROR: qstate init failure !\n");
    break;
  case ERROR_QSTATE_COPY:
    fprintf(stderr, "ERROR: qstate copy failure !\n");
    break;
  case ERROR_QSTATE_GET_CAMP:
    fprintf(stderr, "ERROR: qstate get camp failure !\n");
    break;
  case ERROR_QSTATE_PRINT:
    fprintf(stderr, "ERROR: qstate print failure !\n");
    break;
  case ERROR_QSTATE_BLOCH:
    fprintf(stderr, "ERROR: qstate bloch failure !\n");
    break;
  case ERROR_QSTATE_PRINT_BLOCH:
    fprintf(stderr, "ERROR: qstate bloch print failure !\n");
    break;
  case ERROR_QSTATE_MEASURE:
    fprintf(stderr, "ERROR: qstate measure failure !\n");
    break;
  case ERROR_QSTATE_MEASURE_BELL:
    fprintf(stderr, "ERROR: qstate measure bell failure !\n");
    break;
  case ERROR_QSTATE_OPERATE_QGATE:
    fprintf(stderr, "ERROR: qstate operate qgate failure !\n");
    break;
  case ERROR_QSTATE_EVOLVE:
    fprintf(stderr, "ERROR: qstate evolve failure !\n");
    break;
  case ERROR_QSTATE_INNER_PRODUCT:
    fprintf(stderr, "ERROR: inner product failure !\n");
    break;
  case ERROR_QSTATE_EXPECT_VALUE:
    fprintf(stderr, "ERROR: expect value failure !\n");
    break;
  case ERROR_QSTATE_APPLY_MATRIX:
    fprintf(stderr, "ERROR: apply matrix failure !\n");
    break;

  case ERROR_MDATA_INIT:
    fprintf(stderr, "ERROR: mdata init failure !\n");
    break;
  case ERROR_MDATA_PRINT:
    fprintf(stderr, "ERROR: mdata print failure !\n");
    break;
  case ERROR_MDATA_PRINT_BELL:
    fprintf(stderr, "ERROR: mdata print bell failure !\n");
    break;

  case ERROR_QSYSTEM_INIT:
    fprintf(stderr, "ERROR: qsystem init failure !\n");
    break;
  case ERROR_QSYSTEM_EXECUTE:
    fprintf(stderr, "ERROR: qsystem execute failure !\n");
    break;
  case ERROR_QSYSTEM_INTMODE:
    fprintf(stderr, "ERROR: qsystem intmode failure !\n");
    break;

  case ERROR_SPRO_INIT:
    fprintf(stderr, "ERROR: spro init failure !\n");
    break;

  case ERROR_OBSERVABLE_INIT:
    fprintf(stderr, "ERROR: observable init failure !\n");
    break;

  case ERROR_DENSOP_INIT:
    fprintf(stderr, "ERROR: densop init failure !\n");
    break;
  case ERROR_DENSOP_COPY:
    fprintf(stderr, "ERROR: densop copy failure !\n");
    break;
  case ERROR_DENSOP_GET_ELM:
    fprintf(stderr, "ERROR: densop get_elm failure !\n");
    break;
  case ERROR_DENSOP_PRINT:
    fprintf(stderr, "ERROR: densop print failure !\n");
    break;
  case ERROR_DENSOP_ADD:
    fprintf(stderr, "ERROR: densop add failure !\n");
    break;
  case ERROR_DENSOP_MUL:
    fprintf(stderr, "ERROR: densop mul failure !\n");
    break;
  case ERROR_DENSOP_TRACE:
    fprintf(stderr, "ERROR: densop trace failure !\n");
    break;
  case ERROR_DENSOP_SQTRACE:
    fprintf(stderr, "ERROR: densop sqtrace failure !\n");
    break;
  case ERROR_DENSOP_PATRACE:
    fprintf(stderr, "ERROR: densop patrace failure !\n");
    break;
  case ERROR_DENSOP_APPLY_MATRIX:
    fprintf(stderr, "ERROR: densop aplly_matrix failure !\n");
    break;
  case ERROR_DENSOP_PROBABILITY:
    fprintf(stderr, "ERROR: densop probability failure !\n");
    break;

  case ERROR_NEED_TO_INITIALIZE:
    fprintf(stderr, "ERROR: need to initialize !\n");
    break;
  case ERROR_UNKNOWN_GATE:
    fprintf(stderr, "ERROR: unknown gate !\n");
    break;
  case ERROR_OUT_OF_BOUND:
    fprintf(stderr, "ERROR: out of bound !\n");
    break;
  case ERROR_SAME_QUBIT_ID:
    fprintf(stderr, "ERROR: same qubit id are set !\n");
    break;
  case ERROR_TOO_MANY_ARGUMENTS:
    fprintf(stderr, "ERROR: too many arguments !\n");
    break;
  case ERROR_NEED_MORE_ARGUMENTS:
    fprintf(stderr, "ERROR: need more arguments !\n");
    break;
  case ERROR_CANT_INITIALIZE:
    fprintf(stderr, "ERROR: can't initialize !\n");
    break;
  case ERROR_CANT_WRITE_FILE:
    fprintf(stderr, "ERROR: can't write file !\n");
    break;
  case ERROR_CANT_PRINT_QSTATE:
    fprintf(stderr, "ERROR: can't print quantum state !\n");
    break;
  case ERROR_CANT_PRINT_BLOCH:
    fprintf(stderr, "ERROR: can't print bloch angles !\n");
    break;
  case ERROR_CANT_PRINT_CIRC:
    fprintf(stderr, "ERROR: can't print quantum circit !\n");
    break;
  case ERROR_CANT_PRINT_GATES:
    fprintf(stderr, "ERROR: can't print quantum gates !\n");
    break;
  case ERROR_CANT_PRINT_HELP:
    fprintf(stderr, "ERROR: can't print help (item is not exist) !\n");
    break;
    
  default:
    fprintf(stderr, "ERROR:unidentified error occur (unknown error code) !\n");
    break;
  }
}
