from pathlib import Path
from typing import Iterable

from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".pl", ".md"}


def load_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def load_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"\n[Pagina {index}]\n{text}")
    return "\n".join(pages)


def load_document(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return load_pdf(path)
    if suffix in {".txt", ".pl", ".md"}:
        return load_text_file(path)
    raise ValueError(f"Formato no soportado: {path}")


def iter_documents(folder: Path) -> Iterable[tuple[Path, str]]:
    if not folder.exists():
        raise FileNotFoundError(f"No existe la carpeta de documentos: {folder}")
    for path in sorted(folder.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            text = load_document(path).strip()
            if text:
                yield path, text
