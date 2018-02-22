import numpy as np
import matplotlib.pyplot as plt
from bayesian_regressor import BayesianRegressor
from polynomial import PolynomialFeatures
import csv
import arrow

np.random.seed(1234)


def read_in_csv(file_name):
    x_raw = []
    y_raw = []
    x_today = []
    y_today = []
    with open(file_name) as cf:
        reader = csv.DictReader(cf)
        row = reader.__next__()
        x_today.append(arrow.get(row['timestamp']).replace(tzinfo='US/Pacific').timestamp)
        y_today.append(float(row['close']))
        for row in reader:
            timestamp = arrow.get(row['timestamp']).replace(tzinfo='US/Pacific').timestamp
            x_raw.append(timestamp)
            y_raw.append(float(row['close']))
    return np.asarray(x_raw), np.asarray(y_raw), np.asarray(x_today), np.asarray(y_today)


x_all, y_all, x_t, y_t = read_in_csv('GOOG.csv')
x_train = x_all
y_train = y_all
x_test = x_t
y_test = y_t
# x_train = x_all[int(len(x_all)/3):]
# y_train = y_all[int(len(y_all)/3):]
# x_test = x_all[:int(len(x_all)/3)]
# y_test = y_all[:int(len(y_all)/3)]

# for i, degree in enumerate([0, 1, 3, 25]):
degree = 17
feature = PolynomialFeatures(degree)
X_train = feature.transform(x_train)
X_test = feature.transform(x_test)

model = BayesianRegressor(alpha=0.005, beta=11.1)
model.fit(X_train, y_train)

y, y_err = model.predict(X_test, return_std=True)
print('y_t',y_t)
print('y',y)
print('y_err',y_err)
# plt.scatter(x_train, y_train, facecolor="none", edgecolor="b", s=5, label="training data")
plt.plot(x_train, y_train, c="b")
plt.plot(x_test, y_test, c="g", label="$\sin(2\pi x)$")
plt.plot(x_test, y, c="r", label="mean")
# plt.plot(x_test,y_err,c="r")
plt.fill_between(x_test, y - y_err, y + y_err, color="pink", label="std.", alpha=0.5)
plt.xlim(1393191545, arrow.utcnow().to('US/Pacific').timestamp)
plt.ylim(0,1500)
plt.annotate("M=9", xy=(0.8, 1))
plt.legend(bbox_to_anchor=(1.05, 1.), loc=2, borderaxespad=0.)
plt.show()