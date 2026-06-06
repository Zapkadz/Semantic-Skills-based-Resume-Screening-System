from pathlib import Path

import pytest

from src.document_loader import load_text_file, load_text_files_from_directory


def test_load_text_file_reads_utf8_text(tmp_path: Path) -> None:
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("Java Spring Boot\nREST API", encoding="utf-8")

    text = load_text_file(sample_file)

    assert text == "Java Spring Boot\nREST API"


def test_load_text_file_strips_outer_whitespace(tmp_path: Path) -> None:
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("\nBackend Java Developer\n\n", encoding="utf-8")

    text = load_text_file(sample_file)

    assert text == "Backend Java Developer"


def test_load_text_file_raises_when_file_missing(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError, match="Text file not found"):
        load_text_file(missing_file)


def test_load_text_file_raises_when_path_is_directory(tmp_path: Path) -> None:
    with pytest.raises(IsADirectoryError, match="Expected a text file path"):
        load_text_file(tmp_path)


def test_load_text_file_raises_for_unsupported_extension(tmp_path: Path) -> None:
    pdf_file = tmp_path / "resume.pdf"
    pdf_file.write_text("PDF content is not supported in Phase 02", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file extension"):
        load_text_file(pdf_file)


def test_load_text_files_from_directory_reads_txt_files_in_order(tmp_path: Path) -> None:
    (tmp_path / "b_candidate.txt").write_text("Candidate B", encoding="utf-8")
    (tmp_path / "a_candidate.txt").write_text("Candidate A", encoding="utf-8")
    (tmp_path / "notes.md").write_text("Ignore markdown", encoding="utf-8")

    documents = load_text_files_from_directory(tmp_path)

    assert documents == [
        {
            "path": str(tmp_path / "a_candidate.txt"),
            "filename": "a_candidate.txt",
            "text": "Candidate A",
        },
        {
            "path": str(tmp_path / "b_candidate.txt"),
            "filename": "b_candidate.txt",
            "text": "Candidate B",
        },
    ]


def test_load_text_files_from_directory_raises_when_missing(tmp_path: Path) -> None:
    missing_directory = tmp_path / "missing"

    with pytest.raises(FileNotFoundError, match="Directory not found"):
        load_text_files_from_directory(missing_directory)


def test_load_text_files_from_directory_raises_when_path_is_file(tmp_path: Path) -> None:
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("not a directory", encoding="utf-8")

    with pytest.raises(NotADirectoryError, match="Expected a directory path"):
        load_text_files_from_directory(sample_file)
