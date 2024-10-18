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
import pickle

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from model.utils.functions import calculate_entropy, count_repeats, count_sequential
from model.utils.preprocessing import run_preprocessing
from model.utils.training import run_training

# run preprocessing and training
# run_preprocessing()  # uncomment to run preprocessing
# run_training()  # uncomment to train the model

def prepare_input(password):  # function to prepare input features from password
    # create a dataframe for a single input
    data = {
        'length': [len(password)],  # calculate password length
        'lowercase_count': [sum(c.islower() for c in password)],  # count lowercase characters
        'uppercase_count': [sum(c.isupper() for c in password)],  # count uppercase characters
        'digit_count': [sum(c.isdigit() for c in password)],  # count digits
        'special_count': [sum(not c.isalnum() for c in password)],  # count special characters
        'entropy': [calculate_entropy(password)],  # calculate entropy
        'repetitive_count': [count_repeats(password)],  # count repetitive characters
        'sequential_count': [count_sequential(password)]  # count sequential characters
    }

    with open('model/scaler.pkl', 'rb') as file:  # load the fitted scaler from file
        scaler = pickle.load(file)
    
    # convert to dataframe
    input_df = pd.DataFrame(data)
    
    # normalize using the previously fitted scaler
    normalized_input = scaler.transform(input_df)
    
    return pd.DataFrame(normalized_input, columns=input_df.columns)  # return normalized input as dataframe

def predict(password):  # function to predict password strength
    # load the model
    model = Sequential()  # create a sequential model
    model.add(Dense(128, activation='relu', input_shape=(8,)))  # add input layer with 128 neurons
    model.add(Dense(64, activation='relu'))  # add hidden layer with 64 neurons
    model.add(Dense(3, activation='softmax'))  # add output layer with softmax activation

    # load trained weights
    model.load_weights('model/deep_learning_model.h5')  # load weights from the trained model file

    # prepare the input
    password_to_test = password  # assign password to test
    input_features = prepare_input(password_to_test)  # prepare input features

    # make the prediction
    prediction = model.predict(input_features, verbose=0)  # predict using the model
    predicted_class = prediction.argmax(axis=-1)  # get the predicted class index

    return predicted_class  # return the predicted class