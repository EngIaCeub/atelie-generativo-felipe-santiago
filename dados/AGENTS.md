# Regras locais — dados

- Trate `dados/fontes.csv` como registro auditável; nunca invente metadados.
- Formato obrigatório: `arquivo,url,autor,licenca,data_coleta,fonte,observacoes`.
- Nomes de imagem estáveis e únicos; não substituir arquivo mantendo o mesmo nome sem atualizar hash/evidência.
- `dados/legendas.txt`: uma linha por imagem, separada por TAB: `arquivo`, `caption`, `status_revisao`.
- Status permitidos: `rascunho`, `revisada`, `rejeitada`. Apenas `revisada` entra no treino.
- BLIP produz rascunho; o agente nunca promove para `revisada` sem confirmação humana.
- Toda caption revisada começa com o token exato de `config/project.json`.
- Antes de concluir, execute a validação de dataset e reporte arquivos sem correspondência.
