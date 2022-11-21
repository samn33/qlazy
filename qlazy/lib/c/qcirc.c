/*
 *  qcirc.c
 */

#include "qlazy.h"

bool qcirc_init(void** qcirc_out)
{
  QCirc* qcirc = NULL;
  
  if (!(qcirc = (QCirc*)malloc(sizeof(QCirc))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY,NULL);

  qcirc->qubit_num = 0;
  qcirc->cmem_num = 0;
  qcirc->gate_num = 0;
  qcirc->first = NULL;
  qcirc->last = NULL;

  if (!(tagtable_init(TAG_TABLE_SIZE, (void**)&(qcirc->tag_table))))
    ERR_RETURN(ERROR_TAGTABLE_INIT, false);

  *qcirc_out = qcirc;
  
  SUC_RETURN(true);
}

bool qcirc_copy(QCirc* qcirc_in, void** qcirc_out)
{
  QCirc*	qcirc = NULL;
  QGate*        gate  = NULL;

  if (qcirc_in == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (!(qcirc_init((void**)&qcirc))) ERR_RETURN(ERROR_QCIRC_INIT, false);

  /* copy gates */
  gate = qcirc_in->first;
  while (gate != NULL) {
    if (!(qcirc_append_gate(qcirc, gate->kind, gate->qid, gate->para, gate->c, gate->ctrl, gate->tag)))
      ERR_RETURN(ERROR_QCIRC_APPEND_GATE, false);
    gate = gate->next;
  }

  /* copy tag table */
  if (!(tagtable_merge(qcirc->tag_table, qcirc_in->tag_table))) {
      ERR_RETURN(ERROR_TAGTABLE_MERGE, false);
  }

  *qcirc_out = qcirc;

  SUC_RETURN(true);
}

bool qcirc_merge(QCirc* qcirc_L, QCirc* qcirc_R, void** qcirc_out)
{
  QCirc*	qcirc = NULL;
  QGate*        gate  = NULL;

  if ((qcirc_L == NULL) || (qcirc_R == NULL)) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  /* create NULL circuit (qcirc) */
  if (!(qcirc_init((void**)&qcirc))) ERR_RETURN(ERROR_QCIRC_INIT, NULL);

  if (qcirc_L->qubit_num > qcirc_R->qubit_num) qcirc->qubit_num = qcirc_L->qubit_num;
  else qcirc->qubit_num = qcirc_R->qubit_num;

  if (qcirc_L->cmem_num > qcirc_R->cmem_num) qcirc->cmem_num = qcirc_L->cmem_num;
  else qcirc->cmem_num = qcirc_R->cmem_num;

  /* append left */
  gate = qcirc_L->first;
  while (gate != NULL) {
    if (!(qcirc_append_gate(qcirc, gate->kind, gate->qid, gate->para, gate->c, gate->ctrl, gate->tag)))
      ERR_RETURN(ERROR_QCIRC_APPEND_GATE, NULL);
    gate = gate->next;
  }
  if (!(tagtable_merge(qcirc->tag_table, qcirc_L->tag_table))) {
      ERR_RETURN(ERROR_TAGTABLE_MERGE, false);
  }

  /* append right */
  gate = qcirc_R->first;
  while (gate != NULL) {
    if (!(qcirc_append_gate(qcirc, gate->kind, gate->qid, gate->para, gate->c, gate->ctrl, gate->tag)))
      ERR_RETURN(ERROR_QCIRC_APPEND_GATE, NULL);
    gate = gate->next;
  }
  if (!(tagtable_merge(qcirc->tag_table, qcirc_R->tag_table))) {
      ERR_RETURN(ERROR_TAGTABLE_MERGE, false);
  }

  *qcirc_out = qcirc;

  SUC_RETURN(true);
}

bool qcirc_merge_mutable(QCirc* qcirc_mut, QCirc* qcirc)
{
  QGate* gate  = NULL;

  if ((qcirc_mut == NULL) || (qcirc == NULL)) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (qcirc_mut->qubit_num < qcirc->qubit_num) qcirc_mut->qubit_num = qcirc->qubit_num;
  if (qcirc_mut->cmem_num < qcirc->cmem_num) qcirc_mut->cmem_num = qcirc->cmem_num;

  /* append gate */
  gate = qcirc->first;
  while (gate != NULL) {
    if (!(qcirc_append_gate(qcirc_mut, gate->kind, gate->qid, gate->para, gate->c, gate->ctrl, gate->tag)))
      ERR_RETURN(ERROR_QCIRC_APPEND_GATE, NULL);
    gate = gate->next;
  }

  /* merge tag table */
  if (!(tagtable_merge(qcirc_mut->tag_table, qcirc->tag_table))) {
      ERR_RETURN(ERROR_TAGTABLE_MERGE, false);
  }
  
  SUC_RETURN(true);
}

bool qcirc_is_equal(QCirc* qcirc_L, QCirc* qcirc_R, bool* ans)
{
  QGate*        gate_L = NULL;
  QGate*        gate_R = NULL;

  if ((qcirc_L == NULL) || (qcirc_R == NULL))
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if ((qcirc_L->qubit_num != qcirc_R->qubit_num) ||
      (qcirc_L->cmem_num != qcirc_R->cmem_num) ||
      (qcirc_L->gate_num != qcirc_R->gate_num)) {
    *ans = false;
    SUC_RETURN(true);
  }
  
  gate_L = qcirc_L->first;
  gate_R = qcirc_R->first;
  while ((gate_L != NULL) || (gate_R != NULL)) {
    if ((gate_L->kind != gate_R->kind) ||
	(gate_L->qid[0] != gate_R->qid[0]) ||
	(gate_L->qid[1] != gate_R->qid[1]) ||
	(gate_L->para[0] != gate_R->para[0]) ||
	(gate_L->para[1] != gate_R->para[1]) ||
	(gate_L->para[2] != gate_R->para[2]) ||
	(gate_L->c != gate_R->c) ||
	(gate_L->ctrl != gate_R->ctrl)) {
      *ans = false;
      SUC_RETURN(true);
    }
    gate_L = gate_L->next;
    gate_R = gate_R->next;
  }

  *ans = true;
  SUC_RETURN(true);
}

bool qcirc_is_unitary_only(QCirc* qcirc, bool* ans)
{
  QGate* gate = NULL;

  if (qcirc == NULL)
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  *ans = true;
  gate = qcirc->first;
  while (gate != NULL) {
    if (kind_is_unitary(gate->kind) == false) {
      *ans = false;
      break;
    }
    gate = gate->next;
  }

  SUC_RETURN(true);
}

bool qcirc_is_measurement_only(QCirc* qcirc, bool* ans)
{
  QGate* gate = NULL;

  if (qcirc == NULL)
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  *ans = true;
  gate = qcirc->first;
  while (gate != NULL) {
    if (kind_is_measurement(gate->kind) == false) {
      *ans = false;
      break;
    }
    gate = gate->next;
  }

  SUC_RETURN(true);
}

bool qcirc_append_gate(QCirc* qcirc, Kind kind, int* qid, double* para, int c, int ctrl, char* tag)
{
  QGate* qgate = NULL;
  int qid_size = 0;
  int para_size = 0;
  int i;
  
  if (qcirc == NULL ||
      (kind_is_measurement(kind) == false &&
       kind_is_reset(kind) == false && kind_is_unitary(kind) == false)) {
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }
  /* bell measurement is not supported */
  if (kind == MEASURE_BELL) {
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }

  /* set qgate */
  qid_size = kind_get_qid_size(kind);
  para_size = kind_get_para_size(kind);
  if (qid_size < 0) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  if (qid_size == 2 && qid[0] == qid[1]) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  if (para_size < 0) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (!(qgate = (QGate*)malloc(sizeof(QGate))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
  qgate->kind = kind;
  for (i=0; i<qid_size; i++) qgate->qid[i] = qid[i];
  for (i=qid_size; i<2; i++) qgate->qid[i] = -1;
  for (i=0; i<3; i++) qgate->para[i] = para[i];
  qgate->c = c;
  qgate->ctrl = ctrl;

  if (tag == NULL) {
    strcpy(qgate->tag, "");
  }
  else if (strlen(tag) > TAG_STRLEN) {
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }
  else {
    strcpy(qgate->tag, tag);
  }

  /* set tag table */
  if (strlen(qgate->tag) > 0) {
    if (!(tagtable_set_phase(qcirc->tag_table, qgate->tag, para[0])))
      ERR_RETURN(ERROR_TAGTABLE_SET_PHASE, false);
  }

  /* update qubit_num, cmem_num, gate_num */
  for (i=0; i<qid_size; i++) qcirc->qubit_num = MAX(qcirc->qubit_num, qgate->qid[i] + 1);
  if (qgate->c != -1) qcirc->cmem_num = MAX(qcirc->cmem_num, qgate->c + 1);
  if (qgate->ctrl != -1) qcirc->cmem_num = MAX(qcirc->cmem_num, qgate->ctrl + 1);
  qcirc->gate_num += 1;

  /* append qgate */
  if (qcirc->first == NULL) {
    qcirc->first = qcirc->last = qgate;
    qgate->prev = NULL;
    qgate->next = NULL;
  }
  else {
    qcirc->last->next = qgate;
    qgate->prev = qcirc->last;
    qgate->next = NULL;
    qcirc->last = qgate;
  }
  
  SUC_RETURN(true);
}

bool qcirc_kind_first(QCirc* qcirc, Kind* kind)
{
  if (qcirc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  if (qcirc->first == NULL) {
    *kind = NOT_A_GATE;
  }
  else {
    *kind = qcirc->first->kind;
  }

  SUC_RETURN(true);
}

static void _qcirc_update(QCirc* qcirc)
{
  QGate*	qgate	  = NULL;
  int		qubit_num = 0;
  int		cmem_num  = 0;
  int		gate_num  = 0;
  int		i;
  
  qgate = qcirc->first;
  while (qgate != NULL) {
    for (i=0; i<2; i++) qubit_num = MAX(qubit_num, qgate->qid[i] + 1);
    cmem_num = MAX(cmem_num, qgate->c + 1);
    cmem_num = MAX(cmem_num, qgate->ctrl + 1);
    gate_num += 1;
    qgate = qgate->next;
  }

  qcirc->qubit_num = qubit_num;
  qcirc->cmem_num = cmem_num;
  qcirc->gate_num = gate_num;
}

bool qcirc_pop_gate(QCirc* qcirc, Kind* kind, int* qid, double* para, int* c, int* ctrl,
		    char* tag, int* taglen)
{
  QGate*	ori_first;
  int		q_max = -1;
  int		c_max = -1;
  int           i;
  
  if (qcirc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  /* get first gate */
  *kind = qcirc->first->kind;
  memcpy(qid, qcirc->first->qid, sizeof(int) * 2);
  memcpy(para, qcirc->first->para, sizeof(double) * 3);
  *c = qcirc->first->c;
  *ctrl = qcirc->first->ctrl;
  strcpy(tag, qcirc->first->tag);
  *taglen = strlen(tag);

  /* free first gate (original) */
  ori_first = qcirc->first;
  qcirc->first = qcirc->first->next;
  free(ori_first); ori_first = NULL;

  /* update qubit_num, cmem_num, gate_num */
  for (i=0; i<2; i++) q_max = MAX(q_max, qid[i] + 1);
  c_max = MAX(c_max, *c);
  c_max = MAX(c_max, *ctrl);
  if ((q_max >= qcirc->qubit_num) || (c_max >= qcirc->cmem_num)) _qcirc_update(qcirc);
  else qcirc->gate_num -= 1;
  
  SUC_RETURN(true);
}

bool qcirc_decompose(QCirc* qcirc_in, void** qcirc_uonly_out, void** qcirc_mixed_out,
		     void** qcirc_monly_out)
{
  QCirc*	qcirc_uonly = NULL; /* unitary only */
  QCirc*	qcirc_monly = NULL; /* measurement only */
  QGate*	qgate	    = NULL;
  bool          uonly_flg;
  bool          monly_flg;

  if (qcirc_in == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (!(qcirc_init((void**)&qcirc_uonly))) ERR_RETURN(ERROR_QCIRC_INIT, false);
  if (!(qcirc_init((void**)&qcirc_monly))) ERR_RETURN(ERROR_QCIRC_INIT, false);

  /* qcirc_uonly */

  uonly_flg = false;
  qgate = qcirc_in->first;
  while (qgate != NULL) {
    if (kind_is_unitary(qgate->kind) == true) {
      uonly_flg = true;
      if (!(qcirc_append_gate(qcirc_uonly, qgate->kind, qgate->qid, qgate->para, qgate->c, qgate->ctrl, qgate->tag)))
	ERR_RETURN(ERROR_QCIRC_APPEND_GATE, false);
      *qcirc_uonly_out = qcirc_uonly;
    }
    else {
      if (uonly_flg == false) { /* 1st gate is non-uniary */
	qcirc_free(qcirc_uonly); qcirc_uonly = NULL;
	*qcirc_uonly_out = NULL;
	break;
      }
      uonly_flg = false;
      *qcirc_uonly_out = qcirc_uonly;
      break;
    }
    qgate = qgate->next;
  }

  if (qgate == NULL) { /* include unitary gates only -> return */
    qcirc_free(qcirc_monly); qcirc_monly = NULL;
    *qcirc_mixed_out = NULL;
    *qcirc_monly_out = NULL;
    
    SUC_RETURN(true);
  }

  /* qcirc_mixed, qcirc_monly */

  monly_flg = true;
  while (qgate != NULL) {
    if (kind_is_measurement(qgate->kind) == false) monly_flg = false;
    if (!(qcirc_append_gate(qcirc_monly, qgate->kind, qgate->qid, qgate->para, qgate->c, qgate->ctrl, qgate->tag)))
      ERR_RETURN(ERROR_QCIRC_APPEND_GATE, false);
    qgate = qgate->next;
  }

  if (monly_flg == true) { /* measurement only */
    *qcirc_mixed_out = NULL;
    *qcirc_monly_out = qcirc_monly;
  }
  else { /* mixed */
    *qcirc_mixed_out = qcirc_monly;
    *qcirc_monly_out = NULL;
  }
  
  SUC_RETURN(true);
}

/* set the tag and the phase */
bool qcirc_set_tag_phase(QCirc* qcirc, char* tag, double phase)
{
  double phs;

  if (qcirc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  /* check tag existance */
  if (!(qcirc_get_tag_phase(qcirc, tag, &phs)))
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (strlen(tag) > 0) {
    if (!(tagtable_set_phase(qcirc->tag_table, tag, phase)))
      ERR_RETURN(ERROR_TAGTABLE_SET_PHASE, false);
  }
  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }
  
  SUC_RETURN(true);
}

/* get a phase for the tag */
bool qcirc_get_tag_phase(QCirc* qcirc, char* tag, double* phase)
{
  if (qcirc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (strlen(tag) > 0) {
    if (!(tagtable_get_phase(qcirc->tag_table, tag, phase)))
      ERR_RETURN(ERROR_TAGTABLE_GET_PHASE, false);
  }
  else {
    ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  }
  
  SUC_RETURN(true);
}

bool qcirc_get_tag_info(QCirc* qcirc, int* tag_num, int* tag_strlen)
{
  char** tag_array = NULL;

  if (qcirc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (!(tagtable_get_tags(qcirc->tag_table, (void**)&tag_array, tag_num, tag_strlen)))
    ERR_RETURN(ERROR_TAGTABLE_GET_TAGS, false);

  free(tag_array[0]); tag_array[0] = NULL;
  free(tag_array); tag_array = NULL;

  SUC_RETURN(true);
}

bool qcirc_get_tag_buf(QCirc* qcirc, char* tag_buf)
/* suppose that the tag_buf memory is already allocated */
{
  char**	tag_array = NULL;
  int		tag_num;
  int		tag_strlen;
  int           i, pos;
  
  if (qcirc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (!(tagtable_get_tags(qcirc->tag_table, (void**)&tag_array, &tag_num, &tag_strlen)))
    ERR_RETURN(ERROR_TAGTABLE_GET_TAGS, false);

  pos = 0;
  for (i=0; i<tag_num; i++) {
    strcpy(tag_buf+pos, tag_array[i]);
    pos += (strlen(tag_array[i]) + 1);
  }

  free(tag_array[0]); tag_array[0] = NULL;
  free(tag_array); tag_array = NULL;

  SUC_RETURN(true);
}

bool qcirc_update_phases(QCirc* qcirc)
{
  QGate*	gate = NULL;
  double	phase;
 
  if (qcirc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
   
  gate = qcirc->first;
  while (gate != NULL) {
    if (strlen(gate->tag) > 0) {
      if (!(tagtable_get_phase(qcirc->tag_table, gate->tag, &phase)))
	ERR_RETURN(ERROR_TAGTABLE_GET_PHASE, false);
      gate->para[0] = phase;
    }
    gate = gate->next;
  }
   
  SUC_RETURN(true);
}

void qcirc_free(QCirc* qcirc)
{
  QGate* qgate = NULL;
  
  if (qcirc == NULL || qcirc->first == NULL) return;
  qgate = qcirc->first;
  
  while (qgate != NULL) {
    if (qgate->next == NULL) {
      free(qgate); qgate = NULL;
    }
    else {
      qgate = qgate->next;
      if (qgate->prev != NULL) {
	free(qgate->prev);
	qgate->prev = NULL;
      }
    }
  }

  free(qcirc); qcirc = NULL;
}
