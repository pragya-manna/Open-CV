import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Calibration
neutral_x = None
neutral_y = None
calibrated = False

# Gesture timing
prev_gesture = None
last_action_time = 0
gesture_delay = 0.8  # seconds between actions

# Dead zone (pixels)
dead_zone = 50  # change to adjust sensitivity

print("[INFO] Hold your hand in the center to calibrate. Press 'c' to recalibrate, 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    current_gesture = None

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Get wrist point as center of hand
            cx = int(hand_landmarks.landmark[0].x * w)
            cy = int(hand_landmarks.landmark[0].y * h)

            if not calibrated:
                neutral_x = cx
                neutral_y = cy
                calibrated = True
                print(f"[INFO] Calibrated at ({neutral_x}, {neutral_y})")
            
            # Draw neutral center
            cv2.circle(frame, (neutral_x, neutral_y), 8, (0, 0, 255), -1)
            # Draw current hand position
            cv2.circle(frame, (cx, cy), 8, (0, 255, 0), -1)

            dx = cx - neutral_x
            dy = cy - neutral_y

            # Decide gesture based on movement beyond dead zone
            if abs(dx) > abs(dy):  # horizontal movement
                if dx > dead_zone:
                    current_gesture = "right"
                elif dx < -dead_zone:
                    current_gesture = "left"
            else:  # vertical movement
                if dy > dead_zone:
                    current_gesture = "down"
                elif dy < -dead_zone:
                    current_gesture = "up"

            # Only trigger if delay passed and gesture changed
            if current_gesture and current_gesture != prev_gesture and time.time() - last_action_time > gesture_delay:
                pyautogui.press(current_gesture)
                print(f"Gesture detected: {current_gesture}")
                prev_gesture = current_gesture
                last_action_time = time.time()

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    else:
        prev_gesture = None

    # Show instructions
    cv2.putText(frame, "Press 'c' to recalibrate, 'q' to quit.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Display
    cv2.imshow("Hand Gesture Joystick Control", frame)

    key = cv2.waitKey(5) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        calibrated = False
        print("[INFO] Recalibrate: show your hand in center!")

cap.release()
cv2.destroyAllWindows()
