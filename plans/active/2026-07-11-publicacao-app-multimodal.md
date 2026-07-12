# Publicacao do app multimodal

## Objetivo e resultado observavel

Substituir os provedores pendentes do app Gradio por implementacoes reais de expansao de prompt, geracao Stable Diffusion com LoRA e TTS em portugues. O resultado local deve expor texto, imagem e audio; a publicacao no Space fica pendente de autorizacao humana e teste remoto.

## Contexto atual

Bootstrap, dataset, treino e avaliacao passam em `scripts/project_status.py`. A configuracao escolhida e `config_b`, com pesos locais em `resultados/treino/local/config_b/pytorch_lora_weights.safetensors`. Os provedores do app foram substituidos por implementacoes reais; falta testar a inferencia completa.

## Escopo

Incluido: provedores locais/reais, configuracao, testes unitarios, documentacao local e validacoes. Fora de escopo: upload de pesos, criacao/publicacao remota do Space e afirmacao de URL publica sem autorizacao e evidencia.

## Contratos e restricoes

- Entrada curta; saidas: prompt, imagem e audio.
- Token apenas por ambiente, nunca em arquivo, saida ou log.
- A imagem deve carregar explicitamente `pytorch_lora_weights.safetensors` sobre o modelo base.
- Modelos carregam sob demanda; erros de download, hardware ou inferencia devem ser seguros ao usuario.
- O modo de desenvolvimento nao conta como evidencia de publicacao.

## Plano de execucao

- [x] Marco 1 - Auditar bloqueios e confirmar pesos locais.
- [x] Marco 2 - Implementar provedores reais e interface segura.
- [x] Marco 3 - Criar testes dos contratos e validar app localmente.
- [x] Marco 4 - Atualizar estado, decisao e evidencias de preparo.
- [x] Marco 5 - Space criado, Secret configurado e duas execucoes anonimas completas registradas.

## Evidencias esperadas

- Implementacoes em `app/services/` e testes em `app/tests/`.
- Configuracao de backends em `config/project.json`.
- Registro de preparo em `resultados/auditorias/`.
- Saidas de pytest, ruff, secret scan e `validate_project.py --stage publication`.

## Testes e comandos

`python -m pytest -q`, `python -m ruff check scripts app tests`, `python scripts/check_secrets.py`, `python scripts/validate_project.py --stage publication`.

## Decisoes

- 2026-07-11: usar Qwen local para expandir prompts, Stable Diffusion local com LoRA explicita e MMS-TTS em portugues. Motivo: preserva o contrato multimodal sem supor que uma API remota aplica o adaptador LoRA.

## Progresso e descobertas

- Pesos de `config_b` confirmados localmente, com 6.4 MB.
- Smoke test final em `resultados/app_smoke_v3/`: tres fluxos completos com latencias de 35.086 s, 15.301 s e 14.098 s.
- O Space esta planejado para CPU Basic; a performance remota deve ser medida e documentada antes de qualquer declaracao de funcionamento publico.
- Bundle criado em `space/` e importado localmente.
- A autenticacao confirmou a conta `RalphError`; a API recusou a criacao do Space com `402 Payment Required`, pois Gradio cpu-basic exige PRO para a conta atual.
- Apos upgrade para PRO, o Space foi criado, recebeu o bundle e chegou a `RUNNING` no commit `c6cf72aa1ea181bbb37883acb8e72635747def87`.
- O Space foi corrigido para Python 3.11, Gradio 6.20.0, `peft` e 12 passos em CPU. Duas execucoes anonimas completas foram observadas; a segunda levou 257.671 s.

## Resultado final

Backends implementados, validados por contrato e testados localmente com tres fluxos completos. O Space esta publicado, em execucao e possui duas execucoes anonimas completas registradas. A alta latencia em CPU Basic precisa de contingencia para demonstracao.
