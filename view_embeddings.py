import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import numpy as np
import argparse

def reduzir_dimensao(modelo, metodo="tsne", n=100):
    palavras = modelo.wv.index_to_key[:n]
    vetores = np.array([modelo.wv[w] for w in palavras])

    if metodo == "tsne":
        redutor = TSNE(n_components=2, random_state=42, perplexity=20, init="pca")
    else:
        redutor = PCA(n_components=2)

    vetores_2d = redutor.fit_transform(vetores)
    return palavras, vetores_2d

def plotar(vetores_2d, palavras, titulo):
    plt.figure(figsize=(16, 12))
    for i, palavra in enumerate(palavras):
        x, y = vetores_2d[i]
        plt.scatter(x, y)
        plt.annotate(palavra, (x, y), fontsize=9)
    plt.title(titulo)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Visualizar embeddings CBOW em 2D")
    parser.add_argument("--distro", required=True)
    parser.add_argument("--modo", required=True, choices=["text", "full"])
    parser.add_argument("--n", type=int, default=2, help="Tamanho do n-grama usado no modelo")
    parser.add_argument("--metodo", default="tsne", choices=["tsne", "pca"])

    args = parser.parse_args()
    modelo_path = f"models/modelo_cbow_{args.distro}_{args.modo}_n{args.n}.model"
    titulo = f"CBOW - {args.distro} ({args.modo}, n={args.n}) - {args.metodo.upper()}"

    print(f" Carregando modelo: {modelo_path}")
    modelo = Word2Vec.load(modelo_path)

    print(f" Reduzindo com {args.metodo.upper()}...")
    palavras, vetores_2d = reduzir_dimensao(modelo, metodo=args.metodo, n=100)

    print(" Gerando gráfico...")
    plotar(vetores_2d, palavras, titulo)

if __name__ == "__main__":
    main()
