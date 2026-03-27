# Quickstart: Count directories that contain PDFs

**Feature**: `002-count-pdf-directories`  
**Date**: 2026-03-27

## Prerequisites

- Python **3.10+** on `PATH`
- Repository root contains the `pdf_count/` package (after implementation on this branch)

## Run (after implementation)

From repository root:

**Recursive directory count** (this feature)

```bash
python -m pdf_count --count-pdf-directories /path/to/tree
```

Expected: one line with a non-negative integer (number of directories that **directly** contain at
least one `.pdf` regular file, case-insensitive extension).

**Baseline** (unchanged from `001`)

```bash
python -m pdf_count /path/to/folder
```

Expected: one line with the count of PDF files in that folder’s **immediate** children only.

### Examples

```bash
# Tree: root/sub/a.pdf only → one qualifying directory (sub), root does not qualify
python -m pdf_count --count-pdf-directories ./fixture_root
# Expect: 1

# Same tree: baseline counts PDFs at top level of root only
python -m pdf_count ./fixture_root
# Expect: 0
```

Paths with spaces (shell-quoted):

```bash
python -m pdf_count --count-pdf-directories "/path/with spaces/tree"
```

## Run tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Verify against spec (manual smoke)

1. Build `root/sub/deep/file.pdf` only → `--count-pdf-directories` expects **1** (only `deep`
   qualifies).
2. Put `report.pdf` directly under `root` → count includes **root** if root is the argument.
3. Two sibling folders each with a PDF → count **2** for those folders (plus any other qualifiers).
4. One folder with three PDFs → contributes **1** to the directory count.
5. Subfolder named `archive.pdf` → does **not** qualify its parent as having a PDF.
6. Non-directory or missing path → non-zero exit and stderr message.
