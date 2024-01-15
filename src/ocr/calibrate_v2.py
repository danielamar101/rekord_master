
from pynput.mouse import Button, Controller
import time
import json
import os
import subprocess

mouse = Controller()

sleepTimeBetweenEvents = 3

def convertToInt(x):
    return int(x)

last_json = ''
def watch_file_and_return_new_json():
    global last_json
    file_name = './Coordinates.json'
    # Clear file
    with open(file_name, 'w') as file:
        pass
    last_size = os.path.getsize(file_name)
    while True:
        current_size = os.path.getsize(file_name)
        # print(f'current size: {current_size}, last size is: {last_size}')
        if current_size != last_size:
            with open(file_name, 'r') as file:
                try:
                    new_json = json.load(file)
                    latest_coordinate = ''
                    if(new_json != last_json):
                        latest_coordinate = new_json[len(new_json)-1]

                        last_json = new_json
                        return latest_coordinate
                    #return new_json
                except json.JSONDecodeError:
                    # In case the new content is not a valid JSON object
                    pass
        last_size = current_size
        time.sleep(1)  # Wait for 1 second before checking the file again



def calibrate():

    boxes = subprocess.Popen(['../../swift-calibrator/swift-calibrator'])


    print("Hover over the title bounding box...")
    title_bounding_box = watch_file_and_return_new_json()
    print(f"Captured: {title_bounding_box}")
    os.system('say "Good."')

    print("Hover over the percent speed bounding box...")
    percent_speed_box = watch_file_and_return_new_json()
    print(f"Captured: {percent_speed_box}")
    os.system('say "Good."')

    print("Hover over the elapsed time bounding box...")
    elapsed_time = watch_file_and_return_new_json()
    print(f"Captured: {elapsed_time}")
    os.system('say "Good."')

    print("Hover over the original BPM bounding box...")
    original_bpm = watch_file_and_return_new_json()
    print(f"Captured: {original_bpm}")
    os.system('say "Good."')

    boxes.kill()
    
    deck_boxes =  {
        "title_pos" : title_bounding_box,
        "percent_speed_box" : percent_speed_box,
        "elapsed_time_box" : elapsed_time,
        "original_bpm_box" : original_bpm
    }

    return deck_boxes


def main():
        print("Hello. Welcome to the calibrator. ")
        print("Ready?")
        os.system('say "Beginning Calibration."')

        print("First, we will calibrate the left deck...")

        leftDeck = calibrate()

        print(leftDeck)

        print("Next, we will calibrate the right deck...")

        rightDeck = calibrate()

        # print(leftDeck)
        print(rightDeck)

        return {
             'left_deck': leftDeck,
             'right_deck': rightDeck
        }


if __name__ == "__main__":
     
    new_bounding_boxes = main()
    # boxes = subprocess.Popen(['../../swift-calibrator/swift-calibrator'])


    shouldISave = input("Should we save these results? Y/n:")
    if shouldISave == 'Y':
        file_out = open('./DECK_MOUSE_POS.json', 'w')
        file_out.write(json.dumps(new_bounding_boxes))
        file_out.close()
