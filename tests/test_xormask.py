from wsaccel.xormask import XorMaskerSimple

def test_xormasker():
    masker = XorMaskerSimple(b'\xf0\xf0\x0f\x0f')
    assert b'\xf0\xf0\x0f\x0f\xf0\xf0' == masker.process(b'\x00'*6)
    assert masker.pointer() == 6
    assert b'\x0f\x0f\xf0\xf0\x0f\x0f' == masker.process(b'\x00'*6)
    assert masker.pointer() == 12

