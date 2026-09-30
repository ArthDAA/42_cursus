"""The constrained token-by-token generation loop.

Guarantees: every appended token is legal for its span. The model has
no reusable attention cache through the SDK, so each step recomputes
over the whole sequence; steps with a single legal token skip the
model call since their outcome is already decided.
"""

from collections.abc import Set

from llm_sdk import Small_LLM_Model

from src import sdk_bridge, spans
from src.errors import GenerationError
from src.spans import Span
from src.vocabulary import Vocabulary


def _pick(
    sdk: Small_LLM_Model, ids: list[int], allowed: Set[int]
) -> int:
    """Greedily choose the best allowed token.

    Args:
        sdk: The loaded model wrapper.
        ids: The full token sequence so far.
        allowed: The legal token ids, non-empty.

    Returns:
        The allowed token id with the highest logit.
    """
    if len(allowed) == 1:
        return next(iter(allowed))
    logits = sdk_bridge.next_token_logits(sdk, ids)
    return max(allowed, key=logits.__getitem__)


def generate(
    sdk: Small_LLM_Model,
    vocab: Vocabulary,
    initial_ids: list[int],
    span_list: list[Span],
    max_tokens_per_span: int,
) -> str:
    """Generate text across an ordered list of spans.

    A non-literal span that may terminate also accepts tokens starting
    the next span; choosing one closes the span and the token is
    carried over as the beginning of the next span.

    Args:
        sdk: The loaded model wrapper.
        vocab: The model vocabulary.
        initial_ids: Token ids of the prompt; extended in place.
        span_list: The spans to produce, in emission order.
        max_tokens_per_span: Hard cap on tokens chosen per span.

    Returns:
        The text produced across all spans.

    Raises:
        GenerationError: If no token is legal or the cap is exceeded.
    """
    ids = initial_ids
    output = ""
    carried = ""
    for index, span in enumerate(span_list):
        next_span = (
            span_list[index + 1] if index + 1 < len(span_list) else None
        )
        span_text = carried
        carried = ""
        steps = 0
        while True:
            content = spans.legal_token_ids(span, vocab, span_text)
            terminable = spans.may_terminate(span, span_text)
            if terminable and not content:
                break
            closers: Set[int] = frozenset()
            if terminable and next_span is not None:
                closers = spans.legal_token_ids(next_span, vocab, "")
            if not content and not closers:
                raise GenerationError(
                    f"no legal token after {output + span_text!r}"
                )
            if steps >= max_tokens_per_span:
                raise GenerationError(
                    f"span exceeded {max_tokens_per_span} tokens: "
                    f"{span_text!r}"
                )
            allowed = content | closers if closers else content
            chosen = _pick(sdk, ids, allowed)
            ids.append(chosen)
            steps += 1
            token = vocab.token_string(chosen)
            if chosen in closers and chosen not in content:
                carried = token
                break
            span_text += token
        output += span_text
    return output + carried
