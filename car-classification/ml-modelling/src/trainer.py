from tensorflow.keras.callbacks import EarlyStopping
import config


class Trainer:
    def __init__(self):
        self.early_stopping = EarlyStopping(
            monitor="val_loss", patience=5, restore_best_weights=True
        )

    def fit(self, model, train_generator, valid_generator):
        self.history = model.fit(
            train_generator,
            validation_data=train_generator,
            steps_per_epoch=train_generator.n // train_generator.batch_size,
            validation_steps=valid_generator.n // valid_generator.batch_size,
            callbacks=[self.early_stopping],
            epochs=config.NUM_EPOCHS,
        )
