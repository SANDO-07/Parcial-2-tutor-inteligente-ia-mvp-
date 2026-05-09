from src.tutor_ia.chunker import split_text


def test_split_text_generates_chunks():
    text = "a" * 1200
    chunks = split_text(text, chunk_size=500, overlap=100)
    assert len(chunks) == 3
    assert all(len(chunk) <= 500 for chunk in chunks)
