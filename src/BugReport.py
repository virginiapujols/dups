class BugReport:

    def __init__(self, report_id, description, duplicate_id=None, corpus=None):
        self.id = report_id
        self.description = description
        self.content_corpus = corpus
        self.duplicate_id = duplicate_id
        if duplicate_id is not None:
            self.is_duplicate = True
        else:
            self.is_duplicate = False

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
