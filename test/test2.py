

import subprocess
import time


# while True:
#     current = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC', '/Users/danielamar/Desktop/Code/music_master/rekord2song/videos/What I Might Do.mp4','--fullscreen', f'--start-time=20.5', f'--rate=1' ],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#     current = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC', '/Users/danielamar/Desktop/Code/music_master/rekord2song/videos/What I Might Do.mp4','--fullscreen', f'--start-time=20.5', f'--rate=1' ],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#     time.sleep(5)

#     current.kill()

startTime = time.time
current = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC', '/Users/danielamar/Desktop/Code/music_master/rekord2song/videos/What I Might Do.mp4', f'--start-time=20.5', f'--rate=1', '--audio-visual=ugly' ])
                           #,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
endTime = time.time 

print(endTime-startTime)


#current = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC', '/Users/danielamar/Desktop/Code/music_master/rekord2song/videos/What I Might Do.mp4','--fullscreen', f'--start-time=20.5', f'--rate=1' ],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#current.kill()