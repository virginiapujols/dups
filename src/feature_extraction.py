import pandas as pd
import math
from sklearn.feature_extraction.text import TfidfVectorizer


def get_stop_words():
    with open('../data/stop-words.txt', 'r') as file:
        return file.read().splitlines()


def get_documents_unique_terms(bug_documents):
    unique_terms = set()
    for report in bug_documents:
        corpus = report.content_corpus
        unique_terms.update(corpus)
    return unique_terms


def generate_tf_idf_model(bug_documents):
    document_columns = dict()
    unique_terms = get_documents_unique_terms(bug_documents)
    for report in bug_documents:
        corpus = report.content_corpus
        term_count = [(1 + math.log10(corpus.count(term))) * get_idf(term, bug_documents)
                      if corpus.count(term) > 0 else 0
                      for term in unique_terms
                      ]
        document_columns[report.id] = term_count

    tf_idf_data_frame = pd.DataFrame(data=document_columns, index=list(unique_terms))
    return tf_idf_data_frame


def get_idf(term, bug_documents):
    document_freq = 0  # the number of documents that 'term' occurs in.
    for report in bug_documents:
        if report.content_corpus.count(term) != 0:
            document_freq += 1

    total_docs = len(bug_documents)  # the number of documents in the collection.
    inverse_doc_freq = math.log10(total_docs / document_freq)
    return inverse_doc_freq


def extract_features_tf(list_content_corpus):
    print('Only TF')
    tfidf_vectorizer = TfidfVectorizer(sublinear_tf=True, use_idf=False)
    tfidf_matrix = tfidf_vectorizer.fit_transform(list_content_corpus)
    return tfidf_matrix.toarray()


def extract_features_idf(list_content_corpus):
    print('Only IDF')
    tfidf_vectorizer = TfidfVectorizer(sublinear_tf=True, use_idf=True)
    tfidf_matrix = tfidf_vectorizer.fit_transform(list_content_corpus)
    idf_matrix = tfidf_vectorizer.idf_
    return [idf_matrix]


def extract_features_tf_idf(list_content_corpus):
    # print('Both')
    tfidf_vectorizer = TfidfVectorizer(sublinear_tf=True)
    tfidf_matrix = tfidf_vectorizer.fit_transform(list_content_corpus)
    return tfidf_matrix.toarray()


def extract_features(filtered_bug_reports):
    list_content_corpus = [br.content_corpus for br in filtered_bug_reports]
    print("Begin: Creating TF-IDF")
    matrix = extract_features_tf_idf(list_content_corpus)
    print("End: Creating TF-IDF")
    return matrix


def make_feature_vector_getter(filtered_bug_reports):
    tfidf_matrix = extract_features(filtered_bug_reports)
    bug_report_dict = dict((br.id, i) for i, br in enumerate(filtered_bug_reports))
    return lambda bug_id: get_feature_vector_by_bug_id(bug_id, bug_report_dict, tfidf_matrix)


def get_feature_vector_by_bug_id(bug_id, bug_report_dict, tfidf_matrix):
    pos = bug_report_dict[bug_id]
    tfidf_vector = tfidf_matrix[pos]
    return tfidf_vector


def bug_report_sim(bug_id1, bug_id2, bug_report_dict, tfidf_matrix, idf_vector):
    vector1 = get_feature_vector_by_bug_id(bug_id1, bug_report_dict, tfidf_matrix)
    vector2 = get_feature_vector_by_bug_id(bug_id2, bug_report_dict, tfidf_matrix)

    similarities = [idf_vector[i] for i, (member_vector_1, member_vector_2)
                    in enumerate(zip(vector1, vector2))
                    if member_vector_1 != 0 and member_vector_2 != 0]

    similarity = sum(similarities)

    return similarity


def make_similarity_getter(filtered_bug_reports):
    list_content_corpus = [br.content_corpus for br in filtered_bug_reports]
    tfidf_vectorizer = TfidfVectorizer(sublinear_tf=True)
    tfidf_matrix = tfidf_vectorizer.fit_transform(list_content_corpus).toarray()
    idf_vector = tfidf_vectorizer.idf_
    bug_report_dict = dict((br.id, i) for i, br in enumerate(filtered_bug_reports))

    return lambda bug_id1, bug_id2: \
        bug_report_sim(bug_id1, bug_id2, bug_report_dict, tfidf_matrix, idf_vector)











