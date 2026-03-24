import cv2
import os
import sys

name = sys.stdin.read().strip()

if name == "" or name == "Enter Name":
    print("No valid name ❌")
    exit()

path = f"dataset/{name}"

if not os.path.exists(path):
    os.makedirs(path)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

count = 0

print("Press S to save, Q to quit")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera error ❌")
        continue

    cv2.imshow("Capture Images", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        cv2.imwrite(f"{path}/{count}.jpg", frame)
        count += 1
        print("Saved:", count)

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()