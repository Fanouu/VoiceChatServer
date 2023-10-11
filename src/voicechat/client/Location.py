import math

class Location:

    def __init__(self, x: float = 0, y: float = 0, z: float = 0, world: str = "default"):
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.world: str = world

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def getWorld(self):
        return self.world

    def distance(self, location) -> float:
        return math.sqrt(self.distanceSquared(location))

    def distanceSquared(self, location) -> float:
        if not self.world == location.world:
            return 0.0
        return ((self.x - location.x) ** 2) + ((self.y - location.y) ** 2) + ((self.z - location.z) ** 2)

