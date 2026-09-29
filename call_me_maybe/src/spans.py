"""The legality automaton: literal / candidate / typed-value spans."""

import re
from collections.abc import Set
from functools import lru_cache

from pydantic import BaseModel, ConfigDict

from src.vocabulary import Vocabulary

_JSON_ESCAPES = frozenset('\\/bfnrt')
_NUMBER_CHARS = frozenset("0123456789.-")

_FLOAT_PREFIX = re.compile(r"-?(?:(?:0|[1-9]\d*)(?:\.\d*)?)?")
_FLOAT_FULL = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?")
_INT_PREFIX = re.compile(r"-?(?:0|[1-9]\d*)?")
_INT_FULL = re.compile(r"-?(?:0|[1-9]\d*)")


class LiteralSpan(BaseModel):
    """Fixed text that must be produced verbatim."""

    model_config = ConfigDict(frozen=True)
    text: str


class CandidateSpan(BaseModel):
    """Text that must equal exactly one of a finite set of strings."""

    model_config = ConfigDict(frozen=True)
    candidates: tuple[str, ...]


class NumberSpan(BaseModel):
    """A JSON number, optionally restricted to integers."""

    model_config = ConfigDict(frozen=True)
    allow_fraction: bool


class StringSpan(BaseModel):
    """The content of a JSON string, between its quotes."""

    model_config = ConfigDict(frozen=True)


Span = LiteralSpan | CandidateSpan | NumberSpan | StringSpan


def _escapes_ok(text: str, pending: bool) -> bool:
    """Check that every backslash in text starts a valid JSON escape.

    Args:
        text: Token text, free of quotes and control characters.
        pending: Whether an unfinished backslash precedes text.

    Returns:
        True if text keeps the string content a valid JSON prefix.
    """
    for char in text:
        if pending:
            if char not in _JSON_ESCAPES:
                return False
            pending = False
        elif char == "\\":
            pending = True
    return True


def _is_string_safe(text: str) -> bool:
    """Tell whether a token may appear inside a JSON string at all.

    Args:
        text: Token text.

    Returns:
        True if text is non-empty, decodable and has no quote or
        control character.
    """
    return bool(text) and "�" not in text and '"' not in text and all(
        ord(char) >= 0x20 for char in text
    )


@lru_cache(maxsize=4)
def _string_sets(vocab: Vocabulary) -> tuple[frozenset[int], frozenset[int]]:
    """Precompute the string-content token sets.

    Args:
        vocab: The model vocabulary.

    Returns:
        The legal ids with no pending escape, and with a pending one.
    """
    free: list[int] = []
    pending: list[int] = []
    for token_id in vocab.all_ids():
        text = vocab.token_string(token_id)
        if not _is_string_safe(text):
            continue
        if _escapes_ok(text, False):
            free.append(token_id)
        if _escapes_ok(text, True):
            pending.append(token_id)
    return frozenset(free), frozenset(pending)


@lru_cache(maxsize=4)
def _number_tokens(vocab: Vocabulary) -> tuple[tuple[int, str], ...]:
    """Precompute the tokens made only of number characters.

    Args:
        vocab: The model vocabulary.

    Returns:
        (id, text) pairs of every such token.
    """
    result: list[tuple[int, str]] = []
    for token_id in vocab.all_ids():
        text = vocab.token_string(token_id)
        if text and all(char in _NUMBER_CHARS for char in text):
            result.append((token_id, text))
    return tuple(result)


def _pending_escape(text: str) -> bool:
    """Tell whether text ends with an unfinished backslash escape.

    Args:
        text: String content generated so far.

    Returns:
        True if text ends with an odd number of backslashes.
    """
    count = len(text) - len(text.rstrip("\\"))
    return count % 2 == 1


def _candidates(span: LiteralSpan | CandidateSpan) -> tuple[str, ...]:
    """Return the candidate strings of a literal or candidate span.

    Args:
        span: A literal or candidate span.

    Returns:
        The strings the span may produce.
    """
    if isinstance(span, LiteralSpan):
        return (span.text,)
    return span.candidates


def legal_token_ids(
    span: Span, vocab: Vocabulary, generated_so_far: str
) -> Set[int]:
    """Return the token ids that keep the span's text valid.

    Args:
        span: The span being generated.
        vocab: The model vocabulary.
        generated_so_far: Text produced inside this span so far.

    Returns:
        The set of legal next token ids; empty when the span can
        only terminate.
    """
    if isinstance(span, (LiteralSpan, CandidateSpan)):
        legal: set[int] = set()
        for candidate in _candidates(span):
            if not candidate.startswith(generated_so_far):
                continue
            remaining = candidate[len(generated_so_far):]
            for end in range(1, len(remaining) + 1):
                token_id = vocab.token_id(remaining[:end])
                if token_id is not None:
                    legal.add(token_id)
        return legal
    if isinstance(span, NumberSpan):
        prefix = _FLOAT_PREFIX if span.allow_fraction else _INT_PREFIX
        return {
            token_id
            for token_id, text in _number_tokens(vocab)
            if prefix.fullmatch(generated_so_far + text)
        }
    free, pending = _string_sets(vocab)
    return pending if _pending_escape(generated_so_far) else free


def may_terminate(span: Span, generated_so_far: str) -> bool:
    """Tell whether the span's text is complete as it stands.

    Args:
        span: The span being generated.
        generated_so_far: Text produced inside this span so far.

    Returns:
        True if the span may end here.
    """
    if isinstance(span, (LiteralSpan, CandidateSpan)):
        return generated_so_far in _candidates(span)
    if isinstance(span, NumberSpan):
        full = _FLOAT_FULL if span.allow_fraction else _INT_FULL
        return full.fullmatch(generated_so_far) is not None
    return not _pending_escape(generated_so_far)
