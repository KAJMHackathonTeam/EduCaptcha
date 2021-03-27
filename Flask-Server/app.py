from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
camera_status = "On"
webcam = cv2.VideoCapture(0)

def gen_frames():  
    while True:
        success, frame = webcam.read() 
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

@app.route('/')
def home():
    return render_template("index.html", status=camera_status)

@app.route('/toggle')
def toggle():
    if (camera_status == "On"):
        camera_status = "Off"
    else:
        camera_status = "On"

    # Add trigger here          
    return render_template('index.html', status=camera_status)

@app.route('/preview') 
def preview():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()