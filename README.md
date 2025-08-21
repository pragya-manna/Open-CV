# ✋ Gesture Controlled Game using MediaPipe and OpenCV

A Python-based hand gesture recognition app that allows you to control your system (keyboard presses) using simple finger gestures via webcam. It uses **MediaPipe** for real-time hand tracking and **PyAutoGUI** for simulating keypresses.

---

## 📽️ Demo
- Move hand right → `Right` Arrow
- Move hand left → `Left` Arrow
- Move hand up → `Up` Arrow
- Move hand down → `Down` Arrow

These gestures simulate keyboard arrow keys in any active application (like car racing games, character movement, or presentations).

---

## 🛠️ Requirements

Install dependencies with:

```bash
pip install opencv-python mediapipe pyautogui
```

Python 3.8+ is recommended.

---

## 📁 Project Files

- `gesture_control.py` – Main script that runs the gesture control
- No other files required; runs directly using webcam (Used DroidCam app for camera)

---

## 🚀 How to Run

1. Connect your webcam.
2. Run the script:

```bash
python gesture_control.py
```

3. Hold your hand in the center for auto-calibration.
4. Move hand up/down/left/right to control.
5. Press c to recalibrate anytime.
6. Press q to quit.

---

## 🧠 How It Works
- Detects hand landmarks using MediaPipe Hands.
- Takes the wrist point (landmark 0) as the reference.
- Calibrates a neutral center position.
- Calculates hand displacement (dx, dy) from center:
   - If movement crosses a dead zone threshold → triggers a direction.
- Ensures gestures don’t repeat too fast using a small delay.
- Sends corresponding arrow key presses with PyAutoGUI.


---

## ⚙️ Key Features

- Calibration System → Press c to reset neutral position.
- Dead Zone → Ignores small jittery movements.
- Gesture Delay → Prevents multiple keypress spam.
- Works in real time with ~30fps.

---

## 💡 Gesture Mappings

| Hand Movement                  | Keys Triggered  |
|--------------------------------|-----------------|
| Move Right                     | → Right Arrow   |
| Move Left                      | ← Left Arrow    |
| Mode Up                        | ↑ Up Arrow      |
| Mode Down                      | ↓ Down Arrow    |

---

## 🔒 Notes & Tips

- Good lighting = better tracking.
- Keep only one hand visible.
- Works on Windows, macOS, Linux.
- Can be easily extended (e.g., WASD keys, custom actions).

---

## 🧑‍💻 Author
Built with ❤️ by Pragya using Python, MediaPipe, OpenCV, PyAutoGUI.
