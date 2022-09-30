from tensorflow import keras


def UNET(length):
    drop_rate = 0.1
    kernel_size = [9] #[7,9,11]
    filter_size = [4,8,16,32,64,128,64,32,16,8,4]

    model_inputs = keras.Input(shape=(int(length), 1))

    x = keras.layers.Conv1D(filters=filter_size[2], kernel_size=kernel_size, padding='same', activation=None, input_shape=(int(signal_length), 1))(model_inputs)
    # out1 = x
    # x = keras.layers.MaxPooling1D(2, 2, padding='valid')(x)
    # x = keras.layers.Dropout(rate = drop_rate) (x)

    # x = keras.layers.Conv1D(filters=filter_size[1], kernel_size=kernel_size, activation=None, padding='same')(x)
    # x = keras.layers.LeakyReLU(alpha=0.15)(x)
    # out2 = x
    # x = keras.layers.MaxPooling1D(2, 2, padding='valid')(x)
    # x = keras.layers.Dropout(rate = drop_rate) (x)

    # x = keras.layers.Conv1D(filters=filter_size[2], kernel_size=kernel_size, activation=None, padding='same')(x)
    # x = keras.layers.LeakyReLU(alpha=0.15)(x)
    out3 = x
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.MaxPooling1D(2, 2, padding='valid')(x)
    x = keras.layers.Dropout(rate = drop_rate) (x)

    x = keras.layers.Conv1D(filters=filter_size[3], kernel_size=kernel_size,
                            #kernel_regularizer=tf.keras.regularizers.l2(0.01), 
                            activation=None, padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.LeakyReLU(alpha=0.15)(x)
    out4 = x
    x = keras.layers.MaxPooling1D(5, 5, padding='valid')(x)
    x = keras.layers.Dropout(rate = drop_rate) (x)

    x = keras.layers.Conv1D(filters=filter_size[4], kernel_size=kernel_size,
                            #kernel_regularizer=tf.keras.regularizers.l2(0.01), 
                            activation=None, padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.LeakyReLU(alpha=0.15)(x)
    out5 = x
    x = keras.layers.MaxPooling1D(5, 5, padding='valid')(x)
    x = keras.layers.Dropout(rate = drop_rate) (x)
    

    x = keras.layers.Conv1D(filters=filter_size[5], kernel_size=kernel_size, 
                            #kernel_regularizer=tf.keras.regularizers.l2(0.01), 
                            activation=None, padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.LeakyReLU(alpha=0.15)(x)
    x = keras.layers.Dropout(rate = drop_rate) (x)


    x = keras.layers.UpSampling1D(5)(x)
    x = keras.layers.Concatenate()([x, out5])
    x = keras.layers.Conv1D(filters=filter_size[6], kernel_size=kernel_size, 
                            #kernel_regularizer=tf.keras.regularizers.l2(0.01), 
                            activation=None, padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.LeakyReLU(alpha=0.15)(x)
    x = keras.layers.Dropout(rate = drop_rate) (x)

    x = keras.layers.UpSampling1D(5)(x)
    x = keras.layers.Concatenate()([x, out4])
    x = keras.layers.Conv1D(filters=filter_size[7], kernel_size=kernel_size, 
                            #kernel_regularizer=tf.keras.regularizers.l2(0.01), 
                            activation=None, padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.LeakyReLU(alpha=0.15)(x)
    x = keras.layers.Dropout(rate = drop_rate) (x)

    x = keras.layers.UpSampling1D(2)(x)
    x = keras.layers.Concatenate()([x, out3])
    x = keras.layers.Conv1D(filters=filter_size[8], kernel_size=kernel_size,
                            #kernel_regularizer=tf.keras.regularizers.l2(0.01), 
                            activation=None, padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.LeakyReLU(alpha=0.15)(x)
    x = keras.layers.Dropout(rate = drop_rate) (x)

    # x = keras.layers.UpSampling1D(2)(x)
    # x = keras.layers.Concatenate()([x, out2])
    # x = keras.layers.Conv1D(filters=filter_size[9], kernel_size=kernel_size, activation=None, padding='same')(x)
    # x = keras.layers.LeakyReLU(alpha=0.15)(x)
    # x = keras.layers.Dropout(rate = drop_rate) (x)

    # x = keras.layers.UpSampling1D(2)(x)
    # x = keras.layers.Concatenate()([x, out1])
    # x = keras.layers.Conv1D(filters=filter_size[10], kernel_size=kernel_size, activation=None, padding='same')(x)
    # x = keras.layers.LeakyReLU(alpha=0.15)(x)
    # x = keras.layers.Dropout(rate = drop_rate) (x)

    out = keras.layers.Conv1D(filters=1, kernel_size=kernel_size, activation='sigmoid', padding='same')(x)

    model = keras.Model(inputs=model_inputs, outputs=out)

    return model