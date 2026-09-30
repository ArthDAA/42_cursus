"""File I/O: load prompts, load definitions, write results."""

import json
import os
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from src.errors import InputFileError, SchemaError
from src.schema import FunctionDefinition, ResultItem

DEFAULT_FUNCTION_FILES = (
    "function_definitions.json",
    "functions_definition.json",
)


def _read_json(path: Path) -> Any:
    """Read and parse a JSON file.

    Args:
        path: File to read.

    Returns:
        The parsed JSON value.

    Raises:
        InputFileError: If the file is missing, unreadable or invalid.
    """
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as exc:
        raise InputFileError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise InputFileError(f"invalid JSON in {path}: {exc}") from exc
    except OSError as exc:
        raise InputFileError(f"cannot read {path}: {exc}") from exc


def load_prompts(prompts_path: Path) -> list[str]:
    """Load the list of prompts to process.

    Each entry may be a plain string or an object with a "prompt" key.

    Args:
        prompts_path: Path to the JSON prompts file.

    Returns:
        The prompts as plain strings.

    Raises:
        InputFileError: If the file or one of its entries is invalid.
    """
    data = _read_json(prompts_path)
    if not isinstance(data, list):
        raise InputFileError(f"{prompts_path}: expected a JSON array")
    prompts: list[str] = []
    for index, entry in enumerate(data):
        if isinstance(entry, str):
            prompts.append(entry)
        elif isinstance(entry, dict) and isinstance(entry.get("prompt"), str):
            prompts.append(entry["prompt"])
        else:
            raise InputFileError(
                f"{prompts_path}: entry {index} is neither a string "
                f"nor an object with a string 'prompt'"
            )
    return prompts


def load_function_definitions(
    functions_path: Path | None, search_dir: Path
) -> list[FunctionDefinition]:
    """Load and validate the function definitions.

    Args:
        functions_path: Explicit definitions file, or None to search
            the default file names in search_dir.
        search_dir: Directory searched when functions_path is None.

    Returns:
        The validated function definitions.

    Raises:
        InputFileError: If no file is found or the file is invalid.
        SchemaError: If a definition does not match the schema.
    """
    if functions_path is None:
        candidates = [search_dir / name for name in DEFAULT_FUNCTION_FILES]
        found = [path for path in candidates if path.is_file()]
        if not found:
            tried = ", ".join(str(path) for path in candidates)
            raise InputFileError(
                f"no function definitions found (tried {tried})"
            )
        functions_path = found[0]
    data = _read_json(functions_path)
    if not isinstance(data, list) or not data:
        raise InputFileError(f"{functions_path}: expected a non-empty array")
    definitions: list[FunctionDefinition] = []
    for index, entry in enumerate(data):
        try:
            definitions.append(FunctionDefinition.model_validate(entry))
        except ValidationError as exc:
            name = entry.get("name") if isinstance(entry, dict) else None
            raise SchemaError(
                f"{functions_path}: invalid definition {index} ({name}): {exc}"
            ) from exc
    return definitions


def write_results(output_path: Path, results: list[ResultItem]) -> None:
    """Write the results atomically as a JSON array.

    Args:
        output_path: Destination file; parent directories are created.
        results: The results to write.

    Raises:
        InputFileError: If the file cannot be written.
    """
    tmp_path = output_path.with_name(output_path.name + ".tmp")
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(tmp_path, "w", encoding="utf-8") as file:
            json.dump(
                [result.model_dump() for result in results],
                file,
                indent=2,
                ensure_ascii=False,
            )
            file.write("\n")
        os.replace(tmp_path, output_path)
    except OSError as exc:
        raise InputFileError(f"cannot write {output_path}: {exc}") from exc
