from configs import config_seamer as cf
from dataio import UtilsIO as io
from dataio import SkeletonUtils as sk
import os
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

class Gesture:
    """ Gesture class represents and manipulates data about a single repetition """

    def __init__(self):
        """ Create a new point at the origin """
        self.patient_id = ""
        self.date = ""
        self.gesture_type = 0
        self.repetition = 0
        self.correct = 0
        self.position = ""

    def print(self):
        print(self.patient_id,self.date, self.gesture_type, self.repetition, self.correct, self.position)


def split_file_name(file_name):
    data_file = file_name.split("_")

    gesture = Gesture()
    gesture.patient_id = data_file[0]
    gesture.date = data_file[1]
    gesture.gesture_type = data_file[2]
    gesture.repetition = data_file[3]
    gesture.correct = data_file[4]
    gesture.position = data_file[5].split(".")[0]

    return gesture


def data_stats(data, data_info):
    # What is the average length of the correct sequences?
    number_correct = 0
    avg_correct = 0
    number_incorrect = 0
    avg_incorrect = 0

    for i in range(len(data_info)):
        if data_info[i].correct == "1":
            number_correct += 1
            avg_correct += data[i].shape[0]
        if data_info[i].correct == "2":
            number_incorrect += 1
            avg_incorrect += data[i].shape[0]


    avg_correct /= number_correct
    avg_incorrect /= number_incorrect
    print("Number correct", number_correct, " with an average length of ", avg_correct)
    print("Number incorrect", number_incorrect, " with an average length of ", avg_incorrect)


def simple_threshold_classifier(data, data_info, threshold = 150):
    tp = 0
    fp = 0
    tn = 0
    fn = 0

    for i in range(len(data_info)):
        if data[i].shape[0] > threshold:
            if data_info[i].correct == "2":
                tn += 1
            else:
                fn += 1
        else:
            if data_info[i].correct == "2":
                fp += 1
            else:
                tp += 1

    print("TP",tp,"FP",fp,"TN",tn,"FN",fn)
    print("accuracy", (tp+tn)/(tp+tn+fp+fn))


def process_files(path):
    files = io.get_files(path, '(.*txt$)', full_path=False)

    data = []
    data_info = []
    file_names = []

    nr_ignore = 0
    print("Parsing files")
    for f in files:
        full_name = os.path.join(path, f)
        gesture_info = split_file_name(f)
        data_sk, _ = sk.load_skeleton(full_name)
        features = np.zeros((len(data_sk), cf.feature_dim))
        for i in range(len(data_sk)):
            idx = 0
            for key in data_sk[i].keys():
                features[i][idx] = data_sk[i][key][0]
                features[i][idx+1] = data_sk[i][key][1]
                features[i][idx+2] = data_sk[i][key][2]
                idx += 3

        if gesture_info.correct=="3":
            nr_ignore += 1
            continue
        data.append(features)
        data_info.append(gesture_info)
        file_names.append(f)

    print("Number of ignored files", nr_ignore)

    return data, data_info, file_names
