#!/bin/bash

# ─── [1] Detectar a distro e versão ─────────────────────────────────────
DISTRO=$(grep '^ID=' /etc/os-release | cut -d= -f2 | tr -d '"')
VERSAO=$(grep '^VERSION_ID=' /etc/os-release | cut -d= -f2 | tr -d '"')
TAG="${DISTRO}-${VERSAO}"

echo " Distro detectada: $TAG"

# ─── [2] Criar diretórios de saída ─────────────────────────────────────
DUMP_BASE="dumps/${TAG}"
TEXT_DIR="${DUMP_BASE}/text"
FULL_DIR="${DUMP_BASE}/full"
mkdir -p "$TEXT_DIR" "$FULL_DIR"

echo " Diretórios criados:"
echo "  ├── $TEXT_DIR"
echo "  └── $FULL_DIR"

# ─── [3] Gerar lista de ELFs válidos ───────────────────────────────────
LISTA_ELF="listas/lista_elfs_${TAG}.txt"
echo " Gerando lista de binários ELF em /usr/sbin..."
find /usr/sbin -type f -executable -exec file {} \; | grep ELF | cut -d: -f1 > "$LISTA_ELF"

TOTAL=$(wc -l < "$LISTA_ELF")
echo " Total de ELFs encontrados: $TOTAL"
echo " Lista salva em: $LISTA_ELF"

# ─── [4] Rodar objdump para cada ELF ───────────────────────────────────
echo "️ Gerando disassemblies com objdump..."

while read bin; do
    nome=$(basename "$bin")

    echo "  ➤ $nome"

    # Apenas a seção .text
    objdump -d -Mintel "$bin" > "${TEXT_DIR}/${nome}.text.asm" 2>/dev/null

    # Disassembly completo
    objdump -D -Mintel "$bin" > "${FULL_DIR}/${nome}.full.asm" 2>/dev/null

done < "$LISTA_ELF"

echo "✅ Disassembly finalizado com sucesso!"
echo " Arquivos salvos em: $TEXT_DIR e $FULL_DIR"
