from PIL import Image
import subprocess
import os
import pytesseract
import time
import json
import cv2

pos_path = ''



def loadAndFireCoordinates():
    global pos_path
    
    file_in = open(pos_path, 'r')
    decks = json.load(file_in)

    rawCoordinates = []

    for deck,box in decks.items():
        for attribute,bounding_box in box.items():
            rawCoordinates.append(bounding_box)

    # print(rawCoordinates)

    toReturn = jsonToScreenCaptureFormat(rawCoordinates)
    return toReturn

def jsonToScreenCaptureFormat(coordinates):
    toReturn = []

    for item in coordinates:
        
        x = str(int(item['x']))
        y = str(int(item['y']))
        width = str(int(item['width']))
        height = str(int(item['height']))

        toReturn.append(f'-R{x},{y},{width},{height}')
    
    return toReturn


def getLeftDeck():
    coordinates = loadAndFireCoordinates()
    print(coordinates)
    # Song name
    subprocess.run(['screencapture',coordinates[0],'./song1Name.png'], capture_output=True, text=True, cwd=os.getcwd())
    imagePath = os.path.join(os.getcwd(),'song1Name.png')
    deck1Name = pytesseract.image_to_string(Image.open(imagePath)).strip()
    # print(deck1Name)
    os.remove(imagePath)

    # Percent speed
    subprocess.run(['screencapture',coordinates[1],'./song1PercentSpeed.png'], capture_output=True, text=True, cwd=os.getcwd())
    imagePath = os.path.join(os.getcwd(),'song1PercentSpeed.png')
    deck1PercentSpeed = pytesseract.image_to_string(Image.open(imagePath)).strip()
    # print(deck1PercentSpeed)
    os.remove(imagePath)

    # Elapsed time
    subprocess.run(['screencapture',coordinates[2],'./song1ElapsedTime.png'], capture_output=True, text=True, cwd=os.getcwd())
    imagePath = os.path.join(os.getcwd(),'song1ElapsedTime.png')
    
    # Some tesseract magic here to help us with gray text for elapsed Time
    originalImage = cv2.imread(imagePath)
    gray_image = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    deck1ElapsedTime = pytesseract.image_to_string(thresh_img,config='--psm 7 --oem 3').strip()
    # print(deck1ElapsedTime)
    os.remove(imagePath)

    # Original BPM
    subprocess.run(['screencapture',coordinates[3],'./song1BPM.png'], capture_output=True, text=True, cwd=os.getcwd())
    imagePath = os.path.join(os.getcwd(),'song1BPM.png')

    # Some tesseract magic here to help us with gray text for original BPM
    originalImage = cv2.imread(imagePath)
    gray_image = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    deck1OriginalBPM = pytesseract.image_to_string(thresh_img,config='--psm 7 --oem 3').strip()

    # print(deck1ElapsedTime)
    os.remove(imagePath)

    return [deck1Name,deck1PercentSpeed, deck1ElapsedTime, deck1OriginalBPM]

def getRightDeck():
    coordinates = loadAndFireCoordinates()

    # Song name
    subprocess.run(['screencapture',coordinates[4],'./song2Name.png'], capture_output=True, text=True, cwd=os.getcwd())
    imagePath = os.path.join(os.getcwd(),'song2Name.png')
    deck2Name = pytesseract.image_to_string(Image.open(imagePath)).strip()
    # print(deck2Name)
    os.remove(imagePath)

    subprocess.run(['screencapture',coordinates[5],'./song2PercentSpeed.png'], capture_output=True, text=True, cwd=os.getcwd())
    imagePath = os.path.join(os.getcwd(),'song2PercentSpeed.png')
    deck2PercentSpeed = pytesseract.image_to_string(Image.open(imagePath)).strip()
    # print(deck2PercentSpeed)
    os.remove(imagePath)

    subprocess.run(['screencapture',coordinates[6],'./song2ElapsedTime.png'], capture_output=True, text=True, cwd=os.getcwd())
    imagePath = os.path.join(os.getcwd(),'song2ElapsedTime.png')
    
    # Some tesseract magic here to help us with gray text for elapsed Time
    originalImage = cv2.imread(imagePath)
    gray_image = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    deck2ElapsedTime = pytesseract.image_to_string(thresh_img,config='--psm 7 --oem 3').strip()
    os.remove(imagePath)

    # Original BPM
    subprocess.run(['screencapture',coordinates[7],'./song2BPM.png'], capture_output=True, text=True, cwd=os.getcwd())
    imagePath = os.path.join(os.getcwd(),'song2BPM.png')
        # Some tesseract magic here to help us with gray text for original BPM
    originalImage = cv2.imread(imagePath)
    gray_image = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    deck2OriginalBPM = pytesseract.image_to_string(thresh_img,config='--psm 7 --oem 3').strip()

    # print(deck1ElapsedTime)
    os.remove(imagePath)

    return [deck2Name,deck2PercentSpeed, deck2ElapsedTime, deck2OriginalBPM]

if __name__ == "__main__":
    pos_path = os.path.join('./DECK_MOUSE_POS1.json')
    print(loadAndFireCoordinates())
    # def calibrateScreenCoords():
    #     try:   
    #         print(os.environ['CALIBRATE'])
    #         if (os.environ['CALIBRATE'] == 'true'):
    #             from calibrate_full import main as calibrate
    #             new_mouse_positions = calibrate()
    #             shouldISave = input("Should we save these results? Y/n:")
    #             if shouldISave == 'Y':
    #                 file_out = open('./DECK_MOUSE_POS.json', 'w')
    #                 file_out.write(new_mouse_positions)
    #                 file_out.close()
    #         else:
    #             print('Correct env var was not set. Not calibrating.')
            
    #     except KeyError as e:
    #         print("CALIBRATIONS env var is not set. will not calibrate.")
    #         pass

    # calibrateScreenCoords()

    # time.sleep(3)
    # print(getLeftDeck())
    # print(getRightDeck())
else: 
    from ocr.calibrate_full import main as calibrate
    pos_path = os.path.join(os.getcwd(),'ocr','DECK_MOUSE_POS.json')
    # calibrate()






