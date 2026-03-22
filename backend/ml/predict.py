from PIL import Image
import numpy as np

def predict_plastic_type(image_file):
    image = Image.open(image_file)
    image = image.resize((224, 224))
    image_array = np.array(image)

    # Simple placeholder ML logic
    mean_pixel = image_array.mean()

    if mean_pixel < 85:
        return "PET"
    elif mean_pixel < 170:
        return "HDPE"
    else:
        return "PVC"