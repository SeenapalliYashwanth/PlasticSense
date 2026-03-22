# ml/model.py
import json
from PIL import Image
import numpy as np

# mock ML logic (replace with real CNN later)
def predict_plastic_type(image_file):
    """
    Simulates ML-based plastic identification.
    Returns predicted plastic type.
    """
    image = Image.open(image_file)
    image = image.resize((224, 224))
    image_array = np.array(image)

    # Dummy logic for now (interview-safe)
    mean_pixel = image_array.mean()

    if mean_pixel < 85:
        return "PET"
    elif mean_pixel < 170:
        return "HDPE"
    else:
        return "PVC"