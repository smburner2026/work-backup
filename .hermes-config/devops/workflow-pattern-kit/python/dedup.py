"""
dedup — Duplicate detection for workflow outputs.

Provides:
  - Dedup: token-cosine and Jaccard similarity-based duplicate detection
  - DedupResult: typed result container

Usage:
    from dedup import Dedup, DedupResult

    dedup = Dedup(duplicate_threshold=0.62)
    result = dedup.token_cosine("some text", "some other text")
    if result.is_duplicate:
        print(f"Duplicates: score={result.score:.2f}")
"""

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DedupResult:
    """Result of a deduplication comparison between two strings.

    Attributes:
        is_duplicate: True if the similarity score >= duplicate_threshold.
        score: The computed similarity score (0.0 to 1.0).
        matched_with: The reference string this was compared against, or None.
        possible_duplicates: Any strings that fell between possible_threshold
            and duplicate_threshold.
    """
    is_duplicate: bool = False
    score: float = 0.0
    matched_with: Optional[str] = None
    possible_duplicates: List[str] = field(default_factory=list)


def _tokenize(text: str) -> List[str]:
    """Split *text* on whitespace and punctuation, returning lowercase tokens.

    Uses a regex that matches sequences of word characters (\\w+), which
    includes letters, digits, and underscores. This naturally strips
    punctuation and whitespace.
    """
    return re.findall(r"\w+", text.lower())


class Dedup:
    """Duplicate detector using token-based similarity metrics.

    Thresholds:
        duplicate_threshold: Minimum cosine/Jaccard score to classify as
            a duplicate (default: 0.62).
        possible_threshold: Minimum score to flag as a *possible* duplicate
            (default: 0.40). Scores below this are considered clean.
    """

    def __init__(self, duplicate_threshold: float = 0.62, possible_threshold: float = 0.40):
        if not 0.0 <= duplicate_threshold <= 1.0:
            raise ValueError(f"duplicate_threshold must be in [0, 1], got {duplicate_threshold}")
        if not 0.0 <= possible_threshold <= 1.0:
            raise ValueError(f"possible_threshold must be in [0, 1], got {possible_threshold}")
        if possible_threshold > duplicate_threshold:
            raise ValueError(
                f"possible_threshold ({possible_threshold}) must be ≤ "
                f"duplicate_threshold ({duplicate_threshold})"
            )
        self.duplicate_threshold = duplicate_threshold
        self.possible_threshold = possible_threshold

    @staticmethod
    def token_cosine(text_a: str, text_b: str) -> float:
        """Compute token-cosine similarity between *text_a* and *text_b*.

        Tokenization splits on whitespace and punctuation, lowercasing all
        tokens. Cosine similarity is computed as:

            cos = dot(a, b) / (||a|| * ||b||)

        where each vector is a Counter of token frequencies.

        Returns a float in [0.0, 1.0]. Returns 0.0 if either string is empty.
        """
        tokens_a = _tokenize(text_a)
        tokens_b = _tokenize(text_b)

        if not tokens_a or not tokens_b:
            return 0.0

        counter_a = Counter(tokens_a)
        counter_b = Counter(tokens_b)

        # Dot product: sum of products of overlapping token counts
        dot_product = 0.0
        for token, count_a in counter_a.items():
            count_b = counter_b.get(token, 0)
            dot_product += count_a * count_b

        # Norms
        norm_a = math.sqrt(sum(c * c for c in counter_a.values()))
        norm_b = math.sqrt(sum(c * c for c in counter_b.values()))

        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    @staticmethod
    def jaccard(text_a: str, text_b: str) -> float:
        """Compute Jaccard similarity between *text_a* and *text_b*.

        Jaccard = |intersection| / |union| over token sets (unique tokens).

        Returns a float in [0.0, 1.0]. Returns 0.0 if both strings are empty.
        """
        set_a = set(_tokenize(text_a))
        set_b = set(_tokenize(text_b))

        if not set_a and not set_b:
            return 0.0

        intersection = set_a & set_b
        union = set_a | set_b

        return len(intersection) / len(union)

    def compare(self, text: str, reference: str) -> DedupResult:
        """Compare *text* against a single *reference* string.

        Uses token-cosine similarity and the configured thresholds to produce
        a DedupResult.
        """
        score = self.token_cosine(text, reference)
        return DedupResult(
            is_duplicate=score >= self.duplicate_threshold,
            score=score,
            matched_with=reference,
        )

    def compare_many(self, text: str, references: List[str]) -> DedupResult:
        """Compare *text* against a list of *references*.

        Returns a DedupResult indicating:
          - is_duplicate: True if any reference score >= duplicate_threshold.
          - matched_with: The first reference that matched, if any.
          - score: The highest score found.
          - possible_duplicates: All references with score between
            possible_threshold and duplicate_threshold.
        """
        best_score = 0.0
        best_match: Optional[str] = None
        possible: List[str] = []

        for ref in references:
            score = self.token_cosine(text, ref)
            if score > best_score:
                best_score = score
            if score >= self.duplicate_threshold:
                return DedupResult(
                    is_duplicate=True,
                    score=score,
                    matched_with=ref,
                    possible_duplicates=possible,
                )
            if score >= self.possible_threshold:
                possible.append(ref)

        return DedupResult(
            is_duplicate=False,
            score=best_score,
            matched_with=best_match,
            possible_duplicates=possible,
        )
