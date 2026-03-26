import tensorflow as tf
from tensorflow.keras import layers, models
import os

IMG_SIZE = (128, 128)

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(script_dir, "dataset")

print(f"Loading dataset from: {dataset_path}")

train_data = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_path,
    image_size=IMG_SIZE,
    batch_size=32
)

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(128, 128, 3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dense(3, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("Training model...")
model.fit(train_data, epochs=5, verbose=1)

model_path = os.path.join(script_dir, "model.h5")
print(f"Saving model to: {model_path}")
model.save(model_path)
print("Model training complete!")