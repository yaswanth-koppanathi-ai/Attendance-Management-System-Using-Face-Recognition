import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import os

# Path to Haar Cascade and trained recognizer
CASCADE_PATH = "haarcascade_frontalface_default.xml"
RECOGNIZER_PATH = "trainer.yml"
LABELS_PATH = "labels.npy"  # Numpy file with {label: name} mapping
ATTENDANCE_CSV = "attendance.csv"

# Load face detector and recognizer
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(RECOGNIZER_PATH)

# Load label-name mapping
if os.path.exists(LABELS_PATH):
    label_dict = np.load(LABELS_PATH, allow_pickle=True).item()
else:
    label_dict = {}  # {label: name}

# Attendance dictionary to avoid duplicate entries in this session
attendance_dict = {}

def load_existing_attendance():
    """Load today's attendance from CSV to prevent duplicates across sessions."""
    today = datetime.now().strftime('%Y-%m-%d')
    existing = set()
    if os.path.exists(ATTENDANCE_CSV):
        df = pd.read_csv(ATTENDANCE_CSV)
        if not df.empty:
            for _, row in df.iterrows():
                name = row["Name"]
                timestamp = row["Timestamp"]
                if str(timestamp).startswith(today):
                    existing.add(name)
    return existing

def mark_attendance(name, existing_today):
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
    if name not in attendance_dict and name not in existing_today and name != "Unknown":
        attendance_dict[name] = dt_string
        print(f"Marked attendance for {name} at {dt_string}")
    elif name in existing_today:
        print(f"Attendance for {name} already marked today.")

def save_attendance_to_csv(filename=ATTENDANCE_CSV):
    # Append new attendance to CSV
    if attendance_dict:
        df_new = pd.DataFrame(list(attendance_dict.items()), columns=["Name", "Timestamp"])
        if os.path.exists(filename):
            df_existing = pd.read_csv(filename)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(filename, index=False)
        else:
            df_new.to_csv(filename, index=False)
        print(f"Attendance saved to {filename}")
    else:
        print("No new attendance to save.")

def show_summary():
    print("\n--- Attendance Session Summary ---")
    if attendance_dict:
        for name, timestamp in attendance_dict.items():
            print(f"{name}: {timestamp}")
        print(f"Total unique attendees this session: {len(attendance_dict)}")
    else:
        print("No new attendance marked this session.")

def recognize_and_mark_attendance():
    existing_today = load_existing_attendance()
    cap = cv2.VideoCapture(0)
    print("Starting real-time face recognition. Press 'q' to quit and save attendance.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Resize frame for faster processing
        frame_small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        gray_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_small, scaleFactor=1.1, minNeighbors=4)
        
        # Scale face coordinates back to original frame size
        for (x, y, w, h) in faces:
            x_big, y_big, w_big, h_big = [int(v * 2) for v in (x, y, w, h)]
            roi_gray = cv2.cvtColor(frame[y_big:y_big+h_big, x_big:x_big+w_big], cv2.COLOR_BGR2GRAY)
            try:
                label, confidence = recognizer.predict(roi_gray)
            except:
                continue
            if confidence < 70:
                name = label_dict.get(label, "Unknown")
                print(f"Recognized: {name} (confidence: {confidence})")
                mark_attendance(name, existing_today)
                color = (0, 255, 0)
            else:
                name = "Unknown"
                print("Face not recognized.")
                color = (0, 0, 255)
            cv2.rectangle(frame, (x_big, y_big), (x_big+w_big, y_big+h_big), color, 2)
            cv2.putText(frame, name, (x_big, y_big-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.imshow("Attendance - Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    save_attendance_to_csv()
    show_summary()

if __name__ == "__main__":
    recognize_and_mark_attendance()

# Instructions:
# - Ensure 'haarcascade_frontalface_default.xml', 'trainer.yml', and 'labels.npy' are in the same directory or update the paths.
# - Press 'q' to quit and save attendance.
# - The attendance will be saved in 'attendance.csv'.
# - No duplicate attendance for the same person per day, even across multiple runs.
# - A summary of the session will be printed at the end.
