# Implementation Plan: Print file sizes in a directory

**Branch**: `003-print-file-sizes` | **Date**: 2026-06-09 | **Spec**: [spec.md](spec.md)  
**Input**: Feature specification from `specs/003-print-file-sizes/spec.md`  
**Plan constraints**: Extend existing **plain CLI**, **no third-party dependencies**, **Python stdlib**.

## Summary

Add a **`--list-file-sizes`** mode to the existing `pdf_count` CLI. Given one directory path, list
every **immediate-child regular file** with its filesystem byte size (`lstat.st_size`), one
`name<TAB>size` line per file on stdout, sorted alphabetically by name. Preserve default
document-count and `--count-pdf-directories` behaviors. Reuse established error handling (stderr +
exit `1` on failure).

## Technical Context

**Language/Version**: Python 3.10+ (stdlib only; align with `pdf_count` and workspace rules)  
**Primary Dependencies**: None (standard library only)  
**Storage**: N/A (read-only directory listing and stat)  
**Testing**: `unittest` (stdlib); subprocess CLI tests per `contracts/cli.md`  
**Target Platform**: macOS, Linux, Windows (path/encoding per OS; tests use `pathlib` / temp dirs)  
**Project Type**: CLI utility extension (single package, no network)  
**Performance Goals**: Align with spec **SC-002**: up to **1,000** immediate children listed within
**5 seconds** on a typical PC; single `iterdir` pass with per-entry `lstat`.  
**Constraints**: No PyPI packages; success listing on stdout only; errors on stderr; exit `1` on
failure; `--list-file-sizes` mutually exclusive with `--count-pdf-directories`.  
**Scale/Scope**: One directory argument, non-recursive, all regular files (no extension filter).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify alignment with `.specify/memory/constitution.md` (test_speckit Constitution):

- **Code quality**: Extend `pdf_count/count.py` with a focused function (e.g. `list_file_sizes`);
  reuse `_ArgumentParser` and existing exception mapping; no new dependency surface.
- **Testing**: Unit tests for listing rules (sort order, sizes, symlinks, subfolders, hidden names,
  zero-byte files); subprocess tests for `--list-file-sizes` stdout/stderr/exit codes; regression
  tests that default and `--count-pdf-directories` modes remain unchanged.
- **UX consistency**: Documented deviation—multi-line stdout in listing mode vs single integer in count
  modes; failures match existing stderr patterns; flag mutual exclusion prevents ambiguous output.
- **Performance**: Spec **SC-002**; single non-recursive directory iteration.
- **Traceability**: Plan maps **FR-001**–**FR-006** to `list_file_sizes` + CLI contract; **SC-001**–**SC-003**
  verified by tests + `quickstart.md`.

**Post-Phase-1 re-check**: Artifacts (`research.md`, `data-model.md`, `contracts/`, `quickstart.md`)
introduce no new scope; constitution gates remain satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/003-print-file-sizes/
├── plan.md              # This file
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1
├── contracts/           # Phase 1
└── spec.md
```

### Source Code (repository root)

```text
pdf_count/
├── __init__.py
├── __main__.py          # python -m pdf_count ...
└── count.py             # count_pdfs, count_directories_with_direct_pdfs, list_file_sizes, main()

tests/
├── test_count.py        # extend: list_file_sizes unit + CLI subprocess tests
└── __init__.py
```

**Structure Decision**: No new package; add `list_file_sizes(path) -> list[tuple[str, int]]` (or
equivalent) and wire `--list-file-sizes` in existing `main()`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations; nothing recorded.

---

## Phase 0: Research

See [research.md](research.md). All technical choices resolved; no `NEEDS CLARIFICATION` remains in
this plan.

## Phase 1: Design

- [data-model.md](data-model.md) — target directory, listed file, listing ordering.  
- [contracts/cli.md](contracts/cli.md) — `--list-file-sizes` invocation, streams, exit codes, compatibility.  
- [quickstart.md](quickstart.md) — run and verify locally.

**Agent context**: Updated via `.specify/scripts/bash/update-agent-context.sh cursor-agent` after this
plan was written.
