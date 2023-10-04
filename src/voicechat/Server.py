from typing import Type

from src.voicechat import ServerSocket
from src.voicechat import Logger
from src.voicechat.Logger import Logger


class Server:
    serversocket = None
    logger = None

    def __init__(self):
        self.logger = Logger.Logger
        self.serversocket = ServerSocket.ServerSocket('0.0.0.0', '19132', self)

        self.serversocket.start()

    def getLogger(self) -> Type[Logger]:
        return self.logger