from src.voicechat.packets.Packet import Packet
from src.voicechat.packets.PacketId import PacketId


class ClientAcceptConnection(Packet):
    packet_id = PacketId.CLIENT_ACCEPT_CONNECTION
    magic: bytes = None

    def encodePayload(self):
        if not isinstance(self.magic, bytes):
            self.magic = self.magic.encode('utf-8')
        self.putMagic(self.magic)

