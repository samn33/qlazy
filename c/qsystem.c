/*
 *  qsystem.c
 */

#include "qlazy.h"

bool qsystem_init(void** qsystem_out)
{
  QSystem* qsystem = NULL;

  if (!(qsystem = (QSystem*)malloc(sizeof(QSystem))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  qsystem->qcirc = NULL;
  qsystem->qstate = NULL;
  qsystem->qubit_num = 0;

  *qsystem_out = qsystem;
  
  SUC_RETURN(true);
}

static bool _qsystem_execute_one_line(QSystem* qsystem, char* line)
{
  char*		token[TOKEN_NUM];
  char*		args[TOKEN_NUM];
  char		comment[LINE_STRLEN];
  int           tnum,anum;
  Kind		kind;
  Para          para;
  int           terminal_num = 0;
  int           qubit_id[MAX_QUBIT_NUM];
  QGate*        qgate	     = NULL;
  QCirc*	qcirc	     = qsystem->qcirc;
  QState*       qstate	     = qsystem->qstate;
  int		qubit_num    = qsystem->qubit_num;

  if (!line_check_length(line)) ERR_RETURN(ERROR_CANT_READ_LINE,false);
  if (!line_chomp(line)) ERR_RETURN(ERROR_CANT_READ_LINE,false);

  if ((line_is_blank(line) == true) ||
      (line_is_comment(line) == true)) SUC_RETURN(true);

  if (!line_split(line, " ", token, &tnum)) ERR_RETURN(ERROR_CANT_READ_LINE,false);
  if (!line_getargs(token[0], args, &anum)) ERR_RETURN(ERROR_CANT_READ_LINE,false);

  qgate_get_kind(args[0], &kind);

  /* operate command */
  
  switch (kind) {
  case SHOW:
    /* print quantum state */
    if (tnum > qubit_num + 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    terminal_num = tnum - 1;  /* number of qubits to measure */
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if ((qcirc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE,false);
    for (int i=0; i<terminal_num; i++) {
      qubit_id[i] = strtol(token[1+i], NULL, 10);
      if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
      if (qubit_id[i] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    }
    if (terminal_num == 0) {  /* show all qubits in order */
      terminal_num = qubit_num;
      for (int i=0; i<terminal_num; i++) {
	qubit_id[i] = i;
      }
    }
    if (!(qstate_print(qstate, terminal_num, qubit_id)))
      ERR_RETURN(ERROR_CANT_PRINT_QSTATE,false);
    SUC_RETURN(true);
  case BLOCH:
    /* print bloch sphere (theta,phi) */
    if (tnum > 2) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    else if (tnum == 2) {
      qubit_id[0] = strtol(token[1], NULL, 10);
    }
    else if (tnum == 1) {
      qubit_id[0] = 0;
    }
    if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (!(qstate_print_bloch(qstate, qubit_id[0])))
      ERR_RETURN(ERROR_CANT_PRINT_BLOCH,false);
    SUC_RETURN(true);
  case CIRC:
    /* print quantum circuit */
    if (tnum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if ((qcirc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE,false);
    if (!(qcirc_set_cimage(qcirc))) ERR_RETURN(ERROR_CANT_INITIALIZE,false); 
    if (!(qcirc_print_qcirc(qcirc))) ERR_RETURN(ERROR_CANT_PRINT_CIRC,false);
    SUC_RETURN(true);
  case GATES:
    /* print quantum gates */
    if (tnum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if ((qcirc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE,false);
    if (!(qcirc_print_qgates(qcirc))) ERR_RETURN(ERROR_CANT_PRINT_GATES,false);
    SUC_RETURN(true);
  case ECHO:
    /* echo string */
    line_join_token(comment, token, 1, tnum);
    printf("%s\n", comment);
    SUC_RETURN(true);
  case OUTPUT:
    /* output file */
    if (tnum > 2) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if (tnum < 2) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS,false);
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if ((qcirc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE,false);
    if (!(qcirc_write_file(qcirc, token[1]))) ERR_RETURN(ERROR_CANT_WRITE_FILE,false);
    printf("output file : %s\n", token[1]);
    SUC_RETURN(true);
  case HELP:
    /* print help message */
    if (tnum > 2) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if (tnum == 1) {
      if (!(help_print(NULL))) ERR_RETURN(ERROR_CANT_PRINT_HELP,false);
    }
    else {
      if (!(help_print(token[1]))) ERR_RETURN(ERROR_CANT_PRINT_HELP,false);
    }
    SUC_RETURN(true);
  case QUIT:
    /* quit system */
    if (tnum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if (line != NULL) { free(line); line = NULL; }
    qsystem_free(qsystem); qsystem = NULL;
    exit(0);
  default:
    break;
  }

  /* operate quantum gate */

  switch (kind) {
  case INIT:
    /* initialize quantum state (or reset quantum state) */
    if (tnum > 2) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if (tnum < 2) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS,false);
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    qubit_num = strtol(token[1], NULL, 10);
    if ((qubit_num < 0) || (qubit_num > MAX_QUBIT_NUM))
      ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qstate != NULL) { qstate_free(qstate); qstate = NULL; }
    if (qcirc != NULL) { qcirc_free(qcirc); qcirc = NULL; }
    if (!(qcirc_init(qubit_num, DEF_QCIRC_STEPS, (void**)&qcirc)))
      ERR_RETURN(ERROR_CANT_INITIALIZE,false);
    if (!(qstate_init(qubit_num, (void**)&qstate)))
      ERR_RETURN(ERROR_CANT_INITIALIZE,false);
    break;
  case MEASURE:
    /* measurement */
    if ((qcirc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE,false);
    if (tnum > qubit_num + 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    terminal_num = tnum - 1;  /* number of qubits to measure */
    if (anum == 1) {
      para.mes.shots = DEF_SHOTS;
      para.mes.angle = 0.0;
      para.mes.phase = 0.0;
    }
    else if (anum == 2) {
      para.mes.shots = strtol(args[1], NULL, 10);
      para.mes.angle = 0.0;
      para.mes.phase = 0.0;
    }
    else if (anum == 3) {
      para.mes.shots = strtol(args[1], NULL, 10);
      para.mes.angle = strtod(args[2], NULL);
      para.mes.phase = 0.0;
    }
    else if (anum == 4) {
      para.mes.shots = strtol(args[1], NULL, 10);
      para.mes.angle = strtod(args[2], NULL);
      para.mes.phase = strtod(args[3], NULL);
    }
    else ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    for (int i=0; i<terminal_num; i++) {
      qubit_id[i] = strtol(token[1+i], NULL, 10);
      if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
      if (qubit_id[i] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    }
    if (terminal_num == 0) {  /* measure all qubits in order */
      terminal_num = qubit_num;
      for (int i=0; i<terminal_num; i++) {
	qubit_id[i] = i;
      }
    }
    break;
  case MEASURE_X:
  case MEASURE_Y:
  case MEASURE_Z:
    /* measurement */
    if ((qcirc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE,false);
    if (tnum > qubit_num + 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    terminal_num = tnum - 1;  /* number of qubits to measure */
    if (anum == 1) {
      para.mes.shots = DEF_SHOTS;
    }
    else if (anum == 2) {
      para.mes.shots = strtol(args[1], NULL, 10);
    }
    else ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if (kind == MEASURE_X) {
      para.mes.angle = 0.5;
      para.mes.phase = 0.0;
    }
    else if (kind == MEASURE_Y) {
      para.mes.angle = 0.5;
      para.mes.phase = 0.5;
    }
    else if (kind == MEASURE_Z) {
      para.mes.angle = 0.0;
      para.mes.phase = 0.0;
    }
    else ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

    for (int i=0; i<terminal_num; i++) {
      qubit_id[i] = strtol(token[1+i], NULL, 10);
      if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
      if (qubit_id[i] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    }
    if (terminal_num == 0) {  /* measure all qubits in order */
      terminal_num = qubit_num;
      for (int i=0; i<terminal_num; i++) {
	qubit_id[i] = i;
      }
    }
    break;
  case MEASURE_BELL:
    /* measurement */
    if ((qcirc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE,false);
    if (tnum < 3) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS,false);
    if (tnum > 3) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    terminal_num = 2;  /* number of qubits to measure */
    if (anum == 1) {
      para.mes.shots = DEF_SHOTS;
    }
    else if (anum == 2) {
      para.mes.shots = strtol(args[1], NULL, 10);
    }
    else ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    for (int i=0; i<terminal_num; i++) {
      qubit_id[i] = strtol(token[1+i], NULL, 10);
      if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
      if (qubit_id[i] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    }
    break;
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
    if ((qcirc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE,false);
    if (tnum > 2) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if (tnum < 2) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS,false);
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    terminal_num = 1;
    qubit_id[0] = strtol(token[1], NULL, 10);
    if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    break;
  case ROTATION_X:
  case ROTATION_Y:
  case ROTATION_Z:
  case PHASE_SHIFT:
    /* 1-qubit 1-parameter gate */
    if ((qcirc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE,false);
    if (tnum > 2) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if (tnum < 2) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS,false);
    terminal_num = 1;
    if (anum == 1) {
      para.phase = DEF_PHASE;
    }
    else if (anum == 2) {
      para.phase = strtod(args[1], NULL);
    }
    else ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    qubit_id[0] = strtol(token[1], NULL, 10);
    if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    break;
  case CONTROLLED_X:
  case CONTROLLED_Y:
  case CONTROLLED_Z:
  case CONTROLLED_H:
    /* 2-qubit gate */
    if ((qcirc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE,false);
    if (tnum > 3) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if (tnum < 3) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS,false);

    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    terminal_num = 2;
    qubit_id[0] = strtol(token[1], NULL, 10);
    qubit_id[1] = strtol(token[2], NULL, 10);
    if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_num < qubit_id[1] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_id[1] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_id[0] == qubit_id[1]) ERR_RETURN(ERROR_SAME_QUBIT_ID,false);
    break;
  case CONTROLLED_P:
  case CONTROLLED_RX:
  case CONTROLLED_RY:
  case CONTROLLED_RZ:
    /* 2-qubit, 1-parameter gate */
    if ((qcirc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE,false);
    if (tnum > 3) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if (tnum < 3) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS,false);
    terminal_num = 2;
    if (anum == 1) {
      para.phase = DEF_PHASE;
    }
    else if (anum == 2) {
      para.phase = strtod(args[1], NULL);
    }
    else ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    qubit_id[0] = strtol(token[1], NULL, 10);
    qubit_id[1] = strtol(token[2], NULL, 10);
    if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_num < qubit_id[1] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_id[1] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_id[0] == qubit_id[1]) ERR_RETURN(ERROR_SAME_QUBIT_ID,false);
    break;
  case TOFFOLI:
    /* 3-qubit gate */
    if ((qcirc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE,false);
    if (tnum > 4) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if (tnum < 4) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS,false);
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    terminal_num = 3;
    qubit_id[0] = strtol(token[1], NULL, 10);
    qubit_id[1] = strtol(token[2], NULL, 10);
    qubit_id[2] = strtol(token[3], NULL, 10);
    if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_num < qubit_id[1] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_num < qubit_id[2] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_id[1] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_id[2] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qubit_id[0] == qubit_id[1]) ERR_RETURN(ERROR_SAME_QUBIT_ID,false);
    if (qubit_id[1] == qubit_id[2]) ERR_RETURN(ERROR_SAME_QUBIT_ID,false);
    if (qubit_id[2] == qubit_id[0]) ERR_RETURN(ERROR_SAME_QUBIT_ID,false);
    break;
  default:
    ERR_RETURN(ERROR_UNKNOWN_GATE,false);
  }

  if (!(qcirc_append_qgate(qcirc, kind, terminal_num, &para, qubit_id))) /* set para */
    ERR_RETURN(ERROR_QCIRC_APPEND_QGATE,false);

  qgate = &(qcirc->qgate[qcirc->step_num - 1]);
  if (!(qstate_operate_qgate(qstate, qgate)))
    ERR_RETURN(ERROR_QSTATE_OPERATE_QGATE,false);

  qsystem->qcirc = qcirc;
  qsystem->qstate = qstate;
  qsystem->qubit_num = qubit_num;

  SUC_RETURN(true);
}

bool qsystem_execute(QSystem* qsystem, char* fname)
{
  FILE*         fp = NULL;
  char*		line;

  /* file open */

  if (fname != NULL) {
    if (!(fp = fopen(fname,"r"))) SUC_RETURN(true);
  }
  else ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  if (!(line = (char*)malloc(sizeof(char)*LINE_STRLEN)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  /* read lines and execute */

  while (fgets(line, LINE_STRLEN, fp) != NULL) {
    if (!(_qsystem_execute_one_line(qsystem, line))) {
#ifndef DEV
      error_msg(g_Errno);
#endif
      ERR_RETURN(ERROR_CANT_READ_LINE,false);
    }
  }

  free(line); line = NULL;
  fclose(fp);

  SUC_RETURN(true);
}

bool qsystem_intmode(QSystem* qsystem, char* fname_ini)
{
  char*		line	     = NULL;

  if (qsystem == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (fname_ini != NULL) {
    if (!(qsystem_execute(qsystem, fname_ini))) {
      ERR_RETURN(ERROR_QSYSTEM_EXECUTE,false);
#ifndef DEV
      error_msg(g_Errno);
#endif
    }
  }

  while (1) {
    line = readline(">> ");
    add_history(line);
    _qsystem_execute_one_line(qsystem, line);
#ifndef DEV
    if (g_Errno != SUCCESS) error_msg(g_Errno);
#endif
  }

  free(line); line = NULL;

  SUC_RETURN(true);
}

void qsystem_free(QSystem* qsystem)
{
  if (qsystem != NULL) {
    if (qsystem->qcirc != NULL) {
      qcirc_free(qsystem->qcirc); qsystem->qcirc = NULL;
    }
    if (qsystem->qstate != NULL) {
      qstate_free(qsystem->qstate); qsystem->qstate = NULL;
    }
    free(qsystem);
  }
}
