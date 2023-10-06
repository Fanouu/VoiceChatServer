from src.voicechat.packets.Packet import Packet
from src.voicechat.packets.PacketId import PacketId


class ClientAcceptConnection(Packet):
    packet_id = PacketId.CLIENT_ACCEPT_CONNECTION
