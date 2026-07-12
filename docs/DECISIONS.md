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

## ADR-012 - Backends locais reais para o app multimodal
**Status:** aceita; smoke test local aprovado; publicacao remota pendente.
**Decisao:** usar Qwen 2.5 0.5B para expansao de prompt, Stable Diffusion v1.5 com pesos `config_b` carregados explicitamente e MMS-TTS em portugues.
**Motivo:** preserva o contrato LLM -> LoRA -> TTS sem assumir que uma API de inferencia remota aceita ou aplica um adaptador LoRA. Os modelos carregam apenas na primeira solicitacao e o token, quando necessario, continua restrito ao ambiente. A resposta do LLM passa por validacao estrutural com fallback para manter tema, portugues e o token de estilo.

## ADR-013 - Entrega academica final baseada em evidencias
**Status:** aceita.
**Decisao:** consolidar a entrega em `relatorio/relatorio_final.md`, exportar `relatorio/relatorio_final.pdf`, atualizar README, model card local, declaracao de uso de IA e auditoria final.
**Motivo:** o barema exige relatorio final, reflexao etica, links/evidencias verificaveis e demonstracao preparada. O PDF foi gerado localmente porque o ambiente nao tinha `reportlab`, `pandoc` ou `pdftoppm`; a revisao visual foi feita por previews PNG gerados com Pillow.

## ADR-014 - Codigo sem licenca aberta definida
**Status:** aceita.
**Decisao:** nao atribuir uma licenca aberta ao codigo nesta entrega; o README registra que reutilizacao externa deve pedir autorizacao ao autor ate decisao posterior.
**Motivo:** nao havia decisao humana explicita sobre MIT, Apache, GPL ou outra licenca. As licencas das imagens continuam separadas e registradas em `dados/fontes.csv`.

## Atualizacao das pendencias - 2026-07-11
As pendencias antigas de TTS final e estrategia de inferencia no Space foram resolvidas por ADR-012 e pela publicacao registrada em `resultados/auditorias/space_teste_anonimo_2026-07-11.md`. A licenca do codigo permanece sem licenca aberta definida, conforme ADR-014.

## ADR-015 - Confirmacao de entrega individual e rastreabilidade historica
**Status:** aceita.
**Decisao:** a entrega academica atual e individual, sob responsabilidade de Felipe Santiago. Os commits historicos existentes com outros identificadores Git permanecem preservados, sem reatribuicao ou reescrita de historico.
**Motivo:** `config/project.json` registra somente Felipe Santiago como membro e responsavel por todas as frentes. A consolidacao final sera commitada com a identidade Git configurada pelo responsavel, preservando a rastreabilidade factual do repositorio.
