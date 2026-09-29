*This project has been created as part of the 42 curriculum by arde-ass.*

# call me maybe

## Description

`call me maybe` turns natural-language requests into structured function
calls using a small language model (Qwen3-0.6B). Given a catalogue of
functions and a list of prompts, it produces, for each prompt, a JSON object
naming the function to call and its typed arguments:

```json
{"prompt": "What is the sum of 2 and 3?", "fn_name": "fn_add_numbers", "args": {"a": 2.0, "b": 3.0}}
```

A 0.6B model left alone rarely produces valid JSON reliably. Here the output
is **guaranteed** to be valid and schema-conformant through constrained
decoding: the model only ever chooses among tokens that keep the output
valid.

## Instructions

Requirements: Python >= 3.10 and [uv](https://docs.astral.sh/uv/).

```sh
make install   # uv sync: installs dependencies and the local llm_sdk
make run       # runs python -m src with the default paths
make lint      # flake8 + mypy
make debug     # runs under pdb
make clean     # removes caches
```

Custom paths:

```sh
uv run python -m src \
    --input data/input/function_calling_tests.json \
    --functions data/input/functions_definition.json \
    --output data/output/function_calling_results.json
```

`--functions` is optional: by default `function_definitions.json` then
`functions_definition.json` are searched next to the input file. The first
run downloads the model from the Hugging Face Hub.

## Algorithm explanation

Every output token, including the fixed JSON punctuation, is produced by the
same constrained decoding step. Nothing is spliced in as raw text behind the
model's back, which avoids tokenization mismatches between text encoded
alone and text encoded in context.

The output is described as an ordered sequence of **spans**:

- **Literal spans**: fixed text such as `", "args": {`, a key, `, ` or
  `}}`. Only tokens that are a prefix of the remaining text are legal.
- **Candidate spans**: the value must be one of a finite set of strings
  (the function name among all defined names; `true`/`false`). A token is
  legal if the accumulated text stays a prefix of at least one candidate.
- **Typed-value spans**: numbers (`-?(0|[1-9]\d*)(\.\d+)?`, integers without
  the fractional part) and string contents (any token without a raw quote or
  control character, backslashes only as valid JSON escapes).

Generation walks the spans in order. For each step it (a) asks the model for
the next-token logits, (b) masks every illegal token, (c) greedily picks the
best remaining one and (d) appends it. A literal or candidate span ends when
its text is complete and cannot be extended. A typed span that may end
(e.g. a number ending with a digit) also accepts tokens that start the next
span; choosing one closes the value and the token is carried over to the next
span. This is how the model decides where a string or number stops.

Generation happens in two waves: first the function name, then, once the
function is known, the argument spans built from its definition. The result
is parsed back with `json.loads` as a safety net and validated with pydantic.

## Design decisions

- **Greedy decoding**: deterministic, and the constraint already removes
  the failure modes sampling would otherwise hide.
- **Vocabulary decoding**: `vocab.json` stores byte-level BPE tokens; they
  are mapped back to their real bytes once at startup. Tokens that are
  incomplete UTF-8 sequences are never used in spans.
- **No KV cache**: the SDK recomputes the whole sequence on each call. Steps
  where exactly one token is legal are decided without calling the model.
- **Precomputed token sets**: the tokens allowed inside strings and numbers
  are computed once per run, so a step costs a set lookup rather than a
  scan of the ~150k-token vocabulary.
- **Error isolation**: a failing prompt is reported on stderr and skipped;
  input or model loading errors stop the program with a clear message.
- **Numbers**: `number` arguments are written as floats, `integer` ones as
  ints.

## Performance analysis

Validity is 100% by construction: every produced object parses as JSON and
matches the chosen function's parameter names and types. On the provided
set, the function choice and the numeric/string arguments are correct; the
weakest point is inventing regular expressions from a description (e.g.
"vowels"), which is a limit of the 0.6B model rather than of the decoder.

Speed is bounded by the SDK: without a KV cache, every step re-runs the model
over the whole prompt. On an 8-core CPU without GPU the provided set takes
around 12 minutes, most of it spent on long string arguments.

## Challenges faced

- Deciding where a free value ends: solved by letting the next span's first
  token act as the closing signal.
- Function names that are prefixes of others: a candidate span only ends
  when the model picks a token that starts the next span.
- Backslashes in regular expressions: the string automaton tracks pending
  escapes across token boundaries.

## Testing strategy

- `make lint` (flake8, mypy).
- Runs on the provided prompts and on custom prompt/function files
  (booleans, integers, prefix-sharing function names, missing or malformed
  input files).
- Every output file is checked with `json.load` and against the definitions.

## Example usage

```sh
$ make run
[1/11] What is the sum of 2 and 3?
  -> fn_add_numbers {'a': 2.0, 'b': 3.0}
...
11 succeeded / 0 failed -> data/output/function_calling_results.json
```

## Resources

- [Qwen3 model card](https://huggingface.co/Qwen/Qwen3-0.6B)
- [Hugging Face tokenizers: byte-level BPE](https://huggingface.co/docs/tokenizers)
- [JSON specification (RFC 8259)](https://www.rfc-editor.org/rfc/rfc8259)
- [pydantic documentation](https://docs.pydantic.dev/)
