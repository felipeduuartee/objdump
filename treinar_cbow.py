import argparse
import os
from gensim.models import Word2Vec

def carregar_corpus(path):
    with open(path, "r") as f:
        return [linha.strip().split() for linha in f if linha.strip()]

def main():
    parser = argparse.ArgumentParser(description="Treinar modelo CBOW com corpus de n-gramas")
    parser.add_argument("--distro", required=True, help="Nome da distro usada (ex: ubuntu-22.04)")
    parser.add_argument("--modo", required=True, choices=["text", "full"], help="Tipo de disassembly usado")
    parser.add_argument("--n", type=int, default=2, help="Tamanho do n-grama (default: 2)")

    args = parser.parse_args()
    
    corpus_path = f"corpus/corpus_{args.distro}_{args.modo}_n{args.n}.txt"
    os.makedirs("models", exist_ok=True)
    modelo_path = f"models/modelo_cbow_{args.distro}_{args.modo}_n{args.n}.model"

    print(f" Carregando corpus: {corpus_path}")
    corpus = carregar_corpus(corpus_path)

    print("️ Treinando modelo CBOW...")
    model = Word2Vec(
        sentences=corpus,
        vector_size=100,
        window=2,
        sg=0,  # CBOW
        min_count=1
    )

    model.save(modelo_path)
    print(f"✅ Modelo CBOW salvo como: {modelo_path}")

if __name__ == "__main__":
    main()
