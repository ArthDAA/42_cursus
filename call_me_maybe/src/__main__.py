"""CLI entry point."""

import argparse
import sys
from pathlib import Path

from src import io_utils, pipeline
from src.errors import InputFileError, PromptProcessingError, SchemaError
from src.schema import ResultItem

DEFAULT_INPUT = Path("data/input/function_calling_tests.json")
DEFAULT_OUTPUT = Path("data/output/function_calling_results.json")


def _parse_args() -> argparse.Namespace:
    """Parse the command-line arguments.

    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="python -m src",
        description="Translate prompts into function calls.",
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--functions", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    """Run the whole pipeline.

    Returns:
        The process exit code.
    """
    args = _parse_args()
    try:
        prompts = io_utils.load_prompts(args.input)
        functions = io_utils.load_function_definitions(
            args.functions, args.input.parent
        )
    except (InputFileError, SchemaError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        from llm_sdk import Small_LLM_Model

        from src.vocabulary import Vocabulary

        sdk = Small_LLM_Model()
        vocab = Vocabulary(sdk)
    except Exception as exc:
        print(f"Error: cannot load the model: {exc}", file=sys.stderr)
        return 1

    results: list[ResultItem] = []
    for index, prompt in enumerate(prompts, 1):
        print(f"[{index}/{len(prompts)}] {prompt}", flush=True)
        try:
            result = pipeline.run_one(sdk, vocab, prompt, functions)
        except PromptProcessingError as exc:
            print(f"  failed: {exc}", file=sys.stderr, flush=True)
            continue
        print(f"  -> {result.fn_name} {result.args}", flush=True)
        results.append(result)

    try:
        io_utils.write_results(args.output, results)
    except InputFileError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    failed = len(prompts) - len(results)
    print(f"{len(results)} succeeded / {failed} failed -> {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
