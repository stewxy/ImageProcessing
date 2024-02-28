import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Stephen Wong\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

image = cv2.imread('numbers.png')

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# text = pytesseract.image_to_string(gray)
# print(text)
# Add binarization, noise removal etc

text = pytesseract.image_to_string(image, config="--psm 6")
print(text)

