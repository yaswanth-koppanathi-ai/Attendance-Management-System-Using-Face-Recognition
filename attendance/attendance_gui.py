import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import os

CASCADE_PATH = "haarcascade_frontalface_default.xml"
RECOGNIZER_PATH = "trainer.yml"
LABELS_PATH = "labels.npy"
ATTENDANCE_CSV = "attendance.csv"

class AttendanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Face Recognition Attendance System")
        self.geometry("600x400")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.running = False
        self.create_widgets()

        # Load models and labels
        self.face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(RECOGNIZER_PATH)
        if os.path.exists(LABELS_PATH):
            self.label_dict = np.load(LABELS_PATH, allow_pickle=True).item()
        else:
            self.label_dict = {}

    def create_widgets(self):
        tk.Label(self, text="Attendance System", font=("Arial", 18, "bold")).pack(pady=10)
        self.start_btn = tk.Button(self, text="Start Attendance", width=20, command=self.start_attendance)
        self.start_btn.pack(pady=10)
        self.stop_btn = tk.Button(self, text="Stop Attendance", width=20, command=self.stop_attendance, state='disabled')
        self.stop_btn.pack(pady=5)
        self.log_area = scrolledtext.ScrolledText(self, width=70, height=12, state='disabled')
        self.log_area.pack(pady=10)
        tk.Button(self, text="Exit", width=20, command=self.on_close).pack(pady=5)

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def start_attendance(self):
        self.running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.log("Starting real-time face recognition. Close webcam window or click 'Stop Attendance' to finish.")
        threading.Thread(target=self.recognize_and_mark_attendance, daemon=True).start()

    def stop_attendance(self):
        self.running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.log("Stopping attendance...")

    def on_close(self):
        self.running = False
        self.destroy()

    def load_existing_attendance(self):
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

    def save_attendance_to_csv(self, attendance_dict):
        if attendance_dict:
            df_new = pd.DataFrame(list(attendance_dict.items()), columns=["Name", "Timestamp"])
            if os.path.exists(ATTENDANCE_CSV):
                df_existing = pd.read_csv(ATTENDANCE_CSV)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                df_combined.to_csv(ATTENDANCE_CSV, index=False)
            else:
                df_new.to_csv(ATTENDANCE_CSV, index=False)
            self.log(f"Attendance saved to {ATTENDANCE_CSV}")
        else:
            self.log("No new attendance to save.")

    def recognize_and_mark_attendance(self):
        attendance_dict = {}
        existing_today = self.load_existing_attendance()
        cap = cv2.VideoCapture(0)
        self.log("Webcam started.")
        while self.running:
            ret, frame = cap.read()
            if not ret:
                self.log("Failed to capture frame from webcam.")
                break
            frame_small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            gray_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray_small, scaleFactor=1.1, minNeighbors=4)
            for (x, y, w, h) in faces:
                x_big, y_big, w_big, h_big = [int(v * 2) for v in (x, y, w, h)]
                roi_gray = cv2.cvtColor(frame[y_big:y_big+h_big, x_big:x_big+w_big], cv2.COLOR_BGR2GRAY)
                try:
                    label, confidence = self.recognizer.predict(roi_gray)
                except:
                    continue
                if confidence < 70:
                    name = self.label_dict.get(label, "Unknown")
                    if name not in attendance_dict and name not in existing_today and name != "Unknown":
                        now = datetime.now()
                        dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
                        attendance_dict[name] = dt_string
                        self.log(f"Marked attendance for {name} at {dt_string}")
                    elif name in existing_today:
                        self.log(f"Attendance for {name} already marked today.")
                    color = (0, 255, 0)
                else:
                    name = "Unknown"
                    color = (0, 0, 255)
                cv2.rectangle(frame, (x_big, y_big), (x_big+w_big, y_big+h_big), color, 2)
                cv2.putText(frame, name, (x_big, y_big-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.imshow("Attendance - Face Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.log("Webcam window closed by user.")
                break
        cap.release()
        cv2.destroyAllWindows()
        self.save_attendance_to_csv(attendance_dict)
        self.show_summary(attendance_dict)
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')

    def show_summary(self, attendance_dict):
        self.log("\n--- Attendance Session Summary ---")
        if attendance_dict:
            for name, timestamp in attendance_dict.items():
                self.log(f"{name}: {timestamp}")
            self.log(f"Total unique attendees this session: {len(attendance_dict)}")
        else:
            self.log("No new attendance marked this session.")

if __name__ == "__main__":
    app = AttendanceApp()
    app.mainloop()