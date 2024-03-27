import os
import cv2
import pytesseract
from PIL import Image, ImageGrab, ImageTk, ImageEnhance
import numpy as np
import tkinter as tk

root = tk.Tk()  # initialize tkinter framework
root.title("GUI")
root.resizable(0, 0)  # disable resizing

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Stephen Wong\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
list_of_ascii = [43, 45, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 61, 78]
image_width = 0
image_height = 0


# TODO(optional?): Implement other math operations for more versatility; Refine return statements
def check_input(input_text):
    acceptable_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    text_list = list(input_text)

    for value in text_list:
        if 32 > ord(value) > 57 and ord(value) != 61:
            print("ERROR: NOT ALL VALUES IN ASCII RANGE")
            return "bad"

    if all([c in acceptable_chars for c in text_list[:-1]]):
        print("ERROR: ALL VALUES ARE NUMBERS")
        return "bad"

    return "good"


# TODO: check ASCII value of characters to determine what math equation to use
def calculate(input_text):
    input_list = list(input_text)
    result = 0
    for i in range(len(input_list)):
        if ord(input_list[i]) == 43:
            result += (int(input_list[i-1]) + int(input_list[i+1]))
        if ord(input_list[i]) == 45:
            result += (int(input_list[i-1]) - int(input_list[i + 1]))
        if ord(input_list[i]) == 78 or ord(input_list[i]) == 42:
            result += (int(input_list[i-1]) * int(input_list[i + 1]))
        if ord(input_list[i]) == 47:
            result += (int(input_list[i-1]) / int(input_list[i + 1]))
    return result


# TODO: vary scale size depending on size of snipped image
def process(input_image, matrix):
    resized_image = cv2.resize(input_image, (image_width * 2, image_height * 2))
    # , interpolation=cv2.INTER_AREA

    # Grayscale
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Dilation + Erosion
    kernel = np.ones(matrix, np.uint8)  # Kernel Matrix
    dilate = cv2.dilate(gray, kernel, iterations=1)
    dilate_erode = cv2.erode(dilate, kernel, iterations=2)

    # Threshold
    thresh = cv2.threshold(dilate_erode, 127, 255, cv2.THRESH_BINARY)[1]
    # invert = cv2.bitwise_not(gray)

    join = np.concatenate((gray, dilate, dilate_erode, thresh), axis=1)
    cv2.imshow('gray - dilate - dilate+erode - thresh', join)

    cv2.imshow('resized_image', resized_image)

    return thresh


def main_func(image):
    read_image = cv2.imread(image)
    process_image = process(read_image, (2, 3))
    text = pytesseract.image_to_string(process_image, config="--psm 7")
    if len(text) < 3:
        print("Try 2")
        process_image = process(read_image, (1, 3))
    if len(text) < 3:
        print("Try 3")
        process_image = process(read_image, (4, 3))
    if len(text) < 3:
        print("Error processing text")

    if check_input(text) == "bad":
        return "The text contains invalid characters"
    else:
        print("ANSWER: ", calculate(text))
    print("READ TEXT: ", list(text))


def show_image(image):
    win = tk.Toplevel()
    win.image = ImageTk.PhotoImage(image)
    tk.Label(win, image=win.image).pack()
    win.grab_set()
    # win.wait_window(win)  # leave window open and wait for window to be destroyed/closed
    print(image_width, image_height)
    image.save("images/sample.png")

    main_func("images/sample.png")
    os.remove("images/sample.png")

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
        global image_width, image_height
        x2, y2 = event.x, event.y
        print('{}, {}'.format(x2, y2))
        image_width = x2 - x1
        image_height = y2 - y1
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


cv2.waitKey()
btn = tk.Button(root, text='select area', width=30, command=area_sel).pack()  # select area GUI button
root.mainloop()
