from pynput import keyboard
from .globals import current_deck_number
########## Listener hooks

def on_press(key):
        global current_deck_number
        if hasattr(key,'char') and key.char == 'q':
            print("Q key entered. Exiting...") 
            return False
        elif hasattr(key,'char') and key.char == 'a':
            print('Pressed a') 
            current_deck_number = 1
        elif hasattr(key,'char') and key.char == 'd':
            print('Pressed d') 
            current_deck_number = 2
        else:
            pass;
        print(f'Now we are using deck {current_deck_number}')

def on_release(key):
    if hasattr(key,'char') and key.char == 'e':
        # Stop listener
        return False

def checkListener():
    if not listener.running:
        exit(0)

# non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
