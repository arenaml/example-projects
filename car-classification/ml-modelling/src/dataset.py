import os
from os.path import abspath, dirname
from typing import Optional
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import config
import s3


class Dataset:
    def prepare(
        self,
        from_s3: bool = False,
        path: Optional[str] = None,
        bucket_name: Optional[str] = None,
    ):
        if from_s3:
            if not bucket_name:
                raise Exception("Using S3 requires `bucket_name` arg.")
            s3.download_images(bucket_name)
            self.data_path = "data"
        else:
            if path:
                self.data_path = path
            else:
                self.data_path = os.path.join(
                    abspath(dirname(dirname(dirname(__file__)))),
                    "data-collection",
                    "data",
                )

        self.train_datagen = ImageDataGenerator(
            validation_split=config.VALIDATION_SPLIT
        )

        self.train_generator = self.train_datagen.flow_from_directory(
            self.data_path,
            subset="training",
            target_size=(config.INPUT_SIZE, config.INPUT_SIZE),
            batch_size=config.BATCH_SIZE,
            shuffle=True,
        )

        self.valid_generator = self.train_datagen.flow_from_directory(
            self.data_path,
            subset="validation",
            target_size=(config.INPUT_SIZE, config.INPUT_SIZE),
            batch_size=config.BATCH_SIZE,
            shuffle=True,
        )
