import cv2
import numpy as np
import os

import time

#TODO: Ask aditya about resizing once he finishes it.

'''
What do I need to do in this file?

This is an open cv script that will detect and extract faces from a frame

It will return a numpy array containing the pixel data for the face. It will not resize. The other files will do so.
'''

### ----------- init classifier
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





#if this file is run as main. 
#contains proof of concept logic
if __name__ == '__main__':

    print ("THIS IS A TEST OF FACIAL DETECTION")

    video = cv2.VideoCapture(0)
    print("camera done init")
    
    
    while(True):
        # Capture frame-by-frame
        ret, frame = video.read()

        processed, _ = get_facebox_with_found(frame, True)

        print(_)
        cv2.imshow('frame', processed)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(1)

    # When everything done, release the capture
    video.release()
    cv2.destroyAllWindows()


    

        

