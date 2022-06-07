import spacy


class SpacyNlp(object):
    def __new__(cls):
        """ creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(SpacyNlp, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.nlp = nlp = spacy.load("en_core_web_trf")

    def get(self):
        return self.nlp
