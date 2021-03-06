# -*- coding: utf-8 -*-
"""project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1I3FNauPrzoRGJwqQJFOxfEYRQImszIL8
"""

# Anastassiya Ryabkova
# Project
# BS18-SE2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# load data
x = np.load('x.npy')
y = np.load('y.npy')

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

print('Train: X = %s, y = %s' % (X_train.shape, y_train.shape))
print('Test: X = %s, y = %s' % (X_test.shape, y_test.shape))

for i in range(9):
    # define subplot
    plt.subplot(330 + 1 + i)
    # plot raw pixel data
    plt.imshow(X_train[i].squeeze(), cmap=plt.get_cmap('gray'))
# show the figure
plt.show()

# print the final input shape ready for training
print("Train matrix shape", X_train.shape)
print("Test matrix shape", X_test.shape)

import tensorflow as tf

# unique classes
y_unique = np.unique(y_train, return_counts=True)

# define a model with layers

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(filters = 64, use_bias= False,  kernel_size = 5, input_shape=(28,28,1), activation='relu'))
model.add(tf.keras.layers.MaxPool2D( pool_size = 2, strides = 1)),
model.add(tf.keras.layers.Conv2D( filters = 32, use_bias= False, kernel_size = 3,  activation='relu'))
model.add(tf.keras.layers.MaxPool2D(pool_size = 4, strides = 2))
model.add(tf.keras.layers.Flatten( ))
model.add(tf.keras.layers.Dense(512, use_bias= False, activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(512, use_bias= False,  activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(10, use_bias= False,activation='softmax'))

# def scheduler(epoch, lr):
#   if epoch == 10:
#     return lr * 0.3
#   if epoch == 20:
#     return lr * 0.5
#   return lr

# scheduler_call = tf.keras.callbacks.LearningRateScheduler(scheduler)
# define the scheduler for callback
scheduler_call = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_accuracy',factor=0.5,patience=10)

# compil the model
model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer=tf.keras.optimizers.Adam(1e-04, clipnorm = 1),
    metrics=['accuracy'],
)
model.summary()

# perform data augementations
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    featurewise_center=False, samplewise_center=False,
    featurewise_std_normalization=False, samplewise_std_normalization=False,
    zca_whitening=False, zca_epsilon=1e-06, rotation_range=25, width_shift_range=0.2,
    height_shift_range=0.15, brightness_range=(0.2, 0.8), shear_range=0.2, zoom_range=0.15,
    channel_shift_range=0.0, fill_mode='nearest', cval=0.2, horizontal_flip=False,
    vertical_flip=False, rescale=1./255, preprocessing_function=None,
    data_format=None, validation_split=0.2, dtype=None
)
datagen.fit(X_train)

# define earlystopping for callbacks
earlystopping = tf.keras.callbacks.EarlyStopping(monitor ="val_accuracy", patience = 10,  
                                        restore_best_weights = True)

# fit the model
history = model.fit(datagen.flow(X_train, y_train, batch_size=128), epochs=35, steps_per_epoch = len(X_train)/128,
          validation_data=datagen.flow(X_train, y_train, batch_size=128, subset = 'validation'), callbacks =[earlystopping, scheduler_call])

# evaluate the model on the test data
model.evaluate(X_test,  y_test, verbose=2)

# save the model
model.save('model.h5')