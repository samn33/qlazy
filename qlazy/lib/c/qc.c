/*
 *  qc.c
 */

#include "qlazy.h"

static bool _cimage_init(int qubit_num, int step_num, void** cimage_out)
{
  CImage* cimage = NULL;
  int     glen = 20;
  int     i,j;

  if (!(cimage = (CImage*)malloc(sizeof(CImage))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
  
  cimage->qubit_num = qubit_num;
  if (!(cimage->ch = (char**)malloc(sizeof(char*) * qubit_num)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
  
  for (i = 0; i < qubit_num; i++) {
    if (!(cimage->ch[i] = (char*)malloc(sizeof(char) * step_num*glen)))
      ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,false);
    for (j=0; j<step_num*glen; j++) cimage->ch[i][j] = '-';
    cimage->ch[i][step_num*glen] = '\0';
  }

  *cimage_out = cimage;

  SUC_RETURN(true);
}

static void _cimage_free(CImage* cimage)
{
  int i;
  
  if (cimage != NULL) {
    if (cimage->ch != NULL) {
      for (i=0; i<cimage->qubit_num; i++) {
	free(cimage->ch[i]);
	cimage->ch[i] = NULL;
      }
      free(cimage->ch); cimage->ch = NULL;
    }
    free(cimage);
  }
}

static QC* _qc_alloc(int buf_length)
{
  QC* qc = NULL;

  if (!(qc = (QC*)malloc(sizeof(QC))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, NULL);

  qc->step_num = 0;
  qc->qubit_num = 0;
  qc->buf_length = buf_length;

  if (!(qc->qgate = (QG*)malloc(sizeof(QG) * buf_length))) {
    qc_free(qc); qc = NULL;
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, NULL);
  }
  qc->cimage = NULL;

  SUC_RETURN(qc);
}

static bool _qc_realloc(QC* qc)
{
  QG* qgate = NULL;
  
  if (qc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  qc->buf_length *= 2;

  qgate = (QG*)realloc(qc->qgate, sizeof(QG)*qc->buf_length);
  if (qgate == NULL) ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
  if (qgate != qc->qgate) qc->qgate = qgate;

  SUC_RETURN(true);
}

bool qc_init(int qubit_num, int buf_length, void** qc_out)
{
  QC* qc = NULL;

  if ((qubit_num < 1) || (qubit_num > MAX_QUBIT_NUM))
    ERR_RETURN(ERROR_OUT_OF_BOUND, false);

  if (!(qc = _qc_alloc(buf_length)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
  qc->qubit_num = qubit_num;

  *qc_out = qc;
  
  SUC_RETURN(true);
}

bool qc_append_qgate(QC* qc, Kind kind, int terminal_num,
		       Para* para, int* qubit_id)
{
  if (qc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT,false);

  if (qc->step_num >= qc->buf_length) {
    if (!(_qc_realloc(qc))) ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
  }

  qc->qgate[qc->step_num].kind = kind;
  qc->qgate[qc->step_num].terminal_num = terminal_num;
  memcpy(qc->qgate[qc->step_num].qubit_id, qubit_id, sizeof(int) * MAX_QUBIT_NUM);

  switch (kind) {
  case MEASURE:
  case MEASURE_X:
  case MEASURE_Y:
  case MEASURE_Z:
  case MEASURE_BELL:
    qc->qgate[qc->step_num].para.mes.shots = para->mes.shots;
    qc->qgate[qc->step_num].para.mes.angle = para->mes.angle;
    qc->qgate[qc->step_num].para.mes.phase = para->mes.phase;
    break;
  case ROTATION_X:
  case ROTATION_Y:
  case ROTATION_Z:
  case PHASE_SHIFT:
  case ROTATION_U1:
  case ROTATION_U2:
  case ROTATION_U3:
  case CONTROLLED_RX:
  case CONTROLLED_RY:
  case CONTROLLED_RZ:
  case CONTROLLED_U1:
  case CONTROLLED_U2:
  case CONTROLLED_U3:
  case CONTROLLED_P:
  case ROTATION_XX:
  case ROTATION_YY:
  case ROTATION_ZZ:
    qc->qgate[qc->step_num].para.phase.alpha = para->phase.alpha;
    qc->qgate[qc->step_num].para.phase.beta = para->phase.beta;
    qc->qgate[qc->step_num].para.phase.gamma = para->phase.gamma;
    break;
  default:
    break;
  }

  (qc->step_num)++;
  
  SUC_RETURN(true);
}

bool qc_set_cimage(QC* qc)
{
  char	symbol[TOKEN_STRLEN];
  char	parastr[TOKEN_STRLEN];
  int	pos = 1;
  int	p;
  int   i,j;

  if (qc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  /* free previous cimage */
  if (qc->cimage != NULL) {
    _cimage_free(qc->cimage); qc->cimage = NULL;
  }

  /* allocate cimage and set initial character '-' */
  if (!(_cimage_init(qc->qubit_num, qc->step_num, (void**)&(qc->cimage))))
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  
  /* set gate charactor */
  for (i=0; i<qc->step_num; i++) {
    if (!(qg_get_symbol(qc->qgate[i].kind, symbol)))
      ERR_RETURN(ERROR_QG_GET_SYMBOL, false);
    p = 0;

    switch (qc->qgate[i].kind) {
    case INIT:
      break;
    case MEASURE:
    case MEASURE_X:
    case MEASURE_Y:
    case MEASURE_Z:
    case MEASURE_BELL:
    case RESET:
      for (j=0; j<qc->qgate[i].terminal_num; j++) {
	p = 0;
	while (symbol[p] != '\0') {
	  qc->cimage->ch[qc->qgate[i].qubit_id[j]][pos] = symbol[p];
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
	qc->cimage->ch[qc->qgate[i].qubit_id[0]][pos] = symbol[p];
	pos++; p++;
      }
      pos++;
      break;
    case ROTATION_X:
    case ROTATION_Y:
    case ROTATION_Z:
    case PHASE_SHIFT:
    case ROTATION_U1:
    case ROTATION_U2:
    case ROTATION_U3:
      while (symbol[p] != '\0') {
	qc->cimage->ch[qc->qgate[i].qubit_id[0]][pos] = symbol[p];
	pos++; p++;
      }
      p = 0;
      snprintf(parastr, TOKEN_STRLEN, "(%.3f)", qc->qgate[i].para.phase.alpha);
      while (parastr[p] != '\0') {
	qc->cimage->ch[qc->qgate[i].qubit_id[0]][pos] = parastr[p];
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
      qc->cimage->ch[qc->qgate[i].qubit_id[0]][pos] = '*';
      while (symbol[p] != '\0') {
	qc->cimage->ch[qc->qgate[i].qubit_id[1]][pos] = symbol[p];
	pos++; p++;
      }
      pos++;
      break;
    case SWAP_QUBITS:
      qc->cimage->ch[qc->qgate[i].qubit_id[0]][pos] = 'x';
      qc->cimage->ch[qc->qgate[i].qubit_id[1]][pos] = 'x';
      pos++;
      break;
    case CONTROLLED_P:
    case CONTROLLED_RX:
    case CONTROLLED_RY:
    case CONTROLLED_RZ:
    case CONTROLLED_U1:
    case CONTROLLED_U2:
    case CONTROLLED_U3:
      qc->cimage->ch[qc->qgate[i].qubit_id[0]][pos] = '*';
      while (symbol[p] != '\0') {
	qc->cimage->ch[qc->qgate[i].qubit_id[1]][pos] = symbol[p];
	pos++; p++;
      }
      p = 0;
      snprintf(parastr, TOKEN_STRLEN, "(%.3f)", qc->qgate[i].para.phase.alpha);
      while (parastr[p] != '\0') {
	qc->cimage->ch[qc->qgate[i].qubit_id[1]][pos] = parastr[p];
	pos++; p++;
      }
      pos++;
      break;
    default:
      break;
    }
  }

  for (i=0; i<qc->qubit_num; i++) {
    qc->cimage->ch[i][pos] = '\0';
  }

  SUC_RETURN(true);
}

bool qc_print_qc(QC* qc)
{
  int i;
  
  if (qc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  for (i=0; i<qc->qubit_num; i++) {
    printf("q%02d %s\n", i, qc->cimage->ch[i]);
  }

  SUC_RETURN(true);
}
 
bool qc_print_qgates(QC* qc)
{
  if (!(qc_write_file(qc, NULL)))
    ERR_RETURN(ERROR_QC_WRITE_FILE, false);
  
  SUC_RETURN(true);
}

bool qc_write_file(QC* qc, char* fname)
{
  FILE* fp = NULL;
  char	symbol[TOKEN_STRLEN];
  Kind	kind;
  int   terminal_num;
  Para* para;
  int*  qubit_id;
  int   i,k;

  if (qc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (fname == NULL) fp = stdout;
  else if (!(fp = fopen(fname, "w")))
    ERR_RETURN(ERROR_CANT_OPEN_FILE, false);

  for (i=0; i<qc->step_num; i++) {
    kind = qc->qgate[i].kind;
    terminal_num = qc->qgate[i].terminal_num;
    para = &(qc->qgate[i].para);
    qubit_id = qc->qgate[i].qubit_id;
    if (!(qg_get_symbol(kind, symbol)))
      ERR_RETURN(ERROR_QG_GET_SYMBOL, false);

    switch (kind) {
    case INIT:
      fprintf(fp, "%s %d\n", symbol, qc->qubit_num);
      break;
    case MEASURE:
    case MEASURE_X:
    case MEASURE_Y:
    case MEASURE_Z:
    case MEASURE_BELL:
      fprintf(fp, "%s(%d) ", symbol, para->mes.shots);
      for (k=0; k<terminal_num; k++) {
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
    case ROTATION_U1:
      fprintf(fp, "%s(%f) %d\n", symbol, para->phase.alpha, qubit_id[0]);
      break;
    case ROTATION_U2:
      fprintf(fp, "%s(%f,%f) %d\n", symbol, para->phase.alpha,
	      para->phase.beta, qubit_id[0]);
      break;
    case ROTATION_U3:
      fprintf(fp, "%s(%f,%f,%f) %d\n", symbol, para->phase.alpha,
	      para->phase.beta, para->phase.gamma, qubit_id[0]);
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
      fprintf(fp, "%s %d %d\n", symbol, qubit_id[0], qubit_id[1]);
      break;
    case CONTROLLED_RX:
    case CONTROLLED_RY:
    case CONTROLLED_RZ:
    case CONTROLLED_U1:
    case CONTROLLED_P:
      fprintf(fp, "%s(%f) %d %d\n", symbol, para->phase.alpha, qubit_id[0], qubit_id[1]);
    case CONTROLLED_U2:
      fprintf(fp, "%s(%f,%f) %d %d\n", symbol, para->phase.alpha,
	      para->phase.beta, qubit_id[0], qubit_id[1]);
    case CONTROLLED_U3:
      fprintf(fp, "%s(%f,%f,%f) %d %d\n", symbol, para->phase.alpha,
	      para->phase.beta, para->phase.gamma, qubit_id[0], qubit_id[1]);
      break;
    default:
      break;
    }
  }

  SUC_RETURN(true);
}

bool qc_read_file(char* fname, void** qc_out)
{
  FILE* fp	     = NULL;
  char*	line;
  char*	token[TOKEN_NUM];
  char*	args[TOKEN_NUM];
  int   tnum,anum;
  int	qubit_num    = 0;
  Kind	kind;
  Para  para;
  int   terminal_num = 0;
  int   qubit_id[MAX_QUBIT_NUM];
  QC*	qc	     = NULL;
  int   i;

  /* file open */

  if (fname != NULL) {
    if (!(fp = fopen(fname,"r")))
      ERR_RETURN(ERROR_CANT_OPEN_FILE, false);
  }
  else fp = stdin;

  /* read lines */

  if (!(line = (char*)malloc(sizeof(char) * LINE_STRLEN)))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);

  /* read lines */

  while (fgets(line, LINE_STRLEN, fp) != NULL) {

    if (!line_check_length(line)) ERR_RETURN(ERROR_CANT_READ_LINE, false);
    if (!line_chomp(line)) ERR_RETURN(ERROR_CANT_READ_LINE, false);

    if (line_is_blank(line) || line_is_comment(line)) continue;

    if (!line_split(line, " ", token, &tnum)) ERR_RETURN(ERROR_CANT_READ_LINE, false);
    if (!line_getargs(token[0], args, &anum)) ERR_RETURN(ERROR_CANT_READ_LINE, false);

    qg_get_kind(args[0], &kind);

    switch (kind) {
    case INIT:
      /* initialize quantum state (or reset quantum state) */
      qubit_num = strtol(token[1], NULL, 10);
      if (qc != NULL) { qc_free(qc); qc = NULL; }
      if (!(qc_init(qubit_num, DEF_QC_STEPS, (void**)&qc)))
	ERR_RETURN(ERROR_QC_INIT,false);
      break;
    case MEASURE:
      /* measurement */
      if (qc == NULL) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      if (tnum > qubit_num + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
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
      for (i=0; i<terminal_num; i++) {
	qubit_id[i] = strtol(token[1+i], NULL, 10);
	if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
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
      if (qc == NULL) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      if (tnum > qubit_num + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      terminal_num = tnum - 1;  /* number of qubits to measure */
      if (anum == 1) {
	para.mes.shots = DEF_SHOTS;
      }
      else if (anum == 2) {
	para.mes.shots = strtol(args[1], NULL, 10);
      }
      else ERR_RETURN(ERROR_CANT_READ_LINE, false);

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
      else ERR_RETURN(ERROR_CANT_READ_LINE, false);;

      for (i=0; i<terminal_num; i++) {
	qubit_id[i] = strtol(token[1+i], NULL, 10);
	if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
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
      if (qc == NULL) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      if (tnum < 3) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      if (tnum > 3) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      terminal_num = 2;  /* number of qubits to measure */
      if (anum == 1) {
	para.mes.shots = DEF_SHOTS;
      }
      else if (anum == 2) {
	para.mes.shots = strtol(args[1], NULL, 10);
      }
      else ERR_RETURN(ERROR_CANT_READ_LINE, false);

      for (i=0; i<terminal_num; i++) {
	qubit_id[i] = strtol(token[1+i], NULL, 10);
	if (qubit_num < qubit_id[i] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
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
      if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      break;
    case ROTATION_X:
    case ROTATION_Y:
    case ROTATION_Z:
    case PHASE_SHIFT:
    case ROTATION_U1:
      /* 1-qubit 1-parameter gate */
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
      else ERR_RETURN(ERROR_CANT_READ_LINE, false);
      qubit_id[0] = strtol(token[1], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      break;
    case ROTATION_U2:
      /* 1-qubit 2-parameter gate */
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
      else if (anum == 3) {
	para.phase.alpha = strtod(args[1], NULL);
	para.phase.beta = strtod(args[2], NULL);
	para.phase.gamma = DEF_PHASE;
      }
      else ERR_RETURN(ERROR_CANT_READ_LINE, false);
      qubit_id[0] = strtol(token[1], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      break;
    case ROTATION_U3:
      /* 1-qubit 3-parameter gate */
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
      else if (anum == 3) {
	para.phase.alpha = strtod(args[1], NULL);
	para.phase.beta = strtod(args[2], NULL);
	para.phase.gamma = DEF_PHASE;
      }
      else if (anum == 4) {
	para.phase.alpha = strtod(args[1], NULL);
	para.phase.beta = strtod(args[2], NULL);
	para.phase.gamma = strtod(args[3], NULL);
      }
      else ERR_RETURN(ERROR_CANT_READ_LINE, false);
      qubit_id[0] = strtol(token[1], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
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
      terminal_num = 2;
      qubit_id[0] = strtol(token[1], NULL, 10);
      qubit_id[1] = strtol(token[2], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      if (qubit_num < qubit_id[1] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
      if (qubit_id[1] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
      if (qubit_id[0] == qubit_id[1]) ERR_RETURN(ERROR_SAME_QUBIT_ID, false);
      break;
    case CONTROLLED_RX:
    case CONTROLLED_RY:
    case CONTROLLED_RZ:
    case CONTROLLED_P:
    case CONTROLLED_U1:
      /* 2-qubit, 1-parameter gate */
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
      else ERR_RETURN(ERROR_CANT_READ_LINE, false);
      qubit_id[0] = strtol(token[1], NULL, 10);
      qubit_id[1] = strtol(token[2], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      if (qubit_num < qubit_id[1] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
      if (qubit_id[1] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
      if (qubit_id[0] == qubit_id[1]) ERR_RETURN(ERROR_SAME_QUBIT_ID, false);
      break;
    case CONTROLLED_U2:
      /* 2-qubit, 2-parameter gate */
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
      else if (anum == 3) {
	para.phase.alpha = strtod(args[1], NULL);
	para.phase.beta = strtod(args[2], NULL);
	para.phase.gamma = DEF_PHASE;
      }
      else ERR_RETURN(ERROR_CANT_READ_LINE, false);
      qubit_id[0] = strtol(token[1], NULL, 10);
      qubit_id[1] = strtol(token[2], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      if (qubit_num < qubit_id[1] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
      if (qubit_id[1] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
      if (qubit_id[0] == qubit_id[1]) ERR_RETURN(ERROR_SAME_QUBIT_ID, false);
      break;
    case CONTROLLED_U3:
      /* 2-qubit, 3-parameter gate */
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
      else if (anum == 3) {
	para.phase.alpha = strtod(args[1], NULL);
	para.phase.beta = strtod(args[2], NULL);
	para.phase.gamma = DEF_PHASE;
      }
      else if (anum == 4) {
	para.phase.alpha = strtod(args[1], NULL);
	para.phase.beta = strtod(args[2], NULL);
	para.phase.gamma = strtod(args[3], NULL);
      }
      else ERR_RETURN(ERROR_CANT_READ_LINE, false);
      qubit_id[0] = strtol(token[1], NULL, 10);
      qubit_id[1] = strtol(token[2], NULL, 10);
      if (qubit_num < qubit_id[0] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      if (qubit_num < qubit_id[1] + 1) ERR_RETURN(ERROR_CANT_READ_LINE, false);
      if (qubit_id[0] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
      if (qubit_id[1] < 0) ERR_RETURN(ERROR_OUT_OF_BOUND, false);
      if (qubit_id[0] == qubit_id[1]) ERR_RETURN(ERROR_SAME_QUBIT_ID, false);
      break;
    default:
      break;
    }

    if (!(qc_append_qgate(qc, kind, terminal_num, &para, qubit_id)))
      ERR_RETURN(ERROR_QC_APPEND_QGATE, false);
  }

  /* set cimage */
  if (!(qc_set_cimage(qc)))
    ERR_RETURN(ERROR_QC_SET_CIMAGE, false);
  
  free(line); line = NULL;
  fclose(fp);

  *qc_out = qc;
  
  SUC_RETURN(true);
}

void qc_free(QC* qc)
{
  if (qc != NULL) {
    if (qc->qgate != NULL) {
      free(qc->qgate); qc->qgate = NULL;
    }
    if (qc->cimage != NULL) {
      _cimage_free(qc->cimage); qc->cimage = NULL;
    }
    free(qc);
  }
}
