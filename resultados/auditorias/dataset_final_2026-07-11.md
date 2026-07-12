# Auditoria final do dataset

**Data da auditoria:** 2026-07-11  
**Revisao humana de captions:** confirmada pelo responsavel Felipe Santiago nesta atualizacao.

## Resultado

- Imagens finais aprovadas: **24/24**.
- Registros em `dados/metadata.jsonl`: **24**.
- Imagens rejeitadas ou pendentes: **nenhuma**.
- Resolucao final: 768 x 768 para todos os itens.
- Duplicatas perceptuais no manifesto: nenhuma.

Cada item aprovado foi verificado contra `dados/fontes.csv`, a triagem visual, o manifesto com hash do PNG
final e a caption humana revisada. A triagem confirma coerencia com **Xilogravura Digital do Cerrado** e
ausencia aparente de marca-d'agua, assinatura problematica, IP protegida e pessoa identificavel.

As 24 fontes sao CC-BY-SA, portanto permitem derivacao com atribuicao e compartilhamento sob a mesma
licenca. Os PNGs finais sao declarados como `derivada_editada_deterministica_sem_ia_generativa`: foram
produzidos por Pillow no processamento `woodcut-v2`, nao por modelo generativo. Assim, nao sao
apresentados como imagens simplesmente coletadas ja no estilo, nem como imagens sinteticas por IA.

## Captions e metadata

Todas as captions possuem status `revisada`, comecam por `flpxilobr,` e nao possuem URL, licenca, nome de
arquivo ou outro metadado administrativo. A revisao humana confirmou a adequacao das descricoes aos
elementos visiveis na imagem. `dados/metadata.jsonl` foi gerado somente depois de a pre-validacao aprovar
os 24 pares; cada linha contem `file_name` e `text`.

BLIP nao foi executado retroativamente. No runtime local de curadoria, `torch` e `transformers` nao
estavam disponiveis; as captions foram produzidas por inspecao visual/metadados e revisadas humanamente.

## Evidencias e comandos

- `resultados/auditorias/dataset_validacao_final_2026-07-11.json`: resultado por item e resumo da
  pre-validacao.
- `scripts/finalize_dataset.py --report resultados/auditorias/dataset_validacao_final_2026-07-11.json`:
  aprovou 24 itens sem escrever metadata.
- `scripts/finalize_dataset.py --report resultados/auditorias/dataset_validacao_final_2026-07-11.json --write-metadata`:
  aprovou e gerou 24 registros.

## Limite desta etapa

Dataset validado localmente. Nenhum treino LoRA, checkpoint, publicacao remota ou uso de token foi
executado nesta auditoria.
