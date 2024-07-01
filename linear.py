import numpy as np
import pandas as pd

# Load the dataset
data = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv', delimiter=';')

# Extract the features and target variable
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values.reshape(-1, 1)

# Add a column of ones to X for the intercept term
X = np.hstack((np.ones((X.shape[0], 1)), X))

# Define the cost function
def cost_function(X, y, theta):
    m = len(y)
    J = np.sum((X.dot(theta) - y) ** 2)/(2 * m)
    return J

# Define the gradient descent function
def gradient_descent(X, y, theta, alpha, num_iters):
    m = len(y)
    J_history = np.zeros((num_iters, 1))
    for i in range(num_iters):
        theta = theta - (alpha/m) * X.T.dot(X.dot(theta) - y)
        J_history[i] = cost_function(X, y, theta)
    return theta, J_history

# Initialize theta parameters
theta = np.zeros((X.shape[1], 1))

# Define hyperparameters
alpha = 0.0001
num_iters = 1000

# Run gradient descent
theta, J_history = gradient_descent(X, y, theta, alpha, num_iters)

# Print the coefficients and intercept
print('Coefficients: ', theta[1:])
print('Intercept: ', theta[0])