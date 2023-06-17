# from pynput.keyboard import Key, Controller
# from pynput.mouse import 
import time

# keyboard = Controller()


# time.sleep(3)

# with keyboard.pressed(Key.shift):
#     keyboard.press(Key.cmd)
#     keyboard.press(Key.shift)

#     keyboard.press('c')
#     keyboard.release('c')
#     keyboard.release(Key.cmd)
#     keyboard.release(Key.shift)


# time.sleep(3)

# with keyboard.pressed(Key.cmd):
#     keyboard.press('v')
#     keyboard.release('v')
#     keyboard.release(Key.cmd)


from pynput import keyboard

def on_press(key):
        
        if key == keyboard.Key.esc:
            print("Escape key entered")
        elif hasattr(key,'char') and key.char == '1':
            print(' Pressed 1')
        elif hasattr(key,'char') and key.char == '2':
            print('Pressed 2')
        else:
            pass;

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while True:
    
    if not listener.running:
        exit(0)
    else:
        print('we are still running')
