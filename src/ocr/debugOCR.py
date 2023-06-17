import pytesseract
from pytesseract import Output
import cv2
import subprocess
import time
import os
from PIL import Image
import signal
import sys


def showBoxAroundWords(imagePath):
    img = cv2.imread(imagePath)
    d = pytesseract.image_to_data(img, output_type=Output.DICT)


    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('img', img)

    


def sigterm_handler(signal, frame):
    # save the state here or do whatever you want
    print('booyah! bye bye')
    cv2.destroyAllWindows()
    sys.exit(0)

signal.signal(signal.SIGINT, sigterm_handler)


while True:
    subprocess.run(['screencapture','-R57,283,600,21','./song1Name.png'], capture_output=True, text=True, cwd=os.getcwd())
    imagePath = os.path.join(os.getcwd(),'song1Name.png')
    deck1Name = pytesseract.image_to_string(Image.open(imagePath)).strip()

    showBoxAroundWords(imagePath)
    os.remove(imagePath)

    #   # Percent speed
    # subprocess.run(['screencapture','-R689,443,34,12','./song1PercentSpeed.png'], capture_output=True, text=True, cwd=os.getcwd())
    # imagePath = os.path.join(os.getcwd(),'song1PercentSpeed.png')
    # deck1PercentSpeed = pytesseract.image_to_string(Image.open(imagePath)).strip()
    # # print(deck1PercentSpeed)

    # showBoxAroundWords(imagePath)
    # os.remove(imagePath)

    # # Elapsed time
    # subprocess.run(['screencapture','-R630,302,63,18','./song1ElapsedTime.png'], capture_output=True, text=True, cwd=os.getcwd())
    # imagePath = os.path.join(os.getcwd(),'song1ElapsedTime.png')
    # deck1ElapsedTime = pytesseract.image_to_string(Image.open(imagePath)).strip()
    # # print(deck1ElapsedTime)

    # showBoxAroundWords(imagePath)
    time.sleep(10)
    os.remove(imagePath)


