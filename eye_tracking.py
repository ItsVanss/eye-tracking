import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

# Landmark index untuk mata (MediaPipe)
LEFT_EYE = [33, 133]   # kiri dan kanan batas mata kiri
RIGHT_EYE = [362, 263] # kiri dan kanan batas mata kanan
LEFT_IRIS = [468]      # pupil kiri
RIGHT_IRIS = [473]     # pupil kanan

def get_eye_direction(iris, left_point, right_point):
    eye_width = right_point[0] - left_point[0]
    iris_pos = iris[0] - left_point[0]

    ratio = iris_pos / eye_width

    if ratio < 0.4:
        return "LEFT"
    elif ratio > 0.6:
        return "RIGHT"
    else:
        return "CENTER"

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

        # Ambil titik
        left_iris = mesh_points[LEFT_IRIS[0]]
        right_iris = mesh_points[RIGHT_IRIS[0]]

        left_eye_left = mesh_points[LEFT_EYE[0]]
        left_eye_right = mesh_points[LEFT_EYE[1]]

        right_eye_left = mesh_points[RIGHT_EYE[0]]
        right_eye_right = mesh_points[RIGHT_EYE[1]]

        # Deteksi arah
        left_dir = get_eye_direction(left_iris, left_eye_left, left_eye_right)
        right_dir = get_eye_direction(right_iris, right_eye_left, right_eye_right)

        # Gabungkan hasil
        if left_dir == "LEFT" and right_dir == "LEFT":
            direction = "LOOKING LEFT"
        elif left_dir == "RIGHT" and right_dir == "RIGHT":
            direction = "LOOKING RIGHT"
        else:
            direction = "CENTER"

        cv2.putText(frame, direction, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        # Visualisasi
        cv2.circle(frame, tuple(left_iris), 3, (0, 0, 255), -1)
        cv2.circle(frame, tuple(right_iris), 3, (0, 0, 255), -1)

    cv2.imshow("Eye Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()