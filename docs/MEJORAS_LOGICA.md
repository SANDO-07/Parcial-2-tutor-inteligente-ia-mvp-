# Mejoras recomendadas para la lógica del Tutor RAG

1. Reemplazar TF-IDF por embeddings semánticos con `sentence-transformers` o `text-embedding-3-small`.
2. Usar ChromaDB como vector store real para persistencia semántica.
3. Agregar un LLM generativo con una regla estricta: responder únicamente con contexto recuperado.
4. Incorporar citación automática por documento, página y fragmento.
5. Separar aún más la arquitectura usando interfaces: `DocumentLoader`, `VectorStore`, `Retriever` y `AnswerGenerator`.
6. Agregar evaluación RAG con preguntas esperadas y comparación de precisión.
7. Mejorar seguridad con validación contra prompt injection, filtrado de instrucciones maliciosas y política de rechazo.
8. Agregar interfaz web en Streamlit o FastAPI para presentación final.
9. Agregar soporte OCR solo si los PDF tienen texto no extraíble.
10. Crear dataset de preguntas frecuentes del curso para probar la calidad del tutor.
