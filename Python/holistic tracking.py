import cv2
import matplotlib.pyplot as plt
import IPython.display as display
from IPython.display import clear_output
import mediapipe as mp
import time
import serial
# arduino = serial.Serial('COM9', 9600)  # Change 'COM3' to your Arduino's port

cap=cv2.VideoCapture(0)
mp_holistics=mp.solutions.holistic
mp_drawings=mp.solutions.drawing_utils
holistic=mp_holistics.Holistic(min_detection_confidence=0.5,min_tracking_confidence=0.5)
center_x = cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 2
center_y = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2

# Servo movement calibration values (adjust based on your servos)
servo_pan_offset = 0  # Offset for centering pan servo
servo_tilt_offset = 0  # Offset for centering tilt servo
servo_pan_range = 180  # Pan servo movement range (degrees)
servo_tilt_range = 180  # Tilt servo movement range (degrees)
pan_movement_factor = 0.2  # Factor for scaling pan movement based on face offset
tilt_movement_factor = 0.2  # Factor for scaling tilt movement based on face offset
prevTime = 0

with mp_holistics.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.face_landmarks:
            h, w, _ = image.shape
            face_landmarks = results.face_landmarks.landmark
            x_min = min([lm.x for lm in face_landmarks]) * w
            x_max = max([lm.x for lm in face_landmarks]) * w
            y_min = min([lm.y for lm in face_landmarks]) * h
            y_max = max([lm.y for lm in face_landmarks]) * h
            face_center_x = x_min + x_max // 2
            face_center_y = y_min + y_max // 2
            # Calculate offsets from center
            pan_offset = face_center_x - center_x
            tilt_offset = face_center_y - center_y

            # Scale offsets for servo movement
            pan_movement = int(pan_offset * pan_movement_factor)
            tilt_movement = int(tilt_offset * tilt_movement_factor)

            # Apply offsets with calibration and clamp within servo range
            pan_position = servo_pan_offset + pan_movement
            tilt_position = servo_tilt_offset - tilt_movement  # Tilt often needs inversion

            pan_position = max(0, min(pan_position, servo_pan_range))
            tilt_position = max(0, min(tilt_position, servo_tilt_range))
            print(pan_position, tilt_position)

            cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
        cv2.imshow("Live face Tracking",image)
        key=cv2.waitKey(1)
        if key & 0xFF==ord('q'):
            break

cap.release()
cv2.destroyAllWindows()