import sys
import glob
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog, QWidget, QPushButton
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ui_MainWindow import Ui_MainWindow  # 导入 Qt Designer 生成的界面

def read_image_by_path(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: 图像未找到，请检查路径是否正确。")
        return None
    return image

def canny_edge_detector(image):

    if image.all():
        print("Error: 图像未找到")
        return False
    # 将图像转换为灰度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 对图像进行高斯模糊处理，减少噪声的影响
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # 应用Canny边缘检测
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

    return edges

def segment_image(edges, image):
    # 1. 使用 copyMakeBorder 函数扩展图像，增加边框
    top, bottom, left, right = 1, 1, 1, 1
    border_color = [255, 255, 255]
    bordered_image = cv2.copyMakeBorder(edges, top, bottom, left, right, cv2.BORDER_CONSTANT, value=border_color)
    bordered_origin_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=border_color)

    # 4. 二值化图像
    _, binary = cv2.threshold(bordered_image, 200, 255, cv2.THRESH_BINARY)
    
    # 5. 使用形态学操作分离紧邻区域
    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=3)

    # 6. 查找轮廓
    contours, _ = cv2.findContours(morph.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 用于记录形状、颜色和最小矩形的列表
    shapes = []
    colors = []
    bounding_rects = []

    # 7. 创建一个全黑的图像用于填充区域
    colored_image = np.zeros_like(bordered_origin_image)

    # 8. 为每个区域上色、计算最小矩形并记录
    for i, contour in enumerate(contours):
        if i == 0:
            continue
        # 生成随机颜色
        color = (np.random.randint(50, 255), np.random.randint(50, 255), np.random.randint(50, 255))
        cv2.drawContours(colored_image, [contour], -1, color, thickness=cv2.FILLED)
        
        # 记录轮廓形状和颜色
        shapes.append(contour)
        colors.append(color)
        
        # 计算最小外接矩形
        x, y, w, h = cv2.boundingRect(contour)
        bounding_rects.append((x, y, w, h))

    return {'shapes':shapes, 'colors':colors, 'bounding_rects':bounding_rects}, colored_image

def padding_part(shapes, colors, bounding_rects):
    
    padding = 20
    # 9. 计算合适的图像大小来平铺所有色块
    total_width = 2000  # 平铺图像的最大宽度（可以根据需要调整）
    max_tile_size = max([max(w, h) for _, _, w, h in bounding_rects])  # 动态确定最大矩形

    # 10. 创建一个足够大的新图像来放置平铺结果
    tiled_image = np.zeros((3000, total_width, 3), dtype=np.uint8)

    # 11. 自适应平铺每个色块，增加padding间隔
    offset_x = padding
    offset_y = padding
    max_row_height = 0

    for idx, (shape, color, rect) in enumerate(zip(shapes, colors, bounding_rects)):
        x, y, w, h = rect

        # 创建一个空白图块并将矩形绘制上去
        tile = np.zeros((h, w, 3), dtype=np.uint8)
        cv2.drawContours(tile, [shape - [x, y]], -1, color, thickness=cv2.FILLED)  # 减去偏移量

        # 判断是否需要换行
        if offset_x + w + padding > total_width:
            offset_x = padding
            offset_y += max_row_height + padding
            max_row_height = 0

        # 更新当前行的最大高度
        max_row_height = max(max_row_height, h)

        # 将 tile 放到 tiled_image 中相应的位置
        tiled_image[offset_y:offset_y + h, offset_x:offset_x + w] = tile[:h, :w]

        # 更新下一个 tile 的放置位置，留出padding
        offset_x += w + padding
        
    return tiled_image

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MatplotlibCanvas, self).__init__(self.fig)

    def clear_plot(self):
        self.axes.clear()

    def plot_images(self, origin_image, edges_image):
        # 在画布中绘制图像
        self.fig.clf()  # 清除之前的图像
        self.axes1 = self.fig.add_subplot(121)
        self.axes2 = self.fig.add_subplot(122)

        self.axes1.imshow(cv2.cvtColor(origin_image, cv2.COLOR_BGR2RGB))
        self.axes1.set_title('Original Image')
        self.axes1.axis('off')

        self.axes2.imshow(edges_image, cmap='gray')
        self.axes2.set_title('Edge Detection')
        self.axes2.axis('off')

        self.draw()

    def plot_segmented_images(self, colored_image, tiled_image):
        # 绘制平铺和区域分割的图像
        self.fig.clf()
        self.axes1 = self.fig.add_subplot(121)
        self.axes2 = self.fig.add_subplot(122)

        self.axes1.imshow(cv2.cvtColor(colored_image, cv2.COLOR_BGR2RGB))
        self.axes1.set_title('Colored Regions')
        self.axes1.axis('off')

        self.axes2.imshow(cv2.cvtColor(tiled_image, cv2.COLOR_BGR2RGB))
        self.axes2.set_title('Adaptive Tiled Bounding Rectangles with Padding')
        self.axes2.axis('off')

        self.draw()


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

        # if file_name:
        #     # 加载并显示图片
        #     pixmap = QPixmap(file_name)
        #     self.label.setPixmap(pixmap)
        #     # self.label.setScaledContents(True)  # 让图片适应 QLabel 大小
        #     # 调整 QLabel 的大小以适应图片
        #     self.label.adjustSize()

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
        images = glob.glob('AI/16.*')

        for image_path in images:
            # 读取图像
            origin_image = read_image_by_path(image_path)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())