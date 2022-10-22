import os

# import cv2
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QPixmap
import sys

# from PyQt5.uic.properties import QtCore

import CheAnh

# khai bao giao dien
ui_main, _ = loadUiType('main.ui')
point_XY = []
_LinkIMG_ = [0]
SizeMax = []
SIzelabel = []


# def onclick(event):
#     if event.xdata != None and event.ydata != None:
#         if len(point_XY) >= 2:
#             point_XY.clear()
#         point_XY.append([int(event.xdata), int(event.ydata)])
#         point_XY.sort()


class MainApp(QMainWindow, ui_main):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # click nut bat dau

        self.btn_batdau_vuong.clicked.connect(self.ThucThi_vuong)
        self.btn_batdau_tron.clicked.connect(self.ThucThi_tron)
        self.thanh_dieuchinh.valueChanged.connect(self.CuongDo)
        self.SetViewCuongDo(5)
        # thanh dieu chinh x,y
        self.point_x.textChanged.connect(self.DemoIMG)
        self.point_y.textChanged.connect(self.DemoIMG)
        self.size_che.textChanged.connect(self.DemoIMG)
        self.thanh_dieuchinh.valueChanged.connect(self.DemoIMG)

        self.Slider_X.valueChanged.connect(self.DieuCHinhXY)
        self.Slider_Y.valueChanged.connect(self.DieuCHinhXY)
        self.Slider_R.valueChanged.connect(self.DieuCHinhXY)

        self.path_folder.textChanged.connect(self.DemoIMG)

        # check nhap du lieu

    def DieuCHinhXY(self):
        CuongDo_X = self.Slider_X.value()
        CuongDo_Y = self.Slider_Y.value()
        CuongDo_R = self.Slider_R.value()
        self.point_x.setText(str(CuongDo_X))
        self.Slider_X.setValue(int(CuongDo_X))
        self.point_y.setText(str(CuongDo_Y))
        self.size_che.setText(str(CuongDo_R))

    def DemoIMG(self):
        try:
            path_Folder = str(self.path_folder.text())
            X = int(self.point_x.text())
            Y = int(self.point_y.text())
            R = int(self.size_che.text())

            if X > 0 and Y > 0 and R > 0 and path_Folder != "":
                try:
                    txt = str(path_Folder)
                    CuongDo = self.thanh_dieuchinh.value()
                    path_Vuong = CheAnh.GetIMGinFloderDEmo(X, Y, R, 1, txt, "img_out_demo", CuongDo, 2)
                    path_Tron = CheAnh.GetIMGinFloderDEmo(X, Y, R, 2, txt, "img_out_demo", CuongDo, 2)
                    _LinkIMG_[0] = path_Vuong
                    if "lỗi" not in path_Vuong:
                        self.ShowImg_Vuong(path_Vuong)
                        self.ShowImg_Tron(path_Tron)
                    else:
                        # showLoad
                        self.txt_log.clear()
                        self.txt_log.insertPlainText(path_Tron + "\n")
                        # QMessageBox.information(self, "Thông báo", path_Tron)
                except:
                    self.txt_log.clear()
                    self.txt_log.insertPlainText("Có lỗi vui lòng thử lại" + "\n")
        except:
            self.txt_log.clear()
            self.txt_log.insertPlainText("Có lỗi vui lòng thử lại" + "\n")

    def ShowImg_Vuong(self, file_path):
        label = self.findChild(QLabel, "labviewVuong")
        pixmap = QPixmap(file_path)
        label.setScaledContents(True)
        label.setPixmap(pixmap)

        label.mousePressEvent = self.getPoss
        label.mouseReleaseEvent = self.getPoss
        # label.mouseReleaseEvent = self.ShowFullIMG

    def ShowImg_Tron(self, file_path):
        label1 = self.findChild(QLabel, "labviewTron")
        pixmap = QPixmap(file_path)
        label1.setScaledContents(True)
        label1.setPixmap(pixmap)
        label1.mousePressEvent = self.getPoss
        label1.mouseReleaseEvent = self.getPoss
        # label1.mouseReleaseEvent = self.ShowFullIMG

    def getPoss(self, event):
        x = event.pos().x()
        y = event.pos().y()
        label = self.findChild(QLabel, "labviewVuong")
        print("size broder", label.size())
        size_W, size_H = 481, 389
        import cv2
        SizeH_img, SizeW_img, h = cv2.imread(_LinkIMG_[0]).shape
        print("size img", SizeW_img, SizeH_img)
        ptW = int(((SizeW_img - size_W) / size_W) * 100)
        print("Phan tram Width", ptW)
        ptH = int(((SizeH_img - size_H) / size_H) * 100)
        print("Phan tram Hight", ptH)
        # get value tang size
        x = ( (x * ptW) / 100) + x
        y = ( (y * ptH) / 100) + y

        print(x, y)
        if len(point_XY) >= 2:
            point_XY.clear()
        point_XY.append([int(x), int(y)])
        point_XY.sort()

        if len(point_XY) == 2:
            # print(point_XY)
            x1, y1, x2, y2 = point_XY[0][0], point_XY[0][1], point_XY[1][0], point_XY[1][1]
            pointX = x1
            pointY = y1
            CuongDo_R = x2 - x1

            # print(pointX, pointY, CuongDo_R)
            self.point_x.setText(str(pointX))
            self.point_y.setText(str(pointY))
            self.size_che.setText(str(CuongDo_R))



    # def ShowFullIMG(self, event):
    #     import cv2
    #     import matplotlib.pyplot as plt
    #
    #     image = cv2.imread(_LinkIMG_[0])
    #
    #     ax = plt.gca()
    #     fig = plt.gcf()
    #     ax.imshow(image)
    #     # click
    #     fig.canvas.mpl_connect('button_press_event', onclick)
    #     # buong chuot
    #     fig.canvas.mpl_connect('button_release_event', onclick)
    #     fig.canvas.mpl_connect('button_release_event', self.getPos)
    #     plt.show()


    def CuongDo(self):
        CuongDo = self.thanh_dieuchinh.value()
        self.SetViewCuongDo(CuongDo)

    def SetViewCuongDo(self, txt):
        txt = str(txt)
        self.label = self.findChild(QLabel, "lableCuongDo")
        self.label.setText(txt + "%")

    def ThucThi_vuong(self):
        path_Folder = str(self.path_folder.text())
        X = int(self.point_x.text())
        Y = int(self.point_y.text())
        R = int(self.size_che.text())
        txt = str(path_Folder)
        import CheAnh
        CuongDo = self.thanh_dieuchinh.value()
        Log = CheAnh.InputData(X, Y, R, 1, txt, CuongDo)
        Log = list(Log)
        # showLoad
        self.txt_log.insertPlainText(Log[0])
        QMessageBox.information(self, "Thông báo", "Hoàn thành che anh theo hinh vuông")
        os.startfile(Log[1])

    def ThucThi_tron(self):
        path_Folder = str(self.path_folder.text())
        X = int(self.point_x.text())
        Y = int(self.point_y.text())
        R = int(self.size_che.text())
        txt = str(path_Folder)
        import CheAnh
        CuongDo = self.thanh_dieuchinh.value()
        Log = CheAnh.InputData(X, Y, R, 2, txt, CuongDo)
        Log = list(Log)
        # showLoad
        self.txt_log.insertPlainText(Log[0])
        QMessageBox.information(self, "Thông báo", "Hoàn thành che ảnh theo hình tròn")
        os.startfile(Log[1])


if __name__ == "__main__":
    CheAnh.TaoThuMuc('img_out')
    CheAnh.TaoThuMuc('img_out_demo')

    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()

# xy ly tieng viet
# luu anh cu
