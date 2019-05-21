/*
 *  message.c
 */

#include "qlazy.h"

void warn_msg(WrnCode wrn)
{
  switch (wrn) {
  case NO_WARN:
    break;
  case WARN_NEED_TO_INITIALIZE:
    fprintf(stderr, "Warning: need to initialize !\n");
    break;
  case WARN_UNKNOWN_GATE:
    fprintf(stderr, "Warning: unknown gate !\n");
    break;
  case WARN_OUT_OF_BOUND:
    fprintf(stderr, "Warning: out of bound !\n");
    break;
  case WARN_SAME_QUBIT_ID:
    fprintf(stderr, "Warning: same qubit id are set !\n");
    break;
  case WARN_TOO_MANY_ARGUMENTS:
    fprintf(stderr, "Warning: too many arguments !\n");
    break;
  case WARN_NEED_MORE_ARGUMENTS:
    fprintf(stderr, "Warning: need more arguments !\n");
    break;
  case WARN_CANT_INITIALIZE:
    fprintf(stderr, "Warning: can't initialize !\n");
    break;
  case WARN_CANT_WRITE_FILE:
    fprintf(stderr, "Warning: can't write file !\n");
    break;
  case WARN_CANT_PRINT_QSTATE:
    fprintf(stderr, "Warning: can't print quantum state !\n");
    break;
  case WARN_CANT_PRINT_BLOCH:
    fprintf(stderr, "Warning: can't print bloch angles !\n");
    break;
  case WARN_CANT_PRINT_CIRC:
    fprintf(stderr, "Warning: can't print quantum circit !\n");
    break;
  case WARN_CANT_PRINT_GATES:
    fprintf(stderr, "Warning: can't print quantum gates !\n");
    break;
  case WARN_CANT_PRINT_HELP:
    fprintf(stderr, "Warning: can't print help (item is not exist) !\n");
    break;
  default:
    fprintf(stderr, "Warning: unidentified warning occur (unknown warn code) !\n");
    break;
  }
}

void error_msg(ErrCode err)
{
  switch (err) {
  case NO_ERROR:
    fprintf(stderr, "No Error, OK!\n");
    break;
  case INVALID_ARGUMENT:
    fprintf(stderr, "ERROR:invalid argument !\n");
    break;
  case CANT_ALLOC_MEMORY:
    fprintf(stderr, "ERROR:can't alloc memory !\n");
    break;
  case OUT_OF_QUBIT_NUM:
    fprintf(stderr, "ERROR:out of qubit number !\n");
    break;
  case ERROR_QGATE_PRINT:
    fprintf(stderr, "ERROR:qgate print failure !\n");
    break;
  case ERROR_QCIRC_INIT:
    fprintf(stderr, "ERROR:qcirc init failure !\n");
    break;
  case ERROR_QCIRC_APPEND_QGATE:
    fprintf(stderr, "ERROR:qcirc append qgate failure !\n");
    break;
  case ERROR_QCIRC_READ_FILE:
    fprintf(stderr, "ERROR:qcirc read file failure !\n");
    break;
  case ERROR_QCIRC_WRITE_FILE:
    fprintf(stderr, "ERROR:qcirc write file failure !\n");
    break;
  case ERROR_QCIRC_PRINT_QCIRC:
    fprintf(stderr, "ERROR:qcirc print qcirc failure !\n");
    break;
  case ERROR_QCIRC_PRINT_QGATES:
    fprintf(stderr, "ERROR:qcirc print qgates failure !\n");
    break;
  case ERROR_QSTATE_INIT:
    fprintf(stderr, "ERROR:qstate init failure !\n");
    break;
  case ERROR_QSTATE_COPY:
    fprintf(stderr, "ERROR:qstate copy failure !\n");
    break;
  case ERROR_QSTATE_GET_CAMP:
    fprintf(stderr, "ERROR:qstate get camp failure !\n");
    break;
  case ERROR_QSTATE_PRINT:
    fprintf(stderr, "ERROR:qstate print failure !\n");
    break;
  case ERROR_QSTATE_MEASURE:
    fprintf(stderr, "ERROR:qstate measure failure !\n");
    break;
  case ERROR_QSTATE_OPERATE:
    fprintf(stderr, "ERROR:qstate operate failure !\n");
    break;
  case ERROR_QSTATE_OPERATE_QGATE:
    fprintf(stderr, "ERROR:qstate operate qgate failure !\n");
    break;
  case ERROR_QSTATE_EVOLVE:
    fprintf(stderr, "ERROR:qstate evalve failure !\n");
    break;
  case ERROR_QSTATE_INNER_PRODUCT:
    fprintf(stderr, "ERROR:inner product failure !\n");
    break;
  case ERROR_QSTATE_EXPECT_VALUE:
    fprintf(stderr, "ERROR:expect value failure !\n");
    break;
  case ERROR_QSTATE_BLOCH:
    fprintf(stderr, "ERROR:bloch failure !\n");
    break;
  case ERROR_QSTATE_PRINT_BLOCH:
    fprintf(stderr, "ERROR:bloch print failure !\n");
    break;
  case ERROR_MDATA_INIT:
    fprintf(stderr, "ERROR:mdata init failure !\n");
    break;
  case ERROR_MDATA_PRINT:
    fprintf(stderr, "ERROR:mdata print failure !\n");
    break;
  case ERROR_GBANK_INIT:
    fprintf(stderr, "ERROR:gbank init failure !\n");
    break;
  case ERROR_GBANK_GET:
    fprintf(stderr, "ERROR:gbank get failure !\n");
    break;
  case ERROR_CIMAGE_INIT:
    fprintf(stderr, "ERROR:cimage init failure !\n");
    break;
  case ERROR_LINE_OPERATE:
    fprintf(stderr, "ERROR:line operate failure !\n");
    break;
  case ERROR_QSYSTEM_EXECUTE:
    fprintf(stderr, "ERROR:qsystem execute failure !\n");
    break;
  case ERROR_QSYSTEM_INTMODE:
    fprintf(stderr, "ERROR:qsystem intmode failure !\n");
    break;
  case ERROR_SPRO_INIT:
    fprintf(stderr, "ERROR:spro init failure !\n");
    break;
  case ERROR_OBSERVABLE_INIT:
    fprintf(stderr, "ERROR:observ init failure !\n");
    break;
  case ERROR_HELP_PRINT_MESSAGE:
    fprintf(stderr, "ERROR:help print message failure !\n");
    break;
  default:
    fprintf(stderr, "ERROR:unidentified error occur (unknown error code) !\n");
    break;
  }
}
