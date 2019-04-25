import nltk
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import xml.etree.ElementTree as ET
from src.BugReport import BugReport


lemmatizer = WordNetLemmatizer()
tokenizer = TweetTokenizer()


def stop_words_list():
    with open('data/stop-words.txt', 'r') as file:
        return file.read().splitlines()


def tokenize(sentence):
    word_tokens = tokenizer.tokenize(sentence)
    return word_tokens


def get_lemma_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def preprocess(document):
    standard_stop_words = stop_words_list()

    document = document.replace("/'", " ")
    token_words = tokenize(document)
    token_words = [i.lower() for i in token_words]
    tagged_words = nltk.pos_tag(token_words)

    lemmatized_words = []
    print('------------------------------------')
    print("{0:20}{1:20}".format("Word", "Lemma"))
    print('------------------------------------')
    for tag in tagged_words:
        w = tag[0]
        type = tag[1]

        if w in standard_stop_words:
            continue

        # Keep the lemma of each word
        lemma = lemmatizer.lemmatize(w, pos=get_lemma_pos(type))
        lemmatized_words.append(lemma)
        print("{0:20}{1:20}".format('-'.join(tag), lemma))

    return lemmatized_words


def parse_xml_to_bug_reports(dataset_xml_path):
    tree = ET.parse(dataset_xml_path)
    root = tree.getroot()
    reports = []
    for bug_element in root.findall('bug'):
        bug_id = bug_element.find('bug_id').text
        bug_content_desc = bug_element.find('short_desc').text + " "

        for info in bug_element.findall('long_desc'):
            if info.find('thetext').text is not None:
                bug_content_desc += info.find('thetext').text + " "

        dupl_id = None
        if bug_element.find('dup_id') is not None:
            dupl_id = bug_element.find('dup_id').text

        document_corpus = preprocess(bug_content_desc)

        bug_obj = BugReport(bug_id, bug_content_desc, dupl_id, document_corpus)
        reports.append(bug_obj)
    return reports
