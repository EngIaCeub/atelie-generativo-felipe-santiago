# Conformidade de entrega: Colab, Hub e GitHub

## Objetivo e resultado observável

Adequar os notebooks de treinamento e avaliação para execução de cima para baixo em um Colab limpo, publicar e verificar os pesos LoRA com model card no Hugging Face Hub, e consolidar a entrega acadêmica no repositório GitHub como projeto individual.

## Contexto atual

- Dataset, dois treinos locais, avaliação, Space e relatório estão validados localmente.
- `notebooks/02_treino_lora.ipynb` e `notebooks/03_avaliacao.ipynb` contêm caminhos e verificações específicos do Windows.
- `config/project.json` declara `RalphError/flpxilobr-lora`, mas `resultados/treino/experimentos.csv` ainda não registra URL de publicação.
- A API pública do Space confirmou `RUNNING`; a consulta pública do modelo retornou `401` em 2026-07-11.
- A árvore Git contém as evidências finais ainda sem commit.

## Escopo

Incluído: notebooks 02 e 03, manifestos de treino, documentação de projeto individual, publicação do modelo e commit/push das alterações acadêmicas.

Fora de escopo: repetir o treinamento concluído, alterar o dataset, expor tokens, ou modificar artefatos remotos sem autorização explícita.

## Contratos e restrições

- Executar em Colab limpo sem token em células ou outputs.
- Preservar seed, configurações e resultados existentes; não fabricar novas métricas.
- Publicar apenas pesos selecionados, model card e arquivos necessários para carregamento.
- Não enviar checkpoints pesados ou dados pessoais ao GitHub.
- Projeto individual: documentar a responsabilidade de Felipe Santiago sem atribuir ou apagar autoria histórica de terceiros.

## Plano de execução

- [x] Marco 1 - Adaptar e validar notebooks 02 e 03 em modo Colab.
- [x] Marco 2 - Preparar, publicar e confirmar o repositório LoRA no Hub.
- [x] Marco 3 - Atualizar registros e documentação do projeto individual.
- [x] Marco 4 - Revisar o escopo, commit/push e validar a entrega final.

## Evidências esperadas

- Notebooks com seleção explícita de ambiente e caminhos Colab.
- URL pública do modelo, pesos `.safetensors` e `README.md`/model card no Hub.
- `resultados/treino/experimentos.csv` com URL real da configuração selecionada.
- Registro de decisão individual, commit e remoto GitHub atualizado.

## Testes e comandos

- `python scripts/validate_project.py --stage training`
- `python scripts/validate_project.py --stage evaluation`
- `python scripts/validate_project.py --stage final`
- `python scripts/check_secrets.py`
- `python -m pytest -q`
- `python -m ruff check scripts app tests`

## Decisões

- 2026-07-11: manter os resultados locais concluídos; a adaptação Colab é de portabilidade e reprodutibilidade, não uma nova alegação de treino.
- 2026-07-11: publicar somente a LoRA selecionada (`config_b`) com seu model card e sem checkpoints intermediários.

## Progresso e descobertas

- 2026-07-11: plano criado após auditoria de aderência à Sistematização.
- 2026-07-11: `RalphError/flpxilobr-lora` confirmado público com `README.md` e `pytorch_lora_weights.safetensors`.
- 2026-07-11: alterações consolidadas na branch `agent/finalizar-entrega-academica`, commit `388a2ec`, com checkpoints locais excluídos.

## Resultado final

Concluído: notebooks portáveis para Colab, LoRA pública, documentação individual e evidências enviadas ao GitHub. As validações finais passaram antes do commit: `validate_project.py --stage final`, `check_secrets.py`, `pytest` (22 testes) e `ruff`.
