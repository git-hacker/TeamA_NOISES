import os
import numpy as np


def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def normalize(vec):
    return vec / np.max(np.abs(vec), axis=0)


def draw_wave(*wave):
    from matplotlib import pyplot as plt
    plt.figure()
    for w in wave:
        plt.plot(w, linewidth=.2)
    plt.show()


def play(array, fs=16000):
    import sounddevice as sd
    print("Playing audio...")
    sd.play(array, fs, blocking=True)
    print("Stop playing.\n")
