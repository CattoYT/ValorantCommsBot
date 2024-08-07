# This file is highly experimental, and will only be integrated into the main project if this is
# 1. Useful
# 2. Not a complete waste of time
# 3. Functional
# 4. Doesn't fuck the performance
# This file might also use a bit of code from SociallyIneptWeeb/LanguageLeapAI because there is a text overlay there using tkinter
# I might move this into a different language cuz this python codebase is already a mess
import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt

def setup_overlay():
    app = QApplication(sys.argv)

    # Create the overlay widget to cover the entire screen
    overlay = QWidget()
    overlay.setWindowFlags(
        Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.X11BypassWindowManagerHint)
    overlay.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    overlay.setGeometry(0, 0, 1536, 834)
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

    label1 = QLabel(overlay)
    label1.setText("150")
    label1.setStyleSheet(
        "font-family: 'JetBrains Mono'; font-size: 14pt; font-style: italic; color: white; background-color: rgba(0, 0, 0, 0);")
    label1.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    label1.setGeometry(934, 69, 38, 18)

    # Create and configure the second label
    label2 = QLabel(overlay)
    label2.setText("200")
    label2.setStyleSheet(
        "font-family: 'JetBrains Mono'; font-size: 14pt; font-style: italic; color: white; background-color: rgba(0, 0, 0, 0);")
    label2.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    #(x, y, width, height) :/ This took me about 10 minutes to realise and a chatgpt question
    label2.setGeometry(986, 69, 38, 18) # these values will be hardcoded for my machine, i dont give a fuck fix them yourself

    # Create and configure the second label
    label3 = QLabel(overlay)
    label3.setText("200")
    label3.setStyleSheet(
        "font-family: 'JetBrains Mono'; font-size: 14pt; font-style: italic; color: white; background-color: rgba(0, 0, 0, 0);")
    label3.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    #(x, y, width, height) :/ This took me about 10 minutes to realise and a chatgpt question
    label3.setGeometry(1038, 69, 38, 18) # these values will be hardcoded for my machine, i dont give a fuck fix them yourself

    # Create and configure the second label
    label4 = QLabel(overlay)
    label4.setText("200")
    label4.setStyleSheet(
        "font-family: 'JetBrains Mono'; font-size: 14pt; font-style: italic; color: white; background-color: rgba(0, 0, 0, 0);")
    label4.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    #(x, y, width, height) :/ This took me about 10 minutes to realise and a chatgpt question
    label4.setGeometry(1090, 69, 38, 18) # these values will be hardcoded for my machine, i dont give a fuck fix them yourself

    # Create and configure the second label
    label5 = QLabel(overlay)
    label5.setText("200")
    label5.setStyleSheet(
        "font-family: 'JetBrains Mono'; font-size: 14pt; font-style: italic; color: white; background-color: rgba(0, 0, 0, 0);")
    label5.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    #(x, y, width, height) :/ This took me about 10 minutes to realise and a chatgpt question
    label5.setGeometry(1142, 69, 38, 18) # these values will be hardcoded for my machine, i dont give a fuck fix them yourself


    overlay.show()

    sys.exit(app.exec())

setup_overlay()