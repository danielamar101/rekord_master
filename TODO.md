
MUST:

- Fix process not being killed (DONE)
- Only take screenshot from selected deck, switch which side gets shots on (DONE)
- kill entire process immediately after escape (DONE)

- account for screenshotting + processing delay when figuring out time to open it at
    - Look into VLC CLI docs theres some stuff in there about timestamps that might help us (FALSE)
    - Using a constant of 2 secs * speed

- account for open and closing of videos breaking up the experience between each event (DONE?)
    - We'll have to use tricks here to trick the viewers


- Ensure vid is always played on same screen 
    S: Check for display resolution changes

- Look into faster and more robust OCR method




STRETCH:

- Decrease screenshotting time