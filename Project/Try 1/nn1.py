#!/usr/bin/python2
import gzip
import numpy as np
#from keras.models import Sequential
#from keras.layers import Conv2D
#from keras.regularizers import l2, l1
#from keras.optimizers import SGD

f = gzip.open('train-images-idx3-ubyte.gz')

image_size = 28
num_images = 60000

f.read(16)
buf = f.read(image_size * image_size * num_images)
data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
data = data.reshape(num_images, image_size, image_size, 1)

import matplotlib.pyplot as plt
image = np.asarray(data[2]).squeeze()
plt.imshow(image)

#model = Sequential()
#model.add(Conv2D(3, input_shape=(256,256)))
