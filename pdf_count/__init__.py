"""Count PDF files or PDF-bearing directories (stdlib-only CLI)."""

from pdf_count.count import count_directories_with_direct_pdfs, count_pdfs, main

__all__ = ["count_directories_with_direct_pdfs", "count_pdfs", "main"]
