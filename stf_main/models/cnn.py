from tensorflow import keras

def CNN(length):
    """
    CNN.
    
    Args:  
        length : int -- length of the input sequence
    """
    model_inputs = keras.Input(shape=(length, 4))
    x = keras.layers.Conv1D(filters=8, kernel_size=3, padding='same', input_shape=(length, 4))(model_inputs)

    x = keras.layers.Conv1D(filters=16, kernel_size=3, padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.LeakyReLU(alpha=0.15)(x)
    x = keras.layers.Dropout(0.1)(x)
    x = keras.layers.MaxPooling1D(2, 2, padding='same')(x)

    x = keras.layers.Conv1D(filters=16, kernel_size=3, padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.LeakyReLU(alpha=0.15)(x)
    x = keras.layers.Dropout(0.1)(x)
    x = keras.layers.MaxPooling1D(2, 2, padding='same')(x)

    x = keras.layers.Conv1D(filters=32, kernel_size=3, padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.LeakyReLU(alpha=0.15)(x)
    x = keras.layers.Dropout(0.1)(x)
    x = keras.layers.MaxPooling1D(2, 2, padding='same')(x)

    x = keras.layers.Conv1D(filters=32, kernel_size=3, padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.LeakyReLU(alpha=0.15)(x)
    x = keras.layers.Dropout(0.1)(x)
    x = keras.layers.MaxPooling1D(3, 3, padding='same')(x) 

    x = keras.layers.Conv1D(filters=64, kernel_size=3, padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.LeakyReLU(alpha=0.15)(x)
    x = keras.layers.Dropout(0.1)(x)
    x = keras.layers.MaxPooling1D(4, 4, padding='same')(x)

    x = keras.layers.Conv1D(filters=64, kernel_size=3, padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.LeakyReLU(alpha=0.15)(x)
    x = keras.layers.Dropout(0.1)(x)
    # x = keras.layers.MaxPooling1D(5, 5, padding='same')(x)

    x = keras.layers.Dense(16, activation='relu')(x)
    out = keras.layers.Dense(units=1, activation='sigmoid', activity_regularizer=keras.regularizers.l2(0.001), name='out')(x)
    
    model = keras.Model(inputs=model_inputs, outputs=out, name='Simple_CNN')

    return model
    