# Data model: Count PDFs in a directory

**Feature**: `001-count-pdfs-in-directory`  
**Date**: 2025-03-27

This feature has no database. These are **conceptual** entities used by the tool and tests.

## Target directory

| Attribute | Description |
|-----------|-------------|
| Path | User-supplied filesystem path; MUST exist and be a directory for a successful count. |
| Immediate children | Files and folders directly inside the directory; only these are candidates for counting. |

**Validation rules**

- If the path does not exist → error (spec edge case: missing path).
- If the path is not a directory (e.g. plain file) → error.
- If the directory cannot be listed (e.g. permission denied) → error.

## PDF file (in scope)

| Attribute | Description |
|-----------|-------------|
| Location | Direct child of the target directory (not nested in a subfolder). |
| Kind | Platform **regular file** (`is_file()` with symlinks not followed as in research). |
| Name rule | Final component ends with `.pdf` when compared **case-insensitively**. |

**Examples**

- `report.PDF`, `doc.pdf`, `.hidden.pdf` → in scope if they are regular files.
- Subdirectory named `archive.pdf` → **not** in scope (not a file).
- `nested/foo.pdf` inside a subfolder → **not** in scope (not an immediate child).

## Derived value: PDF count

Non-negative integer: number of in-scope PDF files. On success this is the sole **stdout** payload.
