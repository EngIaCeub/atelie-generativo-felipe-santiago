# Estado do projeto

Atualizado em: 2026-07-10

## Resumo
- Repositório GitHub: **criado**.
- Token Hugging Face: **disponível, não versionado**.
- Arquitetura Codex: **aplicada localmente; validação de bootstrap bloqueada por decisões humanas**.
- Etapa acadêmica atual: **Etapa 0 - organização e proposta**.

## Bloqueios atuais
1. Confirmar integrantes da equipe e papéis.
2. Escolher estilo visual permitido e obter aprovação do professor.
3. Definir token textual exclusivo do estilo, por exemplo `estilo_cerrado_felipe`.
4. Informar namespace Hugging Face e nomes desejados para repositório LoRA e Space em
   `config/project.json`.

## Próximo marco
Portão humano: preencher `config/project.json` com estilo visual permitido, `trigger_token`, namespace
Hugging Face e confirmação dos papéis; submeter `docs/PROPOSTA_ESTILO.md` ao professor. Não iniciar coleta
de imagens antes de estilo/fontes/licenças estarem aprovados.

## Checklist macro
- [x] Repositório criado.
- [x] Token Hugging Face obtido e mantido fora do Git.
- [x] Estrutura Codex aplicada localmente.
- [ ] Bootstrap validado após definição/aprovação de estilo e namespace.
- [ ] Proposta de estilo aprovada.
- [ ] Dataset completo e captions revisadas.
- [ ] Duas configurações LoRA treinadas e comparadas.
- [ ] LoRA escolhido publicado com model card.
- [ ] Avaliação completa com evidências.
- [ ] Space público funcional.
- [ ] Relatório final em PDF.
- [ ] Demo Day ensaiado e com contingência.

## Regra de atualização
O agente deve atualizar este arquivo ao fim de cada tarefa relevante. Não marque itens executivos ou
humanos sem evidência.
