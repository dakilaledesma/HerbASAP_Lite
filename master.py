import subprocess
from glob import glob
import numpy as np

num_workers = 18

files = list(glob("C:/Users/Dakila/Pictures/HA/Input/*.*"))
file_batches = np.array_split(files, num_workers)

subprocesses = [subprocess.Popen(f"python -u cli2.py --files {' '.join(file_batch)}", stdout=subprocess.PIPE, universal_newlines=True) for file_batch in file_batches]

for process in subprocesses:
    process.wait()
    # process_id = popen
    #
    # unique_images_processed = set()
    # for stdout_line in iter(popen.stdout.readline, ""):
    #     print(stdout_line)
    #
    # popen.stdout.close()
    # return_code = popen.wait()
    # popen.kill()


