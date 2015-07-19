#coding: utf-8
import wsaccel.utf8validator

def test_validate():
    v = wsaccel.utf8validator.Utf8Validator()
    x = u"Hello-µ@ßöäüàá-UTF-8!!".encode('utf-8')  # taken from case 6.2.1
    assert v.validate(x) == (True, True, 29, 29)
