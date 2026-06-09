"""Core counting logic and CLI entrypoint."""

from __future__ import annotations

import argparse
import os
import stat
import sys
from pathlib import Path


_IN_SCOPE_SUFFIXES = (".pdf", ".doc")


def _is_in_scope_document_file(name: str, st_mode: int) -> bool:
    """True if ``name`` / ``st_mode`` describe an in-scope document regular file (lstat semantics)."""
    lower = name.lower()
    return stat.S_ISREG(st_mode) and any(lower.endswith(suffix) for suffix in _IN_SCOPE_SUFFIXES)


def _is_in_scope_pdf_file(name: str, st_mode: int) -> bool:
    """True if ``name`` / ``st_mode`` describe an in-scope PDF regular file (lstat semantics)."""
    return stat.S_ISREG(st_mode) and name.lower().endswith(".pdf")


def directory_has_direct_pdf(path: Path) -> bool:
    """Return True if ``path`` has at least one immediate child that is an in-scope PDF file.

    Raises:
        PermissionError, OSError: Cannot list or stat directory entries.
    """
    for entry in path.iterdir():
        st = entry.lstat()
        if _is_in_scope_pdf_file(entry.name, st.st_mode):
            return True
    return False


def count_pdfs(path: Path) -> int:
    """Count immediate-child regular files whose names end with ``.pdf`` or ``.doc`` (case-insensitive).

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
        if _is_in_scope_document_file(entry.name, st.st_mode):
            n += 1
    return n


def _reraise_walk_error(exc: OSError) -> None:
    """Abort ``os.walk`` on any suppressed scandir/listing failure (spec FR-006)."""
    raise exc


def count_directories_with_direct_pdfs(root: Path) -> int:
    """Count directories under ``root`` that directly contain at least one in-scope PDF file.

    Every directory reachable from ``root`` is visited (``os.walk``, symlinks not followed).
    ``root`` itself is included.

    Raises:
        FileNotFoundError: Path does not exist.
        NotADirectoryError: Path exists but is not a directory.
        PermissionError, OSError: Cannot traverse or inspect the tree.
    """
    if not root.exists():
        raise FileNotFoundError(root)
    if not root.is_dir():
        raise NotADirectoryError(root)

    n = 0
    for dirpath, _, _ in os.walk(
        root,
        topdown=True,
        followlinks=False,
        onerror=_reraise_walk_error,
    ):
        if directory_has_direct_pdf(Path(dirpath)):
            n += 1
    return n


class _ArgumentParser(argparse.ArgumentParser):
    """Use exit code 1 for argument errors (see contracts/cli.md)."""

    def error(self, message: str) -> None:  # type: ignore[override]
        self.print_usage(sys.stderr)
        self.exit(1, f"{self.prog}: error: {message}\n")


def main(argv: list[str] | None = None) -> int:
    parser = _ArgumentParser(
        prog="pdf_count",
        description="Count .pdf and .doc files in a directory.",
    )
    parser.add_argument(
        "--count-pdf-directories",
        action="store_true",
        help="Recursively count directories that directly contain at least one .pdf file.",
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory to scan (non-recursive file count by default).",
    )
    args = parser.parse_args(argv)

    target = args.directory
    try:
        if args.count_pdf_directories:
            n = count_directories_with_direct_pdfs(target)
        else:
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
