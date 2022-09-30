import models.ts_cnn as ts_cnn
from tensorflow import keras

model = ts_cnn()

optimizer = keras.optimizers.Adam()
model.compile(optimizer=optimizer,
                # loss=[l1, l1, l1],
                loss=['binary_crossentropy'],
                metrics=['accuracy'])


epochs = 500
batch_size = 32

callbacks = [
    keras.callbacks.ModelCheckpoint(
        "best_model.h5", save_best_only=True, monitor="val_loss"
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss", factor=0.5, patience=20, min_lr=0.0001
    ),
    keras.callbacks.EarlyStopping(monitor="val_loss", patience=50, verbose=1),
    ]

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["sparse_categorical_accuracy"],
)


# history = model.fit(
#     x_train,
#     y_train,
#     batch_size=batch_size,
#     epochs=epochs,
#     callbacks=callbacks,
#     validation_split=0.2,
#     verbose=1,
# )


