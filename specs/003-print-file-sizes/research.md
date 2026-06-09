# Research: Print file sizes in a directory

**Feature**: `003-print-file-sizes`  
**Date**: 2026-06-09

## R1 — Language and dependency policy

**Decision**: Extend the existing **`pdf_count`** package with **Python 3.10+** and **stdlib only**.

**Rationale**: Matches repository conventions (specs 001/002), user-facing CLI already exists, and
`pathlib`, `stat`, and `argparse` cover listing, sizing, and CLI wiring without new dependencies.

**Alternatives considered**: New standalone package (rejected: duplicates CLI/error patterns); third-party
CLI libraries (rejected: violates stdlib-only policy).

## R2 — Directory listing, regular-file detection, and size

**Decision**: Use `pathlib.Path.iterdir()` for **immediate children only**; for each entry call
`entry.lstat()`; include entries where `stat.S_ISREG(st.st_mode)` is true; record `st.st_size` as
the byte size.

**Rationale**: Aligns with existing `count.py` (`lstat` semantics per **FR-006**): symbolic links are
not listed even when their targets are regular files; directories named like files are excluded.
`st_size` is the filesystem-reported logical length required by the spec.

**Alternatives considered**: `entry.is_file()` / `stat()` following symlinks (rejected: violates
**FR-006**); recursive `os.walk` (rejected: spec is non-recursive); human-readable units (rejected:
spec assumes bytes).

## R3 — Output format and ordering

**Decision**: On success, print one line per listed file to **stdout** as `{name}\t{size}\n` where
`{name}` is the entry’s final path component and `{size}` is the decimal byte count with no
thousands separators. Sort lines **alphabetically by `{name}`** using Python’s default string
ordering (case-sensitive, byte order of the displayed name).

**Rationale**: Tab separation keeps names with spaces unambiguous (**FR-004**). Name-first layout
matches common “label then value” reading. Sorting before print satisfies **FR-004** determinism for
tests and scripts.

**Alternatives considered**: Space-separated fields (rejected: ambiguous when names contain spaces);
unsorted output (rejected: **FR-004**); human-readable sizes (rejected: spec **Assumptions**).

## R4 — CLI flag and mode interaction

**Decision**: Add optional flag **`--list-file-sizes`**. When set, run file-size listing mode; when
omitted, preserve existing default document-count and `--count-pdf-directories` behaviors unchanged.
Place `--list-file-sizes` and `--count-pdf-directories` in an **`argparse` mutually exclusive group**
so only one output mode is active per invocation.

**Rationale**: Spec **Assumptions** require an explicit new mode without changing default counting.
Mutual exclusion prevents ambiguous multi-mode output and matches how users treat flags as alternate
commands.

**Alternatives considered**: Subcommand `pdf_count sizes <dir>` (rejected: breaks parity with 002’s
flag extension pattern); always multi-line listing (rejected: breaks 001/002 default).

## R5 — Error handling and streams

**Decision**: Reuse existing `main()` error mapping: `FileNotFoundError`, `NotADirectoryError`,
`PermissionError`, and other `OSError` from listing/stat → message on **stderr**, exit **1**; success
listing on **stdout** only, exit **0**. Empty directory → success with empty **stdout**.

**Rationale**: Constitution **UX consistency** and prior `contracts/cli.md` patterns; **SC-003**
requires distinguishable failures.

**Alternatives considered**: Per-entry skip on stat failure (rejected: spec treats unreadable directory
as failure; partial listing risks misleading output).

## R6 — Testing approach

**Decision**: `unittest` with `tempfile.TemporaryDirectory`; unit tests for `list_file_sizes(path)`
(returning structured rows or lines); subprocess tests for `python -m pdf_count --list-file-sizes`.

**Rationale**: Stdlib-only test runner already used in `tests/test_count.py`; subprocess tests lock
the CLI contract.

**Alternatives considered**: `pytest` (rejected: not repo standard).
