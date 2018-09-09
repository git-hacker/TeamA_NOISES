import os

from loader import read_wav, play, ensure_dir_exists

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))


def get_wave(filename):
    source_root = os.path.join(ROOT_DIR, "editing")
    dirname = os.path.join(source_root, p)
    filepath = os.path.join(dirname, filename)
    if os.path.exists(filepath):
        return read_wav(filepath)
    return None


def save_pair(cd, md, num):
    from librosa.output import write_wav
    dest_dir = os.path.join(ROOT_DIR, 'voices', 'cd2md')
    ensure_dir_exists(os.path.join(ROOT_DIR, 'voices', 'cd2md', 'input'))
    ensure_dir_exists(os.path.join(ROOT_DIR, 'voices', 'cd2md', 'output'))
    write_wav(os.path.join(dest_dir, 'input', '{}.wav'.format(num)), cd, 16000)
    write_wav(os.path.join(dest_dir, 'output', '{}.wav'.format(num)), md, 16000)



if __name__ == "__main__":

    folders = ['pb', 'pl', 'zy', 'ec']

    cnt = 1
    for p in folders:
        for i in range(11):
            inputfile = get_wave('cd{}.wav'.format(i))
            outputfile = get_wave('md{}.wav'.format(i))
            if inputfile is None or outputfile is None:
                continue
            save_pair(inputfile, outputfile, cnt)
            cnt += 1
