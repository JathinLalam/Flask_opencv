from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    Response
)
import numpy as np
import cv2
import sys
import json,time
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Jathin', password='password'))
users.append(User(id=2, username='Shreyansh', password='password'))
users.append(User(id=3, username='Sourav Tambe', password='password'))
users.append(User(id=4, username='Prateek', password='password'))

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return render_template('index.html')
        else:
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')

# @app.route('/verify', methods=['GET', 'POST'])
# def verify():
#     cascPath = './Cascade/data/haarcascade_frontalface_alt2.xml'
#     faceCascade = cv2.CascadeClassifier(cascPath)

#     video_capture = cv2.VideoCapture(0)
#     x = 0
#     w = 0

#     while True:
#         # Capture frame-by-frame
#         ret, frame = video_capture.read()

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         faces = faceCascade.detectMultiScale(
#             gray,
#             scaleFactor=1.1,
#             minNeighbors=5,
#             minSize=(30, 30),
#             # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
#         )

#         # Draw a rectangle around the faces
#         for (x, y, w, h) in faces:
#             #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#             cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)
#         # Display the resulting frame
#         #cv2.imshow('Video', frame)
#         cv2.imshow('frame1',gray)
       
#         # if x+w > 0:
#             #return render_template('output.html')
#             # break
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             if x+w > 0:
#                 # return redirect(url_for('profile'))
#                 return render_template('output.html')

#     #if x+w > 0:
    
#     # When everything is done, release the capture
#     video_capture.release()
#     cv2.destroyAllWindows()
#     # print("is it working")
#     # return render_template('output.html')
#         # When everything is done, release the capture
camera = cv2.VideoCapture(0)
cascPath = './Cascade/data/haarcascade_frontalface_alt2.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
xco=0
yco=0
@app.route('/output')
def output():
    print("This is output")
    print (xco)
    camera.release()
    if xco+yco > 0:
        return render_template('profile.html')
    else:
        return  redirect(url_for('login'))   





def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # ret, buffer = cv2.imencode('.jpg', frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            global xco
            global yco
            for (x, y, w, h) in faces:
                xco = x 
                yco = y
                print(xco)
                print(yco)
                cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)
            ret, buffer = cv2.imencode('.jpg', gray)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            # time.sleep(0.1)
            # if x+y > 0:
            #     print("may be done")
                

                     




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')