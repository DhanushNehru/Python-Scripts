import pandas as pd
import pickle

from model.utils.functions import calculate_entropy, count_repeats, count_sequential
from sklearn.preprocessing import StandardScaler

def run_preprocessing():
    # import data
    dataframe = pd.read_csv('model/passwords.csv', on_bad_lines='skip')   # read csv data file
    dataframe = dataframe.dropna()   # remove rows with empty values
    dataframe = dataframe.drop_duplicates(subset='password')   # remove duplicates

    # add new columns
    dataframe['length'] = dataframe['password'].str.len()   # column for password length
    dataframe['lowercase_count'] = dataframe['password'].apply(lambda x: sum(c.islower() for c in x))   # column for amount of lowercase characters
    dataframe['uppercase_count'] = dataframe['password'].apply(lambda x: sum(c.isupper() for c in x))   # column for amount of uppercase characters
    dataframe['digit_count'] = dataframe['password'].apply(lambda x: sum(c.isdigit() for c in x))   # column for amount of digits
    dataframe['special_count'] = dataframe['password'].apply(lambda x: sum(not c.isalnum() for c in x))   # column for amount of special characters
    dataframe['entropy'] = dataframe['password'].apply(calculate_entropy)  # column for entropy
    dataframe['repetitive_count'] = dataframe['password'].apply(count_repeats)  # column for amount of repetitive characters
    dataframe['sequential_count'] = dataframe['password'].apply(count_sequential)  # column for amount of sequential characters

    scaler = StandardScaler()   # use standard scaler because there is a gaussian distribution in passwords.csv
    numerical_features = ['length', 'lowercase_count', 'uppercase_count', 'digit_count', 'special_count', 'entropy', 'repetitive_count', 'sequential_count']
    dataframe[numerical_features] = scaler.fit_transform(dataframe[numerical_features])

    # save scaler model for future use
    with open('model/scaler.pkl', 'wb') as file:
        pickle.dump(scaler, file)

    # save preprocessed data
    dataframe.to_csv('model/output.csv', index=False, header=True)