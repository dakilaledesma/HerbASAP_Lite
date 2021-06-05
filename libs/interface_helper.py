from backend import process
from helper_functions import read_settings
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interface helper parser')
    parser.add_argument('--config_file', dest='config_file')
    parser.set_defaults(config_file="config/Default.json")

    parsed_args = parser.parse_args()
    config_file = parsed_args.config_file

    settings = read_settings(config_file)
    process(settings=settings, gui_interface=True)
    print("[HAL-DONE]")
