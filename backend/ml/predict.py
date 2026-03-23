import tensorflow as tf
import numpy as np
from PIL import Image
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.h5")

model = tf.keras.models.load_model(MODEL_PATH)

labels = ["PET", "HDPE", "PVC"]

def predict_plastic_type(image_file):
    img = Image.open(image_file).resize((128,128))
    img = np.array(img)/255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    return labels[np.argmax(prediction)]