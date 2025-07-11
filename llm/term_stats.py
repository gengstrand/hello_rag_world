import string
from collections import Counter
from flair.data import Sentence, Label
from flair.models import SequenceTagger
from nltk.stem import PorterStemmer

tagger = SequenceTagger.load("flair/pos-english")

def proper_nouns(text: str, min_score: int) -> list[str]:
    p = Sentence(text)
    tagger.predict(p)
    labels = p.get_labels()
    rv = []
    for label in labels:
        if label.value == 'NNP' and label.score >= min_score:
            rv.append(label.text.lower())
    return rv

class TermStats:
    def __init__(self, question: str):
        self._porter = PorterStemmer()
        self._question = Counter([ self._porter.stem(word) for word in proper_nouns(question, 0.5) ])

    def remove_punctuation(self, value: str) -> list[str]:
        no_punctuation = ''.join(ch for ch in value if ch not in string.punctuation)
        return no_punctuation.split(' ')

    def similarity(self, value: str) -> float:
        terms = Counter([ self._porter.stem(term.lower()) for term in self.remove_punctuation(value) ])
        if len(terms) == 0:
            return 0.0
        return sum((self._question[term] * count) for term, count in terms.items()) / sum(terms.values())