import cv2
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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