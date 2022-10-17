import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QPixmap

import sys

# khai bao giao dien
from pyqt5_plugins.examplebuttonplugin import QtGui

ui_main, _ = loadUiType('main.ui')


class MainApp(QMainWindow, ui_main):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # click nut bat dau
        self.point_x.textChanged.connect(self.DemoIMG)
        self.point_y.textChanged.connect(self.DemoIMG)
        self.size_che.textChanged.connect(self.DemoIMG)
        self.thanh_dieuchinh.valueChanged.connect(self.DemoIMG)

        self.btn_batdau_vuong.clicked.connect(self.ThucThi_vuong)
        self.btn_batdau_tron.clicked.connect(self.ThucThi_tron)
        self.thanh_dieuchinh.valueChanged.connect(self.CuongDo)
        self.SetViewCuongDo(5)
        # check nhap du lieu

    def DemoIMG(self):
        path_Folder = str(self.path_folder.text())
        X = int(self.point_x.text())
        Y = int(self.point_y.text())
        R = int(self.size_che.text())


        if X > 0 and Y > 0 and R > 0 and path_Folder != "":
            txt = str(path_Folder)
            import CheAnh
            CuongDo = self.thanh_dieuchinh.value()
            path_Vuong = CheAnh.GetIMGinFloderDEmo(X, Y, R, 1, txt, "img_out", CuongDo, 2)
            path_Tron = CheAnh.GetIMGinFloderDEmo(X, Y, R, 2, txt, "img_out", CuongDo, 2)
            if "lỗi" not in path_Vuong:
                self.ShowImg_Vuong(path_Vuong)
                self.ShowImg_Tron(path_Tron)
            else:
                # showLoad
                self.txt_log.insertPlainText(path_Tron+"\n")
                # QMessageBox.information(self, "Thông báo", path_Tron)


    def ShowImg_Vuong(self, file_path):
        label = self.findChild(QLabel, "labviewVuong")
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(550, 450)
        label.setPixmap(pixmap)


    def ShowImg_Tron(self, file_path):
        label = self.findChild(QLabel, "labviewTron")
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(550, 450)
        label.setPixmap(pixmap)


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
        # CuongDo = 45 - CuongDo
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
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()

# tu tao thu muc
# and file cmd
