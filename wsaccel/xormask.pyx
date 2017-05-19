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

        payload = PyBytes_FromStringAndSize(cdata, dlen)
        out = <char*>PyBytes_AsString(payload)
        # Assumption: PyBytes_FromStringAndSize returns at least 4-bytes aligned memory.
        assert <size_t>out & 3 == 0

        cdef int start = self.ptr & 3
        cdef char *mask = [
            self.mask[(start + 0) & 3],
            self.mask[(start + 1) & 3],
            self.mask[(start + 2) & 3],
            self.mask[(start + 3) & 3],
        ]

        for i in range(dlen / 4):
            (<unsigned *>out)[i] ^= (<unsigned *>mask)[0]
        for i in range(dlen - (dlen & 3), dlen):
            out[i] ^= mask[i & 3]
        self.ptr += dlen
        return payload


def createXorMasker(mask, len=None):
    return XorMaskerSimple(mask)
