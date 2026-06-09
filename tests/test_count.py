from __future__ import annotations

import contextlib
import io
import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pdf_count.count import count_directories_with_direct_pdfs, count_pdfs, main

REPO_ROOT = Path(__file__).resolve().parents[1]


def _touch(d: Path, name: str) -> Path:
    p = d / name
    p.write_text("", encoding="utf-8")
    return p


class CountPdfsTests(unittest.TestCase):
    """Unit tests for count_pdfs — spec acceptance 1–8."""

    def test_three_pdfs_mixed_other_files(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _touch(root, "a.pdf")
            _touch(root, "b.PDF")
            _touch(root, "c.Pdf")
            _touch(root, "note.txt")
            self.assertEqual(count_pdfs(root), 3)

    def test_mixed_pdf_and_doc_files(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _touch(root, "a.pdf")
            _touch(root, "b.doc")
            _touch(root, "c.DOC")
            _touch(root, "d.Doc")
            _touch(root, "note.txt")
            self.assertEqual(count_pdfs(root), 4)

    def test_empty_directory(self) -> None:
        with TemporaryDirectory() as tmp:
            self.assertEqual(count_pdfs(Path(tmp)), 0)

    def test_subfolder_pdf_not_counted(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _touch(root, "a.pdf")
            _touch(root, "b.pdf")
            inner = root / "inner"
            inner.mkdir()
            _touch(inner, "c.pdf")
            self.assertEqual(count_pdfs(root), 2)

    def test_subfolder_doc_not_counted(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _touch(root, "a.doc")
            inner = root / "inner"
            inner.mkdir()
            _touch(inner, "b.doc")
            self.assertEqual(count_pdfs(root), 1)

    def test_path_does_not_exist(self) -> None:
        with TemporaryDirectory() as tmp:
            missing = Path(tmp) / "nope"
            with self.assertRaises(FileNotFoundError):
                count_pdfs(missing)

    def test_path_is_file_not_directory(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            f = root / "file.pdf"
            f.write_text("", encoding="utf-8")
            with self.assertRaises(NotADirectoryError):
                count_pdfs(f)

    def test_directory_named_like_pdf_not_counted(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "archive.pdf").mkdir()
            _touch(root, "real.pdf")
            self.assertEqual(count_pdfs(root), 1)

    def test_directory_named_like_doc_not_counted(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "archive.doc").mkdir()
            _touch(root, "real.doc")
            self.assertEqual(count_pdfs(root), 1)

    def test_hidden_style_pdf_name_counted(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _touch(root, ".report.pdf")
            self.assertEqual(count_pdfs(root), 1)

    def test_hidden_style_doc_name_counted(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _touch(root, ".report.doc")
            self.assertEqual(count_pdfs(root), 1)

    def test_docx_not_counted(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _touch(root, "letter.docx")
            _touch(root, "letter.doc")
            self.assertEqual(count_pdfs(root), 1)

    def test_unicode_and_spaces_path(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "földer tür"
            root.mkdir()
            _touch(root, "doc.pdf")
            self.assertEqual(count_pdfs(root), 1)

    @unittest.skipUnless(os.name == "posix", "chmod readability is POSIX-oriented")
    def test_permission_denied_directory(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "locked"
            root.mkdir()
            try:
                root.chmod(0)
                with self.assertRaises(PermissionError):
                    count_pdfs(root)
            finally:
                root.chmod(0o700)


class CountDirectoriesWithDirectPdfsTests(unittest.TestCase):
    """Recursive directory aggregation — spec 002 / plan research."""

    def test_one_subfolder_with_pdf_other_without(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            sub_a = root / "a"
            sub_b = root / "b"
            sub_a.mkdir()
            sub_b.mkdir()
            _touch(sub_a, "doc.pdf")
            _touch(sub_b, "notes.txt")
            self.assertEqual(count_directories_with_direct_pdfs(root), 1)

    def test_root_with_direct_pdf_counts_root_once(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _touch(root, "report.pdf")
            (root / "empty").mkdir()
            self.assertEqual(count_directories_with_direct_pdfs(root), 1)

    def test_nested_chain_only_deepest_dir_qualifies(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            deep = root / "sub" / "deep"
            deep.mkdir(parents=True)
            _touch(deep, "file.pdf")
            self.assertEqual(count_directories_with_direct_pdfs(root), 1)

    def test_no_pdfs_anywhere(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sub").mkdir()
            _touch(root / "sub", "readme.txt")
            self.assertEqual(count_directories_with_direct_pdfs(root), 0)

    def test_two_sibling_folders_each_with_pdf(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            s1 = root / "one"
            s2 = root / "two"
            s1.mkdir()
            s2.mkdir()
            _touch(s1, "a.pdf")
            _touch(s2, "b.PDF")
            self.assertEqual(count_directories_with_direct_pdfs(root), 2)

    def test_multiple_pdfs_same_folder_counts_once(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            inner = root / "inner"
            inner.mkdir()
            _touch(inner, "1.pdf")
            _touch(inner, "2.pdf")
            _touch(inner, "3.Pdf")
            self.assertEqual(count_directories_with_direct_pdfs(root), 1)

    def test_directory_named_pdf_does_not_qualify_parent(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "archive.pdf").mkdir()
            _touch(root, "real.pdf")
            self.assertEqual(count_directories_with_direct_pdfs(root), 1)

    def test_hidden_pdf_filename_qualifies_directory(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _touch(root, ".report.pdf")
            self.assertEqual(count_directories_with_direct_pdfs(root), 1)

    def test_path_does_not_exist(self) -> None:
        with TemporaryDirectory() as tmp:
            missing = Path(tmp) / "gone"
            with self.assertRaises(FileNotFoundError):
                count_directories_with_direct_pdfs(missing)

    def test_path_is_file_not_directory(self) -> None:
        with TemporaryDirectory() as tmp:
            f = Path(tmp) / "x.pdf"
            f.write_text("", encoding="utf-8")
            with self.assertRaises(NotADirectoryError):
                count_directories_with_direct_pdfs(f)

    @unittest.skipUnless(os.name == "posix", "chmod readability is POSIX-oriented")
    def test_permission_denied_on_walk(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            inner = root / "inner"
            inner.mkdir()
            _touch(inner, "a.pdf")
            try:
                inner.chmod(0)
                with self.assertRaises(PermissionError):
                    count_directories_with_direct_pdfs(root)
            finally:
                inner.chmod(0o700)


class CliTests(unittest.TestCase):
    """Subprocess CLI tests per contracts/cli.md."""

    def _run(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "pdf_count", *args],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONUTF8": "1"},
        )

    def test_cli_success_prints_count_and_newline(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _touch(root, "x.pdf")
            _touch(root, "y.PDF")
            p = self._run([str(root)])
            self.assertEqual(p.returncode, 0)
            self.assertEqual(p.stdout, "2\n")
            self.assertEqual(p.stderr, "")

    def test_cli_counts_pdf_and_doc(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _touch(root, "x.pdf")
            _touch(root, "y.doc")
            _touch(root, "z.txt")
            p = self._run([str(root)])
            self.assertEqual(p.returncode, 0)
            self.assertEqual(p.stdout, "2\n")
            self.assertEqual(p.stderr, "")

    def test_cli_nonexistent_path(self) -> None:
        with TemporaryDirectory() as tmp:
            p = self._run([str(Path(tmp) / "missing")])
            self.assertEqual(p.returncode, 1)
            self.assertNotIn("0\n", p.stdout)  # not a misleading success line only
            self.assertIn("Error", p.stderr)

    def test_cli_file_instead_of_directory(self) -> None:
        with TemporaryDirectory() as tmp:
            f = Path(tmp) / "f.pdf"
            f.write_text("", encoding="utf-8")
            p = self._run([str(f)])
            self.assertEqual(p.returncode, 1)
            self.assertIn("Error", p.stderr)

    def test_cli_missing_argument_exits_1(self) -> None:
        p = self._run([])
        self.assertEqual(p.returncode, 1)
        self.assertIn("error", p.stderr.lower())

    def test_cli_count_pdf_directories_success(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            deep = root / "sub" / "deep"
            deep.mkdir(parents=True)
            _touch(deep, "file.pdf")
            p = self._run(["--count-pdf-directories", str(root)])
            self.assertEqual(p.returncode, 0)
            self.assertEqual(p.stdout, "1\n")
            self.assertEqual(p.stderr, "")

    def test_cli_count_pdf_directories_two_qualifiers(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            a = root / "a"
            b = root / "b"
            a.mkdir()
            b.mkdir()
            _touch(a, "x.pdf")
            _touch(b, "y.pdf")
            p = self._run(["--count-pdf-directories", str(root)])
            self.assertEqual(p.returncode, 0)
            self.assertEqual(p.stdout, "2\n")

    def test_cli_count_pdf_directories_nonexistent(self) -> None:
        with TemporaryDirectory() as tmp:
            p = self._run(["--count-pdf-directories", str(Path(tmp) / "nope")])
            self.assertEqual(p.returncode, 1)
            self.assertIn("Error", p.stderr)

    def test_cli_without_flag_still_file_count_mode(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            inner = root / "inner"
            inner.mkdir()
            _touch(inner, "only.pdf")
            p = self._run([str(root)])
            self.assertEqual(p.returncode, 0)
            self.assertEqual(p.stdout, "0\n")

    def test_main_function_returns_code(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _touch(root, "a.pdf")
            self.assertEqual(main([str(root)]), 0)
        with TemporaryDirectory() as tmp:
            deep = Path(tmp) / "d"
            deep.mkdir()
            _touch(deep, "f.pdf")
            self.assertEqual(main(["--count-pdf-directories", str(Path(tmp))]), 0)
        with TemporaryDirectory() as tmp:
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(Path(tmp) / "none")]), 1)


if __name__ == "__main__":
    unittest.main()
