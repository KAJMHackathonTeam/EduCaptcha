import pyvirtualcam
import numpy as np
import cv2
from PIL import Image

video = cv2.VideoCapture(0)

inputShape = video.read()[1].shape
camHeight = inputShape[0]
camWidth = inputShape[1]

with pyvirtualcam.Camera(height=camHeight, width=camWidth, fps=30, backend = 'obs') as cam:
    print(f'Using virtual camera: {cam.device}')
    frame = np.zeros((cam.height, cam.width, 3), np.uint8)  # RGB
    while True:
        active, frame = video.read()
        if not active:
            raise RuntimeError('Error fetching frame')

        RGBframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #Backend

        cam.send(RGBframe)
        cam.sleep_until_next_frame()