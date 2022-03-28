import yaml
import os


class Config(object):
    def __init__(self):
        with open(os.getcwd() + "config.yml", "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)

    def setup(self):
        pass
