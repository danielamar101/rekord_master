import subprocess
import time

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

def start_video_process(video_path, start_time, speed):
    """Starts a video process with the given parameters."""
    return subprocess.Popen(['mpv', video_path, f'--start={start_time}', f'--speed={speed}', '--screen=1', '--geometry=720x408+0+1292', '--no-audio'])

def kill_video_process(process):
    """Kills a video process if it exists."""
    if process:
        process.terminate()  # Or use your custom kill_pid function
        process.wait()  # Wait for the process to terminate

def manage_video_processes(main_process, buffer_process, selected_video_path, deck_info):
    """Manages switching between main and buffer video processes."""
    new_process = start_video_process(selected_video_path, deck_info['elapsed_time'], deck_info['percent_speed'])
    time.sleep(2)  # Ensure the new process plays for a few seconds

    if main_process is None:
        print("Killing buffer process and setting new process as main.")
        kill_video_process(buffer_process)
        main_process = new_process
        buffer_process = None
    else:
        print("Killing main process and setting new process as buffer.")
        kill_video_process(main_process)
        buffer_process = new_process
        main_process = None

    return main_process, buffer_process
