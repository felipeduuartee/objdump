# CBOW + Objdump Disassembly


#### QUALQUER DÚVIDA QUE TIVER, CONSULTE O ARQUIVO `explicacao.txt` TEM TUDO LÁ

Este projeto utiliza Word2Vec (CBOW) para gerar embeddings de instruções assembly extraídas de binários ELF usando `objdump`.

---

## 📦 Etapas para rodar

### 1. Extrair disassembly dos binários ELF
```bash
chmod +x extrair_disassembly.sh
./extrair_disassembly.sh
```

- Detecta automaticamente a distro
- Cria dumps em: `dumps/<distro>/text/` (-d) e `dumps/<distro>/full/` (-D)
- Lista de binários salva em: `listas/lista_elfs_<distro>.txt`

---

### 2. Gerar corpus de n-gramas
```bash
python3 preprocessar_ngrama.py --distro <distro> --modo <text|full> --n <tamanho>
```
- Ex: `--distro ubuntu-20.04` `--modo text` `--n 2` para bigramas
- Gera `corpus/corpus_<distro>_<modo>_n<n>.txt`

---

### 3. Treinar modelo CBOW
```bash
python3 treinar_cbow.py --distro <distro> --modo <text|full> --n <tamanho>
```
- Salva modelo em: `models/modelo_cbow_<distro>_<modo>_n<n>.model`

---

### 4. Visualizar embeddings
```bash
python3 view_embeddings.py --distro <distro> --modo <text|full> --n <tamanho> --metodo <tsne|pca>
```

---

### 5. Clusterizar (com opção de gráfico)
```bash
python3 cluster.py --distro <distro> --modo <text|full> --n <tamanho> --clusters <num> --plot
```

---

### 6. Consultar instruções similares
```bash
python3 similares.py --distro <distro> --modo <text|full> --n <tamanho> --instrucao <opcode>
```

---

## ✅ Exemplo completo
```bash
./extrair_disassembly.sh
python3 preprocessar_ngrama.py --distro ubuntu-20.04 --modo text --n 2
python3 treinar_cbow.py --distro ubuntu-20.04 --modo text --n 2
python3 view_embeddings.py --distro ubuntu-20.04 --modo text --n 2
python3 cluster.py --distro ubuntu-20.04 --modo text --n 2 --plot
python3 similares.py --distro ubuntu-20.04 --modo text --n 2 --instrucao mov
```
