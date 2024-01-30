import os
import time
from fuzzywuzzy import fuzz
import traceback

#import signal
# import pytesseract
#from PIL import Image

from helpers.data_conversions import elapsedStringTimeToSeconds, relativeStringPercentToDecimal
from app.process_handlers import manage_video_processes
from app.listeners import checkListener
from ocr.get_both_deck_info import getLeftDeck, getRightDeck
from app.globals import current_deck_number, main_process, buffer_process, debug


def main(): 
    global current_deck_number
    global main_process
    global buffer_process
    global debug

    try:
        checkListener()

        #1. Grab Song info, speed of song, and elapsed time
        deck_list = getLeftDeck() if current_deck_number == 1 else getRightDeck()

        print(deck_list)
        checkListener()

        # Song Name, Elapsed Time, percent speed, starting bpm
        deck_info = {'song_name': deck_list[0], 
                     'elapsed_time': elapsedStringTimeToSeconds(deck_list[2]), 
                     'percent_speed': relativeStringPercentToDecimal(deck_list[1],deck_list[3]), 
                     'starting_bpm': deck_list[3]} 
      
        print("")
        print(f'SELECTED DECK #{current_deck_number}. CONTAINS: {deck_info}')
        print("")

        #2 Find song in file directory  
        videoList = os.listdir(os.path.join(os.getcwd(),"videos"))
            # Obtain song name in the videos directory if its an mp4
        filtered_video_list = [video[0:len(video)-4] for video in videoList if video[(len(video)-3):] == 'mp4']
        #print(f'List of videos in videos dir: {filtered_video_list}') 

        # Goal of the following for loop is to find the song file path
        selected_video_path = ''

        for i in range(len(filtered_video_list)):
            song_title_length = len(deck_info['song_name'])
            current_song = filtered_video_list[i][0:song_title_length]
            fuzzy_ratio = fuzz.ratio(deck_info['song_name'].lower(), current_song.lower())
            # print(f'FUZZY RATIO IS: {fuzz.ratio(deck_info['song_name'].lower(), current_song.lower())} FOR SONG: {current_song}')

            # If the song titles match exactly or have a small levenshtein distance ratio between eachother, we found a match.
            # Note: Levenshtein distance is used for fuzzy string comparison due to OCR inconsistencies
            if(deck_info['song_name'] == current_song or fuzzy_ratio > 80):
                selected_video_path = os.path.join(os.getcwd(),'videos',filtered_video_list[i]) + '.mp4'
            else:
                pass;
        
        if(selected_video_path == ''):
            print("NO VISUALIZATION VIDEO DETECTED TO ACCOMPANY TRACK ( or couldnt find it lol). DOING NOTHING INSTEAD...")
            return;

        print(f'Deck video path is: {selected_video_path}') if debug is True else None 
        #print(f'Starting song at time {deck_info['elapsed_time']} with speed {deck_info['percent_speed']}')


        #3 Use VLC CLI to play song

        #Switching between main process and buffer process to ensure there is always overlap while one is booting up
        main_process, buffer_process = manage_video_processes(main_process, buffer_process,selected_video_path, deck_info)

    except Exception as e:
        print(f"There was an error: {e}")
        traceback.print_exc()


while True:
    try:
        time.sleep(2)
        main()
        checkListener()
    except Exception as e:
        print('Exiting Gracefully...')
        temp = main_process.kill() if hasattr(main_process,'kill') else None
        temp = buffer_process.kill() if hasattr(buffer_process,'kill') else None
        exit(0)



