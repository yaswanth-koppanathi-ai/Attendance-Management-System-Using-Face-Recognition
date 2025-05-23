import cv2
import os

CASCADE_PATH = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def capture_images(person_name, save_dir="dataset", num_samples=50):
    person_dir = os.path.join(save_dir, person_name)
    os.makedirs(person_dir, exist_ok=True)
    cap = cv2.VideoCapture(0)
    count = 0
    print(f"Capturing images for {person_name}. Press 'q' to quit early.")
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
    print(f"Saved {count} images to {person_dir}")

if __name__ == "__main__":
    name = input("Enter the person's name: ")
    capture_images(name)