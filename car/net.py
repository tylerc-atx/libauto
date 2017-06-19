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
           'start_frame_stream_server', 'connect_to_console_server']


from twisted.internet import reactor, protocol, threads
from twisted.protocols import basic

from threading import Thread


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


def start_tcp_client(factory, address, port):
    def connect_client():
        reactor.connectTCP(address, port, factory)
    reactor.callFromThread(connect_client)


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

        def send_img_buffer(self, jpg_buffer):
            header = ('--frame\r\n'
                      'Content-Type: image/jpeg\r\n'
                      'Content-Length: {}\r\n\r\n').format(len(jpg_buffer)).encode()
            jpg_buffer = header + jpg_buffer + b'\r\n'
            for client in self.clients:
                client.transport.write(jpg_buffer)

    factory = MultipartStreamerFactory()

    port = 1025
    start_tcp_server(factory, port)

    def submit_frame(jpg_buffer):
        reactor.callFromThread(factory.send_img_buffer, jpg_buffer)

    return port, submit_frame


def connect_to_console_server():
    class ConsoleClientProtocol(protocol.Protocol):
        def __init__(self, factory):
            self.factory = factory

        def connectionMade(self):
            self.transport.setTcpNoDelay(True)
            for data in self.factory.content:
                self.transport.write(data)
            self.factory.content = []
            self.factory.protocol = self
            self.factory = None

    class ConsoleClientFactory(protocol.ClientFactory):
        def __init__(self):
            self.content = []
            self.protocol = None

        def buildProtocol(self, addr):
            return ConsoleClientProtocol(self)

        def _send(self, data):
            if not self.protocol:
                self.content.append(data)
            else:
                self.protocol.transport.write(data)

        def send(self, data):
            reactor.callFromThread(self._send, data)

    factory = ConsoleClientFactory()
    start_tcp_client(factory, "localhost", 1024)
    binary_send_func = factory.send

    class Writable:
        def write(self, text):
            chunk = text.encode('utf-8')
            chunk_type = 1
            binary_send_func(chunk_type.to_bytes(1, byteorder='big'))
            chunk_len = len(chunk)
            binary_send_func(chunk_len.to_bytes(4, byteorder='big'))
            binary_send_func(chunk)
        def flush(self):
            pass

    return Writable()

