import src.data_preprocessing as data_prep
import src.feature_extraction as feat_extr
import src.buckets_extraction as bucket_ext
import src.train_model as train_model
import src.metrics as metrics
import pickle
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

test_buckets = dict((master, duplicates[-2:])
                    for master, duplicates in buckets.items() if len(buckets[master]) >= 10)
train_buckets = dict((master, duplicates[0:-2] if len(duplicates) >= 10 else duplicates)
                     for master, duplicates in buckets.items())

get_similarity = feat_extr.make_similarity_getter(filtered_bug_reports)
test = get_similarity("1497762", "1497762")


print("Begin: Creating classifier")
if not os.path.isfile("../data/classifier.pickle"):
    classifier = train_model.create_classifier(train_buckets, get_similarity)
    save_pickle("../data/classifier.pickle", classifier)
else:
    classifier = load_pickle("../data/classifier.pickle")
print("End: Creating classifier")

print("Begin: Prediction")

total_tests = 0
top1_guessed = 0
top5_guessed = 0
top10_guessed = 0
rank_list = []

for master, duplicates in test_buckets.items():
    for test_report in duplicates:
        total_tests += 1
        print(f"\nEvaluating report = {test_report.id}, belonging to master:{master.id}")
        candidate_list = bucket_ext.propose_candidate(classifier,
                                                      test_report,
                                                      train_buckets,
                                                      get_similarity)

        print("TOP 100 candidates: ")
        index = 0
        for candidate, probability in candidate_list[0:100]:
            index += 1
            print(f"{index}. Master id: {candidate.id} | probability {probability} ")
            if master.id == candidate.id:
                print(f"----- Found bucket in Top {index}")
                rank_list.append(index)

                if index == 1:
                    top1_guessed += 1
                elif index == 5:
                    top5_guessed += 1
                elif index == 10:
                    top10_guessed += 1

print("End: Prediction")

print("Begin: Metrics")

''' Recall Rate for the Top 1 Rank '''
metrics.recall_rate(top1_guessed, total_tests)
''' Recall Rate for the Top 5 Rank '''
metrics.recall_rate(top5_guessed, total_tests)
''' Recall Rate for the Top 10 Rank '''
metrics.recall_rate(top10_guessed, total_tests)

''' Mean Reciprocal Rank '''
metrics.mean_reciprocal_rank(rank_list, total_tests)

print("End: Metrics")
