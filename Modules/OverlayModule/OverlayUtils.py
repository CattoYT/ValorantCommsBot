# Each agent has a 40x40 area at the top of the screen.
# Player 1 on your team is at x=710 and y=30
# Player 2 is x=644
# P3 is x=578
# The offset for the left team from P1 is -66px
# Once the agent has been found, I can map that agent to the label and position.
# However, when a player dies, their model is shoved closer to the middle
# When this happens, i can run a scan again and move the labels accordingly
# I also don't need to research for each agent, i can just check for the ones found in the first place
# store them in a list or something ideally, maybe even a dict

# This is going to be offset from the first player on the right because it would just be easier lol
#
from detectors import capture_screenshot
import numpy as np





def getAgent(position, screenshot=None): # position is 1 indexed.
    valorantAgents = {
        # I did this manually. Im going to die :|
        (79, 61, 59): "Astra",
        (189, 154, 132): "Breach",
        (218, 169, 132): "Brimstone",
        (214, 195, 181): "Chamber",
        (190, 144, 135): "Clove",
        (20, 23, 33): "Cypher",
        (198, 146, 123): "Deadlock",
        (190, 145, 127): "Fade",
        (189, 134, 107): "Gekko",
        (119, 79, 68): "Harbor",
        (171, 131, 105): "Iso",
        (194, 138, 120): "Jett",
        (110, 126, 131): "KAY/O",
        (233, 213, 233): "Killjoy",
        (17, 18, 21): "Neon",
        (24, 255, 255): "Omen",
        (107, 73, 66): "Phoenix",
        (156, 112, 96): "Raze",
        (129, 85, 79): "Reyna",
        (66, 58, 58): "Sage",
        (183, 179, 157): "Skye",
        (201, 168, 160): "Sova",
        (101, 101, 95): "Viper",
        (8, 12, 24): "Yoru"
    }
    offsetX = 380 + (int (position)*66)
    if position > 5:
        offsetX += 394
    if not screenshot:
        screenshot = capture_screenshot()
    region_y = 30
    region_width = 40
    region_height = 40

    #screenshot = screenshot.crop((offsetX, region_y, offsetX + region_width, region_y + region_height))
    # center pixel of the cropped image
    screenshot = screenshot.convert('RGB')
    centerPixelX, centerPixelY = int(region_width / 2), int(region_height / 2)
    print((offsetX+centerPixelX, region_y+centerPixelY))
    try:
        print(valorantAgents[screenshot.getpixel((offsetX+centerPixelX, region_y+centerPixelY))])
    except KeyError:
        print("No agent")

def getAllAgents(screenshot=None):
    for i in range(1, 11):
        getAgent(i, screenshot=screenshot)

if __name__ == "__main__":
    while True:
        getAllAgents()
        input()