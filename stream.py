from flask import Flask, render_template, Response, request, jsonify
import cv2
import threading
import time

app = Flask(__name__)

camera = cv2.VideoCapture(0)
streaming = False
lock = threading.Lock()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def gen_frames():
    global streaming
    while True:
        with lock:
            if not streaming:
                time.sleep(0.1)
                continue

        success, frame = camera.read()
        if not success:
            break

        # Rotate 180 degrees
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        # Mirror horizontally (flip on X axis)
        frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control_stream', methods=['POST'])
def control_stream():
    global streaming
    data = request.get_json()
    cmd = data.get('command')
    with lock:
        if cmd == 'start':
            streaming = True
        elif cmd == 'stop':
            streaming = False
    return jsonify(status='ok', streaming=streaming)

if __name__ == '__main__':
    streaming = False
    app.run(host='0.0.0.0', port=5000, debug=False)


