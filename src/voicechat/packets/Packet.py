import json
from src.voicechat.packets.Buffer import Buffer


class Packet(Buffer):
    packet_id = 0x00

    def decodeHeader(self):
        return self.readByte()

    def encodeHeader(self):
        self.putUnsignedByte(self.packet_id)

    def decode(self):
        self.decodeHeader()
        if hasattr(self, 'decodePayload'):
            self.decodePayload()

    def encode(self):
        self.encodeHeader()
        if hasattr(self, 'encodePayload'):
            self.encodePayload()

    def toDict(self):
        return {"data": self.data}
