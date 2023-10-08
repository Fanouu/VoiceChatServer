from src.voicechat.packets.Packet import Packet
from src.voicechat.Server import Server


class Client:

    address = None
    server: Server = None

    def __init__(self, server: Server, address: tuple):
        super().__init__()
        self.address = address
        self.server = server

    def onReceivePacket(self, packet: Packet):
        pass