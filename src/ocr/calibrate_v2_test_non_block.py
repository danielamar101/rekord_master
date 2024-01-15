import subprocess
import threading
import queue
import json
import sys

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        print(f"DEBUG: Read line: {line}")  # Debugging line
        queue.put(line)
    out.close()

sys.stdout = open(sys.stdout.fileno(), mode='w', buffering=1)
# Replace 'your_command' with the command you want to execute
command = ["your_command"]

# Start the subprocess
process = subprocess.Popen(['../../swift-calibrator/swift-calibrator'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,  bufsize=1)

# Create a queue to hold the output
q = queue.Queue()

# Start a thread to asynchronously read the subprocess's output
t = threading.Thread(target=enqueue_output, args=(process.stdout, q))
t.daemon = True
t.start()

# Main loop
try:
    while True:
        # Check if there is output from the subprocess
        try:
            line =q.get(timeout=.1)
        except queue.Empty:
            # print("Nothing in stdout")
            # No output yet
            pass
        else:
            # Process the output line (assuming it's JSON)
            try:
                json_data = json.loads(line)
                # Do something with the JSON data
                print(json_data)
            except json.JSONDecodeError:
                print("Error decoding JSON from the output:", line)

        # Check if the subprocess has finished
        if process.poll() is not None:
            break

        # You can do other things here or just sleep
        # time.sleep(1)

finally:
    process.stdout.close()
    process.terminate()

