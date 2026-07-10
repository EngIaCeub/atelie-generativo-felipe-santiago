# Registro de decisões

## ADR-001 — Arquitetura nativa para Codex
**Status:** aceita.  
**Decisão:** usar `AGENTS.md` como mapa curto, `.agents/skills/` para workflows, `.codex/agents/` para
auditorias e `docs/` como sistema de registro.  
**Motivo:** manter instruções permanentes pequenas e carregar detalhes apenas quando necessários.

## ADR-002 — Nome correto de notebooks
**Status:** aceita.  
**Decisão:** migrar `noteboks/` para `notebooks/`, preservando conteúdo e histórico sempre que possível.  
**Motivo:** o nome correto é exigido pela estrutura acadêmica e evita caminhos divergentes.

## ADR-003 — Segredos fora do repositório
**Status:** aceita.  
**Decisão:** usar `HF_TOKEN` em memória/ambiente local e Secret no Space.  
**Motivo:** segurança, barema e prevenção de vazamento.

## ADR-004 — Aplicação modular por provedores
**Status:** aceita.  
**Decisão:** separar expansor, imagem e TTS; decidir backend após benchmark no ambiente gratuito.  
**Motivo:** evitar acoplamento a uma API ou hardware que possa não suportar o LoRA.

## ADR-005 — Execução local do bootstrap em ambiente Codex
**Status:** aceita.  
**Decisão:** executar validações locais com o Python empacotado do Codex quando `python` do PATH não estiver
disponível e a `.venv` local estiver quebrada.  
**Motivo:** permitir auditoria e bootstrap sem instalar dependências globais nem tocar em segredos.

## Pendências de decisão
- Estilo e token textual.
- Namespace/IDs do Hugging Face.
- TTS final com português adequado e custo zero.
- Estratégia de inferência de imagem no Space.
- Licença do código.
