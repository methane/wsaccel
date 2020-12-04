from cpython.buffer cimport *
from cpython.bytes cimport *

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
    cdef char mask[4]

    def __init__(self, const unsigned char[:] mask):
        self.ptr = 0
        if len(mask) != 4:
            raise ValueError("mask should be 4byte.")
        self.mask[0] = mask[0]
        self.mask[1] = mask[1]
        self.mask[2] = mask[2]
        self.mask[3] = mask[3]

    def pointer(self):
        return self.ptr

    def reset(self):
        self.ptr = 0

    def process(self, const unsigned char[:] data):
        cdef Py_ssize_t dlen = len(data)
        cdef Py_ssize_t i
        cdef char* out

        payload = PyBytes_FromStringAndSize(NULL, dlen)
        out = <char*>PyBytes_AsString(payload)

        for i in range(dlen):
            out[i] = data[i] ^ self.mask[self.ptr & 3]
            self.ptr += 1
        return payload


def createXorMasker(mask, len=None):
    return XorMaskerSimple(mask)
