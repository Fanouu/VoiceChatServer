class PacketId:
    DISCONNECT = 0x00
    UNCONNECTED_PING = 0x01
    UNCONNECTED_PONG = 0x02
    CLIENT_ACCEPT_CONNECTION = 0x03
    CLIENT_REQUEST_CONNECTION = 0x04
    CLIENT_OPEN_CONNECTION = 0x05
    ClientOpenConnectionReply = 0x06
    IncompatibleProtocolVersion = 0x07
    ServerAbortConnection = 0x08
    PlayerUpdatePosition = 0x09
    Audio = 0xa
