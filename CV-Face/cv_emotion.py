from fer import FER
import matplotlib.pyplot as plt 
import face
import cv2
import time
import numpy as np
detector = FER(mtcnn=True)

#angry, disgust, fear, happy, sad, surprise, neutral

emotion_name = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

#only set if the array of 5 is the same
previous_5 = ['neutral', 'neutral', 'neutral', 'neutral', 'neutral']

if __name__ == '__main__':
    
    print ("THIS IS A TEST OF CV FACIAL EMOTION DETECTION")

    video = cv2.VideoCapture(0)
    print("camera done init")
    
    
    while(True):
        # Capture frame-by-frame
        ret, frame = video.read()

        processed, _ = face.get_facebox_with_found(frame, True)


        detected = detector.detect_emotions(processed)

        if len(detected) > 0: # if there's actually stuff

            item = detected[0]
            emotion_val_dict = item['emotions']
            extracted_keys = list(emotion_val_dict.values())

            cut_list = extracted_keys.copy()
            cut_list[6] = 0

            if np.max(cut_list) >= 0.2: 
                print(extracted_keys, np.argmax(cut_list), emotion_name[np.argmax(cut_list)] )
            else:
                print(extracted_keys, np.argmax(extracted_keys), emotion_name[np.argmax(extracted_keys)] )
                           



        else:
            print("no face detected")

        cv2.imshow('frame', processed)

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)

    # When everything done, release the capture
    video.release()
    cv2.destroyAllWindows()

