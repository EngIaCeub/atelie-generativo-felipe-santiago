# Space publicado - 2026-07-11

## Evidencia remota confirmada

- Repositorio: `RalphError/atelie-xilogravura-cerrado`.
- Pagina publica: `https://huggingface.co/spaces/RalphError/atelie-xilogravura-cerrado`.
- Dominio do app: `https://ralpherror-atelie-xilogravura-cerrado.hf.space`.
- Commit que iniciou com sucesso: `c6cf72aa1ea181bbb37883acb8e72635747def87`.
- Estado consultado pela API do Hub: `RUNNING`, sem mensagem de erro.

## Correcoes aplicadas durante a publicacao

1. Fixar Python 3.11 no metadata do Space para evitar a ausencia de `audioop` em Python 3.13.
2. Fixar `huggingface_hub>=0.25,<1.0` para compatibilidade com Gradio 5.0.0.
3. Chamar `demo.launch()` no entrypoint raiz do Space.

## Pendente para teste ponta a ponta

O responsavel deve configurar `HF_TOKEN` como Secret no Space. O valor nao foi lido, exibido, gravado ou enviado pelo agente. Depois da configuracao, o fluxo deve ser testado em janela anonima com tres temas e as latencias/falhas devem ser registradas.
