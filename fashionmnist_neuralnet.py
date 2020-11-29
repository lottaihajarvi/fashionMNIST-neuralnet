# -*- coding: utf-8 -*-
"""fashionMNIST-neuralnet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1D0PUU5RoeLmf7WWIyrk12q6hdISZaVhd

#Getting started

Importing everything:

Tensorflow

Keras for building and training models and neural networks in tf

Numpy for for working with numbers and arrays

Matplotlib for visualizing data sets

Imports and loads the Fashion MNIST dataset
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2
from tensorflow import keras
from keras.datasets import fashion_mnist

"""Load_data gives two lists with two sets; the training and testing values for the graphics that contain the clothing items (img) and their labels (lab)."""

(train_img, train_lab), (test_img, test_lab) = fashion_mnist.load_data()

"""The dataset has 70,000 (60,000 training and 10,000 testing) 28x28 grayscale images of clothes, each mapped to a label. The class names stored seperately:"""

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

"""Prints a training image and label. Change the value [0] to see different items from the array."""

plt.imshow(train_img[0])
plt.title('Class: {}'.format(train_lab[0]))
plt.figure()

print(train_img[0])

"""Shows the first 12 images in the dataset to verify the data is in the correct format. Removes the x and yticks. Labels the class names and converts the images to grayscale. """

plt.figure(figsize=(10,10))
for i in range(12):
  plt.subplot(4,3,i+1)
  plt.xticks([])
  plt.yticks([])
  plt.imshow(train_img[i], cmap=plt.cm.binary)
  plt.xlabel(class_names[train_lab[i]])
plt.show()

"""#Defining and training the neural network and model

'Normalizing' the data. Converts the samples from integers to floating-point numbers (0 - 1), making it easier for training a neural network.
"""

train_img = train_img / 255.0
test_img = test_img / 255.0

"""Defining neural network and designing the deep learning model by stacking layers.

Sequential: Defines a sequence of layers in the neural network.

Flatten: Takes the format of the images from 28 by 28 pixels and transforms them to a one-dimensional array (of 28 * 28 = 784 pixels).

Dense: Adds a layer of neurons.

Activation: Functions tell each layer of neurons what to do.

Relu passes values 0 or greater to the next layer in the network.

Softmax converts the logits to probabilities, which are easier to interpret.

Building the model by compiling it with an *optimizer*, *loss* and *metrics* function that updates the model based on the data it sees, measures how accurate the model is during training and reports it.
"""

def create_model():
  model = tf.keras.models.Sequential([tf.keras.layers.Flatten(input_shape=(28, 28)), 
                                   tf.keras.layers.Dense(512, activation='relu'), 
                                   tf.keras.layers.Dense(10, activation='softmax')])
  
  model.compile(optimizer = tf.keras.optimizers.Adam(),
              loss = 'sparse_categorical_crossentropy',
              metrics=['accuracy'])
  
  return model

"""Training the model

Training the model by calling *model.fit*, asking it to fit your training data to your training labels (aka adjust the model parameters) to minimize the loss.
"""

model = create_model()
model.fit(train_img, train_lab, epochs=20)

"""When the model is done training, an accuracy value is shown at the end of the final epoch, which tells how accurate the neural network is in classifying the training data.

Checks for the model's performance on test data, something it hasn't yet *seen*. The result should be a bit lower due to this. Returns an accuracy value.
"""

test_loss, test_acc = model.evaluate(test_img, test_lab, verbose=2)

print("Test accuracy:", test_acc)

"""Making predictions for each image in test data and printing out the prediction for the first image. Returns an array with the "confidence" value to each of the 10 labels."""

predictions = model.predict(test_img)
predictions[0]

"""Predicting the first 9 images and visualizing the result. np.argmax gives the label with highest "confidence" value."""

preds = np.argmax(predictions, axis=1)

for i in range(9):
  plt.imshow(test_img[i], cmap=plt.cm.binary)
  plt.title('Original: {}, Predicted: {}'.format(test_lab[i], preds[i]))
  plt.axis("Off")
  plt.figure()

"""#Trying out own images"""

def get_img(path):
  img = cv2.imread(path)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  return cv2.resize(img, (28,28))

my_images = np.array([get_img("tshirt.png"), get_img("bag.png"), get_img("boot.png"), get_img("coat.png"), get_img("dress.png"), get_img("sneaker.png")])

predictions = model.predict(my_images)
[predictions]

preds = np.argmax(predictions, axis=1)

plt.figure(figsize=(10,10))
for i in range(6):
  plt.subplot(2,3,i+1)
  plt.xticks([])
  plt.yticks([])
  plt.title('Predicted: {}'.format(preds[i]))
  plt.imshow(my_images[i], cmap=plt.cm.binary)
plt.show()