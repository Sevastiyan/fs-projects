from tensorflow import keras

def TS_CNN():
    signal_length = 200
    r = 0.2
    input_layer = keras.layers.Input(shape=(int(signal_length), 1))

    conv1 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(input_layer)
    conv1 = keras.layers.BatchNormalization()(conv1)
    conv1 = keras.layers.LeakyReLU(alpha=0.15)(conv1)
    conv1 = keras.layers.Dropout(rate=r)(conv1)

    conv2 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv1)
    conv2 = keras.layers.BatchNormalization()(conv2)
    conv2 = keras.layers.LeakyReLU(alpha=0.15)(conv2)
    conv2 = keras.layers.Dropout(rate=r)(conv2)

    conv3 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv2)
    conv3 = keras.layers.BatchNormalization()(conv3)
    conv3 = keras.layers.LeakyReLU(alpha=0.15)(conv3)
    conv3 = keras.layers.Dropout(rate=r)(conv3)

    gap = keras.layers.GlobalAveragePooling1D()(conv3)

    output_layer = keras.layers.Dense(2, activation="softmax")(gap)

    return keras.models.Model(inputs=input_layer, outputs=output_layer)


def TS_CNN_2():
    signal_length = 200
    r = 0.2
    input_layer = keras.layers.Input(shape=(int(signal_length), 2))

    conv1 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(input_layer)
    conv1 = keras.layers.BatchNormalization()(conv1)
    conv1 = keras.layers.LeakyReLU(alpha=0.15)(conv1)
    conv1 = keras.layers.Dropout(rate=r)(conv1)

    conv2 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv1)
    conv2 = keras.layers.BatchNormalization()(conv2)
    conv2 = keras.layers.LeakyReLU(alpha=0.15)(conv2)
    conv2 = keras.layers.Dropout(rate=r)(conv2)

    conv3 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv2)
    conv3 = keras.layers.BatchNormalization()(conv3)
    conv3 = keras.layers.LeakyReLU(alpha=0.15)(conv3)
    conv3 = keras.layers.Dropout(rate=r)(conv3)

    gap = keras.layers.GlobalAveragePooling1D()(conv3)

    output_layer = keras.layers.Dense(2, activation="softmax")(gap)

    return keras.models.Model(inputs=input_layer, outputs=output_layer)



def MULTI_TS_CNN():
    signal_length = 200
    r = 0.2
    input_1 = keras.layers.Input(shape=(int(signal_length), 1))
    input_2 = keras.layers.Input(shape=(int(signal_length), 1))
    merge = keras.layers.Concatenate()([input_1, input_2])

    conv1 = keras.layers.Conv1D(input_dim=2, filters=64, kernel_size=5, padding="same")(merge)
    conv1 = keras.layers.BatchNormalization()(conv1)
    conv1 = keras.layers.LeakyReLU(alpha=0.15)(conv1)
    conv1 = keras.layers.Dropout(rate=r)(conv1)

    conv2 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv1)
    conv2 = keras.layers.BatchNormalization()(conv2)
    conv2 = keras.layers.LeakyReLU(alpha=0.15)(conv2)
    conv2 = keras.layers.Dropout(rate=r)(conv2)

    conv3 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv2)
    conv3 = keras.layers.BatchNormalization()(conv3)
    conv3 = keras.layers.LeakyReLU(alpha=0.15)(conv3)
    conv3 = keras.layers.Dropout(rate=r)(conv3)

    conv4 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv3)
    conv4 = keras.layers.BatchNormalization()(conv4)
    conv4 = keras.layers.LeakyReLU(alpha=0.15)(conv4)
    conv4 = keras.layers.Dropout(rate=r)(conv4)

    gap = keras.layers.GlobalAveragePooling1D()(conv4)

    output_layer = keras.layers.Dense(2, activation="softmax")(gap)

    return keras.models.Model(inputs=[input_1, input_2], outputs=output_layer)


def MULTI_CLASS_TS_CNN_22():
    signal_length = 200
    r = 0.2
    input_1 = keras.layers.Input(shape=(int(signal_length), 1))
    input_2 = keras.layers.Input(shape=(int(signal_length), 1))
    merge = keras.layers.Concatenate()([input_1, input_2])

    conv1 = keras.layers.Conv1D(input_dim=2, filters=64, kernel_size=5, padding="same")(merge)
    conv1 = keras.layers.BatchNormalization()(conv1)
    conv1 = keras.layers.LeakyReLU(alpha=0.15)(conv1)
    conv1 = keras.layers.Dropout(rate=r)(conv1)

    conv2 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv1)
    conv2 = keras.layers.BatchNormalization()(conv2)
    conv2 = keras.layers.LeakyReLU(alpha=0.15)(conv2)
    conv2 = keras.layers.Dropout(rate=r)(conv2)

    conv3 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv2)
    conv3 = keras.layers.BatchNormalization()(conv3)
    conv3 = keras.layers.LeakyReLU(alpha=0.15)(conv3)
    conv3 = keras.layers.Dropout(rate=r)(conv3)

    conv4 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv3)
    conv4 = keras.layers.BatchNormalization()(conv4)
    conv4 = keras.layers.LeakyReLU(alpha=0.15)(conv4)
    conv4 = keras.layers.Dropout(rate=r)(conv4)

    gap = keras.layers.GlobalAveragePooling1D()(conv4)

    output_layer = keras.layers.Dense(3, activation="softmax")(gap)

    return keras.models.Model(inputs=[input_1, input_2], outputs=output_layer)



def MULTI_CLASS_TS_CNN_23():
    signal_length = 200
    r = 0.1
    input_1 = keras.layers.Input(shape=(int(signal_length), 1))
    input_2 = keras.layers.Input(shape=(int(signal_length), 1))
    merge = keras.layers.Concatenate()([input_1, input_2])

    conv1 = keras.layers.Conv1D(input_dim=2, filters=64, kernel_size=5, padding="same")(merge)
    conv1 = keras.layers.BatchNormalization()(conv1)
    conv1 = keras.layers.LeakyReLU(alpha=0.15)(conv1)
    conv1 = keras.layers.Dropout(rate=r)(conv1)

    conv2 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv1)
    conv2 = keras.layers.BatchNormalization()(conv2)
    conv2 = keras.layers.LeakyReLU(alpha=0.15)(conv2)
    conv2 = keras.layers.Dropout(rate=r)(conv2)

    conv3 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv2)
    conv3 = keras.layers.BatchNormalization()(conv3)
    conv3 = keras.layers.LeakyReLU(alpha=0.15)(conv3)
    conv3 = keras.layers.Dropout(rate=r)(conv3)

    conv4 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv3)
    conv4 = keras.layers.BatchNormalization()(conv4)
    conv4 = keras.layers.LeakyReLU(alpha=0.15)(conv4)
    conv4 = keras.layers.Dropout(rate=r)(conv4)

    conv5 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv4)
    conv5 = keras.layers.BatchNormalization()(conv5)
    conv5 = keras.layers.LeakyReLU(alpha=0.15)(conv5)
    conv5 = keras.layers.Dropout(rate=r)(conv5)

    gap = keras.layers.GlobalAveragePooling1D()(conv5)

    output_layer = keras.layers.Dense(3, activation="softmax")(gap)

    return keras.models.Model(inputs=[input_1, input_2], outputs=output_layer)

