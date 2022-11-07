# -*- coding: utf-8 -*-
""" wrapper functions for QCirc """
import ctypes
from ctypes.util import find_library
import pathlib

import qlazy.config as cfg
from qlazy.util import get_lib_ext
from qlazy.QCircBase import QCircBase

lib = ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))
libc = ctypes.CDLL(find_library("c"), mode=ctypes.RTLD_GLOBAL)

def qcirc_base_init():
    """ initialize QCirc object """

    qcirc = None
    c_qcirc = ctypes.c_void_p(qcirc)

    lib.qcirc_base_init.restype = ctypes.c_bool
    lib.qcirc_base_init.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.qcirc_base_init(c_qcirc)

    if ret is False:
        raise ValueError("can't initialize QCirc object.")

    return c_qcirc

def qcirc_base_copy(qc):
    """ copy QCirc object """

    qcirc = None
    c_qcirc = ctypes.c_void_p(qcirc)

    lib.qcirc_base_copy.restype = ctypes.c_bool
    lib.qcirc_base_copy.argtypes = [ctypes.POINTER(QCircBase),
                                    ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.qcirc_base_copy(ctypes.byref(qc), c_qcirc)

    if ret is False:
        raise ValueError("can't copy QCirc object.")

    return c_qcirc

def qcirc_base_merge(qc_L, qc_R):
    """ merge QCirc objects """

    qcirc = None
    c_qcirc = ctypes.c_void_p(qcirc)

    lib.qcirc_base_merge.restype = ctypes.c_bool
    lib.qcirc_base_merge.argtypes = [ctypes.POINTER(QCircBase), ctypes.POINTER(QCircBase),
                                     ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.qcirc_base_merge(ctypes.byref(qc_L), ctypes.byref(qc_R), c_qcirc)

    if ret is False:
        raise ValueError("can't merge QCirc objects.")

    return c_qcirc

def qcirc_base_merge_mutable(qc_mut, qc):
    """ merge QCirc objects (mutable) """

    lib.qcirc_base_merge.restype = ctypes.c_bool
    lib.qcirc_base_merge.argtypes = [ctypes.POINTER(QCircBase), ctypes.POINTER(QCircBase)]
    ret = lib.qcirc_base_merge_mutable(ctypes.byref(qc_mut), ctypes.byref(qc))

    if ret is False:
        raise ValueError("can't merge QCirc objects.")

def qcirc_base_is_equal(qc_L, qc_R):
    """ determine if 2 QCirc objects are equal or not """

    ans = True
    c_ans = ctypes.c_bool(ans)

    lib.qcirc_base_is_equal.restype = ctypes.c_bool
    lib.qcirc_base_is_equal.argtypes = [ctypes.POINTER(QCircBase), ctypes.POINTER(QCircBase),
                                        ctypes.POINTER(ctypes.c_bool)]
    ret = lib.qcirc_base_is_equal(ctypes.byref(qc_L), ctypes.byref(qc_R), ctypes.byref(c_ans))

    if ret is False:
        raise ValueError("can't determine equal or not.")

    ans = c_ans.value
    return ans

def qcirc_base_append_gate(qcirc, kind, qid, para, c, ctrl):
    """ append gate to the QCirc objects """

    if para is None:
        para = [0.0, 0.0, 0.0]
    if c is None:
        c = -1
    if ctrl is None:
        ctrl = -1

    qid_num = len(qid)
    para_num = len(para)
    IntArray = ctypes.c_int * qid_num
    DoubleArray = ctypes.c_double * para_num
    c_qid = IntArray(*qid)
    c_para = DoubleArray(*para)

    lib.qcirc_base_append_gate.restype = ctypes.c_bool
    lib.qcirc_base_append_gate.argtypes = [ctypes.POINTER(QCircBase), ctypes.c_int, IntArray,
                                           DoubleArray, ctypes.c_int, ctypes.c_int]
    ret = lib.qcirc_base_append_gate(ctypes.byref(qcirc), ctypes.c_int(kind), c_qid, c_para,
                                     ctypes.c_int(c), ctypes.c_int(ctrl))

    if ret is False:
        raise ValueError("can't append quantum gate.")

def qcirc_base_kind_first(qc):
    """ get 1st gate kind of the quantum circuit """

    kind = 0
    c_kind = ctypes.c_int(kind)

    lib.qcirc_base_kind_first.restype = ctypes.c_bool
    lib.qcirc_base_kind_first.argtypes = [ctypes.POINTER(QCircBase), ctypes.POINTER(ctypes.c_int)]
    ret = lib.qcirc_base_kind_first(ctypes.byref(qc), ctypes.byref(c_kind))

    if ret is False:
        raise ValueError("can't get 1st gate kind.")

    kind = c_kind.value

    if kind == cfg.NOT_A_GATE:
        kind = None

    return kind

def qcirc_base_pop_gate(qc):
    """ pop gate of the quantum circuit """

    kind = 0
    c_kind = ctypes.c_int(kind)
    qid = [0] * 2
    IntArray = ctypes.c_int * 2
    c_qid = IntArray(*qid)
    para = [0.0] * 3
    DoubleArray = ctypes.c_double * 3
    c_para = DoubleArray(*para)
    c = -1
    c_c = ctypes.c_int(c)
    ctrl = -1
    c_ctrl = ctypes.c_int(ctrl)

    lib.qcirc_base_pop_gate.restype = ctypes.c_bool
    lib.qcirc_base_pop_gate.argtypes = [ctypes.POINTER(QCircBase), ctypes.POINTER(ctypes.c_int),
                                        ctypes.POINTER(ctypes.c_int),
                                        ctypes.POINTER(ctypes.c_double),
                                        ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]

    ret = lib.qcirc_base_pop_gate(ctypes.byref(qc), ctypes.byref(c_kind), c_qid, c_para,
                                  ctypes.byref(c_c), ctypes.byref(c_ctrl))

    if ret is False:
        raise ValueError("can't pop gate.")

    kind = c_kind.value
    qid = [c_qid[i] for i in range(2)]
    para = [c_para[i] for i in range(3)]
    c = c_c.value
    ctrl = c_ctrl.value

    if c == -1:
        c = None
    if ctrl == -1:
        ctrl = None

    return (kind, qid, para, c, ctrl)

def qcirc_base_set_phase_list(qcirc, phase_list):
    """ set phase list """

    phase_num = len(phase_list)
    DoubleArray = ctypes.c_double * phase_num
    c_phase_list = DoubleArray(*phase_list)

    lib.qcirc_base_set_phase_list.restype = ctypes.c_bool
    lib.qcirc_base_set_phase_list.argtypes = [ctypes.POINTER(QCircBase), DoubleArray]
    ret = lib.qcirc_base_set_phase_list(ctypes.byref(qcirc), c_phase_list)

    if ret is False:
        raise ValueError("can't set phase list.")

def qcirc_base_free(qcirc):
    """ free memory of the QCirc object """

    lib.qcirc_base_free.argtypes = [ctypes.POINTER(QCircBase)]
    lib.qcirc_base_free(ctypes.byref(qcirc))
