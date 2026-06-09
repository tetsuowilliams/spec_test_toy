---
description: "Task list for feature 003-print-file-sizes"
---

# Tasks: Print file sizes in a directory

**Input**: Design documents from `/Users/gareth/Development/spec_test_toy/specs/003-print-file-sizes/`  
**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/cli.md](contracts/cli.md), [quickstart.md](quickstart.md)

**Tests**: Required per `.specify/memory/constitution.md` and [plan.md](plan.md) (stdlib `unittest`). Add failing tests for `list_file_sizes` before implementation; extend subprocess coverage for `--list-file-sizes` after `main()` supports the flag.

**Organization**: Single user story (**US1**, P1). MVP = complete through Phase 3 checkpoint.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: User story label for Phase 3 tasks only (`[US1]`)

## Path Conventions

Repository root: `/Users/gareth/Development/spec_test_toy`  
Package: `/Users/gareth/Development/spec_test_toy/pdf_count/` · Tests: `/Users/gareth/Development/spec_test_toy/tests/` (per [plan.md](plan.md))

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm existing package layout and design inputs before changing behavior.

- [x] T001 [P] Review `/Users/gareth/Development/spec_test_toy/specs/003-print-file-sizes/contracts/cli.md` and `/Users/gareth/Development/spec_test_toy/specs/003-print-file-sizes/plan.md` for the `--list-file-sizes` flag, output format (`{name}\t{size}`), and touched modules (`pdf_count/count.py`, `tests/test_count.py`)
- [x] T002 [P] Verify `/Users/gareth/Development/spec_test_toy/pdf_count/__main__.py`, `/Users/gareth/Development/spec_test_toy/pdf_count/count.py`, and `/Users/gareth/Development/spec_test_toy/tests/test_count.py` exist and `python3 -m unittest discover -s /Users/gareth/Development/spec_test_toy/tests -p 'test_*.py'` passes on the branch before new work (baseline for **001** default and **002** `--count-pdf-directories` modes)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Stable import surface for `list_file_sizes` before **US1** tests import it.

**⚠️ CRITICAL**: Complete this phase before **US1** implementation beyond stubs.

- [x] T003 Add `list_file_sizes(path: pathlib.Path) -> list[tuple[str, int]]` stub in `/Users/gareth/Development/spec_test_toy/pdf_count/count.py` per [data-model.md](data-model.md): typed return of `(name, size_bytes)` rows; raise `NotImplementedError` until Phase 3 implementation (enables failing-first tests)

**Checkpoint**: `from pdf_count.count import list_file_sizes` works from repo root; calling `list_file_sizes` fails until implemented; all existing tests still pass.

---

## Phase 3: User Story 1 — List file sizes for a folder (Priority: P1) 🎯 MVP

**Goal**: User passes one directory with `--list-file-sizes`; tool prints sorted `name<TAB>size` lines for immediate-child regular files (bytes, `lstat` semantics) or a clear error with non-zero exit ([spec.md](spec.md), [contracts/cli.md](contracts/cli.md)).

**Independent Test**: Build temp fixtures per **User Story 1** in [spec.md](spec.md) (mixed sizes, zero-byte file, subfolder with extra files, invalid path, non-directory path, permission denial if feasible, directory and symlink exclusions, `.hidden` file, unicode/spaces path); run `python3 -m pdf_count --list-file-sizes` and assert stdout/stderr/exit; confirm bare `python3 -m pdf_count <dir>` and `--count-pdf-directories` still match **001**/**002** behavior.

### Tests for User Story 1 (required by constitution unless Complexity Tracking approves deferral) ⚠️

> **NOTE**: Complete **T004** before **T005** so unit tests fail first. Complete **T006** before **T007** so subprocess assertions target a working CLI.

- [x] T004 [US1] Add failing-first `unittest` cases in `/Users/gareth/Development/spec_test_toy/tests/test_count.py` for `list_file_sizes()` covering [spec.md](spec.md) acceptance scenarios 1–9 (use `tempfile.TemporaryDirectory` and `pathlib.Path`; include sort order, byte sizes, non-recursive scope, hidden names, zero-byte file, directory/symlink exclusion where platform allows; permission test with `@unittest.skipUnless(os.name == "posix", ...)` consistent with existing tests)
- [x] T005 [US1] Implement `list_file_sizes()` in `/Users/gareth/Development/spec_test_toy/pdf_count/count.py` per [research.md](research.md) (`Path.iterdir()`, per-entry `lstat()`, `stat.S_ISREG`, `st.st_size`; sort rows alphabetically by name; raise `FileNotFoundError` / `NotADirectoryError` / propagate `PermissionError` and `OSError` for CLI layer)
- [x] T006 [US1] Extend `argparse` and `main()` in `/Users/gareth/Development/spec_test_toy/pdf_count/count.py`: add `--list-file-sizes` in a mutually exclusive group with `--count-pdf-directories`; when set, print `f"{name}\t{size}\n"` for each row from `list_file_sizes`; when unset, keep existing `count_pdfs` / `count_directories_with_direct_pdfs` paths unchanged ([contracts/cli.md](contracts/cli.md))
- [x] T007 [US1] Extend `/Users/gareth/Development/spec_test_toy/tests/test_count.py` with subprocess tests invoking `python3 -m pdf_count --list-file-sizes` on temp dirs and bad paths; assert stdout tab format, stderr, and exit codes; include cases for empty directory, conflicting flags (`--list-file-sizes` + `--count-pdf-directories`), and regression that default and `--count-pdf-directories` modes are unchanged

**Checkpoint**: New mode matches **FR-001**–**FR-006** in [spec.md](spec.md); full unittest suite green from `/Users/gareth/Development/spec_test_toy`.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Manual validation and doc alignment.

- [x] T008 Run `python3 -m unittest discover -s /Users/gareth/Development/spec_test_toy/tests -p 'test_*.py'` from `/Users/gareth/Development/spec_test_toy` and reconcile any gaps with [quickstart.md](quickstart.md) smoke steps
- [x] T009 [P] Manual pass: follow **Independent Test** in [spec.md](spec.md) and success criteria **SC-001**–**SC-003** (optional **SC-002** spot-check with a generated folder within stated bounds)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1** → **Phase 2** → **Phase 3 (US1)** → **Phase 4**
- **US1** is the only story; there is no **US2**/**US3** in this feature.

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Phase 2; no other stories.

### Within User Story 1

1. **T004** before **T005** (unit tests fail first).
2. **T005** before **T006** (core logic before CLI wiring).
3. **T006** before **T007** (CLI exists before subprocess tests).
4. **T008**–**T009** after Phase 3 checkpoint.

### Parallel Opportunities

- **T001** and **T002** in parallel (Phase 1).
- **T009** can run independently once **T008** is green.

---

## Parallel Example: User Story 1

```bash
# Phase 1 only:
# T001: review specs/003-print-file-sizes/contracts/cli.md
# T002: run baseline unittest discover

# US1 sequence (not parallel — shared files):
# T004 → T005 → T006 → T007 in tests/test_count.py and pdf_count/count.py
```

---

## Implementation Strategy

### MVP First (User Story 1 only)

1. Complete Phase 1–2 (review baseline + `list_file_sizes` stub).
2. **T004** → **T005** → **T006** → **T007** (TDD for listing; CLI tests last).
3. **STOP and VALIDATE** at Phase 3 checkpoint; run Phase 4.

### Incremental Delivery

This feature ships as a single increment (**US1**). Future enhancements (recursive listing, human-readable units, totals) would be new specs.

---

## Notes

- No PyPI dependencies; use Python 3.10+ only.
- Tests may import `list_file_sizes` from `pdf_count.count`; re-export from `pdf_count/__init__.py` only if desired.
- Commit after each task or logical group; keep `Complexity Tracking` empty unless constitution exception is required.
