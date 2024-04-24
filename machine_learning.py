import matplotlib.pyplot as plt
import seaborn as sns

import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D , MaxPool2D , Flatten , Dropout
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from Labeler_Data import get_data
from sklearn.metrics import classification_report,confusion_matrix
from keras.utils.vis_utils import plot_model
import pydot

import tensorflow as tf

import numpy as np

def CNN_Training(folderTraining, folderTesting, ep, LearningRate, dataType, img_size):
    #img_size = 32

    trainData = get_data(folderTraining, img_size)

    x_train = []
    y_train = []


    for feature, label in trainData:
      x_train.append(feature)
      y_train.append(label)

    # Normalize the data
    x_train = np.array(x_train) / 255

    x_train.reshape(-1, img_size, img_size, 1)
    y_train = np.array(y_train)

    testData = get_data(folderTesting, img_size)
    x_val = []
    y_val = []

    for feature, label in testData:
        x_val.append(feature)
        y_val.append(label)

    x_val = np.array(x_val) / 255

    x_val.reshape(-1, img_size, img_size, 1)
    y_val = np.array(y_val)

    CAT = ['Or_To_Take_Arms', 'That_Is_The_Question', 'To_be_or_not_to_be', 'To_die', 'To_Sleep', 'Whether']
    num_labels = len(CAT)
    datagen = ImageDataGenerator(
            featurewise_center=False,  # set input mean to 0 over the dataset
            samplewise_center=False,  # set each sample mean to 0
            featurewise_std_normalization=False,  # divide inputs by std of the dataset
            samplewise_std_normalization=False,  # divide each input by its std
            zca_whitening=False,  # apply ZCA whitening
            rotation_range = 0,  # randomly rotate images in the range (degrees, 0 to 180)
            zoom_range = 0.3, # Randomly zoom image
            width_shift_range=0.2,  # randomly shift images horizontally (fraction of total width)
            height_shift_range=False,  # randomly shift images vertically (fraction of total height)
            horizontal_flip = False,  # randomly flip images
            vertical_flip=False)  # randomly flip images


    datagen.fit(x_train)


    model = Sequential()
    model.add(Conv2D(32, 3,padding="same", activation="relu", input_shape=x_train.shape[1:]))
    model.add(MaxPool2D())

    # model.add(Conv2D(64, 3, padding="same", activation="relu"))
    # model.add(MaxPool2D())


    model.add(Conv2D(64, 3, padding="same", activation="relu"))
    model.add(MaxPool2D())
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128,activation="relu"))
    #model.add()
    model.add(Dropout(0.5))
    model.add(Dense(num_labels))

    model.summary()

    opt = Adam(lr=LearningRate)
    model.compile(optimizer = opt , loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True) , metrics = ['accuracy'])

    history = model.fit(x_train,y_train,epochs = ep , validation_data = (x_val, y_val))

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(ep)

    fig = plt.figure(figsize=(15, 15))
    plt.subplot(2, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title(dataType + ' Training and Validation Accuracy')

    plt.subplot(2, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title(dataType + ' Training and Validation Loss')
    plt.show()
    Name = dataType+"AccurracyandErrorPlot.png"
    fig.savefig(Name, transparent=True, bbox_inches='tight')

    model.summary()

    #plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)

    return model, acc, val_acc, loss, val_loss

def TestingNetwrok(model, folderTesting, img_size):
    # img_size = 32
    testData = get_data(folderTesting, img_size)
    x_val = []
    y_val = []

    for feature, label in testData:
      x_val.append(feature)
      y_val.append(label)

    x_val = np.array(x_val) / 255

    x_val.reshape(-1, img_size, img_size, 1)
    y_val = np.array(y_val)

    CAT = ['A', 'B', 'C', 'D', 'E', 'F']

    predictions = model.predict(x_val)
    predictions = np.argmax(predictions,axis=1)
    print(classification_report(y_val, predictions, target_names = CAT))

    confusion_mtx = tf.math.confusion_matrix(y_val, predictions)
    fig1 = plt.figure()
    sns.heatmap(confusion_mtx, xticklabels=CAT, yticklabels=CAT,
                annot=True, fmt='g')
    plt.rc('font', family='Helvetica')
    plt.xlabel('Prediction',fontsize=20)
    plt.ylabel('Label',fontsize=20)
    plt.show()
    return y_val, predictions

def Save_CNN(model, Name):
    json_model = model.to_json()

    with open(Name, 'w') as json_file:
        json_file.write(json_model)