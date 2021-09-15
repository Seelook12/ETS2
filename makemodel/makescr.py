import cv2
import numpy as np
import pandas as pd

x =[]
for i in range(1,20000):

    a = cv2.imread("./0901/frame-" + str(i) + ".jpg")
    if a is None:
        pass
    else:
        if a[0].mean()< 6:
            pass
        else:
            a = a[:, :980,:]
            a1 = a[370:,:,:]

            cv2.imwrite("./BGR/BGR0901-"+str(i)+".jpg",a1)

            cv2.imwrite('./HSV/HSV0901-'+str(i)+'.jpg',cv2.cvtColor(a1,cv2.COLOR_BGR2HSV))


