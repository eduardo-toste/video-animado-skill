# Estruturas de vídeo

Escolha a estrutura pelo que o post quer provocar. Todas usam o mesmo motor e o mesmo visual; o que muda é o tipo dos cards, a disposição e se há setas entre os cards (`links`).

## Sumário
1. Mapa de casos de uso
2. Passo a passo
3. Antes × depois / mito × verdade
4. Números que importam
5. Framework explicado
6. Lista de dicas
7. Comparativo de opções
8. Misturando estruturas

---

## 1. Mapa de casos de uso
**Quando:** "onde X se aplica", "6 jeitos de usar Y", padrões, arquiteturas.
**Cards:** `flow` em todos. Categorias = verbos que agrupam os casos (Rotear, Filtrar…).
**Disposição:** grade de 6 (4:5). Sem `links`.
**Cena:** deixe `scene` vazio para aparecer o nome da categoria.
**Exemplo completo:** `exemplo-agentes.json`.

## 2. Passo a passo
**Quando:** processos, tutoriais, jornadas, "do zero ao X".
**Cards:** um por passo, misturando tipos conforme o conteúdo de cada passo (uma frase em `text`, um checklist em `list`, um fluxo em `flow`).
**Disposição:** zigue-zague ou coluna, com `links` ligando cada card ao próximo; use `{"route": "elbow"}` no zigue-zague. A câmera passeia seguindo a seta e um ponto percorre a ligação.
**Cena:** `"scene": "Passo 1"`, `"Passo 2"`… Categorias = fases (Validar, Construir, Vender).
**Formato:** 9:16 ou 4:5.
**Exemplo completo:** `exemplo-passo-a-passo.json` (9:16).

## 3. Antes × depois / mito × verdade
**Quando:** quebrar crença, mostrar transformação, "pare de fazer X".
**Cards:** `compare` (left com `variant: "bad"`, right com `variant: "ok"`). Abra com um `text` provocativo e feche com um `stat` que prove o ponto.
**Disposição:** 4 cards em 2 × 2 ou coluna larga.
**Cena:** `"Mito 1"`, `"Mito 2"`… ou o nome da categoria.

## 4. Números que importam
**Quando:** dados de pesquisa, resultados, benchmarks, "o que os números dizem".
**Cards:** `stat` para números isolados, `bars` para comparar valores (marque a barra principal com `highlight`). Um `text` no fim para a conclusão.
**Disposição:** grade de 4 ou 6. Formato 1:1 ou 4:5.
**Cuidado:** use apenas números que a pessoa forneceu ou que você confirmou numa fonte; cite a fonte na legenda (`caption`) do card.

## 5. Framework explicado
**Quando:** apresentar um modelo mental, método ou sigla (ex.: AIDA, OKR, Jobs to be done).
**Cards:** um `text` com a ideia central, um card por componente do framework (`flow` ou `list`) e um card de aplicação.
**Disposição:** 5 cards (um largo no topo com o `text`, quatro embaixo). `links` opcionais do card do topo para os demais.
**Cena:** a letra ou o nome de cada componente.

## 6. Lista de dicas
**Quando:** "7 dicas", "erros comuns", checklists.
**Cards:** `list` com `numbered: true`, agrupando 3 a 4 dicas por card; ou um `text` por dica forte.
**Disposição:** 4 cards 2 × 2 ou coluna larga em 9:16.

## 7. Comparativo de opções
**Quando:** ferramenta A × B × C, planos, abordagens.
**Cards:** `bars` para cada critério (custo, velocidade, qualidade), `compare` para prós e contras, `text` com o veredito.
**Disposição:** grade de 4 ou 6.

## 8. Misturando estruturas
Tudo é combinável: um mapa de casos pode abrir com um `stat` de impacto; um passo a passo pode ter um `compare` no meio. Regra prática: cada card responde uma pergunta só, e o tipo de card é o jeito mais simples de mostrar aquela resposta.

| a resposta é… | use |
|---|---|
| um processo, uma decisão, um fluxo | `flow` |
| uma sequência de itens, um checklist | `list` |
| um número | `stat` |
| vários números comparáveis | `bars` |
| um contraste entre dois lados | `compare` |
| uma frase/tese | `text` |
