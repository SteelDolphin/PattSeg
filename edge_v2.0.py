import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
from sklearn.cluster import KMeans

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

# def segment_image(edges, image):
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

def padding_part(shapes, fill_colors, bounding_rects, original_colors):
    
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

    for idx, (shape, color, rect) in enumerate(zip(shapes, fill_colors, bounding_rects)):
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

def classify_by_color_and_area(original_colors, bounding_rects):
    """
    根据原图颜色和区域的面积对图像进行分类
    :param original_colors: 每个区域的原图颜色
    :param bounding_rects: 每个区域的最小外接矩形
    :return: 每个区域的类别标签
    """
    areas = [(w * h) for _, _, w, h in bounding_rects]  # 计算面积
    original_colors = np.array(original_colors).reshape(-1, 3)  # 将颜色转换为二维数组

    # 使用 K-means 对原图颜色进行聚类
    kmeans = KMeans(n_clusters=5, random_state=42)
    color_labels = kmeans.fit_predict(original_colors)

    # 根据面积进行简单的分类：小、中、大三类
    area_labels = np.digitize(areas, bins=np.percentile(areas, [33, 66]))

    # 将颜色标签和面积标签结合，作为最终的类别
    final_labels = color_labels * 10 + area_labels

    return final_labels

def segment_image(edges, image):
    """
    对图像进行区域分割并分类
    """
    top, bottom, left, right = 1, 1, 1, 1
    border_color = [255, 255, 255]
    bordered_image = cv2.copyMakeBorder(edges, top, bottom, left, right, cv2.BORDER_CONSTANT, value=border_color)
    bordered_origin_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=border_color)

    _, binary = cv2.threshold(bordered_image, 200, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=3)

    contours, _ = cv2.findContours(morph.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    shapes = []
    fill_colors = []  # 用于填充的颜色
    original_colors = []  # 每个区域的原图颜色
    bounding_rects = []

    colored_image = np.zeros_like(bordered_origin_image)

    for i, contour in enumerate(contours):
        if i == 0:
            continue
        
        # 生成随机颜色进行填充
        fill_color = (np.random.randint(50, 255), np.random.randint(50, 255), np.random.randint(50, 255))
        cv2.drawContours(colored_image, [contour], -1, fill_color, thickness=cv2.FILLED)

        # 记录轮廓形状和填充颜色
        shapes.append(contour)
        fill_colors.append(fill_color)

        # 计算最小外接矩形
        x, y, w, h = cv2.boundingRect(contour)
        bounding_rects.append((x, y, w, h))

        # 获取区域的原图颜色（通过均值计算）
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [contour], -1, 255, -1)
        mean_color = cv2.mean(image, mask=mask)[:3]  # 获取原图中的主要颜色
        original_colors.append(mean_color)

    # 对区域进行分类
    labels = classify_by_color_and_area(original_colors, bounding_rects)

    # 在 colored_image 上标记类别
    for (x, y, w, h), label in zip(bounding_rects, labels):
        cv2.putText(colored_image, f'Class {label}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    return {'shapes':shapes, 'fill_colors':fill_colors, 'original_colors':original_colors, 'bounding_rects':bounding_rects}, colored_image

def recolor_by_classification(shapes, labels, cluster_centers, bounding_rects, image_size):
    """
    根据颜色类别重新填色
    :param shapes: 每个区域的轮廓
    :param labels: 每个区域的颜色类别标签
    :param cluster_centers: 聚类中心颜色
    :param bounding_rects: 每个区域的最小外接矩形
    :param image_size: 图像大小 (高, 宽, 通道数)
    :return: 重新填色的图像
    """
    color_map = {
        0: (255, 0, 0),    # 红色
        1: (0, 255, 0),    # 绿色
        2: (0, 0, 255),    # 蓝色
        3: (255, 255, 0),  # 黄色
        4: (255, 165, 0),  # 橙色
    }
    # 创建一个空白图像来填充分类后的颜色
    recolored_image = np.zeros(image_size, dtype=np.uint8)

    # 遍历每个区域并根据颜色类别填充相应颜色
    for idx, (shape, label, rect) in enumerate(zip(shapes, labels, bounding_rects)):
        x, y, w, h = rect

        # 获取该区域的颜色类别的聚类中心颜色
        # color = tuple(map(int, cluster_centers[label]))  # 转换为整数
        color = color_map[label]  # 转换为整数

        # 在新的图像上填充该区域
        cv2.drawContours(recolored_image, [shape], -1, color, thickness=cv2.FILLED)

    return recolored_image

def classify_colors(original_colors, n_clusters=5):
    """
    使用 K-means 聚类对原图颜色进行分类
    :param original_colors: 每个区域的原图颜色
    :param n_clusters: 聚类的类别数
    :return: 每个区域的颜色类别标签
    """
    # 将原图颜色转换为二维数组 (n, 3)，每个颜色表示一个区域的主色
    original_colors = np.array(original_colors).reshape(-1, 3)

    # 使用 K-means 对颜色进行聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(original_colors)

    # 返回每个区域的颜色分类标签
    return labels, kmeans.cluster_centers_

# 提供图片的路径
images = glob.glob('AI/17.*')

for image_path in images:

    # 读取图像
    origin_image = read_image_by_path(image_path)
    # 检测图像边沿
    edges_image = canny_edge_detector(origin_image)

    # 显示原图和边缘检测后的图像
    plt.figure(figsize=(10, 5))
    plt.subplot(121), plt.imshow(cv2.cvtColor(origin_image, cv2.COLOR_BGR2RGB))
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(edges_image, cmap='gray')
    plt.title('Edge Detection'), plt.xticks([]), plt.yticks([])
    plt.show()

    # 划分区域
    data, colored_image = segment_image(edges_image, origin_image)
    # 平铺色块
    tiled_image = padding_part(**data)
    # 对原图颜色进行分类
    labels, cluster_centers = classify_colors(data['original_colors'], n_clusters=3)
    # 根据分类重新填色
    recolored_image = recolor_by_classification(
        shapes=data['shapes'], 
        labels=labels, 
        cluster_centers=cluster_centers, 
        bounding_rects=data['bounding_rects'], 
        image_size=origin_image.shape
    )
    # 显示重新填色的图像
    plt.figure(figsize=(12, 12))
    plt.subplot(121), plt.imshow(cv2.cvtColor(origin_image, cv2.COLOR_BGR2RGB))
    plt.title('Original Colored Regions')
    plt.subplot(122), plt.imshow(cv2.cvtColor(recolored_image, cv2.COLOR_BGR2RGB))
    plt.title('Recolored by Classification')
    plt.axis('off')
    plt.show()

    # 12. 显示平铺的图像
    plt.figure(figsize=(12, 12))
    plt.subplot(121), plt.imshow(cv2.cvtColor(colored_image, cv2.COLOR_BGR2RGB))
    plt.title('Colored Regions')
    plt.subplot(122), plt.imshow(cv2.cvtColor(tiled_image, cv2.COLOR_BGR2RGB))
    plt.title('Adaptive Tiled Bounding Rectangles with Padding')
    plt.axis('off')
    plt.show()