# https://zetcode.com/python/yaml/

import yaml
import os


class Config(object):
    def __init__(self):
        with open(os.getcwd() + "/config.yml", "r") as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)
            print(self.data)

    def generate(self):
        pass

    def return_boss_info(self, name):
        return self.data.get("bosses").get(name)

    def return_boss_stat(self, boss, header):
        # name: str | energy: int | rows: int | columns: int | hp: int
        # basic: str | special: str | kill: str | phrases: []
        return self.data.get("bosses").get(boss).get(header)


# # Test
yeet = Config()
# # yeet.return_boss_info("mr_phone")
# print(yeet.data.)
