def patch_autobahn():
    import autobahn.websocket
    from cutf8validator.utf8validator import Utf8Validator
    autobahn.websocket.Utf8Validator = Utf8Validator

def patch_ws4py():
    import ws4py.streaming
    from cutf8validator.utf8validator import Utf8Validator
    ws4py.streaming.Utf8Validator = Utf8Validator
