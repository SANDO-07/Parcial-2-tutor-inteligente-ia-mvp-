# Tutor Inteligente de Inteligencia Artificial — MVP RAG

Proyecto académico basado en las semanas 7 a 11 del curso de Inteligencia Artificial. El sistema propone un tutor académico con arquitectura RAG que ingiere documentos locales del curso y responde preguntas usando recuperación de contexto.

## Objetivo
Diseñar e implementar un MVP de tutor inteligente que permita consultar contenidos de IA: búsqueda, lógica de predicados, Prolog, aprendizaje automático y redes neuronales.

## Estructura

```text
src/tutor_ia/
  config.py       Configuración general
  models.py       Entidades del dominio
  loaders.py      Lectura de PDF, TXT y PL
  chunker.py      Fragmentación de documentos
  indexer.py      Indexación de documentos
  retriever.py    Recuperación y generación de respuesta
  cli.py          Interfaz por consola
docs/
  DOCUMENTO_FINAL_MVP.md
  GUIA_PRUEBAS.md
  MEJORAS_LOGICA.md
examples/
  sample_prolog.pl
  tabla_verdad.txt
```

## Instalación rápida

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Ejecutar indexación

Coloque sus documentos PDF, TXT o PL dentro de `data/docs/` y ejecute:

```bash
python -m src.tutor_ia.indexer --docs data/docs --out storage
```

## Consultar al tutor

```bash
python -m src.tutor_ia.cli --storage storage
```

Ejemplo de pregunta:

```text
¿Qué diferencia hay entre búsqueda en amplitud y búsqueda en profundidad?
```

## Nota académica
El código está pensado como MVP funcional y demostrable. En producción se recomienda usar ChromaDB, embeddings semánticos y un LLM generativo conectado por API o modelo local.
