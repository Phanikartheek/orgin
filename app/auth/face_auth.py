"""
Face Authentication Module
Uses OpenCV LBPH face recognition for user authentication.
Shows a visual verification screen with progress feedback.
"""

import cv2
import time
from app.config import HAARCASCADE_PATH, TRAINER_PATH, FACE_NAMES, FACE_AUTH_ENABLED


def authenticate_face() -> bool:
    """
    Run face authentication using the webcam.
    Shows camera feed with face detection, verifies identity,
    and displays a success/failure screen before closing.
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

        if not cam.isOpened():
            print("[Auth] Camera not available. Skipping face auth.")
            return True

        min_w = 0.1 * cam.get(3)
        min_h = 0.1 * cam.get(4)

        authenticated = False
        auth_name = ""
        auth_accuracy = ""
        frame_count = 0
        verify_count = 0  # Need multiple successful frames for reliable auth
        REQUIRED_VERIFICATIONS = 5  # Must detect face 5 times to confirm

        print("[Auth] Camera opened. Please look at the camera...")

        while True:
            ret, frame = cam.read()
            if not ret:
                break

            frame_count += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(min_w), int(min_h)),
            )

            # Draw scanning overlay
            h, w = frame.shape[:2]
            cv2.rectangle(frame, (0, 0), (w, 40), (0, 0, 0), -1)  # Top bar
            cv2.putText(frame, "JARVIS - Face Authentication", (10, 28),
                        font, 0.7, (0, 210, 255), 2)

            # Draw bottom status bar
            cv2.rectangle(frame, (0, h - 50), (w, h), (0, 0, 0), -1)

            if len(faces) == 0:
                cv2.putText(frame, "Scanning... Please show your face", (10, h - 18),
                            font, 0.6, (100, 100, 255), 1)
                verify_count = 0  # Reset if face lost
            else:
                for (x, y, fw, fh) in faces:
                    face_id, confidence = recognizer.predict(gray[y:y + fh, x:x + fw])

                    if confidence < 100:
                        name = FACE_NAMES[face_id] if face_id < len(FACE_NAMES) else "Unknown"
                        accuracy = round(100 - confidence)

                        # Green box for recognized face
                        cv2.rectangle(frame, (x, y), (x + fw, y + fh), (0, 255, 0), 2)
                        cv2.putText(frame, f"{name}", (x + 5, y - 10),
                                    font, 0.8, (0, 255, 0), 2)
                        cv2.putText(frame, f"Match: {accuracy}%", (x + 5, y + fh + 22),
                                    font, 0.6, (0, 255, 255), 1)

                        verify_count += 1
                        auth_name = name
                        auth_accuracy = f"{accuracy}%"

                        # Show progress bar
                        progress = int((verify_count / REQUIRED_VERIFICATIONS) * (w - 20))
                        cv2.rectangle(frame, (10, h - 45), (10 + progress, h - 35), (0, 255, 0), -1)
                        cv2.rectangle(frame, (10, h - 45), (w - 10, h - 35), (0, 255, 0), 1)
                        cv2.putText(frame, f"Verifying {name}... ({verify_count}/{REQUIRED_VERIFICATIONS})",
                                    (10, h - 12), font, 0.5, (0, 255, 0), 1)
                    else:
                        # Red box for unknown face
                        cv2.rectangle(frame, (x, y), (x + fw, y + fh), (0, 0, 255), 2)
                        cv2.putText(frame, "Unknown", (x + 5, y - 10),
                                    font, 0.8, (0, 0, 255), 2)
                        cv2.putText(frame, "Access Denied", (10, h - 18),
                                    font, 0.6, (0, 0, 255), 1)
                        verify_count = 0

            cv2.imshow("JARVIS - Face Authentication", frame)

            # Check if verified enough times
            if verify_count >= REQUIRED_VERIFICATIONS:
                authenticated = True
                # Show success screen for 2 seconds
                for _ in range(20):
                    ret, frame = cam.read()
                    if ret:
                        h, w = frame.shape[:2]
                        # Green overlay
                        overlay = frame.copy()
                        cv2.rectangle(overlay, (0, 0), (w, h), (0, 80, 0), -1)
                        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
                        # Success text
                        cv2.putText(frame, "ACCESS GRANTED", (w // 2 - 180, h // 2 - 20),
                                    font, 1.2, (0, 255, 0), 3)
                        cv2.putText(frame, f"Welcome, {auth_name}!", (w // 2 - 140, h // 2 + 30),
                                    font, 0.8, (255, 255, 255), 2)
                        cv2.imshow("JARVIS - Face Authentication", frame)
                    cv2.waitKey(100)
                break

            key = cv2.waitKey(10) & 0xFF
            if key == 27:  # ESC to cancel
                break

            # Timeout after 30 seconds
            if frame_count > 900:  # ~30 seconds at 30fps
                print("[Auth] Timeout. Face not recognized.")
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
