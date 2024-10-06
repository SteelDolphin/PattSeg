import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

def canny_edge_detector(image_path):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print("Error: 图像未找到，请检查路径是否正确。")
        return
    
    # 将图像转换为灰度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 对图像进行高斯模糊处理，减少噪声的影响
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # 应用Canny边缘检测
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)
    
    # 3. 使用 copyMakeBorder 函数扩展图像，增加边框
    top, bottom, left, right = 1, 1, 1, 1
    border_color = [255, 255, 255]
    bordered_image = cv2.copyMakeBorder(edges, top, bottom, left, right, cv2.BORDER_CONSTANT, value=border_color)

    # 4. 二值化图像
    _, binary = cv2.threshold(bordered_image, 200, 255, cv2.THRESH_BINARY)
    
    # 5. 使用形态学操作分离紧邻区域
    kernel = np.ones((5, 5), np.uint8)
    morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=3)

    # 6. 查找轮廓
    contours, _ = cv2.findContours(morph.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 用于记录形状和颜色的列表
    shapes = []
    colors = []

    # 7. 创建一个全黑的图像用于填充区域
    colored_image = np.zeros_like(image)

    # 8. 为每个区域上色并记录形状和颜色
    for i, contour in enumerate(contours):
        # 生成随机颜色
        color = (np.random.randint(50, 255), np.random.randint(50, 255), np.random.randint(50, 255))
        cv2.drawContours(colored_image, [contour], -1, color, thickness=cv2.FILLED)
        
        # 记录轮廓形状和颜色
        shapes.append(contour)
        colors.append(color)

    # 9. 在新图像中平铺显示每个色块
    rows = len(contours)
    cols = 10  # 假设每行展示两个形状
    tile_size = 1000  # 每个图块的大小

    tiled_image = np.zeros((rows * tile_size, cols * tile_size, 3), dtype=np.uint8)

    for idx, (shape, color) in enumerate(zip(shapes, colors)):
        # 确定每个形状在 tiled_image 中的位置
        row = idx // cols
        col = idx % cols
        offset_y = row * tile_size
        offset_x = col * tile_size

        # 在 tiled_image 中创建一个小画布来放置当前的轮廓
        tile = np.zeros((tile_size, tile_size, 3), dtype=np.uint8)

        # 将形状绘制到这个小画布上
        cv2.drawContours(tile, [shape], -1, color, thickness=cv2.FILLED)

        # 将 tile 复制到 tiled_image 的相应位置
        tiled_image[offset_y:offset_y + tile_size, offset_x:offset_x + tile_size] = tile

    # 10. 显示原始图像、上色后的图像和平铺图像
    plt.figure(figsize=(15, 5))
    plt.subplot(121), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)), plt.title('Original Image')
    plt.subplot(122), plt.imshow(cv2.cvtColor(colored_image, cv2.COLOR_BGR2RGB)), plt.title('Colored Regions')
    plt.show()

    # 10. 单独显示平铺图像
    plt.figure(figsize=(8, 8))
    plt.imshow(cv2.cvtColor(tiled_image, cv2.COLOR_BGR2RGB))
    plt.title('Tiled Shapes')
    plt.axis('off')
    plt.show()

# 提供图片的路径
images = glob.glob('AI/16.*')

for image_file in images:
    canny_edge_detector(image_file)
