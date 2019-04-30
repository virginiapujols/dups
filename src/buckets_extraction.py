from sklearn.feature_extraction.text import TfidfVectorizer
import numpy


def create_buckets(report_list):

    masters = list(filter(lambda br: not br.is_duplicate, report_list))
    buckets_dict = dict((m, []) for m in masters)
    duplicates = list(filter(lambda br: br.is_duplicate, report_list))

    for master in buckets_dict:
        duplicate_of_master = [dup for dup in duplicates if dup.duplicate_id == master.id]
        buckets_dict[master] = duplicate_of_master
    return buckets_dict


# def create_candidate_pairs(documents, tfidf_matrix):
#     """
#     Create candidate duplicate pairs between new_bug_report and all the reports in the bucket.
#     Each pair is represented by a vector of features.
#     """
#     candidates = []
#     tf_idf_vectorizer = TfidfVectorizer(sublinear_tf=True)
#
#     list_content_corpus = [br.content_corpus for br in documents]
#     tf_idf_matrix = tf_idf_vectorizer.fit_transform(list_content_corpus).toarray()
#     query_features_vector = tf_idf_matrix[0:1]
#     list_of_documents_features = tf_idf_matrix[1:]
#
#     for doc_features__vector in list_of_documents_features:
#         # candidate_pair = (query_features_vector, doc_features__vector)
#         combined_tfidf = numpy.sum([query_features_vector, doc_features__vector], axis=0)
#         candidates.append(combined_tfidf)
#     return candidates


# def predict_bucket(classifier, new_bug_report, bucket, tfidf_matrix):
#     """
#     Returns the similarity between new_bug_report and a bucket.
#     :param classifier: the SVM discriminative model
#     :param new_bug_report: report with which the query is made
#     :param bucket: list of duplicates of a master
#     :return: the maximum similarity between new_bug_report and each report of the bucket
#     """
#     max_similarity = 0
#     documents = [new_bug_report] + bucket
#     candidates = create_candidate_pairs(documents, tfidf_matrix)
#
#     for features_vector in candidates:  # TODO: pass correct candidate pair
#         # probability = svm_predict(t)
#         # prediction = classifier.predict([[2., 2.]])
#         probability = classifier.predict(features_vector)
#         max_similarity = max(max_similarity, probability)
#
#     return max_similarity


def propose_candidate(classifier, new_bug_report, buckets, get_similarity):
    """
    Returns a duplicate candidate list for a new report.
    Iterates over all the buckets in the repository and calculates
    the similarity between the new report and each bucket.
    :param classifier: the SVM discriminative model
    :param new_bug_report: report with which the query is made
    :param buckets: documents
    :return: a list of masters of which new_bug_report is a likely duplicate
    """
    top_similar_buckets = []
    for master in buckets:
        bucket = buckets[master]
        bucket.append(master)
        max_similarity = 0
        '''
        Create candidate duplicate pairs between new_bug_report and all the reports in the bucket.
        Each pair is represented by a vector of features.
        '''
        # bug_reports_vectors = [get_feature_vector_by_bug_id(b.id) for b in bucket]
        # query_features_vector = get_feature_vector_by_bug_id(new_bug_report.id)
        # candidates = [numpy.sum([query_features_vector, doc_features__vector], axis=0)
        #               for doc_features__vector in bug_reports_vectors]

        candidates = [get_similarity(new_bug_report.id, br.id) for br in bucket]
        ''' Returns the similarity between new_bug_report and a bucket. '''
        for candidate_similarity in candidates:
            '''
            predict_proba returns the probabilities of each class (label) in the classifier as 2D ndarray 
            classifier.classes_ return the classes of the model. 
            
            We are only interested in the probability of the positive class, the class that
            contains the likelihood of a bug report belonging to a bucket. 
            '''
            classifier_classes = classifier.classes_
            positive_class = classifier_classes[1]
            features_matrix = numpy.array([candidate_similarity]).reshape(-1, 1)

            classes_probability = classifier.predict_proba(features_matrix)
            max_similarity = max(max_similarity, classes_probability[0, positive_class])
        top_similar_buckets.append((master, max_similarity))

    return sorted(top_similar_buckets, key=lambda item: item[1], reverse=True)






