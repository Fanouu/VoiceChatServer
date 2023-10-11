from src.voicechat.packets.Packet import Packet
from src.voicechat.packets.PacketId import PacketId


class AudioPacket(Packet):
    packet_id = PacketId.Audio
