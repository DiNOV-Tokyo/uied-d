import cv2



pos = (100, 100)



img = cv2.imread("./data/input/news.jpg", cv2.IMREAD_UNCHANGED)

color = img[pos]

print(f"Image[{pos}] = BGRA{color}")
