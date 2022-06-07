import datetime

from spacy.matcher import Matcher
import re

from natural_language.spacy_nlp import SpacyNlp

nlp = SpacyNlp().get()


def _extract_personop(doc, default_val='or'):
    # matcher klasa spacy do dopasowywania wzorcow do tekstu
    matcher_and = Matcher(nlp.vocab)
    # definicja wzorca
    matcher_and.add('and', [[{"ENT_TYPE": "PERSON"}, {"LEMMA": "and"}, {"ENT_TYPE": "PERSON"}]])
    matches = matcher_and(doc)
    if len(matches) > 0:
        return 'and'
    matcher_or = Matcher(nlp.vocab)
    matcher_or.add('or', [[{"ENT_TYPE": "PERSON"}, {"LEMMA": "or"}, {"ENT_TYPE": "PERSON"}]])
    matches = matcher_and(doc)
    if len(matches) > 0:
        return 'or'
    return default_val


def _tees_convert(text):
    m = re.match(r'(\d+)s', text, re.M | re.I)
    if m:
        year = int(m.group(1))
        if year < 20:
            year += 2000
        else:
            year += 1900;
        return True, [year, year + 9]
    return False, None


def _extract_dates(dates):
    if len(dates) == 2:
        years = []
        is_tees, ys = _tees_convert(dates[0])
        if is_tees:
            years = years + ys
        else:
            years.append(int(re.sub(r'[^\d]', '', dates[0])))
        is_tees, ys = _tees_convert(dates[1])
        if is_tees:
            years = years + ys
        else:
            years.append(int(re.sub(r'[^\d]', '', dates[1])))

        return (datetime.date(min(years), 1, 1), datetime.date(max(years), 12, 31))

    m = re.match(r'[^\d]*(\d+)[^\d]+(\d+)', dates[0], re.M | re.I)
    if m:
        return (datetime.date(int(m.group(1)), 1, 1), datetime.date(int(m.group(2)), 12, 31))

    is_tees, years = _tees_convert(dates[0])
    if is_tees:
        return (datetime.date(years[0], 1, 1), datetime.date(years[1], 12, 31))

    m = re.match(r'(\d+)', dates[0], re.M | re.I)
    if m:
        year = int(m.group(1))
        return (datetime.date(year, 1, 1), datetime.date(year, 12, 31))
    return None, None


class MovieActor:
    def __init__(self):
        self.pattern = [[{"OP": "*"},
                         {"LEMMA": {"IN": ["movie", "film"]}},
                         {"OP": "*"},
                         {"ENT_TYPE": "PERSON"},
                         {"LEMMA": "play"}
                         ],
                        [{"OP": "*"},
                         {"LEMMA": {"IN": ["movie", "film"]}},
                         {"OP": "*"},
                         {"LEMMA": "with"},
                         {"ENT_TYPE": "PERSON"},
                         ],
                        ]
        self.matcher = Matcher(nlp.vocab)
        self.matcher.add(self.__class__.__name__, self.pattern)
        self.persons_ = None
        self.personop_ = None
        self.matches_ = None

    def __repr__(self):
        return f'get_movies_by_actor(persons={self.persons_})'

    def get_results(self):
        return {'match': self.__class__.__name__, 'persons': self.persons_, 'personop': self.personop_}

    def match(self, doc):
        matches = self.matcher(doc)
        if len(matches) == 0:
            return False
        self.matches_ = matches
        persons = []
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                persons.append(ent.text)
        if len(persons) != 0:
            self.persons_ = persons
        if len(persons) > 1:
            self.personop_ = _extract_personop(doc)

        return True


class MovieDirector:
    def __init__(self):
        # Get movies directed by Sylvester Stallone.
        # Get movies by Sylvester Stallone.
        self.pattern = [[{"OP": "*"},
                         {"LEMMA": {"IN": ["movie", "film"]}},
                         {"OP": "*"},
                         {"LEMMA": "by"},
                         {"ENT_TYPE": "PERSON"},
                         ],
                        [{"OP": "*"},
                         {"LEMMA": {"IN": ["movie", "film"]}},
                         {"OP": "*"},
                         {"LEMMA": "directed"},
                         {"LEMMA": "by"},
                         {"ENT_TYPE": "PERSON"},
                         ],
                        ]
        self.matcher = Matcher(nlp.vocab)
        self.matcher.add(self.__class__.__name__, self.pattern)
        self.persons_ = None
        self.personop_ = None
        self.matches_ = None

    def __repr__(self):
        return f'get_movies_by_actor(persons={self.persons_})'

    def get_results(self):
        return {'match': self.__class__.__name__, 'persons': self.persons_, 'personop': self.personop_}

    def match(self, doc):
        matches = self.matcher(doc)
        if len(matches) == 0:
            return False
        self.matches_ = matches
        persons = []
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                persons.append(ent.text)
        if len(persons) != 0:
            self.persons_ = persons
        if len(persons) > 1:
            self.personop_ = _extract_personop(doc)

        return True


class MovieActorDate:
    def __init__(self):
        self.pattern = [[{"OP": "*"},
                         {"LEMMA": {"IN": ["movie", "film"]}},
                         {"OP": "*"},
                         {"ENT_TYPE": "PERSON"},
                         {"LEMMA": "play"},
                         {"OP": "*"},
                         {"ENT_TYPE": "DATE"},
                         ],

                        [{"OP": "*"},
                         {"LEMMA": {"IN": ["movie", "film"]}},
                         {"OP": "*"},
                         {"LEMMA": "with"},
                         {"ENT_TYPE": "PERSON"},
                         {"OP": "*"},
                         {"ENT_TYPE": "DATE"},
                         ],

                        [{"OP": "*"},
                         {"LEMMA": {"IN": ["movie", "film"]}},
                         {"OP": "*"},
                         {"LEMMA": "with"},
                         {"ENT_TYPE": "PERSON"},
                         {"OP": "*"},
                         {"ENT_TYPE": "DATE"},
                         {"OP": "*"},
                         {"ENT_TYPE": "DATE"},
                         ],
                        ]
        self.matcher = Matcher(nlp.vocab)
        self.matcher.add(self.__class__.__name__, self.pattern)
        self.persons_ = None
        self.personop_ = None
        self.date_first_ = None
        self.date_second_ = None
        self.matches_ = None

    def __repr__(self):
        return f'get_movies_by_actor_date(persons={self.persons_},from={self.date_first_},to={self.date_second_})'

    def get_results(self):
        return {'match': self.__class__.__name__, 'persons': self.persons_, 'personop': self.personop_,
                'date_first': self.date_first_, 'date_second': self.date_second_}

    def match(self, doc):
        matches = self.matcher(doc)
        if len(matches) == 0:
            return False
        self.matches_ = matches
        persons = []
        dates = []
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                persons.append(ent.text)
            if ent.label_ == 'DATE':
                dates.append(ent.text)

        if len(persons) > 0:
            self.persons_ = persons
        if len(persons) > 1:
            self.personop_ = _extract_personop(doc)

        if len(dates) >= 1:
            self.date_first_, self.date_second_ = _extract_dates(dates)

        return True


class MovieDirectorDate:
    def __init__(self):
        self.pattern = [[{"OP": "*"},
                         {"LEMMA": {"IN": ["movie", "film"]}},
                         {"OP": "*"},
                         {"LEMMA": "directed", "OP": "?"},
                         {"LEMMA": "by"},
                         {"ENT_TYPE": "PERSON"},
                         {"OP": "*"},
                         {"ENT_TYPE": "DATE"},
                         ],

                        [{"OP": "*"},
                         {"LEMMA": {"IN": ["movie", "film"]}},
                         {"OP": "*"},
                         {"LEMMA": "directed", "OP": "?"},
                         {"LEMMA": "by"},
                         {"ENT_TYPE": "PERSON"},
                         {"OP": "*"},
                         {"ENT_TYPE": "DATE"},
                         {"OP": "*"},
                         {"ENT_TYPE": "DATE"},
                         ],
                        ]
        self.matcher = Matcher(nlp.vocab)
        self.matcher.add(self.__class__.__name__, self.pattern)
        self.persons_ = None
        self.personop_ = None
        self.date_first_ = None
        self.date_second_ = None
        self.matches_ = None

    def __repr__(self):
        return f'get_movies_by_actor_date(persons={self.persons_},from={self.date_first_},to={self.date_second_})'

    def get_results(self):
        return {'match': self.__class__.__name__, 'persons': self.persons_, 'personop': self.personop_,
                'date_first': self.date_first_, 'date_second': self.date_second_}

    def match(self, doc):
        matches = self.matcher(doc)
        if len(matches) == 0:
            return False
        self.matches_ = matches
        persons = []
        dates = []
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                persons.append(ent.text)
            if ent.label_ == 'DATE':
                dates.append(ent.text)

        if len(persons) > 0:
            self.persons_ = persons
        if len(persons) > 1:
            self.personop_ = _extract_personop(doc)

        if len(dates) >= 1:
            self.date_first_, self.date_second_ = _extract_dates(dates)

        return True


if __name__ == "__main__":

    corpus = """Get some cool films in which John Travolta played.
    Films with Andrew Young"""

    corpus = """
Get some cool films in which John Travolta or Arnold Schwarzenegger played in 90s or 80s.
Films with Andrew Young between 1978 and 2022
Films with Kevin Spacey from 1970 to 2020
Find a movie with Bill Hogan and Thomas Lauther from 1998 
Movies directed by Polanski from 1970 to 2020.
Movies by Sylvester Stallone in 90s.
Get movies in which Sylvester Stallone played.
Movies in which Marilyn Monroe played between 1930 and 1950

"""

    corpus = """ Movies in which Marilyn Monroe played between 1930 and 1950 """

    for text in corpus.split('\n'):
        if text == "":
            continue
        doc = nlp(text)
        matchers = [MovieActorDate(), MovieActor(), MovieDirectorDate(), MovieDirector()]
        matched = False
        for m in matchers:
            if m.match(doc):
                print(f'{text}\n{m.get_results()}\n')
                matched = True
                break
        if not matched:
            print(f'{text}\nNO MATCH\n')
# doc = nlp("Movie and movies")
# for t in doc:
#     print(t.text,t.lemma_,t.pos_,t.tag_)
