import os
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QPixmap
import sys
from PyQt5 import QtGui
import CheAnh

ui_main, _ = loadUiType('main.ui')
point_XY = []
_LinkIMG_ = [0]
SizeMax = []
SIzelabel = []
folderOut = [0]
folderOut[0] = ""


class ScrollMessageBox(QMessageBox):
    def __init__(self, *args, **kwargs):
        QMessageBox.__init__(self, *args, **kwargs)
        chldn = self.children()
        scrll = QScrollArea(self)
        scrll.setWidgetResizable(True)
        grd = self.findChild(QGridLayout)
        lbl = QLabel(chldn[1].text(), self)
        lbl.setWordWrap(True)
        scrll.setWidget(lbl)
        scrll.setMinimumSize(600, 350)
        grd.addWidget(scrll, 0, 1)
        chldn[1].setText('')
        self.exec_()


class MainApp(QMainWindow, ui_main):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('app.ico'))
        self.btn_batdau_vuong.clicked.connect(self.ThucThi_vuong)
        self.btn_batdau_tron.clicked.connect(self.ThucThi_tron)
        self.btn_batdau_face.clicked.connect(self.ThucThi_face)

        self.thanh_dieuchinh.valueChanged.connect(self.CuongDo)
        self.SetViewCuongDo(5)
        self.point_x.textChanged.connect(self.DemoIMG)
        self.point_y.textChanged.connect(self.DemoIMG)
        self.size_che.textChanged.connect(self.DemoIMG)
        self.thanh_dieuchinh.valueChanged.connect(self.DemoIMG)
        self.Slider_X.valueChanged.connect(self.DieuCHinhXY)
        self.Slider_Y.valueChanged.connect(self.DieuCHinhXY)
        self.Slider_R.valueChanged.connect(self.DieuCHinhXY)
        self.path_folder.textChanged.connect(self.DemoIMG)
        self.path_folder_out.textChanged.connect(self.SaveOutFolder)
        self.btn_in.clicked.connect(self.SelectIn)
        self.btn_out.clicked.connect(self.SelectOut)

    def BatDauLoad(self):
        self.setFixedSize(1141, 10)
        # QMessageBox.information(self, "Xử lý", "Đang xử lý ảnh vui lòng đợi")

    def DungLoad(self):
        self.setFixedSize(1141, 916)

    def getDirectory(self):
        response = QFileDialog.getExistingDirectory(
            self,
            caption='Chọn thư mục'
        )
        return response

    def SelectIn(self):
        IN_ = self.getDirectory()
        self.path_folder.setText(str(IN_))

    def SelectOut(self):
        OUT_ = self.getDirectory()
        self.path_folder_out.setText(str(OUT_))

    def SaveOutFolder(self):
        folderOut[0] = str(self.path_folder_out.text())

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
            if X == 0 and Y == 0 and R == 0 and path_Folder != "":
                X, Y, R = 10, 10, 10

            if X > 0 and Y > 0 and R > 0 and path_Folder != "":
                try:
                    txt = str(path_Folder)
                    CuongDo = self.thanh_dieuchinh.value()
                    path_Vuong = CheAnh.GetIMGinFloderDEmo(X, Y, R, 1, txt, "img_out_demo", CuongDo, 2)
                    path_Tron = CheAnh.GetIMGinFloderDEmo(X, Y, R, 2, txt, "img_out_demo", CuongDo, 2)
                    if "lỗi" not in path_Vuong:
                        _LinkIMG_[0] = path_Vuong
                        self.ShowImg_Vuong(path_Vuong)
                        self.ShowImg_Tron(path_Tron)
                    else:
                        print("LOI")
                except:
                    print("LOI")
        except:
            print("LOI")

    def ShowImg_Vuong(self, file_path):
        label = self.findChild(QLabel, "labviewVuong")
        pixmap = QPixmap(file_path)
        label.setScaledContents(True)
        label.setPixmap(pixmap)
        label.mousePressEvent = self.getPoss
        label.mouseReleaseEvent = self.getPoss

    def ShowImg_Tron(self, file_path):
        label1 = self.findChild(QLabel, "labviewTron")
        pixmap = QPixmap(file_path)
        label1.setScaledContents(True)
        label1.setPixmap(pixmap)
        label1.mousePressEvent = self.getPoss
        label1.mouseReleaseEvent = self.getPoss

    def getPoss(self, event):
        x = event.pos().x()
        y = event.pos().y()
        label = self.findChild(QLabel, "labviewVuong")
        size_W, size_H = 481, 519
        import cv2
        SizeH_img, SizeW_img, h = cv2.imread(_LinkIMG_[0]).shape
        ptW = int(((SizeW_img - size_W) / size_W) * 100)
        ptH = int(((SizeH_img - size_H) / size_H) * 100)
        x = ((x * ptW) / 100) + x
        y = ((y * ptH) / 100) + y

        if len(point_XY) >= 2:
            point_XY.clear()
        point_XY.append([int(x), int(y)])
        point_XY.sort()

        if len(point_XY) == 2:
            x1, y1, x2, y2 = point_XY[0][0], point_XY[0][1], point_XY[1][0], point_XY[1][1]
            pointX = x1
            pointY = y1
            CuongDo_R = x2 - x1
            self.point_x.setText(str(pointX))
            self.point_y.setText(str(pointY))
            self.size_che.setText(str(CuongDo_R))

    def CuongDo(self):
        CuongDo = self.thanh_dieuchinh.value()
        self.SetViewCuongDo(CuongDo)

    def SetViewCuongDo(self, txt):
        txt = str(txt)
        self.label = self.findChild(QLabel, "lableCuongDo")
        self.label.setText(txt + "%")

    def ThucThi_vuong(self):
        X = int(self.point_x.text())
        Y = int(self.point_y.text())
        R = int(self.size_che.text())
        path_Folder = str(self.path_folder.text())
        if len(path_Folder) < 2 or X == 0 or Y == 0 or R == 0:
            QMessageBox.information(self, "Thông báo", "Vui lòng nhập đủ thông tin")
            return False
        else:
            self.BatDauLoad()
            txt = str(path_Folder)
            import CheAnh
            CuongDo = self.thanh_dieuchinh.value()
            Log = CheAnh.InputData(X, Y, R, 1, txt, folderOut[0], CuongDo)
            Log = list(Log)
            self.DungLoad()
            QMessageBox.information(self, "Thông báo", "Hoàn thành che ảnh theo hình vuông")
            if len(Log[0]) > 2:
                ScrollMessageBox(QMessageBox.Critical, "Có lỗi !", Log[0])
            os.startfile(Log[1])


    def ThucThi_face(self):
        path_Folder = str(self.path_folder.text())
        if len(path_Folder) < 2:
            QMessageBox.information(self, "Thông báo", "Vui lòng nhập đủ thông tin")
            return False
        else:
            self.BatDauLoad()
            # QMessageBox.information(self, "Thông báo", "Đang xử lý vui lòng đợi trong giấy lát")
            X = int(self.point_x.text())
            Y = int(self.point_y.text())
            R = int(self.size_che.text())
            txt = str(path_Folder)
            import CheAnh
            CuongDo = self.thanh_dieuchinh.value()
            Log = CheAnh.InputData(X, Y, R, 3, txt, folderOut[0], CuongDo)
            Log = list(Log)
            # self.txt_log.insertPlainText(Log[0])
            self.DungLoad()
            QMessageBox.information(self, "Thông báo", "Hoàn thành che ảnh theo khuôn mặt")
            if len(Log[0]) > 2:
                ScrollMessageBox(QMessageBox.Critical, "Có lỗi !", Log[0])
            os.startfile(Log[1])


    def ThucThi_tron(self):
        X = int(self.point_x.text())
        Y = int(self.point_y.text())
        R = int(self.size_che.text())
        path_Folder = str(self.path_folder.text())
        if len(path_Folder) < 2 or X == 0 or Y == 0 or R == 0:
            QMessageBox.information(self, "Thông báo", "Vui lòng nhập đủ thông tin")
            return False
        else:
            self.BatDauLoad()
            # QMessageBox.information(self, "Thông báo", "Đang xử lý vui lòng đợi trong giấy lát")
            X = int(self.point_x.text())
            Y = int(self.point_y.text())
            R = int(self.size_che.text())
            txt = str(path_Folder)
            import CheAnh
            CuongDo = self.thanh_dieuchinh.value()
            Log = CheAnh.InputData(X, Y, R, 2, txt, folderOut[0], CuongDo)
            Log = list(Log)
            # self.txt_log.insertPlainText(Log[0])
            self.DungLoad()
            QMessageBox.information(self, "Thông báo", "Hoàn thành che ảnh theo hình tròn")
            if len(Log[0]) > 2:
                ScrollMessageBox(QMessageBox.Critical, "Có lỗi !", Log[0])
            os.startfile(Log[1])


if __name__ == "__main__":
    CheAnh.TaoThuMuc('img_out')
    CheAnh.TaoThuMuc('img_out_demo')
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()
