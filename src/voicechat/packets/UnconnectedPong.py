from src.voicechat.packets.PacketId import PacketId
from src.voicechat.packets.Packet import Packet

class UnconnectedPong(Packet):
    packet_id = PacketId.UNCONNECTED_PONG