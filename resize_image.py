import cv2 as cv

img = cv.imread("fadi.jpg")
resized_image = cv.resize(img, (300, 300))
cv.imshow("Resize", resized_image)
cv.imwrite("fadi_resized.jpg",resized_image)
cv.waitKey(0)
cv.destroyAllWindows()
