import cv2
import numpy as np

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
    tiled_image = np.zeros((4000, total_width, 3), dtype=np.uint8)

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
