# Contribuição e processo

## Fluxo
1. Abrir issue vinculada ao marco e critério do barema.
2. Criar branch curta: `feat/dataset-caption`, `exp/lora-rank-4`, `docs/relatorio-etica`.
3. Fazer commits pequenos, verificáveis e distribuídos no tempo.
4. Rodar validações locais e anexar evidências na issue/PR.
5. Revisar, mesclar e atualizar `PROJECT_STATE.md`.

## Commits
Use mensagens objetivas, por exemplo:
- `chore: cria estrutura inicial para Codex`
- `data: adiciona proveniência de 8 imagens CC-BY`
- `exp: registra treino LoRA rank 4`
- `eval: calcula CLIPScore base e LoRA`
- `docs: adiciona reflexão sobre direitos autorais`

Não use um único commit para todo o projeto. Não reescreva histórico público sem necessidade.

## Evidências
Issues e PRs devem apontar para arquivos em `resultados/`, notebook/commit executado ou URL confirmada.
Nunca usar screenshot como única evidência de dado que possa ser exportado em CSV/JSON.
