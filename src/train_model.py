import random
import numpy
from sklearn import svm


"""
Generic steps to produce a classifier

INPUT: buckets
Generate pairs of duplicates
Generate pairs of non-duplicates

Generate feature vector of duplicates
Generate feature vector of non-duplicates

Train using SVM

OUTPUT: return classifier (discriminative model)
"""


def generate_pair_of_duplicates(buckets):
    """
    To create positive examples, for each bucket, we perform
    the following:
        1. Create the pair (master, duplicate), where duplicate is
        one of the duplicates in the bucket and master is the
        original report in the bucket. [We implement this approach]
        2. Create the pairs (duplicate1,duplicate2) where the two
        duplicates belong to the same bucket. [TODO: alternative approach]
    Paper: A Discriminative Model Approach for Accurate Duplicate Bug Report Retrieval
    :param buckets: dictionary of masters (key) with its duplicate bug reports (value).
    :return: Tuples of duplicates (dup1, dup2)
    """
    pair_of_duplicates = []
    for master in buckets:
        duplicates = buckets[master]
        for duplicate in duplicates:
            pair_of_duplicates.append((master, duplicate))

    return pair_of_duplicates


def generate_pair_of_non_duplicates(buckets):
    """
    To create negative examples, one could pair one report
    from one bucket with another report from the another bucket.
    Paper: A Discriminative Model Approach for Accurate Duplicate Bug Report Retrieval

    :param buckets: dictionary of masters (key) with its duplicate bug reports (value).
    :return: Tuples of non-duplicates (dup1 of a bucket, dup2 of a different bucket)

    The variable 'pair_of_non_duplicates' allows for repeated values.

    the 'count' variable limits the amount of members in the pair_of_non_duplicates
    list that in this case will be the total number of duplicates in
    all buckets.

    """
    count = len(buckets.keys())
    for master in buckets:
        count += len(buckets[master])

    pair_of_non_duplicates = []
    keys = buckets.keys()
    while count is not 0:
        random_keys = random.sample(keys, 2)
        bucket_list1 = buckets[random_keys[0]]
        bucket_list2 = buckets[random_keys[1]]

        dup_pair1 = random.choice(bucket_list1)
        dup_pair2 = random.choice(bucket_list2)

        non_dup_pair = (dup_pair1, dup_pair2)

        pair_of_non_duplicates.append(non_dup_pair)
        count -= 1

    return pair_of_non_duplicates


def create_classifier(buckets, get_feature_vector_by_bug_id):
    pair_of_duplicates = generate_pair_of_duplicates(buckets)
    pair_of_non_duplicates = generate_pair_of_non_duplicates(buckets)
    print("Begin: Create feature vectors")
    tfidf_sum = []
    merged_pairs = pair_of_duplicates + pair_of_non_duplicates
    for dup1, dup2 in merged_pairs:
        # position_dup1 = bug_report_dict[dup1.id]
        # position_dup2 = bug_report_dict[dup2.id]
        #
        # tfidf_dup1 = tfidf_matrix[position_dup1]
        # tfidf_dup2 = tfidf_matrix[position_dup2]
        tfidf_dup1 = get_feature_vector_by_bug_id(dup1.id)
        tfidf_dup2 = get_feature_vector_by_bug_id(dup2.id)

        combined_tfidf = numpy.sum([tfidf_dup1, tfidf_dup2], axis=0)
        tfidf_sum.append(combined_tfidf)
    print("End: Create feature vectors")
    print("Begin: Train model")
    # features_labels creates a combined list of labels where 1 represents duplicates and 0 represent non-duplicates.
    features_labels = len(pair_of_duplicates) * [1] + len(pair_of_non_duplicates) * [0]
    features_matrix = tfidf_sum

    classifier = svm.SVC(kernel='linear', probability=True, verbose=True, max_iter=1)
    classifier.fit(features_matrix, features_labels)
    print("End: Train model")
    return classifier

