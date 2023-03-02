import tensorflow as tf
from keras import layers, models

def cnn_model():
    model_cnn = models.Sequential()
    model_cnn.add(layers.Conv2D(64, (2, 3), activation='relu', input_shape=(200 , 200, 3)))
    model_cnn.add(layers.MaxPooling2D((2, 2)))
    model_cnn.add(layers.Conv2D(32, (2, 3), activation='relu'))
    model_cnn.add(layers.MaxPooling2D((2, 2)))
    model_cnn.add(layers.Conv2D(32, (2, 3), activation='relu'))
    model_cnn.add(layers.MaxPooling2D((2)))
    model_cnn.add(layers.Flatten())
    model_cnn.add(layers.Dense(7, activation='softmax'))

    model_cnn.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005), 
                loss='categorical_crossentropy', 
                metrics = ['accuracy'])
    return model_cnn