# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 20:50:03 2021

@author: Aditya
"""

from fer import FER
import matplotlib.pyplot as plt 
from . import face
import cv2
import time
import numpy as np

detector = FER(mtcnn=True)

#angry, disgust, fear, happy, sad, surprise, neutral

def rolling(arr1, emotion):
    a1 = np.roll(arr1, -1)
    a1[-1] = emotion
    return a1
def createArr(length):
    arrMain = []
    for i in range(length):
        arrMain.append('fjfjfjfjf')
    return np.array(arrMain)

emotion_name = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
arrMain = createArr(5)



def findFace(frame):
    
    processed, _ = face.get_facebox_with_found(frame, True)
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

def main(frame):
    processed, detected = findFace(frame)
    if len(detected) > 0:
        emotion = findEmotion(detected)
        print(emotion)
    
    cv2.imshow('frame', processed)

    



if __name__ == '__main__':
    
    #print ("THIS IS A TEST OF CV FACIAL EMOTION DETECTION")

    video = cv2.VideoCapture(0)
    #print("camera done init")
    


    
    while(True):
        ret, frame = video.read()
        main(frame)

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)

    # When everything done, release the capture
    video.release()
    cv2.destroyAllWindows()

    