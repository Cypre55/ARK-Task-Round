import cv2
import sys
from os import path


cascPath1 = "haarcascade_frontalface_alt.xml"
cascPath = "haarcascade_eye.xml"
eyeCascade = cv2.CascadeClassifier(cascPath)
faceCascade = cv2.CascadeClassifier(cascPath1)


def isHigher(a, b):

    if a > b + 10:
        return a - b - 10, "DOWN"
    elif a < b - 10:
        return b - 10 - a, "UP"
    else:
        return b, "SAME"


def comp(a, b):
    if a[1] == b[1]:
        return a[1]
    else:
        if a[0] > b[0]:
            return a[1]
        else:
            return b[1]


video_capture = cv2.VideoCapture(0)

i = 0
j = 0
k = 0
fuavg = 0
fdavg = 0
euavg = 0
edavg = 0

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.FONT_HERSHEY_SIMPLEX
    )

    eyes = eyeCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.FONT_HERSHEY_SIMPLEX
    )

    if i < 100:
        if len(faces) > 0:
            fuavg += (faces[0][1] + faces[0][3]) / 100
            fdavg += faces[0][1] / 100
            i += 1

    if j < 100:
        if len(eyes) > 0:
            euavg += (eyes[0][1] + eyes[0][3]) / 100
            edavg += (eyes[0][1]) / 100
            j += 1

    if i == 100 and k == 0 and j == 100:
        favg = round((fuavg + fdavg) / 2)
        eavg = round((euavg + edavg) / 2)
        print(f"Face upper avg {fuavg}")
        print(f"Face lower avg {fdavg}")
        print(f"Eye upper avg {euavg}")
        print(f"Eye lower avg {edavg}")
        print(f"Face avg {favg}")
        print(f"Eye avg {eavg}")
        k += 1

    if k == 1:
        if len(eyes) > 0:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cure = (eyes[0][1] + eyes[0][3] + eyes[0][1]) / 2
            action = isHigher(cure, eavg)
            print(action[1])
            with open("Pipe", 'w') as f:
                f.write(action[1])

        elif len(faces) > 0:
            curf = (faces[0][1] + faces[0][3] + faces[0][1]) / 2
            action = isHigher(curf, favg)
            print(action[1])
            with open("Pipe", 'w') as f:
                f.write(action[1])

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    for (x, y, w, h) in eyes:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
