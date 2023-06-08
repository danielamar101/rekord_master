import subprocess
import os
import time;
from pynput import keyboard


currentDeckNumber = 1
mainProcess = None
bufferProcess = None

debug = True

def main(): 
    global currentDeckNumber
    global mainProcess
    global bufferProcess
    global debug
    try:

        subprocess_env = os.environ.copy()
        subprocess_env["DECK"] = f'{currentDeckNumber}'

        checkListener()

        #1. Grab Song info, speed of song, and elapsed time
        result = subprocess.run('./getRekordInfo.sh', capture_output=True, text=True, env=subprocess_env)

        startTime = current_milli_time()

        checkListener()

        songList = result.stdout.split('\n')

        # Song Name, Elapsed time, Percent speed
        deckInUse = [songList[0], elapsedStringTimeToIntegerEpoch(songList[2]), relativeStringPercentToDecimal(songList[1])] 
      
        print("")
        print(f'SELECTED DECK #{currentDeckNumber}. CONTAINS: {deckInUse}')
        print("")

        #2 Find song in file directory  
        videoList = os.listdir("./videos")
        filteredVideoList = [video[0:len(video)-4] for video in videoList if video[(len(video)-3):] == 'mp4']
        print(f'List of videos in videos dir: {filteredVideoList}') 

        # Goal of the following for loop is to find a song path
        selectedVideoPath = ''

        for i in range(len(filteredVideoList)):
            lengthOfSongTitle = len(deckInUse[0])
            if(len(filteredVideoList[i]) < lengthOfSongTitle):
                pass;
            elif(deckInUse[0] == filteredVideoList[i][0:lengthOfSongTitle]):
                selectedVideoPath = os.path.join(os.getcwd(),'videos',filteredVideoList[i]) + '.mp4'
            else:
                pass;
        
        if(selectedVideoPath == ''):
            print("ERROR: NO VISUALIZATION VIDEO DETECTED TO ACCOMPANY TRACK. DOING NOTHING INSTEAD...")

            return;

        print(f'Deck video path is: {selectedVideoPath}') if debug is True else None
        
           
        print(f'Starting song at time {deckInUse[1]} with speed {deckInUse[2]}')
        #3 use vlc cli to play song

        #Switching between main process and buffer process to ensure there is always overlap while one is booting up
        if(mainProcess is None):
            mainProcess.kill() if hasattr(mainProcess, 'kill') else None
            mainProcess = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC',selectedVideoPath, f'--start-time={deckInUse[1] + 2 * float(deckInUse[2])}', f'--rate={deckInUse[2]}' ],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            #mainProcess = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC',selectedVideoPath, '--fullscreen', f'--start-time={deckInUse[1]}', f'--rate={deckInUse[2]}' ],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            endTime = current_milli_time()
            print(f"Took {endTime-startTime} to complete operation.")
            time.sleep(1)
            bufferProcess.kill() if hasattr(bufferProcess, 'kill') else None
        else:   
            bufferProcess.kill() if hasattr(bufferProcess, 'kill') else None 
            bufferProcess = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC',selectedVideoPath, f'--start-time={deckInUse[1] + 2 * float(deckInUse[2])}', f'--rate={deckInUse[2]}' ],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            endTime = current_milli_time()
            print(f"Took {endTime-startTime} to complete operation.")
            time.sleep(1)
            mainProcess.kill() if hasattr(mainProcess, 'kill') else None
        

    except Exception as e:
        print(f"There was an error: ${e}")
        raise e


#### Helpers 


# Given a relative percent speed as a string return the absolute speed as a double
def relativeStringPercentToDecimal(percentSpeed):

    sign = percentSpeed[0]
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
            print('Pressed a') if debug is True else None
            currentDeckNumber = 1
        elif hasattr(key,'char') and key.char == 's':
            print('Pressed s') if debug is True else None
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
        main()
        checkListener()
        time.sleep(5)
    except Exception as e:
        print('Exiting Gracefully...')
        temp = mainProcess.kill() if hasattr(mainProcess,'kill') else None
        temp = bufferProcess.kill() if hasattr(bufferProcess,'kill') else None
        raise e 
        exit(0)








# /Applications/VLC.app/Contents/MacOS/VLC
# --qt-fullscreen-screennumber=<integer> 
#                                  Define which screen fullscreen goes
#           Screennumber of fullscreen, instead of same screen where interface
#           is.
# main()




# The event listener will be running in this block
