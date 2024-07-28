import os
import time
from multiprocessing import Process, Event, Value

import detectors
import cv2
import numpy as np
from mss.windows import MSS as mss
from PIL import Image
import speaker as spk


# The current dilemma with this module is that Valorant already has something like it whith the agent callouts
# This isn't really needed tbh
# However, it is cool so I'll leave this module as deprecated.



class EnemyManager:
    def __init__(self, visualize=False):
        self.visualize = visualize
        self.stopEvent = Event()
        self.monitorProcess = None
        self.model = None
        self.enemyCount = Value('i', 0)




    def findEnemy(self):

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

            img_np = np.array(sct_img)
            height, width, _ = img_np.shape
            box_coords = (width - 70, 93, width - 30, 400)  # (x_min, y_min, x_max, y_max)

            # Set the specified area to black
            img_np[box_coords[1]:box_coords[3], box_coords[0]:box_coords[2]] = [0, 0, 0]
            img = Image.fromarray(img_np)



            results = self.model(img)

            self.enemyCount = 0

            # thanks copilot for this lol
            if self.visualize:
                cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
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

    def recordScreen(self): # will implement later

        with mss() as sct:
            # cap my first monitor
            monitor = sct.monitors[2]

            while True:
                cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)


                sct_img = sct.grab(monitor)
                img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')


    def yoloV8Detection(self):
        # This needs to run as fast as possible cuz valorant is fast asf

        if self.model == None:
            import ultralytics
            modelPath = "Models/epoch270.pt"
            self.model = ultralytics.YOLO(modelPath)
            # converts the model to engine if it isnt already
            print(modelPath[:-3] + ".engine")
            if modelPath[-2:] == "pt":

                try:
                    self.model = ultralytics.YOLO(modelPath[:-3] + ".engine")
                except:
                    if input("Do you want to convert this model to "
                             "TensorRT for faster inference? (y/n): ").lower() == "y":

                        self.model.export(dynamic=True, format="engine")
                        os.remove(modelPath[:-3] + ".onnx")
                        self.model = ultralytics.YOLO(modelPath[:-3] + ".engine")
        cooldown = 0
        while not self.stopEvent.is_set():
        #while True:
            screenshot = detectors.capture_screenshot()
            results = self.model(screenshot, conf=0.70, device="0")

            detections = results[0].boxes
            class_ids = detections.cls.cpu().numpy() if detections.cls is not None else [] # thanks copilot
            detected = 0
            for class_id in class_ids:
                if class_id == 1.0: # check if the class id is actually an enemy
                    detected += 1

            if detected >= 1:
                if time.time() - cooldown > 30:  # 30 seconds
                    cooldown = time.time()
                    spk.sayVoice("voices/mio/new-round/respawn - more_enemies_what_do_we_do.wav")




    def beginYoloV8Detection(self):


        if self.monitorProcess is None or not self.monitorProcess.is_alive():
            self.monitorProcess = Process(target=self.yoloV8Detection)
            self.monitorProcess.daemon = True
            self.monitorProcess.start()
            return


        return



    def beginEnemyDetection(self):


        if self.monitorProcess is None or not self.monitorProcess.is_alive():
            self.monitorProcess = Process(target=self.findEnemy)
            self.monitorProcess.daemon = True
            self.monitorProcess.start()
            return


        return

if __name__ == "__main__":
    em = EnemyManager(visualize=True)
    em.yoloV8Detection()