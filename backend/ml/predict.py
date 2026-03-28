import os
import numpy as np
from PIL import Image
import tensorflow as tf

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

def _build_inference_model():
    """Rebuild the known training architecture and load weights only."""
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(*IMAGE_SIZE, 3),
        include_top=False,
        weights=None,
    )
    base_model.trainable = False

    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(3, activation="softmax"),
    ])

    # Build weights before loading from the H5 file.
    model(np.zeros((1, IMAGE_SIZE[0], IMAGE_SIZE[1], 3), dtype=np.float32))
    model.load_weights(MODEL_PATH)
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
    except Exception:
        try:
            _model = _build_inference_model()
        except Exception as fallback_exc:
            raise RuntimeError(
                "Model file could not be loaded in the current TensorFlow/Keras runtime, "
                "and rebuilding the known architecture from saved weights also failed."
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
