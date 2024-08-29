import os
import time
from multiprocessing import Process, Event, Value

import detectors
import cv2
import numpy as np
from mss.windows import MSS as mss
from PIL import Image
import speaker as spk
from Modules.BaseLiveManager import BaseLiveManager


# The current dilemma with this module is that Valorant already has something like it whith the agent callouts
# This isn't really needed tbh
# However, it is cool so I'll leave this module as deprecated.



class EnemyManager(BaseLiveManager):
    def __init__(self, visualize=True):
        """
        This class is the main module for detecting the enemies. Ideally a YOLOv8 model should be used for this, but its still cooking
        and im not going to finish cooking it.
        Please run this using the
        :param visualize: Boolean
        """
        super().__init__()
        self.visualize = visualize
        self.stopEvent = Event()
        self.liveProcess = self.yoloV8Detection # self.findEnemy can be used for yolov5, legacy tho
        self.model = None # set to none just in case, generally will be initialized by the yolo function
        self.enemyCount = Value('i', 0)




    def findEnemy(self):
        """
        This function is the main function for detecting enemies. It uses a YOLOv5 model to detect enemies.
        Currently deprecated in favour of yoloV8Detection

        :return:
        """

        if self.model == None:
            import torch
            print("Loading model")

# for this, I am planning to move back to a custom trained yolov8 model using the above dataset, since ripping the model didn't really work
# will also have to learn how yolov8 works, or if i can hotswap it into the below code

            # Change me to the right model!
            modelname = "valorant-11.engine"
            self.model = torch.hub.load(R'yolov5', 'custom', modelname, source='local', force_reload=True)

        previousCount = 0
        self.model.conf = 0.69
        # Calculate the top right corner coordinates for the 300x300 pixels box

        while not self.stopEvent.is_set():

            sct_img = detectors.capture_screenshot()

            # box code genned from copilot
            # Define the box coordinates (x_min, y_min, x_max, y_max)





            results = self.model(self.overlayCensor(sct_img))

            self.enemyCount = 0

            # thanks copilot for this lol
            if self.visualize:
                cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)

                img = None # hey, i dont use this but i might later
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

                for det in results.pred[0]:
                    label = det[5]  # Class label
                    conf = det[4]  # Confidence score
                    bbox = det[:4]  # Bounding box coordinates

                    if conf > self.model.conf:
                        x_min, y_min, x_max, y_max = map(int, bbox)
                        cv2.rectangle(img_cv, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                        label_text = f"{self.model.names[int(label)]} {conf:.2f}"
                        cv2.putText(img_cv, label_text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (0, 255, 0), 2)
                        self.enemyCount += 1

                cv2.imshow("Detection", img_cv)
                cv2.waitKey(10)
            else:
                for det in results.pred[0]:
                    if det[4] > self.model.conf:
                        self.enemyCount += 1

            if self.enemyCount > 0:
                print(f"[OVERRIDE] Enemies: {self.enemyCount}")


            if self.enemyCount > 0 and previousCount != self.enemyCount:
                print("Speaking")

            previousCount = self.enemyCount

    def overlayCensor(self, img):
        img_np = np.array(img)
        height, width, _ = img_np.shape
        box_coords = (width - 70, 93, width - 30, 400)  # (x_min, y_min, x_max, y_max)

        # Set the specified area to black
        img_np[box_coords[1]:box_coords[3], box_coords[0]:box_coords[2]] = [0, 0, 0]
        return img



    def yoloV8Detection(self):
        """
        Main detection loop for YOLOv8. Detects enemies, and plays the voice line if an enemy is detected.
        :return:
        """
        # This needs to run as fast as possible cuz valorant is fast asf
        import logging

        # Suppress logging output

        if self.model == None:
            import ultralytics
            modelPath = "Models/keremberke.pt"
            self.model = ultralytics.YOLO(modelPath)
            # converts the model to engine if it isnt already
            print(modelPath[:-3] + ".engine")
            if modelPath[-2:] == "pt":

                try:
                    self.model = ultralytics.YOLO(modelPath[:-3] + ".engine")
                except:
                    if input("Do you want to convert this model to "
                             "TensorRT for faster inference? DO NOT DO THIS IN A GAME! IT TAKES A LONG TIME! (y/n): ").lower() == "y":

                        self.model.export(dynamic=True, format="engine")
                        os.remove(modelPath[:-3] + ".onnx")
                        self.model = ultralytics.YOLO(modelPath[:-3] + ".engine")
        cooldown = 0
        logging.getLogger('ultralytics').setLevel(logging.WARNING) #chatgpt'd because the documentation is kinda shit
        while not self.stopEvent.is_set():
            screenshot = detectors.capture_screenshot()
            overlayedSS = self.overlayCensor(screenshot)
            results = self.model(overlayedSS, conf=0.70, device="0")

            detections = results[0].boxes
            class_ids = detections.cls.cpu().numpy() if detections.cls is not None else [] # thanks copilot
            detected = 0

            for i, class_id in enumerate(class_ids):
                if class_id == 1.0: # check if the class id is actually an enemy

                    detected += 1
                if self.visualize:
                    x_min, y_min, x_max, y_max = detections.xyxy[i].cpu().numpy()
                    # Draw bounding box on the image
                    overlayedSS = cv2.cvtColor(overlayedSS, cv2.COLOR_RGB2BGR)
                    cv2.rectangle(overlayedSS, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
                    cv2.putText(overlayedSS, f'Class: {int(class_id)}', (int(x_min), int(y_min) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            if detected >= 1:
                if time.time() - cooldown > 30:  # 30 seconds
                    cooldown = time.time()
                    spk.sayVoice(r"D:\Coding\python\ValorantCommsBot\voices\mio\new-round\respawn - more_enemies_what_do_we_do.wav")



if __name__ == "__main__":
    em = EnemyManager(visualize=True)
    em.yoloV8Detection()