import os
from PIL import Image
def checkFiles():
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
    # iterate through every image in the "Correct Agents" directory

    for file in os.listdir("."):
        f = os.path.join(".", file)
        if not ".png" in f:
            continue
        image = Image.open(f)
        image = image.convert('RGB')
        try:
            agent = valorantAgents.pop(image.getpixel((20,20)))
            print("[+] "+ agent)
        except KeyError:
            print("Failed to find agent for: "+ f)

    print("Missing the following agents: ")
    for i in valorantAgents.values():
        print(i)

checkFiles()