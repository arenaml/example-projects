from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import EfficientNetV2B0
import config


class Model:
    def prepare(self, num_classes: int):
        self.base_model = EfficientNetV2B0(
            include_top=False,
            weights="imagenet",
            input_tensor=Input(shape=(config.INPUT_SIZE, config.INPUT_SIZE, 3)),
        )
        for layer in self.base_model.layers:
            layer.trainable = False

        self.model = Sequential(
            [
                self.base_model,
                Flatten(),
                Dense(512, activation="relu"),
                Dense(num_classes, activation="softmax"),
            ]
        )

        self.model.compile(
            loss="categorical_crossentropy",
            optimizer=Adam(learning_rate=config.LEARNING_RATE),
            metrics=["accuracy"],
        )

        return self.model
