import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["AUTOGRAPH_VERBOSITY"] = "0"

from dataset import Dataset
from model import Model
from trainer import Trainer
from uploader import Uploader


def main():
    dataset = Dataset()
    dataset.prepare(from_s3=True, bucket_name=os.environ.get("S3_BUCKET_NAME"))
    model = Model()
    model = model.prepare(num_classes=dataset.train_generator.num_classes)
    trainer = Trainer()
    trainer.fit(
        model=model,
        train_generator=dataset.train_generator,
        valid_generator=dataset.valid_generator,
    )
    uploader = Uploader()
    uploader.save_model(model)


if __name__ == "__main__":
    main()
