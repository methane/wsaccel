# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import gevent
import gevent.pywsgi

from ws4py.server.geventserver import WebSocketWSGIApplication, WSGIServer
from ws4py.websocket import EchoWebSocket
from ws4py.client.geventclient import WebSocketClient

import time
import wsaccel
patched = False
#wsaccel.patch_ws4py()

msg = b'Hello World' * 100


class EchoWebSocketApplication(object):
    def __init__(self):
        self.ws = WebSocketWSGIApplication(handler_cls=EchoWebSocket)

    def __call__(self, environ, start_response):
        """
        Good ol' WSGI application. This is a simple demo
        so I tried to stay away from dependencies.
        """
        return self.ws(environ, start_response)

class EchoClient(WebSocketClient):
    def opened(self):
        self.cnt = 0
        self.started_at = time.time()
        self.send(msg)

    def closed(self, code, reason):
        print(("Closed down", code, reason))

    def received_message(self, m):
        self.cnt += 1
        if self.cnt < 1000:
            self.send(msg)
        else:
            self.close(reason='Bye bye')
            print(time.time() - self.started_at)
            global patched
            if not patched:
                patched = True
                wsaccel.patch_ws4py()
                start_client()
            else:
                server.stop()

def start_client():
    ws = EchoClient('ws://127.0.0.1:9000/ws')
    ws.connect()

if __name__ == '__main__':
    server = WSGIServer(('127.0.0.1', 9000), EchoWebSocketApplication())
    server.start()
    start_client()
    while not server.closed:
        gevent.sleep(1)
