#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 18:56:09 2019

@author: eric
"""

# starting imports
import keras as k
import numpy as np
import pandas as pd
import os
from PIL import Image, ImageOps
from sklearn import cross_validation

# read images and add to big dataset in memory
"""
original dataset sized down to:
elephant
persian+cat
tiger
wolf
"""
image_size = (256, 256)
l_data = []
animals = {"elephant":0, "persian+cat":1, "tiger":2, "wolf":3}
for d in os.listdir("./data/"):
    print("Loading: {0}".format(d))
    for f in os.listdir("./data/{0}".format(d)):
        i = Image.open("./data/{0}/{1}".format(d,f)).convert('L')
        scaled = ImageOps.fit(i, image_size, Image.ANTIALIAS)
        im_data = list(scaled.getdata())
        im_data.append(animals[d])
        l_data.append(im_data)
        
data = np.array(l_data)

# shuffle data and separate into X_train, X_test, y_train, y_test
print("Preparing data...")
np.random.shuffle(data)
X = data[:, :-1]
Y = pd.get_dummies(data[:, -1])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        X, Y, test_size=0.2, random_state=5)

X_train = X_train.reshape(X_train.shape[0], 256, 256, 1)
X_train = X_train.astype('float32')
X_test = X_test.reshape(X_test.shape[0], 256, 256, 1)
X_test = X_test.astype('float32')

# build NN
print("Building model...")
model = k.Sequential()

# convolutional layer w/ rectified linear unit activation
input_shape = list(image_size)
input_shape.append(1)
model.add(k.layers.Conv2D(32, kernel_size=(3,3), activation='relu', input_shape=input_shape))
# 32 convolution filters used, each of size 3x3

# again
model.add(k.layers.Conv2D(64, (3,3), activation='relu'))
# 64 convolution filters used, each of size 3x3

# again
#model.add(k.layers.Conv2D(128, (3,3), activation='relu'))
# 128 convolution filters used, each of size 3x3

# choose best features via pooling
model.add(k.layers.MaxPooling2D(pool_size=(2,2)))

# randomly turn neurons on/off to improve convergence
model.add(k.layers.Dropout(0,25))

# flatten since too many dimensions, we only want classification output
model.add(k.layers.Flatten())

# fully connected to get all relevant data
model.add(k.layers.Dense(128, activation='relu'))

# one more for convergence's sake
model.add(k.layers.Dropout(0.5))

# output a softmax to squash the matrix into output probabilities
model.add(k.layers.Dense(4, activation='softmax'))

# compile  model
# use categorical_crossentropy as we have multiple classes
model.compile(loss=k.losses.categorical_crossentropy, optimizer=k.optimizers.Adadelta(), metrics=['accuracy'])

# train & test model
print("Training model...")
batch_size = 128
num_epoch = 10
model_log = model.fit(X_train, y_train, batch_size=batch_size, epochs=num_epoch, verbose=1, validation_data=(X_test,y_test))

# evaluate model
score = model.evaluate(X_test, y_test, verbose=0)
print 'Test loss:', score[0]
print 'Test accuracy:', score[1]

# plot model training
import matplotlib.pyplot as plt
fig = plt.figure()
plt.subplot(2,1,1)
plt.plot(model_log.history['acc'])
plt.plot(model_log.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='lower right')

plt.subplot(2,1,2)
plt.plot(model_log.history['loss'])
plt.plot(model_log.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')

plt.tight_layout()

fig