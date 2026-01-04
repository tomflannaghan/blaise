from abc import ABC, abstractmethod


class Scorer(ABC):
    @abstractmethod
    def score(self, text: str) -> float:
        pass


_default_scorer = None


def as_scorer(scorer) -> Scorer:
    global _default_scorer

    from blaise.scores.ngram import NGramScorer

    if isinstance(scorer, Scorer):
        return scorer
    elif scorer is None:
        if _default_scorer is None:
            _default_scorer = NGramScorer(2, "en_wiki")
        return _default_scorer
    else:
        raise ValueError(f"Unknown scorer: {scorer}")
