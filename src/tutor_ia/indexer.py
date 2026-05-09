import argparse
from pathlib import Path
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer

from .chunker import build_chunks
from .config import RagConfig
from .loaders import iter_documents
from .models import DocumentChunk


def build_index(docs_path: Path, storage_path: Path, config: RagConfig = RagConfig()) -> int:
    chunks: list[DocumentChunk] = []
    for path, text in iter_documents(docs_path):
        chunks.extend(build_chunks(path.name, text, config.chunk_size, config.overlap))

    if not chunks:
        raise RuntimeError("No se encontraron documentos válidos para indexar.")

    vectorizer = TfidfVectorizer(strip_accents="unicode", lowercase=True, ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([chunk.text for chunk in chunks])

    storage_path.mkdir(parents=True, exist_ok=True)
    payload = {"vectorizer": vectorizer, "matrix": matrix, "chunks": chunks, "config": config}
    with (storage_path / config.index_filename).open("wb") as file:
        pickle.dump(payload, file)

    return len(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Indexa documentos locales para el Tutor Inteligente de IA.")
    parser.add_argument("--docs", default="data/docs", help="Carpeta con documentos PDF, TXT, PL o MD")
    parser.add_argument("--out", default="storage", help="Carpeta de salida del índice")
    args = parser.parse_args()

    total = build_index(Path(args.docs), Path(args.out))
    print(f"Indexación completada. Fragmentos generados: {total}")


if __name__ == "__main__":
    main()
