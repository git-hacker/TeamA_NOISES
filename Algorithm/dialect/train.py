from loader import generate_train_data
from prototypes import wavenet
from transform import load_model
from utils import ensure_dir_exists, play

if __name__ == '__main__':
    input_length = 4000
    epochs = 5000
    ensure_dir_exists('models/')

    # cont = False
    # if cont:
    #     model = load_model('models/pb_overfit.h5', input_length)
    # else:
    model = wavenet(input_length)

    b = generate_train_data(input_length, 1000)
    for x, y in b:
        print(x.shape, y.shape)

    # for e in range(epochs):
    #     train_batches = generate_train_data(input_length, 1000)
    #     print("Epoch {}/{}:".format(e + 1, epochs))
    #     for x, y in train_batches:
    #         model.fit(x, y, batch_size=4, epochs=1, verbose=1)
    #
    #     if (e + 1) % 50 == 0:
    #         print("Saving intermediate model weights...")
    #         model.save_weights('models/tmp.h5')
    #
    # print("\nTraining complete!\nSaving model...")
    # model.save_weights('models/final_weights.h5')
    # print("Model saved, terminate.")
