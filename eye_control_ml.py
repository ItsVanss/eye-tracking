import cv2
import mediapipe as mp
import numpy as np
import serial
import time
import joblib

# Load model
model = joblib.load('eye_model.pkl')

arduino = serial.Serial('COM7', 9600)
time.sleep(2)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

LEFT_EYE  = [33, 133]
RIGHT_EYE = [362, 263]
LEFT_IRIS  = [468]
RIGHT_IRIS = [473]

def get_feature(iris, left_point, right_point):
    eye_width = right_point[0] - left_point[0]
    if eye_width == 0:
        return 0
    iris_pos = iris[0] - left_point[0]
    return iris_pos / eye_width

last = ""

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        mesh_points = np.array([
            [int(p.x * frame.shape[1]), int(p.y * frame.shape[0])]
            for p in results.multi_face_landmarks[0].landmark
        ])

        left_iris  = mesh_points[LEFT_IRIS[0]]
        right_iris = mesh_points[RIGHT_IRIS[0]]

        left_eye_left  = mesh_points[LEFT_EYE[0]]
        left_eye_right = mesh_points[LEFT_EYE[1]]
        right_eye_left  = mesh_points[RIGHT_EYE[0]]
        right_eye_right = mesh_points[RIGHT_EYE[1]]

        f1 = get_feature(left_iris, left_eye_left, left_eye_right)
        f2 = get_feature(right_iris, right_eye_left, right_eye_right)

        pred = model.predict([[f1, f2]])[0]

        if pred != last:
            if pred == "LEFT":
                arduino.write(b'L')
            elif pred == "RIGHT":
                arduino.write(b'R')
            else:
                arduino.write(b'C')
            last = pred

        cv2.putText(frame, pred, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("ML Eye Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()