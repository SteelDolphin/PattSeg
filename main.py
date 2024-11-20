import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from src.views.main_window_view import MainWindow

# import qdarkstyle

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/icon.png"))
    # 应用 QDarkStyle 主题
    # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
