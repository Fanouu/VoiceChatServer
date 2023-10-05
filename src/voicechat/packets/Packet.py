import json


class Packet:
    packet_id = 0
    data = None
    body = None

    def encode(self):
        data = {'packetId': self.packet_id, 'packetData': self.data}
        self.body = json.dumps(data)

    def decode(self):
        body = json.loads(self.body)
        self.packet_id = body['packetId']
        self.data = body['packetData']
