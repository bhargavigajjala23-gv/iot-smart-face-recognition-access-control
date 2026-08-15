import os
import cv2
import numpy as np

DATASET_PATH = "Dataset_split/train"


def load_dataset(dataset_path):

    faces = []
    labels = []

    for person_name in os.listdir(dataset_path):

        person_folder = os.path.join(dataset_path, person_name)

        if not os.path.isdir(person_folder):
            continue

        for image_name in os.listdir(person_folder):

            image_path = os.path.join(person_folder, image_name)

            img = cv2.imread(image_path)

            if img is None:
                continue

            img = cv2.resize(img, (160,160))

            faces.append(img)
            labels.append(person_name)

    faces = np.array(faces)
    labels = np.array(labels)

    return faces, labels

if __name__ == "__main__":

    faces, labels = load_dataset("aligned_faces")

    print("Faces loaded:", len(faces))
    print("Labels loaded:", len(labels))

    print("Example label:", labels[0])
    print("Face shape:", faces[0].shape)

    import matplotlib.pyplot as plt

    plt.imshow(faces[0])
    plt.title(labels[0])
    plt.show()