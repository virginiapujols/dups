import src.data_preprocessing as data_prep
import src.feature_extraction as feat_extr
import src.buckets_extraction as bucket_ext
import pandas
import pickle

def test_read_xml_dataset():
    path = "/Users/virginiapujols/Documents/RIT/SEMESTER 4/Data science/FinalProject/bugs_dedupl_data_science/src/data/filtered_mozilla_report_2018.xml"
    reports = data_prep.parse_xml_to_bug_reports(path)
    print(reports[0].id)
    assert reports[0].id != ""
    return reports


def test_tf_idf_features(reports):
    return feat_extr.generate_tf_idf_model(reports)


bug_reports = test_read_xml_dataset()
# result_df = test_tf_idf_features(bug_reports)
# result_df.to_csv('data/tf_idf_data_frame.csv')

buckets = bucket_ext.create_buckets(bug_reports)
pickle_out = open('dict_buckets.pickle', 'wb')
pickle.dump(buckets, pickle_out)
pickle_out.close()

pickle_in = open('dict_buckets.pickle', 'rb')
saved_buckets = pickle.load(pickle_in)
print(saved_buckets)
