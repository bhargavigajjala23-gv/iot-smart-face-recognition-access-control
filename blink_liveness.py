import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# Blink variables
CLOSED_FRAMES = 0
EAR_THRESHOLD = 0.21

def eye_aspect_ratio(eye):
    A = abs(eye[1][1] - eye[5][1])
    B = abs(eye[2][1] - eye[4][1])
    C = abs(eye[0][0] - eye[3][0])

    if C == 0:
        return 0

    return (A + B) / (2.0 * C)


def detect_blink(frame):
    global CLOSED_FRAMES

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return "NO_FACE"

    mesh = results.multi_face_landmarks[0]
    h, w, _ = frame.shape

    left_eye = [(int(mesh.landmark[i].x * w),
                 int(mesh.landmark[i].y * h)) for i in LEFT_EYE]

    right_eye = [(int(mesh.landmark[i].x * w),
                  int(mesh.landmark[i].y * h)) for i in RIGHT_EYE]

    left_ear = eye_aspect_ratio(left_eye)
    right_ear = eye_aspect_ratio(right_eye)
    ear = (left_ear + right_ear) / 2.0

    # Eye closed
    if ear < EAR_THRESHOLD:
        CLOSED_FRAMES += 1

    else:
        # Blink detected only at reopening moment
        if CLOSED_FRAMES > 2:
            CLOSED_FRAMES = 0
            return "LIVE"

        CLOSED_FRAMES = 0

    return "WAITING"