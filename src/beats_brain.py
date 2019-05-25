import numpy as np
import tensorflow as tf

from tensorflow import keras


def main():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(256, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])
    model.compile(optimizer = tf.train.AdamOptimizer(),
                  loss = 'sparse_categorical_crossentropy',
                  metrics = ['accuracy'])

    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    train_images = train_images / 255.0
    test_images = test_images / 255.0

    callbacks = Callback()

    model.fit(train_images, train_labels, epochs=10, callbacks=[callbacks])
    model.evaluate(test_images, test_labels)


class Callback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if (logs.get('loss') < 0.5):
            print("\n Loss is less than 0.5, training cancelled.")
            self.model.stop_training = True
        elif (logs.get('acc') > 0.65):
            print("\n Accuracy is greater than 0.65, training cancelled.")
            self.model.stop_training = True


if __name__ == '__main__':
    main()

