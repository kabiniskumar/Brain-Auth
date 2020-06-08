import pandas as pd
import pyedflib
import numpy as np
from scipy.fftpack import fft
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import ComplementNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import KFold, ShuffleSplit
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import warnings


def warn(*args, **kwargs):
    pass


warnings.warn = warn

fft_n = 5


def get_data(file):
    data = pyedflib.EdfReader(file)
    signals = data.signals_in_file
    L = data.getNSamples()[0]

    user_data = None
    init = True
    for i in range(signals):
        channel = data.readSignal(i)
        Y = fft(channel)
        P2 = abs(Y / L) * 2
        P1 = P2[0:int(L / 2)+1]
        if init:
            user_data = P1[0:fft_n]
            init = False
        else:
            user_data = np.concatenate((user_data, P1[0:fft_n]))
    user_data_final = user_data.reshape(1, fft_n * signals)[0]
    return user_data_final


labels = []
complete_data = []
f = open("../files/RECORDS", "r")
fp = f.readlines()
for file in fp:
    filename = "dummy/" + str(file).strip()
    user = int(file[1:4])
    labels.append(user)
    feature_mat = get_data(filename)
    complete_data.append(feature_mat)

# Train the model
print(len(labels))
complete_data = pd.DataFrame(complete_data).values
pickle.dump(complete_data, open("test_data.sav", 'wb'))
pickle.dump(labels, open("labels.sav", 'wb'))

labels = np.array(labels)
print("\nSVC\n")
kf = ShuffleSplit(n_splits=5, test_size=0.2)
for train_index, test_index in kf.split(complete_data):
    train, test = complete_data[train_index], complete_data[test_index]
    ltrain, ltest = labels[train_index], labels[test_index]
    clf = SVC(kernel='linear')
    clf = clf.fit(train, ltrain)
    predictions = clf.predict(test)
    accuracy = accuracy_score(ltest, predictions) * 100
    print(accuracy)
    filename = "model_" + str(0) + ".sav"
    pickle.dump(clf, open(filename, 'wb'))

#######################################################

print("\nMLPClassifier\n")
kf = ShuffleSplit(n_splits=5, test_size=0.2)
for train_index, test_index in kf.split(complete_data):
    train, test = complete_data[train_index], complete_data[test_index]
    ltrain, ltest = labels[train_index], labels[test_index]
    neural_network = MLPClassifier(alpha=0.0001, max_iter=400)
    clf = clf.fit(train, ltrain)
    predictions = clf.predict(test)
    accuracy = accuracy_score(ltest, predictions) * 100
    print(accuracy)
    filename = "model_" + str(1) + ".sav"
    pickle.dump(clf, open(filename, 'wb'))


print("\nMultinomial Naive Bayes\n")
kf = ShuffleSplit(n_splits=5, test_size=0.2)
for train_index, test_index in kf.split(complete_data):
    train, test = complete_data[train_index], complete_data[test_index]
    ltrain, ltest = labels[train_index], labels[test_index]
    clf = MultinomialNB()
    clf = clf.fit(train, ltrain)
    predictions = clf.predict(test)
    accuracy = accuracy_score(ltest, predictions) * 100
    print(accuracy)
    filename = "model_" + str(2) + ".sav"
    pickle.dump(clf, open(filename, 'wb'))

print("\nRandom Forest\n")
kf = ShuffleSplit(n_splits=5, test_size=0.2)
for train_index, test_index in kf.split(complete_data):
    train, test = complete_data[train_index], complete_data[test_index]
    ltrain, ltest = labels[train_index], labels[test_index]
    clf = RandomForestClassifier(max_depth=4, n_estimators=150)
    clf = clf.fit(train, ltrain)
    predictions = clf.predict(test)
    accuracy = accuracy_score(ltest, predictions) * 100
    print(accuracy)
    filename = "model_" + str(3) + ".sav"
    pickle.dump(clf, open(filename, 'wb'))


print("\nLogistic Regression\n")
kf = ShuffleSplit(n_splits=5, test_size=0.2)
for train_index, test_index in kf.split(complete_data):
    train, test = complete_data[train_index], complete_data[test_index]
    ltrain, ltest = labels[train_index], labels[test_index]
    clf = LogisticRegression(solver='lbfgs', max_iter=2000)
    clf = clf.fit(train, ltrain)
    predictions = clf.predict(test)
    accuracy = accuracy_score(ltest, predictions) * 100
    print(accuracy)
    filename = "model_" + str(4) + ".sav"
    pickle.dump(clf, open(filename, 'wb'))


print("\nSVC with C\n")
kf = ShuffleSplit(n_splits=5, test_size=0.2)
for train_index, test_index in kf.split(complete_data):
    train, test = complete_data[train_index], complete_data[test_index]
    ltrain, ltest = labels[train_index], labels[test_index]
    clf = SVC(kernel="linear", C=0.025)
    clf = clf.fit(train, ltrain)
    predictions = clf.predict(test)
    accuracy = accuracy_score(ltest, predictions) * 100
    print(accuracy)
    filename = "model_" + str(5) + ".sav"
    pickle.dump(clf, open(filename, 'wb'))
