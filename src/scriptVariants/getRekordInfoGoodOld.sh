#!/bin/bash

#Ease value, lower value means more bot-like movement
EV=700
waitValue=1


if [ $DECK  == "1" ]; then

    # Get first deck song
    ocr & cliclick -e $EV dd:55,310 du:671,330 w:100

    # Get percentage
    ocr & cliclick -e $EV dd:692,472 du:727,490 w:50
    
    # Get first deck time position
    ocr & cliclick -e $EV dd:627,333 du:691,351 

    
else
    #Get second deck song
    ocr & cliclick -e $EV dd:977,310 du:1605,330 w:50

    #Get percentage speed
    ocr & cliclick -e $EV dd:987,472 du:1014,490 w:50

    # Get second deck time position
    ocr & cliclick -e $EV dd:1548,332 du:1609,349 

    
fi


exit 0

