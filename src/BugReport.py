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

    def __eq__(self, o):
        return isinstance(o, BugReport) and \
               self.id == o.id

    def __hash__(self):
        return hash(self.id)
