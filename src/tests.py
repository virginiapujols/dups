import src.data_preprocessing as data_prep
import src.feature_extraction as feat_extr
import pandas


def test_read_xml_dataset():
    path = "/Users/virginiapujols/Documents/RIT/SEMESTER 4/Data science/FinalProject/bugs_dedupl_data_science/src/data/test_reports.xml"
    reports = data_prep.parse_xml_to_bug_reports(path)
    print(reports[0].id)
    assert reports[0].id != ""
    return reports


def test_tf_idf_features(reports):
    return feat_extr.generate_tf_idf_model(reports)


bug_reports = test_read_xml_dataset()
result_df = test_tf_idf_features(bug_reports)
result_df.to_csv('data/tf_idf_data_frame.csv')

