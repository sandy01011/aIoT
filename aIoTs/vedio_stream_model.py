from flask import Flask, render_template, Response
import cv2
import tensorflow as tf
app = Flask(__name__)

#camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')  # use 0 for web camera
#  for cctv camera use rtsp://admin:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)
camera = cv2.VideoCapture('rtsp://admin:123456@192.168.0.105:554/user=admin_password=123456_channel=channel_number_stream=0.sdp')

face_detection = cv2.CascadeClassifier('haar_cascade_face_detection.xml')

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
settings = {
    'scaleFactor': 1.3, 
    'minNeighbors': 5, 
    'minSize': (50, 50)
}

labels = ["Neutral","Happy","Sad","Surprise","Angry"]

model = tf.keras.models.load_model('expression.model')



def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def gen_frames_1():
    print('--->>>>>>>>>>------------------------->>>>--------------------------------------------------------------------->>>>>>---------------------------------------------------------->>>>>detected')
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, img = camera.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            detected = face_detection.detectMultiScale(gray, **settings)
            ret, img = camera.read()
            detected = face_detection.detectMultiScale(gray, **settings)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            for x, y, w, h in detected:
                cv2.rectangle(img, (x, y), (x+w, y+h), (245, 135, 66), 2)
                cv2.rectangle(img, (x, y), (x+w//3, y+20), (245, 135, 66), -1)
                face = gray[y+5:y+h-5, x+20:x+w-20]
                face = cv2.resize(face, (48,48))
                face = face/255.0
                predictions = model.predict(np.array([face.reshape((48,48,1))])).argmax()
                state = labels[predictions]
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img,state,(x+10,y+15), font, 0.5, (255,255,255), 2, cv2.LINE_AA)
            #cv2.imshow('Facial Expression', img)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imshow('Facial Expression', img) + b'\r\n')  # concat frame one by one and show result
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            print('---------------------------->>>>--------------------------------------------------------------------->>>>>>---------------------------------------------------------->>>>>detected')
            #yield (b'--frame\r\n'
            #       b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  # concat frame one by one and show result
"""
            a
            a
            a
            a
        ret, img = camera.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detected = face_detection.detectMultiScale(gray, **settings)
        for x, y, w, h in detected:
            cv2.rectangle(img, (x, y), (x+w, y+h), (245, 135, 66), 2)
            cv2.rectangle(img, (x, y), (x+w//3, y+20), (245, 135, 66), -1)
            face = gray[y+5:y+h-5, x+20:x+w-20]
            face = cv2.resize(face, (48,48))
            face = face/255.0
            predictions = model.predict(np.array([face.reshape((48,48,1))])).argmax()
            state = labels[predictions]
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img,state,(x+10,y+15), font, 0.5, (255,255,255), 2, cv2.LINE_AA)
        #cv2.imshow('Facial Expression', img)
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imshow('Facial Expression', img) + b'\r\n')  # concat frame one by one and show result
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # writer.writeFrame(img)
        if cv2.waitKey(5) != -1:
            break
"""

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames_1(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3381, debug=True)
    #app.run(debug=True)