"""Thin wrapper isolating every SDK quirk in one place."""

from llm_sdk import Small_LLM_Model


def encode_prompt(sdk: Small_LLM_Model, text: str) -> list[int]:
    """Tokenize text into plain token ids.

    Args:
        sdk: The loaded model wrapper.
        text: The text to tokenize.

    Returns:
        The token ids.
    """
    ids: list[int] = sdk.encode(text).tolist()[0]
    return ids


def next_token_logits(
    sdk: Small_LLM_Model, input_ids: list[int]
) -> list[float]:
    """Return the raw next-token logits for a sequence.

    Args:
        sdk: The loaded model wrapper.
        input_ids: The full token sequence so far.

    Returns:
        One logit per token id of the model.
    """
    return sdk.get_logits_from_input_ids(input_ids)
