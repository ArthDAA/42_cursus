"""Token id <-> string map."""

import json

from llm_sdk import Small_LLM_Model

from src.errors import InputFileError


def _byte_decoder() -> dict[str, int]:
    """Build the inverse of the byte-level BPE byte-to-unicode table.

    Returns:
        A map from each printable stand-in character to its byte value.
    """
    printable = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    chars = list(printable)
    extra = 0
    for byte in range(256):
        if byte not in printable:
            printable.append(byte)
            chars.append(256 + extra)
            extra += 1
    return {chr(char): byte for byte, char in zip(printable, chars)}


class Vocabulary:
    """Decoded vocabulary of the model, indexed by token id.

    Tokens whose bytes are not valid UTF-8 on their own decode to a
    string containing U+FFFD and are treated as unusable by the spans.
    """

    def __init__(self, sdk: Small_LLM_Model) -> None:
        """Load the vocabulary file exposed by the SDK.

        Args:
            sdk: The loaded model wrapper.

        Raises:
            InputFileError: If the vocabulary file cannot be loaded.
        """
        try:
            path = sdk.get_path_to_vocab_file()
            with open(path, encoding="utf-8") as file:
                raw: dict[str, int] = json.load(file)
        except (OSError, json.JSONDecodeError) as exc:
            raise InputFileError(f"cannot load vocabulary: {exc}") from exc
        decoder = _byte_decoder()
        self._tokens: list[str] = [""] * (max(raw.values()) + 1)
        self._ids: dict[str, int] = {}
        for token, token_id in raw.items():
            try:
                data = bytes(decoder[char] for char in token)
            except KeyError:
                continue
            text = data.decode("utf-8", errors="replace")
            self._tokens[token_id] = text
            if "�" not in text:
                self._ids.setdefault(text, token_id)

    @property
    def size(self) -> int:
        """Number of token ids covered by the vocabulary."""
        return len(self._tokens)

    def token_string(self, token_id: int) -> str:
        """Return the text of a token.

        Args:
            token_id: A token id; unknown ids map to the empty string.

        Returns:
            The decoded token text.
        """
        if 0 <= token_id < len(self._tokens):
            return self._tokens[token_id]
        return ""

    def token_id(self, text: str) -> int | None:
        """Return the id of the token spelling exactly text, if any.

        Args:
            text: The exact token text.

        Returns:
            The token id, or None if no single token spells it.
        """
        return self._ids.get(text)

    def all_ids(self) -> range:
        """Return the range of every token id."""
        return range(len(self._tokens))
