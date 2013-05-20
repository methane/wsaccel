from cpython.buffer cimport *
from cpython.bytes cimport *

cdef extern from "Python.h":
    cdef int PyObject_AsReadBuffer(object o, const void** buff, Py_ssize_t* buf_len) except -1

cdef class XorMaskerNull:

    cdef Py_ssize_t ptr

    def __init__(self, mask=None):
        self.ptr = 0

    def pointer(self):
        return self.ptr

    def reset(self):
        self.ptr = 0

    def process(self, data):
        self.ptr += len(data)
        return data


cdef class XorMaskerSimple:

    cdef Py_ssize_t ptr
    cdef object _maskobj
    cdef char mask[4]

    def __init__(self, mask):
        cdef const char* msk
        cdef Py_ssize_t msk_len
        self.ptr = 0
        self._maskobj = mask  # keep object
        PyObject_AsReadBuffer(mask, <const void**>&msk, &msk_len)
        if msk_len != 4:
            raise ValueError("mask should be 4byte.")
        self.mask[0] = msk[0]
        self.mask[1] = msk[1]
        self.mask[2] = msk[2]
        self.mask[3] = msk[3]

    def pointer(self):
        return self.ptr

    def reset(self):
        self.ptr = 0

    def process(self, data):
        cdef Py_ssize_t dlen
        cdef char* cdata
        cdef char* out
        cdef int i
        PyObject_AsReadBuffer(data, <const void**>&cdata, &dlen)

        payload = PyBytes_FromStringAndSize(NULL, dlen)
        out = <char*>PyBytes_AsString(payload)

        for i in range(dlen):
            out[i] = cdata[i] ^ self.mask[self.ptr & 3]
            self.ptr += 1
        return payload


def createXorMasker(mask, len=None):
    return XorMaskerSimple(mask)
