from src.voicechat.packets.Packet import Packet
from src.voicechat.packets.PacketId import PacketId


class PlayerUpdatePosition(Packet):
    packet_id = PacketId.PlayerUpdatePosition

    x = None
    y = None
    z = None
    world = None

    def decodePayload(self):
        self.x = self.readUnsignedInt()
        self.y = self.readUnsignedInt()
        self.z = self.readUnsignedInt()
        self.world = self.readString()
