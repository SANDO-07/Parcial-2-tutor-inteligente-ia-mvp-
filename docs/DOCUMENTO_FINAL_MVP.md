# Documento final — Tutor Inteligente de Inteligencia Artificial

## Contexto del ejercicio

El proyecto propone el diseño de un MVP llamado **Tutor Inteligente de Inteligencia Artificial**, un agente académico con arquitectura RAG que responde preguntas de estudiantes utilizando fuentes locales del curso: guía didáctica, reglas de Prolog, tablas de verdad y documentos relacionados con búsqueda informada, lógica de predicados, aprendizaje automático y redes neuronales.

## 1. Stack tecnológico requerido

| Componente | Herramienta | Qué hace | Justificación | Integración |
|---|---|---|---|---|
| Lenguaje base | Python 3.11+ | Implementa el pipeline, lectura de archivos, indexación y consulta. | Python es estándar en IA por su ecosistema y facilidad académica. | Todos los módulos del MVP se desarrollan en Python. |
| Carga de documentos | PyPDF / lectura TXT y PL | Extrae contenido de PDF, archivos de texto y reglas Prolog. | Permite trabajar con fuentes locales reales del curso. | `loaders.py` entrega texto limpio al chunker. |
| Chunking | Módulo propio | Divide documentos en fragmentos con solapamiento. | Evita perder contexto entre secciones. | `chunker.py` crea `DocumentChunk`. |
| Embeddings / recuperación | TF-IDF en MVP; recomendado: sentence-transformers u OpenAI embeddings | Convierte texto en representación numérica para búsqueda. | TF-IDF permite demostración local sin API; embeddings reales mejoran semántica. | `indexer.py` crea matriz; `retriever.py` consulta similitud. |
| Vector store | MVP local con pickle; recomendado: ChromaDB | Persiste índice y fragmentos recuperables. | Para el MVP local es simple; ChromaDB sería ideal en versión avanzada. | Carpeta `storage/`. |
| LLM generativo | MVP sintetiza con contexto; recomendado: GPT-4o, Mistral o Llama 3 | Genera respuesta final. | Un LLM mejora redacción, pero debe limitarse al contexto recuperado. | En versión avanzada se agrega `AnswerGenerator`. |
| Interfaz | CLI; recomendado: Streamlit o FastAPI | Permite hacer preguntas al tutor. | CLI es suficiente para validar el MVP. | `cli.py` ejecuta la interacción. |

## 2. Fase sdd-init: ingestión del repositorio y documentación

El sistema debe ingerir documentos en formatos PDF, `.txt`, `.md` y `.pl`. Los PDF se procesan con PyPDF, mientras que TXT, Markdown y Prolog se leen como texto plano. El proceso inicia cargando los documentos desde `data/docs/`, limpiando espacios innecesarios y dividiendo el contenido en fragmentos.

La estrategia recomendada de chunking es de **900 caracteres con 150 caracteres de solapamiento**. Esta decisión mantiene suficiente contexto para que el tutor comprenda definiciones y ejemplos, sin generar fragmentos demasiado grandes. Para el MVP se utiliza TF-IDF, pero para una versión más profesional se recomienda `text-embedding-3-small` o `sentence-transformers`, ya que capturan similitud semántica y no solo coincidencia literal de palabras.

El vector store sugerido para producción es **ChromaDB local**, porque permite persistencia, búsqueda semántica y uso sin depender de una nube. Para la entrega académica se incluye una implementación local sencilla para demostrar la lógica.

### Prompt propuesto para sdd-init

```markdown
Eres un agente de análisis técnico para un curso de Inteligencia Artificial. Analiza el repositorio local compuesto por PDF, archivos .pl de Prolog y tablas de verdad en .txt. Identifica los temas principales, términos clave, dependencias entre documentos y posibles preguntas que un estudiante podría realizar. No inventes información: todo debe estar basado en los documentos. Entrega un resumen por documento, una lista de conceptos importantes y recomendaciones de chunking para construir un sistema RAG académico.
```

Se recomienda un modelo con gran ventana de contexto, como uno de 128k tokens, porque en la fase inicial se necesita revisar muchos documentos completos, detectar relaciones entre semanas del curso y comprender la estructura global antes de fragmentar el contenido.

## 3. Fases sdd-propose y sdd-spec

### Arquitectura limpia propuesta

| Capa | Componentes | Responsabilidad |
|---|---|---|
| Dominio | `Query`, `DocumentChunk`, `AnswerResponse` | Define entidades puras sin depender de tecnología externa. |
| Aplicación | Casos de uso: indexar documentos y consultar tutor | Coordina las operaciones principales. |
| Infraestructura | Loaders, vectorizador, almacenamiento local o ChromaDB | Implementa detalles técnicos concretos. |
| Interfaz | CLI, futura API o Streamlit | Expone el sistema al usuario final. |

### Prompt para sdd-spec

```markdown
# Spec Request: Tutor Inteligente de IA – RAG MVP

## Contexto
Diseñar un tutor académico que responda preguntas sobre Inteligencia Artificial usando documentos locales del curso. El sistema debe aplicar arquitectura RAG para recuperar fragmentos relevantes y generar una respuesta fundamentada.

## Requisitos Funcionales
- RF-01: El sistema debe cargar documentos PDF, TXT, MD y PL desde una carpeta local.
- RF-02: El sistema debe fragmentar los documentos usando chunking con solapamiento.
- RF-03: El sistema debe indexar los fragmentos para permitir recuperación por similitud.
- RF-04: El estudiante debe poder realizar preguntas en lenguaje natural.
- RF-05: El sistema debe mostrar fuentes recuperadas junto con la respuesta.
- RF-06: El sistema debe rechazar consultas con instrucciones maliciosas o prompt injection.

## Criterios de Aceptación
**Escenario 1:** Dado que existen documentos en `data/docs`, cuando ejecuto `indexer.py`, entonces el sistema genera un índice persistente.

**Escenario 2:** Dado que el índice existe, cuando pregunto por A*, entonces el sistema recupera fragmentos relacionados con `g(n)`, `h(n)` y búsqueda informada.

**Escenario 3:** Dado que el usuario intenta una instrucción maliciosa, cuando escribe una consulta de prompt injection, entonces el sistema la bloquea.

## Restricciones No Funcionales
- El sistema debe ejecutarse localmente.
- Debe usar separación entre indexación y consulta.
- Debe incluir manejo de errores.
- Debe evitar respuestas no fundamentadas en los documentos.
- La respuesta debe generarse en menos de 10 segundos en un conjunto pequeño de documentos.
```

Un modelo especializado en especificaciones técnicas es adecuado porque esta fase requiere convertir requisitos académicos en criterios verificables, casos de aceptación y restricciones medibles.

## 4. Fase sdd-apply

### Prompt para generar código Python del pipeline RAG

```markdown
## sdd-apply Prompt: RAG Indexer + Retriever

Eres un agente de implementación. Genera código Python puro, ordenado y mantenible para un MVP académico llamado Tutor Inteligente de Inteligencia Artificial.

### Módulo 1: indexer.py
- Lee documentos desde: data/docs/
- Soporta formatos: PDF, TXT, MD y PL
- Estrategia de chunking: chunk_size=900, overlap=150
- Modelo de recuperación inicial: TF-IDF local; dejar preparado para embeddings semánticos
- Persiste el índice en: storage/rag_index.joblib

### Módulo 2: retriever.py
- Recibe una query en lenguaje natural
- Valida que la query no sea prompt injection
- Recupera los top-4 fragmentos más relevantes
- Construye una respuesta basada solamente en el contexto recuperado
- Retorna respuesta y fuentes consultadas

### Restricciones
- Usar type hints
- Aplicar try/except donde sea necesario
- Separar responsabilidades por archivo
- No mezclar indexación con consulta
- No inventar respuestas fuera del contexto recuperado
```

Para esta fase se recomienda un modelo especializado en programación porque debe generar código funcional, modular, con tipado, manejo de errores y separación clara de responsabilidades.

## 5. Fase sdd-verify

### Prompt de auditoría

```markdown
## sdd-verify Prompt: Senior Code Reviewer

Eres un revisor senior de IA con experiencia en sistemas RAG, Python y seguridad. Audita el código del Tutor Inteligente de IA.

### Checklist
1. Calidad del código: PEP 8, type hints, claridad y manejo de errores.
2. Alucinaciones: verificar si el sistema puede responder fuera del contexto recuperado.
3. Prompt Injection: revisar si el usuario puede insertar instrucciones maliciosas.
4. SOLID: validar separación de responsabilidades.
5. Indexer/Retriever: confirmar que indexación y consulta estén desacopladas.
6. Pruebas: sugerir casos unitarios y funcionales.

### Para cada hallazgo reporta
- Severidad: CRÍTICO / ADVERTENCIA / SUGERENCIA
- Línea o función afectada
- Descripción del problema
- Corrección recomendada
- Ejemplo de código cuando aplique
```

Se recomienda un modelo de alta capacidad de razonamiento porque la verificación requiere detectar errores sutiles, riesgos de seguridad, alucinaciones, problemas de arquitectura y fallos de lógica que no siempre son evidentes.

## 6. Buenas prácticas SOLID

| Principio | Aplicación | Ejemplo concreto |
|---|---|---|
| S — Single Responsibility | Cada módulo tiene una tarea principal. | `indexer.py` indexa documentos; `retriever.py` responde consultas. |
| O — Open/Closed | El sistema puede extenderse sin modificar toda la lógica. | Se puede agregar ChromaDB reemplazando el almacenamiento local. |
| L — Liskov Substitution | Los componentes deben poder intercambiarse por implementaciones equivalentes. | TF-IDF puede sustituirse por embeddings semánticos si conserva el método de búsqueda. |
| I — Interface Segregation | Las interfaces deben ser pequeñas y enfocadas. | Separar una futura interfaz `IIndexer` de `IRetriever`. |
| D — Dependency Inversion | La lógica principal no debe depender directamente de una tecnología concreta. | Los casos de uso deberían depender de abstracciones, no directamente de ChromaDB. |

## Conclusión

El MVP propuesto cumple con el enfoque académico solicitado porque integra búsqueda, lógica, recuperación de conocimiento, aprendizaje automático y buenas prácticas de ingeniería. La versión entregada es funcional a nivel local, pero está diseñada para crecer hacia un sistema RAG más avanzado con embeddings semánticos, ChromaDB, LLM generativo, interfaz web y citación automática.
