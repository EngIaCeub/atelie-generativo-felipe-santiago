# Regras locais — aplicação

- Contrato da função principal: entrada `tema: str`; saídas `prompt: str`, `imagem`, `audio`.
- Separar orquestração dos provedores em `app/services/`.
- Nunca hardcodar token. Ler `HF_TOKEN` do ambiente e falhar com mensagem segura se ausente.
- Não registrar cabeçalhos, secrets ou conteúdo de ambiente em logs.
- Validar tema vazio/tamanho, tratar timeout/falha de cada modalidade e manter interface responsiva.
- O modo de desenvolvimento/mock não pode ser usado como evidência de publicação final.
- Antes de publicar, testar que o backend de imagem realmente aplica o LoRA escolhido.
- Manter `app/requirements.txt`, README do Space e model card coerentes.
