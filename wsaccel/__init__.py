__version__ = '0.6.2'

def patch_autobahn():
    from wsaccel.utf8validator import Utf8Validator
    from wsaccel.xormask import XorMaskerNull, XorMaskerSimple
    import autobahn.websocket

    autobahn.websocket.Utf8Validator = Utf8Validator
    autobahn.websocket.XorMaskerNull = XorMaskerNull
    autobahn.websocket.XorMaskerSimple = XorMaskerSimple
    autobahn.websocket.XorMaskerShifted1 = XorMaskerSimple


def patch_ws4py():
    from wsaccel.utf8validator import Utf8Validator
    from wsaccel.xormask import XorMaskerSimple
    from ws4py import streaming, framing

    streaming.Utf8Validator = Utf8Validator

    def mask(self, data):
        if self.masking_key:
            masker = XorMaskerSimple(self.masking_key)
            return masker.process(data)
        return data

    framing.Frame.mask = mask
    framing.Frame.unmask = mask


def patch_tornado():
    from tornado.websocket import WebSocketProtocol13
    from wsaccel.xormask import XorMaskerSimple

    def _apply_mask(self, mask, data):
        masker = XorMaskerSimple(mask)
        return masker.process(data)

    WebSocketProtocol13._apply_mask = _apply_mask
