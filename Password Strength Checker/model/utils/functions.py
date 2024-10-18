import numpy as np

def calculate_entropy(password):   # function to calculate the entropy of a password
    if len(password) == 0:   # check if the password is empty
        return 0   # return 0 for empty passwords
    char_counts = np.array(list(password))   # convert password to a numpy array
    unique, counts = np.unique(char_counts, return_counts=True)   # get unique characters and their counts
    probabilities = counts / len(password)   # calculate the probability of each character
    entropy = -np.sum(probabilities * np.log2(probabilities))   # compute the entropy using the probabilities
    return entropy  # return the calculated entropy

def count_repeats(password):   # function to count consecutive repeated characters in the password
    return sum(password[i] == password[i + 1] for i in range(len(password) - 1))   # sum the repeated characters

def count_sequential(password):   # function to count sequential characters in the password
    sequences = [''.join(chr(i) for i in range(start, start + 3)) for start in range(ord('a'), ord('z') - 1)]   # generate sequences of 3 lowercase letters
    sequences += [''.join(str(i) for i in range(start, start + 3)) for start in range(10)]   # generate sequences of 3 digits
    return sum(1 for seq in sequences if seq in password)   # count how many of the sequences are in the password