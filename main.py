import os
import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

import CheAnh

ui_main, _ = loadUiType('main.ui')

Savebtn, _LinkIMG_, linkcache, folderOut, point_XY, ViTriXY, \
LinkSaveIMG, XYTam, IMGXuLy = 0, "", "", "", [], [], [], [], ""


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
        self.path_folder.textChanged.connect(self.ReloadData)
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
        self.btnSave.clicked.connect(self.SetSaveIMG)

    def ReloadData(self):
        global Savebtn

        Savebtn = 0
        self.point_x.setText(str(0))
        self.Slider_X.setValue(int(0))
        self.point_y.setText(str(0))
        self.size_che.setText(str(0))

    def SetSaveIMG(self):
        global Savebtn, _LinkIMG_, linkcache, ViTriXY, LinkSaveIMG, XYTam
        Savebtn += 1
        ViTriXY.append(XYTam[len(XYTam) - 1])
        print(len(ViTriXY))
        QMessageBox.information(self, "Thông báo", "Lưu thành công vị trí thứ " + str(Savebtn))

    def BatDauLoad(self):
        self.setFixedSize(1141, 10)

    def DungLoad(self):
        self.point_x.setText(str(0))
        self.point_y.setText(str(0))
        self.size_che.setText(str(0))
        global ViTriXY
        ViTriXY.clear()
        self.setFixedSize(1141, 902)

    def getDirectory(self):
        response = QFileDialog.getExistingDirectory(self, caption='Chọn thư mục')
        return response

    def SelectIn(self):
        IN_ = self.getDirectory()
        self.path_folder.setText(str(IN_))

    def SelectOut(self):
        OUT_ = self.getDirectory()
        self.path_folder_out.setText(str(OUT_))

    def SaveOutFolder(self):
        global folderOut

        folderOut = str(self.path_folder_out.text())

    def DieuCHinhXY(self):
        CuongDo_X = self.Slider_X.value()
        CuongDo_Y = self.Slider_Y.value()
        CuongDo_R = self.Slider_R.value()
        self.point_x.setText(str(CuongDo_X))
        self.Slider_X.setValue(int(CuongDo_X))
        self.point_y.setText(str(CuongDo_Y))
        self.size_che.setText(str(CuongDo_R))

    def convert_cv_qt(self, cv_img):
        try:
            import cv2
            height, width, channel = cv_img.shape
            bytesPerLine = 3 * width
            qImg = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            return qImg
        except Exception as ex:
            print(ex)
            return False

    def DemoIMG(self):
        try:
            import cv2
            global Savebtn, _LinkIMG_, linkcache, IMGXuLy, ViTriXY

            path_Folder = str(self.path_folder.text())
            FileIMG = CheAnh.GetIMGinFloderDEmo(path_Folder)

            CuongDo = self.thanh_dieuchinh.value()
            X = int(self.point_x.text())
            Y = int(self.point_y.text())
            R = int(self.size_che.text())
            if X == 0 and Y == 0 and R == 0 and path_Folder != "":
                X, Y, R = 10, 10, 10
            if X > 0 and Y > 0 and R > 0 and path_Folder != "":
                try:
                    # VUONG
                    IMGXuLy = CheAnh.CheAnh(X, Y, R, FileIMG, 1, CuongDo)
                    if len(ViTriXY) > 0:
                        for i in ViTriXY:
                            IMGXuLy = CheAnh.CheAnh(i[0], i[1], i[2], IMGXuLy, 1, CuongDo, True)
                    IMGVUONG_ = self.convert_cv_qt(IMGXuLy)
                    self.ShowImg_Vuong(IMGVUONG_)
                    #FACE
                    FileIMG = os.path.split(FileIMG)[-1]
                    cv2.imwrite(str(CheAnh.path()) + "\\img_out_demo\\" + FileIMG, IMGXuLy)
                    for i in CheAnh.GetXyFace(str(CheAnh.path()) + "\\img_out_demo\\" + FileIMG):

                        IMGXuLy = CheAnh.CheAnh(i[0], i[1], i[2], IMGXuLy, 1, CuongDo, True)
                    IMGFACE_ = self.convert_cv_qt(IMGXuLy)
                    self.ShowImg_Face(IMGFACE_)
                except Exception as ex:
                    print(ex)
                    self.point_x.setText(str(0))
                    self.point_y.setText(str(0))
                    self.size_che.setText(str(0))

        except Exception as ex:
            print(ex)

    def ShowImg_Vuong(self, IMG):
        label = self.findChild(QLabel, "labviewVuong")
        pixmap = QPixmap(IMG)
        label.setScaledContents(True)
        label.setPixmap(pixmap)
        label.mousePressEvent = self.getPoss
        label.mouseReleaseEvent = self.getPoss

    def ShowImg_Face(self, IMG):
        label2 = self.findChild(QLabel, "labviewFace")
        pixmap = QPixmap(IMG)
        label2.setScaledContents(True)
        label2.setPixmap(pixmap)
        label2.mousePressEvent = self.getPoss
        label2.mouseReleaseEvent = self.getPoss

    def getPoss(self, event):
        global point_XY, XYTam, IMGXuLy
        x = event.pos().x()
        y = event.pos().y()
        label = self.findChild(QLabel, "labviewVuong")
        size_W, size_H = 481, 519
        SizeH_img, SizeW_img, h = IMGXuLy.shape
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
            XYTam.append([int(pointX), int(pointY), int(CuongDo_R)])
            print("nho tam", XYTam)
            self.point_x.setText(str(pointX))
            self.point_y.setText(str(pointY))
            self.size_che.setText(str(CuongDo_R))

    def CuongDo(self):
        CuongDo = self.thanh_dieuchinh.value()
        self.SetViewCuongDo(CuongDo)

    def SetViewCuongDo(self, txt):
        txt = str(txt)
        self.label_ = self.findChild(QLabel, "lableCuongDo")
        self.label_.setText(txt + "%")

    def ThucThi_vuong(self):
        try:
            import cv2
            global Savebtn, _LinkIMG_, linkcache, IMGXuLy, folderOut, ViTriXY

            # bat dau  ###

            path_Folder = str(self.path_folder.text())
            if len(path_Folder) < 2:
                QMessageBox.information(self, "Thông báo", "Vui lòng nhập đủ thông tin")
                return False
            self.BatDauLoad()
            FileIMG = CheAnh.GetIMGinFloderOut(path_Folder)
            from datetime import datetime
            now = datetime.now()
            if folderOut != "" and len(folderOut) > 3:
                path_ = folderOut
            else:
                path_ = str(CheAnh.path()) + "\\img_out\\" + str(now.strftime("%m-%d-%Y_%H"))
                path_ = path_ + "\\VUONG"
                CheAnh.TaoThuMuc(str(path_))

            CuongDo = self.thanh_dieuchinh.value()
            X = int(self.point_x.text())
            Y = int(self.point_y.text())
            R = int(self.size_che.text())
            if X == 0 and Y == 0 and R == 0 and path_Folder != "":
                X, Y, R = 10, 10, 10
            if X > 0 and Y > 0 and R > 0 and path_Folder != "":
                LogERR = []
                for a in FileIMG:
                    FileIMG = a
                    try:
                        # VUONG
                        IMGXuLy = CheAnh.CheAnh(X, Y, R, FileIMG, 1, CuongDo)
                        if len(ViTriXY) > 0:
                            for i in ViTriXY:
                                IMGXuLy = CheAnh.CheAnh(i[0], i[1], i[2], IMGXuLy, 1, CuongDo, True)

                        FileIMG = os.path.split(FileIMG)[-1]
                        print(path_ + str(FileIMG))
                        cv2.imwrite(path_ + "\\" + str(FileIMG), IMGXuLy)

                    except Exception as ex:
                        print(ex)
                        LogERR.append("\n" + "ANH :\t" + FileIMG + "\t Co loi bo qua" + "\n")
                # hoan thanh ####
                self.DungLoad()
                QMessageBox.information(self, "Thông báo", "Hoàn thành che ảnh")
                if len(LogERR) > 2:
                    strLOG = ""
                    for i in LogERR:
                        strLOG += i
                    ScrollMessageBox(QMessageBox.Critical, "Có lỗi !", strLOG)
                os.startfile(path_)
        except Exception as ex:
            print(ex)

    def ThucThi_face(self):
        try:
            import cv2
            global Savebtn, _LinkIMG_, linkcache, IMGXuLy, folderOut, ViTriXY

            # bat dau  ###

            path_Folder = str(self.path_folder.text())
            if len(path_Folder) < 2:
                QMessageBox.information(self, "Thông báo", "Vui lòng nhập đủ thông tin")
                return False
            self.BatDauLoad()
            FileIMG = CheAnh.GetIMGinFloderOut(path_Folder)
            from datetime import datetime
            now = datetime.now()
            if folderOut != "" and len(folderOut) > 3:
                path_ = folderOut
            else:
                path_ = str(CheAnh.path()) + "\\img_out\\" + str(now.strftime("%m-%d-%Y_%H"))
                path_ = path_ + "\\FACE"
                CheAnh.TaoThuMuc(str(path_))

            CuongDo = self.thanh_dieuchinh.value()
            X = int(self.point_x.text())
            Y = int(self.point_y.text())
            R = int(self.size_che.text())
            if X == 0 and Y == 0 and R == 0 and path_Folder != "":
                X, Y, R = 10, 10, 10
            if X > 0 and Y > 0 and R > 0 and path_Folder != "":
                LogERR = []
                for a in FileIMG:
                    FileIMG = a
                    try:
                        # FACE
                        # input
                        IMGXuLy = CheAnh.CheAnh(X, Y, R, FileIMG, 1, CuongDo)
                        if len(ViTriXY) > 0:
                            for i in ViTriXY:
                                IMGXuLy = CheAnh.CheAnh(i[0], i[1], i[2], IMGXuLy, 1, CuongDo, True)
                        # ai input
                        FileIMG = os.path.split(FileIMG)[-1]
                        print(path_ + str(FileIMG))
                        cv2.imwrite(path_ + "\\" + str(FileIMG), IMGXuLy)

                        for i in CheAnh.GetXyFace(path_ + "\\" + str(FileIMG)):
                            print(i)
                            IMGXuLy = CheAnh.CheAnh(i[0], i[1], i[2], IMGXuLy, 1, CuongDo, True)

                        cv2.imwrite(path_ + "\\" + str(FileIMG), IMGXuLy)


                    except Exception as ex:
                        print(ex)
                        LogERR.append("\n" + "ANH :\t" + FileIMG + "\t Co loi bo qua" + "\n")
                # hoan thanh ####
                self.DungLoad()
                QMessageBox.information(self, "Thông báo", "Hoàn thành che ảnh")
                if len(LogERR) > 2:
                    strLOG = ""
                    for i in LogERR:
                        strLOG += i
                    ScrollMessageBox(QMessageBox.Critical, "Có lỗi !", strLOG)
                os.startfile(path_)
        except Exception as ex:
            print(ex)

    def ThucThi_tron(self):
        try:
            import cv2
            global Savebtn, _LinkIMG_, linkcache, IMGXuLy, folderOut, ViTriXY

            # bat dau  ###

            path_Folder = str(self.path_folder.text())
            if len(path_Folder) < 2:
                QMessageBox.information(self, "Thông báo", "Vui lòng nhập đủ thông tin")
                return False
            self.BatDauLoad()

            FileIMG = CheAnh.GetIMGinFloderOut(path_Folder)
            from datetime import datetime
            now = datetime.now()
            if folderOut != "" and len(folderOut) > 3:
                path_ = folderOut
            else:
                path_ = str(CheAnh.path()) + "\\img_out\\" + str(now.strftime("%m-%d-%Y_%H"))
                path_ = path_ + "\\TRON"
                CheAnh.TaoThuMuc(str(path_))

            CuongDo = self.thanh_dieuchinh.value()
            X = int(self.point_x.text())
            Y = int(self.point_y.text())
            R = int(self.size_che.text())
            if X == 0 and Y == 0 and R == 0 and path_Folder != "":
                X, Y, R = 10, 10, 10
            if X > 0 and Y > 0 and R > 0 and path_Folder != "":
                LogERR = []
                for a in FileIMG:
                    FileIMG = a
                    try:
                        # TRON
                        IMGXuLy = CheAnh.CheAnh(X, Y, R, FileIMG, 2, CuongDo)
                        if len(ViTriXY) > 0:
                            for i in ViTriXY:
                                IMGXuLy = CheAnh.CheAnh(i[0], i[1], i[2], IMGXuLy, 2, CuongDo, True)

                        FileIMG = os.path.split(FileIMG)[-1]
                        print(path_ + str(FileIMG))
                        cv2.imwrite(path_ + "\\" + str(FileIMG), IMGXuLy)

                    except Exception as ex:
                        print(ex)
                        LogERR.append("\n" + "ANH :\t" + FileIMG + "\t Co loi bo qua" + "\n")
                # hoan thanh ####
                self.DungLoad()
                QMessageBox.information(self, "Thông báo", "Hoàn thành che ảnh")
                if len(LogERR) > 2:
                    strLOG = ""
                    for i in LogERR:
                        strLOG += i
                    ScrollMessageBox(QMessageBox.Critical, "Có lỗi !", strLOG)
                os.startfile(path_)
        except Exception as ex:
            print(ex)


def Main():
    CheAnh.TaoThuMuc('img_out')
    CheAnh.TaoThuMuc('img_out_demo')
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    Main()
