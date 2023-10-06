import socket
from threading import Thread
from src.voicechat import Server
from src.voicechat.packets.Packet import Packet
from src.voicechat.packets.PacketId import PacketId
from src.voicechat.packets.UnconnectedPing import UnconnectedPing
from src.voicechat.packets.UnconnectedPong import UnconnectedPong


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

    def sendPacketTo(self, packet: Packet, address):
        self.socket.sendto(packet.data, address)

    def onRun(self, data, address):
        packetId = data[0]

        if not self.server.getClientManager().getClient(address) is None:
            client = self.server.getClientManager().getClient(address)
            client.onReceivePacket(data)

        if packetId == PacketId.UNCONNECTED_PING:
            packet = UnconnectedPing(data)
            packet.decode()

            pong = UnconnectedPong()
            pong.client_timestamp = packet.client_timestamp
            pong.magic = packet.magic
            pong.encode()

            self.sendPacketTo(pong, address)
