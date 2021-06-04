from backend import *
import argparse


def build_menu_string():
    settings = read_settings()

    newline = '\n'
    tab = '\t'

    settings_params = [f"{tab}{tab}{k}: {v}\n" for k, v in settings.items()]
    out_string = f"""
    Current settings
{''.join(settings_params)}

    Options
        1: Change input folder
        2: Change output folder
        P: Process
        R: Refresh configuration from file
        Q: Quit
    """

    return out_string


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLI/Interface Parser')
    parser.add_argument('--interface', dest='interface', action='store_true')
    parser.set_defaults(interface=False)

    while True:
        print(build_menu_string())
        _input = str(input("What would you like to do?: ")).upper()

        if _input == 'Q':
            break
        elif _input == 'R':
            continue
        elif _input == 'P':
            process()
        elif _input in [str(v) for v in range(1, 3)]:
            if _input == '1':
                folder = str(input("Enter input folder directory: "))
                set_input_folder(folder)
            elif _input == '2':
                folder = str(input("Enter output folder directory: "))
                set_output_folder(folder)

                # write_settings()
