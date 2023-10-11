from src.voicechat.packets.Packet import Packet
from src.voicechat.packets.PacketId import PacketId

class ClientOpenConnection(Packet):
    packet_id = PacketId.CLIENT_OPEN_CONNECTION

    magic: bytes = None

    def decodePayload(self):
        self.magic = self.read_magic()