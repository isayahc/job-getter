"""
Lil Snippy: An OCR-based GUI application for capturing screen snippets and extracting text from them.
"""

from tkinter import Tk, Frame, Button, Text, Toplevel, Canvas, BOTH, YES, INSERT, END
import pyautogui
import datetime
from paddleocr import PaddleOCR
import numpy as np
import threading
import os
from typing import Optional


ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Initialize OCR engine


def take_bounded_screenshot(x1: int, y1: int, x2: int, y2: int, app: 'Application') -> None:
    """
    Takes a screenshot of the region defined by the given coordinates.
    Performs OCR on the screenshot and displays the recognized text in the application.

    :param x1: The x-coordinate of one corner of the region.
    :param y1: The y-coordinate of one corner of the region.
    :param x2: The x-coordinate of the opposite corner of the region.
    :param y2: The y-coordinate of the opposite corner of the region.
    :param app: The Application instance for displaying recognized text.
    """
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    image = pyautogui.screenshot(region=(x1, y1, width, height))  # Take screenshot of defined region
    file_name = datetime.datetime.now().strftime("%f")  # Use microseconds for unique file names
    directory = "snips/"
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
    image.save(os.path.join(directory, file_name + ".png"))  # Save the image
    image_np = np.array(image)
    text = ocr.ocr(image_np, cls=True)  # Perform OCR on the image
    complete_text = [i[1][0] for i in text[0]]  # Extract the recognized text
    complete_text = "\n".join(complete_text)
    app.display_text(complete_text)  # Display the recognized text in the application


class Application:
    """
    Defines the main GUI application for capturing screen snippets and performing OCR on them.
    """

    def __init__(self, master: Tk):
        self.snip_surface: Optional[Canvas] = None
        self.master: Tk = master
        self.start_x: Optional[int] = None
        self.start_y: Optional[int] = None
        self.current_x: Optional[int] = None
        self.current_y: Optional[int] = None

        root.geometry('800x600')  # set new geometry
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

    def create_screen_canvas(self) -> None:
        """
        Creates the canvas for capturing screen snippets.
        """
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

    def on_button_release(self, event) -> None:
        """
        Callback for when the button is released.
        """
        self.display_rectangle_position()

        left = min(self.start_x, self.current_x)
        upper = min(self.start_y, self.current_y)
        right = max(self.start_x, self.current_x)
        lower = max(self.start_y, self.current_y)

        screenshot_thread = threading.Thread(target=take_bounded_screenshot, args=(left, upper, right, lower, self))
        screenshot_thread.start()

        self.exit_screenshot_mode()
        return event

    def exit_screenshot_mode(self) -> None:
        """
        Exits screenshot mode, destroying the screenshot canvas and bringing back the main window.
        """
        self.snip_surface.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def on_button_press(self, event) -> None:
        """
        Callback for when the button is pressed.
        """
        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(0, 0, 1, 1, outline='red', width=3, fill="maroon3")

    def on_snip_drag(self, event) -> None:
        """
        Callback for when the mouse is dragged.
        """
        self.current_x, self.current_y = (event.x, event.y)
        self.snip_surface.coords(1, self.start_x, self.start_y, self.current_x, self.current_y)

    def display_rectangle_position(self) -> None:
        """
        Prints the coordinates of the current rectangle.
        """
        print(self.start_x)
        print(self.start_y)
        print(self.current_x)
        print(self.current_y)

    def display_text(self, text: str) -> None:
        """
        Displays the given text in the application.
        """
        self.display.delete("1.0", END)
        self.display.insert(INSERT, text)


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()
