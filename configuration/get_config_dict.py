# --------------------------------------------------------------------------------------------
# NOTE: THIS FILE REQUIRES THAT YOU INSTALL BOTH YAML AND PYPERCLIP IN ORDER FOR IT TO WORK
# --------------------------------------------------------------------------------------------

import os
import pyperclip
import yaml


def run():
    file_name = input("Please enter the name of the config file you want: ")
    config_dict = {}

    try:
        with open(os.getcwd() + "/" + file_name + ".yml", "r") as f:
            config_dict = yaml.safe_load(f)
    except FileNotFoundError:
        print("Could not find " + file_name + "./yml")
    return config_dict


if __name__ == '__main__':
    output = run()
    print(output)
    pyperclip.copy(str(output))
    print("\nThe dictionary has successfully been copied to your clipboard")
