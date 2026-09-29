# 2-Conception.md - call me maybe

| DRAFT D2 | Author: Arthus | Based on: 1-Conditions.md (2026-09-29, revised) | Date: 2026-09-29 |
|---|---|---|---|

---

## GLOBAL VIEW

The whole system boils down to one trick applied uniformly: **every single output token, including the fixed JSON punctuation, is produced by the same constrained-decoding call to the model.** Nothing is injected as raw text behind the model's back (that would risk a BPE tokenization mismatch between text encoded in isolation and text encoded in context). Instead, the output is described as an ordered sequence of **spans**:

- **Literal spans**: fixed punctuation we already know (`{"fn_name": "`, `", "args": {`, a key name, `": `, `, `, `}}`, ...). Legal continuation set of size 1: the model is still asked, but only one token is ever legal, so it has no real choice.
- **Candidate spans**: the value must be exactly one of a known finite set of strings (the function name, among all defined names; a boolean, among `true`/`false`). Legality = "does appending this token keep the accumulated text a prefix of at least one candidate", and closing becomes legal exactly once the accumulated text equals one full candidate.
- **Typed-value spans**: number, integer, or string values, governed by a small per-type character automaton (digits/sign/decimal-point for numbers; any character except a raw quote or control character for strings) with a "may-terminate-here" flag.

Driving the whole output is therefore just: walk the span list in order, and for each span, repeatedly (a) call the model for logits, (b) mask everything illegal for that span given what has already been generated inside it, (c) greedily pick the highest surviving logit, (d) append, (e) check the span's termination condition. This single mechanism covers the skeleton, the function name, every argument, and closes the object - no separate "JSON grammar engine" is needed, because the grammar is fully known in advance and only the values inside the holes are actually chosen by the model.

Two components sit outside this loop and are computed once, up front, before the first prompt is even processed: the **vocabulary** (`vocabulary.py`, id-to-string map, loaded once) and nothing else is cached, because `get_logits_from_input_ids` gives no way to reuse past attention state - each call recomputes over the full sequence so far. This is a known, accepted performance ceiling (see `decoder.py` Guarantees) rather than an oversight.

---

## TRANSVERSAL CONSTRAINTS (apply identically to every file below, not repeated per block)

| D1 id | Constraint | How it's enforced |
|---|---|---|
| F1 | Python >= 3.10 | `pyproject.toml` `requires-python`, checked by `uv sync` |
| F2 | flake8 clean | `make lint`, no per-file exception |
| F3 | Full type hints, mypy zero-error | Every function signature in every block above is typed; `make lint` runs mypy with the exact flags from F11 |
| F4 | PEP 257 docstrings (Google style, O6) | One docstring per function/class in every block above; not restated per-block since it is uniform |
| F5 | All classes use pydantic | Only `schema.py` defines classes carrying data (`ParameterSpec`, `FunctionDefinition`, `ResultItem`) - those are pydantic `BaseModel`. `Vocabulary` in `vocabulary.py` is stateful but holds no externally-validated data, so it is a plain class, not a pydantic model; flagged here explicitly rather than left ambiguous, since F5 could otherwise be read as "every class, no exception" |
| F11 | Makefile (`install`, `run`, `debug`, `clean`, `lint`) | Repo-level file, outside `src/`, not a logical unit of the drafted system itself - produced directly in D3 from F11's own definition, no BIOPGE needed |
| F12 | `.gitignore` | Same as F11: repo-level, not a logical unit |
| F13 | Repo layout (`src/`, `pyproject.toml`, `uv.lock`, `llm_sdk/`, `data/input/`, `README.md`, no `output/`) | Structural constraint on where the 9 files above live, not a behavior of any one of them; verified at D3 by inspecting the tree, not by a BIOPGE guarantee |
| F17 | README.md content | Entirely outside `src/` - a documentation deliverable, not a logical unit of the system. Its "Algorithm explanation" section is exactly the Global View above, restated in prose; its "Design decisions" section draws on the Open Points (O1-O9) and resolved Ambiguities (A1, A11) |

D2's BIOPGE blocks below therefore only carry `M`/`O`/`A` ids and the file-specific `F` ids (F7, F9, F10, F14, F15, F16) - the ones that shape one particular file's contract rather than the whole repo uniformly.

---

## LOGICAL VIEW

<details>
  <summary>`src/errors.py`</summary>

"Exception hierarchy"

| Field | Content |
|---|---|
| **Boundary** | Owns: the project's exception classes. Does NOT own: catching or formatting - only defines types other modules raise and catch. |
| **Inputs** | None (pure definitions). |
| **Outputs** | Exception classes: `InputFileError` (missing/unreadable/invalid-JSON input file), `SchemaError` (a definitions or result object fails its pydantic schema), `GenerationError` (the decoder reaches a state with zero legal tokens, or exceeds a hard step cap), `PromptProcessingError` (wraps any of the above for a single prompt, carries the offending prompt text). |
| **Process** | 1. Define each class as a subclass of `Exception` -> 2. Each carries a human-readable message set at construction, no logic. |
| **Guaranty** | Every exception raised anywhere in `src/` that can reach `__main__.py` is one of these four types, or is caught and re-wrapped into one before crossing a module boundary. |
| **Errors** | N/A (this file defines error types, it does not raise during its own execution). |

> Covers : M11

</details>

<details>
  <summary>`src/schema.py`</summary>

"Pydantic models"

| Field | Content |
|---|---|
| **Boundary** | Owns: the typed shape of a parameter spec, a function definition, and a result item, plus the set of supported argument types. Does NOT own: reading files, or generating values. |
| **Inputs** | Raw `dict`/`list` objects freshly parsed from JSON, handed to it by `io_utils.py` and `pipeline.py`. |
| **Outputs** | `ParameterSpec` (field: `type: Literal["number","integer","string","boolean"]`), `FunctionDefinition` (`name: str`, `description: str`, `parameters: dict[str, ParameterSpec]`, `returns: ParameterSpec`), `ResultItem` (`prompt: str`, `fn_name: str`, `args: dict[str, int \| float \| str \| bool]`). |
| **Process** | 1. Declare each model as a `pydantic.BaseModel` -> 2. Constrain `ParameterSpec.type` to the closed literal set -> 3. Let pydantic's own validation raise on anything else. |
| **Guaranty** | Any `FunctionDefinition` or `ResultItem` instance that exists in memory is schema-valid by construction; an unsupported `type` string can never produce a silently-accepted instance. |
| **Errors** | `pydantic.ValidationError`: unknown `type` value, missing required field, wrong Python type -> propagates to the caller (`io_utils.py` or `pipeline.py`), which wraps it into `SchemaError`. |

> Covers : M6, A4, A5, A6

</details>

<details>
  <summary>`src/io_utils.py`</summary>

"File I/O: load prompts, load definitions, write results"

| Field | Content |
|---|---|
| **Boundary** | Owns: every filesystem read/write and the raw-JSON-to-domain-object normalization. Does NOT own: what the values mean once loaded, or how they get filled in (that's `pipeline.py`). |
| **Inputs** | `prompts_path: Path`, `functions_path: Path \| None` (`None` triggers the default-name search), `results: list[ResultItem]`, `output_path: Path`. |
| **Outputs** | `load_prompts(prompts_path) -> list[str]`; `load_function_definitions(functions_path, search_dir) -> list[FunctionDefinition]`; `write_results(output_path, results) -> None`. |
| **Process** | `load_prompts`: 1. open file as context manager -> 2. `json.load` -> 3. for each array entry, accept either a `str` or a `dict` with key `prompt`, normalize to `str`, else raise -> 4. return list. `load_function_definitions`: 1. if `functions_path` given, use it, else try `function_definitions.json` then `functions_definition.json` in `search_dir` -> 2. open as context manager, `json.load` -> 3. validate each entry through `schema.FunctionDefinition` -> 4. return list. `write_results`: 1. create parent directory if missing -> 2. open as context manager -> 3. `json.dump` the list of `ResultItem.model_dump()`, numbers kept as int/float per their declared type -> 4. flush and close via context manager exit. |
| **Guaranty** | On success, `load_prompts` returns only plain strings (the object/string ambiguity from A11 is fully resolved before this function returns); `load_function_definitions` returns only schema-valid definitions; `write_results` always leaves either a complete, valid JSON file or no file at all (write to a temp path then rename, never a partial file on crash). |
| **Errors** | `FileNotFoundError` (neither candidate filename exists, or `prompts_path` missing) -> wrapped `InputFileError` naming the path(s) tried. `json.JSONDecodeError` -> wrapped `InputFileError` naming the file and the parse error. A prompt entry that is neither `str` nor `{"prompt": str}` -> wrapped `InputFileError` naming the offending index. `SchemaError` from `schema.py` -> re-raised as-is, naming the offending function definition. |

> Covers : F15, F16, A2, A3, A11, M7, M11, M12

</details>

<details>
  <summary>`src/vocabulary.py`</summary>

"Token id <-> string map"

| Field | Content |
|---|---|
| **Boundary** | Owns: the loaded vocabulary and both lookup directions. Does NOT own: calling the model, or deciding legality (that's `spans.py`). |
| **Inputs** | `sdk: Small_LLM_Model` (only to call its public `get_path_to_vocab_file()`). |
| **Outputs** | `Vocabulary` object exposing `size: int`, `token_string(id: int) -> str`, `all_ids() -> range`. |
| **Process** | 1. Call `sdk.get_path_to_vocab_file()` once at construction -> 2. open and `json.load` the returned path as a context manager -> 3. build `id -> token_string` from the loaded `{token_string: id}` mapping -> 4. store as a plain Python list indexed by id. |
| **Guaranty** | Built exactly once per run and reused for every prompt; `token_string(id)` never raises for any `id` in `all_ids()`. |
| **Errors** | `FileNotFoundError` / `json.JSONDecodeError` on the vocab file -> wrapped `InputFileError` (this is a setup failure, not a per-prompt one, and aborts the whole run since nothing can proceed without it). |

> Covers : O4, F9

</details>

<details>
  <summary>`src/sdk_bridge.py`</summary>

"Thin wrapper isolating every SDK quirk in one place"

| Field | Content |
|---|---|
| **Boundary** | Owns: the only two places in `src/` that touch an `llm_sdk` return value shaped by `torch` (`encode`'s `Tensor`, `decode`'s `Tensor \| list[int]` input). Does NOT own: the generation loop itself, or logits interpretation. |
| **Inputs** | `sdk: Small_LLM_Model`, `text: str` (for encoding), `input_ids: list[int]` (for logits). |
| **Outputs** | `encode_prompt(sdk, text) -> list[int]`; `next_token_logits(sdk, input_ids) -> list[float]`. |
| **Process** | `encode_prompt`: 1. call `sdk.encode(text)` -> 2. call `.tolist()[0]` on the result, no explicit type naming `torch.Tensor` anywhere, no `import torch` in this file or any other -> 3. return the plain `list[int]`. `next_token_logits`: 1. call `sdk.get_logits_from_input_ids(input_ids)` -> 2. return it unchanged (already `list[float]` per the audited signature). |
| **Guaranty** | No module outside `sdk_bridge.py` ever sees a `torch`-typed object; both functions return plain built-in Python types only. |
| **Errors** | Any exception raised inside the SDK call (e.g. the model failing to load, an encode error on pathological input) propagates unwrapped - it is a setup/environment failure, not a data-shape failure this layer can meaningfully recover from; caught one level up in `pipeline.py` per prompt where relevant, or in `__main__.py` at startup. |

> Covers : A1, O9, F9, F7

</details>

<details>
  <summary>`src/spans.py`</summary>

"The legality automaton: literal / candidate / typed-value spans"

| Field | Content |
|---|---|
| **Boundary** | Owns: for any span and any text generated so far inside that span, the set of currently-legal token ids and whether the span may end now. Does NOT own: calling the model, or choosing among legal tokens (that's `decoder.py`). |
| **Inputs** | A `Vocabulary`; a span descriptor (`LiteralSpan(text: str)`, `CandidateSpan(candidates: list[str])`, `NumberSpan(allow_fraction: bool)`, `StringSpan()`); `generated_so_far: str` (the text produced inside the current span only). |
| **Outputs** | `legal_token_ids(span, vocab, generated_so_far) -> set[int]`; `may_terminate(span, generated_so_far) -> bool`. |
| **Process** | `LiteralSpan`/`CandidateSpan` (same rule, `LiteralSpan` is a `CandidateSpan` of exactly one candidate): 1. filter `vocab`'s tokens to those whose string, appended to `generated_so_far`, is a prefix of at least one candidate -> 2. `may_terminate` is true iff `generated_so_far` exactly equals one candidate. `NumberSpan`: 1. if `generated_so_far` is empty, legal alphabet = digits + `-` -> 2. else if last char is `-` or a digit continuing the integer part, legal = digits (+ `.` once, only if `allow_fraction` and no `.` yet) -> 3. `may_terminate` is true iff `generated_so_far` ends in a digit (never right after `-` or `.`). `StringSpan`: 1. legal alphabet = any vocabulary token whose string contains no raw `"` and no control character -> 2. `may_terminate` is true always (including on the empty string, per M13). |
| **Guaranty** | `legal_token_ids` is never empty for a reachable state (by construction: at minimum one candidate/digit/character always remains legal, or the span is already terminable); every `str` obtainable by repeatedly appending returned-legal tokens and eventually terminating is valid for that span's intended type. |
| **Errors** | `GenerationError` if a caller manages to reach a state where `legal_token_ids` would be empty (defensive check in `decoder.py`, treated as an internal bug, not a data error - see `decoder.py` Errors). |

> Covers : M2, M3, M5, A4, M13

</details>

<details>
  <summary>`src/prompt_builder.py`</summary>

"Builds the natural-language instruction prompt"

| Field | Content |
|---|---|
| **Boundary** | Owns: turning a user prompt plus the list of available functions into the exact text handed to the model before generation starts. Does NOT own: tokenizing it, or generating anything. |
| **Inputs** | `user_prompt: str`, `functions: list[FunctionDefinition]`. |
| **Outputs** | `build_prompt(user_prompt, functions) -> str`. |
| **Process** | 1. Render each function's name, description, and parameter names/types into a compact catalogue block -> 2. append the user's request -> 3. append the fixed instruction telling the model it is choosing a function call -> 4. append the start of the forced skeleton (`{"fn_name": "`) so the model's very first generated token is already inside the first span. |
| **Guaranty** | The returned string is deterministic for a given `(user_prompt, functions)` pair (no randomness); every function in `functions` appears in the catalogue, so the model is never asked to choose among functions it cannot see. |
| **Errors** | None raised - a pure string-building function over already-validated inputs. |

> Covers : O1, M1, M4

</details>

<details>
  <summary>`src/decoder.py`</summary>

"The constrained token-by-token generation loop"

| Field | Content |
|---|---|
| **Boundary** | Owns: driving generation across an ordered list of spans to completion. Does NOT own: what the spans mean (that's `pipeline.py`/`spans.py`), or talking to the SDK directly except through `sdk_bridge.py`. |
| **Inputs** | `sdk: Small_LLM_Model`, `vocab: Vocabulary`, `initial_ids: list[int]` (the encoded prompt, ending mid-first-span), `spans: list[Span]` (in emission order), `max_tokens_per_span: int` (hard cap, safety net). |
| **Outputs** | `generate(sdk, vocab, initial_ids, spans, max_tokens_per_span) -> str` (the concatenated text produced across all spans, i.e. everything after the prompt). |
| **Process** | 1. `ids = initial_ids`, `output_text = ""` -> 2. for each `span` in `spans`: `span_text = ""` -> 3. loop: `logits = sdk_bridge.next_token_logits(sdk, ids)` -> 4. `legal = spans.legal_token_ids(span, vocab, span_text)` -> 5. if `legal` empty, raise `GenerationError` -> 6. set every non-legal logit to `-inf` -> 7. pick `argmax` (greedy, O5) among the masked logits -> 8. `ids.append(chosen_id)`, `span_text += vocab.token_string(chosen_id)`, `output_text += vocab.token_string(chosen_id)` -> 9. if `spans.may_terminate(span, span_text)` and (span is a `LiteralSpan` and `span_text == span.text`, or the chosen token is itself a closing signal for candidate/typed spans) stop the inner loop -> 10. if the inner loop runs `max_tokens_per_span` times without terminating, raise `GenerationError` -> 11. after all spans, return `output_text`. |
| **Guaranty** | Every token appended to `ids` was legal for its span at the moment it was chosen (M2); the returned `output_text`, once concatenated after the skeleton's own literal spans, forms syntactically valid JSON matching the function/argument schema by construction (M3, M9) - no post-hoc string repair is ever needed. |
| **Errors** | `GenerationError`: empty legal set (an internal contract violation between `spans.py` and `decoder.py`) or `max_tokens_per_span` exceeded (a genuine safety net, e.g. a string value that never chooses to close) -> propagates to `pipeline.py`, which treats it as a per-prompt failure (A7). |

> Covers : M2, M3, M4, M5, O5, M13

</details>

<details>
  <summary>`src/pipeline.py`</summary>

"Per-prompt orchestration"

| Field | Content |
|---|---|
| **Boundary** | Owns: turning one raw prompt string into one `ResultItem`, or a reported, isolated failure. Does NOT own: reading/writing files, or the token-level mechanics. |
| **Inputs** | `sdk: Small_LLM_Model`, `vocab: Vocabulary`, `prompt: str`, `functions: list[FunctionDefinition]`. |
| **Outputs** | `run_one(sdk, vocab, prompt, functions) -> ResultItem` (raises `PromptProcessingError` instead of returning, on failure). |
| **Process** | 1. `text = prompt_builder.build_prompt(prompt, functions)` -> 2. `ids = sdk_bridge.encode_prompt(sdk, text)` -> 3. build the full span list: skeleton literal -> `CandidateSpan([f.name for f in functions])` -> for each parameter of the chosen... **note**: the parameter list depends on which function was chosen, so spans are generated in two waves: first the skeleton + function-name `CandidateSpan` alone are run through `decoder.generate`, then, once the function name is known, the argument spans (one `NumberSpan`/`StringSpan`/boolean `CandidateSpan` per parameter, interleaved with literal spans for keys/commas/closing braces) are appended and a second `decoder.generate` call continues from the same `ids` -> 4. concatenate both generated fragments with the skeleton literals into one JSON string -> 5. `json.loads` it (a safety-net parse, not a correctness requirement) -> 6. validate into `schema.ResultItem` together with the original `prompt` text. |
| **Guaranty** | On success, the returned `ResultItem` always passes its own pydantic validation (M6, M9); the function name is always one of `functions`, and every argument name/type matches that function's definition exactly (M3, M7 - nothing here depends on which particular functions or prompt were passed in). |
| **Errors** | `GenerationError` from `decoder.py` -> wrapped `PromptProcessingError` carrying `prompt`. `json.JSONDecodeError` or `SchemaError` on the safety-net parse (should be unreachable given `decoder.py`'s guarantee, but never trusted blindly) -> wrapped `PromptProcessingError` carrying `prompt`. |

> Covers : M1, M4, M6, M7, M9, A7, M14

</details>

<details>
  <summary>`src/__main__.py`</summary>

"CLI entry point"

| Field | Content |
|---|---|
| **Boundary** | Owns: argument parsing, wiring every other module together, and the top-level per-prompt error isolation loop. Does NOT own: any file format detail or generation logic. |
| **Inputs** | `sys.argv` (`--input`, `--output`, `--functions`, each optional). |
| **Outputs** | Process exit code; the results file on disk; error messages on stderr. |
| **Process** | 1. Parse args, defaulting `--input` to `data/input/function_calling_tests.json`, `--output` to `data/output/function_calling_results.json`, `--functions` to the default-name search in `data/input/` (A2) -> 2. `io_utils.load_prompts`, `io_utils.load_function_definitions` -> 3. construct `Small_LLM_Model()` and `Vocabulary(sdk)` once -> 4. for each prompt, call `pipeline.run_one` inside a `try/except PromptProcessingError`, collecting successes and printing failures to stderr with the offending prompt -> 5. `io_utils.write_results` with whatever succeeded -> 6. print a one-line summary (N succeeded / M failed) to stdout. |
| **Guaranty** | The process never terminates via an unhandled exception for a per-prompt failure (M11); a setup-level failure (bad input files, SDK load failure) does exit with a non-zero code and a clear message, since no output can be meaningful without it. |
| **Errors** | `InputFileError` at setup (steps 1-2) -> print to stderr, exit non-zero, no output file written. `PromptProcessingError` per prompt (step 4) -> printed to stderr, that prompt skipped, loop continues (A7). |

> Covers : F14, A2, A3, F10, M7, M11, M12

</details>

---

## D2 exit

- [x] Gate applied and decision recorded: 9 logical units, well above the 4-interface BIOPGE threshold -> full BIOPGE, no free schema
- [x] All blocks complete
- [x] `> Covers :` filled, every D1 M/F/A id traced to at least one block or to the Transversal Constraints table (spot-check: M2/M3/M5 -> spans.py+decoder.py; A1 -> sdk_bridge.py; A11 -> io_utils.py; A2 -> __main__.py+io_utils.py; F1-F5/F11-F13/F17 -> Transversal Constraints table, not per-block)
- [x] Cross-block I/O types consistent: `Vocabulary`, `FunctionDefinition`, `ResultItem`, `Span` objects flow in one direction, no orphan dependency
- [x] Zero code written
