import os
import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5 import QtCore
import CheAnh

ui_main, _ = loadUiType('_data_\\main.ui')

_LinkIMG_, linkcache, folderOut, point_XY, ViTriXY, \
LinkSaveIMG, XYTam, IMGXuLy,\
countIMG, MaxIMG, ListFileRun, selectFile = "", "", "", [], [], [], [], "", 0, 0, [], {}


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
        self.setWindowIcon(QtGui.QIcon('_data_\\app.ico'))
        self.path_folder.textChanged.connect(self.ReloadData)
        self.btn_batdau_vuong.clicked.connect(self.ThucThi_vuong)
        self.btn_batdau_vuong.clicked.connect(self.ReloadData)
        self.btn_batdau_vuong.setIcon(QIcon("_data_\\icon\\icons8-surface-40.png"))
        self.btn_batdau_vuong.setIconSize(QtCore.QSize(35, 35))

        self.btn_batdau_tron.clicked.connect(self.ThucThi_tron)
        self.btn_batdau_tron.clicked.connect(self.ReloadData)
        self.btn_batdau_tron.setIcon(QIcon("_data_\\icon\\icons8-circled-thin-48.png"))
        self.btn_batdau_tron.setIconSize(QtCore.QSize(35, 35))

        self.btn_batdau_face.clicked.connect(self.ThucThi_face)
        self.btn_batdau_face.clicked.connect(self.ReloadData)
        self.btn_batdau_face.setIcon(QIcon("_data_\\icon\\icons8-npc-face-48.png"))
        self.btn_batdau_face.setIconSize(QtCore.QSize(35, 35))

        self.thanh_dieuchinh.valueChanged.connect(self.CuongDo)
        self.SetViewCuongDo(5)
        self.point_x.textChanged.connect(self.DemoIMG)
        self.point_y.textChanged.connect(self.DemoIMG)
        self.size_che.textChanged.connect(self.DemoIMG)
        self.thanh_dieuchinh.valueChanged.connect(self.DemoIMG)

        self.path_folder.textChanged.connect(self.AddItemToListMain)
        self.path_folder_out.textChanged.connect(self.SaveOutFolder)
        self.btn_in.clicked.connect(self.SelectIn)
        self.btn_in.setIcon(QIcon("_data_\\icon\\icons8-documents-folder-48.png"))
        self.btn_in.setIconSize(QtCore.QSize(45, 45))
        self.btn_in.setToolTip("Chọn thư mục")
        self.btn_out.clicked.connect(self.SelectOut)
        self.btn_out.setIcon(QIcon("_data_\\icon\\icons8-documents-folder-48.png"))
        self.btn_out.setIconSize(QtCore.QSize(45, 45))
        self.btn_out.setToolTip("Chọn thư mục xuất ảnh")
        self.btnSave.clicked.connect(self.SetSaveIMG)
        self.btnSave.setIcon(QIcon("_data_\\icon\\icons8-save-as-48.png"))
        self.btnSave.setIconSize(QtCore.QSize(45, 45))
        self.btnSave.setToolTip("Lưu vị trí")
        self.btnDelete.clicked.connect(self.SetDeleIMG)
        self.btnDelete.setIcon(QIcon("_data_\\icon\\icons8-remove-64.png"))
        self.btnDelete.setIconSize(QtCore.QSize(45, 45))
        self.btnDelete.setToolTip("Xoá vị trí")

        self.btnNext.clicked.connect(self.nextIMG)
        self.btnNext.setIcon(QIcon("_data_\\icon\\icons8-next-page-50.png"))
        self.btnNext.setIconSize(QtCore.QSize(45, 45))
        self.btnNext.setToolTip("Ảnh tiếp theo")

        self.btnBack.clicked.connect(self.backIMG)
        self.btnBack.setIcon(QIcon("_data_\\icon\\icons8-left-50.png"))
        self.btnBack.setIconSize(QtCore.QSize(45, 45))
        self.btnBack.setToolTip("Ảnh trước")

        self.btnReload.clicked.connect(self.ReloadData)
        self.btnReload.setIcon(QIcon("_data_\\icon\\refresh.png"))
        self.btnReload.setIconSize(QtCore.QSize(45, 45))
        self.btnReload.setToolTip("Reload dữ liệu")


        self.DelteListFileBut.clicked.connect(self.DelteListFile)
        self.DelteListFileBut.setIcon(QIcon("_data_\\icon\\remove-file.png"))
        self.DelteListFileBut.setIconSize(QtCore.QSize(45, 45))
        self.DelteListFileBut.setToolTip("Xoá ảnh")

        self.ListFile.itemClicked.connect(self.Clicked_Selec)





    def nextIMG(self):
        global countIMG, MaxIMG
        if countIMG + 1 >= MaxIMG:
            QMessageBox.information(self, "Thông báo", "Không có ảnh ở phía trước")
            return False
        countIMG += 1
        self.DemoIMG()

    def backIMG(self):
        global countIMG, MaxIMG
        if countIMG - 1 < 0:
            QMessageBox.information(self, "Thông báo", "Không có ảnh ở phía sau")
            return False
        countIMG -= 1
        self.DemoIMG()

    def ReloadData(self):
        if ListFileRun != []:
            self.point_x.setText(str(0))
            self.point_y.setText(str(0))
            self.size_che.setText(str(0))
        else:
            print("List file rong")

    def SetSaveIMG(self):
        global _LinkIMG_, linkcache, ViTriXY, LinkSaveIMG, XYTam
        if len(XYTam) > 0:
            ViTriXY.append(XYTam[len(XYTam) - 1])
            QMessageBox.information(self, "Thông báo", "Lưu thành công vị trí thứ " + str(len(ViTriXY)))
        else:
            QMessageBox.information(self, "Thông báo", "Lỗi lưu vị trí hoặc không tồn tại vị trí")
    def SetDeleIMG(self):
        global ViTriXY
        if len(ViTriXY) > 0:
            print("Xoa vi tri")
            ViTriXY.pop(len(ViTriXY) - 1)
            QMessageBox.information(self, "Thông báo", "Đã xoá vị trí gần nhất")
        else:
            QMessageBox.information(self, "Thông báo", "Lỗi xoá vị trí hoặc không tồn tại vị trí")

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

    def convert_cv_qt(self, cv_img, err = False):
        try:
            import cv2
            height, width, channel = cv_img.shape
            bytesPerLine = 3 * width
            qImg = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            return qImg
        except Exception as ex:
            print("conver", ex)
            if err == True:
                QMessageBox.information(self, "Thông báo", "Vi trí che không phù hợp với ảnh")
            return "ERR"

    def AddItemToListMain(self):
        global ListFileRun
        self.BatDauLoad()
        path_Folder = str(self.path_folder.text())
        FileIMG = CheAnh.GetIMGinFloderDEmo(path_Folder)
        ListFileRun.clear()
        for i in FileIMG:
            ListFileRun.append([i, os.path.split(i)[-1]])
        print("Run demo")
        self.DemoIMG()
        self.DungLoad()


    def DemoIMG(self, Click = False):
        try:
            import cv2
            global _LinkIMG_, linkcache, IMGXuLy, ViTriXY, countIMG, MaxIMG, ListFileRun
            print("Lits file run", ListFileRun)
            if Click == False:
                self.ListFile.clear()
                for i in ListFileRun:
                    self.ListFile.addItem(i[1])

            FileIMG = ListFileRun[countIMG][0]
            MaxIMG = len(ListFileRun)
            CuongDo = self.thanh_dieuchinh.value()
            X = int(self.point_x.text())
            Y = int(self.point_y.text())
            R = int(self.size_che.text())
            if X == 0 and Y == 0 and R == 0 and ListFileRun != []:
                X, Y, R = 10, 10, 10
            if X > 0 and Y > 0 and R > 0 and ListFileRun != []:
                try:
                    # VUONG
                    IMGXuLy = CheAnh.CheAnh(X, Y, R, FileIMG, 1, CuongDo)
                    if len(ViTriXY) > 0:
                        for i in ViTriXY:
                            IMGXuLy = CheAnh.CheAnh(i[0], i[1], i[2], IMGXuLy, 1, CuongDo, True)
                    IMGVUONG_ = self.convert_cv_qt(IMGXuLy, True)
                    self.ShowImg_Vuong(IMGVUONG_)
                    # FACE
                    FileIMG = os.path.split(FileIMG)[-1]
                    cv2.imwrite(str(CheAnh.path()) + "\\_data_\\img_out_demo\\" + FileIMG, IMGXuLy)
                    for i in CheAnh.GetXyFace(str(CheAnh.path()) + "\\_data_\\img_out_demo\\" + FileIMG):
                        IMGXuLy = CheAnh.CheAnh(i[0], i[1], i[2], IMGXuLy, 1, CuongDo, True)
                    IMGFACE_ = self.convert_cv_qt(IMGXuLy)
                    self.ShowImg_Face(IMGFACE_)

                except Exception as ex:
                    print("demo load", ex)
                    # self.point_x.setText(str(0))
                    # self.point_y.setText(str(0))
                    # self.size_che.setText(str(0))
        except Exception as ex:
            try:
                self.ShowImg_Vuong("_data_\\er.png")
                self.ShowImg_Face("_data_\\er.png")
            except Exception as ex:
                print(ex)
            print(ex)
    def Clicked_Selec(self, item):
        global selectFile, countIMG, ListFileRun
        selectFile = countIMG = self.ListFile.row(item)
        print("Click ", countIMG)
        self.ListFile.clear()
        countSelec = 0
        from PyQt5.QtCore import Qt
        for a in ListFileRun:
            a = a[1]
            if countSelec == countIMG:
                print("set bac", a)
                item = QListWidgetItem(str(a))
                item.setForeground(Qt.red)
                self.ListFile.addItem(item)
            else:
                print("Bo qua")
                self.ListFile.addItem(a)
            countSelec += 1
        self.DemoIMG(True)


    def DelteListFile(self):
        try:
            global selectFile, ListFileRun
            self.ListFile.takeItem(selectFile)
            ListFileRun.pop(selectFile)
            self.DemoIMG()
        except:
            QMessageBox.information(self, "Thông báo", "Lỗi xoá danh sách ảnh")
            print("Loi xoa slec")

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
        size_W, size_H = 442, 499
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
            global _LinkIMG_, linkcache, IMGXuLy, folderOut, ViTriXY

            # bat dau  ###

            if len(ListFileRun) <= 0:
                QMessageBox.information(self, "Thông báo", "Không có file để thực thi")
                return False
            self.BatDauLoad()
            FileIMG = []
            for i in ListFileRun:
                FileIMG.append(i[0])

            from datetime import datetime
            now = datetime.now()
            if folderOut != "" and len(folderOut) > 3:
                path_ = folderOut
            else:
                path_ = str(CheAnh.path()) + "\\_data_\\img_out\\" + str(now.strftime("%m-%d-%Y_%H"))
                path_ = path_ + "\\VUONG"
                CheAnh.TaoThuMuc(str(path_))

            CuongDo = self.thanh_dieuchinh.value()
            X = int(self.point_x.text())
            Y = int(self.point_y.text())
            R = int(self.size_che.text())
            if X == 0 and Y == 0 and R == 0 and ListFileRun != []:
                X, Y, R = 10, 10, 10
            if X > 0 and Y > 0 and R > 0 and ListFileRun != []:
                LogERR = []
                for a in FileIMG:
                    FileIMG = a
                    try:
                        # VUONG
                        IMGXuLy = CheAnh.CheAnh(X, Y, R, FileIMG, 1, CuongDo)
                        if len(ViTriXY) > 0:
                            for i in ViTriXY:
                                IMGXuLy = CheAnh.CheAnh(i[0], i[1], i[2], IMGXuLy, 1, CuongDo, True)

                        if len(IMGXuLy) <= 0:
                            LogERR.append("\n" + "ANH :\t" + FileIMG + "\t Co loi bo qua" + "\n")
                        else:
                            FileIMG = os.path.split(FileIMG)[-1]
                            cv2.imwrite(path_ + "\\" + str(FileIMG), IMGXuLy)
                            print("SIZE", os.path.getsize(path_ + "\\" + str(FileIMG)))

                    except Exception as ex:
                        print("Loi xuat", ex)
                        LogERR.append("\n" + "ANH :\t" + FileIMG + "\t Co loi bo qua" + "\n")
                        continue
                # hoan thanh ####
                self.DungLoad()
                QMessageBox.information(self, "Thông báo", "Hoàn thành che ảnh")
                if len(LogERR) > 0:
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
            global _LinkIMG_, linkcache, IMGXuLy, folderOut, ViTriXY

            # bat dau  ###

            if len(ListFileRun) <= 0:
                QMessageBox.information(self, "Thông báo", "Không có file để thực thi")
                return False
            self.BatDauLoad()

            FileIMG = []
            for i in ListFileRun:
                FileIMG.append(i[0])

            from datetime import datetime
            now = datetime.now()
            if folderOut != "" and len(folderOut) > 3:
                path_ = folderOut
            else:
                path_ = str(CheAnh.path()) + "\\_data_\\img_out\\" + str(now.strftime("%m-%d-%Y_%H"))
                path_ = path_ + "\\FACE"
                CheAnh.TaoThuMuc(str(path_))

            CuongDo = self.thanh_dieuchinh.value()
            X = int(self.point_x.text())
            Y = int(self.point_y.text())
            R = int(self.size_che.text())
            if X == 0 and Y == 0 and R == 0 and ListFileRun != []:
                X, Y, R = 10, 10, 10
            if X > 0 and Y > 0 and R > 0 and ListFileRun != []:
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
                            IMGXuLy = CheAnh.CheAnh(i[0], i[1], i[2], IMGXuLy, 1, CuongDo, True)

                        if len(IMGXuLy) <= 0:
                            LogERR.append("\n" + "ANH :\t" + FileIMG + "\t Co loi bo qua" + "\n")
                        else:
                            cv2.imwrite(path_ + "\\" + str(FileIMG), IMGXuLy)
                            print("SIZE", os.path.getsize(path_ + "\\" + str(FileIMG)))


                    except Exception as ex:
                        print(ex)
                        LogERR.append("\n" + "ANH :\t" + FileIMG + "\t Co loi bo qua" + "\n")
                # hoan thanh ####
                self.DungLoad()
                QMessageBox.information(self, "Thông báo", "Hoàn thành che ảnh")
                if len(LogERR) > 0:
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
            global _LinkIMG_, linkcache, IMGXuLy, folderOut, ViTriXY

            # bat dau  ###

            if len(ListFileRun) <= 0:
                QMessageBox.information(self, "Thông báo", "Không có file để thực thi")
                return False
            self.BatDauLoad()

            FileIMG = []
            for i in ListFileRun:
                FileIMG.append(i[0])
            from datetime import datetime
            now = datetime.now()
            if folderOut != "" and len(folderOut) > 3:
                path_ = folderOut
            else:
                path_ = str(CheAnh.path()) + "\\_data_\\img_out\\" + str(now.strftime("%m-%d-%Y_%H"))
                path_ = path_ + "\\TRON"
                CheAnh.TaoThuMuc(str(path_))

            CuongDo = self.thanh_dieuchinh.value()
            X = int(self.point_x.text())
            Y = int(self.point_y.text())
            R = int(self.size_che.text())
            if X == 0 and Y == 0 and R == 0 and ListFileRun != []:
                X, Y, R = 10, 10, 10
            if X > 0 and Y > 0 and R > 0 and ListFileRun != []:
                LogERR = []
                for a in FileIMG:
                    FileIMG = a
                    try:
                        # TRON
                        IMGXuLy = CheAnh.CheAnh(X, Y, R, FileIMG, 2, CuongDo)
                        if len(ViTriXY) > 0:
                            for i in ViTriXY:
                                IMGXuLy = CheAnh.CheAnh(i[0], i[1], i[2], IMGXuLy, 2, CuongDo, True)

                        if len(IMGXuLy) <= 0:
                            LogERR.append("\n" + "ANH :\t" + FileIMG + "\t Co loi bo qua" + "\n")
                        else:
                            FileIMG = os.path.split(FileIMG)[-1]
                            cv2.imwrite(path_ + "\\" + str(FileIMG), IMGXuLy)
                            print("SIZE", os.path.getsize(path_ + "\\" + str(FileIMG)))

                    except Exception as ex:
                        print(ex)
                        LogERR.append("\n" + "ANH :\t" + FileIMG + "\t Co loi bo qua" + "\n")
                # hoan thanh ####
                self.DungLoad()
                QMessageBox.information(self, "Thông báo", "Hoàn thành che ảnh")
                if len(LogERR) > 0:
                    strLOG = ""
                    for i in LogERR:
                        strLOG += i
                    ScrollMessageBox(QMessageBox.Critical, "Có lỗi !", strLOG)
                os.startfile(path_)
        except Exception as ex:
            print(ex)


def Main():
    CheAnh.TaoThuMuc('_data_\\img_out')
    CheAnh.TaoThuMuc('_data_\\img_out_demo')
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    Main()