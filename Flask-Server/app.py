from flask import Flask, render_template

app = Flask(__name__)
camera_status = "On"

@app.route('/')
def home():
    return render_template("index.html", status=camera_status);

@app.route('/on')
def on():
    if ()
    return render_template('index.html', status=camera_status)
if __name__ == '__main__':
    app.run(debug=True)