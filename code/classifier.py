from sklearn import svm
from sklearn.externals import joblib


def predict(clf, X):
    # clf is the classifier
    # X is a 2D list [[X1],[X2]]
    clf.predict(X)


def train(X, y):
    # y being the labels
    clf = svm.SVC()
    clf.fit(X, y)
    return clf


def save_model(clf, path=""):
    # TODO set path
    joblib.dump(clf, 'model.pkl')


def load_model(path=""):
    return joblib.load('model.pkl')

##
## Data processing
##


def generate_feature(data):
    # data is 2*2 