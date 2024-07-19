from multiprocessing import Process, Event
from Modules import speaker as spk
import cv2
import numpy as np
from mss.windows import MSS as mss
from PIL import Image

class EnemyManger:
    def __init__(self, visualize=False):

        self.visualize = visualize
        self.stopEvent = Event()
        self.monitorProcess = None
        self.model = None




    def findEnemy(self):

        if self.model == None:
            import torch
            self.model = torch.hub.load(R'yolov5', 'custom', 'valorant-11.engine', source='local', force_reload=True)

        with mss() as sct:
            # cap my first monitor
            monitor = sct.monitors[2]

            while not self.stopEvent.is_set():

                sct_img = sct.grab(monitor)
                img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
                self.model.conf = 0.5
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
if __name__ == "__main__":

    enemyMGR = EnemyManger()
    enemyMGR.beginScreenRecording()
