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

    def __init__(self, mask):
        cdef Py_buffer view
        cdef char* msk
        PyObject_GetBuffer(mask, &view, PyBUF_SIMPLE)
        assert view.len == 4
        msk = <char*>view.buf
        self.ptr = 0
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
        cdef Py_buffer view
        cdef int i
        PyObject_GetBuffer(data, &view, PyBUF_SIMPLE)
        dlen = view.len
        cdata = <char*>view.buf

        payload = PyBytes_FromStringAndSize(NULL, dlen)
        out = <char*>PyBytes_AsString(payload)

        for i in range(dlen):
            out[i] = cdata[i] ^ self.mask[self.ptr & 3]
            self.ptr += 1
        return payload
