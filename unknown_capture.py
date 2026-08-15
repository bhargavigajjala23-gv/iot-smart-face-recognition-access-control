import os
import cv2
import time

# -----------------------------
# Folder Setup
# -----------------------------
SAVE_DIR = "unauthorized_attempts"
os.makedirs(SAVE_DIR, exist_ok=True)

# -----------------------------
# Parameters
# -----------------------------
UNKNOWN_CONFIRM_FRAMES = 5     # frames to confirm unknown
CAPTURE_INTERVAL = 10          # seconds between saves
MIN_FACE_SIZE = 120            # ignore very small faces

# -----------------------------
# State Variables
# -----------------------------
last_unknown_capture = 0
unknown_counter = 0


def save_unknown(face, confidence):
    global last_unknown_capture, unknown_counter

    # -----------------------------
    # Safety checks
    # -----------------------------
    if face is None or face.size == 0:
        return

    h, w = face.shape[:2]

    if h < MIN_FACE_SIZE or w < MIN_FACE_SIZE:
        return

    # -----------------------------
    # Check if truly unknown
    # -----------------------------
    if confidence >= 0.60:
        unknown_counter = 0
        return

    unknown_counter += 1

    # -----------------------------
    # Confirm unknown over frames
    # -----------------------------
    if unknown_counter < UNKNOWN_CONFIRM_FRAMES:
        return

    # -----------------------------
    # Prevent frequent saving
    # -----------------------------
    current_time = time.time()

    if current_time - last_unknown_capture < CAPTURE_INTERVAL:
        return

    # -----------------------------
    # Improve saved image quality
    # -----------------------------
    face_resized = cv2.resize(face, (300, 300))

    # -----------------------------
    # Unique filename (timestamp + ms)
    # -----------------------------
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    millis = int((current_time % 1) * 1000)

    filename = f"{SAVE_DIR}/unknown_{timestamp}_{millis}_{confidence:.2f}.jpg"

    cv2.imwrite(filename, face_resized)

    # -----------------------------
    # Update state
    # -----------------------------
    last_unknown_capture = current_time
    unknown_counter = 0

    print(f"[INFO] Unknown person stored: {filename}")