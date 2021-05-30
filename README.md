# HerbASAP Lite

![HerbASAP Lite Window](https://imgur.com/eYVc9IQ.png)


This repository contains a much faster version of HerbASAP that is made for batch processing of already taken images rather than processing in real-time. This version is much better tuned for multiprocessing and tries to be less dependent on certain libraries to reduce bulk, increase platform compatibility (such as ARM/Apple Silicon), and minimize the codebase for debugging.

HerbASAP Lite is *not* meant to replace HerbASAP, but rather serve a different purpose while being much less buggy and easier to maintain.


## Compared to normal HerbASAP
- It loses:
  - Real-time processing of images as you take them from the camera.
  - A "proper" GUI via PyQT5 with viewing processed images as you take them.
- To gain:
  - Significant speed up in batch processing.
  - A CLI-friendly script you can run in headless machines that does all of the backend processing.
  - A simpler HTML5 interface that is *completely* separate from the CLI/backend script, allowing for extension of the interface without messing with the backend.
  - Much easier to maintain and less buggy codebase at less than 1/3rd of the main "master" script.


## How much faster is HerbASAP Lite for batch processing? 
| HerbASAP | HerbASAP Lite | Speedup |
|---|---|---|
| 3m:08.56s | 54.98s | 3.43x faster |

Tested:
  - 50 RAW Files
  - 18 threads
  - All functions enabled except lens correction
