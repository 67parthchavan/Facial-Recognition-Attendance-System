import cv2
import face_recognition
import pickle
import numpy as np
from datetime import datetime
import os

print("🚀 Starting Face Attendance System...")

# ---------------- LOAD ENCODINGS ----------------
with open("encodings/encodings.pkl", "rb") as f:
    data = pickle.load(f)

print("Encodings loaded:", len(data["names"]))

# ---------------- CSV FILE ----------------
file_name = "attendance.csv"

# Create file if not exists
if not os.path.exists(file_name):
    with open(file_name, "w") as f:
        f.write("Name,Time\n")

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera error ❌")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, faces)

    print("Faces found:", len(faces))

    for encoding, face in zip(encodings, faces):

        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        face_dist = face_recognition.face_distance(data["encodings"], encoding)

        if len(face_dist) > 0:
            best_match = np.argmin(face_dist)

            if matches[best_match]:
                name = data["names"][best_match]

        print("Detected:", name)

        top, right, bottom, left = face

        # Draw box
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # ---------------- FORCE SAVE ----------------
        if name != "Unknown":
            now = datetime.now().strftime("%H:%M:%S")

            try:
                with open(file_name, "a") as f:
                    f.write(f"{name},{now}\n")

                print(f"✅ SAVED: {name}")

            except Exception as e:
                print("❌ SAVE ERROR:", e)

    cv2.imshow("Face Attendance System", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()