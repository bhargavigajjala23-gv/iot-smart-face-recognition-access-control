import cv2
import numpy as np
import pickle
import mediapipe as mp
import time
from keras_facenet import FaceNet
from thingspeak_module import send_to_thingspeak
from unknown_capture import save_unknown
from blink_liveness import detect_blink
from csv_logger import initialize_csv, log_event
from arduino_comm import connect_arduino, send_signal
from profile_ui import draw_profile_panel

# ------------------------------
# Load FaceNet
# ------------------------------
embedder = FaceNet()
 
# ------------------------------
# Load SVM classifier
# ------------------------------
with open("face_classifier.pkl", "rb") as f:
    model, normalizer = pickle.load(f)

# ------------------------------
# MediaPipe Face Detection
# ------------------------------
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(
    model_selection=1,
    min_detection_confidence=0.6
)

# ------------------------------
# Parameters
# ------------------------------
THRESHOLD = 0.60
BUFFER_SIZE = 5
prediction_buffer = []
intrusion_count = 0

system_conf = 0


UNKNOWN_FRAME_THRESHOLD = 10
unknown_counter = 0

# ------------------------------
# Feature Switches
# ------------------------------
ENABLE_UNKNOWN_SAVE = False
ENABLE_BLINK_LIVENESS = False
ENABLE_ARDUINO = False


# -----------------------------

# Verification State Machine
# -----------------------------
verified = False
verified_name = None
verification_time = 0

previous_name = None
VERIFICATION_WINDOW = 10  # seconds access remains valid
name = "Unknown"

initialize_csv()

# ------------------------------
# Connect Arduino
# ------------------------------
if ENABLE_ARDUINO:
    connect_arduino('COM7')
    time.sleep(2)
# ------------------------------
# Start Camera
# ------------------------------
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame,1)

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_detection.process(rgb)

    if results.detections:

        for detection in results.detections:

            bbox = detection.location_data.relative_bounding_box

            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            width = int(bbox.width * w)
            height = int(bbox.height * h)

            # expand bounding box
            x = int(x - width * 0.2)
            y = int(y - height * 0.2)
            width = int(width * 1.4)
            height = int(height * 1.4)

            x = max(0,x)
            y = max(0,y)
            x2 = min(w,x+width)
            y2 = min(h,y+height)

            face_original = frame[y:y2, x:x2]

            if face_original.size == 0:
                continue

            face = cv2.resize(face_original,(160,160))

            # ------------------------------
            # Face Preprocessing
            # ------------------------------
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = face.astype("float32")
            face = np.expand_dims(face, axis=0)

            # ------------------------------
            # Generate embedding
            # ------------------------------
            embedding = embedder.embeddings(face)
            embedding = normalizer.transform(embedding)
            embedding_vector = embedding[0]

            # -----------------------------
            # Face Recognition
            # -----------------------------
            prediction = model.predict(embedding)
            prob = model.predict_proba(embedding)

            name = prediction[0]
            confidence = np.max(prob)

            system_conf = confidence * 100

            if confidence < THRESHOLD:
                name = "Unknown"
                prediction_buffer.append(name)

            # -----------------------------
            # Unknown Face Save
            # -----------------------------
            if ENABLE_UNKNOWN_SAVE and name == "Unknown":
                save_unknown(face_original, confidence)

            # -----------------------------
            # Prediction smoothing
            # -----------------------------
            prediction_buffer.append(name)

            if len(prediction_buffer) > BUFFER_SIZE:
                prediction_buffer.pop(0)

            # Wait until buffer is full before making decision
            if len(prediction_buffer) == BUFFER_SIZE:

                stable_name = max(set(prediction_buffer), key=prediction_buffer.count)
            else:
                stable_name = name
                name = stable_name


            # -----------------------------
            # Face-Change Auto Reset
            # -----------------------------
            if name != previous_name:
                verified = False
                verified_name = None

            previous_name = name

            current_time = time.time()

            # -----------------------------
            # Blink + Access Logic (FIXED)
            # -----------------------------
            if ENABLE_BLINK_LIVENESS:

                blink_state = detect_blink(frame)
                print("Blink:", blink_state)

                current_time = time.time()

                # -----------------------------
                # If already verified and same person
                # -----------------------------
                if verified and name == verified_name:

                    if current_time - verification_time < VERIFICATION_WINDOW:
                        status = "Live Granted"
                        color = (0, 255, 0)
                    else:
                        # Expired session → require new blink
                        verified = False
                        verified_name = None
                        status = "Waiting for Blink"
                        color = (0, 165, 255)

                else:
                    # -----------------------------
                    # Reset verification if person changed
                    # -----------------------------
                    if name != verified_name:
                        verified = False
                        verified_name = None

                    # -----------------------------
                    # Unknown → always deny (IMPORTANT FIX)
                    # -----------------------------
                    if name == "Unknown":
                        status = "Access Denied"
                        color = (0, 0, 255)

                    # -----------------------------
                    # Known person → require blink
                    # -----------------------------
                    else:
                        if blink_state == "LIVE":
                            verified = True
                            verified_name = name
                            verification_time = current_time

                            status = "Live Granted"
                            color = (0, 255, 0)
                        else:
                            status = "Waiting for Blink"
                            color = (0, 165, 255)

            # -----------------------------
            # Normal Mode (No Blink)
            # -----------------------------
            else:

                if name == "Unknown":

                    unknown_counter += 1

                    if unknown_counter >= UNKNOWN_FRAME_THRESHOLD:
                        status = "Access Denied"
                        color = (0, 0, 255)
                    else:
                        status = "Processing..."
                        color = (0, 165, 255)

                else:
                    unknown_counter = 0
                    status = "Access Granted"
                    color = (0, 255, 0)


            # -----------------------------
            # Send Decision to ThingSpeak
            # -----------------------------

            FINAL_STATES = [
                "Access Granted",
                "Access Denied",
                "Live Granted",
                "Spoof Attack",
                "Unknown - Live"
            ]

            if status in FINAL_STATES:

                # -----------------------------
                # Send to Arduino
                # -----------------------------
                if status in ["Access Granted", "Live Granted"] and name != "Unknown":
                    signal = '1'
                else:
                    signal = '0'

                if ENABLE_ARDUINO:
                    send_signal(signal)

                # -----------------------------
                # Send to ThingSpeak
                # -----------------------------
                send_to_thingspeak(name, system_conf, status, intrusion_count)

                # -----------------------------
                # CSV Logging
                # -----------------------------

                if status == "Access Granted":
                    log_event(name, "ACCESS_GRANTED", confidence, "NO_BLINK", "Authorized")

                elif status == "Live Granted":
                    log_event(name, "ACCESS_GRANTED", confidence, "BLINK_OK", "Authorized")

                elif status == "Spoof Attack":
                    log_event(name, "ACCESS_DENIED", confidence, "NO_BLINK", "Spoof_Attempt")

                elif status == "Unknown - Live":
                    log_event("Unknown", "ACCESS_DENIED", confidence, "BLINK_OK", "Unauthorized")

                elif status == "Access Denied":
                    log_event(name, "ACCESS_DENIED", confidence, "NO_BLINK", "Unauthorized")



            # -----------------------------
            # Intrusion Counter
            # -----------------------------
            if status in ["Spoof Attack", "Access Denied", "Unknown - Live"]:
                intrusion_count += 1


            label = f"{name} ({confidence*100:.1f}%)"

            # ------------------------------
            # Draw box
            # ------------------------------
            cv2.rectangle(frame,(x,y),(x2,y2),color,2)

            cv2.putText(frame,label,
                        (x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        color,
                        2)

            cv2.putText(frame,
                        status,
                        (x,y2+30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        color,
                        2)
    # ------------------------------
    # Profile Panel UI
    # ------------------------------

    frame = draw_profile_panel(frame, name, status, confidence, w)


    # ------------------------------
    # System confidence display
    # ------------------------------
    cv2.putText(frame,
                f"System Confidence: {system_conf:.1f}%",
                (20,60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255,255,255),
                2)

    cv2.imshow("AI Face Recognition Access Control",frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()