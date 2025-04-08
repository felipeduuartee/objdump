import argparse
from gensim.models import Word2Vec

def main():
    parser = argparse.ArgumentParser(description="Consulta de instruções similares no modelo CBOW")
    parser.add_argument("--distro", required=True)
    parser.add_argument("--modo", required=True, choices=["text", "full"])
    parser.add_argument("--n", type=int, default=2)
    parser.add_argument("--instrucao", required=True, help="Instrução a consultar (ex: mov)")

    args = parser.parse_args()
    modelo_path = f"models/modelo_cbow_{args.distro}_{args.modo}_n{args.n}.model"

    print(f" Carregando modelo: {modelo_path}")
    modelo = Word2Vec.load(modelo_path)

    print(f" Instruções similares a '{args.instrucao}':\n")
    try:
        similares = modelo.wv.most_similar(args.instrucao)
        for termo, score in similares:
            print(f"{termo}\t{score:.4f}")
    except KeyError:
        print(" Instrução não encontrada no vocabulário.")

if __name__ == "__main__":
    main()
