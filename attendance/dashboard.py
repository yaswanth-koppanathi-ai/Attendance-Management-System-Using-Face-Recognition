import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, ttk
import subprocess
import os
import pandas as pd
import threading

# Paths to scripts
CAPTURE_SCRIPT = "capture_faces.py"
TRAIN_SCRIPT = "train_recognizer.py"
ATTENDANCE_SCRIPT = "real_time_face_recognition.py"
ATTENDANCE_CSV = "attendance.csv"

class AttendanceDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Attendance Management System")
        self.geometry("600x420")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Attendance Management System", font=("Arial", 18, "bold")).pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Capture Face Images", width=25, command=self.capture_faces).grid(row=0, column=0, pady=5)
        tk.Button(btn_frame, text="Train Recognizer", width=25, command=self.train_recognizer).grid(row=1, column=0, pady=5)
        tk.Button(btn_frame, text="Start Attendance", width=25, command=self.start_attendance).grid(row=2, column=0, pady=5)
        tk.Button(btn_frame, text="Export Attendance (CSV)", width=25, command=self.export_attendance).grid(row=3, column=0, pady=5)
        tk.Button(btn_frame, text="View Attendance History", width=25, command=self.view_attendance_history).grid(row=4, column=0, pady=5)
        tk.Button(btn_frame, text="Exit", width=25, command=self.quit).grid(row=5, column=0, pady=5)

        tk.Label(self, text="Status / Log:", font=("Arial", 12, "bold")).pack(pady=(20, 0))
        self.log_area = scrolledtext.ScrolledText(self, width=70, height=8, state='disabled')
        self.log_area.pack(pady=5)

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def run_script_with_log(self, command, input_text=None):
        def target():
            try:
                process = subprocess.Popen(
                    ['python', command],
                    stdin=subprocess.PIPE if input_text else None,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                if input_text:
                    process.stdin.write(input_text)
                    process.stdin.flush()
                    process.stdin.close()
                for line in process.stdout:
                    self.log(line.rstrip())
                process.stdout.close()
                process.wait()
                self.log(f"Process finished with exit code {process.returncode}")
            except Exception as e:
                self.log(f"Error running {command}: {e}")

        threading.Thread(target=target, daemon=True).start()

    def capture_faces(self):
        name = simpledialog.askstring("Input", "Enter the person's name:")
        if name:
            self.log(f"Capturing faces for {name}...")
            self.run_script_with_log(CAPTURE_SCRIPT, input_text=f"{name}\n")

    def train_recognizer(self):
        self.log("Training recognizer...")
        self.run_script_with_log(TRAIN_SCRIPT)

    def start_attendance(self):
        self.log("Starting real-time attendance. Close the webcam window to finish.")
        self.run_script_with_log(ATTENDANCE_SCRIPT)

    def export_attendance(self):
        if os.path.exists(ATTENDANCE_CSV):
            self.log(f"Attendance exported to {ATTENDANCE_CSV}")
            messagebox.showinfo("Export", f"Attendance exported to {ATTENDANCE_CSV}")
        else:
            self.log("No attendance file found to export.")
            messagebox.showwarning("Export", "No attendance file found to export.")
            
    def view_attendance_history(self):
        if not os.path.exists(ATTENDANCE_CSV):
            messagebox.showwarning("No Data", "No attendance file found to display.")
            return
        try:
            df = pd.read_csv(ATTENDANCE_CSV)
            win = tk.Toplevel(self)
            win.title("Attendance History")
            win.geometry("450x300")
            tree = ttk.Treeview(win)
            tree.pack(expand=True, fill='both')
            tree["columns"] = list(df.columns)
            tree["show"] = "headings"
            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            for _, row in df.iterrows():
                tree.insert("", "end", values=list(row))
        except Exception as e:
            messagebox.showerror("Error", f"Could not load attendance history: {e}")

if __name__ == "__main__":
    app = AttendanceDashboard()
    app.mainloop()
