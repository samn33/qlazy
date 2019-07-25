/*
 *  qcirc.c
 */

#include "qlazy.h"

static QCirc* _qcirc_alloc(int buf_length)
{
  QCirc* qcirc = NULL;

  if (!(qcirc = (QCirc*)malloc(sizeof(QCirc))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);

  qcirc->step_num = 0;
  qcirc->qubit_num = 0;
  qcirc->buf_length = buf_length;

  if (!(qcirc->qgate = (QGate*)malloc(sizeof(QGate)*buf_length))) {
    qcirc_free(qcirc); qcirc = NULL;
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);
  }
  qcirc->cimage = NULL;

  SUC_RETURN(qcirc);
}

static bool _qcirc_realloc(QCirc* qcirc)
{
  QGate* qgate = NULL;
  
  if (qcirc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  qcirc->buf_length *= 2;

  qgate = (QGate*)realloc(qcirc->qgate, sizeof(QGate)*qcirc->buf_length);
  if (qgate == NULL) ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  if (qgate != qcirc->qgate) qcirc->qgate = qgate;

  SUC_RETURN(true);
}

bool qcirc_init(int qubit_num, int buf_length, void** qcirc_out)
{
  QCirc* qcirc = NULL;

  if ((qubit_num < 1) || (qubit_num > MAX_QUBIT_NUM))
    ERR_RETURN(ERROR_OUT_OF_BOUND,false);

  if (!(qcirc = _qcirc_alloc(buf_length)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  qcirc->qubit_num = qubit_num;

  *qcirc_out = qcirc;
  
  SUC_RETURN(true);
}

bool qcirc_append_qgate(QCirc* qcirc, Kind kind, int terminal_num,
		       Para* para, int qubit_id[MAX_QUBIT_NUM])
{
  if (qcirc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (qcirc->step_num >= qcirc->buf_length) {
    if (!(_qcirc_realloc(qcirc))) ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
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
  case PHASE_SHIFT:
  case CONTROLLED_RX:
  case CONTROLLED_RY:
  case CONTROLLED_RZ:
  case CONTROLLED_P:
    qcirc->qgate[qcirc->step_num].para.phase = para->phase;
    break;
  default:
    break;
  }

  (qcirc->step_num)++;
  
  SUC_RETURN(true);
}

bool qcirc_set_cimage(QCirc* qcirc)
{
  char	symbol[TOKEN_STRLEN];
  char	parastr[TOKEN_STRLEN];
  int	pos = 1;
  int	p;

  if (qcirc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* free previous cimage */
  if (qcirc->cimage != NULL) {
    cimage_free(qcirc->cimage); qcirc->cimage = NULL;
  }

  /* allocate cimage and set initial character '-' */
  if (!(cimage_init(qcirc->qubit_num, qcirc->step_num, (void**)&(qcirc->cimage))))
    ERR_RETURN(ERROR_CIMAGE_INIT,false);
  
  /* set gate charactor */
  for (int i=0; i<qcirc->step_num; i++) {
    if (!(qgate_get_symbol(symbol, qcirc->qgate[i].kind)))
      ERR_RETURN(ERROR_QGATE_GET_SYMBOL,false);
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
    case PHASE_SHIFT:
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
    case CONTROLLED_Y:
    case CONTROLLED_Z:
    case CONTROLLED_XR:
    case CONTROLLED_XR_:
    case CONTROLLED_H:
    case CONTROLLED_S:
    case CONTROLLED_S_:
    case CONTROLLED_T:
    case CONTROLLED_T_:
      qcirc->cimage->ch[qcirc->qgate[i].qubit_id[0]][pos] = '*';
      while (symbol[p] != '\0') {
	qcirc->cimage->ch[qcirc->qgate[i].qubit_id[1]][pos] = symbol[p];
	pos++; p++;
      }
      pos++;
      break;
    case CONTROLLED_P:
    case CONTROLLED_RX:
    case CONTROLLED_RY:
    case CONTROLLED_RZ:
      qcirc->cimage->ch[qcirc->qgate[i].qubit_id[0]][pos] = '*';
      while (symbol[p] != '\0') {
	qcirc->cimage->ch[qcirc->qgate[i].qubit_id[1]][pos] = symbol[p];
	pos++; p++;
      }
      p = 0;
      sprintf(parastr, "(%.3f)", qcirc->qgate[i].para.phase);
      while (parastr[p] != '\0') {
	qcirc->cimage->ch[qcirc->qgate[i].qubit_id[1]][pos] = parastr[p];
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

  SUC_RETURN(true);
}

bool qcirc_print_qcirc(QCirc* qcirc)
{
  if (qcirc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  for (int i=0; i<qcirc->qubit_num; i++) {
    printf("q%02d %s\n", i, qcirc->cimage->ch[i]);
  }

  SUC_RETURN(true);
}
 
bool qcirc_print_qgates(QCirc* qcirc)
{
  if (!(qcirc_write_file(qcirc, NULL)))
    ERR_RETURN(ERROR_QCIRC_WRITE_FILE,false);
  
  SUC_RETURN(true);
}

bool qcirc_write_file(QCirc* qcirc, char* fname)
{
  FILE* fp = NULL;
  char	symbol[TOKEN_STRLEN];
  Kind	kind;
  int   terminal_num;
  Para* para;
  int*  qubit_id;

  if (qcirc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (fname == NULL) fp = stdout;
  else if (!(fp = fopen(fname, "w")))
    ERR_RETURN(ERROR_CANT_OPEN_FILE,false);

  for (int i=0; i<qcirc->step_num; i++) {
    kind = qcirc->qgate[i].kind;
    terminal_num = qcirc->qgate[i].terminal_num;
    para = &(qcirc->qgate[i].para);
    qubit_id = qcirc->qgate[i].qubit_id;
    if (!(qgate_get_symbol(symbol, kind)))
      ERR_RETURN(ERROR_QGATE_GET_SYMBOL,false);

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
    case PHASE_SHIFT:
      fprintf(fp, "%s(%f) %d\n", symbol, para->phase, qubit_id[0]);
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
      fprintf(fp, "%s %d %d\n", symbol, qubit_id[0], qubit_id[1]);
      break;
    case CONTROLLED_RX:
    case CONTROLLED_RY:
    case CONTROLLED_RZ:
    case CONTROLLED_P:
      fprintf(fp, "%s(%f) %d %d\n", symbol, para->phase, qubit_id[0], qubit_id[1]);
      break;
    case TOFFOLI:
      fprintf(fp, "%s %d %d %d\n", symbol, qubit_id[0], qubit_id[1], qubit_id[2]);
      break;
    default:
      break;
    }
  }

  SUC_RETURN(true);
}

bool qcirc_read_file(char* fname, void** qcirc_out)
{
  FILE*         fp	     = NULL;
  char*		line;
  char*		token[TOKEN_NUM];
  char*		args[TOKEN_NUM];
  int           tnum,anum;
  int		qubit_num    = 0;
  Kind		kind;
  Para          para;
  int           terminal_num = 0;
  int           qubit_id[MAX_QUBIT_NUM];
  QCirc*	qcirc	     = NULL;

  /* file open */

  if (fname != NULL) {
    if (!(fp = fopen(fname,"r")))
      ERR_RETURN(ERROR_CANT_OPEN_FILE,false);
  }
  else ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  /* read lines */

  if (!(line = (char*)malloc(sizeof(char)*LINE_STRLEN)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);

  /* read lines */

  while (fgets(line, LINE_STRLEN, fp) != NULL) {

    if (!line_check_length(line)) ERR_RETURN(ERROR_CANT_READ_LINE,false);
    if (!line_chomp(line)) ERR_RETURN(ERROR_CANT_READ_LINE,false);

    if (line_is_blank(line) || line_is_comment(line)) continue;

    if (!line_split(line, " ", token, &tnum)) ERR_RETURN(ERROR_CANT_READ_LINE,false);
    if (!line_getargs(token[0], args, &anum)) ERR_RETURN(ERROR_CANT_READ_LINE,false);

    qgate_get_kind(args[0], &kind);

    switch (kind) {
    case INIT:
      /* initialize quantum state (or reset quantum state) */
      qubit_num = strtol(token[1], NULL, 10);
      if (qcirc != NULL) { qcirc_free(qcirc); qcirc = NULL; }
      if (!(qcirc_init(qubit_num, DEF_QCIRC_STEPS, (void**)&qcirc)))
	ERR_RETURN(ERROR_QCIRC_INIT,false);
      break;
    case MEASURE:
      /* measurement */
      if (qcirc == NULL) ERR_RETURN(ERROR_CANT_READ_LINE,false);
      if (tnum > qubit_num + 1) ERR_RETURN(ERROR_CANT_READ_LINE,false);
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
      else ERR_RETURN(ERROR_CANT_READ_LINE,false);
      for (int i=0; i<terminal_num; i++) {
	qubit_id[i] = strtol(token[1+i], NULL, 10);
	if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_CANT_READ_LINE,false);
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
      if (qcirc == NULL) ERR_RETURN(ERROR_CANT_READ_LINE,false);
      if (tnum > qubit_num + 1) ERR_RETURN(ERROR_CANT_READ_LINE,false);
      terminal_num = tnum - 1;  /* number of qubits to measure */
      if (anum == 1) {
	para.mes.shots = DEF_SHOTS;
      }
      else if (anum == 2) {
	para.mes.shots = strtol(args[1], NULL, 10);
      }
      else ERR_RETURN(ERROR_CANT_READ_LINE,false);

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
      else ERR_RETURN(ERROR_CANT_READ_LINE,false);;

      for (int i=0; i<terminal_num; i++) {
	qubit_id[i] = strtol(token[1+i], NULL, 10);
	if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_CANT_READ_LINE,false);
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
      if (qcirc == NULL) ERR_RETURN(ERROR_CANT_READ_LINE,false);
      if (tnum < 3) ERR_RETURN(ERROR_CANT_READ_LINE,false);
      if (tnum > 3) ERR_RETURN(ERROR_CANT_READ_LINE,false);
      terminal_num = 2;  /* number of qubits to measure */
      if (anum == 1) {
	para.mes.shots = DEF_SHOTS;
      }
      else if (anum == 2) {
	para.mes.shots = strtol(args[1], NULL, 10);
      }
      else ERR_RETURN(ERROR_CANT_READ_LINE,false);

      for (int i=0; i<terminal_num; i++) {
	qubit_id[i] = strtol(token[1+i], NULL, 10);
	if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_CANT_READ_LINE,false);
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
      if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_CANT_READ_LINE,false);
      break;
    case ROTATION_X:
    case ROTATION_Y:
    case ROTATION_Z:
    case PHASE_SHIFT:
      /* 1-qubit 1-parameter gate */
      terminal_num = 1;
      if (anum == 1) {
	para.phase = DEF_PHASE;
      }
      else if (anum == 2) {
	para.phase = strtod(args[1], NULL);
      }
      else ERR_RETURN(ERROR_CANT_READ_LINE,false);
      qubit_id[0] = strtol(token[1], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_CANT_READ_LINE,false);
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
      /* 2-qubit gate */
      terminal_num = 2;
      qubit_id[0] = strtol(token[1], NULL, 10);
      qubit_id[1] = strtol(token[2], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_CANT_READ_LINE,false);
      if (qubit_num < qubit_id[1] + 1) ERR_RETURN(ERROR_CANT_READ_LINE,false);
      if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
      if (qubit_id[1] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
      if (qubit_id[0] == qubit_id[1]) ERR_RETURN(ERROR_SAME_QUBIT_ID,false);
      break;
    case CONTROLLED_RX:
    case CONTROLLED_RY:
    case CONTROLLED_RZ:
    case CONTROLLED_P:
      /* 2-qubit, 1-parameter gate */
      terminal_num = 2;
      if (anum == 1) {
	para.phase = DEF_PHASE;
      }
      else if (anum == 2) {
	para.phase = strtod(args[1], NULL);
      }
      else ERR_RETURN(ERROR_CANT_READ_LINE,false);
      qubit_id[0] = strtol(token[1], NULL, 10);
      qubit_id[1] = strtol(token[2], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_CANT_READ_LINE,false);
      if (qubit_num < qubit_id[1] + 1) ERR_RETURN(ERROR_CANT_READ_LINE,false);
      if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
      if (qubit_id[1] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND,false);
      if (qubit_id[0] == qubit_id[1]) ERR_RETURN(ERROR_SAME_QUBIT_ID,false);
      break;
    case TOFFOLI:
      /* 3-qubit gate */
      terminal_num = 3;
      qubit_id[0] = strtol(token[1], NULL, 10);
      qubit_id[1] = strtol(token[2], NULL, 10);
      qubit_id[2] = strtol(token[3], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_CANT_READ_LINE,false);
      if (qubit_num < qubit_id[1] + 1) ERR_RETURN(ERROR_CANT_READ_LINE,false);
      if (qubit_num < qubit_id[2] + 1) ERR_RETURN(ERROR_CANT_READ_LINE,false);
      break;
    default:
      break;
    }

    if (!(qcirc_append_qgate(qcirc, kind, terminal_num, &para, qubit_id)))
      ERR_RETURN(ERROR_QCIRC_APPEND_QGATE,false);
  }

  /* set cimage */
  if (!(qcirc_set_cimage(qcirc)))
    ERR_RETURN(ERROR_QCIRC_SET_CIMAGE,false);
  
  free(line); line = NULL;
  fclose(fp);

  *qcirc_out = qcirc;
  
  SUC_RETURN(true);
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
