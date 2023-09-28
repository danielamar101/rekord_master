# This script is for fixing singular positions without having to go through
# an entire full calibration session



from pynput.mouse import Button, Controller
import time
import json
import os

mouse = Controller()

def convertToInt(x):
    return int(x)

def calibrate():
    print("Hover over the position you would like to record...")
    singularPos = tuple(map(convertToInt,mouse.position))
    print(f"Captured: {singularPos}")
    os.system('say "Good."')

    return singularPos

def main():
        os.system('say "Beginning Partial Calibration."')
        singularPos = calibrate()

        return singularPos


if __name__ == "__main__":
     
    validList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    whichToFix = int(input("Which pos are you trying to fix? (1-16): "))
    if whichToFix not in validList:
         print("Error. Invalid input. Enter a valid number!")
         exit
    
    singularPos = main()

    file_in = open('./DECK_MOUSE_POS.json', 'r')
    decks = json.load(file_in)

    # This large if/else statement does a good job explaining 
    # how the input number affects what position is overwritten
    if whichToFix == 1:
        decks['left_deck']['titlePos']['topLeft'] = singularPos
    elif whichToFix == 2:
        decks['left_deck']['titlePos']['bottomRight'] = singularPos
    elif whichToFix == 3:
        decks['left_deck']['percentSpeedPos']['topLeft'] = singularPos
    elif whichToFix == 4:
        decks['left_deck']['percentSpeedPos']['bottomRight'] = singularPos
    elif whichToFix == 5:
        decks['left_deck']['elapsedTimePos']['topLeft'] = singularPos
    elif whichToFix == 6:
        decks['left_deck']['elapsedTimePos']['bottomRight'] = singularPos
    elif whichToFix == 7:
        decks['left_deck']['originalBPM']['topLeft'] = singularPos
    elif whichToFix == 8:
        decks['left_deck']['originalBPM']['bottomRight'] = singularPos
    elif whichToFix == 9:
        decks['right_deck']['titlePos']['topLeft'] = singularPos
    elif whichToFix == 10:
        decks['right_deck']['titlePos']['bottomRight'] = singularPos
    elif whichToFix == 11:
        decks['right_deck']['percentSpeedPos']['topLeft'] = singularPos
    elif whichToFix == 12:
        decks['right_deck']['percentSpeedPos']['bottomRight'] = singularPos
    elif whichToFix == 13:
        decks['right_deck']['elapsedTimePos']['topLeft'] = singularPos
    elif whichToFix == 14:
        decks['right_deck']['elapsedTimePos']['bottomRight'] = singularPos
    elif whichToFix == 15:
        decks['right_deck']['originalBPM']['topLeft'] = singularPos
    elif whichToFix == 16:
        decks['right_deck']['originalBPM']['bottomRight'] = singularPos
    
    # Write back out!
    file_out = open('./DECK_MOUSE_POS.json', 'w')
    file_out.write(json.dumps(decks))
    file_out.close()
