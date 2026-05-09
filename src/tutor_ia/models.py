from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class DocumentChunk:
    id: str
    source: str
    text: str


@dataclass(frozen=True)
class Query:
    text: str


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: DocumentChunk
    score: float


@dataclass(frozen=True)
class AnswerResponse:
    question: str
    answer: str
    sources: List[RetrievedChunk]
