from tkinter import *
import pyautogui
import datetime
from paddleocr import PaddleOCR
import numpy as np
import threading
import os
import json

ocr = PaddleOCR(use_angle_cls=True, lang='en')


with open('config.ini') as f:
    config = json.load(f)
    
directory = config['screenshot_directory']



def take_bounded_screenshot(x1, y1, x2, y2, app):
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    image = pyautogui.screenshot(region=(x1, y1, width, height))
    file_name = datetime.datetime.now().strftime("%f")
    directory = "snips/"
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
    image.save(os.path.join(directory, file_name + ".png"))
    image_np = np.array(image)
    text = ocr.ocr(image_np, cls=True)
    complete_text = [i[1][0] for i in text[0]]
    complete_text = "\n".join(complete_text)
    app.display_text(complete_text)


class Application():
    def __init__(self, master):
        self.snip_surface = None
        self.master = master
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None

        root.geometry('400x50+200+200')  # set new geometry
        root.title('Lil Snippy')

        self.menu_frame = Frame(master)
        self.menu_frame.pack(fill=BOTH, expand=YES, padx=1, pady=1)

        self.buttonBar = Frame(self.menu_frame, bg="")
        self.buttonBar.pack()

        self.snipButton = Button(self.buttonBar, width=5, height=5, command=self.create_screen_canvas, background="green")
        self.snipButton.pack()

        self.display = Text(self.buttonBar, height=10, width=30)
        self.display.pack()

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = Frame(self.master_screen, background="maroon3")
        self.picture_frame.pack(fill=BOTH, expand=YES)

    def create_screen_canvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.snip_surface = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.snip_surface.pack(fill=BOTH, expand=YES)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        self.display_rectangle_position()

        left = min(self.start_x, self.current_x)
        upper = min(self.start_y, self.current_y)
        right = max(self.start_x, self.current_x)
        lower = max(self.start_y, self.current_y)

        screenshot_thread = threading.Thread(target=take_bounded_screenshot, args=(left, upper, right, lower, self))
        screenshot_thread.start()

        self.exit_screenshot_mode()
        return event

    def exit_screenshot_mode(self):
        self.snip_surface.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def on_button_press(self, event):
        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(0, 0, 1, 1, outline='red', width=3, fill="maroon3")

    def on_snip_drag(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        self.snip_surface.coords(1, self.start_x, self.start_y, self.current_x, self.current_y)

    def display_rectangle_position(self):
        print(self.start_x)
        print(self.start_y)
        print(self.current_x)
        print(self.current_y)

    def display_text(self, text):
        self.display.delete("1.0", END)
        self.display.insert(INSERT, text)

if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()
