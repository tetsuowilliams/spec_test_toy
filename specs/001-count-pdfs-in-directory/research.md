# Research: Count PDFs in a directory

**Feature**: `001-count-pdfs-in-directory`  
**Date**: 2025-03-27

## R1 — Language and dependency policy

**Decision**: Implement with **Python 3.10+** using **only the standard library**.

**Rationale**: User requirement “plain CLI no added dependencies” plus “Use python”; stdlib provides
`pathlib.Path`, `Path.iterdir()`, `Path.is_file()`, and suffix checks without third-party packages.

**Alternatives considered**: Rust/Go (rejected: user asked for Python); Python + `click` or `typer`
(rejected: extra dependencies).

## R2 — Directory listing and PDF detection

**Decision**: Use `pathlib.Path` for the user argument; iterate **immediate children only** via
`iterdir()`; count entries where `entry.is_file(follow_symlinks=False)` is true and
`entry.name.lower().endswith(".pdf")`.

**Rationale**: Matches spec **FR-002**–**FR-003** (regular files only, non-recursive,
case-insensitive extension). `is_file(follow_symlinks=False)` avoids counting symlinked paths as
files when the platform would follow; `archive.pdf` as a **directory** name fails `is_file` and is
excluded per acceptance scenario 6.

**Alternatives considered**: `os.scandir` (valid for performance; `pathlib` is sufficient for 1k
entries and simpler); content-based magic-byte PDF detection (rejected by spec assumptions).

## R3 — CLI interface and errors

**Decision**: `python -m pdf_count <directory>`; parse with `argparse`; on success print the integer
and newline to **stdout**; on failure print a short explanation to **stderr** and exit with code **1**
(user-visible “non-success” per **FR-005** / **SC-003**).

**Rationale**: Single positional path matches **FR-001**; stream split matches Unix conventions and
spec UX notes; `argparse` is stdlib and avoids custom argv parsing bugs.

**Alternatives considered**: Zero exit on all paths (rejected: obscures failure); silent stderr
(rejected: **SC-003**).

## R4 — Testing approach

**Decision**: `unittest` with `tempfile.TemporaryDirectory` and `pathlib` to create fixtures for
acceptance scenarios (mixed files, subfolders, wrong path, non-directory path).

**Rationale**: No test runner dependency beyond stdlib; subprocess or `unittest.mock` can exercise
`python -m pdf_count` end-to-end when needed.

**Alternatives considered**: `pytest` (rejected: adds dependency unless later adopted repo-wide).
