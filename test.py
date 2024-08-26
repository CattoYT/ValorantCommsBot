import sys
import threading
import time

from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject

from Modules.OverlayModule.OverlayUtils import HealthLabel


# Worker object and signals are done by chatgpt,I couldn't find out how this works and i couldn't find the docs :/



class Worker(QObject):
    update_label_signal = pyqtSignal(int, int)  # Signal to update label (index, value)
    updateLabelPositionSignal = pyqtSignal(int, int)  # Signal to update label position (index, value)
    def __init__(self):
        super().__init__()

    def update_label(self, index, value):
        self.update_label_signal.emit(index, value)

global overlay, worker, label1, label2, label3, label4, label5
worker = Worker()


class QTOverlay:
    def __init__(self, agentTracker=None):
        self.agentTracker = agentTracker


    global worker
    def getWorker(self):
        return worker
    def setup_overlay(self):
        global overlay, worker, label1, label2, label3, label4, label5

        app = QApplication(sys.argv)

        overlay = QWidget()
        overlay.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        overlay.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        overlay.setGeometry(0, 0, 1536, 834)

        # Instantiate HealthLabel instances
        label1 = HealthLabel(overlay, 150, 0)
        label2 = HealthLabel(overlay, 150, 1)
        label3 = HealthLabel(overlay, 150, 2)
        label4 = HealthLabel(overlay, 150, 3)
        label5 = HealthLabel(overlay, 150, 4)




        # Worker and thread setup
        worker_thread = QThread()
        worker.moveToThread(worker_thread)

        # Connect signals to the slot that updates labels
        worker.update_label_signal.connect(lambda index, value: self.update_label(index, value))
        worker.updateLabelPositionSignal.connect(lambda index, value: self.updateLabelPosition(index, value))

        worker_thread.start()
        overlay.show()
        sys.exit(app.exec())





    def startSetup(self):
        global worker
        threading.Thread(target=self.setup_overlay, daemon=True).start()



if __name__ == "__main__":
    overlay = QTOverlay()
    overlay.startSetup()
    while True:
        time.sleep(5)
        label5.updateLabel(str(600))
        print("he")