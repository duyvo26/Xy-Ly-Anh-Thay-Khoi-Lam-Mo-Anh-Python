import os

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys


# khai bao giao dien
ui_main, _ = loadUiType('main.ui')


class MainApp(QMainWindow, ui_main):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # click nut bat dau
        self.btn_batdau_vuong.clicked.connect(self.ThucThi_vuong)
        self.btn_batdau_tron.clicked.connect(self.ThucThi_tron)

    def ThucThi_vuong(self):
        path_Folder = str(self.path_folder.text())
        X = int(self.point_x.text())
        Y = int(self.point_y.text())
        R = int(self.size_che.text())
        txt = str(path_Folder)
        import CheAnh
        Log = CheAnh.InputData(X, Y, R, 1, txt)
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
        Log = CheAnh.InputData(X, Y, R, 2, txt)
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