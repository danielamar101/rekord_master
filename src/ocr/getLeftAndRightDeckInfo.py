from PIL import Image
import subprocess
import os
import pytesseract

from .calibrate_full import main as calibrate
import time
import json



def loadAndFireCoordinates():
    file_in = open('/Users/danielamar/Desktop/Code/music_master/rekord2song/src/ocr/DECK_MOUSE_POS.json', 'r')
    decks = json.load(file_in)

    rawCoordinates = []

    for deck,attributes in decks.items():
        for attribute,boundingVertices in attributes.items():
            #print(f"{deck}: {attribute} {boundingVertices} ")
            for topOrBottom, coordinates in boundingVertices.items():
                rawCoordinates.append(coordinates)

    toReturn = jsonToScreenCaptureFormat(rawCoordinates)
    return toReturn

def jsonToScreenCaptureFormat(coordinates):
    toReturn = []

    for i in range(1, len(coordinates),2):
        
        topLeftX, topLeftY = coordinates[i-1]
        bottomRightX, bottomRightY = coordinates[i] 
        width = bottomRightX - topLeftX
        height = bottomRightY - topLeftY

        toReturn.append(f'-R{topLeftX},{topLeftY},{width},{height}')
    
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
    deck1ElapsedTime = pytesseract.image_to_string(Image.open(imagePath)).strip()
    # print(deck1ElapsedTime)
    os.remove(imagePath)

    return [deck1Name,deck1ElapsedTime,deck1PercentSpeed]

def getRightDeck():
    coordinates = loadAndFireCoordinates()

    # Song name
    subprocess.run(['screencapture',coordinates[3],'./song2Name.png'], capture_output=True, text=True, cwd=os.getcwd())
    imagePath = os.path.join(os.getcwd(),'song2Name.png')
    deck2Name = pytesseract.image_to_string(Image.open(imagePath)).strip()
    # print(deck2Name)
    os.remove(imagePath)

    subprocess.run(['screencapture',coordinates[4],'./song2PercentSpeed.png'], capture_output=True, text=True, cwd=os.getcwd())
    imagePath = os.path.join(os.getcwd(),'song2PercentSpeed.png')
    deck2PercentSpeed = pytesseract.image_to_string(Image.open(imagePath)).strip()
    # print(deck2PercentSpeed)
    os.remove(imagePath)

    subprocess.run(['screencapture',coordinates[5],'./song2ElapsedTime.png'], capture_output=True, text=True, cwd=os.getcwd())
    imagePath = os.path.join(os.getcwd(),'song2ElapsedTime.png')
    deck2ElapsedTime = pytesseract.image_to_string(Image.open(imagePath)).strip()
    # print(deck2ElapsedTime)
    os.remove(imagePath)

    return [deck2Name,deck2ElapsedTime,deck2PercentSpeed]

if __name__ == "__main__":

    def calibrateScreenCoords():
        try:   
            print(os.environ['CALIBRATE'])
            if (os.environ['CALIBRATE'] == 'true'):
                new_mouse_positions = calibrate()
                file_out = open('./DECK_MOUSE_POS.json', 'w')
                file_out.write(new_mouse_positions)
                file_out.close()
            else:
                print('Correct env var was not set. Not calibrating.')
            
        except KeyError as e:
            print("CALIBRATIONS env var is not set. will not calibrate.")
            pass

    calibrateScreenCoords()

    time.sleep(3)
    print(getLeftDeck())
    print(getRightDeck())






