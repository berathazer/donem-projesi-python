from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import pyqtSlot,QTimer,QDate,Qt
from PyQt5.QtWidgets import QDialog,QMessageBox,QMainWindow
from PyQt5.QtGui import QImage,QPixmap
import cv2
import numpy as np
import face_recognition
import os
import csv
import datetime

cap = cv2.VideoCapture(0)

print('Encoding Complete')
cap = cv2.VideoCapture(0)

class Ui_YuzTanima(object):
    def setupUi(self, YuzTanima):
        YuzTanima.setObjectName("YuzTanima")
        YuzTanima.resize(978, 600)
        self.centralwidget = QtWidgets.QWidget(YuzTanima)
        self.centralwidget.setObjectName("centralwidget")
        self.lblimg = QtWidgets.QLabel(self.centralwidget)
        self.lblimg.setGeometry(QtCore.QRect(30, 10, 561, 461))
        self.lblimg.setText("")
        self.lblimg.setObjectName("lblimg")
        self.btntani = QtWidgets.QPushButton(self.centralwidget)
        self.btntani.setGeometry(QtCore.QRect(40, 490, 241, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btntani.setFont(font)
        self.btntani.setObjectName("btntani")
        self.btncikis = QtWidgets.QPushButton(self.centralwidget)
        self.btncikis.setGeometry(QtCore.QRect(290, 490, 261, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btncikis.setFont(font)
        self.btncikis.setObjectName("btncikis")
        self.llbtarih = QtWidgets.QLabel(self.centralwidget)
        self.llbtarih.setGeometry(QtCore.QRect(620, 40, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.llbtarih.setFont(font)
        self.llbtarih.setObjectName("llbtarih")
        self.lblsaat = QtWidgets.QLabel(self.centralwidget)
        self.lblsaat.setGeometry(QtCore.QRect(620, 80, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblsaat.setFont(font)
        self.lblsaat.setObjectName("lblsaat")
        self.gbdetay = QtWidgets.QGroupBox(self.centralwidget)
        self.gbdetay.setGeometry(QtCore.QRect(620, 140, 221, 341))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.gbdetay.setFont(font)
        self.gbdetay.setObjectName("gbdetay")
        self.lblisim = QtWidgets.QLabel(self.gbdetay)
        self.lblisim.setGeometry(QtCore.QRect(10, 60, 191, 41))
        self.lblisim.setObjectName("lblisim")
        self.lbbldurum = QtWidgets.QLabel(self.gbdetay)
        self.lbbldurum.setGeometry(QtCore.QRect(10, 140, 191, 51))
        self.lbbldurum.setObjectName("lbbldurum")
        self.lbltoplam = QtWidgets.QLabel(self.gbdetay)
        self.lbltoplam.setGeometry(QtCore.QRect(10, 220, 201, 61))
        self.lbltoplam.setObjectName("lbltoplam")
        YuzTanima.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(YuzTanima)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 978, 21))
        self.menubar.setObjectName("menubar")
        YuzTanima.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(YuzTanima)
        self.statusbar.setObjectName("statusbar")
        YuzTanima.setStatusBar(self.statusbar)


        self.retranslateUi(YuzTanima)
        QtCore.QMetaObject.connectSlotsByName(YuzTanima)

    def setPhoto(self, image):
        try:
            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            self.lblimg.setPixmap(QtGui.QPixmap.fromImage(image))

        except:
            print("bir hata oluştu")
    def retranslateUi(self, YuzTanima):
        _translate = QtCore.QCoreApplication.translate
        YuzTanima.setWindowTitle(_translate("YuzTanima", "MainWindow"))
        self.btntani.setText(_translate("YuzTanima", "Tanımla"))
        self.btncikis.setText(_translate("YuzTanima", "Çıkış"))
        self.llbtarih.setText(_translate("YuzTanima", "Tarih:"))
        self.lblsaat.setText(_translate("YuzTanima", "Saat:"))
        self.gbdetay.setTitle(_translate("YuzTanima", "Detaylar"))
        self.lblisim.setText(_translate("YuzTanima", "İsim:"))
        self.lbbldurum.setText(_translate("YuzTanima", "Durum:"))
        self.lbltoplam.setText(_translate("YuzTanima", "Toplam zaman:"))

    def faceencode(self):
        print("")
    def initProgram(self):

        self.path = 'Images'
        self.images = []
        self.classNames = []
        self.myList = os.listdir(self.path)

        print(self.myList)
        for cl in self.myList:
            curImg = cv2.imread(f'{self.path}/{cl}')
            self.images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])
        print(self.classNames)

        encodeListKnown = self.findEncodings(self.images)

        while True:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)  # find locations
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)  # yüzün konumunu gönderiyoruz

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                # print(matches,faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = self.classNames[matchIndex].upper()
                    # print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # çözünürlük artırıldı.daha iyi çalışması için girdi görüntüsünü büyütmek, yüz tanıma algoritmasının performansını artırırken, işlem süresini kısaltabilir.

                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                    # markAttendance('Elon')
                else:

                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # çözünürlük artırıldı.daha iyi çalışması için girdi görüntüsünü büyütmek, yüz tanıma algoritmasının performansını artırırken, işlem süresini kısaltabilir.

                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Kisi taninamadi", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255),
                                2)
            cv2.imshow('Webcam', img)
            if cv2.waitKey(1) == ord('q'):
                break
            # self.setPhoto(img)
            # if cv2.waitKey(1) == ord('q'):
            #    break


    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    # encodeListKnown=findEncodings(images)
    # print(len(encodeListKnown))6

    def markAttendance(name):#sadece adını ve geldikleri zamanı yazacağız
        with open('Attendance.csv','r+') as f:#csv, virgülle ayrılmış değerleri ifade eder.
            myDataList=f.readlines()
            nameList=[]
            #print(myDataList)
            for line in myDataList:
                entry=line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now =datetime.now()
                dtString=now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')





    def setPhoto(self, image):
        try:
            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            self.lblimg.setPixmap(QtGui.QPixmap.fromImage(image))

        except:
            print("bir hata oluştu")



if __name__ == "_main_":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    YuzTanima = QtWidgets.QMainWindow()
    ui = Ui_YuzTanima()
    ui.setupUi(YuzTanima)
    YuzTanima.show()
    sys.exit(app.exec_())