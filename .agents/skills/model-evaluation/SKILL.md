---
name: model-evaluation
description: Avalia modelo base versus LoRA com grade, CLIPScore, memorização e avaliação humana cega; use para notebook 03, métricas e evidências de qualidade/overfitting.
---

# Avaliação completa

1. Congelar 6 prompts e parâmetros; usar a mesma seed base × LoRA.
2. Salvar imagens individuais e grade 6×2 com rótulos claros.
3. Calcular CLIPScore de cada geração e média por modelo; exportar CSV reproduzível.
4. Gerar 10 casos próximos às captions e comparar com o dataset; registrar risco de cópia/memorização.
5. Preparar avaliação humana cega com ordem aleatória, chave separada e 5+ pessoas externas.
6. Anonimizar dados, exportar respostas brutas e resumo; não inventar participantes.
7. Interpretar as três fontes de evidência, incluindo resultados ruins/contraditórios.
8. Rodar `validate_project.py --stage evaluation`.

Não use FID/LPIPS como substituto dos requisitos. Métricas extras são opcionais e só entram com
justificativa e implementação válida.
