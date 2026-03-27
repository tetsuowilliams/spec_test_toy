# Implementation Plan: Count directories that contain PDFs

**Branch**: `002-count-pdf-directories` | **Date**: 2026-03-27 | **Spec**: [spec.md](spec.md)  
**Input**: Feature specification from `specs/002-count-pdf-directories/spec.md`  
**Plan constraints**: Extend existing **`pdf_count`** CLI; **no third-party dependencies**; **Python**
standard library only (matches `001-count-pdfs-in-directory`).

## Summary

Extend the existing Python CLI (`python -m pdf_count`) so users can optionally count **how many
directories** under a given root **directly contain** at least one qualifying `.pdf` regular file
(case-insensitive suffix), visiting **every descendant directory** under that root. Default mode
remains **unchanged**: count immediate-child PDF files only (non-recursive), preserving backward
compatibility. New mode prints a single integer on success; errors use **stderr** and non-zero exit,
consistent with the current contract. Traversal uses **`os.walk(..., followlinks=False)`** plus the
same **per-directory** `lstat` + extension rules as `count_pdfs`, so symlinked directories are not
descended and directory names ending in `.pdf` never qualify as PDFs.

## Technical Context

**Language/Version**: Python 3.10+ (stdlib only; align with `pdf_count` and workspace rules)  
**Primary Dependencies**: None (standard library only)  
**Storage**: N/A (read-only directory traversal)  
**Testing**: `unittest` (stdlib); temp directories + subprocess or direct `main()` calls  
**Target Platform**: macOS, Linux, Windows (path and `os.walk` behavior per OS)  
**Project Type**: CLI utility (extends existing package)  
**Performance Goals**: Align with spec **SC-002**: up to **2,000** directories and **10,000** files
under the root, result within **10 seconds** on a typical PC; one linear traversal, no repeated
full-tree rescans.  
**Constraints**: No PyPI packages; success = one decimal integer line on **stdout**; failures on
**stderr** with exit **1** (or consistent with existing `pdf_count` error handling).  
**Scale/Scope**: Single directory argument plus one optional flag for mode selection; extension-based
PDF detection only.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify alignment with `.specify/memory/constitution.md` (test_speckit Constitution):

- **Code quality**: Reuse `pdf_count` patterns (`Path`, `argparse`, `lstat` / `stat.S_ISREG`); shared
  helper for “immediate child is in-scope PDF” avoids divergent rules; keep modules small.
- **Testing**: Unit tests for traversal counting, deduplication per directory, extension and file-type
  rules, empty trees; integration tests for CLI flag, invalid root, and simulated unreadable
  subtree where feasible; matches spec **Independent Test** and acceptance scenarios.
- **UX consistency**: Same invocation style as `001`; additive flag; success = single numeric line;
  failures = stderr + non-zero exit (**FR-005** / **FR-006**, **SC-003**).
- **Performance**: Spec **SC-002**; `os.walk` + O(children) work per directory—no N² replays.
- **Traceability**: Plan maps **FR-001**–**FR-006** to new counting function + CLI; **SC-001**–**SC-003**
  covered by tests and `quickstart.md`.

**Post-Phase-1 re-check**: `research.md`, `data-model.md`, `contracts/cli.md`, and `quickstart.md` add
no scope beyond the spec; constitution gates remain satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/002-count-pdf-directories/
├── plan.md              # This file
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1
├── contracts/           # Phase 1
│   └── cli.md
├── checklists/
└── spec.md
```

### Source Code (repository root)

```text
pdf_count/
├── __init__.py
├── __main__.py
└── count.py             # count_pdfs; new traversal helper + argparse flag

tests/
├── test_count.py        # extend: new counting mode + CLI
└── __init__.py
```

**Structure Decision**: Single package `pdf_count` at repo root (existing layout); implement
recursive **directory** counting in `count.py` next to `count_pdfs`, exposed via CLI flag documented
in `contracts/cli.md`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations; nothing recorded.

---

## Phase 0: Research

See [research.md](research.md). All technical choices resolved; no `NEEDS CLARIFICATION` remains in
this plan.

## Phase 1: Design

- [data-model.md](data-model.md) — entities and rules for qualifying directories.  
- [contracts/cli.md](contracts/cli.md) — invocation, flag, streams, exit codes.  
- [quickstart.md](quickstart.md) — run and verify locally.

**Agent context**: Updated via `.specify/scripts/bash/update-agent-context.sh cursor-agent` after this
plan was written.
