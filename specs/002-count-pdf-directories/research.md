# Research: Count directories that contain PDFs

**Feature**: `002-count-pdf-directories`  
**Date**: 2026-03-27

## R1 — Integration with existing `pdf_count` CLI

**Decision**: Add an optional flag **`--count-pdf-directories`** to `python -m pdf_count`. When
absent, behavior remains **identical** to `001` (non-recursive count of immediate-child PDF files).
When present, the tool performs a **recursive** visit of all directories under the root and prints the
number of directories that **directly** contain at least one in-scope PDF.

**Rationale**: One installable entry point, one spec extension, minimal user confusion; backward
compatible for scripts that already call `pdf_count` without flags.

**Alternatives considered**: Separate module / console script (rejected: duplicates PDF detection and
error messaging); mandatory positional mode argument (rejected: breaks existing one-arg usage).

## R2 — Tree traversal and symlink policy

**Decision**: Use **`os.walk(top, topdown=True[, followlinks=False])`** (default
`followlinks=False`) to enumerate directory paths. At each `dirpath`, evaluate immediate children for
at least one in-scope PDF using the **same** regular-file and extension rules as `count_pdfs` in
`count.py` (`pathlib.Path` + `entry.lstat()` + `stat.S_ISREG` + case-insensitive `.pdf` suffix).

**Rationale**: Spec assumption: symlinks follow OS defaults—“do not follow symlinks when walking”
matches Python’s default and avoids cycles/extra scope from linked trees; aligns with existing use of
`lstat` for PDF detection.

**Alternatives considered**: `pathlib.Path.rglob` only (awkward for “every directory” without
double-counting files); `followlinks=True` (rejected: spec does not require descending symlinked
directories).

## R3 — Failure semantics on partial traversal

**Decision**: If **any** directory listing or `lstat` needed for the walk fails (e.g., permission
denied on a subtree), **abort** the whole operation: print an explanatory message to **stderr**, exit
non-zero, **no** success count on stdout (per **FR-006** / **SC-003**).

**Rationale**: Avoid silently under-counting when part of the tree is unreadable; matches strict
interpretation of “must not report a successful directory count as if the input were fully valid and
traversable.”

**Alternatives considered**: Skip unreadable subtrees and continue (rejected: misleading totals);
partial counts on stdout (rejected: spec).

## R4 — Testing approach

**Decision**: Extend `tests/test_count.py` with `unittest` and temporary directory fixtures: nested
layouts from acceptance scenarios, multiple PDFs in one folder (count once), `archive.pdf` as a
directory name, and CLI subprocess tests for `--count-pdf-directories` output and error paths.

**Rationale**: Same stack as `001`; tree fixtures exercise traversal and deduplication.

**Alternatives considered**: New test file only (optional; keeping one module is simpler unless size
grows unwieldy).
