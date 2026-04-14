import cv2
import mediapipe as mp
import numpy as np
import csv

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

LEFT_EYE  = [33, 133]
RIGHT_EYE = [362, 263]
LEFT_IRIS  = [468]
RIGHT_IRIS = [473]

file = open('eye_dataset.csv', mode='a', newline='')
writer = csv.writer(file)

def get_feature(iris, left_point, right_point):
    eye_width = right_point[0] - left_point[0]
    if eye_width == 0:
        return 0
    iris_pos = iris[0] - left_point[0]
    return iris_pos / eye_width

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

        cv2.putText(frame, "Press L/R/C to label", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('l'):
            writer.writerow([f1, f2, 'LEFT'])
            print("Saved LEFT")
        elif key == ord('r'):
            writer.writerow([f1, f2, 'RIGHT'])
            print("Saved RIGHT")
        elif key == ord('c'):
            writer.writerow([f1, f2, 'CENTER'])
            print("Saved CENTER")

    cv2.imshow("Collect Data", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
file.close()
cv2.destroyAllWindows()