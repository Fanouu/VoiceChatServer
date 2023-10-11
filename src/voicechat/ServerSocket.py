import socket
from threading import Thread
from src.voicechat import Server
from src.voicechat.packets.Packet import Packet
from src.voicechat.packets.PacketId import PacketId
from src.voicechat.packets.UnconnectedPing import UnconnectedPing
from src.voicechat.packets.UnconnectedPong import UnconnectedPong
from src.voicechat.packets.ClientOpenConnection import ClientOpenConnection
from src.voicechat.packets.ClientOpenConnectionReply import ClientOpenConnectionReply
from src.voicechat.packets.PlayerUpdatePosition import PlayerUpdatePosition
from src.voicechat.client.Location import Location


class ServerSocket(Thread):
    socket = None

    ip = None
    port = None

    server = None

    running = None

    players: dict = {}

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

        if packetId == PacketId.PlayerUpdatePosition:
            packet = PlayerUpdatePosition(data)
            packet.decode()

            self.players[self.addressToStr(address)] = Location(packet.x, packet.y, packet.z, packet.world)
        if not self.server.getClientManager().getClient(address) is None:
            client = self.server.getClientManager().getClient(address)
            packet = Packet(data)
            packet.decode()
            client.onReceivePacket(packet)

        if packetId == PacketId.UNCONNECTED_PING:
            packet = UnconnectedPing(data)
            packet.decode()

            pong = UnconnectedPong()
            pong.client_timestamp = packet.client_timestamp
            pong.magic = packet.magic
            pong.encode()

            self.sendPacketTo(pong, address)
        if packetId == PacketId.CLIENT_OPEN_CONNECTION:
            packet = ClientOpenConnection(data)
            packet.decode()

            reply = ClientOpenConnectionReply()
            reply.magic = packet.magic
            reply.encode()

            self.server.getClientManager().addClient(address, packet.magic)
            self.sendPacketTo(reply, address)

    def addressToStr(self, address):
        return ":".join(self.server.clientManager.toSTR(address))