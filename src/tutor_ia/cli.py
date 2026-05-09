import argparse
from pathlib import Path

from .retriever import RagRetriever


def main() -> None:
    parser = argparse.ArgumentParser(description="Consulta interactiva del Tutor Inteligente de IA.")
    parser.add_argument("--storage", default="storage", help="Carpeta donde está guardado el índice")
    args = parser.parse_args()

    retriever = RagRetriever(Path(args.storage))
    print("Tutor Inteligente de IA listo. Escriba 'salir' para terminar.\n")
    while True:
        question = input("Pregunta: ").strip()
        if question.lower() in {"salir", "exit", "quit"}:
            break
        try:
            response = retriever.answer(question)
            print("\n" + response.answer)
            if response.sources:
                print("\nFuentes recuperadas:")
                for item in response.sources:
                    print(f"- {item.chunk.source} | score={item.score:.3f}")
            print()
        except Exception as exc:
            print(f"Error: {exc}\n")


if __name__ == "__main__":
    main()
