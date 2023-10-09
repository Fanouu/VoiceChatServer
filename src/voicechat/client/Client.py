from src.voicechat.packets.Packet import Packet
from src.voicechat.Server import Server
from src.voicechat.packets.PacketId import PacketId
from src.voicechat.packets.ClientRequestConnection import ClientRequestConnection
from src.voicechat.packets.ClientAcceptConnection import ClientAcceptConnection
from src.voicechat.packets.IncompatibleProtocolVersion import IncompatibleProtocolVersion


class Client:
    address = None
    server: Server = None

    def __init__(self, server: Server, address: tuple):
        super().__init__()
        self.address = address
        self.server = server
        self.connected: bool = False

    def onReceivePacket(self, packet: Packet):
        packetId = packet.packet_id
        packetData = packet.data

        if packetId == PacketId.CLIENT_REQUEST_CONNECTION:
            clientRequest = ClientRequestConnection(packetData)
            clientRequest.decode()

            if not clientRequest.client_protocol_version == self.server.PROTOCOL_VERSION:
                reply = IncompatibleProtocolVersion()
                reply.server_protocol_version = self.server.PROTOCOL_VERSION
                reply.magic = clientRequest.magic
            else:
                reply = ClientAcceptConnection()
                reply.magic = clientRequest.magic
                reply.encode()

            self.sendPacket(reply)

    def sendPacket(self, packet: Packet):
        self.server.serversocket.sendPacketTo(packet, self.address)
