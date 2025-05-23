import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import cv2
import os

CASCADE_PATH = "haarcascade_frontalface_default.xml"
DATASET_DIR = "dataset"

class FaceCaptureApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("User Registration & Face Capture")
        self.geometry("500x300")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Register New User", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self, text="Enter Name:").pack()
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.pack(pady=5)
        tk.Button(self, text="Capture Face Images", width=25, command=self.capture_faces).pack(pady=10)
        self.log_area = scrolledtext.ScrolledText(self, width=60, height=8, state='disabled')
        self.log_area.pack(pady=5)
        tk.Button(self, text="Exit", width=20, command=self.destroy).pack(pady=5)

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def capture_faces(self):
        person_name = self.name_entry.get().strip()
        if not person_name:
            messagebox.showwarning("Input Error", "Please enter a name.")
            return
        person_dir = os.path.join(DATASET_DIR, person_name)
        os.makedirs(person_dir, exist_ok=True)
        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
        count = 0
        num_samples = 50
        self.log(f"Capturing images for {person_name}. Press 'q' to quit early.")
        while count < num_samples:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in faces:
                count += 1
                face_img = gray[y:y+h, x:x+w]
                img_path = os.path.join(person_dir, f"{person_name}_{count}.jpg")
                cv2.imwrite(img_path, face_img)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(frame, f"{count}/{num_samples}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            cv2.imshow("Capture Faces", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if count >= num_samples:
                break
        cap.release()
        cv2.destroyAllWindows()
        self.log(f"Saved {count} images to {person_dir}")
        messagebox.showinfo("Done", f"Saved {count} images for {person_name}.")

if __name__ == "__main__":
    app = FaceCaptureApp()
    app.mainloop()