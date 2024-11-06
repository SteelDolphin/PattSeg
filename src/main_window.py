import sys
import glob
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog
from src.ui_main_window import Ui_MainWindow
from src.matplot_canvas import MatplotlibCanvas
from src.utils import *

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # 将 "打开文件" 菜单项的点击事件绑定到 self.open_file 方法
        self.actionOpenFile.triggered.connect(self.open_file)

        # 创建一个 Matplotlib 画布
        self.canvas_1 = MatplotlibCanvas(self, width=8, height=6, dpi=100)
        self.canvas_2 = MatplotlibCanvas(self, width=8, height=6, dpi=100)


        # 创建加载图像按钮
        self.button.clicked.connect(self.load_and_process_images)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.canvas_1)
        layout.addWidget(self.canvas_2)

        # 将 canvas 添加到 plotWidget 中
        self.plotWidget.setLayout(layout)

    def open_file(self):
        # 弹出文件对话框，选择图像文件
        file_name, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "图片文件 (*.png *.jpg *.bmp)")
        self.process_images(file_name)

    def process_images(self, file_name):
        # 读取图像
        origin_image = read_image_by_path(file_name)
        # 检测图像边沿
        edges_image = canny_edge_detector(origin_image)

        # 显示原图和边缘检测后的图像在画布上
        self.canvas_1.plot_images(origin_image, edges_image)

        # 划分区域
        data, colored_image = segment_image(edges_image, origin_image)
        # 平铺色块
        tiled_image = padding_part(**data)

        # 显示分割的彩色区域和平铺后的图像在画布上
        self.canvas_2.plot_segmented_images(colored_image, tiled_image)

    def load_and_process_images(self):
        # 获取所有图像路径
        images = glob.glob('data/AI_processed/16.*')

        for image_path in images:
            self.process_images(image_path)