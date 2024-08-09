import pytesseract
import time
import detectors


def readChat():
    # This one runs on a 5 second delay, might be able to run it with KillsManager
    screenshot = detectors.capture_screenshot()
    region_x = 10  # X-coordinate of the top-left corner of the region
    region_y = 804  # Y-coordinate of the top-left corner of the region
    region_width = 436  # Width of the region
    region_height = 242  # Height of the region

    screenshot = screenshot.crop((region_x, region_y, region_x + region_width, region_y + region_height))

    text = pytesseract.image_to_string(screenshot, config=r'--psm 6 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789():<>?!& "')

    data = []

    for line in text.splitlines():
        no = False
        if "(Party)" in line:
            line = line.replace("(Party) ", "")
            channel = "Party"
        elif "(All)" in line:
            line = line.replace("(All) ", "")
            channel = "All"
        elif "(Team)" in line:
            line = line.replace("(Team) ", "")
            channel = "Team"
        else:
            no = True

        user = ""
        for char in line:
            if char == ":":
                line = line.replace(user, "")
                break
            else:
                user = user + char
        if not no:

            data.append((channel, user, line))



    return data


# since this file returns a pretty nice data struct, and it seems computationally heavy, it might be agood idea to rewrite this one in a differnet language
# I know that exposing rust to python is decently easy, so il research that
if __name__ == "__main__":
    while True:
        data = readChat()
        for i in data:

            print(f"({i[0]}) {i[1]}{i[2]}")
        time.sleep(4.5)