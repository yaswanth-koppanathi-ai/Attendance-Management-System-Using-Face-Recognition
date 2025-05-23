# Attendance Management System using Face Recognition

## Overview

This Attendance Management System is a Python-based application that leverages face recognition technology to automate student attendance. It features a user-friendly GUI for both user registration (face image capture) and real-time attendance marking, using OpenCV and Tkinter. Attendance is stored in a CSV file for easy export and analysis.

---

## Features

- **Face Registration GUI:** Register new users and capture face images via webcam.
- **Training Script:** Train the face recognizer on your dataset.
- **Attendance GUI:** Real-time face recognition and attendance marking with session summary.
- **No duplicate attendance per day:** Each person is marked only once per day.
- **CSV Export:** Attendance records are saved in `attendance.csv`.
- **Optimized for speed:** Fast face detection and recognition.
- **User-friendly:** All interactions via Tkinter GUIs.

---

## Technologies Used

- Python 3.x
- OpenCV
- Tkinter
- NumPy
- Pandas

---

## Setup Instructions

1. **Clone the repository or download the source code.**

2. **Install dependencies:**
   ```bash
   pip install opencv-contrib-python numpy pandas
   ```

3. **Ensure these files are in your project directory:**
   - `haarcascade_frontalface_default.xml`
   - `face_capture_gui.py`
   - `train_recognizer.py`
   - `attendance_gui.py`
   - `trainer.yml` and `labels.npy` (generated after training)

---

## Usage

### 1. Register Users (Face Image Capture)
```bash
python face_capture_gui.py
```
- Enter the user's name and capture face images (50 per user recommended).

### 2. Train the Recognizer
```bash
python train_recognizer.py
```
- This will generate `trainer.yml` and `labels.npy`.

### 3. Mark Attendance (Real-Time Recognition)
```bash
python attendance_gui.py
```
- Click "Start Attendance" to begin.
- Recognized faces are marked in `attendance.csv` (no duplicates per day).
- Click "Stop Attendance" or close the webcam window to finish.
- View session summary in the GUI.

---

## Attendance CSV Format

| Name      | Timestamp           |
|-----------|---------------------|
| John Doe  | 2024-06-09 09:15:23 |
| Jane Doe  | 2024-06-09 09:16:10 |

---

## Screenshots

*(Add screenshots of your GUIs here for extra polish!)*

---

## Credits

- OpenCV for face detection and recognition
- Tkinter for GUI
- NumPy and Pandas for data handling

---

## License

MIT License
