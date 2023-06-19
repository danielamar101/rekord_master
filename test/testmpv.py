

import subprocess
import time
import os
import signal



current = subprocess.Popen(['mpv', '/Users/danielamar/Desktop/Code/music_master/rekord2song/src/videos/What I Might Do.mp4', '--no-audio', '--screen=0' ])

time.sleep(3)
                           #,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
current1 = subprocess.Popen(['mpv', '/Users/danielamar/Desktop/Code/music_master/rekord2song/src/videos/What I Might Do.mp4', '--no-audio','--screen=0' ])

time.sleep(3)

print("Killing..")
os.kill(current.pid, signal.SIGTERM)

time.sleep(3)

print("killing again")
os.kill(current1.pid, signal.SIGTERM)


#current = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC', '/Users/danielamar/Desktop/Code/music_master/rekord2song/videos/What I Might Do.mp4','--fullscreen', f'--start-time=20.5', f'--rate=1' ],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#current.kill()