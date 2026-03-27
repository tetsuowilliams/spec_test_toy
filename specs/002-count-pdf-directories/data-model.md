# Data model: Count directories that contain PDFs

**Feature**: `002-count-pdf-directories`  
**Date**: 2026-03-27

No database. These are **conceptual** entities used by the tool and tests.

## Root directory

| Attribute | Description |
|-----------|-------------|
| Path | User-supplied filesystem path; MUST exist and be a directory for a successful run. |
| Traversal scope | The entire directory tree rooted at this path: every descendant directory is visited (subject to OS walk behavior and `followlinks=False`). |

**Validation rules**

- Path does not exist → error.
- Path is not a directory → error.
- Any error while walking or inspecting entries (e.g., permission denied) → error for the **whole**
  run (no success count).

## PDF file (in scope)

Same definition as `001`: **regular file** (via `lstat` / `S_ISREG`), name ends with `.pdf`
case-insensitively, extension-only detection.

| Attribute | Description |
|-----------|-------------|
| Location | **Immediate child** of the directory currently being evaluated. |
| Kind | Regular file; entries that are directories, symlinks to non-regular files, etc., do not qualify. |

## Qualifying directory

| Attribute | Description |
|-----------|-------------|
| Definition | Any visited directory (including the root) that has **≥1** in-scope PDF among its **immediate** children. |
| Contribution | Each qualifying directory adds **1** to the output total, regardless of how many in-scope PDFs it directly contains. |

## Derived value: Directory count

Non-negative integer: number of qualifying directories in the tree. On success in
`--count-pdf-directories` mode, this is the sole **stdout** payload (one line, decimal, newline).
