import os
import cv2
import numpy as np
from keras_facenet import FaceNet

# Initialize FaceNet
embedder = FaceNet()

aligned_path = "aligned_faces"

embeddings = []
labels = []

for person in os.listdir(aligned_path):

    person_folder = os.path.join(aligned_path, person)

    for image_name in os.listdir(person_folder):

        img_path = os.path.join(person_folder, image_name)

        img = cv2.imread(img_path)

        if img is None:
            continue

        # Resize to FaceNet size
        img = cv2.resize(img, (160,160))

        # BGR → RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = np.expand_dims(img, axis=0)

        # Generate embedding
        embedding = embedder.embeddings(img)

        embeddings.append(embedding[0])
        labels.append(person)

embeddings = np.array(embeddings)
labels = np.array(labels)

print("Embeddings created:", embeddings.shape)
print("Identities:", np.unique(labels))

np.save("embeddings.npy", embeddings)
np.save("labels.npy", labels)

print("Database saved successfully")

print("\nExtracting Face Embedding...\n")
print("Embedding Shape:", embedding.shape)
print("\nEmbedding Vector:\n")
print(embedding)