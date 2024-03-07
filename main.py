import os
import cv2
import pytesseract
from PIL import Image, ImageGrab, ImageTk, ImageEnhance
import numpy as np
import tkinter as tk

'''
root = tk.Tk()  # initialize tkinter framework
root.title("GUI")
root.resizable(0, 0)  # disable resizing
'''

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Stephen Wong\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# # Add Binarization (Thresholding), Noise Removal, Dilation and Erosion, Deskewing from openCV
# # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # text = pytesseract.image_to_string(gray)
# # print(text)
#


def calculate(text):
    x = text.split("+")
    print(x)
    return sum([int(i) for i in x])

alpha = 1.5 # Contrast control
beta = 10 # Brightness control


image = cv2.imread("messy.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#img_smooth = cv2.GaussianBlur(gray, (13,13), 0)
con = cv2.convertScaleAbs(gray, alpha = alpha, beta = beta)

invert = cv2.bitwise_not(gray)

text = pytesseract.image_to_string(image, config="--psm 7, -l eng+equ")
print(text)

#(calculate(text))

cv2.imshow('gray', gray)
cv2.imshow('invert', invert)
cv2.imshow('con', con)

cv2.waitKey()

'''
def show_image(image):
    win = tk.Toplevel()
    win.image = ImageTk.PhotoImage(image)
    tk.Label(win, image=win.image).pack()
    win.grab_set()
    # win.wait_window(win)  # leave window open and wait for window to be destroyed/closed

    image = image.save("sample.png")
    read_image = cv2.imread("sample.png")
    text = pytesseract.image_to_string(read_image, config="--psm 6")
    print(text)
    os.remove("sample.png")
    win.destroy()


# Record mouse coordinates

def area_sel():

    x1 = x2 = y1 = y2 = 0
    roi_image = None

    def on_mouse_down(event):
        nonlocal x1, y1
        x1, y1 = event.x, event.y
        canvas.create_rectangle(x1, y1, x1, y1, outline='red', tag='roi')
        print('{}, {}'.format(x1, y1))

    def on_mouse_move(event):
        nonlocal roi_image, x2, y2
        x2, y2 = event.x, event.y
        canvas.delete('roi-image')  # remove old selected image
        roi_image = image.crop((x1, y1, x2, y2))  # get the image of selected region
        canvas.image = ImageTk.PhotoImage(roi_image)
        canvas.create_image(x1, y1, image=canvas.image, tag=('roi-image'), anchor='nw')
        canvas.coords('roi', x1, y1, x2, y2)
        canvas.lift('roi')  # places select rectangle on top of overlay image

    def on_mouse_release(event):
            x2, y2 = event.x, event.y
            print('{}, {}'.format(x2, y2))
            win.destroy()

    root.withdraw()  # hide GUI
    image = ImageGrab.grab()  # grab current screen

    bgimage = ImageEnhance.Brightness(image).enhance(0.3)  # darken background

    win = tk.Toplevel()  # initializes instance of tkinter window
    win.attributes('-fullscreen', 1)  # GUI window size
    win.attributes('-topmost', 1)

    canvas = tk.Canvas(win, highlightthickness=0)  # set canvas to be drawn on
    canvas.pack(fill='both', expand=1)
    tkimage = ImageTk.PhotoImage(bgimage)
    canvas.create_image(0, 0, image=tkimage, anchor='nw', tag='images')

    win.bind('<ButtonPress-1>', on_mouse_down)
    win.bind('<B1-Motion>', on_mouse_move)
    win.bind('<ButtonRelease-1>', on_mouse_release)
    win.bind('<Escape>', lambda e: win.destroy())

    win.focus_force()
    win.grab_set()
    win.wait_window(win)
    root.deiconify()

    # show selected region as an image if an area was selected
    if roi_image:
        show_image(roi_image)


btn = tk.Button(root, text='select area', width=30, command=area_sel).pack()  # select area GUI button
root.mainloop()
'''