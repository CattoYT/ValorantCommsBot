import time
from multiprocessing import Process, Event
import speaker as spk
import cv2
from PIL import Image
import numpy as np
from mss.windows import MSS as mss

class EnemyManger:
    def __init__(self, visualize=False):
        import torch
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', 'valorant-11.engine', source="local")
        self.visualize = visualize
        self.stopEvent = Event()
        self.monitorProcess = None




    def findEnemy(self):


        with mss() as sct:
            # cap my first monitor
            monitor = sct.monitors[2]

            while not self.stopEvent.is_set():

                sct_img = sct.grab(monitor)

                self.model.conf = 0.5
                results = self.model(sct_img)
                self.enemyCount = 0

                # thanks copilot for this lol
                if self.visualize:
                    cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
                    img_cv = cv2.cvtColor(np.array(sct_img), cv2.COLOR_RGB2BGR)

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
                    cv2.waitKey(1)
                else:
                    for det in results.pred[0]:
                        if det[4] > self.model.conf:
                            self.enemyCount += 1

                if self.enemyCount > 0:
                    print("Enemies: self.enemyCount")
                    spk.sayVoice("voices/VO_Firefly_Enemy_Target_Found_01.ogg")

    def beginScreenRecording(self):


        if self.monitorProcess is None or not self.monitorProcess.is_alive():
            self.monitorProcess = Process(target=self.findEnemy)
            self.monitorProcess.start()

enemyMGR = EnemyManger()
enemyMGR.beginScreenRecording()
