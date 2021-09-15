import cv2
import numpy as np
import model



mask = np.zeros(shape=(700, 1281), dtype=np.uint8)
mm = np.array([[0, 698], [0, 600], [584, 370], [890, 420], [980, 490], [980, 698]])
cv2.fillPoly(mask, [mm], (255, 255, 255))

k = np.array([[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0]], np.uint8)
k1 = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], np.uint8)


frame = cv2.imread('wwww.jpg')

HSV = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
rr = cv2.inRange(HSV, (0, 0, 210), (255, 40, 255))

erode1 = cv2.erode(gray, k, iterations=9)
erode = cv2.subtract(gray, erode1)

r1 = cv2.dilate(rr, k1, iterations=3)


c = cv2.bitwise_and(erode, erode, mask=r1)
d = cv2.Canny(c, 130, 180, apertureSize=3)
d1 = cv2.bitwise_and(d, d, mask=mask)



line1 = cv2.HoughLines(d1, 1, np.pi / 180, 90)

if line1 is None:
    n = 0
else:
    n = len(line1)
c = 0
c1 = 0
r = []
l = []
for i in range(n):
    if 0.1 < line1[i, 0, 1] < 1.3:
        c += 1
        if c >= 3:
            pass
        else:
            rho = line1[i, 0, 0]
            th = line1[i, 0, 1]

            p = [rho, th]
            l.append(p)
    elif 1.9 < line1[i, 0, 1] < 3.1:
        c1 += 1
        if c1 >= 3:
            pass
        else:
            rho = line1[i, 0, 0]
            th = line1[i, 0, 1]

            q = [rho, th]
            r.append(q)

print('r =',r)
print('l =',l)



if len(l) <= 1:
    pass
else:
    for i in range(len(l)):
        rho, theta = l[i]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 2000 * (-b))
        y1 = int(y0 + 2000 * (a))
        x2 = int(x0 - 2000 * (-b))
        y2 = int(y0 - 2000 * (a))

        cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

if len(r) <= 1:
    pass
else:
    for i in range(len(r)):
        rho, theta = r[i]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 2000 * (-b))
        y1 = int(y0 + 2000 * (a))
        x2 = int(x0 - 2000 * (-b))
        y2 = int(y0 - 2000 * (a))

        cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)




cv2.imshow('a',frame)
cv2.waitKey(0)





# l,r = self.huplines(d1)
#
#
# center = self.lll(l,r)
# frame1 = self.hupdrow(l,r,frame)