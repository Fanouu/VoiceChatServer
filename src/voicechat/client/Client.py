from src.voicechat.packets.Packet import Packet

class Client:

    address = None
    def __init__(self, address):
        super().__init__()
        self.address = address

    def onReceivePacket(self, packet: Packet):
        pass