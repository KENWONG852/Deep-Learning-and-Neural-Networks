# CNN for MNIST handwritten digit classification
# Usage:
#   python3 mnist_cnn.py

from __future__ import print_function

import keras
import argparse
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, BatchNormalization, Conv2D, MaxPooling2D
from keras.optimizers import SGD
from keras import backend as K

from tensorflow.keras.callbacks import TensorBoard

# arguments passed from the terminal
parser = argparse.ArgumentParser(description='Tensorflow (Keras) MNIST Example')

parser.add_argument('--mode', type=str, default='train', 
                    help='train or test the model.')
parser.add_argument('--batch-size', type=int, default=128, metavar='N',
                    help='input batch size for training (default: 128)')
parser.add_argument('--epochs', type=int, default=20, metavar='N',
                    help='number of epochs to train (default: 20)')
parser.add_argument('--model_path', type=str, default='models/mnist_cnn.keras', 
                    help='The path where the trained model is saved.')

args = parser.parse_args()
epochs = args.epochs
batch_size = args.batch_size
num_classes = 10

# input image dimensions
img_rows, img_cols = 28, 28

# the data, shuffled and split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# CNN structure definition
model = Sequential()
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
# model.add(Conv2D(64, kernel_size=(3, 3), activation='sigmoid', input_shape=input_shape))
# model.add(Conv2D(64, kernel_size=(3, 3), activation='tanh', input_shape=input_shape)) 
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(Conv2D(64, (3, 3), activation='sigmoid'))
# model.add(Conv2D(64, (3, 3), activation='tanh'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
for i in range(0,3):
    model.add(Dense(128, activation='relu'))
    # model.add(Dense(128, activation='sigmoid'))
    # model.add(Dense(128, activation='tanh'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.summary()

model.compile(loss=keras.losses.categorical_crossentropy, optimizer=SGD(learning_rate=0.01), metrics=['accuracy'])

if __name__ == '__main__':
    
    if args.mode == 'train':
        
        tbCallBack = TensorBoard(log_dir='./log_keras', # the path of the directory where to save the log files to be parsed by TensorBoard
                        histogram_freq=1,         # frequency (in epochs) at which to compute activation and weight histograms for the layers
                        write_graph=True,         # whether to visualize the graph in TensorBoard
                        #write_grads=False,         # whether to visualize the histogram of gradient values in TensorBoard
                        write_images=False,       # whether to write model weights to visualize as image in TensorBoard
                        update_freq='epoch')      # 'batch' or 'epoch' or integer
        
        model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1, shuffle=False,
          callbacks=[tbCallBack])
        
        # Save the model
        model_file = args.model_path
        print('Saving CNN to %s' % model_file)
        model.save(model_file)
    
    elif args.mode == 'test':
                
        model = keras.models.load_model(args.model_path)
        score = model.evaluate(x_test, y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy: %.2f%%' % (score[1]*100))