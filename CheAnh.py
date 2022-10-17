import os
import pathlib
import cv2
import numpy as np


def path():
    return pathlib.Path().resolve()


# LOAD 1: vuong; LOAD 2 tron
def CheAnh(x, y, size, path_img, LOAD, output, CuongDo):
    image_r = cv2.imread(path_img)
    h_max, w_max, c = image_r.shape
    img_name = "duyvo26_" + os.path.split(path_img)[-1]


    leftTop = (x, y)
    LeftToRight_TopToBottom = (size, size)
    R = LeftToRight_TopToBottom[0]
    x, y = leftTop[0], leftTop[1]
    w, h = LeftToRight_TopToBottom[0], LeftToRight_TopToBottom[1]


    if x > w_max - R or y > h_max - R or w > w_max - R or h > h_max - R:
        # print("Loi kich thuoc anh")
        return False

# 5 - 40
    # hinh vuong
    if LOAD == 1:
        # print("Vung che vuong")
        image = image_r
        ROI = image[y:y + h, x:x + w]
        size_IMG = (ROI.shape[1], ROI.shape[0])
        CuongDo = int((((h_max - (h_max * CuongDo) / 100) / 10) + 10) / 4)
        temp = cv2.resize(ROI, (CuongDo, CuongDo), interpolation=cv2.INTER_NEAREST)
        blur = cv2.resize(temp, size_IMG, interpolation=cv2.INTER_NEAREST)
        image[y:y + h, x:x + w] = blur
        cv2.imwrite(output + "\\" + "(VUONG)_" + img_name, image)
        return output + "\\" + "(VUONG)_" + img_name
    # hinh tron
    if LOAD == 2:
        ROI = image_r.copy()
        maskShape = (image_r.shape[0], image_r.shape[1], 1)
        mask = np.full(maskShape, 0, dtype=np.uint8)
        cv2.circle(ROI, (int((x + x + w) / 2), int((y + y + h) / 2)), int(R / 2), (255, 255, 255), 0)
        size_IMG = (ROI.shape[1], ROI.shape[0])
        CuongDo = int((((h_max - (h_max * CuongDo) / 100) / 10) + 10))
        temp = cv2.resize(ROI, (CuongDo, CuongDo), interpolation=cv2.INTER_NEAREST)
        tempImg = cv2.resize(temp, size_IMG, interpolation=cv2.INTER_NEAREST)
        cv2.circle(mask, (int((x + x + w) / 2), int((y + y + h) / 2)), int(R / 2), 255, -1)
        mask_inv = cv2.bitwise_not(mask)
        img1_bg = cv2.bitwise_and(image_r, image_r, mask=mask_inv)
        img2_fg = cv2.bitwise_and(tempImg, tempImg, mask=mask)
        dst = cv2.add(img1_bg, img2_fg)
        cv2.imwrite(output + "\\" + "(TRON)_" + img_name, dst)
        return output + "\\" + "(TRON)_" + img_name


def GetIMGinFloder(x, y, r, status, folder, output, CuongDo):
    SumFile = 0  # sum file
    LOG_TXT = ""
    for (root, dirs, file) in os.walk(folder):  # lap lay danh sach
        for f in file:
            if ".jpg" in f or ".png" in f or ".webp" in f:
                SumFile += 1
                FileIMG = root + "\\" + f
                try:
                    if CheAnh(x, y, r, FileIMG, status, output, CuongDo) == False:
                        # print("ANH :\t", f, "\t Co loi bo qua")
                        LOG_TXT += "----------------------\n"
                        LOG_TXT += str(SumFile) + "\n" + "ANH :\t" + f + "\t Co loi bo qua" + "\n"
                except Exception as mess:
                    # print("ANH :\t", f, "\t Co loi bo qua")
                    LOG_TXT += "----------------------\n"
                    LOG_TXT += str(SumFile) + "\n" + "ANH :\t" + f + "\t Co loi bo qua" + "\n"
    return LOG_TXT

def GetIMGinFloderDEmo(x, y, r, status, folder, output, CuongDo, coutIMG):
    SumFile = 0  # sum file
    LOG_TXT = ""
    for (root, dirs, file) in os.walk(folder):  # lap lay danh sach
        if coutIMG is None:
            if SumFile > coutIMG:
                break
        for f in file:
            if ".jpg" in f or ".png" in f or ".webp" in f:
                SumFile += 1
                FileIMG = root + "\\" + f
                try:
                    kq = CheAnh(x, y, r, FileIMG, status, output, CuongDo)
                    if  kq== False:
                        return "Co lỗi khi nhập kich thươc ảnh vui lòng thử lại"
                    else:
                        return kq
                except Exception as mess:
                    return False




def InputData(x, y, r, status, input_path, CuongDo):
    yield GetIMGinFloder(x, y, r, status, input_path, str(path()) + "\\img_out", CuongDo)
    yield str(path()) + "\\img_out"

