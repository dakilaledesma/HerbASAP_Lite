# HerbASAP Lite

### HerbASAP Lite may be run in multiple formats:


| As a standalone program (with preliminary native Apple Silicon support) | ...or even online for free (proof of concept code: [Google Colab Notebook](https://colab.research.google.com/drive/10KKkkNkTW3rOWyzJdD5XkiKmUJfdSJAy?usp=sharing))|
| --- | --- |
| ![HerbASAP Lite Window](https://imgur.com/1GEPJG2.gif) | ![HerbASAP Lite Colab](https://imgur.com/Ww2hZD6.gif) |


This repository contains a much faster version of HerbASAP that is made for batch and headless processing of already taken images rather than processing in real-time. This version is much better tuned for multiprocessing and tries to be less dependent on certain libraries to reduce bulk, increase platform compatibility (such as ARM/Apple Silicon or running on online platforms such as Google Colab), and minimize the codebase for debugging.

HerbASAP Lite is *not* meant to replace HerbASAP, but rather serve a different purpose while being much less buggy and easier to maintain.


## Current usage (Windows)
Executables have not been built yet. In order to use HA Lite, please do the following: 

1. Install Anaconda or Miniconda
2. Clone this repository
3. Using Anaconda PowerShell Prompt or your terminal, `cd` into the repo.
4. `conda env create -f conda_environment.yml`
5. `conda activate HAL`
6. Do one of the following:
  - For the CLI: `python -u cli.py [args]`
  - For the GUI interface `python -u interface.py`

## Compared to normal HerbASAP
- It loses:
  - Real-time processing of images as you take them from the camera.
  - A "proper" GUI via PyQT5 with viewing processed images as you take them.
  - GPU inferencing support (for ColorNet)
- To gain:
  - Significant speed up in batch processing.
  - A CLI-friendly script you can run in headless machines that does all of the backend processing.
    - May be run within servers or even on online platforms such as Google Colab 
  - A simpler HTML5 interface that is *completely* separate from the CLI/backend script, allowing for extension of the interface without messing with the backend.
  - Much easier to maintain and less buggy codebase at less than 1/3rd of the main "master" script.
  - Higher cross-compatibility support due to less libraries being needed. For example, an initial build works natively with Apple Silicon - see the "apple_silicon" branch


## How much faster is HerbASAP Lite for batch processing? 

Tested:
  - 50 RAW Files
  - All functions enabled except lens correction

| Name | Time | Specs |
|---|---|---|
| HerbASAP Lite | 54.98s | Core i9-7900X @ 18 workers
| HerbASAP | 3m:08.56s | Core i9-7900X @ 15 workers + Nvidia 1080Ti
| Speedup | 3.43x faster | |

| Name | Time | Specs |
|---|---|---|
| HerbASAP Lite | 2m:36.05s | Core i7-8550U @ 6 workers
| HerbASAP | 4m:17.35s | Core i7-8550U @ 6 workers + Nvidia MX150
| Speedup | 1.64x faster | |


## Apple Silicon Comparison
  - 50 RAW Files
  - All functions enabled except lens correction and TensorFlow (TF2 not compatible with ColorNet)

| Processor Name | Time | Specs |
|---|---|---|
| Intel Core i9-7900X | 14.2s | 10C/20T @ 20 workers
| Intel Core i7-8550U | 38.0s | 4C/8T @ 8 workers
| Apple Silicon M1 | 15.2s | 8C/8T @ 8 workers (fanless, MacBook Air late 2020)


