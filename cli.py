from libs.backend import *
import argparse


def build_menu_string():
    settings = read_settings()

    tab = '\t'

    settings_params = [f"{tab}{tab}{k}: {v}\n" for k, v in settings.items()]
    out_string = f"""
    Current settings
{''.join(settings_params)}

    Options
        P: Process
        R: View current configuration from file
        Q: Quit
    """

    return out_string


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLI/Interface Parser')
    parser.add_argument('--config_file', dest='config_file', action='store_true')
    parser.add_argument('--interface', dest='interface', action='store_true')
    parser.set_defaults(config_file="config/config.json")
    parser.set_defaults(interface=False)

    parsed_args = parser.parse_args()
    config_file = parsed_args.config_file
    interface = parsed_args.interface

    settings = read_settings(config_file)
    if interface:
        while True:
            print(build_menu_string())
            _input = str(input("What would you like to do?: ")).upper()

            if _input == 'Q':
                break
            elif _input == 'R':
                print(build_menu_string())
            elif _input == 'P':
                process(config_file)
    else:
        settings = read_settings()

