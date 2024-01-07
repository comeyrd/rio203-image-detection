import cv2
import numpy as np
from lib.ocr import path_to_text, most_common


def analyse(path_to_image):
    image = cv2.imread(path_to_image, cv2.IMREAD_COLOR)
    save = image.copy()

    po = image.copy()
    do = (80, 50, 128)
    up = (120, 255, 200)
    mask = cv2.inRange(po, do, up)
    result = cv2.bitwise_and(po, po, mask=mask)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    contours, hier = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
    for c in contours:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.drawContours(image, [box], 0, (0, 255, 0), 1)
        x, w, y, h = box[0][0], box[2][0] - box[0][0], box[0][1], box[2][1] - box[0][1]
        new_img = save[y : y + h, x : x + w]

    a = "analyse.png"
    cv2.imwrite(a, new_img)

    def transform(a):
        from skimage import io, img_as_ubyte, transform as tf

        tab = []
        for she in np.arange(-0.2, 0.2, 0.1):
            img = io.imread(a)
            afine_tf = tf.AffineTransform(shear=she)
            modified = tf.warp(img, inverse_map=afine_tf)
            io.imsave(a, img_as_ubyte(modified))
            text = path_to_text(a)
            tab.append(text)

        return most_common(tab)

    o = transform(a)
    return o
