# Air Drawing Application

A real-time air drawing application that uses hand tracking to allow users to draw on a virtual canvas using their index finger.

## Technologies

- Python
- OpenCV
- MediaPipe
- NumPy

## Features

- Real-time hand tracking through a webcam
- Draw using index finger movements
- Change drawing colors using hand gestures
- Clear the canvas using an open-hand gesture

## How It Works

The application uses MediaPipe to detect hand landmarks from the webcam. The position of the index fingertip is tracked and converted into coordinates on a virtual canvas.

Different hand gestures are used to control the application. Holding up the index finger allows the user to draw, while additional gestures allow the user to change colors or clear the canvas.

## How to Run

1. Install Python 3.
2. Install the required libraries:

```bash
pip install opencv-python mediapipe numpy
