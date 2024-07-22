import tensorflow as tf
from tensorflow.keras.models import load_model
import spacy

# Load pre-trained models
nlp = spacy.load('en_core_web_sm')
model = load_model('path/to/your/model.h5')

def extract_entities(text):
    """Extract entities from text using NLP."""
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def classify_image(image_path):
    """Classify image using the deep learning model."""
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = tf.expand_dims(image, 0)
    
    predictions = model.predict(image)
    return predictions
