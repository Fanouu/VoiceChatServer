from src.voicechat.packets.Packet import Packet
from src.voicechat.packets.PacketId import PacketId


class ClientRequestConnection(Packet):
    packet_id = PacketId.CLIENT_REQUEST_CONNECTION

    magic: bytes = None

    def decodePayload(self):
        self.magic = self.read_magic()
