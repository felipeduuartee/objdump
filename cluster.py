import argparse
import numpy as np
from sklearn.cluster import KMeans
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def reduzir_dimensao(vetores, metodo="tsne"):
    if metodo == "tsne":
        redutor = TSNE(n_components=2, random_state=42, perplexity=20, init="pca")
    else:
        redutor = PCA(n_components=2)
    return redutor.fit_transform(vetores)

def plotar_clusters(vetores_2d, palavras, labels, clusters, titulo):
    plt.figure(figsize=(16, 12))
    for i in range(clusters):
        cluster_pts = vetores_2d[labels == i]
        plt.scatter(cluster_pts[:, 0], cluster_pts[:, 1], label=f"Cluster {i}", s=40)

    for i, palavra in enumerate(palavras):
        x, y = vetores_2d[i]
        plt.annotate(palavra, (x, y), fontsize=8)

    plt.title(titulo)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Clusterização e visualização dos embeddings CBOW")
    parser.add_argument("--distro", required=True)
    parser.add_argument("--modo", required=True, choices=["text", "full"])
    parser.add_argument("--n", type=int, default=2)
    parser.add_argument("--clusters", type=int, default=10)
    parser.add_argument("--plot", action="store_true", help="Exibe gráfico da clusterização")
    parser.add_argument("--metodo", default="tsne", choices=["tsne", "pca"], help="Método de redução de dimensionalidade")

    args = parser.parse_args()
    modelo_path = f"models/modelo_cbow_{args.distro}_{args.modo}_n{args.n}.model"

    print(f" Carregando modelo: {modelo_path}")
    modelo = Word2Vec.load(modelo_path)

    palavras = modelo.wv.index_to_key
    vetores = np.array([modelo.wv[w] for w in palavras])

    print(f" Aplicando K-Means com {args.clusters} clusters...")
    kmeans = KMeans(n_clusters=args.clusters, random_state=42, n_init="auto")
    labels = kmeans.fit_predict(vetores)

    print("\n Instruções agrupadas por cluster:\n")
    for palavra, label in sorted(zip(palavras, labels), key=lambda x: x[1]):
        print(f"{palavra}\t→ Cluster {label}")

    if args.plot:
        print(f"\n Reduzindo vetores para 2D com {args.metodo.upper()}...")
        vetores_2d = reduzir_dimensao(vetores, metodo=args.metodo)
        titulo = f"CBOW Clusterização - {args.distro} ({args.modo}, n={args.n})"
        print(" Plotando clusters...")
        plotar_clusters(vetores_2d, palavras, np.array(labels), args.clusters, titulo)

if __name__ == "__main__":
    main()
