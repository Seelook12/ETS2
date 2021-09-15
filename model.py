import cv2
import numpy as np
from tensorflow.keras.models import load_model

## inrange 함수에 들어갈 S V 값을 모델을 통해 구함
class models:
    def __init__(self):

        ## 6번 시점 모델
        self.Smodel = load_model('my_modelS7.h5')
        self.Vmodel = load_model('my_modelV7.h5')

        ## 1번 시점 모델
        self.Smodel1 = load_model('model1S.h5')
        self.Vmodel1 = load_model('model1V.h5')

        self.mask = np.zeros(shape=(700, 1281), dtype=np.uint8)
        mm = np.array([[0, 698], [0, 600], [584, 370], [890, 420], [980, 490], [980, 698]])
        cv2.fillPoly(self.mask ,[mm],(255,255,255))

        self.mask1 = np.zeros(shape=(700, 1281), dtype=np.uint8)
        m = np.array([[900, 466], [521, 429], [599, 330], [709, 330]])
        cv2.fillPoly(self.mask1, [m], (255, 255, 255))

    ## 6번시점 스크린샷을 받아서 모델어 넣어서 inrange 함수 이미지 반환
    def view6(self, frame):
        HSV = frame
        da = cv2.bitwise_and(HSV, HSV, mask=self.mask)
        #
        Smean = int(da[370:, :980, 1].mean() * 100)
        Vmean = int(da[370:, :980, 2].mean() * 100)
        Sstd = int(np.std(da[370:, :980, 1]) * 100)
        Vstd = int(np.std(da[370:, :980, 2]) * 100)
        #
        data = np.zeros(shape=(1, 4))
        data[0, 0] = Smean
        data[0, 1] = Vmean
        data[0, 2] = Sstd
        data[0, 3] = Vstd

        S = int(np.argmax(self.Smodel.predict(data)))
        V = int(np.argmax(self.Vmodel.predict(data)))

        S = (S + 4) * 10
        V = (V + 2) * 10
        r = cv2.inRange(HSV, (0, 0, V), (255, S, 255))
        print('S :', S)
        print('V : ', V)
        return r

    ## 1번 시점
    def view1(self,frame):
        HSV =frame
        da = cv2.bitwise_and(HSV, HSV, mask=self.mask1)
        Smean = int(da[370:, :980, 1].mean() * 1000)
        Vmean = int(da[370:, :980, 2].mean() * 1000)
        Sstd = int(np.std(da[370:, :980, 1]) * 1000)
        Vstd = int(np.std(da[370:, :980, 2]) * 1000)
        #
        data = np.zeros(shape=(1, 4))
        data[0, 0] = Smean
        data[0, 1] = Vmean
        data[0, 2] = Sstd
        data[0, 3] = Vstd

        S = int(np.argmax(self.Smodel1.predict(data)))
        V = int(np.argmax(self.Vmodel1.predict(data)))

        S = (S + 1) * 10
        V = (V + 1) * 10
        r = cv2.inRange(HSV, (0, 0, V), (255, S, 255))
        return r



## d는 케니언 엣지 이미지 , center1는 차선의 중심과 차 중심간의 이격 , self.img_frame는 원본이미지에 허프 직선표시한 이미지 반환
class line:
    def __init__(self):
        self.model = models()

        self.mask = np.zeros(shape=(700, 1281), dtype=np.uint8)
        mm = np.array([[0, 698], [0, 600], [584, 370], [890, 420], [980, 490], [980, 698]])
        cv2.fillPoly(self.mask ,[mm],(255,255,255))

        self.mask1 = np.zeros(shape=(700, 1281), dtype=np.uint8)
        m = np.array([[900, 466], [521, 429], [599, 330], [709, 330]])
        cv2.fillPoly(self.mask1, [m], (255, 255, 255))

        self.k = np.array([[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0]], np.uint8)
        self.k1 = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], np.uint8)


    def view6(self,frame):
        HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rr = self.model.view6(HSV)

        erode1 = cv2.erode(gray, self.k, iterations=9)
        erode = cv2.subtract(gray, erode1)

        r1 = cv2.dilate(rr, self.k1, iterations=3)
        c = cv2.bitwise_and(erode, erode, mask=r1)
        d = cv2.Canny(c, 130, 180, apertureSize=3)
        d1 = cv2.bitwise_and(d, d, mask=self.mask)
        l,r = self.huplines(d1)
        center = self.lll(l,r)
        frame1 = self.hupdrow(l,r,frame)

        return d ,center,frame1

    def view1(self,frame):
        HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rr = self.model.view6(HSV)

        erode1 = cv2.erode(gray, self.k, iterations=9)
        erode = cv2.subtract(gray, erode1)

        r1 = cv2.dilate(rr, self.k1, iterations=3)
        c = cv2.bitwise_and(erode, erode, mask=r1)
        d = cv2.Canny(c, 130, 180, apertureSize=3)
        d1 = cv2.bitwise_and(d, d, mask=self.mask1)
        l, r = self.huplines(d1)
        center = self.lll(l, r)
        frame1 = self.hupdrow(l, r, frame)

        return d, center, frame1


    def lll(self,l,r):

        lft = []
        rht = []

        ## self.huplines 에서 받은 왼쪽 오른쪽 차선 직선 방정식을 가지고 세로가 600위치일때 가로 좌표를 각각 구함
        if len(l) < 1:
            pass
        else:
            for i in range(len(l)):
                rho, theta = l[i]
                a = np.cos(theta)
                b = np.sin(theta)
                c = (rho - 600 * b) / a
                lft.append(c)

        if len(r) < 1:
            pass
        else:
            for i in range(len(r)):
                rho, theta = r[i]
                a = np.cos(theta)
                b = np.sin(theta)
                c = (rho - 600 * b) / a
                rht.append(c)



        ## 위에서 받은 값을 바탕으로 차선의 중심을 구하고 차량의 중심선인 640 에서 빼서 이격정도를 구하여 반환함
        if len(r) > 1 and len(l) > 1:
            lft1 = max(lft)
            rht1 = min(rht)

            center = (rht1 - lft1)/2 + lft1
            center1 = 640 - center




        elif len(r) > 1 and len(l) < 1:

            rht1 = min(rht) -370
            center1 = 640 -rht1



        elif len(r) < 1 and len(l) > 1:


            lft1 = max(lft) + 370
            center1 = 640 - lft1


        else:
            center1 = 0

        return center1


    ## self.huplines 에서 받은 왼쪽 오른쪽 차선 직선 방정식을 가지고 원본 화면에 직선을 그림후 반환함
    def hupdrow(self,l,r,frame):
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

        return frame


    ## 허프변한 함수사용후 반환된 값을 차선의 각도를 이용해 오른쪽 왼쪽 각각 최대 2개씩 r,l에 저장함
    def huplines(self,d1):
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


        return l,r
