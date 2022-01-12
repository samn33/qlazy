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

  *qcirc_out = qcirc;
  
  SUC_RETURN(true);
}

bool qcirc_copy(QCirc* qcirc_in, void** qcirc_out)
{
  QCirc*	qcirc = NULL;
  QGate*        gate  = NULL;

  if (qcirc_in == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (!(qcirc_init((void**)&qcirc))) ERR_RETURN(ERROR_QCIRC_INIT, NULL);

  gate = qcirc_in->first;
  while (gate != NULL) {
    if (!(qcirc_append_gate(qcirc, gate->kind, gate->qid, gate->para, gate->c, gate->ctrl)))
      ERR_RETURN(ERROR_QCIRC_APPEND_GATE, NULL);
    gate = gate->next;
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
    if (!(qcirc_append_gate(qcirc, gate->kind, gate->qid, gate->para, gate->c, gate->ctrl)))
      ERR_RETURN(ERROR_QCIRC_APPEND_GATE, NULL);
    gate = gate->next;
  }

  /* append right */
  gate = qcirc_R->first;
  while (gate != NULL) {
    if (!(qcirc_append_gate(qcirc, gate->kind, gate->qid, gate->para, gate->c, gate->ctrl)))
      ERR_RETURN(ERROR_QCIRC_APPEND_GATE, NULL);
    gate = gate->next;
  }

  *qcirc_out = qcirc;

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

bool qcirc_append_gate(QCirc* qcirc, Kind kind, int* qid, double* para, int c, int ctrl)
{
  QGate* qgate = NULL;
  int qid_size = 0;
  int para_size = 0;
  
  if (qcirc == NULL ||
      (kind_is_measurement(kind) == false &&
       kind_is_reset(kind) == false && kind_is_unitary(kind) == false)) {
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }
  /* bell measurement is not supported */
  if (kind == MEASURE_BELL) {
    ERR_RETURN(ERROR_INVALID_ARGUMENT,false);
  }

  /* set qgate */
  qid_size = kind_get_qid_size(kind);
  para_size = kind_get_para_size(kind);
  if (qid_size < 0) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);
  if (para_size < 0) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  if (!(qgate = (QGate*)malloc(sizeof(QGate))))
    ERR_RETURN(ERROR_CANT_ALLOC_MEMORY, false);
  qgate->kind = kind;
  for (int i=0; i<qid_size; i++) qgate->qid[i] = qid[i];
  for (int i=qid_size; i<2; i++) qgate->qid[i] = -1;
  for (int i=0; i<para_size; i++) qgate->para[i] = para[i];
  for (int i=para_size; i<3; i++) qgate->para[i] = 0.0;
  qgate->c = c;
  qgate->ctrl = ctrl;

  /* update qubit_num, cmem_num, gate_num */
  for (int i=0; i<qid_size; i++) qcirc->qubit_num = MAX(qcirc->qubit_num, qgate->qid[i] + 1);
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
  
  qgate = qcirc->first;
  while (qgate != NULL) {
    for (int i=0; i<2; i++) qubit_num = MAX(qubit_num, qgate->qid[i] + 1);
    cmem_num = MAX(cmem_num, qgate->c + 1);
    cmem_num = MAX(cmem_num, qgate->ctrl + 1);
    gate_num += 1;
    qgate = qgate->next;
  }

  qcirc->qubit_num = qubit_num;
  qcirc->cmem_num = cmem_num;
  qcirc->gate_num = gate_num;
}

bool qcirc_pop_gate(QCirc* qcirc, Kind* kind, int* qid, double* para, int* c, int* ctrl)
{
  QGate*	ori_first;
  int		q_max = -1;
  int		c_max = -1;
  
  if (qcirc == NULL) ERR_RETURN(ERROR_INVALID_ARGUMENT, false);

  /* get first gate */
  *kind = qcirc->first->kind;
  memcpy(qid, qcirc->first->qid, sizeof(int) * 2);
  memcpy(para, qcirc->first->para, sizeof(double) * 3);
  *c = qcirc->first->c;
  *ctrl = qcirc->first->ctrl;

  /* free first gate (original) */
  ori_first = qcirc->first;
  qcirc->first = qcirc->first->next;
  free(ori_first); ori_first = NULL;

  /* update qubit_num, cmem_num, gate_num */
  for (int i=0; i<2; i++) q_max = MAX(q_max, qid[i] + 1);
  c_max = MAX(c_max, *c);
  c_max = MAX(c_max, *ctrl);
  if ((q_max >= qcirc->qubit_num) || (c_max >= qcirc->cmem_num)) _qcirc_update(qcirc);
  else qcirc->gate_num -= 1;
  
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
      free(qgate->prev); qgate->prev = NULL;
    }
  }

  free(qcirc); qcirc = NULL;
}
