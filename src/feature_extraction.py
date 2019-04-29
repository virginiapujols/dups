import pandas as pd
import math
from sklearn.feature_extraction.text import TfidfVectorizer

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


def extract_features(filtered_bug_reports):
    list_content_corpus = [br.content_corpus for br in filtered_bug_reports]
    print("Begin: Creating TF-IDF")
    tfidf_vectorizer = TfidfVectorizer(sublinear_tf=True)
    tfidf_matrix = tfidf_vectorizer.fit_transform(list_content_corpus).toarray()
    print("End: Creating TF-IDF")
    return tfidf_matrix


def make_feature_vector_getter(filtered_bug_reports):
    tfidf_matrix = extract_features(filtered_bug_reports)
    bug_report_dict = dict((br.id, i) for i, br in enumerate(filtered_bug_reports))

    def get_feature_vector_by_bug_id(bug_id):
        pos = bug_report_dict[bug_id]
        tfidf_vector = tfidf_matrix[pos]
        return tfidf_vector
    return get_feature_vector_by_bug_id
