from tensorflow import keras


def DNN(length):
    dilation_rates = [2**i for i in range(6)]
    model_inputs = keras.Input(shape=(length, 4))
    x = model_inputs
    for dilation_rate in dilation_rates:
        layer_in = x
        x = keras.layers.Conv1D(filters=32, kernel_size=5, padding='same', dilation_rate = dilation_rate)(layer_in)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.LeakyReLU(alpha=0.15)(x)
        x = keras.layers.Dropout(0.1)(x)
        x = keras.layers.Concatenate()([x, layer_in])

    x = keras.layers.Dense(8, activation='relu')(x)
    out = keras.layers.Dense(units=1, activation='sigmoid', activity_regularizer=keras.regularizers.l2(0.001), name='out')(x)
    
    model = keras.Model(inputs=model_inputs, outputs=out, name='Simple_DCNN')

    return model
    