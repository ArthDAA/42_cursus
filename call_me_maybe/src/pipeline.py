"""Per-prompt orchestration."""

import json

from llm_sdk import Small_LLM_Model
from pydantic import ValidationError

from src import decoder, prompt_builder, sdk_bridge
from src.errors import GenerationError, PromptProcessingError
from src.schema import ArgValue, FunctionDefinition, ParameterSpec, ResultItem
from src.spans import (
    CandidateSpan,
    LiteralSpan,
    NumberSpan,
    Span,
    StringSpan,
)
from src.vocabulary import Vocabulary

MAX_TOKENS_PER_SPAN = 96
_ARGS_OPEN = '", "args": {'


def _value_spans(spec: ParameterSpec) -> list[Span]:
    """Build the spans producing one argument value.

    Args:
        spec: The parameter's type specification.

    Returns:
        The spans for the value; string quotes belong to the
        surrounding literals.
    """
    if spec.type == "string":
        return [StringSpan()]
    if spec.type == "boolean":
        return [CandidateSpan(candidates=("true", "false"))]
    return [NumberSpan(allow_fraction=spec.type == "number")]


def _argument_spans(function: FunctionDefinition) -> list[Span]:
    """Build the spans producing the arguments object's content.

    Args:
        function: The chosen function.

    Returns:
        Spans from the first key up to the closing braces.
    """
    result: list[Span] = []
    separator = ""
    closing = ""
    for name, spec in function.parameters.items():
        key = json.dumps(name, ensure_ascii=False)
        opening = '"' if spec.type == "string" else ""
        result.append(
            LiteralSpan(text=f"{closing}{separator}{key}: {opening}")
        )
        result.extend(_value_spans(spec))
        separator = ", "
        closing = '"' if spec.type == "string" else ""
    result.append(LiteralSpan(text=f"{closing}}}}}"))
    return result


def _convert(value: object, spec: ParameterSpec) -> ArgValue:
    """Coerce a parsed JSON value to its declared type.

    Args:
        value: The value parsed from the generated JSON.
        spec: The parameter's declared type.

    Returns:
        The value as float, int, str or bool.

    Raises:
        TypeError: If the value does not match the declared type.
    """
    if spec.type == "number" and isinstance(value, (int, float)):
        return float(value)
    if spec.type == "integer" and isinstance(value, int):
        return int(value)
    if spec.type == "string" and isinstance(value, str):
        return value
    if spec.type == "boolean" and isinstance(value, bool):
        return value
    raise TypeError(f"{value!r} is not a valid {spec.type}")


def run_one(
    sdk: Small_LLM_Model,
    vocab: Vocabulary,
    prompt: str,
    functions: list[FunctionDefinition],
) -> ResultItem:
    """Turn one prompt into one function call.

    Args:
        sdk: The loaded model wrapper.
        vocab: The model vocabulary.
        prompt: The user's request.
        functions: The functions the model may choose from.

    Returns:
        The validated function call.

    Raises:
        PromptProcessingError: If generation or validation fails.
    """
    by_name = {function.name: function for function in functions}
    text = prompt_builder.build_prompt(prompt, functions)
    ids = sdk_bridge.encode_prompt(sdk, text)
    try:
        head = decoder.generate(
            sdk,
            vocab,
            ids,
            [
                CandidateSpan(candidates=tuple(by_name)),
                LiteralSpan(text=_ARGS_OPEN),
            ],
            MAX_TOKENS_PER_SPAN,
        )
        function = by_name[head[: -len(_ARGS_OPEN)]]
        tail = decoder.generate(
            sdk, vocab, ids, _argument_spans(function), MAX_TOKENS_PER_SPAN
        )
        raw = json.loads(prompt_builder.SKELETON_START + head + tail)
        args = {
            name: _convert(raw["args"][name], spec)
            for name, spec in function.parameters.items()
        }
        return ResultItem(prompt=prompt, fn_name=raw["fn_name"], args=args)
    except GenerationError as exc:
        raise PromptProcessingError(
            prompt, f"generation failed: {exc}"
        ) from exc
    except (
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValidationError,
    ) as exc:
        raise PromptProcessingError(
            prompt, f"invalid generated call: {exc}"
        ) from exc
