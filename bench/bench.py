#!/usr/bin/env python
###############################################################################
##
##  Copyright 2011,2012 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

from twisted.internet import reactor
from autobahn.twisted.websocket import (
    WebSocketClientFactory,
    WebSocketClientProtocol,
    connectWS,
    WebSocketServerFactory,
    WebSocketServerProtocol,
    listenWS,
)

import time

msg = b"hello world" * 1000

class EchoServerProtocol(WebSocketServerProtocol):

    def onMessage(self, msg, binary):
        self.sendMessage(msg, binary)

class EchoClientProtocol(WebSocketClientProtocol):

    def __init__(self):
        super().__init__()
        self.cnt = 0
        self.t_start = time.time()

    def sendHello(self):
        self.sendMessage(msg)

    def onOpen(self):
        self.sendHello()

    def onMessage(self, received, binary):
        #assert msg == received
        self.cnt += 1
        if self.cnt < 10000:
            self.sendHello()
        else:
            self.sendClose()
            print(time.time() - self.t_start)

    def onClose(self, *args):
        reactor.stop()
        return

def start_server():
    factory = WebSocketServerFactory("ws://127.0.0.1:9000")
    factory.protocol = EchoServerProtocol
    listenWS(factory)

def start_client():
    factory = WebSocketClientFactory('ws://127.0.0.1:9000')
    factory.protocol = EchoClientProtocol
    connectWS(factory)

if __name__ == '__main__':
    start_server()
    start_client()
    reactor.run()
