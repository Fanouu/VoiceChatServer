from src.voicechat.packets.Packet import Packet
from src.voicechat.packets.PacketId import PacketId


class ClientRequestConnection(Packet):
    packet_id = PacketId.CLIENT_REQUEST_CONNECTION

    client_protocol_version: bytes = None
    magic: bytes = None

    def decodePayload(self):
        self.client_protocol_version = self.readByte()
        self.magic = self.read_magic()
