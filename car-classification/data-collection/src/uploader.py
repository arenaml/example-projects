import os
from os.path import abspath, dirname
import shutil
from urllib3.response import HTTPResponse


class Uploader:
    def __init__(self, local: bool = True):
        self.local = local

    def save_local(self, img_data: HTTPResponse, img_filename: str, make: str) -> None:
        folder = os.path.join(abspath(dirname(dirname(__file__))), "data", make)
        if not os.path.exists(folder):
            os.makedirs(folder)
        filepath = os.path.join(folder, img_filename)
        with open(filepath, "wb") as f:
            shutil.copyfileobj(img_data, f)

    def save_s3(self, img_data: HTTPResponse, img_filename: str, make: str) -> None:
        raise NotImplementedError

    def save_image(self, img_data: HTTPResponse, img_filename: str, make: str) -> None:
        if self.local:
            self.save_local(img_data, img_filename, make)
        else:
            self.save_s3(img_data, img_filename, make)
