from .models import DocumentChunk


def split_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size debe ser mayor que cero")
    if overlap >= chunk_size:
        raise ValueError("overlap debe ser menor que chunk_size")

    clean = " ".join(text.split())
    chunks: list[str] = []
    start = 0
    while start < len(clean):
        end = min(start + chunk_size, len(clean))
        chunks.append(clean[start:end])
        if end == len(clean):
            break
        start = end - overlap
    return chunks


def build_chunks(source: str, text: str, chunk_size: int, overlap: int) -> list[DocumentChunk]:
    return [
        DocumentChunk(id=f"{source}::chunk-{i}", source=source, text=chunk)
        for i, chunk in enumerate(split_text(text, chunk_size, overlap), start=1)
    ]
