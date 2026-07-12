# Regras locais — dados

- Trate `dados/fontes.csv` como registro auditável; nunca invente metadados.
- Campos mínimos de compatibilidade: `arquivo,url,autor,licenca,data_coleta,fonte,observacoes`.
- Para arquivos finais derivados ou sintéticos, também registre: `arquivo_final`, `origem_tipo`,
  `url_origem`, `autor_original`, `licenca_original`, `transformacao_ia`, `ferramenta_modelo`,
  `prompt_transformacao`, `data_transformacao`, `responsavel_transformacao`, `licenca_derivada` e
  `status_curadoria`. Não descreva uma derivação como simples imagem coletada.
- Nomes de imagem estáveis e únicos; não substituir arquivo mantendo o mesmo nome sem atualizar hash/evidência.
- `dados/legendas.txt`: uma linha por imagem, separada por TAB: `arquivo`, `caption`, `status_revisao`.
- Status permitidos: `rascunho`, `revisada`, `rejeitada`. Apenas `revisada` entra no treino.
- BLIP produz rascunho; o agente nunca promove para `revisada` sem confirmação humana.
- Toda caption revisada começa com o token exato de `config/project.json`.
- Antes de concluir, execute a validação de dataset e reporte arquivos sem correspondência.
