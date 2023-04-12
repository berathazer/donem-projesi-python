import cv2

# reader = easyocr.Reader(['en'], gpu=True)

image = cv2.imread("./cars/car-3.jpg")

x, y, ch = image.shape
image = image[int(x / 2):x, 0:y]
image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

_, image = cv2.threshold(
    image, 0, 25, cv2.THRESH_BINARY + cv2.THRESH_OTSU,
)

cv2.imshow("resim", image)
cv2.waitKey(0)

'''

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

filter = cv2.bilateralFilter(gray, 9, 75, 75)

edges = cv2.Canny(filter, 100, 200)

contours, a = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# bulunan kontürleri numpy array'ine çevircik
contours = imutils.grab_contours((contours, a))

# En iyi 20 konturu bulduk
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:20]

border = None

for contour in contours:
    epsilon = 0.012 * cv2.arcLength(contour, True)

    approx = cv2.approxPolyDP(contour, epsilon, True)

    # 4 kenarlı bir şekil bulduğumuzda duruyoruz.
    if len(approx) == 4:
        border = approx
        break

# resmin boyutu kadar siyah bir filtre oluşturduk
maske = np.zeros(gray.shape, np.uint8)

# önceden oluşturduğumuz siyah filtrenin border bölgesini beyaza boyuyoruz.
cv2.drawContours(maske, [border], 0, (255, 255, 255), -1)

filteredPlate = cv2.bitwise_and(image, image, mask=maske)

(x, y) = np.where(maske == 255)
(x_min, y_min) = (np.min(x), np.min(y))
(x_max, y_max) = (np.max(x), np.max(y))

# ROI (kırpma işlemi)
correctPlate = gray[x_min:x_max, y_min:y_max]


cv2.imshow("Filtre", filter)
cv2.imshow("Canny", edges)
cv2.imshow("maske", maske)
cv2.imshow("filteredPlate", filteredPlate)
cv2.imshow("currentPlate", correctPlate)


# Resimden plaka okuma
result = reader.readtext(correctPlate, detail=0)
print(result)


cv2.waitKey(0)
cv2.destroyAllWindows()

'''
