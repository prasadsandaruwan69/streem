import cv2
from flask import Flask, Response
import time

app = Flask(_name_)

def get_camera():
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('U','Y','V','Y'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    time.sleep(2)
    return cap

def generate_frames():
    cap = get_camera()
    while True:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            cap = get_camera()
            continue
        # Convert UYVY to BGR first
        frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_UYVY)
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame_bytes + b'\r\n')

@app.route('/cam/1')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=9000, debug=False)
