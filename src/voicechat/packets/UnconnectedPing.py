from src.voicechat.packets.Packet import Packet
from src.voicechat.packets.PacketId import PacketId


class UnconnectedPing(Packet):
    packet_id = PacketId.UNCONNECTED_PING

    client_timestamp: int = None
    magic: bytes = None

    def read_long(self):
        if len(self.data) < 8:
            raise ValueError("Insufficient data to read a long value")

        long_value = int.from_bytes(self.data[:8], byteorder='big', signed=False)
        self.data = self.data[8:]

        return long_value

    def decodePayload(self):
        self.client_timestamp = self.read_long()
        self.magic = self.read_magic()

    def toDict(self) -> dict:
        dict = super().toDict()
        dict["magic"] = self.magic
        dict["client_timestamp"] = self.client_timestamp

        return dict
