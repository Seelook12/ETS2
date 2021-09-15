import mmap
import struct


## SDK 값
class SDKmmap:
    def __init__(self):
        self.mm = mmap.mmap(0, 1024, "Local\\SimTelemetryETS2")
        self.gameSteer = struct.unpack("f", self.mm[120:124])[0]
        self.userSteer = struct.unpack("f", self.mm[104:108])[0]
        self.speed = struct.unpack("f", self.mm[24:28])[0]
        self.gameBrake = struct.unpack("f",self.mm[128:132])[0]
        self.engineRpm = struct.unpack("f", self.mm[80:84])[0]

    def getspeed(self):
        self.speed = struct.unpack("f", self.mm[24:28])[0]
        return self.speed

    def getgameSteer(self):
        self.gameSteer = struct.unpack("f", self.mm[120:124])[0]
        return self.gameSteer

    def getgameBrake(self):
        self.gameBrake = struct.unpack("f", self.mm[128:132])[0]
        return self.gameBrake

    def getengineRpm(self):
        self.engineRpm = struct.unpack("f", self.mm[80:84])[0]
        return self.gameSteer


