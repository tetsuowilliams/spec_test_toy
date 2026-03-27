# CLI contract: `pdf_count` (directory aggregation mode)

**Feature**: `002-count-pdf-directories`  
**Date**: 2026-03-27  

This document extends [the baseline `pdf_count` CLI](../../001-count-pdfs-in-directory/contracts/cli.md)
(`001-count-pdfs-in-directory`). Unless stated here, behavior is unchanged.

## Invocation

**Default mode (unchanged)**

```text
python -m pdf_count <directory>
```

**Recursive directory count mode (this feature)**

```text
python -m pdf_count --count-pdf-directories <directory>
```

- **`<directory>`**: Required positional argument (same path rules as baseline: spaces/Unicode when
  the shell/OS passes them through correctly).

## Success behavior

### Default mode

Unchanged: **stdout** is one line with the count of **immediate-child** in-scope PDF files (non-recursive).

### `--count-pdf-directories` mode

- **stdout**: Exactly one line: decimal representation of the non-negative integer count of **directories**
  under `<directory>` (including `<directory>` itself) that **directly** contain at least one in-scope
  PDF regular file, followed by a newline (`\n`). No leading/trailing spaces. No extra prose.
- **stderr**: Empty or unused in success scenarios.
- **Exit code**: `0`.

## Failure behavior

Applies to both modes where relevant.

Failures include: path does not exist; path is not a directory; cannot complete traversal or classify
entries (e.g., permission denied on any part of the tree needed for the count).

- **stdout**: Must not emit a misleading success count (empty is acceptable).
- **stderr**: At least one line of human-readable English explaining the failure.
- **Exit code**: Non-zero (use `1` consistent with baseline unless a future spec distinguishes codes).

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `directory` | Yes | Root of the tree to scan. |
| `--count-pdf-directories` | No | When set, output is the recursive **directory** count per feature spec; when omitted, baseline **file** count (immediate children only). |

## Compatibility

`python -m pdf_count <directory>` with **no** flags MUST remain the `001` behavior for the same
`<directory>` inputs.
