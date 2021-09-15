import SDK
import cv2
import numpy as np


class handle:


    def gethandle(self):
        self.steer = SDK.SDKmmap()
        self.x = 180 - self.steer.getgameSteer() * 180
        a = np.zeros(shape=(200, 200, 3), dtype=np.uint8)
        a = a + 255
        cv2.circle(a, (100, 100), 100, (0, 100, 255), -1)
        dd = cv2.ellipse(a, (100, 100), (100, 100), 90, 180, self.x, (0, 0, 0), -1)

        return dd


