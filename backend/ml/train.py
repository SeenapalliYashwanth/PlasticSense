import tensorflow as tf
from tensorflow.keras import layers, models

IMG_SIZE = (128, 128)

train_data = tf.keras.preprocessing.image_dataset_from_directory(
    "dataset",
    image_size=IMG_SIZE,
    batch_size=32
)

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(128,128,3),
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

model.fit(train_data, epochs=5)

model.save("model.h5")