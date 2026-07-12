---
name: lora-training
description: Planeja, executa e documenta o fine-tuning LoRA no Colab T4; use para notebook 02, Diffusers, Accelerate, duas configurações, checkpoints, resume, Hub e model card.
---

# Fine-tuning LoRA

## Pré-condições
- Dataset validado e captions revisadas.
- Token disponível no ambiente/login sem ser exibido.
- Namespace e `lora_repo_id` definidos.

## Procedimento
1. Use o script oficial atual de `diffusers/examples/text_to_image/train_text_to_image_lora.py` e
   registre a versão/commit efetivamente usada.
2. Instale os requisitos do exemplo e configure Accelerate no notebook.
3. Use fp16, seed, checkpoints, Drive/Hub e `resume_from_checkpoint`.
4. Execute no mínimo as duas configurações de `config/project.json`; mantenha base, dataset e seed
   comparáveis.
5. Registrar em `resultados/treino/experimentos.csv`: commit, versões, parâmetros, tempo, status,
   checkpoint, URL e observações visuais.
6. Escolher a configuração com evidência de estilo, qualidade e menor memorização; justificar.
7. Publicar pesos e model card, confirmar download/carregamento em sessão limpa.

## Não fazer
- Não afirmar que o treino rodou apenas porque a célula existe.
- Não inventar duração, loss ou URL.
- Não depender do armazenamento efêmero do Colab.
- Não alterar várias variáveis ao mesmo tempo sem explicar a comparabilidade.
