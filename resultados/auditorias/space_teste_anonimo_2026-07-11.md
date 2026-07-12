# Teste anonimo do Space - 2026-07-11

## Ambiente

- URL: `https://ralpherror-atelie-xilogravura-cerrado.hf.space`.
- Navegacao realizada sem sessao autenticada.
- Secret `HF_TOKEN` foi configurado pelo responsavel humano na interface do Space.
- Runtime consultado pela API: `RUNNING` antes dos testes.

## Resultados observados

| Tema | Prompt | Imagem | Audio | Status | Latencia observada |
|---|---|---|---|---|---:|
| lobo-guara entre capim dourado no Cerrado | Sim | Sim | Sim, 15 s | `Concluido.` | nao registrada com precisao durante a carga inicial |
| seriema ao amanhecer no Cerrado | Sim | Sim | Sim, 13 s | `Concluido.` | 257.671 s |

O navegador bloqueou a continuacao do terceiro teste nesta sessao por politica de seguranca. Nenhum resultado foi atribuido ao terceiro tema.

## Correcoes verificadas durante a publicacao

- Python 3.11 para compatibilidade de audio.
- Gradio 6.20.0 e `huggingface_hub` 1.x para corrigir a API publica.
- `peft` incluido para carregar os pesos LoRA.
- Inferencia em CPU reduzida para 12 passos; GPU local preserva 30 passos.

## Limite

O Space funciona em CPU Basic, mas a latencia observada e alta para demonstracao ao vivo. A evidencia local em `resultados/app_smoke_v3/` contem tres fluxos completos com GPU local.
