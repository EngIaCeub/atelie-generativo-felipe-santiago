# Criacao do Space recusada - 2026-07-11

## Tentativa autorizada

- Conta autenticada confirmada: `RalphError`.
- Repositorio solicitado: `RalphError/atelie-xilogravura-cerrado`.
- Tipo solicitado: Space publico com SDK Gradio.
- Bundle local validado: `space/`.

## Resultado observado

A API do Hugging Face respondeu `402 Payment Required` em `POST /api/repos/create`. A mensagem do Hub informa que Spaces Gradio/Docker com `cpu-basic` exigem assinatura PRO para a conta atual; somente Static Spaces sao gratuitos.

Nenhum Space foi criado e nenhum arquivo foi enviado.

## Proxima decisao humana

Ativar Hugging Face PRO e repetir a criacao do Space Gradio, ou autorizar formalmente outra estrategia de hospedagem. Um Static Space gratuito nao atende ao contrato atual de executar Gradio, Stable Diffusion com LoRA e TTS no servidor.
