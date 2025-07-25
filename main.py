import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from PyQt6.QtGui import QIcon
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Zet het taakbalkicoon (vereist voor Windows)
    icon_path = os.path.join(os.path.dirname(__file__), "resources", "icon.png")
    app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
