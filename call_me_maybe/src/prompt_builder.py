"""Builds the natural-language instruction prompt."""

from src.schema import FunctionDefinition

SKELETON_START = '{"fn_name": "'

_SYSTEM = (
    "You are a function-calling assistant. Given the user's request, "
    "choose the single most appropriate function from the catalogue and "
    "fill in its arguments. Reply with one JSON object of the form "
    '{"fn_name": <name>, "args": {<parameter>: <value>, ...}}.\n'
    "Rules:\n"
    "- Use only the parameter names listed for the chosen function.\n"
    "- Copy values from the request exactly: keep the original spelling "
    "and case, and do not add quotes that are not part of the value.\n"
    "- Numbers are written as plain JSON numbers.\n"
    "- A regex parameter holds a real regular expression pattern "
    "matching what must be found (for example [0-9]+ for numbers, "
    "[aeiouAEIOU] for vowels), never a description of it.\n"
    "- A replacement written as a word for a symbol is given as the "
    "symbol itself (for example * for asterisks).\n"
    "- Regular expressions are written as JSON strings, with "
    "backslashes escaped.\n\n"
    "Function catalogue:\n"
)


def _render_function(function: FunctionDefinition) -> str:
    """Render one catalogue entry.

    Args:
        function: The function to describe.

    Returns:
        A one-line description with the typed parameter list.
    """
    params = ", ".join(
        f"{name}: {spec.type}" for name, spec in function.parameters.items()
    )
    return (
        f"- {function.name}({params}) -> {function.returns.type}: "
        f"{function.description}"
    )


def build_prompt(user_prompt: str, functions: list[FunctionDefinition]) -> str:
    """Build the full text handed to the model before generation.

    Args:
        user_prompt: The user's natural-language request.
        functions: Every function the model may choose from.

    Returns:
        The chat-formatted prompt, ending with the start of the JSON
        skeleton so that generation begins inside the function name.
    """
    catalogue = "\n".join(_render_function(f) for f in functions)
    return (
        f"<|im_start|>system\n{_SYSTEM}{catalogue}<|im_end|>\n"
        f"<|im_start|>user\n{user_prompt}<|im_end|>\n"
        f"<|im_start|>assistant\n<think>\n\n</think>\n\n"
        f"{SKELETON_START}"
    )
