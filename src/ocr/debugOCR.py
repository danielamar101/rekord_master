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


# while True:
    # subprocess.run(['screencapture','-R57,283,600,21','./song1Name.png'], capture_output=True, text=True, cwd=os.getcwd())
    # imagePath = os.path.join(os.getcwd(),'song1Name.png')
    # deck1Name = pytesseract.image_to_string(Image.open(imagePath)).strip()

imagePath='/Users/danielamar/Desktop/Code/music_master/rekord2song/src/ocr/song2BPM.png'
showBoxAroundWords(imagePath)


print("Text is:")
print(pytesseract.image_to_string(Image.open(imagePath)).strip())

originalImage = cv2.imread(imagePath)
grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
thresh_img = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
print(pytesseract.image_to_string(thresh_img,config='--psm 7 --oem 3'))
# Converting grey image to binary image by Thresholding


cv2.imwrite('/Users/danielamar/Desktop/Code/music_master/rekord2song/src/ocr/song2BPMModded.png',thresh_img)
# showBoxAroundWords(imagePath)

time.sleep(10)
#os.remove(imagePath)


