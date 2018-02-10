from __future__ import division
from sklearn import svm
from sklearn.externals import joblib
from dft import *
from scale import scale
import numpy as np

labels = {
    "hello": 0,
    "my": 1,
    "name": 2,
    "tartan": 3,
    "hacks": 4,
    "whatsup": 5
}

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


def read_data_and_transform(dirpath, thres=0.85):
    output = {}
    

    for sign_folder in os.listdir(dirpath):
        print(sign_folder)
        result = None
        if (sign_folder.startswith('.')):
            continue
        label = labels[sign_folder]
        for example_folder in os.listdir(dirpath + "/" + sign_folder):
            if (example_folder.startswith('.')):
                continue
            for csv_data in os.listdir("{}/{}/{}".format(dirpath, sign_folder, example_folder)):
                current_path = "{}/{}/{}".format(dirpath, sign_folder, example_folder)
                if csv_data.startswith('a'):
                    file_acc = current_path + "/" + csv_data
                if csv_data.startswith('g'):
                    file_gyro = current_path + "/" + csv_data
            assert(file_acc is not None)
            assert(file_gyro is not None)

            gyro_segments = np.array([scale(file_acc, file_gyro, thres)])
            # print(result)
            # print(gyro_segments)
            if result is None:
                result = gyro_segments
            else:
                result = np.concatenate((result, gyro_segments))

            file_acc = None
            file_gyro = None
        output[label] = result
    return output


def time_frame_to_features(time_frame):
    dft_frame = fft(time_frame)
    dc_offset = np.real(find_trans_mean(dft_frame))
    energy = np.real(find_trans_energy(dft_frame))
    entropy = np.real(find_trans_entropy(dft_frame))
    # singal_mean = find_ori_mean(time_frame)
    signal_deviation = np.real(find_ori_deviation(time_frame))
    return (dc_offset, energy, entropy, signal_deviation)


def main():
    # Read data
    # 
    labeled_data = read_data_and_transform("data")

    # Do dtfs and output features
    labeled_features = {}
    for sign, label in labels.items():
        print(label)
        for example in labeled_data[label]:
            dft_features = np.array(list(map(time_frame_to_features, example))).flatten()
            if labeled_features.get(label) is None:
                labeled_features[label] = np.array([dft_features])
            else:
                labeled_features[label] = np.concatenate((labeled_features[label], np.array([dft_features])))
                print(labeled_features[label].size)
                # TODO: we stop here

    assert(False)

    # train model
    # test

