/*
 *  qsystem.c
 */

#include "qlazy.h"

QSystem* qsystem_init()
{
  QSystem* qsystem = NULL;
  if (!(qsystem = (QSystem*)malloc(sizeof(QSystem)))) return NULL;
  qsystem->qcirc = NULL;
  qsystem->qstate = NULL;
  qsystem->qubit_num = 0;
  return qsystem;
}

static int qsystem_execute_one_line(QSystem* qsystem, char* line)
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

  g_Wrnno = NO_WARN;
  
  if (line_check_length(line) == FALSE) goto ERROR_EXIT;

  line_chomp(line);

  if ((line_is_blank(line) == TRUE) ||
      (line_is_comment(line) == TRUE)) return TRUE;;

  tnum = line_split(line, " ", token);
  anum = line_getargs(token[0], args);

  kind = qgate_get_kind(args[0]);

  /* operate command */
  
  switch (kind) {
  case SHOW:
    /* print quantum state */
    if (tnum > qubit_num + 1) goto TOO_MANY_ARGUMENTS;
    terminal_num = tnum - 1;  /* number of qubits to measure */
    if (anum > 1) goto TOO_MANY_ARGUMENTS;
    if ((qcirc == NULL) || (qstate == NULL)) goto NEED_TO_INITIALIZE;
    for (int i=0; i<terminal_num; i++) {
      qubit_id[i] = strtol(token[1+i], NULL, 10);
      if (qubit_num < qubit_id[i] + 1) goto OUT_OF_BOUND;
    }
    if (terminal_num == 0) {  /* show all qubits in order */
      terminal_num = qubit_num;
      for (int i=0; i<terminal_num; i++) {
	qubit_id[i] = i;
      }
    }
    qstate_print(qstate, terminal_num, qubit_id);
    return TRUE;
  case CIRC:
    /* print quantum circuit */
    if (tnum > 1) goto TOO_MANY_ARGUMENTS;
    if (anum > 1) goto TOO_MANY_ARGUMENTS;
    if ((qcirc == NULL) || (qstate == NULL)) goto NEED_TO_INITIALIZE;
    if (qcirc_set_cimage(qcirc) == FALSE) goto CANT_INITIALIZE; 
    if (qcirc_print_qcirc(qcirc) == FALSE) goto CANT_PRINT_CIRC;
    return TRUE;
  case GATES:
    /* print quantum gates */
    if (tnum > 1) goto TOO_MANY_ARGUMENTS;
    if (anum > 1) goto TOO_MANY_ARGUMENTS;
    if ((qcirc == NULL) || (qstate == NULL)) goto NEED_TO_INITIALIZE;
    if (qcirc_print_qgates(qcirc) == FALSE) goto CANT_PRINT_GATES;
    return TRUE;
  case ECHO:
    /* echo string */
    line_join_token(comment, token, 1, tnum);
    printf("%s\n", comment);
    return TRUE;
  case OUTPUT:
    /* output file */
    if (tnum > 2) goto TOO_MANY_ARGUMENTS;
    if (tnum < 2) goto NEED_MORE_ARGUMENTS;
    if (anum > 1) goto TOO_MANY_ARGUMENTS;
    if ((qcirc == NULL) || (qstate == NULL)) goto NEED_TO_INITIALIZE;
     if (qcirc_write_file(qcirc, token[1]) == FALSE) goto CANT_WRITE_FILE;
    printf("output file : %s\n", token[1]);
    return TRUE;
  case HELP:
    /* print help message */
    if (tnum > 2) goto TOO_MANY_ARGUMENTS;
    if (anum > 1) goto TOO_MANY_ARGUMENTS;
    if (tnum == 1) {
      if (help_print(NULL) == FALSE) goto CANT_PRINT_HELP;
    }
    else {
       if (help_print(token[1]) == FALSE) goto CANT_PRINT_HELP;
    }
    return TRUE;
  case QUIT:
    /* quit system */
    if (tnum > 1) goto TOO_MANY_ARGUMENTS;
    if (anum > 1) goto TOO_MANY_ARGUMENTS;
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
    if (tnum > 2) goto TOO_MANY_ARGUMENTS;
    if (tnum < 2) goto NEED_MORE_ARGUMENTS;
    if (anum > 1) goto TOO_MANY_ARGUMENTS;
    qubit_num = strtol(token[1], NULL, 10);
    if (qstate != NULL) { qstate_free(qstate); qstate = NULL; }
    if (qcirc != NULL) { qcirc_free(qcirc); qcirc = NULL; }
    if (!(qcirc = qcirc_init(qubit_num, DEF_QCIRC_STEPS))) goto CANT_INITIALIZE;
    if (!(qstate = qstate_init(qubit_num))) goto CANT_INITIALIZE;
    break;
  case MEASURE:
    /* measurement */
    if ((qcirc == NULL) || (qstate == NULL)) goto NEED_TO_INITIALIZE;
    if (tnum > qubit_num + 1) goto TOO_MANY_ARGUMENTS;
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
    else goto ERROR_EXIT;
    for (int i=0; i<terminal_num; i++) {
      qubit_id[i] = strtol(token[1+i], NULL, 10);
      if (qubit_num < qubit_id[i] + 1) goto OUT_OF_BOUND;
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
    if ((qcirc == NULL) || (qstate == NULL)) goto NEED_TO_INITIALIZE;
    if (tnum > qubit_num + 1) goto TOO_MANY_ARGUMENTS;
    terminal_num = tnum - 1;  /* number of qubits to measure */
    if (anum == 1) {
      para.mes.shots = DEF_SHOTS;
    }
    else if (anum == 2) {
      para.mes.shots = strtol(args[1], NULL, 10);
    }
    else goto ERROR_EXIT;

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
    else goto ERROR_EXIT;

    for (int i=0; i<terminal_num; i++) {
      qubit_id[i] = strtol(token[1+i], NULL, 10);
      if (qubit_num < qubit_id[i] + 1) goto OUT_OF_BOUND;
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
    if ((qcirc == NULL) || (qstate == NULL)) goto NEED_TO_INITIALIZE;
    if (tnum < 3) goto NEED_MORE_ARGUMENTS;
    if (tnum > 3) goto TOO_MANY_ARGUMENTS;
    terminal_num = 2;  /* number of qubits to measure */
    if (anum == 1) {
      para.mes.shots = DEF_SHOTS;
    }
    else if (anum == 2) {
      para.mes.shots = strtol(args[1], NULL, 10);
    }
    else goto ERROR_EXIT;
    for (int i=0; i<terminal_num; i++) {
      qubit_id[i] = strtol(token[1+i], NULL, 10);
      if (qubit_num < qubit_id[i] + 1) goto OUT_OF_BOUND;
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
    if ((qcirc == NULL) || (qstate == NULL)) goto NEED_TO_INITIALIZE;
    if (tnum > 2) goto TOO_MANY_ARGUMENTS;
    if (tnum < 2) goto NEED_MORE_ARGUMENTS;
    if (anum > 1) goto TOO_MANY_ARGUMENTS;
    terminal_num = 1;
    qubit_id[0] = strtol(token[1], NULL, 10);
    if (qubit_num < qubit_id[0] + 1) goto OUT_OF_BOUND;
    break;
  case ROTATION_X:
  case ROTATION_Y:
  case ROTATION_Z:
    /* 1-qubit 1-parameter gate */
    if ((qcirc == NULL) || (qstate == NULL)) goto NEED_TO_INITIALIZE;
    if (tnum > 2) goto TOO_MANY_ARGUMENTS;
    if (tnum < 2) goto NEED_MORE_ARGUMENTS;
    terminal_num = 1;
    if (anum == 1) {
      para.phase = DEF_PHASE;
    }
    else if (anum == 2) {
      para.phase = strtod(args[1], NULL);
    }
    else goto ERROR_EXIT;
    qubit_id[0] = strtol(token[1], NULL, 10);
    if (qubit_num < qubit_id[0] + 1) goto OUT_OF_BOUND;
    break;
  case CONTROLLED_X:
  case CONTROLLED_Z:
    /* 2-qubit gate */
    if ((qcirc == NULL) || (qstate == NULL)) goto NEED_TO_INITIALIZE;
    if (tnum > 3) goto TOO_MANY_ARGUMENTS;
    if (tnum < 3) goto NEED_MORE_ARGUMENTS;
    if (anum > 1) goto TOO_MANY_ARGUMENTS;
    terminal_num = 2;
    qubit_id[0] = strtol(token[1], NULL, 10);
    qubit_id[1] = strtol(token[2], NULL, 10);
    if (qubit_num < qubit_id[0] + 1) goto OUT_OF_BOUND;
    if (qubit_num < qubit_id[1] + 1) goto OUT_OF_BOUND;
    if (qubit_id[0] == qubit_id[1]) goto SAME_QUBIT_ID;
    break;
  case TOFFOLI:
    /* 3-qubit gate */
    if ((qcirc == NULL) || (qstate == NULL)) goto NEED_TO_INITIALIZE;
    if (tnum > 4) goto TOO_MANY_ARGUMENTS;
    if (tnum < 4) goto NEED_MORE_ARGUMENTS;
    if (anum > 1) goto TOO_MANY_ARGUMENTS;
    terminal_num = 3;
    qubit_id[0] = strtol(token[1], NULL, 10);
    qubit_id[1] = strtol(token[2], NULL, 10);
    qubit_id[2] = strtol(token[3], NULL, 10);
    if (qubit_num < qubit_id[0] + 1) goto OUT_OF_BOUND;
    if (qubit_num < qubit_id[1] + 1) goto OUT_OF_BOUND;
    if (qubit_num < qubit_id[2] + 1) goto OUT_OF_BOUND;
    if (qubit_id[0] == qubit_id[1]) goto SAME_QUBIT_ID;
    if (qubit_id[1] == qubit_id[2]) goto SAME_QUBIT_ID;
    if (qubit_id[2] == qubit_id[0]) goto SAME_QUBIT_ID;
    break;
  default:
    goto UNKNOWN_GATE;
  }

  if (qcirc_append_qgate(qcirc, kind, terminal_num, &para, qubit_id) == FALSE)
    goto ERROR_EXIT;

  qgate = &(qcirc->qgate[qcirc->step_num - 1]);
  if (qstate_operate_qgate(qstate, qgate) == FALSE)
    goto ERROR_EXIT;

  qsystem->qcirc = qcirc;
  qsystem->qstate = qstate;
  qsystem->qubit_num = qubit_num;

  return TRUE;
  
 NEED_TO_INITIALIZE:
  warn_msg(WARN_NEED_TO_INITIALIZE);
  return TRUE;

 UNKNOWN_GATE:
  warn_msg(WARN_UNKNOWN_GATE);
  return TRUE;

 OUT_OF_BOUND:
  warn_msg(WARN_OUT_OF_BOUND);
  return TRUE;

 SAME_QUBIT_ID:
  warn_msg(WARN_SAME_QUBIT_ID);
  return TRUE;

 TOO_MANY_ARGUMENTS:
  warn_msg(WARN_TOO_MANY_ARGUMENTS);
  return TRUE;

 NEED_MORE_ARGUMENTS:
  warn_msg(WARN_NEED_MORE_ARGUMENTS);
  return TRUE;

 CANT_INITIALIZE:
  warn_msg(WARN_CANT_INITIALIZE);
  return TRUE;

 CANT_WRITE_FILE:
  warn_msg(WARN_CANT_WRITE_FILE);
  return TRUE;

 CANT_PRINT_CIRC:
  warn_msg(WARN_CANT_PRINT_CIRC);
  return TRUE;

 CANT_PRINT_GATES:
  warn_msg(WARN_CANT_PRINT_GATES);
  return TRUE;

 CANT_PRINT_HELP:
  warn_msg(WARN_CANT_PRINT_HELP);
  return TRUE;

 ERROR_EXIT:
  return FALSE;
}

int qsystem_execute(QSystem* qsystem, char* fname)
{
  FILE*         fp = NULL;
  char*		line;

  g_Errno = NO_ERROR;

  /* file open */

  if (fname != NULL) {
    if (!(fp = fopen(fname,"r"))) return TRUE;
  }
  else goto ERROR_EXIT;

  if (!(line = (char*)malloc(sizeof(char)*LINE_STRLEN)))
    goto ERROR_EXIT;

  /* read lines and execute */

  while (fgets(line, LINE_STRLEN, fp) != NULL) {
    if (qsystem_execute_one_line(qsystem, line) == FALSE) goto ERROR_EXIT;
  }

  free(line); line = NULL;
  fclose(fp);

  return TRUE;

 ERROR_EXIT:
  g_Errno = ERROR_QSYSTEM_EXECUTE;
  return FALSE;
}

int qsystem_intmode(QSystem* qsystem, char* fname_ini)
{
  char*		line	     = NULL;

  if (qsystem == NULL) goto ERROR_EXIT;

  if (fname_ini != NULL) {
    if (qsystem_execute(qsystem, fname_ini) == FALSE) goto ERROR_EXIT;
  }

  while (1) {
    line = readline(">> ");
    add_history(line);
    if (qsystem_execute_one_line(qsystem, line) == FALSE) goto ERROR_EXIT;
  }

  free(line); line = NULL;

  return TRUE;
  
 ERROR_EXIT:
  g_Errno = ERROR_QSYSTEM_INTMODE;
  return FALSE;
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
