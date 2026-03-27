import sys
from PyQt6.QtWidgets import QApplication
from xuly2 import DangNhapWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DangNhapWindow()
    window.show()
    sys.exit(app.exec())


