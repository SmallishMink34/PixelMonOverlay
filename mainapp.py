import time

import cv2
import mss
import numpy
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\\tesseract'
def get_pk():
    mon = {'top': 0, 'left': 172, 'width': 170, 'height': 75}
    counter = 0
    with mss.mss() as sct:
        while counter < 1:
            im = numpy.asarray(sct.grab(mon))
            # im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

            text = pytesseract.image_to_string(im)
            return text

            cv2.imshow('Image', im)

            # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            # One screenshot per second
            time.sleep(1)
            counter += 1
            