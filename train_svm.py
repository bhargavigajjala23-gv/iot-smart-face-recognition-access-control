import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import Normalizer
import pickle

# Load embeddings
X = np.load("embeddings.npy")
y = np.load("labels.npy")

print("Embeddings shape:", X.shape)
print("Labels shape:", y.shape)

# Normalize embeddings
normalizer = Normalizer(norm='l2')
X = normalizer.fit_transform(X)

# Train SVM
model = SVC(kernel='linear', probability=True)
model.fit(X, y)

print("Training completed")

# Save BOTH model and normalizer together
with open("face_classifier.pkl", "wb") as f:
    pickle.dump((model, normalizer), f)

print("Model + normalizer saved successfully")