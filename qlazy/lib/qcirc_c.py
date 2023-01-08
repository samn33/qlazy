# -*- coding: utf-8 -*-
""" wrapper functions for QCirc """
import ctypes
from ctypes.util import find_library
import pathlib

import qlazy.config as cfg
from qlazy.util import get_lib_ext
from qlazy.QCirc import QCirc

lib = ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))

def qcirc_init():
    """ initialize QCirc object """

    qcirc = None
    c_qcirc = ctypes.c_void_p(qcirc)

    lib.qcirc_init.restype = ctypes.c_bool
    lib.qcirc_init.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.qcirc_init(c_qcirc)

    if ret is False:
        raise ValueError("can't initialize QCirc object.")

    return c_qcirc

def qcirc_copy(qc):
    """ copy QCirc object """

    qcirc = None
    c_qcirc = ctypes.c_void_p(qcirc)

    lib.qcirc_copy.restype = ctypes.c_bool
    lib.qcirc_copy.argtypes = [ctypes.POINTER(QCirc),
                                    ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.qcirc_copy(ctypes.byref(qc), c_qcirc)

    if ret is False:
        raise ValueError("can't copy QCirc object.")

    return c_qcirc

def qcirc_merge(qc_L, qc_R):
    """ merge QCirc objects """

    qcirc = None
    c_qcirc = ctypes.c_void_p(qcirc)

    lib.qcirc_merge.restype = ctypes.c_bool
    lib.qcirc_merge.argtypes = [ctypes.POINTER(QCirc), ctypes.POINTER(QCirc),
                                     ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.qcirc_merge(ctypes.byref(qc_L), ctypes.byref(qc_R), c_qcirc)

    if ret is False:
        raise ValueError("can't merge QCirc objects.")

    return c_qcirc

def qcirc_merge_mutable(qc_mut, qc):
    """ merge QCirc objects (mutable) """

    lib.qcirc_merge.restype = ctypes.c_bool
    lib.qcirc_merge.argtypes = [ctypes.POINTER(QCirc), ctypes.POINTER(QCirc)]
    ret = lib.qcirc_merge_mutable(ctypes.byref(qc_mut), ctypes.byref(qc))

    if ret is False:
        raise ValueError("can't merge QCirc objects.")

def qcirc_is_equal(qc_L, qc_R):
    """ determine if 2 QCirc objects are equal or not """

    ans = True
    c_ans = ctypes.c_bool(ans)

    lib.qcirc_is_equal.restype = ctypes.c_bool
    lib.qcirc_is_equal.argtypes = [ctypes.POINTER(QCirc), ctypes.POINTER(QCirc),
                                        ctypes.POINTER(ctypes.c_bool)]
    ret = lib.qcirc_is_equal(ctypes.byref(qc_L), ctypes.byref(qc_R), ctypes.byref(c_ans))

    if ret is False:
        raise ValueError("can't determine equal or not.")

    ans = c_ans.value
    return ans

def qcirc_append_gate(qcirc, kind, qid, para, c, ctrl, tag):
    """ append gate to the QCirc objects """

    if para is None:
        para = [0.0, 0.0, 1.0]  # [phase, gphase, factor]
    if c is None:
        c = -1
    if ctrl is None:
        ctrl = -1
    if tag is None:
        tag = ""

    qid_num = len(qid)
    para_num = len(para)
    IntArray = ctypes.c_int * qid_num
    DoubleArray = ctypes.c_double * para_num
    c_qid = IntArray(*qid)
    c_para = DoubleArray(*para)
    c_tag = tag.encode('utf-8')

    lib.qcirc_append_gate.restype = ctypes.c_bool
    lib.qcirc_append_gate.argtypes = [ctypes.POINTER(QCirc), ctypes.c_int, IntArray,
                                      DoubleArray, ctypes.c_int, ctypes.c_int,
                                      ctypes.c_char_p]
    ret = lib.qcirc_append_gate(ctypes.byref(qcirc), ctypes.c_int(kind), c_qid, c_para,
                                ctypes.c_int(c), ctypes.c_int(ctrl), c_tag)

    if ret is False:
        raise ValueError("can't append quantum gate.")

def qcirc_kind_first(qc):
    """ get 1st gate kind of the quantum circuit """

    kind = 0
    c_kind = ctypes.c_int(kind)

    lib.qcirc_kind_first.restype = ctypes.c_bool
    lib.qcirc_kind_first.argtypes = [ctypes.POINTER(QCirc), ctypes.POINTER(ctypes.c_int)]
    ret = lib.qcirc_kind_first(ctypes.byref(qc), ctypes.byref(c_kind))

    if ret is False:
        raise ValueError("can't get 1st gate kind.")

    kind = c_kind.value

    if kind == cfg.NOT_A_GATE:
        kind = None

    return kind

def qcirc_pop_gate(qc):
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
    tag = '0' * cfg.TAG_STRLEN
    c_tag = tag.encode('utf-8')
    taglen = 0
    c_taglen = ctypes.c_int(taglen)

    lib.qcirc_pop_gate.restype = ctypes.c_bool
    lib.qcirc_pop_gate.argtypes = [ctypes.POINTER(QCirc), ctypes.POINTER(ctypes.c_int),
                                   ctypes.POINTER(ctypes.c_int),
                                   ctypes.POINTER(ctypes.c_double),
                                   ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
                                   ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]

    ret = lib.qcirc_pop_gate(ctypes.byref(qc), ctypes.byref(c_kind), c_qid, c_para,
                             ctypes.byref(c_c), ctypes.byref(c_ctrl), c_tag, ctypes.byref(c_taglen))

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

    tag = c_tag.decode('utf-8')
    taglen = c_taglen.value
    if taglen == 0:
        tag = ""
    else:
        tag = tag[:taglen]

    return (kind, qid, para, c, ctrl, tag)

def qcirc_set_params(qcirc, params):
    """ set params """

    lib.qcirc_set_tag_phase.restype = ctypes.c_bool
    lib.qcirc_set_tag_phase.argtypes = [ctypes.POINTER(QCirc), ctypes.c_char_p, ctypes.c_double]
    
    for tag, phase in params.items():
        c_tag = tag.encode('utf-8')
        c_phase = ctypes.c_double(phase)
        ret = lib.qcirc_set_tag_phase(ctypes.byref(qcirc), c_tag, c_phase)
        if ret is False:
            raise ValueError("can't set tag:{}, phase:{}.".format(tag, phase))
        
    lib.qcirc_update_phases.restype = ctypes.c_bool
    lib.qcirc_update_phases.argtypes = [ctypes.POINTER(QCirc)]

    ret = lib.qcirc_update_phases(ctypes.byref(qcirc))

    if ret is False:
        raise ValueError("can't update phases.")

def qcirc_get_tag_phase(qcirc, tag):
    """ get phase for the tag """

    lib.qcirc_get_tag_phase.restype = ctypes.c_bool
    lib.qcirc_get_tag_phase.argtypes = [ctypes.POINTER(QCirc), ctypes.c_char_p,
                                        ctypes.POINTER(ctypes.c_double)]

    c_tag = tag.encode('utf-8')
    phase = 0.0
    c_phase = ctypes.c_double(phase)
    ret = lib.qcirc_get_tag_phase(ctypes.byref(qcirc), c_tag, ctypes.byref(c_phase))

    if ret is False:
        raise ValueError("can't get param (= phase) for the tag: {}.".format(tag))

    phase = c_phase.value

    return phase

def qcirc_get_tag_list(qcirc):
    """ get tag_list """

    tag_num = 0
    c_tag_num = ctypes.c_int(tag_num)
    tag_strlen = 0
    c_tag_strlen = ctypes.c_int(tag_strlen)

    lib.qcirc_get_tag_info.restype = ctypes.c_bool
    lib.qcirc_get_tag_info.argtypes = [ctypes.POINTER(QCirc), ctypes.POINTER(ctypes.c_int),
                                       ctypes.POINTER(ctypes.c_int)]

    ret = lib.qcirc_get_tag_info(ctypes.byref(qcirc), c_tag_num, c_tag_strlen)
    if ret is False:
        raise ValueError("can't get tag info.")

    tag_num = c_tag_num.value
    tag_strlen = c_tag_strlen.value

    tag_buf = '0' * tag_num * tag_strlen
    c_tag_buf = tag_buf.encode('utf-8')
    
    lib.qcirc_get_tag_buf.restype = ctypes.c_bool
    lib.qcirc_get_tag_buf.argtypes = [ctypes.POINTER(QCirc), ctypes.POINTER(ctypes.c_char)]

    ret = lib.qcirc_get_tag_buf(ctypes.byref(qcirc), c_tag_buf)
    if ret is False:
        raise ValueError("can't get tag info.")

    tag_byte_list = c_tag_buf.split(b'\x00')
    tag_list = []
    for i in range(tag_num):
        tag_list.append(tag_byte_list[i].decode('utf-8'))

    return tag_list

def qcirc_free(qcirc):
    """ free memory of the QCirc object """

    lib.qcirc_free.argtypes = [ctypes.POINTER(QCirc)]
    lib.qcirc_free(ctypes.byref(qcirc))
