# Regras locais — notebooks

- Manter os nomes `01_dataset.ipynb`, `02_treino_lora.ipynb` e `03_avaliacao.ipynb`.
- Notebooks devem ser executáveis de cima para baixo em Colab limpo e conter títulos/explicações.
- Primeira seção: ambiente, instalação silenciosa sem esconder falha, versões e verificação de GPU.
- Nunca escrever token em célula. Usar `login()` interativo ou `HF_TOKEN` sem imprimir o valor.
- Caminhos e IDs vêm de `config/project.json`; evitar placeholders espalhados.
- Salvar artefatos pequenos em `resultados/`; checkpoints/pesos pesados no Drive/Hub.
- Fixar seeds e registrar versões/commit do código de treino.
- Notebook 02: duas configurações, checkpoints, resume e manifesto de experimentos.
- Notebook 03: mesma seed base × LoRA, CLIPScore, memorização e análise humana real.
- Não salvar outputs que contenham token, caminho pessoal ou dado privado.
