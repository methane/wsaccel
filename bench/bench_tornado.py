from __future__ import print_function

from tornado import ioloop, websocket, web

import time
import wsaccel

patched = 0
msg = b"hello world" * 100


class TornadoClient(object):
    def __init__(self, url):
        websocket.WebSocketConnect(url, callback=self.on_connect)
        self.url = url
        self.client = None
        self.cnt = 0
        self.started_at = time.time()

    def on_connect(self, client):
        self.client = client.result()
        self.client.on_message = self.on_received
        self.client.write_message(msg)

    def on_received(self, message):
        if not message:
            return
        #print("client received:", message[:20])
        self.cnt += 1
        if self.cnt < 1000:
            self.client.write_message(msg)
        else:
            print(self.cnt, time.time() - self.started_at)
            self.client.protocol.close()
            global patched
            if not patched:
                patched += 1
                wsaccel.patch_tornado()
                TornadoClient(self.url)

class EchoHandler(websocket.WebSocketHandler):
    def on_message(self, msg):
        #print("server received:", msg[:20])
        self.write_message(msg)

application = web.Application(
        [(r'/', EchoHandler)],
        debug=True,
        )

def main():
    application.listen(9000)
    TornadoClient("ws://127.0.0.1:9000")
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
