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
