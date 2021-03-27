import pyvirtualcam
import numpy as np
import cv2
from PIL import Image
from urllib.request import urlopen

video = cv2.VideoCapture(0)

inputShape = video.read()[1].shape
camHeight = inputShape[0]
camWidth = inputShape[1]


def getEmotions():
    #ML results
    return()

def writeEmotions(result):
    emojiDict = {"peace": ":simple_smile:", "affection":":heart_eyes:", "esteem":"", "anticipation":"", "engagement":"", "confidence":"", "happiness":"", "pleasure":"", "excitement":"", "surprise":"", "sympathy":"", "confusion":"", "disconnection":"", "fatigue":"", "embarrassment":"" ,"yearning":"" ,"disapproval":"" ,"aversion":"", "annoyance":"", "anger":"", "sensitivity":"", "sadness":"", "disquietment":"", "fear":"", "pain":"", "suffering":""}
    return emojiDict.get(result)



with pyvirtualcam.Camera(height=camHeight, width=camWidth, fps=30, backend = 'obs') as cam:
    print(f'Using virtual camera: {cam.device}')
    while True:
        active, frame = video.read()
        if not active:
            raise RuntimeError('Error fetching frame')

        RGBframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)



        emojiFrame = Image.new('RGB', (camWidth, camHeight), color = 'black')
        
        emojiOverlay = Image.open(urlopen('https://newevolutiondesigns.com/images/freebies/colorful-background-14.jpg'))
        
        width, height= emojiOverlay.size
        scale = (camHeight * 0.75) / height
        emojiOverlay = emojiOverlay.resize((int(width * scale), int(height * scale)))
        offset = ((camWidth - int(width * scale)) // 2, (camHeight - int(height * scale)) // 2)
        emojiFrame.paste(emojiOverlay, offset)
        emojiFrame = np.array(emojiFrame)
        
        cam.send(emojiFrame)
        cam.sleep_until_next_frame()


