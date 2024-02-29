import cv2
import pytesseract
from PIL import ImageGrab
import numpy as np
import tkinter as tk

root = tk.Tk()
root.title("GUI")

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Stephen Wong\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

image = cv2.imread('numbers.png')

# Add Binarization (Thresholding), Noise Removal, Dilation and Erosion, Deskewing from openCV
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# text = pytesseract.image_to_string(gray)
# print(text)

text = pytesseract.image_to_string(image, config="--psm 6")
print(text)

# Screenshot
# screenshot = ImageGrab.grab()
# screenshot.save("screenshot.png")
# screenshot.close()

# Record mouse coordinates
win = tk.Toplevel()
def area_sel():

    x1, x2, y1, y2 = 0

    def on_mouse_down(event):
        x1, y1 = event.x, event.y
    def on_mouse_release(event):
        x2, y2 = event.x, event.y

    win.bind('<ButtonPress-1>', on_mouse_down)
    win.bind('<ButtonRelease-1>', on_mouse_release)

btn = tk.Button(root, text='select area', width=20, command=area_sel).pack()
root.mainloop()