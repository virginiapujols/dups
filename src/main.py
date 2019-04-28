import src.data_preprocessing as data_prep
import src.feature_extraction as feat_extr
import src.buckets_extraction as bucket_ext
import pandas
import pickle
import os
from src import train_model as train_model
import os

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


def save_pickle(pickle_path, to_pickle):
    pickle_out = open(pickle_path, 'wb')
    pickle.dump(to_pickle, pickle_out)
    pickle_out.close()


def load_pickle(pickle_path):
    pickle_in = open(pickle_path, 'rb')
    loaded_object = pickle.load(pickle_in)
    return loaded_object


def load_object(pickle_path, method_to_invoke, args=()):
    if not os.path.isfile(pickle_path):
        obj = method_to_invoke(args)
        save_pickle(pickle_path, obj)
    else:
        obj = load_pickle(pickle_path)
    return obj


filtered_bug_reports = load_object(pickle_path=r"../data/bug_reports.pickle",
                                   method_to_invoke=data_prep.parse_xml_to_bug_reports,
                                   args=r"../data/filtered_mozilla_report_2018.xml")

buckets = load_object(pickle_path=r"../data/dict_buckets.pickle",
                      method_to_invoke=bucket_ext.create_buckets,
                      args=filtered_bug_reports)

for master in buckets:
    report_list = buckets[master]
    if len(report_list) > 10:
        print("bucket: {} - total: {}".format(master.id, len(report_list)))

test_bug_reports = dict((master, duplicates[-2:]) for master, duplicates in buckets.items() if len(buckets[master]) >= 10)
buckets = dict((master, duplicates[0:-2] if len(duplicates) >= 10 else duplicates) for master, duplicates in buckets.items())

print("Begin: Creating classifier")
if not os.path.isfile("../data/classifier.pickle"):
    classifier = train_model.create_classifier(buckets, filtered_bug_reports)
    save_pickle("../data/classifier.pickle", classifier)
else:
    classifier = load_pickle("../data/classifier.pickle")
print("End: Creating classifier")

print("Begin: Prediction")
for master, duplicates in test_bug_reports.items():
    for test_report in duplicates:
        print(f"MASTER:{master.id} - Current bug: {test_report.id}")
        candidate_list = bucket_ext.propose_candidate(classifier, test_report, buckets)
        print("TOP 10 candidates: ", candidate_list[0:10])
        break  # TODO: remove this line
print("End: Prediction")


