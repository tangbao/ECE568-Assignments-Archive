import numpy as np
import matplotlib.pyplot as plt
from bayesian_regressor import BayesianRegressor
from polynomial import PolynomialFeatures
import csv
import arrow

alpha = 0.005
beta = 11.1
degree = 9

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
        time_last = arrow.get(row['timestamp']).replace(tzinfo='US/Pacific').timestamp
        x_raw = [int((i-time_last)/86400) for i in x_raw]
        x_today = [int((x_today[0]-time_last)/86400)]
    return np.asarray(x_raw), np.asarray(y_raw), np.asarray(x_today), np.asarray(y_today)

x_all, y_all, x_t, y_t = read_in_csv('./datasets/GOOG.csv')
x_train = x_all
y_train = y_all
x_test = x_all
y_test = y_all

def phi(x):
    phi = [x**i for i in range(degree + 1)]
    return np.asarray(phi)

#formula (1.72)
def S():
    S_inv = alpha*np.identity(degree+1) + beta*np.sum([phi(x).dot(phi(x).T) for x in x_train], axis=0)
    S = np.linalg.inv(S_inv)
    return S

#formula (1.70)
def mx(x):
    return beta*(phi(x).T).dot(S()).dot(np.sum([phi(xt)*t for xt, t in zip(x_train, y_train)], axis=0))

#formula (1.71)
def s2x(x):
    return 1/beta+ (phi(x).T).dot(S()).dot(phi(x))

# formula (1.69)
def Gaussian(xx, mx, s2x):
    # miu = mx[0]
    # sigma2 = s2x[0][0]
    print(2*np.pi*s2x)
    term1 = 1/np.sqrt(2*np.pi*s2x)
    term2 = -1/(2*s2x)*(xx-mx)**2
    return term1*np.exp(term2)

a=s2x(x_train)
b=mx(x_train)
print(a)
Gaussian(x_train,b,a)

# x_train = x_all[int(len(x_all)/3):]
# y_train = y_all[int(len(y_all)/3):]
# x_test = x_all[:int(len(x_all)/3)]
# y_test = y_all[:int(len(y_all)/3)]

feature = PolynomialFeatures(degree)
X_train = feature.transform(x_train)
X_test = feature.transform(x_test)

model = BayesianRegressor(alpha=0.005, beta=11.1)
model.fit(X_train, y_train)

y, y_err = model.predict(X_test, return_std=True)
# print('x_t',x_t)
# print('y_t',y_t)
# print('y',y)
# print('y_err',y_err)

# plt.scatter(x_train, y_train, facecolor="none", edgecolor="b", s=5, label="training data")
plt.plot(x_train, y_train, c="b")
# plt.plot(x_test, y_test, c="g", label="$\sin(2\pi x)$")


plt.plot(x_test, y, c="r", label="mean")
# plt.scatter(x_test,y,facecolor = "none", edgecolor="b",s=50)

plt.fill_between(x_test, y - y_err, y + y_err, color="pink", label="std.", alpha=0.5)
# plt.xlim(0,1500)
# plt.ylim(300,1400)


#sin函数的范围
# plt.xlim(-0.1, 1.1)
# plt.ylim(-1.5, 1.5)

# 图例喝M = 9
# plt.annotate("M=9", xy=(0.8, 1))
# plt.legend(bbox_to_anchor=(1.05, 1.), loc=2, borderaxespad=0.)
plt.show()
