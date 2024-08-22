# Voices

ValorantCommsBot uses a structured directory to get and play voice lines.
Luckily, this means that adding voice lines is pretty easy!


The structure is as follows:
```
voices/{character}/{event}/{voice_line}.wav
```
I haven't tested other audio formats, but they should work(?)

To add your own voice lines, copy the voices/mio folder and rename it. Then just populate with your own voice lines!  
I use the mio voice lines in development, so follow the same structure as the mio folder.   
KEEP THE EVENT NAMES THE SAME!!!! It won't work otherwise!

To actually replace the voicelines, go to speaker.py and replace "va" in getRandomFile() to the name of the character's folder


The following events are currently supported and can be triggered:
- death (player dies)
- encouragement (teammate gets a kill)
- low-hp
- victory (round win)
- loss (round loss)
- new-round (these are lines that can be for a win or a loss)


The other events are not used in the bot, but probably will be in the future.
- health-recovered (sage/skye heal)
- teammate-death (The code for this is already in detectors.py, however I don't need it yet)

