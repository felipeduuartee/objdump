import os
import re
import argparse
from tqdm import tqdm

def extrair_mnemonicos(path):
    instrucoes = []
    with open(path, "r") as f:
        for linha in f:
            match = re.match(r'^\s*[0-9a-fA-F]+:\s+(?:[0-9a-fA-F]{2}\s+)+(\S+)', linha)
            if match:
                instrucoes.append(match.group(1))
    return instrucoes

def gerar_ngrama(instrs, n=2):
    return [instrs[i:i+n] for i in range(len(instrs) - n + 1)]

def main():
    parser = argparse.ArgumentParser(description="Extrair n-gramas de instruções de disassembly")
    parser.add_argument("--distro", required=True, help="Nome da distro detectada (ex: ubuntu-22.04)")
    parser.add_argument("--modo", required=True, choices=["text", "full"], help="Tipo de disassembly: text ou full")
    parser.add_argument("--n", type=int, default=2, help="Tamanho do n-grama (default: 2)")

    args = parser.parse_args()
    DUMP_DIR = os.path.join("dumps", args.distro, args.modo)
    os.makedirs("corpus", exist_ok=True)
    BIGRAMA_OUT = f"corpus/corpus_{args.distro}_{args.modo}_n{args.n}.txt"

    arquivos = [f for f in os.listdir(DUMP_DIR) if f.endswith(".asm")]
    ngramas_total = []

    print(f" Lendo arquivos de: {DUMP_DIR}")
    for arq in tqdm(arquivos, desc="Processando dumps"):
        caminho = os.path.join(DUMP_DIR, arq)
        instrs = extrair_mnemonicos(caminho)
        if len(instrs) >= args.n:
            ngramas = gerar_ngrama(instrs, n=args.n)
            ngramas_total.extend(ngramas)

    with open(BIGRAMA_OUT, "w") as out:
        for ngrama in ngramas_total:
            out.write(" ".join(ngrama) + "\n")

    print(f"\n✅ Corpus de n-gramas salvo em: {BIGRAMA_OUT}")

if __name__ == "__main__":
    main()
