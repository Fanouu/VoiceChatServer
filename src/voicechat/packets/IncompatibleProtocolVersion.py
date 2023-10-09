from src.voicechat.packets.Packet import Packet
from src.voicechat.packets.PacketId import PacketId


class IncompatibleProtocolVersion(Packet):
    packet_id = PacketId.INCOMPATIBLE_PROTOCOL_VERSION

    server_protocol_version: bytes = None
    magic: bytes = None

    def encode(self):
        self.putByte(self.server_protocol_version)
        self.putMagic(self.magic)