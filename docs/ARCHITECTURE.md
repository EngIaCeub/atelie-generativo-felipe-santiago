# Arquitetura do projeto

## Camadas de controle do agente
```text
AGENTS.md (mapa curto e regras permanentes)
    ├── PROJECT_STATE.md + config/project.json
    ├── docs/ (fonte de verdade e runbooks)
    ├── .agents/skills/ (workflows sob demanda)
    ├── .codex/agents/ (auditores especializados)
    └── scripts/ (regras executáveis e validação)
```

## Pipeline acadêmico
```text
Tema curto
  → expansor de prompt (LLM)
  → prompt com token do estilo
  → modelo base + pesos LoRA
  → imagem
  → TTS da descrição
  → Gradio: prompt + imagem + áudio
```

## Contratos entre etapas
1. **Proposta → dataset**: estilo, token e licenças planejadas aprovados.
2. **Dataset → treino**: 20–40 imagens, proveniência completa, captions revisadas e metadata exportada.
3. **Treino → avaliação**: duas execuções registradas, checkpoints/pesos e IDs no Hub.
4. **Avaliação → publicação**: configuração escolhida e limitações documentadas.
5. **Publicação → relatório**: Space testado anonimamente, model card e evidências congeladas.

## Organização de dados
- `dados/imagens/`: imagens finais com nomes estáveis `img_001.ext` etc.
- `dados/fontes.csv`: proveniência e licença por arquivo.
- `dados/legendas.txt`: `arquivo<TAB>caption<TAB>status_revisao`.
- `dados/metadata.jsonl`: artefato derivado para o script de treino; não é fonte manual.
- `resultados/`: evidências geradas, pequenas e versionáveis.
- Pesos/checkpoints pesados ficam no Drive/Hub e são referenciados por URL/ID.

## Aplicação
O app deve separar orquestração de provedores:
- `services/prompt_expander.py`
- `services/image_generator.py`
- `services/speech_synthesizer.py`

A escolha local/remota é configuração, não lógica espalhada. O backend final precisa ser comprovadamente
compatível com o Space gratuito. Nunca presumir que um repositório contendo apenas LoRA será servido por
uma API; testar e registrar a estratégia escolhida (adaptador carregado localmente, modelo mesclado ou
serviço remoto compatível).

## Evidência e reprodutibilidade
Cada experimento registra data, commit, versões, seed, dataset hash, parâmetros, saída e URL do Hub. O
relatório referencia somente arquivos existentes e IDs remotos confirmados.
