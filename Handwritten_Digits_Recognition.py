import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
import os


# Check if to load an existing model or to train a new one
train_new_model = False

if train_new_model:

    # Loading the MNIST data set with samples and splitting it
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # Normalizing the data (making length = 1)
    x_train = tf.keras.utils.normalize(x_train, axis=1)
    x_test = tf.keras.utils.normalize(x_test, axis=1)

    # Create a neural network model
    model = tf.keras.models.Sequential()
    # Add one flattened input layer for the pixels
    model.add(tf.keras.layers.Flatten(input_shape=(28,28)))
    # Add two dense hidden layers
    model.add(tf.keras.layers.Dense(units=128, activation='relu'))
    model.add(tf.keras.layers.Dense(units=128, activation='relu'))
    # Add one dense output layer for the 10 digits
    model.add(tf.keras.layers.Dense(units=10, activation='softmax'))

    # Compiling and optimizing model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Training the model
    model.fit(x_train, y_train, epochs=3)

    # Evaluating the model
    loss, accuracy = model.evaluate(x_test, y_test)
    print(loss)
    print(accuracy)

    # Saving the model
    model.save('handwritten_digits.model')

else:
    # Load the model
    model = tf.keras.models.load_model('handwritten_digits.model')



# Load custom images and predict them (Images must be 28x28)
image_number = 1

while os.path.isfile('digits/digit{}.png'.format(image_number)):
    
    try:
        img = cv2.imread('digits/digit{}.png'.format(image_number))[:,:,0]
        img = np.invert(np.array([img]))
        prediction = model.predict(img)
        print("The number is probably a {}".format(np.argmax(prediction)))
        plt.imshow(img[0], cmap=plt.cm.binary)
        plt.show()
        image_number += 1

    except:
        print("Error reading image! Proceeding with next image...")
        image_number += 1
