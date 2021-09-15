import cv2
import numpy as np
import pandas as pd

z3 = np.zeros(shape=(330,980),dtype=np.uint8)
mmm = np.array([[140,224],[159,224],[342,124],[327,126]])
mmm1 = np.array([[756,100],[776,100],[886,193],[855,193]])
cv2.fillPoly(z3,[mmm,mmm1],(255,255,255))

z = np.zeros(shape=(330,980),dtype=np.uint8)
m = np.array([[378,150],[393,151],[182,299],[159,298]])
m1 = np.array([[946,183],[977,183],[825,87],[805,87]])
cv2.fillPoly(z,[m,m1],(255,255,255))

z1 = np.zeros(shape=(330, 980), dtype=np.uint8)
mm = np.array([[0, 328],[0,230], [584, 0], [890, 50], [980, 120], [980, 328]])
cv2.fillPoly(z1, [mm], (255, 255, 255))

# z1 = np.zeros(shape=(700, 1281), dtype=np.uint8)
# mm = np.array([[0, 698],[0,600], [584, 370], [890, 420], [980, 490], [980, 698]])
# cv2.fillPoly(z1, [mm], (255, 255, 255))


# z1 = np.zeros(shape=(330,980),dtype=np.uint8)
# mm = np.array([[330,150],[630,150],[410,300],[110,300]])
#
# cv2.fillPoly(z1,[mm],(255,255,255))

# z1 = np.zeros(shape=(700, 1281), dtype=np.uint8)
# mm = np.array([[0, 698],[0,600], [384, 430], [890, 420], [980, 490], [980, 698]])
#
# cv2.fillPoly(z1,[mm],(255,255,255))



# z1 = np.zeros(shape=(330,980), dtype=np.uint8)
# mm = np.array([[0, 328],[0,230], [384, 60], [890, 50], [980, 120], [980, 328]])
#
# cv2.fillPoly(z1,[mm],(255,255,255))

# z1 = np.zeros(shape=(330,980),dtype=np.uint8)
# mm = np.array([[0,0],[0,90],[450,0]])
# mm1 = np.array([[980,100],[770,0],[980,0]])
# cv2.fillPoly(z1,[mm,mm1],(255,255,255))
# z1 = z1 -255

mean = 3.9

Smean1 = []
Vmean1 = []
Sstd1 = []
Vstd1 = []
S1 =[]
V1 = []
title1 = []


for k in range(1,20000):
    title = "HSV8m15-" + str(k) + ".jpg"
    ah = cv2.imread("./HSV/HSV8m15-" + str(k) + ".jpg")

    if ah is None:
        pass
    else:
        for i in range(3,23):
            i = int(i)
            a1 = cv2.inRange(ah, (0, 0, 250-10*i), (255, 255, 255))
            a2 = cv2.bitwise_and(a1,a1,mask=z)
            if a2.mean() > mean:
                for j in range(3,23):
                    aa1 = cv2.inRange(ah, (0, 0, 0), (255, 0 + 10*j, 255))
                    aa2 = cv2.bitwise_and(aa1,aa1,mask=z)


                    if aa2.mean() > mean:
                        S = ((0 + 10*j)/10) -3
                        V =((250 - 10*i)/10) -3

                        k = cv2.bitwise_and(ah,ah,mask=z1)
                        x = k[:, :, 1]
                        y = k[:, :, 2]

                        Smean = int(x.mean()*100)
                        Vmean = int(y.mean()*100)
                        Sstd = int(np.std(x)*100)
                        Vstd =int(np.std(y)*100)

                        Smean1.append(Smean)
                        Vmean1.append(Vmean)
                        Sstd1.append(Sstd)
                        Vstd1.append(Vstd)
                        S1.append(S)
                        V1.append(V)
                        title1.append(title)
                        break
                break


a = pd.DataFrame({'Smean': Smean1,
                  'Vmean': Vmean1,
                  'Sstd' : Sstd1,
                  'Vstd' : Vstd1,
                  'S': S1,
                  'V': V1},index=title1)


a.to_csv('./Data/newf3.csv')


