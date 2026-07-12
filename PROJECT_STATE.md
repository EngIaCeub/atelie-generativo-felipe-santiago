# Estado do projeto

Atualizado em: 2026-07-11

## Resumo

- Bootstrap, dataset, treino LoRA, avaliacao, publicacao e entrega final: **validados localmente**.
- Configuracoes `config_a` e `config_b`: concluidas; a LoRA selecionada no app e `config_b`, publicada em `https://huggingface.co/RalphError/flpxilobr-lora` com model card.
- Avaliacao: grade 6 x 2, 12 CLIPScores, 10 testes de memorizacao e respostas com 5 identificadores unicos.
- Aplicacao: provedores reais de prompt, imagem LoRA e TTS implementados; smoke test local com tres temas concluiu texto, PNG e WAV em cada caso.
- Space publico: criado e em estado `RUNNING` na evidencia registrada; duas execucoes anonimas produziram prompt, imagem e audio apos a configuracao humana do Secret.
- Relatorio final: `relatorio/relatorio_final.md` preenchido e `relatorio/relatorio_final.pdf` gerado.

## Etapa atual

**Entrega academica final preparada e validada localmente.**

## Bloqueios atuais

Nenhum bloqueio tecnico local detectado pela validacao final. Para apresentacao ao vivo, permanece uma limitacao operacional: o Space em CPU Basic tem latencia alta; usar a contingencia local documentada se o tempo da banca for curto.

## Nota sobre autoria e Git

O projeto e **individual** e tem Felipe Santiago como unico responsavel academico. Caso o historico local do Git apresente outros logins em algum momento, isso deve ser interpretado como efeito de sessoes equivocadas do Git ou do ambiente local, e nao como colaboracao real de outros membros no projeto. A autoria academica, as decisoes e a revisao humana final permanecem atribuídas a Felipe Santiago.

## Proximo marco

Revisao humana final do PDF e demonstracao: conferir visualmente o relatorio, abrir o Space antes da apresentacao e manter o plano B com evidencias offline.

## Checklist macro

- [x] Repositorio criado e bootstrap validado.
- [x] Dataset com 24 imagens, proveniencia e captions revisadas.
- [x] Duas configuracoes LoRA treinadas e registradas.
- [x] Avaliacao base x LoRA com evidencias tecnicas e dados humanos importados.
- [x] Smoke test local completo do app multimodal.
- [x] Space publico criado, em execucao e testado anonimamente.
- [x] Relatorio final em PDF.
- [x] Demo Day com contingencia documentada.

## Evidencias recentes

- `relatorio/relatorio_final.md`
- `relatorio/relatorio_final.pdf`
- `MODEL_CARD.md`
- `resultados/treino/experimentos.csv`
- `resultados/avaliacao/resumo_avaliacao.json`
- `resultados/avaliacao/grade_comparativa.png`
- `resultados/avaliacao/clipscore.csv`
- `resultados/avaliacao/memorizacao.csv`
- `resultados/avaliacao/avaliacao_humana.csv`
- `resultados/auditorias/publicacao_app_preparo_2026-07-11.md`
- `resultados/auditorias/publicacao_space_2026-07-11.md`
- `resultados/auditorias/space_teste_anonimo_2026-07-11.md`
- `resultados/auditorias/demo_day_plano_2026-07-11.md`
- `resultados/auditorias/rubric_audit_final_2026-07-11.md`
- `resultados/app_smoke_v3/smoke_report.json`

## Validacoes finais executadas

- `.\.venv\Scripts\python.exe scripts/validate_project.py --stage final` - aprovado.
- `.\.venv\Scripts\python.exe scripts/project_status.py` - todas as etapas `[OK]`.
- `.\.venv\Scripts\python.exe scripts/check_secrets.py` - nenhum padrao de segredo detectado.
- `.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest-tmp-final` - 22 testes aprovados; houve apenas aviso de cache do pytest no OneDrive.
- `.\.venv\Scripts\python.exe -m ruff check scripts app tests` - aprovado.

## Regra de atualizacao

Nao marcar publicacao como concluida sem URL publica confirmada, teste anonimo e evidencia registrada. Nenhum token deve ser salvo, exibido ou versionado.
