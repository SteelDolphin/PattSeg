import cv2
import numpy as np

# 读取图像
image = cv2.imread('./pattern/01.jpg')
Z = image.reshape((-1, 3))

# 转换为浮点数
Z = np.float32(Z)

# 定义K-means参数
K = 3
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# 将中心转回到uint8
center = np.uint8(center)
segmented_image = center[label.flatten()]
segmented_image = segmented_image.reshape(image.shape)

# 显示结果
cv2.imshow('Segmented Image', segmented_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
