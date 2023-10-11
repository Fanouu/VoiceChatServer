from src.voicechat.packets.Packet import Packet
from src.voicechat.packets.PacketId import PacketId

class ServerAbortConnection(Packet):
    packet_id = PacketId.ServerAbortConnection

    reason = None

    def encodePayload(self):
        self.putString(self.reason)