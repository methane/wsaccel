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
        assert len(mask) == 4
        assert isinstance(mask, (bytes, bytearray))
        self.ptr = 0
        self.mask[0] = mask[0]
        self.mask[1] = mask[1]
        self.mask[2] = mask[2]
        self.mask[3] = mask[3]

    def pointer(self):
        return self.ptr

    def reset(self):
        self.ptr = 0

    def process(self, data):
        cdef Py_ssize_t dlen, ptr
        cdef char* cdata
        cdef char* out
        cdef Py_buffer view
        cdef int i
        PyObject_GetBuffer(data, &view, PyBUF_SIMPLE)
        dlen = view.len
        cdata = <char*>view.buf

        payload = PyBytes_FromStringAndSize(NULL, dlen)
        out = <char*>PyBytes_AsString(payload)
        ptr = self.ptr

        for i in range(dlen):
            payload[i] = cdata[i] ^ self.mask[ptr & 3]
        self.ptr = ptr
        return payload

