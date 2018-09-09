import glob
import re

import librosa

from utils import *

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
SPEECH_ROOT = os.path.join(ROOT_DIR, 'voices', 'data')


def read_wav(path, fs=16000):
    data, _ = librosa.load(path, sr=fs)
    return np.trim_zeros(data)


def input_file(path):
    return path.startswith('cd') and path.endswith('.wav')


def output_file(path):
    return path.startswith("md") and path.endswith('.wav')


def get_speeches():
    files = os.listdir(SPEECH_ROOT)

    input_files = list(filter(input_file, files))
    output_files = list(filter(output_file, files))

    assert len(input_files) == len(output_files)

    cnt = len(input_files)
    wave_pairs = []
    for i in range(1, cnt + 1):
        cd = read_wav(os.path.join(SPEECH_ROOT, 'cd{}.wav'.format(i)))
        md = read_wav(os.path.join(SPEECH_ROOT, 'md{}.wav'.format(i)))
        cd = cd[8000:]
        md = md[8000:]
        wave_pairs.append([cd, md])
    return wave_pairs


def assemble_matrices(arr1, arr2, window_size, shift):
    x, y = [], []
    length = min(len(arr1), len(arr2))
    arr1 = arr1[:length]
    arr2 = arr2[:length]

    for i in range(0, length - window_size, shift):
        x.append(arr1[i : i + window_size])
        y.append(arr2[i : i + window_size])
    return np.array(x), np.array(y)

speech_list = get_speeches()
def generate_train_data(input_length, shift):
    for dl, md in speech_list:
        origin = normalize(dl)
        target = normalize(md)
        x, y = assemble_matrices(origin, target, input_length, shift)
        yield np.expand_dims(x, axis=2), np.expand_dims(y, axis=2)


if __name__ == '__main__':
    # batches = generate_train_data(4000, 1000)
    # x, y = next(batches)
    # print(x.shape, y.shape)
    speech_list = get_speeches()
    for x, y in speech_list:
        draw_wave(x, y)
        play(x)
        play(y)
