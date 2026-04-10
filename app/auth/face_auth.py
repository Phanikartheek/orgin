"""
Face Authentication Module
Uses OpenCV LBPH face recognition for user authentication.
Cleaned up version of the legacy face auth system.
"""

import cv2
from app.config import HAARCASCADE_PATH, TRAINER_PATH, FACE_NAMES, FACE_AUTH_ENABLED


def authenticate_face() -> bool:
    """
    Run face authentication using the webcam.
    Returns True if a known face is recognized, False otherwise.
    """
    if not FACE_AUTH_ENABLED:
        return True

    try:
        # Initialize LBPH face recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(TRAINER_PATH)

        # Load Haar cascade for face detection
        face_cascade = cv2.CascadeClassifier(HAARCASCADE_PATH)
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Open camera
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cam.set(3, 640)  # Width
        cam.set(4, 480)  # Height

        min_w = 0.1 * cam.get(3)
        min_h = 0.1 * cam.get(4)

        authenticated = False

        while True:
            ret, frame = cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(min_w), int(min_h)),
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                face_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                if confidence < 100:
                    name = FACE_NAMES[face_id] if face_id < len(FACE_NAMES) else "Unknown"
                    accuracy = f"{round(100 - confidence)}%"
                    authenticated = True
                else:
                    name = "Unknown"
                    accuracy = f"{round(100 - confidence)}%"

                cv2.putText(frame, name, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(frame, accuracy, (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

            cv2.imshow("Jarvis — Face Authentication", frame)

            key = cv2.waitKey(10) & 0xFF
            if key == 27:  # ESC to cancel
                break
            if authenticated:
                break

        cam.release()
        cv2.destroyAllWindows()
        return authenticated

    except FileNotFoundError:
        print("[Auth] Trainer file not found. Skipping face authentication.")
        return True
    except Exception as e:
        print(f"[Auth] Error: {e}")
        return True
