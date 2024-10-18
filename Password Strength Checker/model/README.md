# Password Strength Classification Model

## Overview
This model is designed to evaluate the strength of passwords using machine learning techniques. It analyzes input passwords and classifies them based on their strength, providing feedback for users to create stronger passwords.

## Model Architecture
- **Input Layer**: The model accepts passwords as input.
- **Dense Layers**: A series of dense layers with activation functions (e.g., ReLU) process the input features.
- **Output Layer**: The final layer outputs a classification score indicating password strength (e.g., weak - 0, medium - 1, strong - 2).

## Training
- The model is trained on a labeled dataset of passwords classified by strength.

## Future improvements
- In future engineering, columns about the amount of common used passwords (etc. 'password') or common used words should be added and be taken into consideration properly in model training.