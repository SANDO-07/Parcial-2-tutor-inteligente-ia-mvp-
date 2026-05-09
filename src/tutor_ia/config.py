from dataclasses import dataclass


@dataclass(frozen=True)
class RagConfig:
    chunk_size: int = 900
    overlap: int = 150
    top_k: int = 4
    min_score: float = 0.08
    index_filename: str = "rag_index.joblib"
