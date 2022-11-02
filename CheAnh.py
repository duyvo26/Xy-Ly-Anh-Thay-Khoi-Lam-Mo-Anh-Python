import os
import pathlib

import cv2
import numpy as np

BanQuyen = "BQ-duyvo26_"


def path():
    return pathlib.Path().resolve()


def GetXyFace(IMG):
    face_detector = cv2.CascadeClassifier('_data_\\DataSet\\haarcascade_frontalface_default.xml')
    img = cv2.imread(IMG)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray,
                                           scaleFactor=1.3,
                                           minNeighbors=4,
                                           minSize=(30, 30),
                                           flags=cv2.CASCADE_SCALE_IMAGE)
    return faces


def CheAnh(x, y, size, path_img, LOAD, CuongDo, LOOP=False):
    global BanQuyen
    if LOOP == False:
        import numpy
        stream = open(path_img, "rb")
        bytes = bytearray(stream.read())
        numpyarray = numpy.asarray(bytes, dtype=numpy.uint8)
        image_r = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
    else:
        image_r = path_img
    try:
        h_max, w_max, c = image_r.shape

        leftTop = (x, y)
        LeftToRight_TopToBottom = (size, size)
        R = LeftToRight_TopToBottom[0]
        x, y = leftTop[0], leftTop[1]
        w, h = LeftToRight_TopToBottom[0], LeftToRight_TopToBottom[1]
        if x > w_max - R or y > h_max - R or w > w_max or h > h_max:
            print("xl qua kich thuoc")
            return []
        else:
            if LOAD == 1:
                image = image_r
                ROI = image[y:y + h, x:x + w]
                size_IMG = (ROI.shape[1], ROI.shape[0])
                CuongDo = int((((h_max - (h_max * CuongDo) / 100) / 10) + 10) / 4)
                temp = cv2.resize(ROI, (CuongDo, CuongDo), interpolation=cv2.INTER_NEAREST)
                blur = cv2.resize(temp, size_IMG, interpolation=cv2.INTER_NEAREST)
                image[y:y + h, x:x + w] = blur
                return image

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
                return dst
    except Exception as ex:
        return []


def GetIMGinFloderDEmo(folder, point=0):
    point_arr = []
    for (root, dirs, file) in os.walk(folder):  # lap lay danh sach
        for f in file:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                point_arr.append(str(root + "\\" + f))

    return point_arr[point]


def GetIMGinFloderOut(folder):
    point_arr = []
    for (root, dirs, file) in os.walk(folder):  # lap lay danh sach
        for f in file:
            if ".jpg" in f or ".png" in f or ".webp" in f:
                point_arr.append(str(root + "\\" + f))
    return point_arr


def path():
    return pathlib.Path().resolve()


def TaoThuMuc(fileName):
    try:
        from pathlib import Path
        Path(fileName).mkdir(parents=True, exist_ok=True)
    except:
        return True

# cv2.imshow("NameIMG", CheAnh(10, 20, 40, "D:\\USER\\Pictures\\img facebook\\13cadfa.jpg", 1, 90))
# cv2.waitKey(0)
# cv2.destroyAllWindows()
