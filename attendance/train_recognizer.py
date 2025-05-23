import cv2
import numpy as np
import os

DATASET_DIR = "dataset"
CASCADE_PATH = "haarcascade_frontalface_default.xml"
TRAINER_PATH = "trainer.yml"
LABELS_PATH = "labels.npy"

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
recognizer = cv2.face.LBPHFaceRecognizer_create()

def get_images_and_labels(dataset_dir):
    faces = []
    labels = []
    label_dict = {}
    current_label = 0
    for person_name in os.listdir(dataset_dir):
        person_dir = os.path.join(dataset_dir, person_name)
        if not os.path.isdir(person_dir):
            continue
        label_dict[current_label] = person_name
        for img_name in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            faces.append(img)
            labels.append(current_label)
        current_label += 1
    return faces, labels, label_dict

def train_and_save():
    faces, labels, label_dict = get_images_and_labels(DATASET_DIR)
    if len(faces) == 0:
        print("No images found for training!")
        return
    recognizer.train(faces, np.array(labels))
    recognizer.save(TRAINER_PATH)
    np.save(LABELS_PATH, label_dict)
    print(f"Training complete. Saved recognizer to {TRAINER_PATH} and labels to {LABELS_PATH}.")

if __name__ == "__main__":
    train_and_save()