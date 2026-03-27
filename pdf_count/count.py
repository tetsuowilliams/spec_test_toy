"""Core counting logic and CLI entrypoint."""

from __future__ import annotations

import argparse
import stat
import sys
from pathlib import Path


def count_pdfs(path: Path) -> int:
    """Count immediate-child regular files whose names end with ``.pdf`` (case-insensitive).

    Uses ``lstat`` per entry so symbolic links are not counted as regular files even if their
    targets are.

    Raises:
        FileNotFoundError: Path does not exist.
        NotADirectoryError: Path exists but is not a directory.
        PermissionError, OSError: Cannot list or stat directory entries.
    """
    if not path.exists():
        raise FileNotFoundError(path)
    if not path.is_dir():
        raise NotADirectoryError(path)

    n = 0
    for entry in path.iterdir():
        st = entry.lstat()
        if stat.S_ISREG(st.st_mode) and entry.name.lower().endswith(".pdf"):
            n += 1
    return n


class _ArgumentParser(argparse.ArgumentParser):
    """Use exit code 1 for argument errors (see contracts/cli.md)."""

    def error(self, message: str) -> None:  # type: ignore[override]
        self.print_usage(sys.stderr)
        self.exit(1, f"{self.prog}: error: {message}\n")


def main(argv: list[str] | None = None) -> int:
    parser = _ArgumentParser(prog="pdf_count", description="Count .pdf files in a directory.")
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory whose immediate children are scanned (non-recursive).",
    )
    args = parser.parse_args(argv)

    target = args.directory
    try:
        n = count_pdfs(target)
    except FileNotFoundError:
        print(f"Error: directory does not exist: {target}", file=sys.stderr)
        return 1
    except NotADirectoryError:
        print(f"Error: not a directory: {target}", file=sys.stderr)
        return 1
    except PermissionError as e:
        print(f"Error: permission denied: {e.filename or target}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Error: cannot read directory ({e.strerror or e}): {target}", file=sys.stderr)
        return 1

    print(n)
    return 0
