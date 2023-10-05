import socket
from threading import Thread
from src.voicechat import Server

class ServerSocket(Thread):
    socket = None

    ip = None
    port = None

    server: Server.Server = None

    running = None

    def __init__(self, ip, port, server):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.SOL_UDP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.server = server

        self.ip = ip
        self.port = port

    def start(self) -> None:
        super().start()
        self.running = True

    def stop(self) -> None:
        self.running = False

    def run(self) -> None:
        self.socket.bind((self.ip, self.port))
        while self.running:
            data, clientAddress = self.socket.recvfrom(65535)
            self.onRun(data, clientAddress)

    def onRun(self, data, address):
        pass