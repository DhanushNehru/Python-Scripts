# disable debugging messages
def warn(*args, **kwargs):   
    pass  
import warnings   
warnings.warn = warn  
warnings.filterwarnings("ignore", category=DeprecationWarning)  
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
from silence_tensorflow import silence_tensorflow
silence_tensorflow("WARNING")

import pandas as pd

from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical


def run_training():   # function to run the training process
    dataframe = pd.read_csv('model/output.csv')  # load the processed data from output.csv

    # split the data into features and target variable
    X = dataframe[['length', 'lowercase_count', 'uppercase_count', 'digit_count', 'special_count', 'entropy', 'repetitive_count', 'sequential_count']]  # feature columns
    y = dataframe['strength']  # target variable

    # convert target variable to categorical
    y = to_categorical(y)  # convert labels to categorical format for multi-class classification

    # split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # 80-20 split

    # initialize the model
    model = Sequential()  # create a sequential model
    model.add(Dense(128, activation='relu', input_shape=(X_train.shape[1],)))  # add input layer with 128 neurons
    model.add(Dense(64, activation='relu'))  # add hidden layer with 64 neurons
    model.add(Dense(y.shape[1], activation='softmax'))  # add output layer with softmax activation

    # compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])  # compile the model with adam optimizer

    # train the model
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)  # fit the model on training data

    # save the model to a file
    model.save('model/deep_learning_model.h5')  # save the trained model