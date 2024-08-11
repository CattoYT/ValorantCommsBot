# This file is highly experimental, and will only be integrated into the main project if this is
# 1. Useful
# 2. Not a complete waste of time
# 3. Functional
# 4. Doesn't fuck the performance
# This file might also use a bit of code from SociallyIneptWeeb/LanguageLeapAI because there is a text overlay there using tkinter
# I might move this into a different language cuz this python codebase is already a mess


# TODO: ORGANISE THIS FILE
import sys
import threading
from multiprocessing import Process

from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt

class HealthLabel:
    def __init__(self, parentWindow, initialValue=150, offset=0):
        # the offset variable controls which player indicator is which
        # the first enemy from the left on the top hud is offset 0, second is offset 1, etc

        self.label = QLabel(parentWindow)

        self.label.setText(str(initialValue))

        self.label.setStyleSheet(
            "font-family: 'JetBrains Mono'; font-size: 14pt; font-style: italic; color: white; background-color: rgba(0, 0, 0, 0);")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.label.setGeometry(934 + (offset*52), 69, 38, 18)

    def updateLabel(self, value):
        self.label.setText(str(value))
    def getLabel(self):
        self.label.text()



def drawIMG(overlay):
    # This image code can be used later ig for a lineup guide but will only be used for debugging for now. Thanks chatgpt for this section
    scaling_factor = 1.25
    pixmap = QPixmap('../img.png')
    scaled_width = int(pixmap.width() / scaling_factor)
    scaled_height = int(pixmap.height() / scaling_factor)
    scaled_pixmap = pixmap.scaled(scaled_width, scaled_height, Qt.AspectRatioMode.KeepAspectRatio)
    transparent_pixmap = QPixmap(scaled_pixmap.size())
    transparent_pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(transparent_pixmap)
    #painter.setOpacity(0.5)
    painter.drawPixmap(0, 0, scaled_pixmap)
    painter.end()
    image_label = QLabel(overlay)
    image_label.setPixmap(transparent_pixmap)
    image_label.setGeometry(0, 0, transparent_pixmap.width(), transparent_pixmap.height())

# Issue with this file, it causes MAD PERFORMANCE ISSUES

global label1, label2, label3, label4, label5
def setup_overlay():
    global label1, label2, label3, label4, label5
    global overlay
    app = QApplication(sys.argv)

    # Create the overlay widget to cover the entire screen
    overlay = QWidget()
    overlay.setWindowFlags(
        Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.X11BypassWindowManagerHint)
    overlay.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    overlay.setGeometry(0, 0, 1536, 834)
    #drawIMG(overlay)
    label1 = HealthLabel(overlay, 150, 0)
    label2 = HealthLabel(overlay, 150, 1)
    label3 = HealthLabel(overlay, 150, 2)
    label4 = HealthLabel(overlay, 150, 3)
    label5 = HealthLabel(overlay, 150, 4)

    app.exec()

    sys.exit(app.exec())





setup_overlay()

