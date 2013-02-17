def patch_autobahn():
    import autobahn.websocket
    from wsaccel.utf8validator import Utf8Validator
    autobahn.websocket.Utf8Validator = Utf8Validator
    from wsaccel.xormask import XorMaskerNull, XorMaskerSimple
    autobahn.XorMaskerNull = XorMaskerNull
    autobahn.XorMaskerSimple = XorMaskerSimple
    autobahn.XorMaskerShifted1 = XorMaskerSimple

def patch_ws4py():
    import ws4py.streaming
    from wsaccel.utf8validator import Utf8Validator
    ws4py.streaming.Utf8Validator = Utf8Validator
