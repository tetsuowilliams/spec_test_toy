# CLI contract: `pdf_count`

**Feature**: `001-count-pdfs-in-directory`  
**Date**: 2025-03-27

## Invocation

```text
python -m pdf_count <directory>
```

- **`<directory>`**: Required positional argument. Accepts paths with spaces or Unicode when the
  shell/OS passes them through to Python (user responsibility to quote paths as usual).

## Success behavior

- **stdout**: Exactly one line: decimal representation of the non-negative integer count, followed by
  a newline (`\n`). No leading/trailing spaces. No extra prose.
- **stderr**: Empty or unused in success scenarios.
- **Exit code**: `0`.

## Failure behavior

Failures include: path does not exist; path is not a directory; cannot read directory contents
(permission or OS error).

- **stdout**: Must not emit a misleading success count (empty is acceptable).
- **stderr**: At least one line of human-readable English explaining the failure (may include OS
  message context).
- **Exit code**: Non-zero (use `1` for all logical failures unless a future spec distinguishes codes).

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `directory` | Yes | Filesystem path to the folder whose **immediate** children are scanned. |

No optional flags in v1 (keeps “plain CLI” minimal).
