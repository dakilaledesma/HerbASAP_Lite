# HerbASAP Lite

This repository contains a much faster version of HerbASAP that is made for batch processing of already taken images rather than processing in real-time. This version is much better tuned for multiprocessing and tries to be less dependent on certain libraries to reduce bulk, increase platform compatibility (such as ARM/Apple Silicon), and minimize the codebase for debugging.

In a nutshell, HerbASAP Lite is faster in batch processing and contains a much slimmer and easier-to-maintain codebase.

How much faster is HerbASAP Lite for batch processing? 
| HerbASAP | HerbASAP Lite | Speedup |
|---|---|---|
| 3m:08.56s | 54.98s | 3.43x faster |

Tested:
  - 50 RAW Files
  - 18 threads
  - All functions enabled except lens correction
