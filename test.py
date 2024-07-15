#
# import mouse
# import sounddevice as sd
# import soundfile as sf
# import time
# def find_device_id(device_name):
#     devices = sd.query_devices()
#     for device in devices:
#         if device['name'] == device_name:
#             print(device['index'])
#     return None
#
#
# def play_audio(file_path):
#
#
#     data, fs = sf.read(file_path, dtype='float32')
#
#     #mouse.press(button='x2')
#     sd.play(data, fs, device=find_device_id('CABLE Input (VB-Audio Virtual C'))
#     #d.play(data, fs, device=find_device_id('Microphone (Realtek(R) Audio)'))
#     #sd.play(data, fs)
#
#     sd.wait()
#     time.sleep(0.1)
#     #mouse.release(button='x2')
#
# from multiprocessing import Process
#
#
#
# # Kill management
#
# # this should be pushed into a different thread because it needs to run every 7 seconds. This is a fixed
# # timer cuz valorant despawns its kill messages after 7 secs
#
#
# class KillsManager:
#     def __init__(self):
#         self.stop = False
#         self.monitorProcess = None
#     def getStopper(self): # python seems to create a clone of self.stop in the while loop sooooo
#         return self.stop
#
#     def monitorKills(self):
#         while not self.getStopper():
#             print(self.getStopper())
#             time.sleep(1)
#     def beginMonitoring(self):
#         if self.monitorProcess is None or not self.monitorProcess.is_alive():
#             self.monitorProcess = Process(target=self.monitorKills)
#             self.monitorProcess.start()
#         return
#
#     def stopMonitoring(self):
#         self.stop = True
#         if self.monitorProcess is not None:
#             self.monitorProcess.join()
#
# if __name__ == '__main__':
#     KillsMgr = KillsManager()
#     KillsMgr.beginMonitoring()
#     print("returned")
#     time.sleep(10)
#     KillsMgr.stopMonitoring()
#     print("Monitoring stopped")
# import time
#
# import keras_ocr
#
# import detectors
#
#
# if __name__ == '__main__':
#     pipeline = keras_ocr.pipeline.Pipeline()
#     while True:
#         frame = detectors.capture_screenshot()
#         groups = pipeline.recognize(frame)
#         time.sleep(1)
# Future me note: don't try using keras ocr its fucked
#
import time

import detectors

if __name__ == '__main__':
    # import easyocr
    # import numpy
    # # Initialize the EasyOCR reader
    # reader = easyocr.Reader(['en'])  # You can specify the list of languages


    while True:
        print("new")
        frame = detectors.capture_screenshot()

        # region_x = 574  # X-coordinate of the top-left corner of the region
        # region_y = 1003  # Y-coordinate of the top-left corner of the region
        # region_width = 77  # Width of the region
        # region_height = 46  # Height of the region
        #
        # frame = frame.crop((region_x, region_y, region_x + region_width, region_y + region_height)).convert('L')
        #
        #
        # # Perform OCR
        # results = reader.readtext(numpy.array(frame))
        #
        # # Print the results
        # for (bbox, text, prob) in results:
        #     print(f'Text: {text}, Probability: {prob}, Bounding box: {bbox}')

        print(detectors.getPlayerHealth(frame))
        time.sleep(1)

# Easyocr is a lot worse performance wise - might stick with tesseract