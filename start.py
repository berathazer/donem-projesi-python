import re
import threading
from datetime import datetime

import cv2
import numpy as np
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\berat\AppData\Local\Programs\Tesseract-OCR\tesseract'

custom_tesseract_config = r'--oem 3 --psm 6'

areatxt = open("area.txt","a")
aspecttxt = open("aspect_ratio.txt","a")

capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
capture2 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
plakalar = dict({})

def filtre(string):
    temiz_string = re.sub(r'[^a-zA-Z0-9]', '', string)
    return temiz_string

def turkiye_plakasimi(plaka):
    regex = r'^[0-8][0-9][A-Z]{1,3}[0-9]{2,4}$'
    if re.match(regex, plaka):
        return True
    else:
        return False

def plakayiOku(image, x, y, frame):

    plaka = pytesseract.image_to_string(image,config=custom_tesseract_config)

    plaka = filtre(plaka)

    if turkiye_plakasimi(plaka):
        height, width, _ = image.shape

        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

        cv2.putText(frame, plaka, (x - 10, y - 20), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), thickness=3)

        if plaka not in plakalar:
            plakalar[plaka] = 1
            print(f"Okunan Plaka: {plaka}, Okunma Sayisi: {1}")

            su_an = datetime.now()

            su_an_str = su_an.strftime("%Y-%m-%d_%H.%M.%S")

            cv2.imwrite("./plateOnly/plaka-" + su_an_str + ".jpg", image)

            cv2.imwrite("./okunanPlakalar/plaka-" + su_an_str + ".jpg", frame)

        else:
            plakalar[plaka] += 1
            cv2.imwrite("./plates/plate.jpg", frame)
            print(f"Okunan Plaka: {plaka}, Okunma Sayisi: {plakalar[plaka]}")





while True:
    ret, frame = capture.read()
    ret, frame2 = capture2.read()
    cv2.imshow("kamera",frame2)
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    filter = cv2.bilateralFilter(gray, 7, 50, 50)

    edges = cv2.Canny(filter, 25, 75)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:100]

    for contour in contours:

        epsilon = 0.012 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:


            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            area = cv2.contourArea(contour)

            areatxt.write(str(area) + "\n")
            aspecttxt.write(str(aspect_ratio) + "\n")

            # Belirli boyut ve oran kriterlerine göre filtreleme yaptık
            if 1500 < area < 50000 and 2.8 <= aspect_ratio <= 5:

                roi = frame[y:y + h, x:x + w]


                # Plaka renk aralığı değerleri
                alt_hsv = np.array([0, 0, 100], dtype=np.uint8)  # Alt sınır HSV değeri
                ust_hsv = np.array([100, 100, 255], dtype=np.uint8)  # Üst sınır HSV değeri
                hsv_image = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                # Renk aralığına göre maske oluşturduk
                maske = cv2.inRange(hsv_image, alt_hsv, ust_hsv)
                # Maskeyi uygulayarak plaka bölgesini ayıkladık
                plaka_bolgesi = cv2.bitwise_and(roi, roi, mask=maske)
                gri_plaka = cv2.cvtColor(plaka_bolgesi, cv2.COLOR_BGR2GRAY)
                # Beyaz pixel sayısını hesapladık.
                beyaz_pixel_sayisi = cv2.countNonZero(gri_plaka)
                # Beyaz pixel sayısı bu değerden yüksekse arkaplan beyazdır dedik.
                threshold = 1000

                if beyaz_pixel_sayisi > threshold:

                    kernel = np.array([[-1, -1, -1],
                                       [-1, 9, -1],
                                       [-1, -1, -1]])

                    sharp_image = cv2.filter2D(roi, -1, kernel)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)


                    areatxt.write("Konum Bulundu: "+str(area)+"\n")

                    cv2.imwrite("./plates/normal.jpg", roi)
                    cv2.imwrite("./plates/sharp.jpg", sharp_image)

                    plaka_thread = threading.Thread(target=plakayiOku, args=(sharp_image, x, y, frame,))

                    plaka_thread.start()

                    #plaka_thread.join()

    frame = cv2.resize(frame, (800, 600))


    cv2.imshow("Video", frame)
    cv2.imshow("edges", edges)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        print(plakalar)
        break


areatxt.close()
aspecttxt.close()

capture.release()
cv2.destroyAllWindows()








"""
import cv2

carEnter = cv2.VideoCapture(0, cv2.CAP_DSHOW)
carExit = cv2.VideoCapture(1, cv2.CAP_DSHOW)


while True:
    enterRet, enterFrame = carEnter.read()
    exitRet, exitFrame = carExit.read()

    if not enterRet or not exitRet:
        break

    cv2.imshow("enter",enterFrame)
    cv2.imshow("exit",exitFrame)


    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
carEnter.release()
carExit.release()
"""