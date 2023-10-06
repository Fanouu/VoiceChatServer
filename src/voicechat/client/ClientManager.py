from src.voicechat.client.Client import Client


class ClientException(Exception):
    pass


class ClientManager:
    server = None

    clients = {}

    def __init__(self, Server: server):
        self.server = Server

    def getClients(self) -> dict[Client]:
        return self.clients

    def getClient(self, address: tuple) -> Client | None:
        addressSTR = ":".join(self.toSTR(address))
        if addressSTR in self.clients:
            return self.clients[addressSTR]
        else:
            return None

    def getClientByAddressStr(self, addressStr):
        if addressStr in self.clients:
            return self.clients[addressStr]
        else:
            return None

    def addClient(self, address: tuple, mtu_size):
        addressSTR = ":".join(self.toSTR(address))
        if not self.getClient(address) is None:
            raise ClientException("§cClient with this address: " + addressSTR + " can be registered, because it is already registered !")
        self.clients[addressSTR] = Client(self.server, address, mtu_size)

    def removeClient(self, address: tuple):
        print("Remove Client")
        addressSTR = ":".join(self.toSTR(address))
        if self.getClient(address) is None:
            raise ClientException("No Client with this address: " + addressSTR + " registered !")
        del self.clients[addressSTR]

    def toSTR(self, array: tuple):
        new_tuple = ()
        index = 0
        for i in array:
            y = list(new_tuple)
            y.append(str(i))
            new_tuple = tuple(y)
        index += 1
        return new_tuple