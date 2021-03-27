from flask import Flask, render_template, Response, url_for 
import cv2
from camera import main
app = Flask(__name__)
camera_status = "On"
webcam = cv2.VideoCapture(0)

@app.route('/')
def home():
    return render_template("index.html", status=camera_status)

@app.route('/toggle')
def toggle():
    if (camera_status == "On"):
        camera_status = "Off"
        main(False)
    else:
        camera_status = "On"
        main(True)

    # Add trigger here          
    return render_template(url_for('index'), status=camera_status)

if __name__ == '__main__':
    app.run()