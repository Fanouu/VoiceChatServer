from src.voicechat.packets.Packet import Packet
from src.voicechat.Server import Server
from src.voicechat.packets.PacketId import PacketId
from src.voicechat.packets.ClientRequestConnection import ClientRequestConnection
from src.voicechat.packets.ClientAcceptConnection import ClientAcceptConnection
from src.voicechat.packets.IncompatibleProtocolVersion import IncompatibleProtocolVersion
from src.voicechat.packets.ServerAbortConnection import ServerAbortConnection
from time import time
from src.voicechat.client.Location import Location
from src.voicechat.packets.PlayerUpdatePosition import PlayerUpdatePosition
from src.voicechat.packets.AudioPacket import AudioPacket


class Client:
    address = None
    server: Server = None
    channel_uuid = None

    def __init__(self, server: Server, address: tuple, magic):
        super().__init__()
        self.address = address
        self.server = server
        self.connected: bool = False
        self.last_receive_packet: float = time()
        self.magic = magic
        self.location: Location = Location()

    def getLocation(self) -> Location:
        return self.location

    def setLocation(self, location:Location):
        self.location = location

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
        if packetId == PacketId.PlayerUpdatePosition:
            packet = PlayerUpdatePosition(packetData)
            packet.decode()

            self.location = Location(packet.x, packet.y, packet.z, packet.world)

        if packetId == PacketId.Audio:
            for client in self.server.getClientManager().getClients():
                packet = AudioPacket(packetData)
                if self.getLocation().distance(client.getLocation()) <= self.server.MAX_DISTANCE:
                    client.sendPacket(packet)

    def onUpdate(self):
        if time() - self.last_receive_packet <= 0:
            self.disconnect()
            self.close()

    def sendPacket(self, packet: Packet):
        self.server.serversocket.sendPacketTo(packet, self.address)


    def disconnect(self, reason=1):
        packet = ServerAbortConnection()
        packet.reason = reason
        packet.encode()

        self.sendPacket(packet)

    def close(self):
        self.server.getClientManager().removeClient(self.address)
