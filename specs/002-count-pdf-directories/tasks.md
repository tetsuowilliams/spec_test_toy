---
description: "Task list for feature 002-count-pdf-directories"
---

# Tasks: Count directories that contain PDFs

**Input**: Design documents from `/Users/gareth/personal_dev/spec_test_toy/specs/002-count-pdf-directories/`  
**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/cli.md](contracts/cli.md), [quickstart.md](quickstart.md)

**Tests**: Required per `.specify/memory/constitution.md` and [plan.md](plan.md) (stdlib `unittest`). Add failing tests for the new counting function before implementation; extend subprocess coverage for `--count-pdf-directories` after `main()` supports the flag.

**Organization**: Single user story (**US1**, P1). MVP = complete through Phase 3 checkpoint.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: User story label for Phase 3 tasks only (`[US1]`)

## Path Conventions

Repository root: `/Users/gareth/personal_dev/spec_test_toy`  
Package: `/Users/gareth/personal_dev/spec_test_toy/pdf_count/` · Tests: `/Users/gareth/personal_dev/spec_test_toy/tests/` (per [plan.md](plan.md))

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm existing package layout and design inputs before changing behavior.

- [x] T001 [P] Review `/Users/gareth/personal_dev/spec_test_toy/specs/002-count-pdf-directories/contracts/cli.md` and `/Users/gareth/personal_dev/spec_test_toy/specs/002-count-pdf-directories/plan.md` for the `--count-pdf-directories` flag and touched modules (`pdf_count/count.py`, `tests/test_count.py`)
- [x] T002 [P] Verify `/Users/gareth/personal_dev/spec_test_toy/pdf_count/__main__.py`, `/Users/gareth/personal_dev/spec_test_toy/pdf_count/count.py`, and `/Users/gareth/personal_dev/spec_test_toy/tests/test_count.py` exist and `python -m unittest discover -s /Users/gareth/personal_dev/spec_test_toy/tests -p 'test_*.py'` passes on the branch before new work (baseline for **001** default CLI)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Single-source PDF detection rules and expose a stable function name for **US1** tests to import.

**⚠️ CRITICAL**: Complete this phase before **US1** implementation beyond stubs.

- [x] T003 Refactor `/Users/gareth/personal_dev/spec_test_toy/pdf_count/count.py` so `count_pdfs()` and future traversal logic share one helper for “immediate child is an in-scope `.pdf` regular file” (same `lstat` / `stat.S_ISREG` / case-insensitive suffix semantics as today); re-run `/Users/gareth/personal_dev/spec_test_toy/tests/test_count.py` to confirm default mode is unchanged per [contracts/cli.md](../001-count-pdfs-in-directory/contracts/cli.md)
- [x] T004 Add `count_directories_with_direct_pdfs(root: pathlib.Path) -> int` in `/Users/gareth/personal_dev/spec_test_toy/pdf_count/count.py` per [data-model.md](data-model.md) (full implementation landed with T006)

**Checkpoint**: `from pdf_count.count import count_directories_with_direct_pdfs` works from repo root; calling it fails until implemented; all existing tests still pass.

---

## Phase 3: User Story 1 — Count PDF-holding directories under a folder (Priority: P1) 🎯 MVP

**Goal**: User passes one directory and optional `--count-pdf-directories`; in that mode the tool prints a single integer count of directories in the tree (including the root when applicable) that **directly** contain at least one in-scope PDF, or a clear error with non-zero exit ([spec.md](spec.md), [contracts/cli.md](contracts/cli.md)).

**Independent Test**: Build temp fixtures per **User Story 1** in [spec.md](spec.md) (nested chains, multiple qualifiers, one directory with many PDFs still counts once, `archive.pdf` directory exclusion, leading-dot filenames, extension casing, empty tree, invalid root); run `python -m pdf_count --count-pdf-directories` and assert stdout/stderr/exit; confirm bare `python -m pdf_count <dir>` still matches **001** behavior.

### Tests for User Story 1 (required by constitution unless Complexity Tracking approves deferral) ⚠️

> **NOTE**: Complete **T005** before **T006** so unit tests fail first. Complete **T007** before or alongside **T008** so subprocess assertions target a working CLI.

- [x] T005 [US1] Add failing-first `unittest` cases in `/Users/gareth/personal_dev/spec_test_toy/tests/test_count.py` for `count_directories_with_direct_pdfs()` covering [spec.md](spec.md) acceptance scenarios (nested-only PDF, root with direct PDF, sibling folders, multiple PDFs in one folder, `.pdf` directory name exclusion, empty tree, extension case rules)
- [x] T006 [US1] Implement `count_directories_with_direct_pdfs()` in `/Users/gareth/personal_dev/spec_test_toy/pdf_count/count.py` using `os.walk(..., followlinks=False)` and the shared per-directory PDF check; on any traversal/`lstat` failure, raise/propagate so `main()` can exit with stderr + non-zero without printing a success count ([research.md](research.md) R2–R3)
- [x] T007 [US1] Extend `argparse` and `main()` in `/Users/gareth/personal_dev/spec_test_toy/pdf_count/count.py`: add optional `--count-pdf-directories`; when set, print `count_directories_with_direct_pdfs` result; when unset, keep existing `count_pdfs` path unchanged ([contracts/cli.md](contracts/cli.md))
- [x] T008 [US1] Extend `/Users/gareth/personal_dev/spec_test_toy/tests/test_count.py` with subprocess tests invoking `python -m pdf_count --count-pdf-directories` on temp trees and bad paths; assert stdout, stderr, and exit codes; include one case verifying omission of the flag still runs **001** behavior

**Checkpoint**: New mode matches **FR-001**–**FR-006** in [spec.md](spec.md); full unittest suite green from `/Users/gareth/personal_dev/spec_test_toy`.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Manual validation and doc alignment.

- [x] T009 Run `python -m unittest discover -s /Users/gareth/personal_dev/spec_test_toy/tests -p 'test_*.py'` from `/Users/gareth/personal_dev/spec_test_toy` and reconcile any gaps with [quickstart.md](quickstart.md) smoke steps
- [x] T010 [P] Manual pass: follow **Independent Test** in [spec.md](spec.md) and success criteria **SC-001**–**SC-003** (optional **SC-002** spot-check with a generated tree within stated bounds)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1** → **Phase 2** → **Phase 3 (US1)** → **Phase 4**
- **US1** is the only story in [spec.md](spec.md); there is no **US2**/**US3**.

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Phase 2; depends on **T003**–**T004** (shared helper + importable API).

### Within User Story 1

1. **T005** before **T006** (unit tests fail first).  
2. **T006** before **T007** (core logic before CLI wiring).  
3. **T007** before **T008** (CLI exists for subprocess tests), or implement **T007** and **T008** together once **T006** passes.

### Parallel Opportunities

- **Phase 1**: **T001** and **T002** touch different verification activities (docs vs baseline test run)—safe to parallelize procedurally.
- **Phase 4**: **T010** can run independently after **T009** completes.

---

## Parallel Example: User Story 1

Sequential implementation is recommended because tests and code share `/Users/gareth/personal_dev/spec_test_toy/tests/test_count.py` and `/Users/gareth/personal_dev/spec_test_toy/pdf_count/count.py`.

```text
After T006 passes unit tests:
  Developer A: T007 (CLI) then T008 (subprocess) on the same branch in order.
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1–2 (shared helper, stub, green baseline).  
2. Complete Phase 3 (**T005**→**T008**).  
3. **STOP and VALIDATE**: `python -m pdf_count --count-pdf-directories <dir>` matches [spec.md](spec.md).  
4. Complete Phase 4 (quickstart + manual SC checks).

### Incremental Delivery

This feature is a single story; delivery is binary: flag off (**001**), flag on (**002**). Ship Phase 3 as the feature; Phase 4 is validation only.

---

## Notes

- Every checkbox line uses the required `- [ ] TID ...` pattern and includes file paths.  
- Keep default CLI invocation backward compatible ([contracts/cli.md](contracts/cli.md) compatibility section).  
- Prefer the exact flag spelling `--count-pdf-directories` from design docs.
