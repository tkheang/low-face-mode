# dim the computer screen when not looking at it with opencv

from cv2 import cv2
import osascript
import argparse
import platform
from subprocess import call
from custom_recognition.recognize_faces_video import get_name

# if running on Linux, load linux scripts
if platform.system() == 'Linux':

    with open("linux_scripts/brighten.sh") as f:
        brighten_script = f.read()

    with open("linux_scripts/dim.sh") as f:
        dim_script = f.read()

# if running on MacOS, load apple scripts
elif platform.system() == 'Darwin':

    with open("scripts/brighten.applescript") as brighten:
        brighten_script = brighten.read()

    with open("scripts/dim.applescript") as dim:
        dim_script = dim.read()

# if running on Windows, load windows scripts
elif platform.system() == 'Windows':

    with open("windows_scripts/brighten.bat") as f:
        brighten_script = f.read()
    
    with open("windows_scripts/dim.bat") as f:
        dim_script = f.read()

def dim():

    if platform.system() == 'Linux':
        call(dim_script, shell=True)

    elif platform.system() == 'Darwin':
        osascript.osascript(dim_script)

    elif platform.system() == 'Windows':
        call(dim_script, shell=True)

def brighten():

    if platform.system() == 'Linux':
        call(brighten_script, shell=True)

    elif platform.system() == 'Darwin':
        osascript.osascript(brighten_script)

    elif platform.system() == 'Windows':
        call(brighten_script, shell=True)

face_cascade = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")

capture = cv2.VideoCapture(0)

face_counter = []
frames = 0
dimmed = False

while True:
    _, img = capture.read()
    frames += 1
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    face_counter.append(len(faces))

    users, verified_users, rec = get_name(img)

    if frames > 20:

        if dimmed == False:
            if 1 not in face_counter[frames - 20 : frames] or (
                (bool(set(users) & set(verified_users)) == False) and rec == True
            ):
                dim()
                dimmed = True

        if dimmed == True:
            if rec == True:
                if set(users) & set(verified_users):
                    if 1 in face_counter[frames - 20 : frames]:
                        brighten()
                        dimmed = False
            else:
                if 1 in face_counter[frames - 20 : frames]:
                    brighten()
                    dimmed = False

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("Low Face Mode On", img)
    k = cv2.waitKey(30) & 0xFF
    if k == 27 or k == 113:
        break

capture.release()
cv2.destroyAllWindows()
