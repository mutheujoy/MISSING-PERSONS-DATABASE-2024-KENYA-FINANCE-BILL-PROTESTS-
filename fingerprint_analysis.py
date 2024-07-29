import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load custom fingerprint recognition model
fingerprint_model = load_model('path/to/your/fingerprint_model.h5')

def preprocess_fingerprint(image_path):
    """Preprocess fingerprint image for recognition."""
    img = cv2.imread(image_path, 0)  # Read as grayscale
    img = cv2.resize(img, (224, 224))
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=-1)
    img = np.expand_dims(img, axis=0)
    return img

def recognize_fingerprint(image_path):
    """Recognize fingerprint using the custom model."""
    fingerprint = preprocess_fingerprint(image_path)
    prediction = fingerprint_model.predict(fingerprint)
    return prediction

def process_fingerprint_recognition(image_path):
    """Process image for fingerprint recognition and return results."""
    results = recognize_fingerprint(image_path)
    return results


# results = process_fingerprint_recognition('path/to/fingerprint.jpg')
# print(results)
