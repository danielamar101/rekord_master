
import time

def main():

    print("Let's determine if the calibration settings are correct:")
    print("Open Rekordbox and load the song: deadmau5 & Lights - When The Summer Dies on Deck #1")
    print("Open Rekordbox and load the song: Transtechnics - Hard Groovey Meditation on Deck #2")

    time.sleep(10)

    # expectedTest1 = 
    actualTest1 = getLeftDeck()


if __name__ == '__main__':
    from rekord2song.src.ocr.get_both_deck_info import getLeftDeck, getRightDeck
    main()
else:
    from rekord2song.src.ocr.get_both_deck_info import getLeftDeck, getRightDeck
