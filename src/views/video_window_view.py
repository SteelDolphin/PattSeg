import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QVBoxLayout, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

class VideoStreamWidget(QDialog):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和布局
        self.setWindowTitle("视频流显示窗口")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建布局和控件
        self.layout = QVBoxLayout()
        self.video_label = QLabel()
        self.start_button = QPushButton("开始视频")
        self.stop_button = QPushButton("停止视频")
        
        # 将控件添加到布局中
        self.layout.addWidget(self.video_label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.setLayout(self.layout)

        # 初始化摄像头捕获
        self.cap = cv2.VideoCapture(0)  # 0 表示使用默认摄像头
        self.timer = QTimer()
        
        # 连接按钮和定时器
        self.start_button.clicked.connect(self.start_video)
        self.stop_button.clicked.connect(self.stop_video)
        self.timer.timeout.connect(self.update_frame)

    def start_video(self):
        self.timer.start(30)  # 每30ms更新一次图像

    def stop_video(self):
        self.timer.stop()
        self.video_label.clear()  # 清除视频标签上的内容

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # 将图像从BGR格式转换为RGB格式
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 获取图像大小并转换为Qt格式
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            # 显示图像
            self.video_label.setPixmap(QPixmap.fromImage(qimg))

    def closeEvent(self, event):
        # 释放摄像头
        self.cap.release()
        event.accept()

if __name__ == "__main__":
    # 主程序
    app = QApplication(sys.argv)
    window = VideoStreamWidget()
    window.show()
    sys.exit(app.exec_())
