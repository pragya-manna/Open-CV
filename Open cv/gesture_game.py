import cv2
import mediapipe as mp
import pygame
import threading
import time

# ----------------------------
# === Gesture Detection Part ===
# ----------------------------

gesture_command = None
last_gesture_time = 0
cooldown = 0.5  # seconds

def gesture_detection():
    global gesture_command, last_gesture_time

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Can't receive frame. Exiting ...")
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        gesture = None

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index_tip = hand_landmarks.landmark[8]
                x = int(index_tip.x * w)
                y = int(index_tip.y * h)

                cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

                current_time = time.time()
                if current_time - last_gesture_time > cooldown:
                    if x < w * 0.3:
                        gesture = 'LEFT'
                    elif x > w * 0.7:
                        gesture = 'RIGHT'
                    elif y < h * 0.3:
                        gesture = 'UP'
                    elif y > h * 0.7:
                        gesture = 'DOWN'

                    if gesture:
                        gesture_command = gesture
                        last_gesture_time = current_time
                        print(f"✋ Detected Gesture: {gesture}")

                # Overlay text
                if x < w * 0.3:
                    cv2.putText(frame, "LEFT", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif x > w * 0.7:
                    cv2.putText(frame, "RIGHT", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif y < h * 0.3:
                    cv2.putText(frame, "UP", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif y > h * 0.7:
                    cv2.putText(frame, "DOWN", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Webcam - Gesture Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# ----------------------------
# === Simple Pygame Subway Clone ===
# ----------------------------

def game_loop():
    global gesture_command

    pygame.init()
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Subway Surfers - Gesture Controlled")

    clock = pygame.time.Clock()

    # Player settings
    player = pygame.Rect(WIDTH//2 - 25, HEIGHT - 60, 50, 50)
    player_color = (0, 128, 255)
    jump = False
    slide = False
    jump_count = 10

    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Background
        screen.fill((30, 30, 30))

        # Gesture control
        if gesture_command:
            if gesture_command == 'LEFT':
                player.x -= 50
            elif gesture_command == 'RIGHT':
                player.x += 50
            elif gesture_command == 'UP' and not jump:
                jump = True
            elif gesture_command == 'DOWN':
                slide = True

            gesture_command = None

        # Jump mechanic
        if jump:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player.y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                jump = False
                jump_count = 10

        # Slide mechanic
        if slide:
            player.height = 30
        else:
            player.height = 50
        slide = False

        # Boundaries
        if player.x < 0:
            player.x = 0
        if player.x > WIDTH - player.width:
            player.x = WIDTH - player.width

        # Draw player
        pygame.draw.rect(screen, player_color, player)

        # Update display
        pygame.display.flip()

    pygame.quit()


# ----------------------------
# === Run Both Threads ===
# ----------------------------

if __name__ == "__main__":
    # Run gesture detection in a separate thread
    t1 = threading.Thread(target=gesture_detection)
    t1.start()

    # Run the game in the main thread
    game_loop()

    # Wait for gesture detection thread to finish
    t1.join()
