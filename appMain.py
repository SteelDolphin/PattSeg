import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap
from ui_MainWindow import Ui_MainWindow  # 导入 Qt Designer 生成的界面

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # 将 "打开文件" 菜单项的点击事件绑定到 self.open_file 方法
        self.actionOpenFile.triggered.connect(self.open_file)

    def open_file(self):
        # 弹出文件对话框，选择图像文件
        file_name, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "图片文件 (*.png *.jpg *.bmp)")

        if file_name:
            # 加载并显示图片
            pixmap = QPixmap(file_name)
            self.label.setPixmap(pixmap)
            # self.label.setScaledContents(True)  # 让图片适应 QLabel 大小
            # 调整 QLabel 的大小以适应图片
            self.label.adjustSize()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
