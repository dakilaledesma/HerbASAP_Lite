from backend import *
import argparse
from tqdm import tqdm


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


def process():
    settings = read_settings()
    files = glob(f'{settings["input_folder"]}/*.CR2')

    # Getting number of workers for multiprocessing, minimum 3 workers
    num_workers = max([3, multiprocessing.cpu_count()])

    # joblib synchronous processing. Async through subprocess actually not much faster.
    out = Parallel(n_jobs=num_workers, verbose=9)(
        delayed(compute)(idx, file, settings) for idx, file in enumerate(files))


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='CLI/Interface Parser')
    # parser.add_argument('--interface', dest='interface', action='store_true')
    # parser.set_defaults(interface=False)

    while True:
        print(build_menu_string())
        _input = str(input("What would you like to do?: ")).upper()

        if _input == 'Q':
            break
        elif _input == 'R':
            print(build_menu_string())
        elif _input == 'P':
            process()
