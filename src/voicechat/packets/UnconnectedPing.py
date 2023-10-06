from src.voicechat.packets.Packet import Packet
from src.voicechat.packets.PacketId import PacketId
class UnconnectedPing(Packet):
    packet_id = PacketId.UNCONNECTED_PING