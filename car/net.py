###############################################################################
#
# Copyright (c) 2017 AutoAuto, LLC
# ALL RIGHTS RESERVED
#
# Use of this library, in source or binary form, is prohibited without written
# approval from AutoAuto, LLC.
#
###############################################################################

"""
Hacky Twisted code.
"""

__all__ = ['start_reactor_thread', 'stop_reactor_thread',
           'start_frame_stream_server']


from twisted.internet import reactor, protocol, threads
from twisted.protocols import basic

from threading import Thread

import cv2


def start_reactor_thread():
    def run_reactor():
        reactor.run(installSignalHandlers=0)
    if 'reactorThread' not in globals():
        global reactorThread
        reactorThread = Thread(target=run_reactor)
        reactorThread.daemon = True
        reactorThread.start()


def stop_reactor_thread():
    def stop_reactor():
        reactor.stop()
    threads.blockingCallFromThread(reactor, stop_reactor)
    reactorThread.join()


def start_tcp_server(factory, port):
    def listen():
        reactor.listenTCP(port, factory)
    reactor.callFromThread(listen)


def start_frame_stream_server():
    """
    Starts a frame streaming server and returns the port it is running on
    plus a callable to post new frames.
    """
    class MultipartStreamerProtocol(basic.LineReceiver):
        def __init__(self, factory):
            self.factory = factory

        def connectionMade(self):
            # don't add yet because we want to wait for the http header to come in
            self.transport.setTcpNoDelay(True)

        def connectionLost(self, reason):
            if self in self.factory.clients:
                self.factory.clients.remove(self)

        def lineReceived(self, line):
            if line == b'':   # end of http headers
                self.transport.write("HTTP/1.1 200 OK\r\n".encode())
                self.transport.write("Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n".encode())
                self.factory.clients.add(self)

    class MultipartStreamerFactory(protocol.Factory):
        def __init__(self):
            self.clients = set()

        def buildProtocol(self, addr):
            return MultipartStreamerProtocol(self)

        def send_img_buffer(self, data):
            header = ('--frame\r\n'
                      'Content-Type: image/jpeg\r\n'
                      'Content-Length: {}\r\n\r\n').format(len(data)).encode()
            data = header + data + b'\r\n'
            for client in self.clients:
                client.transport.write(data)

    factory = MultipartStreamerFactory()

    port = 1025
    start_tcp_server(factory, port)

    def submit_frame(frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        data = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 20])[1].tobytes()
        reactor.callFromThread(factory.send_img_buffer, data)

    return port, submit_frame

