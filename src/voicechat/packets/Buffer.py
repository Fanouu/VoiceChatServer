import struct

class BinaryDataException(Exception):
    pass


class Buffer:
    data = b''
    offset = 0

    BYTE_SIZE = 1
    BOOL_SIZE = 1
    SHORT_SIZE = 2
    INT_SIZE = 4
    LONG_SIZE = 8
    FLOAT_SIZE = 4
    DOUBLE_SIZE = 8

    def __init__(self, data=b'', offset=0):
        self.data = data
        self.offset = offset
    def feos(self):
        return bool(len(self.data) <= self.offset)

    def get(self, pos):
        if not self.feos():
            self.offset += pos
            return self.data[self.offset - pos:self.offset]
        else:
            raise BinaryDataException(
                f"Not enough bytes left in buffer: need {pos}, have {len(self.data) - self.offset}")

    def getRemaining(self):
        return self.get(len(self.data) - self.offset)

    def readVarInt(self) -> int:
        value: int = 0
        for i in range(0, 35, 7):
            if self.feos():
                raise Exception("Data position exceeded")
            number: int = self.readUnsignedbyte()
            value |= ((number & 0x7f) << i)
            if (number & 0x80) == 0:
                return value
        raise Exception("VarInt is too big")

    def putVarInt(self, value: int) -> None:
        data: bytes = b""
        value &= 0xffffffff
        for i in range(0, 5):
            to_write: int = value & 0x7f
            value >>= 7
            if value != 0:
                self.putUnsignedByte(to_write | 0x80)
            else:
                self.putUnsignedByte(to_write)
                break

    def add(self, value):
        if not isinstance(value, bytes):
            value = bytes(str(value), 'utf-8')
        self.data += bytearray(value)

    def readByte(self):
        return struct.unpack('b', self.get(self.BYTE_SIZE))[0]

    def putByte(self, value):
        if not isinstance(value, bytes):
            data = str(value).encode()
        self.add(struct.pack('b', int(value)))

    def readBool(self):
        return struct.unpack('?', self.get(self.BOOL_SIZE))[0]

    def putBool(self, value):
        self.add(struct.pack('?', value))

    def readUnsignedbyte(self):
        return struct.unpack('B', self.get(1))[0]

    def putUnsignedByte(self, value):
        #if not isinstance(value, bytes) or not isinstance(value, int):
        #    value = value.encode('utf-8')
        self.add(struct.pack('B', value))

    def putShort(self, value):
        self.add(struct.pack('>h', value))

    def readShort(self):
        return struct.unpack('>h', self.get(self.SHORT_SIZE))[0]

    def putUnsignedShort(self, value):
        self.add(struct.pack('>H', value))

    def readUnsignedShort(self):
        return struct.unpack('>H', self.get(self.SHORT_SIZE))[0]

    def putInt(self, value):
        self.add(struct.pack('>i', value))

    def readInt(self):
        return struct.unpack('>i', self.get(self.INT_SIZE))[0]

    def putUnsignedInt(self, value):
        self.add(struct.pack('>I', value))

    def readUnsignedInt(self):
        return struct.unpack('>I', self.get(self.INT_SIZE))[0]

    def readString(self):
        length = self.readShort()
        return self.get(length).decode('utf-8')

    def putString(self, value):
        self.putShort(len(value))
        if not isinstance(value, bytes):
            value = value.encode('utf-8')
        self.add(value)

    def read_magic(self):
        if len(self.data) - self.offset < 16:
            raise BinaryDataException('End of buffer')
        return self.get(16)

    def putMagic(self, value=b'00ffff00fefefefefdfdfdfd12345678'):
        if not isinstance(value, bytes):
            value = value.encode('utf-8')
        self.add(value)

    def readUnsignedInt24le(self):
        return struct.unpack("<I", self.get(3) + b'\x00')[0]

    def putUnsignedInt24le(self, value):
        self.add(struct.pack("<I", value)[:3])

    def readLong(self):
        return struct.unpack('>q', self.get(self.LONG_SIZE))[0]

    def putLong(self, value):
        self.add(struct.pack('>q', value))

    def readUnsignedlong(self):
        return struct.unpack('>Q', self.get(self.LONG_SIZE))[0]

    def putUnsignedlong(self, value):
        self.add(struct.pack('>Q', value))

    def putUnsignedTriad_le(self, value: int):
        self.add(struct.pack("<I", value)[:3])

    def readUnsignedTriad_le(self):
        return struct.unpack("<I", self.get(3) + b"\x00")[0]

    def readAddress(self):
        ipv = self.readUnsignedbyte()
        if ipv == 4:
            hostname_parts = []
            for part in range(4):
                hostname_parts.append(str(~self.readByte() & 0xff))
            hostname = ".".join(hostname_parts)
            port = self.readUnsignedShort()
            return hostname, port, ipv
        else:
            raise BinaryDataException('IP version is not 4, ip version is:' + str(ipv))

    def putAddress(self, addr: str, port: int, version: int = 4):
        if version == 4:
            self.putUnsignedByte(version)
            for s in str(addr).split("."):
                self.putUnsignedByte(int(s) & 0xff)
            self.putUnsignedShort(port)