"""Document loading utilities for text-based JD and resume inputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any


SUPPORTED_TEXT_EXTENSIONS = {".txt"}
DEFAULT_ENCODING = "utf-8"


def load_text_file(path: str | Path, encoding: str = DEFAULT_ENCODING) -> str:
    """Read a supported text file and return its raw content.

    The loader is intentionally narrow in the MVP: it only supports `.txt`
    files. PDF and DOCX support will be added in later phases after the text
    pipeline is stable.
    """
    file_path = Path(path)
    _validate_text_file_path(file_path)

    return file_path.read_text(encoding=encoding).strip()


def load_text_files_from_directory(
    directory: str | Path,
    encoding: str = DEFAULT_ENCODING,
) -> list[dict[str, Any]]:
    """Load all supported text files from a directory in filename order."""
    directory_path = Path(directory)
    _validate_directory_path(directory_path)

    documents: list[dict[str, Any]] = []
    for file_path in sorted(directory_path.iterdir()):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_TEXT_EXTENSIONS:
            documents.append(
                {
                    "path": str(file_path),
                    "filename": file_path.name,
                    "text": load_text_file(file_path, encoding=encoding),
                }
            )

    return documents


def _validate_text_file_path(file_path: Path) -> None:
    """Validate a path before reading it as an MVP text document."""
    if not file_path.exists():
        raise FileNotFoundError(f"Text file not found: {file_path}")

    if not file_path.is_file():
        raise IsADirectoryError(f"Expected a text file path, got directory: {file_path}")

    if file_path.suffix.lower() not in SUPPORTED_TEXT_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_TEXT_EXTENSIONS))
        raise ValueError(
            f"Unsupported file extension '{file_path.suffix}'. "
            f"Supported extensions: {supported}"
        )


def _validate_directory_path(directory_path: Path) -> None:
    """Validate a directory before scanning text documents inside it."""
    if not directory_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    if not directory_path.is_dir():
        raise NotADirectoryError(f"Expected a directory path, got file: {directory_path}")
