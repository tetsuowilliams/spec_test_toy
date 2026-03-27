---
description: "Task list for feature 001-count-pdfs-in-directory"
---

# Tasks: Count PDFs in a directory

**Input**: Design documents from `/Users/gareth/personal_dev/spec_test_toy/test_speckit/specs/001-count-pdfs-in-directory/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/cli.md](contracts/cli.md), [quickstart.md](quickstart.md)

**Tests**: Required per `.specify/memory/constitution.md` and [plan.md](plan.md) (stdlib `unittest`). Write unit tests before implementing `count_pdfs`; add CLI subprocess tests after the entrypoint exists.

**Organization**: Single user story (**US1**, P1). MVP = complete through Phase 3 checkpoint.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: User story label for Phase 3 tasks only (`[US1]`)

## Path Conventions

Repository root: `/Users/gareth/personal_dev/spec_test_toy/test_speckit/`  
Package: `pdf_count/` · Tests: `tests/` (per [plan.md](plan.md))

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize package and test package layout (stdlib only; no `requirements.txt` with PyPI pins).

- [x] T001 Create project structure: `/Users/gareth/personal_dev/spec_test_toy/test_speckit/pdf_count/__init__.py`, `/Users/gareth/personal_dev/spec_test_toy/test_speckit/pdf_count/__main__.py`, `/Users/gareth/personal_dev/spec_test_toy/test_speckit/pdf_count/count.py`, `/Users/gareth/personal_dev/spec_test_toy/test_speckit/tests/__init__.py`, `/Users/gareth/personal_dev/spec_test_toy/test_speckit/tests/test_count.py` (empty or placeholder) per [plan.md](plan.md)
- [x] T002 [P] Add minimal package marker content to `/Users/gareth/personal_dev/spec_test_toy/test_speckit/pdf_count/__init__.py` (docstring or `__all__` plan only; no third-party imports)
- [x] T003 [P] Add minimal `/Users/gareth/personal_dev/spec_test_toy/test_speckit/tests/__init__.py` so `python -m unittest discover -s /Users/gareth/personal_dev/spec_test_toy/test_speckit/tests -p 'test_*.py'` can run from repo root per [quickstart.md](quickstart.md)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Stable import surface for `count_pdfs` before **US1** tests import it.

**⚠️ CRITICAL**: No user story implementation work proceeds until this phase is complete.

- [x] T004 Add `count_pdfs` stub in `/Users/gareth/personal_dev/spec_test_toy/test_speckit/pdf_count/count.py`: accept `pathlib.Path`, typed per [data-model.md](data-model.md), raise `NotImplementedError` until Phase 3 implementation (enables failing-first tests)

**Checkpoint**: `from pdf_count.count import count_pdfs` works from repo root; calling `count_pdfs` fails until implemented.

---

## Phase 3: User Story 1 — Get PDF count for a folder (Priority: P1) 🎯 MVP

**Goal**: User passes one directory; tool prints a single integer count of immediate-child `.pdf` regular files (case-insensitive extension) or a clear error with non-zero exit (see [spec.md](spec.md), [contracts/cli.md](contracts/cli.md)).

**Independent Test**: Build temp fixtures per **User Story 1** in [spec.md](spec.md) (mixed files, subfolder with extra PDF, invalid path, non-directory path, permission denial if feasible, `archive.pdf` directory, `.report.pdf`, unicode/spaces path); verify counts and CLI outcomes.

### Tests for User Story 1 (required by constitution unless Complexity Tracking approves deferral) ⚠️

> **NOTE**: Implement **T005** before **T006** so tests fail first (`count_pdfs`). Add **T008** after **T007** so CLI subprocess cases can pass.

- [x] T005 [US1] Implement unittest cases in `/Users/gareth/personal_dev/spec_test_toy/test_speckit/tests/test_count.py` for `count_pdfs` covering [spec.md](spec.md) acceptance scenarios 1–8 (use `tempfile.TemporaryDirectory` and `pathlib.Path`; include non-recursive, extension case, directory named like `.pdf`, leading-dot filename)
- [x] T006 [US1] Implement `count_pdfs` in `/Users/gareth/personal_dev/spec_test_toy/test_speckit/pdf_count/count.py` per [research.md](research.md) (`Path.iterdir()`, `is_file(follow_symlinks=False)`, `.name.lower().endswith(".pdf")`); raise or propagate filesystem errors for CLI layer per plan
- [x] T007 [US1] Implement CLI entry in `/Users/gareth/personal_dev/spec_test_toy/test_speckit/pdf_count/__main__.py` and `main()` (or equivalent) in `/Users/gareth/personal_dev/spec_test_toy/test_speckit/pdf_count/count.py` using `argparse`: single positional directory, success prints count + newline on stdout only, failures message stderr + exit `1` per [contracts/cli.md](contracts/cli.md)
- [x] T008 [US1] Extend `/Users/gareth/personal_dev/spec_test_toy/test_speckit/tests/test_count.py` with `subprocess` tests invoking `python -m pdf_count` against temp dirs and bad paths; assert stdout, stderr, and exit codes match [contracts/cli.md](contracts/cli.md)

**Checkpoint**: `python -m pdf_count <dir>` from `/Users/gareth/personal_dev/spec_test_toy/test_speckit` matches spec **FR-001**–**FR-005**; full unittest suite green.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Validation against design docs and performance sanity (single `iterdir` pass).

- [x] T009 Run `python -m unittest discover -s /Users/gareth/personal_dev/spec_test_toy/test_speckit/tests -p 'test_*.py'` from `/Users/gareth/personal_dev/spec_test_toy/test_speckit` and reconcile any gaps with [quickstart.md](quickstart.md) smoke steps
- [x] T010 [P] Manual pass: follow **Independent Test** in [spec.md](spec.md) and success criteria **SC-001**–**SC-003** (timing **SC-002** spot-check optional for ~1k entries)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1** → **Phase 2** → **Phase 3 (US1)** → **Phase 4**
- **US1** is the only story; there is no **US2**/**US3** in this feature.

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Phase 2; no other stories.

### Within User Story 1

1. **T005** before **T006** (unit tests fail first).
2. **T006** before **T007** (core logic before CLI).
3. **T007** before **T008** (CLI exists before subprocess tests).
4. **T009**–**T010** after Phase 3 checkpoint.

### Parallel Opportunities

- After **T001**: **T002** and **T003** in parallel.
- **T010** can run independently once **T009** is green.

---

## Parallel Example: User Story 1

```bash
# After T001 only:
# T002: edit pdf_count/__init__.py
# T003: edit tests/__init__.py
```

---

## Implementation Strategy

### MVP First (User Story 1 only)

1. Complete Phase 1–2 (layout + `count_pdfs` stub).
2. **T005** → **T006** → **T007** → **T008** (TDD for counting; CLI tests last).
3. **STOP and VALIDATE** at Phase 3 checkpoint; run Phase 4.

### Incremental Delivery

This feature ships as a single increment (**US1**). Future enhancements (recursive scan, content-based PDF detection) would be new specs.

---

## Notes

- No PyPI dependencies; use Python 3.10+ only.
- Re-export `count_pdfs` from `pdf_count/__init__.py` only if desired for public API; tests may import from `pdf_count.count`.
- Commit after each task or logical group; keep `Complexity Tracking` empty unless constitution exception is required.
