import time
from multiprocessing import Process, Event

import detectors
import cv2
import numpy as np
from mss.windows import MSS as mss
from PIL import Image


class EnemyManager:
    def __init__(self, visualize=False):
        self.visualize = visualize
        self.stopEvent = Event()
        self.monitorProcess = None
        self.model = None
        self.enemyCount = 0




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


    def beginEnemyDetection(self):


        if self.monitorProcess is None or not self.monitorProcess.is_alive():
            self.monitorProcess = Process(target=self.findEnemy)
            self.monitorProcess.daemon = True
            self.monitorProcess.start()
            return
        return

if __name__ == "__main__":
    em = EnemyManager(visualize=True)
    em.beginEnemyDetection()
    while True:
        print(em.enemyCount)
        time.sleep(1)
        pass