
from pynput.mouse import Button, Controller
import time
import json
import os
import subprocess

mouse = Controller()

sleepTimeBetweenEvents = 3

def convertToInt(x):
    return int(x)


def calibrate():

    boxes = subprocess.Popen(['../../swift-calibrator/swift-calibrator'])

    output = boxes.stdout.decode('utf-8')

        # Parse the JSON output
    try:
        json_data = json.loads(output)
    except json.JSONDecodeError:
        print("Error decoding JSON from the output")
        json_data = None

    print("Hover over the top left of the title bounding box...")
    time.sleep(sleepTimeBetweenEvents)
    topLeftTitlePos = tuple(map(convertToInt,mouse.position))
    print(f"Captured: {topLeftTitlePos}")
    os.system('say "Good."')


    # print("Hover over the top left of the percent speed bounding box...")
    # time.sleep(sleepTimeBetweenEvents)
    # topLeftSpeedPos = tuple(map(convertToInt,mouse.position))
    # print(f"Captured: {topLeftSpeedPos}")
    # os.system('say "Good."')


    # print("Hover over the top left of the elapsed time bounding box...")
    # time.sleep(sleepTimeBetweenEvents)
    # topLeftElapsedTimePos = tuple(map(convertToInt,mouse.position))
    # print(f"Captured: {topLeftElapsedTimePos}")
    # os.system('say "Good."')


    # print("Hover over the top left of the original BPM bounding box...")
    # time.sleep(sleepTimeBetweenEvents)
    # topLeftBPMPos = tuple(map(convertToInt,mouse.position))
    # print(f"Captured: {topLeftElapsedTimePos}")
    # os.system('say "Good."')



    # deckBoundingBoxes =  {
    #     "titlePos" : {'topLeft': topLeftTitlePos, 'bottomRight': bottomRightTitlePos},
    #     "percentSpeedPos" : { 'topLeft': topLeftSpeedPos, 'bottomRight': bottomRightSpeedPos},
    #     "elapsedTimePos" : {'topLeft': topLeftElapsedTimePos, 'bottomRight': bottomRightElapsedTimePos},
    #     "originalBPM" : {'topLeft': topLeftBPMPos, 'bottomRight': bottomRightBPMPos}
    # }

    # return deckBoundingBoxes


def main():
        print("Hello. Welcome to the calibrator. You will have 3 seconds between each mouse position")
        print("Ready?")
        # os.system('say "Beginning Calibration."')

        print("First, we will calibrate the left deck...")

        leftDeck = calibrate()

        # print(leftDeck)

        # print("Next, we will calibrate the right deck...")

        # rightDeck = calibrate()

        # print(leftDeck)
        # print(rightDeck)

        # return json.dumps({
        #      'left_deck': leftDeck,
        #      'right_deck': rightDeck
        # })


if __name__ == "__main__":
     
    new_mouse_positions = main()
    shouldISave = input("Should we save these results? Y/n:")
    if shouldISave == 'Y':
        file_out = open('./DECK_MOUSE_POS.json', 'w')
        file_out.write(new_mouse_positions)
        file_out.close()
