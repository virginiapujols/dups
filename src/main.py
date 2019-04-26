import src.data_preprocessing as data_prep
import src.feature_extraction as feat_extr
import src.buckets_extraction as bucket_ext
import pandas
import pickle
import os

import os


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


bug_reports = load_object(pickle_path=r"../data/bug_reports.pickle",
                          method_to_invoke=data_prep.parse_xml_to_bug_reports,
                          args=r"../data/filtered_mozilla_report_2018.xml")

buckets = load_object(pickle_path=r"../data/dict_buckets.pickle",
                      method_to_invoke=bucket_ext.create_buckets,
                      args=bug_reports)
print(bug_reports)

print(buckets)
#Pairs of duplicates
#Pairs of non-duplicates








#
# if not os.path.isfile(r"../data/bug_reports.pickle"):
#     path = r"../data/filtered_mozilla_report_2018.xml"
#     bug_reports = data_prep.parse_xml_to_bug_reports(path)
#     save_pickle(r"../data/bug_reports.pickle", bug_reports)
# else:
#     bug_reports = load_pickle(r"../data/bug_reports.pickle")
#
#
# # pickle for dictionary with bucket
# if not os.path.isfile(r"../data/dict_buckets.pickle"):  # exists
#     tf_idf_data_frame = feat_extr.generate_tf_idf_model(bug_reports)
#     buckets = bucket_ext.create_buckets(bug_reports)
#     save_pickle(r"../data/dict_buckets.pickle", buckets)
# else:
#     buckets = load_pickle(r"../data/dict_buckets.pickle")


# pickle for TF-IDF with bucket









#
# path = r"../data/filtered_mozilla_report_2018.xml"
# bug_reports = data_prep.parse_xml_to_bug_reports(path)
# feat_extr.generate_tf_idf_model(bug_reports)
#
# buckets = bucket_ext.create_buckets(bug_reports)
# pickle_out = open(r"../data/dict_buckets.pickle", 'wb')
# pickle.dump(buckets, pickle_out)
# pickle_out.close()
#
# pickle_in = open(r"../data/dict_buckets.pickle", 'rb')
# saved_buckets = pickle.load(pickle_in)
# print(saved_buckets)
