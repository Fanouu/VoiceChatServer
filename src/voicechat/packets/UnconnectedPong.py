from src.voicechat.packets.PacketId import PacketId
from src.voicechat.packets.Packet import Packet


class UnconnectedPong(Packet):
    packet_id = PacketId.UNCONNECTED_PONG

    client_timestamp: int = None
    magic: bytes = None

    def encodePayload(self):
        self.putLong(self.client_timestamp)
        if not isinstance(self.magic, bytes):
            self.magic = self.magic.encode('utf-8')
        self.putMagic(self.magic)
