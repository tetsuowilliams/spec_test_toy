# Quickstart: Count PDFs in a directory

**Feature**: `001-count-pdfs-in-directory`  
**Date**: 2025-03-27

## Prerequisites

- Python **3.10+** on `PATH`
- Repository root is `test_speckit/` (parent of `pdf_count/` once implementation exists)

## Run (after implementation)

From repository root:

```bash
python -m pdf_count /path/to/your/folder
```

Expected: one line with a non-negative integer.

### Examples

```bash
# Empty folder
python -m pdf_count ./empty_dir
# Expect: 0

# Folder with three PDFs at top level only
python -m pdf_count ./mixed
# Expect: 3
```

Path with spaces (shell-quoted):

```bash
python -m pdf_count "/path/with spaces/inbox"
```

## Run tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Verify against spec (manual smoke)

1. Create a temp folder with `a.pdf`, `b.PDF`, `note.txt`, and a subfolder `inner/` containing
   `c.pdf` → expect count **2** (not 3).
2. Point at a non-existent path → expect non-zero exit and message on stderr.
3. Point at a file path → expect non-zero exit and clear error.
