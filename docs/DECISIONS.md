# Registro de decisões

## ADR-001 - Arquitetura nativa para Codex
**Status:** aceita.  
**Decisão:** usar `AGENTS.md` como mapa curto, `.agents/skills/` para workflows, `.codex/agents/` para
auditorias e `docs/` como sistema de registro.  
**Motivo:** manter instruções permanentes pequenas e carregar detalhes apenas quando necessários.

## ADR-002 - Nome correto de notebooks
**Status:** aceita.  
**Decisão:** migrar `noteboks/` para `notebooks/`, preservando conteúdo e histórico sempre que possível.  
**Motivo:** o nome correto é exigido pela estrutura acadêmica e evita caminhos divergentes.

## ADR-003 - Segredos fora do repositório
**Status:** aceita.  
**Decisão:** usar `HF_TOKEN` em memória/ambiente local e Secret no Space.  
**Motivo:** segurança, barema e prevenção de vazamento.

## ADR-004 - Aplicação modular por provedores
**Status:** aceita.  
**Decisão:** separar expansor, imagem e TTS; decidir backend após benchmark no ambiente gratuito.  
**Motivo:** evitar acoplamento a uma API ou hardware que possa não suportar o LoRA.

## ADR-005 - Execução local do bootstrap em ambiente Codex
**Status:** aceita.  
**Decisão:** executar validações locais com o Python empacotado do Codex quando `python` do PATH não estiver
disponível e a `.venv` local estiver quebrada.  
**Motivo:** permitir auditoria e bootstrap sem instalar dependências globais nem tocar em segredos.

## ADR-006 - Estilo aprovado do projeto
**Status:** aceita.  
**Decisão:** usar o estilo `Xilogravura Digital do Cerrado` com trigger token exclusivo `flpxilobr`.  
**Motivo:** decisão confirmada pelo responsável humano Felipe Santiago em 2026-07-10 como aprovada pelo
professor. Não foram informados nome do professor, canal de aprovação, URL ou comprovante local.

## ADR-007 - Equipe individual e papéis obrigatórios
**Status:** aceita.  
**Decisão:** registrar a equipe como individual, composta por Felipe Santiago, e atribuir a ele os papéis
`dados_e_licencas`, `treinamento_lora`, `avaliacao`, `aplicacao_e_publicacao` e `documentacao`.  
**Motivo:** o responsável humano confirmou a composição atual da equipe em 2026-07-10.

## ADR-008 - IDs planejados no Hugging Face
**Status:** aceita.  
**Decisão:** registrar `RalphError` como namespace, `RalphError/flpxilobr-lora` como repositório LoRA
planejado e `RalphError/atelie-xilogravura-cerrado` como Space planejado.  
**Motivo:** valores confirmados pelo responsável humano. Nenhum token ou segredo foi lido, exibido ou
versionado.

## ADR-009 - Curadoria inicial via Wikimedia Commons
**Status:** aceita.  
**Decisão:** selecionar 24 imagens do Wikimedia Commons, validar autor/licença/dimensões pela API pública e
gerar derivações locais em preto e marfim com hachuras determinísticas.  
**Motivo:** as páginas de arquivo fornecem URL verificável, autoria, licença e dimensões; o processamento
local aproxima as fontes aprovadas do estilo sem imitar artista vivo.

## ADR-010 - Transparencia sobre arquivos finais derivados
**Status:** aceita.
**Decisao:** registrar os PNGs finais como derivacoes deterministicas de fontes licenciadas, com arquivo
final, origem, licenca original/derivada, ferramenta, ausencia de IA generativa e evidencia local por
item em `dados/fontes.csv` e na auditoria de origem final.
**Motivo:** as fontes originais nao foram coletadas ja no estilo escolhido. O processamento `woodcut-v2`
usa Pillow, sem modelo ou prompt generativo; trata-lo como simples coleta no estilo, ou como sintese por
IA, seria impreciso. A aprovacao de curadoria e captions continua exclusivamente humana.

## ADR-011 - Fechamento local do dataset apos revisao humana
**Status:** aceita.
**Decisao:** exportar `dados/metadata.jsonl` apenas depois da confirmacao humana de Felipe Santiago sobre a
revisao das captions e da auditoria final aprovar cada PNG final, fonte, licenca, triagem, hash e caption.
**Motivo:** manter o contrato dataset -> treino verificavel. BLIP nao foi executado no runtime local por
ausencia de `torch` e `transformers`; as captions derivam de inspecao visual/metadados e foram revisadas
por humano antes da exportacao.

## Pendências de decisão
- TTS final com português adequado e custo zero.
- Estratégia de inferência de imagem no Space.
- Licença do código.
