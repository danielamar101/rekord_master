# rekord master


The idea behind rekordmaster is to play and syncronize music videos automatically while a DJ is playing songs in Rekordbox. So on one screen you're havin a good ol mixin sesh with da boys, and on another you have visualizers to your music, with the video speed matching your bpm.

The aim one day is to enable video playback from a variety of different sources. For now the videos must already be downloaded and in a directory. 

And maybe we can get a video generated from an LLM implemented to be played back automatically! Thats the end goal. 

# Installation

Use conda to create a virtual environment with python 3.11:
`conda env create -f environment.yaml`
Then install required dependencies
`pip install -r requirements.txt`


# Screen Coordinate Calibrator

Since rekordbox does not have an api, we rely on OCR and CV to grab the necessary information off the decks to enable us to start playback. As such, you must calibrate the coordinates on your rekordbox using the script in: `src/ocr/calibrate_full.py`

The script will start asking you to drag select the coordinates in order. Here is a reference chart:

<add it here lol>

Add videos to the directory `src/videos`. Ensure the video names match your song names in rekordbox. After that you should be good to go.

Start `src/main.py` and start mixing!

How it works currently:

`rekord_master` employs the use of a fuzzy string compare on the OCR text that is received, in the event OCR makes a few mistakes with song names.

Feel free to open PR's and help. This is in rough alpha at the moment, and will need many many features and improvements.

