from keras import Input, Model
from keras.layers import Dense
import numpy as np


if __name__ == "__main__":
    x = Input(shape=(1000,))
    h = Dense(5000, activation='relu')(x)
    h = Dense(2000, activation='relu')(h)
    h = Dense(1000, activation='relu')(h)
    h = Dense(200, activation='relu')(h)
    o = Dense(20, activation='relu')(h)
    model = Model(x, o)
    model.compile(loss='mse', optimizer='adam')

    a = np.random.randn(10000, 1000)
    b = np.random.randn(10000, 20)
    model.fit(a, b, epochs=10)
