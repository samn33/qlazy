/*
 *  qsystem.c
 */

#include "qlazy.h"

#ifndef USE_LIBREADLINE

static char* _rdline(const char* prompt) {
  char* buf = NULL;

  if (!(buf = (char*)malloc(sizeof(char) * LINE_STRLEN)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, NULL);

  printf("%s", prompt);

  if (fgets(buf, LINE_STRLEN, stdin) == NULL)
    ERR_RETURN(ERROR_CANT_READ_LINE, NULL);

  return buf;
}

#endif

bool qsystem_init(void** qsystem_out)
{
  QSystem* qsystem = NULL;

  if (!(qsystem = (QSystem*)malloc(sizeof(QSystem))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
  qsystem->qc = NULL;
  qsystem->qstate = NULL;
  qsystem->qubit_num = 0;

  *qsystem_out = qsystem;
  
  SUC_RETURN(true);
}

static bool _operate_qgate(QState* qstate, QG* qgate)
{
  Kind		kind	     = qgate->kind;
  Para*         para	     = &(qgate->para);
  int           terminal_num = qgate->terminal_num;
  int*          qubit_id     = qgate->qubit_id;
  MData*	mdata	     = NULL;
  
  if ((qstate == NULL) || (qgate == NULL))
      ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (!(qstate_operate_qgate(qstate, kind, para->phase.alpha, para->phase.beta,
  			     para->phase.gamma,qubit_id)))
    ERR_RETURN(ERROR_QSTATE_OPERATE_QGATE,false);

  switch (kind) {
  case INIT:
    break;
  case MEASURE:
  case MEASURE_X:
  case MEASURE_Y:
  case MEASURE_Z:
    if (!(qstate_measure_stats(qstate, para->mes.shots,
			       para->mes.angle, para->mes.phase, terminal_num,
			       qubit_id, (void**)&mdata)))
      ERR_RETURN(ERROR_QSTATE_MEASURE_STATS, false);
    mdata_print(mdata);
    mdata_free(mdata); mdata = NULL;
    break;
  case MEASURE_BELL:
    if (!(qstate_measure_bell_stats(qstate, para->mes.shots, terminal_num, qubit_id,
				    (void**)&mdata)))
      ERR_RETURN(ERROR_QSTATE_MEASURE_BELL_STATS, false);
    mdata_print_bell(mdata);
    mdata_free(mdata); mdata = NULL;
    break;
  case RESET:
    if (!(qstate_reset(qstate, terminal_num, qubit_id)))
      ERR_RETURN(ERROR_CANT_RESET, false);
    break;
  default:
    ;
  }

  SUC_RETURN(true);
}

static bool _qsystem_execute_one_line(QSystem* qsystem, char* line, bool use_gpu)
{
  char*		token[TOKEN_NUM];
  char*		args[TOKEN_NUM];
  char		comment[LINE_STRLEN];
  int           tnum,anum;
  Kind		kind;
  Para          para;
  int           terminal_num = 0;
  int           qubit_id[MAX_QUBIT_NUM];
  QG*           qgate	     = NULL;
  QC*		qc	     = qsystem->qc;
  QState*       qstate	     = qsystem->qstate;
  int		qubit_num    = qsystem->qubit_num;
  int		i;

  if (!line_check_length(line)) ERR_RETURN(ERROR_CANT_READ_LINE, false);
  if (!line_chomp(line)) ERR_RETURN(ERROR_CANT_READ_LINE, false);

  if ((line_is_blank(line) == true) ||
      (line_is_comment(line) == true)) SUC_RETURN(true);

  if (!line_split(line, " ", token, &tnum)) ERR_RETURN(ERROR_CANT_READ_LINE, false);
  if (!line_getargs(token[0], args, &anum)) ERR_RETURN(ERROR_CANT_READ_LINE, false);

  qg_get_kind(args[0], &kind);

  /* operate command */
  
  switch (kind) {
  case SHOW:
    /* print quantum state */
    if (tnum > qubit_num + 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    terminal_num = tnum - 1;  /* number of qubits to show */
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    if ((qc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE, false);
    for (i=0; i<terminal_num; i++) {
      qubit_id[i] = strtol(token[1+i], NULL, 10);
      if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
      if (qubit_id[i] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    }
    if (terminal_num == 0) {  /* show all qubits in order */
      terminal_num = qubit_num;
      for (i=0; i<terminal_num; i++) {
	qubit_id[i] = i;
      }
    }
    if (!(qstate_print(qstate, terminal_num, qubit_id, false)))
      ERR_RETURN(ERROR_CANT_PRINT_QSTATE, false);
    SUC_RETURN(true);
  case BLOCH:
    /* print bloch sphere (theta,phi) */
    if (tnum > 2) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    else if (tnum == 2) {
      qubit_id[0] = strtol(token[1], NULL, 10);
    }
    else if (tnum == 1) {
      qubit_id[0] = 0;
    }
    if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    if (!(qstate_print_bloch(qstate, qubit_id[0])))
      ERR_RETURN(ERROR_CANT_PRINT_BLOCH, false);
    SUC_RETURN(true);
  case ECHO:
    /* echo string */
    line_join_token(comment, token, 1, tnum);
    printf("%s\n", comment);
    SUC_RETURN(true);
  case OUTPUT:
    /* output file */
    fprintf(stderr, "Warn: output(>) command will be not supported in the near future.\n");
    if (tnum > 2) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    if (tnum < 2) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS, false);
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    if ((qc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE, false);
    if (!(qc_write_file(qc, token[1]))) ERR_RETURN(ERROR_CANT_WRITE_FILE, false);
    printf("output file : %s\n", token[1]);
    SUC_RETURN(true);
  case HELP:
    /* print help message */
    if (tnum > 2) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    if (tnum == 1) {
      if (!(help_print(NULL))) ERR_RETURN(ERROR_CANT_PRINT_HELP, false);
    }
    else {
      if (!(help_print(token[1]))) ERR_RETURN(ERROR_CANT_PRINT_HELP, false);
    }
    SUC_RETURN(true);
  case QUIT:
    /* quit system */
    if (tnum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
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
    if (tnum > 2) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    if (tnum < 2) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS, false);
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    qubit_num = strtol(token[1], NULL, 10);
    if ((qubit_num <= 0) || (qubit_num > MAX_QUBIT_NUM))
      ERR_RETURN(ERROR_OUT_OF_BOUND,false);
    if (qstate != NULL) { qstate_free(qstate); qstate = NULL; }
    if (qc != NULL) { qc_free(qc); qc = NULL; }
    if (!(qc_init(qubit_num, DEF_QC_STEPS, (void**)&qc)))
      ERR_RETURN(ERROR_CANT_INITIALIZE,false);
    //if (!(qstate_init(qubit_num, (void**)&qstate)))
    //    if (!(qstate_init(qubit_num, (void**)&qstate, proc)))
    if (!(qstate_init(qubit_num, (void**)&qstate, use_gpu)))
      ERR_RETURN(ERROR_CANT_INITIALIZE,false);
    break;
  case MEASURE:
    /* measurement */
    if ((qc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE, false);
    if (tnum > qubit_num + 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
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
    else ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    for (i=0; i<terminal_num; i++) {
      qubit_id[i] = strtol(token[1+i], NULL, 10);
      if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
      if (qubit_id[i] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    }
    if (terminal_num == 0) {  /* measure all qubits in order */
      terminal_num = qubit_num;
      for (i=0; i<terminal_num; i++) {
	qubit_id[i] = i;
      }
    }
    break;
  case MEASURE_X:
  case MEASURE_Y:
  case MEASURE_Z:
    /* measurement */
    if ((qc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE, false);
    if (tnum > qubit_num + 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    terminal_num = tnum - 1;  /* number of qubits to measure */
    if (anum == 1) {
      para.mes.shots = DEF_SHOTS;
    }
    else if (anum == 2) {
      para.mes.shots = strtol(args[1], NULL, 10);
    }
    else ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
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
    else ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

    for (i=0; i<terminal_num; i++) {
      qubit_id[i] = strtol(token[1+i], NULL, 10);
      if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
      if (qubit_id[i] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    }
    if (terminal_num == 0) {  /* measure all qubits in order */
      terminal_num = qubit_num;
      for (i=0; i<terminal_num; i++) {
	qubit_id[i] = i;
      }
    }
    break;
  case MEASURE_BELL:
    /* measurement */
    if ((qc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE, false);
    if (tnum < 3) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS, false);
    if (tnum > 3) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    terminal_num = 2;  /* number of qubits to measure */
    if (anum == 1) {
      para.mes.shots = DEF_SHOTS;
    }
    else if (anum == 2) {
      para.mes.shots = strtol(args[1], NULL, 10);
    }
    else ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    for (i=0; i<terminal_num; i++) {
      qubit_id[i] = strtol(token[1+i], NULL, 10);
      if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
      if (qubit_id[i] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    }
    break;
  case RESET:
    /* reset qubit */
    if (tnum > qubit_num + 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    terminal_num = tnum - 1;  /* number of qubits to reset */
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    if ((qc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE, false);
    for (i=0; i<terminal_num; i++) {
      qubit_id[i] = strtol(token[1+i], NULL, 10);
      if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
      if (qubit_id[i] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    }
    if (terminal_num == 0) {  /* reset all qubit */
      terminal_num = qubit_num;
      for (i=0; i<terminal_num; i++) {
	qubit_id[i] = i;
      }
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
    if ((qc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE, false);
    if (tnum > 2) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    if (tnum < 2) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS, false);
    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    terminal_num = 1;
    qubit_id[0] = strtol(token[1], NULL, 10);
    if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    break;
  case ROTATION_X:
  case ROTATION_Y:
  case ROTATION_Z:
  case PHASE_SHIFT:
    /* 1-qubit 1-parameter gate */
    if ((qc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE, false);
    if (tnum > 2) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    if (tnum < 2) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS, false);
    terminal_num = 1;
    if (anum == 1) {
      para.phase.alpha = DEF_PHASE;
      para.phase.beta = DEF_PHASE;
      para.phase.gamma = DEF_PHASE;
    }
    else if (anum == 2) {
      para.phase.alpha = strtod(args[1], NULL);
      para.phase.beta = DEF_PHASE;
      para.phase.gamma = DEF_PHASE;
    }
    else ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    qubit_id[0] = strtol(token[1], NULL, 10);
    if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
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
    /* 2-qubit gate */
    if ((qc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE, false);
    if (tnum > 3) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    if (tnum < 3) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS, false);

    if (anum > 1) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    terminal_num = 2;
    qubit_id[0] = strtol(token[1], NULL, 10);
    qubit_id[1] = strtol(token[2], NULL, 10);
    if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    if (qubit_num < qubit_id[1] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    if (qubit_id[1] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    if (qubit_id[0] == qubit_id[1]) ERR_RETURN(ERROR_SAME_QUBIT_ID, false);
    break;
  case CONTROLLED_P:
  case CONTROLLED_RX:
  case CONTROLLED_RY:
  case CONTROLLED_RZ:
  case ROTATION_XX:
  case ROTATION_YY:
  case ROTATION_ZZ:
    /* 2-qubit, 1-parameter gate */
    if ((qc == NULL) || (qstate == NULL)) ERR_RETURN(ERROR_NEED_TO_INITIALIZE, false);
    if (tnum > 3) ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS, false);
    if (tnum < 3) ERR_RETURN(ERROR_NEED_MORE_ARGUMENTS, false);
    terminal_num = 2;
    if (anum == 1) {
      para.phase.alpha = DEF_PHASE;
      para.phase.beta = DEF_PHASE;
      para.phase.gamma = DEF_PHASE;
    }
    else if (anum == 2) {
      para.phase.alpha = strtod(args[1], NULL);
      para.phase.beta = DEF_PHASE;
      para.phase.gamma = DEF_PHASE;
    }
    else ERR_RETURN(ERROR_TOO_MANY_ARGUMENTS,false);
    qubit_id[0] = strtol(token[1], NULL, 10);
    qubit_id[1] = strtol(token[2], NULL, 10);
    if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    if (qubit_num < qubit_id[1] + 1) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    if (qubit_id[1] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
    if (qubit_id[0] == qubit_id[1]) ERR_RETURN(ERROR_SAME_QUBIT_ID, false);
    break;
    
  default:
    ERR_RETURN(ERROR_UNKNOWN_GATE, false);
  }

  if (!(qc_append_qgate(qc, kind, terminal_num, &para, qubit_id))) /* set para */
    ERR_RETURN(ERROR_QC_APPEND_QGATE, false);

  qgate = &(qc->qgate[qc->step_num - 1]);
  if (!(_operate_qgate(qstate, qgate)))
    ERR_RETURN(ERROR_QSTATE_OPERATE_QGATE, false);

  qsystem->qc = qc;
  qsystem->qstate = qstate;
  qsystem->qubit_num = qubit_num;

  SUC_RETURN(true);
}

bool qsystem_execute(QSystem* qsystem, char* fname, bool use_gpu)
{
  FILE*         fp = NULL;
  char*		line;

  /* file open */

  if (fname != NULL) {
    if (!(fp = fopen(fname,"r"))) SUC_RETURN(true);
  }
  else fp = stdin;
  
  if (!(line = (char*)malloc(sizeof(char) * LINE_STRLEN)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  /* read lines and execute */

  while (fgets(line, LINE_STRLEN, fp) != NULL) {
    if (!(_qsystem_execute_one_line(qsystem, line, use_gpu))) {
      ERR_RETURN(ERROR_CANT_READ_LINE, false);
    }
  }

  free(line); line = NULL;
  fclose(fp);

  SUC_RETURN(true);
}

bool qsystem_intmode(QSystem* qsystem, char* fname_ini, bool use_gpu)
{
  char*		line	     = NULL;

  if (qsystem == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (fname_ini != NULL) {
    if (!(qsystem_execute(qsystem, fname_ini, use_gpu))) {
      ERR_RETURN(ERROR_QSYSTEM_EXECUTE, false);
    }
  }

#ifdef USE_LIBREADLINE
  
  while (1) {
    line = readline(">> ");
    add_history(line);
    _qsystem_execute_one_line(qsystem, line, use_gpu);
    free(line); line = NULL;
  }

#else

  while (1) {
    line = _rdline(">> ");
    if (line == NULL) ERR_RETURN(ERROR_CANT_READ_LINE, false);
    _qsystem_execute_one_line(qsystem, line, use_gpu);
    free(line); line = NULL;
  }

#endif
  
  SUC_RETURN(true);
}

void qsystem_free(QSystem* qsystem)
{
  if (qsystem != NULL) {
    if (qsystem->qc != NULL) {
      qc_free(qsystem->qc); qsystem->qc = NULL;
    }
    if (qsystem->qstate != NULL) {
      qstate_free(qsystem->qstate); qsystem->qstate = NULL;
    }
    free(qsystem);
  }
}
