import cv2
import dlib
from scipy.spatial import distance
from playsound import playsound

# Load the pre-trained face detector and facial landmarks predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Define function to calculate eye aspect ratio (EAR)
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Threshold for blink detection (EAR)
EAR_THRESHOLD = 0.2
CONSEC_FRAMES = 30  # Number of frames to wait before triggering alert

# Initialize variables
blink_counter = 0
alarm_triggered = False

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # Get the coordinates for the left and right eyes
        left_eye = []
        right_eye = []

        for i in range(36, 42):
            left_eye.append((landmarks.part(i).x, landmarks.part(i).y))
        for i in range(42, 48):
            right_eye.append((landmarks.part(i).x, landmarks.part(i).y))

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        # Average EAR for both eyes
        ear = (left_ear + right_ear) / 2.0

        # Blink detection
        if ear < EAR_THRESHOLD:
            blink_counter += 1
        else:
            if blink_counter >= CONSEC_FRAMES:
                print("Eye Blink Detected!")
                if not alarm_triggered:
                    playsound('alert_sound.mp3')  # Alert sound
                    alarm_triggered = True
            blink_counter = 0
            alarm_triggered = False

    # Display the webcam feed
    cv2.imshow("Eye Blink Detection", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

