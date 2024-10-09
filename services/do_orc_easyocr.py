import cv2 as cv
import easyocr

def do_ocr_easyocr (image) :
    img = cv.cvtColor(image, cv.IMREAD_GRAYSCALE)
    _, result = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    reader = easyocr.Reader(['id', 'en'], gpu=True)
    text_ = reader.readtext(img)
    
    return text_