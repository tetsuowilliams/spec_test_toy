# Data model: Print file sizes in a directory

**Feature**: `003-print-file-sizes`  
**Date**: 2026-06-09

This feature has no database. These are **conceptual** entities used by the tool and tests.

## Target directory

| Attribute | Description |
|-----------|-------------|
| Path | User-supplied filesystem path; MUST exist and be a directory for a successful listing. |
| Immediate children | Files, folders, and other entries directly inside the directory; only regular files among these are listed. |

**Validation rules**

- If the path does not exist → error (spec edge case: missing path).
- If the path is not a directory (e.g. plain file) → error.
- If the directory cannot be listed or an entry cannot be stat’d as required → error.

## Listed file

| Attribute | Description |
|-----------|-------------|
| Location | Direct child of the target directory (not nested in a subfolder). |
| Kind | Platform **regular file** per `lstat` (`S_ISREG`); symbolic links are excluded even if the target is a file. |
| Name | Final path component as displayed to the user (includes leading-dot names). |
| Size (bytes) | Non-negative integer from `lstat.st_size` for that entry. |

**Examples**

- `notes.txt` (1,024 bytes), `.hidden.cfg` (0 bytes) → in scope with reported sizes.
- Subdirectory `archive/` → **not** listed (not a regular file).
- Symbolic link `link.txt` → **not** listed (**FR-006**).
- `nested/extra.txt` inside a subfolder → **not** in scope (not an immediate child).

## Derived value: file-size listing

Ordered sequence of **listed file** rows, sorted alphabetically by **Name** (case-sensitive string
order). Rendered on success as one stdout line per row: `{Name}\t{Size (bytes)}`.

On success with zero in-scope files, the listing is **empty** (no lines).
