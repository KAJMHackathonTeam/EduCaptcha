from fer import FER
import matplotlib.pyplot as plt 
import face
import cv2
import time
import numpy as np
detector = FER(mtcnn=True)

#angry, disgust, fear, happy, sad, surprise, neutral

emotion_name = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']



def rolling(arr1, emotion):
    a1 = np.roll(arr1, -1)
    a1[-1] = emotion
    return a1
def createArr(length):
    arrMain = []
    for i in range(length):
        arrMain.append('')
    return np.array(arrMain)
def findFace(video):
    ret, frame = video.read()
    processed, _ = face.get_facebox_with_found(frame, True)
    detected = detector.detect_emotions(processed)
    return [processed, detected]
def findEmotion(detectedFaces, arr1):
    item = detected[0]
    emotion_val_dict = item['emotions']
    extracted_keys = list(emotion_val_dict.values())

    cut_list = extracted_keys.copy()
    cut_list[6] = 0
    
    
    
    
    if np.max(cut_list) >= 0.2: 
        #print(extracted_keys, np.argmax(cut_list), emotion_name[np.argmax(cut_list)] )
        detectedEmotion = emotion_name[np.argmax(cut_list)]
        arr1 = rolling(arr1, detectedEmotion)
        
    else:
        #print(extracted_keys, np.argmax(extracted_keys), emotion_name[np.argmax(extracted_keys)] )
        detectedEmotion = emotion_name[np.argmax(extracted_keys)]
        arr1 = rolling(arr1, detectedEmotion)
                   
    b = np.unique(arr1, return_counts=True)
    print(b[0][np.argmax(b[1])])
    return [b[0][np.argmax(b[1])], arr1]
if __name__ == '__main__':
    
    print ("THIS IS A TEST OF CV FACIAL EMOTION DETECTION")

    video = cv2.VideoCapture(0)
    print("camera done init")
    
    arrMain = createArr(5)

    
    while(True):

        processed, detected = findFace(video)

        if len(detected) > 0: # if there's actually stuff

            emotion, arrMain = findEmotion(detected, arrMain)
            print(emotion)

        else:
            print("no face detected")

        cv2.imshow('frame', processed)

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)

    # When everything done, release the capture
    video.release()
    cv2.destroyAllWindows()
