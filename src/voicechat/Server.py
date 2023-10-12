from typing import Type

from src.voicechat import ServerSocket
from src.voicechat import Logger
from src.voicechat.Logger import Logger
from src.voicechat.client.ClientManager import ClientManager


class Server:
    serversocket = None
    logger = None
    clientManager = None
    PROTOCOL_VERSION = 1
    MAX_DISTANCE = 50

    def __init__(self):
        self.logger = Logger.Logger
        self.clientManager = ClientManager(self)
        self.serversocket = ServerSocket.ServerSocket('0.0.0.0', '19132', self)

        self.serversocket.start()

    def getLogger(self) -> Type[Logger]:
        return self.logger

    def getClientManager(self) -> ClientManager:
        return self.clientManager
