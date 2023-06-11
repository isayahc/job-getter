# Lil Snippy

Lil Snippy is an OCR-based GUI application for capturing screen snippets and extracting text from them. It uses Python's Tkinter library to create the GUI, PyAutoGUI for taking screenshots, and PaddleOCR for Optical Character Recognition.

## How to Run

To run the application, navigate to the project's root directory and run the command:

```bash
python3 snipping_tool.py
```

Make sure that you have all the dependencies installed. You can install them with:

```bash
pip install -r requirements.txt
```

## Installing PaddlePaddle

If you want to use PaddlePaddle in this project, you can add the following lines to your requirements.txt file:

```bash
paddlepaddle-gpu  # for GPU version
paddlepaddle # for CPU version
```

You can choose between the GPU and CPU versions of PaddlePaddle depending on your hardware configuration.

If you have any questions about installing PaddlePaddle, feel free to reach out to me.

Here are the pip commands you can use to install PaddlePaddle:

```bash
# For GPU version
python -m pip install paddlepaddle-gpu -f https://mirror.baidu.com/pypi/simple

# For CPU version
python -m pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
```

## How to Use

When the application starts, a window titled 'Lil Snippy' appears. To begin taking a screen snippet, press the green button in the window. This will minimize the main window and allow you to select an area on the screen by clicking and dragging your mouse. Once you release the mouse button, the application takes a screenshot of the selected area and uses OCR to recognize any text in it. The recognized text is then displayed in the application's main window.

## Dependencies

* Python 3.6+
* Tkinter
* PyAutoGUI
* PaddleOCR
* NumPy

## Structure

The application's code is divided into a main class `Application`, which is responsible for the GUI interface, and a function `take_bounded_screenshot`, which handles the screenshot and OCR part.

The `Application` class initializes the Tkinter GUI and binds the relevant mouse events. It has methods for creating the screenshot canvas, handling button presses, drags and releases, exiting screenshot mode, and displaying the recognized text.

The `take_bounded_screenshot` function takes in the coordinates of the screen area to capture and an instance of the `Application` class. It captures a screenshot of the specified area, performs OCR on it, and uses the `Application` instance to display the recognized text.

## Disclaimer

This project is intended for educational purposes and personal use. Please ensure any use of this code complies with your local laws and regulations related to screen capturing.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)