# # import time
# #
# # import cv2
# # import numpy as np
# # from PIL import Image
# # import speaker as spk
# # import detectors
# #
# # from ultralytics import YOLO
# # # - = enemy
# # # roboflow is an end to end = teammate
# # # exportd via roboflow = planted spike
# # # valorant = unplanted spike
# #
# # model = YOLO("Models/best.pt")
# # cooldown = 0
# # while True:
# #     results = model(detectors.capture_screenshot(), conf=0.60)
# #
# #     detections = results[0].boxes
# #     class_ids = detections.cls.cpu().numpy() if detections.cls is not None else []  # thanks copilot
# #     detected = 0
# #     for class_id in class_ids:
# #         if class_id == 1.0:
# #             detected += 1
# #
# #
# #
# #     if detected >= 1:
# #         print("Heeh")
# #         if time.time() - cooldown > 30: # 30 seconds
# #             cooldown = time.time()
# #             spk.sayVoice(r"D:\Coding\python\ValorantCommsBot\voices\mio\new-round\respawn - more_enemies_what_do_we_do.wav")
#
# import requests
#
# from PIL import Image
# import numpy as np
# import io
# from mss.windows import MSS as mss
#
#
# sct = mss()
# def capture_screenshot():
#     region = sct.grab(sct.monitors[2])
#     region = Image.frombytes('RGB', region.size, region.bgra, 'raw', 'BGRX')
#     #region = pyautogui.screenshot(region=(0, 0, 1920, 1080))
#     # screenshot = Image.open('testimage.png')
#
#     return region
#
# def hello():
#     while True:
#
#         imagedata = capture_screenshot()
#
#         # Convert the image to a byte array
#         buffered = io.BytesIO()
#         imagedata.save(buffered, format="JPEG")
#

#         img_bytes = buffered.getvalue()
#
#         # Send the byte array in a POST request
#         response = requests.post("https://cheaply-caring-pup.ngrok-free.app/inference", data=img_bytes)
#
#         print(response.text)
# hello()
#
#
#
# import keyboard
# import time
# pressedKeys = []
# while True:
#
#
#     for key in keyboard._:
#         pressedKeys.append(key)
#         print(key)
#         keyboard.keyUp(key)
#     keyboard.press('enter')
#     keyboard.release('enter')
#     time.sleep(1)
#
#
#     keyboard.press('enter')
#     keyboard.release('enter')
#
#
#
#     print(pressedKeys)
#     for key in pressedKeys:
#
#         keyboard.keyDown(key)
#     time.sleep(5)
#

import RustModules

print(RustModules.readChatTest)