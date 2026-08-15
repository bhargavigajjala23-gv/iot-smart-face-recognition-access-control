import os
import random
import shutil

if os.path.exists("Dataset_split"):
    shutil.rmtree("Dataset_split")

SOURCE_DIR = "Dataset"      # your current folder
OUTPUT_DIR = "Dataset_split"

TRAIN_RATIO = 0.8
random.seed(42)

train_dir = os.path.join(OUTPUT_DIR, "train")
test_dir = os.path.join(OUTPUT_DIR, "test")

os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

for person in os.listdir(SOURCE_DIR):
    person_path = os.path.join(SOURCE_DIR, person)

    if not os.path.isdir(person_path):
        continue

    images = [img for img in os.listdir(person_path) if img.endswith(".jpg")]

    if len(images) < 5:
        continue

    random.shuffle(images)
    split = int(len(images) * TRAIN_RATIO)

    train_imgs = images[:split]
    test_imgs = images[split:]

    os.makedirs(os.path.join(train_dir, person), exist_ok=True)
    os.makedirs(os.path.join(test_dir, person), exist_ok=True)

    for img in train_imgs:
        shutil.copy(
            os.path.join(person_path, img),
            os.path.join(train_dir, person, img)
        )

    for img in test_imgs:
        shutil.copy(
            os.path.join(person_path, img),
            os.path.join(test_dir, person, img)
        )
        print(person, len(os.listdir(person_path)))

    print(f"{person}: {len(train_imgs)} train | {len(test_imgs)} test")

print("✅ Proper split completed!")