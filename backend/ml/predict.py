import os
import numpy as np
from PIL import Image
import tensorflow as tf

# reduce TensorFlow logging spam in terminal
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')
# set Keras logger to error only
tf.get_logger().setLevel('ERROR')

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.h5")

# Global model variable - lazy loaded
_model = None
labels = ["PET", "HDPE", "PVC"]

TRAIN_DATA_DIR = os.path.join(os.path.dirname(__file__), "dataset")

def build_model():
    """Build a fresh model."""
    print("Building a fresh model...")
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(128, 128, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False

    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(3, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


def train_model(model):
    """Train model on built-in dataset if pre-trained weights are unavailable."""
    if not os.path.exists(TRAIN_DATA_DIR):
        raise FileNotFoundError(f"Training data folder not found: {TRAIN_DATA_DIR}")

    print("Training model from dataset -- this may take a few minutes")
    train_data = tf.keras.preprocessing.image_dataset_from_directory(
        TRAIN_DATA_DIR,
        image_size=(128, 128),
        batch_size=16
    )

    model.fit(train_data, epochs=5, verbose=1)
    model.save(MODEL_PATH)

    return model

def get_model():
    """Get or load the model lazily; train if none exists."""
    global _model

    if _model is not None:
        return _model

    # Try to load existing model
    if os.path.exists(MODEL_PATH):
        try:
            print(f"Loading model from {MODEL_PATH}")
            _model = tf.keras.models.load_model(MODEL_PATH)
            return _model
        except Exception as e:
            print(f"Saved model load failure: {type(e).__name__}: {e}")

    # Build + train from dataset
    print("Saved model unavailable or invalid. Rebuilding and training a new model.")
    _model = build_model()
    _model = train_model(_model)
    return _model

def predict_plastic_type(image_file):
    """Predict the plastic type from an image file."""
    model = get_model()
    
    img = Image.open(image_file).resize((128, 128))
    img = np.array(img) / 255.0
    
    # Handle grayscale images by converting to RGB
    if len(img.shape) == 2:
        img = np.stack([img] * 3, axis=-1)
    elif img.shape[2] == 4:  # RGBA
        img = img[:, :, :3]
    
    img = np.expand_dims(img, axis=0)
    
    prediction = model.predict(img, verbose=0)[0]
    predicted_index = int(np.argmax(prediction))
    predicted_confidence = float(np.max(prediction))

    # Avoid blind invalid predictions from an untrained/low-confidence model
    if predicted_confidence < 0.50:
        raise RuntimeError(f"Low ML confidence ({predicted_confidence:.2f}); please use a clearer image or retrain model.")

    return labels[predicted_index]
