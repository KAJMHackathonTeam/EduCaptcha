from flask import Flask, render_template, Response, url_for 
import cv2
import pyvirtualcam
import numpy as np
import cv2
from PIL import Image
import os
from . import EmotionDetection as emotions

app = Flask(__name__)
camera_status = "On"
webcam = cv2.VideoCapture(0)

@app.route('/')
def index():
    camera(True)
    return render_template("index.html", status=camera_status)

def getEmotions(frame):
    processed, detected = emotions.findFace(frame)
    if len(detected) > 0:
        emotion = emotions.findEmotion(detected)
        return emotion
    return "neutral"

def writeEmotions(result):
    
    script_dir = os.path.dirname(__file__)
    rel_path = f"assets/{result}.png"
    output = os.path.join(script_dir, rel_path)
    return output

def alpha_to_color(image, color=(255, 255, 255)):
    x = np.array(image)
    r, g, b, a = np.rollaxis(x, axis=-1)
    r[a == 0] = color[0]
    g[a == 0] = color[1]
    b[a == 0] = color[2] 
    x = np.dstack([r, g, b, a])
    return Image.fromarray(x, 'RGBA')


def camera(toggle):
    video = cv2.VideoCapture(0)
    inputShape = video.read()[1].shape
    camHeight = inputShape[0]
    camWidth = inputShape[1]

    with pyvirtualcam.Camera(height=camHeight, width=camWidth, fps=30, backend = 'obs') as cam:
        print(f'Using virtual camera: {cam.device}')
        while toggle == True:
            ret, frame = video.read()
            if not ret:
                raise RuntimeError('Error fetching frame')
            
            RGBframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            emojiFrame = Image.new('RGB', (camWidth, camHeight), color = 'black')
            
            emojiOverlay = alpha_to_color(Image.open(writeEmotions(getEmotions(RGBframe))))
            width, height= emojiOverlay.size
    
            offset = ((camWidth - int(width )) // 2, (camHeight - int(height)) // 2)
            emojiFrame.paste(emojiOverlay, offset)
            emojiFrame = np.array(emojiFrame)
            
            cam.send(emojiFrame)
            cam.sleep_until_next_frame()


if __name__ == '__main__':
    app.run()