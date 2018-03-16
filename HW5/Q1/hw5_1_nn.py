'''

A neural network using backpropagtion (with gradient descent) to train the XOR function.

One input layer with two units, one hidden layer with two units, one output layer with one unit.

{ (x1, x2, t) | x1, x2 ∈ {0, 1}, and t = x1⨁x2 } = {(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)}

'''

import numpy as np
import time


input_unit_num = 2
hidden_unit_num = 2
output_unit_num = 1
# training data
X = [[0, 0], [0, 1], [1, 0], [1, 1]]
Y = [[0], [1], [1], [0]]
m = 4  # training data size


# activate function
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def sigmoid_gradient(z):
    return sigmoid(z)*(1-sigmoid(z))


def random_init_weight(l_in, l_out):
    epsilon_init = np.sqrt(6) / np.sqrt(l_in + l_out)
    rand_seed = np.random.RandomState(int(round(time.time())))
    w = rand_seed.rand(l_out, 1 + l_in) * 2 * epsilon_init - epsilon_init
    return np.asarray(w)


def train(theta_1, theta_2):
    # forward propagation
    a1 = X
    a1 = np.concatenate((np.ones((m, 1)), a1), axis=1)
    z2 = np.dot(np.asarray(a1), theta_1.T)
    a2 = sigmoid(z2)
    a2 = np.concatenate((np.ones((m, 1)), a2), axis=1)
    z3 = np.dot(np.asarray(a2), theta_2.T)
    a3 = sigmoid(z3)

    # compute cost
    cost = np.asarray(Y) * np.log(a3) + (1 - np.asarray(Y)) * np.log(1 - a3)
    J = -np.sum(cost) / m

    # back propagation
    delta3 = a3 - np.asarray(Y)
    delta2 = (delta3 * theta_2)[:, 2:] * sigmoid_gradient(z2)
    Delta1 = np.dot(delta2.T, a1)
    Delta2 = np.dot(delta3.T, a2)
    theta1_grad = Delta1 / m
    theta2_grad = Delta2 / m
    return J, theta1_grad, theta2_grad


def gradient_descent(learning_rate, target_error, theta1, theta2):
    J, theta1_grad, theta2_grad = train(theta1, theta2)
    print("The first batch error is ", J)
    cnt = 0
    while J >= target_error:
        theta1 = theta1 - theta1_grad * learning_rate
        theta2 = theta2 - theta2_grad * learning_rate
        J, theta1_grad, theta2_grad = train(theta1, theta2)
        cnt = cnt + 1
        # print(J)
    return J, theta1, theta2, cnt


def predict(x, theta1, theta2):
    a1 = x
    a1 = np.concatenate((np.ones((m, 1)), a1), axis=1)
    z2 = np.dot(np.asarray(a1), theta1.T)
    a2 = sigmoid(z2)
    a2 = np.concatenate((np.ones((m, 1)), a2), axis=1)
    z3 = np.dot(np.asarray(a2), theta2.T)
    a3 = sigmoid(z3)
    print(a3)


def main():
    # learning_rate = input("Please input learning rate: ")
    # target_error = input("Plase input target error: ")
    learning_rate = 0.5
    target_error = 0.02
    theta1_init = random_init_weight(input_unit_num, hidden_unit_num)
    theta2_init = random_init_weight(hidden_unit_num, output_unit_num)
    print("The init weights Theta_1 is ", theta1_init)
    print("The init weights Theta_2 is ", theta2_init)
    J, theta1, theta2, cnt = gradient_descent(learning_rate, target_error, theta1_init, theta2_init)
    print("The final weights Theta_1 is ", theta1)
    print("The final weights Theta_2 is ", theta2)
    print("The final error is ", J)
    print("the total number of batches run is ", cnt)
    print("The prediction of [0, 0], [0, 1], [1, 0], [1, 1] is:")
    predict(X, theta1, theta2)


if __name__ == '__main__':
    main()

