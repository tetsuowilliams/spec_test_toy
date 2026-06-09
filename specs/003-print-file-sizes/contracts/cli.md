# CLI contract: `pdf_count` (file-size listing mode)

**Feature**: `003-print-file-sizes`  
**Date**: 2026-06-09

This document extends [the baseline `pdf_count` CLI](../../001-count-pdfs-in-directory/contracts/cli.md)
and coexists with [directory aggregation mode](../../002-count-pdf-directories/contracts/cli.md).
Unless stated here, behavior of other modes is unchanged.

## Invocation

**Default mode (unchanged)**

```text
python -m pdf_count <directory>
```

**Recursive directory count mode (unchanged, feature 002)**

```text
python -m pdf_count --count-pdf-directories <directory>
```

**File-size listing mode (this feature)**

```text
python -m pdf_count --list-file-sizes <directory>
```

- **`<directory>`**: Required positional argument (same path rules as baseline: spaces/Unicode when
  the shell/OS passes them through correctly).
- **`--list-file-sizes`** and **`--count-pdf-directories`** MUST NOT be combined in one invocation;
  the tool MUST reject conflicting flags with a clear argument error (exit `1`, message on stderr).

## Success behavior

### Default and `--count-pdf-directories` modes

Unchanged per linked contracts.

### `--list-file-sizes` mode

- **stdout**: Zero or more lines, each exactly one listed regular file. Each line is `{name}\t{size}\n`
  where `{name}` is the file’s final path component and `{size}` is the decimal byte count with no
  separators. Lines are sorted alphabetically by `{name}` (case-sensitive). No header line. No
  trailing blank line beyond the final newline of the last data line (if any).
- **stderr**: Empty or unused in success scenarios.
- **Exit code**: `0`.

**Example** (illustrative):

```text
alpha.txt	10
beta.txt	0
```

### Empty directory

Success with **stdout** empty (no lines).

## Failure behavior

Applies to `--list-file-sizes` where relevant; other modes unchanged.

Failures include: path does not exist; path is not a directory; cannot list directory or stat entries
needed for the listing (e.g., permission denied).

- **stdout**: Must not emit a misleading file listing (empty is acceptable).
- **stderr**: At least one line of human-readable English explaining the failure.
- **Exit code**: Non-zero (use `1` consistent with baseline unless a future spec distinguishes codes).

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `directory` | Yes | Filesystem path whose **immediate** children are scanned for regular files. |
| `--list-file-sizes` | No | When set, output is the per-file byte listing per this contract; mutually exclusive with `--count-pdf-directories`. |
| `--count-pdf-directories` | No | Unchanged from feature 002 when `--list-file-sizes` is not set. |

## Compatibility

`python -m pdf_count <directory>` with **no** flags MUST remain the `001` document-count behavior.
`python -m pdf_count --count-pdf-directories <directory>` MUST remain the `002` behavior when
`--list-file-sizes` is not set.
