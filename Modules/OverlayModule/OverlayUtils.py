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
import detectors
import numpy as np





def getAgent(position, screenshot=None): # position is 1 indexed.
    valorantAgents = {
        # I did this manually. Im going to die :|
        "Astra": (79, 61, 59),
        "Breach": (189, 154, 132),
        "Brimstone": (218, 169, 132),
        "Chamber": (214, 195, 181),
        "Clove": (190, 144, 135),
        "Cypher": (20, 23, 33),
        "Deadlock": (198, 146, 123),
        "Fade": (190, 145, 127),
        "Gekko": (189, 134, 107),
        "Harbor": (119, 79, 68),
        "Iso": (171, 131, 105),
        "Jett": (194, 138, 120),
        "KAY/O": (110, 126, 131),
        "Killjoy": (233, 213, 233),
        "Neon": (17, 18, 21),
        "Omen": (24, 255, 255),
        "Phoenix": (107, 73, 66),
        "Raze": (156, 112, 96),
        "Reyna": (129, 85, 79),
        #   TODO: Add the rest of the agents
        "Sage": (),
        "Skye": (),
        "Sova": (),
        "Viper": (),
        "Yoru": ()

    }
    offsetX = 380 + (int (position)*66)
    if not screenshot:
        screenshot = detectors.capture_screenshot()
    region_y = 30
    region_width = 40
    region_height = 40

    #screenshot = screenshot.crop((offsetX, region_y, offsetX + region_width, region_y + region_height))
    # center pixel of the cropped image
    screenshot = screenshot.convert('RGB')
    centerPixelX, centerPixelY = int(region_width / 2), int(region_height / 2)
    print(centerPixelX, centerPixelY)
    print(offsetX+centerPixelX, region_y+centerPixelY)
    print(screenshot.getpixel((offsetX+centerPixelX, region_y+centerPixelY)))


if __name__ == "__main__":
    while True:
        getAgent(5)
        input()