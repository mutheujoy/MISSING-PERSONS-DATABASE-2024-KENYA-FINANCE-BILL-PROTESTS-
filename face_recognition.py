import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load pre-trained face detection model and custom facial recognition model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognition_model = load_model('path/to/your/recognition_model.h5')

def detect_faces(image_path):
    """Detect faces in an image."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return faces, img

def recognize_face(image_path):
    """Recognize face using the custom recognition model."""
    faces, img = detect_faces(image_path)
    results = []

    for (x, y, w, h) in faces:
        face = img[y:y+h, x:x+w]
        face = cv2.resize(face, (224, 224))
        face = face / 255.0  # Normalize pixel values
        face = np.expand_dims(face, axis=0)
        
        prediction = recognition_model.predict(face)
        results.append(prediction)

    return results

def process_face_recognition(image_path):
    """Process image for face recognition and return results."""
    results = recognize_face(image_path)
    return results


# results = process_face_recognition('path/to/image.jpg')
# print(results)
