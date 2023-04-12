import os
import datetime
from os.path import abspath, dirname


class Uploader:
    def save_model(self, model, local: bool = True):
        if local:
            self.save_local(model)
        else:
            raise NotImplementedError

    @staticmethod
    def save_local(model):
        folder = os.path.join(abspath(dirname(dirname(__file__))), "models")
        if not os.path.exists(folder):
            os.makedirs(folder)

        filepath = os.path.join(
            folder, datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "-model.tf"
        )
        model.save(filepath)
