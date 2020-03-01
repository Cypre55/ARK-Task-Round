import cv2
import numpy as np


image = '1.png'
img = cv2.imread(image, 1)
img_orig = img.copy()
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img1 = cv2.GaussianBlur(img, (7, 7), 0)
#
# dst = cv2.Canny(img1, 50, 200, None, 3)
# edges = cv2.Canny(img1, 75, 150)
# lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40, maxLineGap=30)
# cv2.imshow("detected circles", img1)
# cv2.imshow("detected circles", edges)

# X1, Y1, X2, Y2 = 0, 0, 0, 0
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     print(f"({x1}, {y1}), ({x2}, {y2})")
#     X1 += x1/2
#     Y1 += y1/2
#     X2 += x2/2
#     Y2 += y2/2
#
# X1 = int(X1)
# Y1 = int(Y1)
# X2 = int(X2)
# Y2 = int(Y2)
#
# WIDTH, HEIGHT = img.shape
#
# print(WIDTH, " ", HEIGHT)
#
# cv2.line(img_orig, (X1, Y1), (X2, Y2), (0, 255, 0), 2)
#
all_circs = cv2.HoughCircles(img1, cv2.HOUGH_GRADIENT, 1, 120,
                             param1=100, param2=30, minRadius=0, maxRadius=0)
all_circs_rounded = np.uint16(np.around(all_circs))
#
#
# print(all_circs_rounded[0])
# print(all_circs_rounded.shape)
# print(all_circs_rounded.shape[1])
#
count = 1
for i in all_circs_rounded[0, :]:
    cv2.circle(img_orig, (i[0], i[1]), i[2], 50, 200, 200, 15)
    cv2.circle(img_orig, (i[0], i[1]), 2, 255, 0, 0, 15)
    # cv2.putText(img_orig, "Coin "+str(count), (i[0], i[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 0, 0, 2)
    count += 1

cv2.imshow("detected circles", img_orig)
cv2.waitKey(0)
cv2.destroyAllWindows()
