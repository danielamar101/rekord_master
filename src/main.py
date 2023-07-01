import subprocess
import os
import time
from pynput import keyboard
import signal
import traceback

import pytesseract
from PIL import Image
from ocr.getLeftAndRightDeckInfo import getLeftDeck, getRightDeck
from fuzzywuzzy import fuzz

currentDeckNumber = 1
mainProcess = None
bufferProcess = None

debug = True

def kill_pid(process):        
    """ Check For the existence of a unix pid. """
    print(process)
    try:
        if(hasattr(process,'terminate')):
            process.terminate()
            return True
    except OSError:
        return False
    

    return False

def main(): 
    global currentDeckNumber
    global mainProcess
    global bufferProcess
    global debug

    try:
        checkListener()

        #1. Grab Song info, speed of song, and elapsed time
        deckList = getLeftDeck() if currentDeckNumber == 1 else getRightDeck()

        print(deckList)
        checkListener()

        # Song Name, Percent speed, Elapsed Time, starting bpm
        deckInUse = [deckList[0], elapsedStringTimeToIntegerEpoch(deckList[2]), relativeStringPercentToDecimal(deckList[1], deckList[3])] 
      
        print("")
        print(f'SELECTED DECK #{currentDeckNumber}. CONTAINS: {deckInUse}')
        print("")

        #2 Find song in file directory  
        videoList = os.listdir("./videos")
        filteredVideoList = [video[0:len(video)-4] for video in videoList if video[(len(video)-3):] == 'mp4']
        #print(f'List of videos in videos dir: {filteredVideoList}') 

        # Goal of the following for loop is to find a song path
        selectedVideoPath = ''

        for i in range(len(filteredVideoList)):
            lengthOfSongTitle = len(deckInUse[0])
            currentSong = filteredVideoList[i][0:lengthOfSongTitle]
            fuzzyStringComparisonRatio = fuzz.ratio(deckInUse[0].lower(), currentSong.lower())
            # print(f'FUZZY RATIO IS: {fuzz.ratio(deckInUse[0].lower(), currentSong.lower())} FOR SONG: {currentSong}')

            # If the song titles match exactly or have a small levenshtein distance ratio between eachother, we found a match.
            # Note: Levenshtein distance is used for fuzzy string comparison due to expected OCR inconsistencies
            if(deckInUse[0] == currentSong or fuzzyStringComparisonRatio > 80):
                selectedVideoPath = os.path.join(os.getcwd(),'videos',filteredVideoList[i]) + '.mp4'
            else:
                pass;
        
        if(selectedVideoPath == ''):
            print("ERROR: NO VISUALIZATION VIDEO DETECTED TO ACCOMPANY TRACK. DOING NOTHING INSTEAD...")
            return;

        print(f'Deck video path is: {selectedVideoPath}') if debug is True else None
        
           
        #print(f'Starting song at time {deckInUse[1]} with speed {deckInUse[2]}')
        #3 use vlc cli to play song

        #Switching between main process and buffer process to ensure there is always overlap while one is booting up
        if(mainProcess is None):
            print("in main proc")
            # mainProcess.kill() if hasattr(mainProcess, 'kill') else print("Not killing anything..")
            print("Starting screen...")
            kill_pid(mainProcess)
            mainProcess = subprocess.Popen(['mpv',selectedVideoPath, f'--start={deckInUse[1]}' , f'--speed={deckInUse[2]}', '--screen=1', '--no-audio' ])
          
            time.sleep(2)
            print("Killing screen...")
            print(kill_pid(bufferProcess))
            time.sleep(1)
            bufferProcess = None
            # os.kill(bufferProcess.pid, signal.SIGTERM) if hasattr(bufferProcess, 'pid') else print("Not killing anything..")
        else:   
            print("in buffer proc")
            # bufferProcess.kill() if hasattr(bufferProcess, 'kill') else print("Not killing anything..") 
            print("Starting screen...")
            kill_pid(bufferProcess)
            bufferProcess = subprocess.Popen(['mpv',selectedVideoPath, f'--start={deckInUse[1]}', f'--speed={deckInUse[2]}', '--screen=1', '--no-audio' ])
            
            time.sleep(2)
            print("Killing screen...")
            print(kill_pid(mainProcess))
            time.sleep(1)
            mainProcess = None
            #os.kill(mainProcess.pid, signal.SIGTERM) if hasattr(mainProcess, 'pid') else print("Not killing anything..")
        

    except Exception as e:
        print(f"There was an error: {e}")
        traceback.print_exc()


#### Helpers 


# Given a relative percent speed as a string return the absolute speed as a double
def relativeStringPercentToDecimal(percentSpeed, originalBPM):

    sign = percentSpeed[0]

    isBeatSynced = False if percentSpeed[len(percentSpeed)-1] == '%' else True

    if not isBeatSynced:

        isNegative = True if sign == '-' else False

        # remove the percent and sign if it exists
        justTheNumber = percentSpeed[1:len(percentSpeed)-1] if isNegative else percentSpeed[0:len(percentSpeed)-1]

        #convert percent to decimal number
        relativePercentage = float(justTheNumber) / 100.0

        # Return the relative percent speed from 1.0
        if isNegative:
            return "{:.2f}".format(1 - relativePercentage)
        else:
            return "{:.2f}".format(1 + relativePercentage)
    else:

        return "{:.2f}".format(float(percentSpeed) / float(originalBPM))


# Given a string with an elapsed time in MM:SS format, convert to an integer
def elapsedStringTimeToIntegerEpoch(elapsedTime):
    print(elapsedTime)
    ones = float(elapsedTime[0:2])
    seconds = float(elapsedTime[3:7])

    return ones * 60 + seconds

def current_milli_time():
    return round(time.time() * 1000)


########## Listener hooks

def on_press(key):
        global currentDeckNumber
        if hasattr(key,'char') and key.char == 'q':
            print("Q key entered. Exiting...") 
            return False
        elif hasattr(key,'char') and key.char == 'a':
            print('Pressed a') 
            currentDeckNumber = 1
        elif hasattr(key,'char') and key.char == 'd':
            print('Pressed d') 
            currentDeckNumber = 2
        else:
            pass;
        print(f'Now we are using deck {currentDeckNumber}')

def on_release(key):
    if hasattr(key,'char') and key.char == 'e':
        # Stop listener
        return False

def checkListener():
    if not listener.running:
        exit(0)


##### Logic


# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while True:
    try:
        time.sleep(2)
        main()
        checkListener()
    except Exception as e:
        print('Exiting Gracefully...')
        temp = mainProcess.kill() if hasattr(mainProcess,'kill') else None
        temp = bufferProcess.kill() if hasattr(bufferProcess,'kill') else None
        exit(0)



