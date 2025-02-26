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

    conv1 = keras.layers.Conv1D(input_dim=2, filters=64, kernel_size=5, padding="same")(
        merge
    )
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

    conv1 = keras.layers.Conv1D(input_dim=2, filters=64, kernel_size=5, padding="same")(
        merge
    )
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

    conv1 = keras.layers.Conv1D(input_dim=2, filters=64, kernel_size=5, padding="same")(
        merge
    )
    conv1 = keras.layers.BatchNormalization()(conv1)
    conv1 = keras.layers.LeakyReLU(alpha=0.15)(conv1)
    conv1 = keras.layers.Dropout(rate=r)(conv1)

    conv2 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv1)
    conv2 = keras.layers.BatchNormalization()(conv2)
    conv2 = keras.layers.LeakyReLU(alpha=0.15)(conv2)
    conv2 = keras.layers.Dropout(rate=r)(conv2)

    conv3 = keras.layers.Conv1D(filters=128, kernel_size=5, padding="same")(conv2)
    conv3 = keras.layers.BatchNormalization()(conv3)
    conv3 = keras.layers.LeakyReLU(alpha=0.15)(conv3)
    conv3 = keras.layers.Dropout(rate=r)(conv3)

    conv4 = keras.layers.Conv1D(filters=128, kernel_size=5, padding="same")(conv3)
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


def MULTI_CLASS_TS_RNN():
    signal_length = 200
    r = 0.2  # Increased dropout for better regularization

    # Input layers
    input_1 = keras.layers.Input(shape=(signal_length, 1))
    input_2 = keras.layers.Input(shape=(signal_length, 1))
    merge = keras.layers.Concatenate()([input_1, input_2])

    # First block with smaller kernel for local patterns
    conv1 = keras.layers.Conv1D(filters=32, kernel_size=3, padding="same")(merge)
    conv1 = keras.layers.BatchNormalization()(conv1)
    conv1 = keras.layers.ReLU()(conv1)
    conv1 = keras.layers.MaxPooling1D(pool_size=2)(conv1)
    conv1 = keras.layers.Dropout(rate=r)(conv1)

    # Second block with residual connection
    conv2 = keras.layers.Conv1D(filters=64, kernel_size=5, padding="same")(conv1)
    conv2 = keras.layers.BatchNormalization()(conv2)
    conv2 = keras.layers.ReLU()(conv2)
    conv2 = keras.layers.MaxPooling1D(pool_size=2)(conv2)
    conv2 = keras.layers.Dropout(rate=r)(conv2)

    # Third block with larger kernel for temporal patterns
    conv3 = keras.layers.Conv1D(filters=128, kernel_size=7, padding="same")(conv2)
    conv3 = keras.layers.BatchNormalization()(conv3)
    conv3 = keras.layers.ReLU()(conv3)
    conv3 = keras.layers.Dropout(rate=r)(conv3)

    # Add residual connection
    res_connection = keras.layers.Conv1D(filters=128, kernel_size=1)(conv2)
    conv3 = keras.layers.Add()([conv3, res_connection])

    # Global pooling and output
    gap = keras.layers.GlobalAveragePooling1D()(conv3)
    dense = keras.layers.Dense(64, activation="relu")(gap)
    output_layer = keras.layers.Dense(3, activation="softmax")(dense)

    return keras.models.Model(inputs=[input_1, input_2], outputs=output_layer)


def ATTENTION_MODEL_TS_CNN(
    signal_length=200, filters=64, kernel_size=5, dropout_rate=0.1
):
    """
    Multi-class time series CNN with residual connections and attention mechanism.

    Args:
        signal_length: Length of input signals
        filters: Number of convolutional filters
        kernel_size: Size of convolution kernel
        dropout_rate: Dropout rate for regularization
    """
    # Input layers
    input_1 = keras.layers.Input(shape=(signal_length, 1))
    input_2 = keras.layers.Input(shape=(signal_length, 1))
    merge = keras.layers.Concatenate()([input_1, input_2])

    # Initial convolution
    x = keras.layers.Conv1D(
        filters=filters,
        kernel_size=kernel_size,
        padding="same",
        kernel_regularizer=keras.regularizers.l2(1e-4),
    )(merge)

    # Residual blocks
    for i in range(5):
        # Residual connection
        residual = x

        # Convolution block
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.Activation("swish")(x)
        x = keras.layers.Conv1D(
            filters=filters,
            kernel_size=kernel_size,
            padding="same",
            kernel_regularizer=keras.regularizers.l2(1e-4),
        )(x)
        x = keras.layers.Dropout(rate=dropout_rate)(x)

        # Add attention mechanism
        attention = keras.layers.GlobalAveragePooling1D()(x)
        attention = keras.layers.Dense(filters, activation="sigmoid")(attention)
        attention = keras.layers.Reshape((1, filters))(attention)
        x = keras.layers.Multiply()([x, attention])

        # Add residual
        x = keras.layers.Add()([x, residual])

    # Global pooling with attention
    gap = keras.layers.GlobalAveragePooling1D()(x)

    # Classification head
    x = keras.layers.Dense(32, activation="swish")(gap)
    x = keras.layers.Dropout(dropout_rate / 2)(x)
    output_layer = keras.layers.Dense(3, activation="softmax")(x)

    model = keras.models.Model(inputs=[input_1, input_2], outputs=output_layer)

    # Use learning rate schedule
    initial_learning_rate = 0.001
    lr_schedule = keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate, decay_steps=1000, decay_rate=0.9
    )

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=lr_schedule),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model
