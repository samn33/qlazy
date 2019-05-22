/*
 *  qcirc.c
 */

#include "qlazy.h"

static QCirc* qcirc_alloc(int buf_length)
{
  QCirc* qcirc = NULL;

  if (!(qcirc = (QCirc*)malloc(sizeof(QCirc)))) goto ERROR_EXIT;

  qcirc->step_num = 0;
  qcirc->qubit_num = 0;
  qcirc->buf_length = buf_length;

  if (!(qcirc->qgate = (QGate*)malloc(sizeof(QGate)*buf_length)))
    goto ERROR_EXIT;

  qcirc->cimage = NULL;

  return qcirc;
  
 ERROR_EXIT:
  return NULL;
}

static int qcirc_realloc(QCirc* qcirc)
{
  QGate* qgate = NULL;
  
  if (qcirc == NULL) goto ERROR_EXIT;

  qcirc->buf_length *= 2;

  qgate = (QGate*)realloc(qcirc->qgate, sizeof(QGate)*qcirc->buf_length);
  if (qgate == NULL) goto ERROR_EXIT;
  if (qgate != qcirc->qgate) qcirc->qgate = qgate;

  return TRUE;

 ERROR_EXIT:
  return FALSE;
}

QCirc* qcirc_init(int qubit_num, int buf_length)
{
  QCirc* qcirc = NULL;
  
  g_Errno = NO_ERROR;

  if ((qubit_num < 1) || (qubit_num > MAX_QUBIT_NUM)) goto ERROR_EXIT;

  if (!(qcirc = qcirc_alloc(buf_length))) goto ERROR_EXIT;
  qcirc->qubit_num = qubit_num;

  return qcirc;
  
 ERROR_EXIT:
  g_Errno = ERROR_QCIRC_INIT;
  return NULL;
}

int qcirc_append_qgate(QCirc* qcirc, Kind kind, int terminal_num,
		       Para* para, int qubit_id[MAX_QUBIT_NUM])
{
  g_Errno = NO_ERROR;

  if (qcirc == NULL) goto ERROR_EXIT;

  if (qcirc->step_num >= qcirc->buf_length) {
    if (qcirc_realloc(qcirc) == FALSE) goto ERROR_EXIT;
  }

  qcirc->qgate[qcirc->step_num].kind = kind;
  qcirc->qgate[qcirc->step_num].terminal_num = terminal_num;
  memcpy(qcirc->qgate[qcirc->step_num].qubit_id, qubit_id, sizeof(int)*MAX_QUBIT_NUM);

  switch (kind) {
  case MEASURE:
  case MEASURE_X:
  case MEASURE_Y:
  case MEASURE_Z:
  case MEASURE_BELL:
    qcirc->qgate[qcirc->step_num].para.mes.shots = para->mes.shots;
    qcirc->qgate[qcirc->step_num].para.mes.angle = para->mes.angle;
    qcirc->qgate[qcirc->step_num].para.mes.phase = para->mes.phase;
    break;
  case ROTATION_X:
  case ROTATION_Y:
  case ROTATION_Z:
    qcirc->qgate[qcirc->step_num].para.phase = para->phase;
    break;
  default:
    break;
  }

  (qcirc->step_num)++;
  
  return TRUE;

 ERROR_EXIT:
  g_Errno = ERROR_QCIRC_APPEND_QGATE;
  return FALSE;
}

int qcirc_set_cimage(QCirc* qcirc)
{
  char	symbol[TOKEN_STRLEN];
  char	parastr[TOKEN_STRLEN];
  int	pos = 1;
  int	p;
  
  if (qcirc == NULL) return FALSE;

  if (qcirc->cimage != NULL) {
    cimage_free(qcirc->cimage); qcirc->cimage = NULL;
  }

  /* allocate cimage and set initial character '-' */
  
  if (cimage_init(qcirc->qubit_num, qcirc->step_num, (void**)&(qcirc->cimage)) == FALSE)
    return FALSE;
  
  /* set gate charactor */
  for (int i=0; i<qcirc->step_num; i++) {
    qgate_get_symbol(symbol, qcirc->qgate[i].kind);
    p = 0;

    switch (qcirc->qgate[i].kind) {
    case INIT:
      break;
    case MEASURE:
    case MEASURE_X:
    case MEASURE_Y:
    case MEASURE_Z:
    case MEASURE_BELL:
      for (int j=0; j<qcirc->qgate[i].terminal_num; j++) {
	p = 0;
	while (symbol[p] != '\0') {
	  qcirc->cimage->ch[qcirc->qgate[i].qubit_id[j]][pos] = symbol[p];
	  pos++; p++;
	}
	pos++;
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
      while (symbol[p] != '\0') {
	qcirc->cimage->ch[qcirc->qgate[i].qubit_id[0]][pos] = symbol[p];
	pos++; p++;
      }
      pos++;
      break;
    case ROTATION_X:
    case ROTATION_Y:
    case ROTATION_Z:
      while (symbol[p] != '\0') {
	qcirc->cimage->ch[qcirc->qgate[i].qubit_id[0]][pos] = symbol[p];
	pos++; p++;
      }
      p = 0;
      sprintf(parastr, "(%.3f)", qcirc->qgate[i].para.phase);
      while (parastr[p] != '\0') {
	qcirc->cimage->ch[qcirc->qgate[i].qubit_id[0]][pos] = parastr[p];
	pos++; p++;
      }
      pos++;
      break;
    case CONTROLLED_X:
    case CONTROLLED_Z:
      qcirc->cimage->ch[qcirc->qgate[i].qubit_id[0]][pos] = '*';
      while (symbol[p] != '\0') {
	qcirc->cimage->ch[qcirc->qgate[i].qubit_id[1]][pos] = symbol[p];
	pos++; p++;
      }
      pos++;
      break;
    case TOFFOLI:
      qcirc->cimage->ch[qcirc->qgate[i].qubit_id[0]][pos] = '*';
      qcirc->cimage->ch[qcirc->qgate[i].qubit_id[1]][pos] = '*';
      while (symbol[p] != '\0') {
	qcirc->cimage->ch[qcirc->qgate[i].qubit_id[2]][pos] = symbol[p];
	pos++; p++;
      }
      pos++;
      break;
    default:
      break;
    }
  }

  for (int i=0; i<qcirc->qubit_num; i++) {
    qcirc->cimage->ch[i][pos] = '\0';
  }

  return TRUE;
}

int qcirc_print_qcirc(QCirc* qcirc)
{
  g_Errno = NO_ERROR;

  if (qcirc == NULL) goto ERROR_EXIT;

  for (int i=0; i<qcirc->qubit_num; i++) {
    printf("q%02d %s\n", i, qcirc->cimage->ch[i]);
  }

  return TRUE;

 ERROR_EXIT:
  g_Errno = ERROR_QCIRC_PRINT_QCIRC;
  return FALSE;
}
 
int qcirc_print_qgates(QCirc* qcirc)
{
  g_Errno = NO_ERROR;

  if (qcirc_write_file(qcirc, NULL) == FALSE) goto ERROR_EXIT;

  return TRUE;

 ERROR_EXIT:
  g_Errno = ERROR_QCIRC_PRINT_QGATES;
  return FALSE;
}

int qcirc_write_file(QCirc* qcirc, char* fname)
{
  FILE* fp = NULL;
  char	symbol[TOKEN_STRLEN];
  Kind	kind;
  int   terminal_num;
  Para* para;
  int*  qubit_id;
  
  g_Errno = NO_ERROR;

  if (qcirc == NULL) goto ERROR_EXIT;

  if (fname == NULL) fp = stdout;
  else if (!(fp = fopen(fname, "w"))) goto ERROR_EXIT;

  for (int i=0; i<qcirc->step_num; i++) {
    kind = qcirc->qgate[i].kind;
    terminal_num = qcirc->qgate[i].terminal_num;
    para = &(qcirc->qgate[i].para);
    qubit_id = qcirc->qgate[i].qubit_id;
    qgate_get_symbol(symbol, kind);

    switch (kind) {
    case INIT:
      fprintf(fp, "%s %d\n", symbol, qcirc->qubit_num);
      break;
    case MEASURE:
    case MEASURE_X:
    case MEASURE_Y:
    case MEASURE_Z:
    case MEASURE_BELL:
      fprintf(fp, "%s(%d) ", symbol, para->mes.shots);
      for (int k=0; k<terminal_num; k++) {
	printf("%d ",qubit_id[k]);
      }
      fprintf(fp, "\n");
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
      fprintf(fp, "%s %d\n", symbol, qubit_id[0]);
      break;
    case ROTATION_X:
    case ROTATION_Y:
    case ROTATION_Z:
      fprintf(fp, "%s(%f) %d\n", symbol, para->phase, qubit_id[0]);
      break;
    case CONTROLLED_X:
    case CONTROLLED_Z:
      fprintf(fp, "%s %d %d\n", symbol, qubit_id[0], qubit_id[1]);
      break;
    case TOFFOLI:
      fprintf(fp, "%s %d %d %d\n", symbol, qubit_id[0], qubit_id[1], qubit_id[2]);
      break;
    default:
      break;
    }
  }

  return TRUE;

 ERROR_EXIT:
  g_Errno = ERROR_QCIRC_WRITE_FILE;
  return FALSE;
}

QCirc* qcirc_read_file(char* fname)
{
  FILE*         fp = NULL;
  char*		line;
  char*		token[TOKEN_NUM];
  char*		args[TOKEN_NUM];
  int           tnum,anum;
  int		qubit_num = 0;
  Kind	kind;
  Para          para;
  int           terminal_num = 0;
  int           qubit_id[MAX_QUBIT_NUM];
  QCirc*	qcirc = NULL;

  g_Errno = NO_ERROR;

  /* file open */

  if (fname != NULL) {
    if (!(fp = fopen(fname,"r"))) goto ERROR_EXIT;
  }
  else goto ERROR_EXIT;

  /* read lines */

  if (!(line = (char*)malloc(sizeof(char)*LINE_STRLEN))) goto ERROR_EXIT;

  /* read lines */

  while (fgets(line, LINE_STRLEN, fp) != NULL) {

    if (line_check_length(line) == FALSE) goto ERROR_EXIT;

    line_chomp(line);

    if ((line_is_blank(line) == TRUE) ||
	(line_is_comment(line) == TRUE)) continue;

    tnum = line_split(line, " ", token);
    anum = line_getargs(token[0], args);

    kind = qgate_get_kind(args[0]);

    switch (kind) {
    case INIT:
      /* initialize quantum state (or reset quantum state) */
      qubit_num = strtol(token[1], NULL, 10);
      if (qcirc != NULL) { qcirc_free(qcirc); qcirc = NULL; }
      if (!(qcirc = qcirc_init(qubit_num, DEF_QCIRC_STEPS))) goto ERROR_EXIT;
      break;
    case MEASURE:
      /* measurement */
      if (qcirc == NULL) goto ERROR_EXIT;
      if (tnum > qubit_num + 1) goto ERROR_EXIT;
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
	if (qubit_num < qubit_id[i] + 1) goto ERROR_EXIT;
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
      if (qcirc == NULL) goto ERROR_EXIT;
      if (tnum > qubit_num + 1) goto ERROR_EXIT;
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
	if (qubit_num < qubit_id[i] + 1) goto ERROR_EXIT;
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
      if (qcirc == NULL) goto ERROR_EXIT;
      if (tnum < 3) goto ERROR_EXIT;
      if (tnum > 3) goto ERROR_EXIT;
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
	if (qubit_num < qubit_id[i] + 1) goto ERROR_EXIT;
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
      terminal_num = 1;
      qubit_id[0] = strtol(token[1], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) goto ERROR_EXIT;
      break;
    case ROTATION_X:
    case ROTATION_Y:
    case ROTATION_Z:
      /* 1-qubit 1-parameter gate */
      terminal_num = 1;
      if (anum == 1) {
	para.phase = DEF_PHASE;
      }
      else if (anum == 2) {
	para.phase = strtod(args[1], NULL);
      }
      else goto ERROR_EXIT;
      qubit_id[0] = strtol(token[1], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) goto ERROR_EXIT;
      break;
    case CONTROLLED_X:
    case CONTROLLED_Z:
      /* 2-qubit gate */
      terminal_num = 2;
      qubit_id[0] = strtol(token[1], NULL, 10);
      qubit_id[1] = strtol(token[2], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) goto ERROR_EXIT;
      if (qubit_num < qubit_id[1] + 1) goto ERROR_EXIT;
      break;
    case TOFFOLI:
      /* 3-qubit gate */
      terminal_num = 3;
      qubit_id[0] = strtol(token[1], NULL, 10);
      qubit_id[1] = strtol(token[2], NULL, 10);
      qubit_id[2] = strtol(token[3], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) goto ERROR_EXIT;
      if (qubit_num < qubit_id[1] + 1) goto ERROR_EXIT;
      if (qubit_num < qubit_id[2] + 1) goto ERROR_EXIT;
      break;
    default:
      break;
    }

    if (qcirc_append_qgate(qcirc, kind, terminal_num, &para, qubit_id) == FALSE)
      goto ERROR_EXIT;

  }

  /* set cimage */
  if (qcirc_set_cimage(qcirc) == FALSE) goto ERROR_EXIT;
  
  free(line); line = NULL;
  fclose(fp);

  return qcirc;

 ERROR_EXIT:
  g_Errno = ERROR_QCIRC_READ_FILE;
  return NULL;
}

void qcirc_free(QCirc* qcirc)
{
  if (qcirc != NULL) {
    if (qcirc->qgate != NULL) {
      free(qcirc->qgate); qcirc->qgate = NULL;
    }
    if (qcirc->cimage != NULL) {
      cimage_free(qcirc->cimage); qcirc->cimage = NULL;
    }
    free(qcirc);
  }
}
