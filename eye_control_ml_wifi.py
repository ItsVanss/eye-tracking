import cv2
import mediapipe as mp
import numpy as np
import socket
import joblib
import time

# ================= LOAD MODEL =================
model = joblib.load('eye_model.pkl')

# ================= KONEKSI KE ESP32 =================
ESP_IP = "10.50.127.67"
PORT = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)

# coba connect berulang sampai berhasil
while True:
    try:
        print("Mencoba connect ke ESP32...")
        sock.connect((ESP_IP, PORT))
        print("✅ Connected to ESP32!")
        break
    except:
        print("❌ Gagal connect, coba lagi...")
        time.sleep(2)

# ================= MEDIAPIPE =================
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

# ================= LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480))

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

        # ================= KIRIM DATA =================
        if pred != last:
            try:
                if pred == "LEFT":
                    sock.send(b'L')
                    print("KIRI")
                elif pred == "RIGHT":
                    sock.send(b'R')
                    print("KANAN")
                else:
                    sock.send(b'C')
                    print("TENGAH")

                last = pred

            except:
                print("⚠️ Koneksi putus, reconnect...")
                sock.close()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # ================= DISPLAY =================
        cv2.putText(frame, pred, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.circle(frame, tuple(left_iris), 3, (0, 0, 255), -1)
        cv2.circle(frame, tuple(right_iris), 3, (0, 0, 255), -1)

    cv2.imshow("Eye Tracking WIFI Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

    time.sleep(0.03)

# ================= CLEANUP =================
cap.release()
sock.close()
cv2.destroyAllWindows()