# Quickstart: Print file sizes in a directory

**Feature**: `003-print-file-sizes`  
**Date**: 2026-06-09

## Prerequisites

- Python **3.10+** on `PATH`
- Repository root contains `pdf_count/` and `tests/`

## Run (after implementation)

From repository root:

```bash
python -m pdf_count --list-file-sizes /path/to/your/folder
```

Expected: zero or more lines of `name<TAB>size` (bytes), sorted by name.

### Examples

```bash
# Empty folder
python -m pdf_count --list-file-sizes ./empty_dir
# Expect: no output, exit 0

# Folder with two files at top level
python -m pdf_count --list-file-sizes ./mixed
# Expect lines like:
# a.txt	12
# b.txt	0
```

Path with spaces (shell-quoted):

```bash
python -m pdf_count --list-file-sizes "/path/with spaces/inbox"
```

Verify default count mode is unchanged:

```bash
python -m pdf_count ./mixed
# Expect: single integer line (document count), not a file listing
```

## Run tests

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## Verify against spec (manual smoke)

1. Create a temp folder with `small.txt` (10 bytes), `large.txt` (100 bytes), `.hidden` (0 bytes),
   subfolder `inner/` with `other.txt`, and a symlink to a file → expect **three** lines for the
   immediate regular files only, sorted by name, correct byte sizes.
2. Point at a non-existent path → expect non-zero exit and message on stderr.
3. Point at a file path → expect non-zero exit and clear error.
4. Run with both `--list-file-sizes` and `--count-pdf-directories` → expect argument error, exit 1.
