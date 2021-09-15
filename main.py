
# -*- coding: utf-8 -*-

import time
from PyQt5 import QtCore,  QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import QLabel
from time import sleep
import threading
import cv2
import pyautogui
import pydirectinput
from pywinauto.application import Application
import SDK
import model
import steer
import numpy as np



class Ui_Dialog(object):
    def __init__(self):
        self.mask = np.zeros(shape=(700, 1281), dtype=np.uint8)
        mm = np.array([[0, 698], [0, 600], [584, 370], [890, 420], [980, 490], [980, 698]])
        cv2.fillPoly(self.mask ,[mm],(255,255,255))

        self.mask1 = np.zeros(shape=(700, 1281), dtype=np.uint8)
        m = np.array([[900, 466], [521, 429], [599, 330], [709, 330]])
        cv2.fillPoly(self.mask1, [m], (255, 255, 255))

        self.mmap = SDK.SDKmmap()
        self.line1 = model.line()
        self.steer = steer.handle()

        self.k = np.array([[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0]], np.uint8)
        self.k1 = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], np.uint8)
        self.rr = 1
        self.c1 = 0
        self.line = cv2.imread('../eurotruck_line/line.jpg')

        self.spd = 0
        self.speed = 0
        self.runnig = False

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.move(1281,0)
        MainWindow.resize(640, 730)
        MainWindow.setWindowTitle("Dialog")

        ## 프레임 ##
        self.frame_2 = QtWidgets.QFrame(MainWindow)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 640, 700))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.frame1 = QtWidgets.QFrame(self.frame_2)
        self.frame1.setGeometry(QtCore.QRect(15, 10, 640, 700))
        self.frame1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame1.setObjectName("frame")

        ## 버튼 ##
        self.start1 = QtWidgets.QPushButton(self.frame1)
        self.start1.setGeometry(QtCore.QRect(0, 210, 75, 24))
        self.start1.setObjectName("start1")
        self.start1.setText("1번시점")
        self.start1.clicked.connect(self.st1)

        self.stop1 = QtWidgets.QPushButton(self.frame1)
        self.stop1.setGeometry(QtCore.QRect(80, 210, 75, 24))
        self.stop1.setObjectName("stop1")
        self.stop1.setText("6번시점")
        self.stop1.clicked.connect(self.st6)

        self.sp = QtWidgets.QPushButton(self.frame1)
        self.sp.setGeometry(QtCore.QRect(270, 210, 75, 24))
        self.sp.setObjectName("sp")
        self.sp.setText("자동 가속")
        self.sp.clicked.connect(self.swc)

        self.lineEdit = QtWidgets.QLineEdit(self.frame1)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QtCore.QRect(160, 210, 113, 24))


        ## 이미지 보드 ##
        self.wg = QtWidgets.QLabel(self.frame1)
        self.wg.setGeometry(QtCore.QRect(0, 0, 300, 200))
        self.wg.setObjectName("wg")


        self.wg2 = QtWidgets.QLabel(self.frame1)
        self.wg2.setGeometry(QtCore.QRect(310, 0, 300, 200))
        self.wg2.setObjectName("wg2")

        self.wg3 = QtWidgets.QLabel(self.frame1)
        self.wg3.setGeometry(QtCore.QRect(0,460, 200, 200))
        self.wg3.setObjectName("wg3")

        self.wg4 = QtWidgets.QLabel(self.frame1)
        self.wg4.setGeometry(QtCore.QRect(45, 240, 520, 200))
        self.wg4.setObjectName("wg4")


        ## 라벻 ##
        font = QFont()
        font.setPointSize(12)

        self.label = QLabel(self.frame1)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QtCore.QRect(220, 460, 200, 30))
        self.label.setFont(font)

        self.label2 = QLabel(self.frame1)
        self.label2.setObjectName(u"label_2")
        self.label2.setGeometry(QtCore.QRect(220, 500, 200, 30))
        self.label2.setFont(font)

        self.label3 = QLabel(self.frame1)
        self.label3.setObjectName(u"label_3")
        self.label3.setGeometry(QtCore.QRect(220, 540, 200, 30))
        self.label3.setFont(font)

        self.label4 = QLabel(self.frame1)
        self.label4.setObjectName(u"label_4")
        self.label4.setGeometry(QtCore.QRect(220, 580, 200, 30))
        self.label4.setFont(font)

        self.label5 = QLabel(self.frame1)
        self.label5.setObjectName(u"label_5")
        self.label5.setGeometry(QtCore.QRect(220, 620, 200, 30))
        self.label5.setFont(font)



        ## 라벨에 출력하는 sdk thread ##
        self.sdk_thread()








        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # self.sdk_thread()


    ## 속도제한 입력값 받기 ##
    def spd1(self):
        a = self.lineEdit.text()
        if type(self.spd) == int:
            self.spd = a




    ## sdk 정보 라벨에 업로드 ##
    def sdk(self,MainWindow):
        while True:
            l1 = str(self.mmap.getspeed() * 3)
            l2 = str(self.mmap.getgameSteer())
            l4 = str(self.mmap.getgameBrake())
            l5 = str(self.mmap.getengineRpm())
            self.label.setText("SPEED      :" + l1)
            self.label2.setText("STEER     :" + l2)
            self.label4.setText('BRAKE     :' + l4)
            self.label5.setText("RPM       :" + l5)
            time.sleep(0.1)


    ## 시점 전환 키 1번 6번 시점마다 다른 모델 적용 ##
    def st1(self):
        self.rr = 2
        app = Application().connect(path=r"C:\Program Files (x86)\Steam\steamapps\common\Euro Truck Simulator 2\bin\win_x64\eurotrucks2.exe")
        app.top_window().set_focus()
        time.sleep(1)
        pydirectinput.press('1')

    def st6(self):
        self.rr = 1
        app = Application().connect(path=r"C:\Program Files (x86)\Steam\steamapps\common\Euro Truck Simulator 2\bin\win_x64\eurotrucks2.exe")
        app.top_window().set_focus()
        time.sleep(1)
        pydirectinput.press('6')


    ## 자동 가속 ##
    def speedcontrol(self,MainWindow):
        a = self.lineEdit.text()

        self.spd = int(a)/3
        print(self.spd)


        while self.runnig:

            self.speed = self.mmap.getspeed()
            if self.speed < self.spd:
                pydirectinput.keyDown('w')

                time.sleep(0.01)
                pydirectinput.press('w')
                print('w')
            elif self.speed > self.spd:
                pydirectinput.keyDown('s')

                time.sleep(0.01)
                pydirectinput.press('s')
                print('s')

    ##메인 쓰레드 ##
    def Video_to_frame(self, MainWindow):


        while True:

            ## 화면 스크린샷 ##
            vid = pyautogui.screenshot(region=(0, 50, 1281, 700))
            self.pic = vid
            self.img_frame = np.array(self.pic)




            ## 게임 시점 전환시 다른 모델 적용 ##
            if self.rr == 1:

                ## d는 케니언 엣지 이미지 , center1는 차선의 중심과 차 중심간의 이격 , self.img_frame는 원본이미지에 허프 직선그림
                d ,center1, self.img_frame = self.line1.view6(self.img_frame)




            elif self.rr == 2:
                ## d는 케니언 엣지 이미지 , center1는 차선의 중심과 차 중심간의 이격 , self.img_frame는 원본이미지에 허프 직선그림
                d ,center1, self.img_frame = self.line1.view1(self.img_frame)




            ## 크기변환, pt에 맞는 형식의 이미지로 전환
            ## 원본에 차선 직선 그려진 이미지
            self.frame = cv2.resize(self.img_frame, dsize=(300, 200), interpolation=cv2.INTER_AREA)
            self.rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
            self.convertToQtFormat = QImage(self.rgbImage.data, self.rgbImage.shape[1], self.rgbImage.shape[0],
                                            QImage.Format_BGR888)
            self.pixmap = QPixmap(self.convertToQtFormat)
            self.wg.setPixmap(self.pixmap)
            self.wg.update()


            d = cv2.resize(d, dsize=(300, 200), interpolation=cv2.INTER_AREA)
            self.convertToQtFormat1 = QImage(d.data, self.rgbImage.shape[1], self.rgbImage.shape[0],
                                            QImage.Format_Grayscale8)
            self.pixmap1 = QPixmap(self.convertToQtFormat1)
            self.wg2.setPixmap(self.pixmap1)
            self.wg2.update()




            ## 핸들값 그림
            dd = self.steer.gethandle()
            self.convertToQtFormat2 = QImage(dd.data, 200, 200,QImage.Format_BGR888)
            self.pixmap2 = QPixmap(self.convertToQtFormat2)
            self.wg3.setPixmap(self.pixmap2)
            self.wg3.update()


            ## 차선과 차의 위치 2d
            self.line = cv2.imread('../eurotruck_line/line.jpg')
            center = 260 + center1 *0.35
            lc =int(center - 75)
            rc =int(center+75)
            cv2.rectangle(self.line, (lc, 90), (rc, 190), (0, 0, 0), -1)
            self.convertToQtFormat3 = QImage(self.line.data, 520, 200, QImage.Format_BGR888)
            self.pixmap3 = QPixmap(self.convertToQtFormat3)
            self.wg4.setPixmap(self.pixmap3)
            self.wg4.update()

            ## 차선이달 글씨 출력
            if center > 300:
                loc = '우측이탈'
            elif center <220:
                loc = '좌측이탈'
            else:
                loc = '중앙'

            l3 = loc
            self.label3.setText("LOCATION  :"+l3)

            sleep(0.01)





        # cv2.destroyAllWindows()

        # 창 이름 설정



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("ForSign", "ForSign"))

        # video_to_frame을 쓰레드로 사용
        # 이게 영상 재생 쓰레드 돌리는거 얘를 조작하거나 함수를 생성해서 연속재생 관리해야할듯

    def video_thread(self, MainWindow):
        thread = threading.Thread(target=self.Video_to_frame, args=(self,))
        thread.daemon = True  # 프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()

    ## 자동가속 쓰레드 온 오프 ##
    def swc(self):
        self.c1 += 1
        if self.c1 % 2 == 1:
            thread1 = threading.Thread(target=self.speedcontrol, args=(self,))
            self.runnig = True
            thread1.start()
        else:
            self.runnig = False
            print(self.runnig)




    def sdk_thread(self):
        thread2 = threading.Thread(target=self.sdk, args=(self,))
        thread2.start()








if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    ui.video_thread(MainWindow)


    MainWindow.show()
    sys.exit(app.exec_())
