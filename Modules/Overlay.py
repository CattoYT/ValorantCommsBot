# This file is highly experimental, and will only be integrated into the main project if this is
# 1. Useful
# 2. Not a complete waste of time
# 3. Functional
# 4. Doesn't fuck the performance
# This file might also use a bit of code from SociallyIneptWeeb/LanguageLeapAI because there is a text overlay there using tkinter
# I might move this into a different language cuz this python codebase is already a mess

from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtCore import Qt
import sys

def setup_overlay():
    app = QApplication(sys.argv)

    overlay = QWidget()
    overlay.setWindowFlags(
        Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.X11BypassWindowManagerHint)
    overlay.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    overlay.setGeometry(180, -800, app.primaryScreen().size().width(), app.primaryScreen().size().height())

    label1 = QLabel(overlay)
    label1.setText("150")
    label1.setStyleSheet(
        "font-family: 'Comic Sans MS'; font-size: 14pt; font-style: italic; color: white; background-color: rgba(0, 0, 0, 0);")
    label1.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
    label1.setGeometry(0, overlay.height() - 50, overlay.width(), 50)

    overlay.show()

    sys.exit(app.exec())

setup_overlay()