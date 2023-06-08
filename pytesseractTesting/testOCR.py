from PIL import Image
import subprocess
import os
import cv2

import pytesseract
from pytesseract import Output

result = subprocess.run(['screencapture','-R 57,283,700,39','./input.png'], capture_output=True, text=True, cwd=os.getcwd())
songList = result.stdout.split('\n')

imagePath = os.path.join(os.getcwd(),'input.png')
print(pytesseract.image_to_boxes(Image.open(imagePath)))


img = cv2.imread(imagePath)

d = pytesseract.image_to_data(img, output_type=Output.DICT)
n_boxes = len(d['level'])
for i in range(n_boxes):
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)