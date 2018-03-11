import numpy as np
import matplotlib.pyplot as plt
import csv
import arrow

alpha = 5e-3
beta = 11.1
degree = 7

data_folder = './datasets'
data_files = ['GOOG_0.csv', 'GOOG_1.csv', 'GOOG_2.csv', 'GOOG_3.csv'
    , 'GOOG_4.csv', 'GOOG_5.csv', 'GOOG_6.csv', 'GOOG_7.csv', 'GOOG_8.csv', 'GOOG_9.csv'
    , 'GOOG_10.csv']

# data_files = ['test1.csv', 'test2.csv', 'test3.csv', 'test4.csv', 'test5.csv']
# data_files = ['test4.csv']

absolute_err_all = []
relative_err_all = []


def read_in_csv(file_name):
    x_raw = []
    y_raw = []
    x_today = []
    y_today = []
    with open(file_name) as cf:
        reader = csv.DictReader(cf)
        row = reader.__next__()
        # get timestamp and the price of close today
        x_today.append(arrow.get(row['timestamp']).replace(tzinfo='US/Pacific').timestamp)
        y_today.append(float(row['close']))
        for row in reader:
            # get timestamp and the price of close every day before
            timestamp = arrow.get(row['timestamp']).replace(tzinfo='US/Pacific').timestamp
            x_raw.append(timestamp)
            y_raw.append(float(row['close']))
        # get the earliest timestamp
        time_earliest = arrow.get(row['timestamp']).replace(tzinfo='US/Pacific').timestamp
        # calculate the number of days from the earliest day
        x_raw = [int((i-time_earliest)/86400) for i in x_raw]
        x_today = [int((x_today[0]-time_earliest)/86400)]
    return np.asarray(x_raw), np.asarray(y_raw), np.asarray(x_today), np.asarray(y_today)


def phi(x):
    phi = [[x**i] for i in range(degree + 1)]
    return np.asarray(phi)


# formula (1.70), mean
def mx(x):
    return beta*(phi(x).T).dot(S).dot(np.sum([t*phi(xt) for xt, t in zip(x_train, y_train)], axis=0))[0][0]


# formula (1.71), variance
def s2x(x):
    return (1/beta + (phi(x).T).dot(S.dot(phi(x))))[0][0]


for data_file in data_files:
    print(data_file)
    data_name = data_folder + '/' + data_file
    x_all, y_all, x_t, y_t = read_in_csv(data_name)
    '''
    # x_train = x_all[int(len(x_all)/3):]
    # y_train = y_all[int(len(y_all)/3):]
    # x_test = x_all[:int(len(x_all)/3)]
    # y_test = y_all[:int(len(y_all)/3)]
    '''
    # x_train = x_all[::-1]
    # y_train = y_all[::-1]
    N = len(x_all)
    x_train = np.arange(0, 1.0, 1.0 / N)
    y_train = y_all[::-1]
    x_test = np.arange(0, 1.0 + 1.0 / N, 1.0 / N)

    # formula (1.72)
    S_inv = alpha * np.identity(degree + 1) + beta * np.sum([phi(x).dot(phi(x).T) for x in x_train], axis=0)
    S = np.linalg.inv(S_inv)

    # plt.plot(x_test, [mx(x) for x in x_test], color='0')
    # for x, t in zip(x_train, y_train):
    #     plt.scatter(x, t, color='b')

    predict_v = mx(x_test[-2])
    variance = s2x(x_test[-2])
    print("The prediction of N+1 time is", predict_v, "+-", variance)
    print("The real value is", y_t)

    absolute_err = abs(y_t-predict_v)
    relative_err = absolute_err/y_t
    absolute_err_all.append(absolute_err)
    relative_err_all.append(relative_err)

    print("The absolute error is", absolute_err)
    print("The relative error is", relative_err)

    print()
    # plt.show()


absolute_mean_err = np.average(absolute_err_all)
ave_relative_err = np.average(relative_err_all)

print("The overall absolute mean error is ", absolute_mean_err)
print("The overall average relative error is ", ave_relative_err)
