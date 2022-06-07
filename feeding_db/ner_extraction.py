import sys

modulename = 'spacy'
nlp = None

if modulename not in sys.modules:
    import spacy
if nlp is None:
    nlp = spacy.load("en_core_web_trf")

from model.named_entity import NamedEntity


def get_nlp():
    return nlp


# def nlp_init():
#     pass

def extract_NERs(text, return_named_entities=True):
    if text is None:
        return []
    doc = nlp(text)
    if return_named_entities:
        ners = [NamedEntity(value=ent.text, tag=ent.label_) for ent in doc.ents]
    else:
        ners = [(ent.text, ent.label_) for ent in doc.ents]
    return ners
