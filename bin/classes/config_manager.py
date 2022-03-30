# https://zetcode.com/python/yaml/

import yaml
import os


class Config(object):
    def __init__(self):
        self.data = None

    def load_config(self):
        if not os.path.exists(os.getcwd() + "config.yml"):
            print("[CW] Config file does not exist, generating a new one")
        with open(os.getcwd() + "/config_copy.yml", "w") as f:
            self.data = f
        print(yaml.load(f, Loader=yaml.FullLoader))

    def get_config(self):
        return self.data

    def get_boss_info(self, name):
        return self.data.get("bosses").get(name)

    def get_boss_stat(self, boss, header):
        # name: str | energy: int | rows: int | columns: int | hp: int
        # basic: str | special: str | kill: str | phrases: []
        return self.data.get("bosses").get(boss).get(header)


# # Test
yeet = Config()
yeet.load_config()
print(yeet.get_config())
# # yeet.return_boss_info("mr_phone")
# print(yeet.data.)
