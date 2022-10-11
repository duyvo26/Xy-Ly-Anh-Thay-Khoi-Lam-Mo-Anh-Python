import math
import cv2
import matplotlib.pyplot as plt
import numpy as np

# LOAD 1: vuong; LOAD 2 tron
def CheAnh(x, y, size, path_img, LOAD):
    image_r = cv2.imread(path_img)
    h_max, w_max, c = image_r.shape
    print('width:  ', w_max)
    print('height: ', h_max)
    print('channel:', c)
    leftTop = (x, y)
    LeftToRight_TopToBottom = (size, size)
    R = LeftToRight_TopToBottom[0]
    x, y = leftTop[0], leftTop[1]
    w, h = LeftToRight_TopToBottom[0], LeftToRight_TopToBottom[1]
    if x > w_max or y > h_max:
        print("Loi kich thuoc anh")
    elif w > w_max or h > h_max:
        print("Loi kich thuoc anh")
    elif LOAD == 1:
        image = image_r
        # lay vung ra ra hinh vuong
        # ROI = image[y:y + h, x:x + w]
        # blur = cv2.GaussianBlur(ROI, (101, 101), 0)
        # blur = cv2.medianBlur(ROI, 21)
        # blur = cv2.blur(ROI, (101,101) )
        ROI = image[y:y + h, x:x + w]
        size_IMG = (ROI.shape[1], ROI.shape[0])
        temp = cv2.resize(ROI, (30, 30), interpolation=cv2.INTER_NEAREST)
        blur = cv2.resize(temp, size_IMG, interpolation=cv2.INTER_NEAREST)
        # add lam mo vao anh11
        image[y:y + h, x:x + w] = blur

        cv2.imshow("img", image)
        cv2.waitKey()

    elif LOAD == 2:
        ROI = image_r.copy()
        maskShape = (image_r.shape[0], image_r.shape[1], 1)
        mask = np.full(maskShape, 0, dtype=np.uint8)
        cv2.circle(ROI, (int((x + x + w) / 2), int((y + y + h) / 2)), int(R / 2), (255, 255, 255), 0)
        # lay vung ra ra tron
        # tempImg = cv2.GaussianBlur(tempImg, (51, 51), 0)
        # ROI = image[y:y + h, x:x + w]
        # blur = cv2.GaussianBlur(ROI, (101, 101), 0)
        # blur = cv2.medianBlur(ROI, 21)
        # blur = cv2.blur(ROI, (101,101) )
        size_IMG = (ROI.shape[1], ROI.shape[0])
        temp = cv2.resize(ROI, (60, 60), interpolation=cv2.INTER_NEAREST)
        tempImg = cv2.resize(temp, size_IMG, interpolation=cv2.INTER_NEAREST)

        cv2.circle(mask, (int((x + x + w) / 2), int((y + y + h) / 2)), int(R / 2), 255, -1)
        mask_inv = cv2.bitwise_not(mask)
        img1_bg = cv2.bitwise_and(image_r, image_r, mask=mask_inv)
        img2_fg = cv2.bitwise_and(tempImg, tempImg, mask=mask)
        dst = cv2.add(img1_bg, img2_fg)

        cv2.imshow("img", dst)
        cv2.waitKey()
