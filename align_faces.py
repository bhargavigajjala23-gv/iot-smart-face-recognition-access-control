import os
import cv2
import mediapipe as mp
import numpy as np

DATASET_PATH = "Dataset_split/train"
OUTPUT_PATH = "aligned_faces"

os.makedirs(OUTPUT_PATH, exist_ok=True)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

LEFT_EYE = 33
RIGHT_EYE = 263


def align_face(image):

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return None

    landmarks = results.multi_face_landmarks[0]

    h, w, _ = image.shape

    left_eye = landmarks.landmark[LEFT_EYE]
    right_eye = landmarks.landmark[RIGHT_EYE]

    left_eye = (int(left_eye.x * w), int(left_eye.y * h))
    right_eye = (int(right_eye.x * w), int(right_eye.y * h))

    dx = right_eye[0] - left_eye[0]
    dy = right_eye[1] - left_eye[1]

    angle = np.degrees(np.arctan2(dy, dx))

    center = ((left_eye[0] + right_eye[0]) // 2,
              (left_eye[1] + right_eye[1]) // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1)

    aligned = cv2.warpAffine(image, M, (w, h))

    face = cv2.resize(aligned, (160, 160))

    return face


for person in os.listdir(DATASET_PATH):

    person_path = os.path.join(DATASET_PATH, person)
    save_path = os.path.join(OUTPUT_PATH, person)

    os.makedirs(save_path, exist_ok=True)

    for img_name in os.listdir(person_path):

        img_path = os.path.join(person_path, img_name)

        image = cv2.imread(img_path)

        aligned = align_face(image)

        if aligned is not None:
            cv2.imwrite(os.path.join(save_path, img_name), aligned)

print("Face alignment completed!")