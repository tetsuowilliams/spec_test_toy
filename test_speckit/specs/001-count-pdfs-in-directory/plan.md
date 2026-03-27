# Implementation Plan: Count PDFs in a directory

**Branch**: `001-count-pdfs-in-directory` | **Date**: 2025-03-27 | **Spec**: [spec.md](spec.md)  
**Input**: Feature specification from `specs/001-count-pdfs-in-directory/spec.md`  
**Plan constraints (user)**: Plain CLI, **no third-party dependencies**, implementation in **Python**.

## Summary

Deliver a small Python command-line tool that accepts one directory path, counts **immediate child**
regular files whose names end with `.pdf` (case-insensitive), prints a single integer on success, and
prints a clear error message to the standard error stream with a non-zero exit status on failure paths
described in the spec. Use **Python standard library only** (`argparse`, `pathlib`, `os`/`sys`).

## Technical Context

**Language/Version**: Python 3.10+ (stdlib only; 3.10+ for consistent `Path`/`stat` usage patterns)  
**Primary Dependencies**: None (standard library only)  
**Storage**: N/A (read-only directory listing)  
**Testing**: `unittest` (stdlib); optional manual runs per `quickstart.md`  
**Target Platform**: macOS, Linux, Windows (path and encoding behavior per OS; tests use `pathlib` / temp dirs)  
**Project Type**: CLI utility (single feature, no network)  
**Performance Goals**: Align with spec **SC-002**: list and classify up to **1,000** immediate children and
return within **5 seconds** on a typical PC; single `scandir`/`iterdir` pass avoids N+1 stat storms.  
**Constraints**: No PyPI packages; success output is one line containing digits only (the count);
errors on `stderr`; non-zero exit code on failure.  
**Scale/Scope**: One directory argument, non-recursive, extension-based PDF detection only.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify alignment with `.specify/memory/constitution.md` (test_speckit Constitution):

- **Code quality**: Small modules, clear naming, no dependency surface beyond stdlib; adopt
  `ruff`/`mypy` when project CI adds them—for now complexity stays low enough to satisfy intent.
- **Testing**: Core counting and extension rules covered by **unit tests**; error paths (missing
  path, file-not-dir, permission errors simulated where feasible) covered by **integration-style**
  tests using temporary directories; matches spec **Independent Test**.
- **UX consistency**: First CLI in repo—behavior documented in `contracts/cli.md`; success = one
  numeric line on **stdout**; failures = message on **stderr** + non-zero exit (per spec **FR-004** /
  **FR-005**).
- **Performance**: Spec **SC-002**; implementation uses single directory iteration, no recursive
  walks.
- **Traceability**: Plan maps **FR-001**–**FR-005** to `pdf_count` package and CLI contract; **SC-001**–**SC-003**
  verified by tests + manual quickstart.

**Post-Phase-1 re-check**: Artifacts (`research.md`, `data-model.md`, `contracts/`, `quickstart.md`)
introduce no new scope; constitution gates remain satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/001-count-pdfs-in-directory/
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
├── __main__.py          # python -m pdf_count <directory>
└── count.py             # count_pdfs(path) and CLI wiring helpers

tests/
├── test_count.py        # unittest: counting rules and CLI integration
└── __init__.py
```

**Structure Decision**: Single package `pdf_count` at repo root with `tests/` alongside it keeps
imports simple (`from pdf_count.count import count_pdfs`) and matches “plain CLI / no deps”.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations; nothing recorded.

---

## Phase 0: Research

See [research.md](research.md). All technical choices resolved; no `NEEDS CLARIFICATION` remains in
this plan.

## Phase 1: Design

- [data-model.md](data-model.md) — conceptual entities and counting rules.  
- [contracts/cli.md](contracts/cli.md) — invocation, streams, exit codes.  
- [quickstart.md](quickstart.md) — run and verify locally.

**Agent context**: Updated via `.specify/scripts/bash/update-agent-context.sh cursor-agent` after this
plan was written.
