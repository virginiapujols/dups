import src.data_preprocessing as data_prep
import src.feature_extraction as feat_extr
import src.buckets_extraction as bucket_ext
import pandas
import pickle
import os

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

sample_bug_report = filtered_bug_reports[0]

sample_master = list(buckets.keys())[3]
sample_bucket = buckets[sample_master]
sample_bucket_corpus = [bug.content_corpus for bug in sample_bucket]
bucket_ext.predict_bucket(sample_bug_report.content_corpus, sample_bucket_corpus)












# clf = SVC(kernel='linear')
# clf.fit(x_train,y_train)
# y_pred = clf.predict(x_test)
# print(accuracy_score(y_test,y_pred))



