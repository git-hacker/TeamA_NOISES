import librosa
import numpy as np

def read_wav(path, fs=16000):
    data, _ = librosa.load(path, sr=fs)
    return np.trim_zeros(data)

def play(array, fs=16000):
    import sounddevice as sd
    print("Playing audio...")
    sd.play(array, fs, blocking=True)
    print("Stop playing.\n")

def denoise(wave, sr=16000):
    from oct2py import octave
    x = octave.feval('api/logmmse', wave, sr)
    x = np.float32(x)
    return np.squeeze(x)

def draw_wave(*wave):
    from matplotlib import pyplot as plt
    plt.figure()
    for w in wave:
        plt.plot(w, linewidth=.2)
    plt.show()

wave = read_wav('media/noise_2jts5xo.wav')


clean = denoise(wave)
print()
# play(wave)
# play(clean)
print(clean)