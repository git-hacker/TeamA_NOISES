from loader import get_speeches, assemble_matrices, play, draw_wave, read_wav
from prototypes import wavenet
import numpy as np


def load_model(weights_file, input_length):
    print("Creating model and loading weights...")
    model = wavenet(input_length)
    model.load_weights(weights_file)
    print("Model creation complete!\n")
    return model


def denoise(wave):
    from oct2py import octave
    output = octave.feval('logmmse', np.trim_zeros(wave), 16000)
    return np.float32(np.squeeze(output))


if __name__ == '__main__':
    input_length = 4000

    # sample, real = get_speeches()[1]
    sample = real = read_wav('test.wav')
    play(sample)
    # denoised = denoise(sample)
    # play(denoised)

    feed, _ = assemble_matrices(sample, sample, input_length, shift=input_length)

    # model = load_model('models/pb_overfit.h5', input_length)
    model = load_model('models/tmp.h5', input_length)

    predictions = model.predict(np.expand_dims(feed, axis=2), batch_size=8)
    output = predictions.flatten()
    denoised = denoise(output)
    draw_wave(sample, real, output, denoised)
    print("Playing the transformed audio")
    play(output * 5)
    print("Playing the denoised transform")
    play(denoised * 5)

