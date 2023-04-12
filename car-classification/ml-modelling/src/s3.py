import os
import boto3
from botocore import UNSIGNED
from botocore.config import Config


def download_images(bucket_name: str):
    s3 = boto3.resource("s3", config=Config(signature_version=UNSIGNED))
    bucket = s3.Bucket(bucket_name)

    num_images = len(list(bucket.objects.all()))

    for i, obj in enumerate(bucket.objects.all()):
        folder = os.path.join("data", obj.key.split("/")[0])
        if not os.path.exists(folder):
            os.makedirs(folder)

        filepath = os.path.join("data", obj.key)
        bucket.download_file(obj.key, filepath)
        print(f"{i+1}/{num_images} images downloaded", end="\r")
