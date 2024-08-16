import sys
import threading

from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject

# Worker object and signals are done by chatgpt,I couldn't find out how this works and i couldn't find the docs :/
class Worker(QObject):
    update_label_signal = pyqtSignal(int, int)  # Signal to update label (index, value)

    def __init__(self):
        super().__init__()

    def update_label(self, index, value):
        self.update_label_signal.emit(index, value)

class HealthLabel:
    def __init__(self, parentWindow, initialValue=150, offset=0):
        self.label = QLabel(parentWindow)
        self.label.setText(str(initialValue))
        self.label.setStyleSheet("font-family: 'JetBrains Mono'; font-size: 14pt; font-style: italic; color: white; background-color: rgba(0, 0, 0, 0);")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.label.setGeometry(934 + (offset * 52), 69, 38, 18)

    def updateLabel(self, value):
        print("Desired value: " + value)
        self.label.setText(str(value))

global worker, label1, label2, label3, label4, label5

def setup_overlay():
    global worker, label1, label2, label3, label4, label5

    app = QApplication(sys.argv)

    overlay = QWidget()
    overlay.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.X11BypassWindowManagerHint)
    overlay.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    overlay.setGeometry(0, 0, 1536, 834)

    # Instantiate HealthLabel instances
    label1 = HealthLabel(overlay, 150, 0)
    label2 = HealthLabel(overlay, 150, 1)
    label3 = HealthLabel(overlay, 150, 2)
    label4 = HealthLabel(overlay, 150, 3)
    label5 = HealthLabel(overlay, 150, 4)

    # Worker and thread setup
    worker = Worker()
    worker_thread = QThread()
    worker.moveToThread(worker_thread)

    # Connect signals to the slot that updates labels
    worker.update_label_signal.connect(lambda index, value: update_label(index, value))
    worker_thread.start()

    overlay.show()
    sys.exit(app.exec())

def update_label(index, value):
    labels = [label1, label2, label3, label4, label5]
    if 0 <= index < len(labels):
        labels[index].updateLabel(str(int(labels[index].label.text()) - int(value)))

def startSetup():
    global worker
    threading.Thread(target=setup_overlay, daemon=True).start()


# Each agent has a 40x40 area at the top of the screen.
# Player 1 on your team is at x=710 and y=30
# Player 2 is x=644
# P3 is x=578
# The offset for the left team from P1 is
# Once the agent has been found, I can map that agent to the label and position.
# However, when a player dies, their model is shoved closer to the middle
# When this happens, i can run a scan again and move the labels accordingly
# I also don't need to research for each agent, i can just check for the ones found in the first place
# store them in a list or something ideally, maybe even a dict
