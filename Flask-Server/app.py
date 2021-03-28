from flask import Flask, render_template, Response, url_for 
import pyvirtualcam
from PIL import Image
import os


from fer import FER
import matplotlib.pyplot as plt 

import cv2
import time
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')





def _get_best_face(faces):
    """
    determines the largest face box. That becomes the face we return.

    Parameters:
        face: a list of (x,y,w,h)

    Return: 
        (x,y,w,h) of largest/closest
    """
    def comp(face):
        """
        sort function
        """
        (x,y,w,h) = face

        return w * h

    list_faces = list(faces)


    list_faces.sort(key=comp, reverse=True)

    return list_faces[0]


def get_facebox_with_found(frame, isReturnColor=True):
    """
    detects faces from the input frame. If there are mutliple faces, the code will pick the face with the largest size.

    Parameters:
        frame: video frame from open cv. No processing needed (numpy)
        isReturnColor: boolean on whether to return color numpy array or greyscale numpy array (default=True (color))
    
    Return:
        numpy array of face. If no face is found, it will return the entire frame in a numpy array
        boolean of if a face is found. (True == face found)

    """

    #detect
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    #if there are no faces, we can save a lot of time
    if len(faces) == 0:
        return frame if isReturnColor else gray, False
    else:
        #determine
        best_face = _get_best_face(faces)

        #unpack
        (x,y,w,h) = best_face

        #determine which image to return (color/no color)
        ret_img = frame if isReturnColor else gray

        ret_crop_img = ret_img[y:y+h, x:x+w]

        return ret_crop_img, True


def get_facebox_without_found(frame, isReturnColor=True):
    """
    detects faces from the input frame. If there are mutliple faces, the code will pick the face with the largest size.

    Parameters:
        frame: video frame from open cv. No processing needed (numpy)
        isReturnColor: boolean on whether to return color numpy array or greyscale numpy array (default=True (color))
    
    Return:
        numpy array of face. If no face is found, it will return the entire frame in a numpy array
    """

    res, isFound = get_facebox_with_found(frame, isReturnColor)

    return res

detector = FER(mtcnn=True)

#angry, disgust, fear, happy, sad, surprise, neutral

def rolling(arr1, emotion):
    a1 = np.roll(arr1, -1)
    a1[-1] = emotion
    return a1
def createArr(length):
    arrMain = []
    for i in range(length):
        arrMain.append('fjfjfjfjfjfj')
    return np.array(arrMain)

emotion_name = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
arrMain = createArr(5)



def findFace(frame):
    
    processed, _ = get_facebox_with_found(frame, True)
    detected = detector.detect_emotions(processed)
    return [processed, detected]
def findEmotion(detectedFaces):
    global arrMain
    item = detectedFaces[0]
    emotion_val_dict = item['emotions']
    extracted_keys = list(emotion_val_dict.values())

    cut_list = extracted_keys.copy()
    cut_list[6] = 0
    
    
    
    
    if np.max(cut_list) >= 0.2: 
        #print(extracted_keys, np.argmax(cut_list), emotion_name[np.argmax(cut_list)] )
        detectedEmotion = emotion_name[np.argmax(cut_list)]
        arrMain = rolling(arrMain, detectedEmotion)
        
    else:
        #print(extracted_keys, np.argmax(extracted_keys), emotion_name[np.argmax(extracted_keys)] )
        detectedEmotion = emotion_name[np.argmax(extracted_keys)]
        arrMain = rolling(arrMain, detectedEmotion)
                   
    b = np.unique(arrMain, return_counts=True)

    return b[0][np.argmax(b[1])]

app = Flask(__name__)
camera_status = "On"
webcam = cv2.VideoCapture(0)

@app.route('/')
def index():
    camera(True)
    return render_template("index.html", status=camera_status)

def getEmotions(frame):
    processed, detected = findFace(frame)
    if len(detected) > 0:
        emotion = findEmotion(detected)
        if emotion == "fjfjfjfjfjfj":
            emotion = 'neutral'
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

            RGBframe_new = cv2.resize(RGBframe,(camWidth // 4, camHeight // 4))
            RGBframe_new = Image.fromarray(RGBframe_new)
            print(RGBframe_new)

            offset = ((camWidth - int(width )) // 2, (camHeight - int(height)) // 2)
            emojiFrame.paste(emojiOverlay, offset)

            offset = (0, 0)
            emojiFrame.paste(RGBframe_new, offset)
            emojiFrame = np.array(emojiFrame)
            
            cam.send(emojiFrame)
            cam.sleep_until_next_frame()


    
if __name__ == '__main__':
    camera(True)