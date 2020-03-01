import cv2
import numpy as np
import math


def LandC(image):
    img = cv2.imread(image, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img1 = cv2.GaussianBlur(img, (7, 7), 0)

    edges = cv2.Canny(img1, 75, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40, maxLineGap=30)

    X1, Y1, X2, Y2 = 0, 0, 0, 0
    n = len(lines)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        X1 += x1/n
        Y1 += y1/n
        X2 += x2/n
        Y2 += y2/n

    X1 = int(X1)
    Y1 = int(Y1)
    X2 = int(X2)
    Y2 = int(Y2)

    HEIGHT, WIDTH = img.shape

    all_circs = cv2.HoughCircles(img1, cv2.HOUGH_GRADIENT, 1, 120,
                                 param1=100, param2=30, minRadius=0, maxRadius=0)
    all_circs_rounded = np.uint16(np.around(all_circs))

    circs = list(all_circs_rounded[0])
    for i in range(len(circs)):
        circs[i] = list(circs[i])

    radians = math.atan2(Y1 - Y2, X1 - X2)

    dx = math.cos(radians)
    dy = math.sin(radians)

    print(f"{radians} {dx} {dy}")

    return dx, dy, circs, WIDTH, HEIGHT, X1, Y1, X2, Y2
