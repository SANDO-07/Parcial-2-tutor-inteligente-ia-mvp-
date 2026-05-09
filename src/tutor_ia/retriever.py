from pathlib import Path
import pickle

from sklearn.metrics.pairwise import cosine_similarity

from .config import RagConfig
from .models import AnswerResponse, Query, RetrievedChunk


class RagRetriever:
    def __init__(self, storage_path: Path, config: RagConfig = RagConfig()) -> None:
        self.config = config
        index_file = storage_path / config.index_filename
        if not index_file.exists():
            raise FileNotFoundError("No existe el índice. Ejecute primero indexer.py")
        with index_file.open("rb") as file:
            payload = pickle.load(file)
        self.vectorizer = payload["vectorizer"]
        self.matrix = payload["matrix"]
        self.chunks = payload["chunks"]

    def retrieve(self, query: Query) -> list[RetrievedChunk]:
        query_vector = self.vectorizer.transform([query.text])
        similarities = cosine_similarity(query_vector, self.matrix).flatten()
        best_indexes = similarities.argsort()[::-1][: self.config.top_k]
        results: list[RetrievedChunk] = []
        for idx in best_indexes:
            score = float(similarities[idx])
            if score >= self.config.min_score:
                results.append(RetrievedChunk(chunk=self.chunks[idx], score=score))
        return results

    def answer(self, query_text: str) -> AnswerResponse:
        safe_query = self._sanitize_query(query_text)
        query = Query(text=safe_query)
        results = self.retrieve(query)
        if not results:
            return AnswerResponse(
                question=query_text,
                answer="No encontré suficiente información en los documentos indexados para responder con seguridad.",
                sources=[],
            )
        answer = self._compose_answer(safe_query, results)
        return AnswerResponse(question=query_text, answer=answer, sources=results)

    @staticmethod
    def _sanitize_query(query: str) -> str:
        blocked_terms = ["ignora las instrucciones", "borra", "elimina", "system prompt", "api key"]
        clean = query.strip()
        lowered = clean.lower()
        for term in blocked_terms:
            if term in lowered:
                raise ValueError("La pregunta contiene instrucciones potencialmente inseguras.")
        return clean

    @staticmethod
    def _compose_answer(query: str, results: list[RetrievedChunk]) -> str:
        context = "\n".join(f"- {item.chunk.text}" for item in results)
        return (
            "Respuesta basada en los documentos recuperados:\n\n"
            f"Pregunta: {query}\n\n"
            "Síntesis: "
            "Según el material encontrado, la respuesta debe construirse a partir de los siguientes puntos clave:\n"
            f"{context}\n\n"
            "Nota: este MVP no inventa información fuera del contexto recuperado."
        )
