from sklearn.feature_extraction.text import TfidfVectorizer


def create_buckets(report_list):
    buckets_dict = {}
    for bug_report in report_list:
        if bug_report.is_duplicate:
            # if it's already in the bucket update the list
            if bug_report.duplicate_id in buckets_dict:
                buckets_dict[bug_report].append(bug_report)
            # else, create a new list with the bug report
            else:
                buckets_dict[bug_report] = [bug_report]

    return buckets_dict


def svm_predict(t):
    # TODO: apply SVM
    return 0


def propose_candidate(new_bug_report, buckets, n_top):
    """
    Returns a duplicate candidate list for a new report.
    Iterates over all the buckets in the repository and calculates
    the similarity between the new report and each bucket.

    :param new_bug_report: report with which the query is made
    :param buckets: documents
    :return: a list of masters of which new_bug_report is a likely duplicate
    """
    top_similar_buckets = []
    for master in buckets:
        bucket = buckets[master]
        bucket.append(master)
        similarity = predict_bucket(new_bug_report, bucket)
        top_similar_buckets.append((master, similarity))

    sorted(top_similar_buckets, key=lambda item: item[1])
    return top_similar_buckets


def predict_bucket(new_bug_report, bucket):
    """
    Returns the similarity between new_bug_report and a bucket.

    :param new_bug_report: report with which the query is made
    :param bucket: list of duplicates of a master
    :return: the maximum similarity between new_bug_report and each report of the bucket
    """
    max_similarity = 0
    documents = [new_bug_report] + bucket
    candidates = create_candidate_pairs(documents)

    for t in candidates:  # TODO: pass correct candidate pair
        probability = svm_predict(t)
        max_similarity = max(max_similarity, probability)
    return max_similarity


def create_candidate_pairs(documents):
    """
    Create candidate duplicate pairs between new_bug_report and all the reports in the bucket.
    Each pair is represented by a vector of features.
    """
    candidates = set()

    tf_idf_vectorizer = TfidfVectorizer(sublinear_tf=True)
    tf_idf_matrix = tf_idf_vectorizer.fit_transform(documents)
    query_features_vector = tf_idf_matrix[0:1]
    list_of_documents_features = tf_idf_matrix[1:]
    for doc_features__vector in list_of_documents_features:
        candidate_pair = (query_features_vector, doc_features__vector)
        candidates.add(candidate_pair)
    return candidates




