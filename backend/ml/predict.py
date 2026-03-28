import os
import json
import numpy as np
from PIL import Image
import tensorflow as tf
import h5py

# reduce TensorFlow logging spam in terminal
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')
# set Keras logger to error only
tf.get_logger().setLevel('ERROR')

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.h5")
IMAGE_SIZE = (128, 128)
CONFIDENCE_THRESHOLD = 0.50

# Global model variable - lazy loaded
_model = None
labels = ["PET", "HDPE", "PVC"]


def _strip_unsupported_config(value):
    """Recursively remove config keys unsupported by the deployed Keras runtime."""
    if isinstance(value, dict):
        return {
            key: _strip_unsupported_config(inner_value)
            for key, inner_value in value.items()
            if key != "quantization_config"
        }
    if isinstance(value, list):
        return [_strip_unsupported_config(item) for item in value]
    return value


def _load_h5_model_without_quant_config(model_path):
    """Load legacy H5 models by stripping unsupported quantization config fields."""
    with h5py.File(model_path, "r") as h5_file:
        model_config = h5_file.attrs.get("model_config")

    if model_config is None:
        raise RuntimeError("model_config metadata is missing from the H5 model file.")

    if isinstance(model_config, bytes):
        model_config = model_config.decode("utf-8")

    cleaned_config = _strip_unsupported_config(json.loads(model_config))
    model = tf.keras.models.model_from_json(json.dumps(cleaned_config))
    model.load_weights(model_path)
    return model

def get_model():
    """Load the saved inference model lazily."""
    global _model

    if _model is not None:
        return _model

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Saved model not found at {MODEL_PATH}. The deployed app expects a pre-trained model file."
        )

    print(f"Loading model from {MODEL_PATH}")
    try:
        _model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    except TypeError:
        # Older/newer Keras builds vary in supported load_model kwargs.
        _model = tf.keras.models.load_model(MODEL_PATH)
    except Exception as exc:
        try:
            _model = _load_h5_model_without_quant_config(MODEL_PATH)
        except Exception as fallback_exc:
            raise RuntimeError(
                "Model file could not be loaded in the current TensorFlow/Keras runtime. "
                "This is usually a version compatibility issue, not a missing frontend/backend file."
            ) from fallback_exc
    return _model


def warmup_model():
    """Load the model and run one tiny inference to reduce first-request latency."""
    model = get_model()
    dummy_input = np.zeros((1, IMAGE_SIZE[0], IMAGE_SIZE[1], 3), dtype=np.float32)
    model.predict(dummy_input, verbose=0)


def _prepare_image(image_file):
    """Convert uploads to a small RGB tensor for faster inference."""
    image = Image.open(image_file).convert("RGB")
    image = image.resize(IMAGE_SIZE, Image.Resampling.BILINEAR)
    image_array = np.asarray(image, dtype=np.float32) / 255.0
    return np.expand_dims(image_array, axis=0)

def predict_plastic_type(image_file):
    """Predict the plastic type from an image file."""
    model = get_model()

    image_tensor = _prepare_image(image_file)
    prediction = model.predict(image_tensor, verbose=0)[0]
    predicted_index = int(np.argmax(prediction))
    predicted_confidence = float(np.max(prediction))

    # Avoid blind invalid predictions from an untrained/low-confidence model
    if predicted_confidence < CONFIDENCE_THRESHOLD:
        raise RuntimeError(f"Low ML confidence ({predicted_confidence:.2f}); please use a clearer image or retrain model.")

    return labels[predicted_index]
