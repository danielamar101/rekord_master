import time

# Given a relative percent speed as a string return the absolute speed as a double
def relativeStringPercentToDecimal(percentSpeed, originalBPM):

    try: 
        sign = percentSpeed[0]
        isBeatSynced = False if percentSpeed[len(percentSpeed)-1] == '%' else True

        if not isBeatSynced:

            isNegative = True if sign == '-' else False

            # remove the percent and sign if it exists
            justTheNumber = percentSpeed[1:len(percentSpeed)-1] if isNegative else percentSpeed[0:len(percentSpeed)-1]

            #convert percent to decimal number
            relativePercentage = float(justTheNumber) / 100.0

            # Return the relative percent speed from 1.0
            if isNegative:
                return "{:.2f}".format(1 - relativePercentage)
            else:
                return "{:.2f}".format(1 + relativePercentage)
        else:

            return "{:.2f}".format(float(percentSpeed) / float(originalBPM))
    except Exception as e:
        print("Error getting the relative percent speed.")


def elapsedStringTimeToSeconds(time_str):
    # Split the time string into minutes, seconds, and (optionally) milliseconds
    
    try:

        parts = time_str.split(":")
    
        # Convert minutes and seconds to integers
        minutes = int(parts[0])
        seconds = int(parts[1][0:2])

        
        # Calculate total seconds
        total_seconds = (minutes * 60) + seconds
        
        return total_seconds
    except Exception as e:
        print(e)
        # raise ValueError("Time string must be at least in MM:SS format")
        print("Error getting the time. sending 00:00 for now..")
        return "00:00"

    


def current_milli_time():
    return round(time.time() * 1000)
