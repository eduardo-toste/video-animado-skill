# Layouts e padrões de diagrama

Formatos (`"format"` no JSON): `4:5` = 1080 × 1350 (padrão, feed do LinkedIn/Instagram), `1:1` = 1080 × 1080, `9:16` = 1080 × 1920 (stories, reels, shorts).
O cabeçalho ocupa até y = 190. Cards ficam entre x 20–1060 e y 190 até (altura − 20), com 20 px entre eles.
Na visão geral, a câmera enquadra todos os cards automaticamente; na cena, dá zoom no card em foco.

## Sumário
0. Tabela rápida: tipo × formato × quantidade
1. Grades de cards prontas (4, 5, 6 e 8 cards)
2. Área útil dentro de um card
3. Padrões de diagrama com coordenadas
4. Tamanhos de nó e texto
5. Paletas de categoria

---

## 0. Tabela rápida: tipo × formato × quantidade

Use esta tabela para transformar as respostas do briefing direto em posições. "Grade" = cards lado a lado sem setas entre eles; "trilha" = cards em zigue-zague ligados por `links` (para passo a passo).

| formato | cards | grade | trilha (passo a passo) |
|---|---|---|---|
| 4:5 | 4 | 2 × 2: w 500, h 550, x 30/550, y 200/770 | w 470, h 515; card 0 (30,200), 1 (580,200), 2 (580,785), 3 (30,785); links [[0,1],[1,2],[2,3]] |
| 4:5 | 5 | 1 largo (30,200,1020,360) + 2 × 2 de 500 × 360 em y 580/960 | coluna: x 30, w 1020, h 170, y 200/430/660/890/1120, links retos |
| 4:5 | 6 | grade de 6 (seção 1) | w 470, h 320, x 30/580, y 200/590/980; cobra: 0(30,200) 1(580,200) 2(580,590) 3(30,590) 4(30,980) 5(580,980), links [[0,1],[1,2],[2,3],[3,4],[4,5]] |
| 4:5 | 8 | 4 × 2: w 500, h 265, x 30/550, y 200/485/770/1055 | w 470, h 230, y 200/490/780/1070; cobra como a de 6 (linhas pares da esquerda para a direita, ímpares da direita para a esquerda); links consecutivos |
| 1:1 | 4 | w 500, h 405, x 30/550, y 200/625 | w 470, h 380; card 0 (30,200), 1 (580,200), 2 (580,640), 3 (30,640); links [[0,1],[1,2],[2,3]] |
| 1:1 | 6 | w 330, h 275, x 30/375/720, y 200/495 | w 300, h 260; card 0 (30,200), 1 (390,200), 2 (750,200), 3 (750,540), 4 (390,540), 5 (30,540); links [[0,1],[1,2],[2,3],[3,4],[4,5]] |
| 9:16 | 4 | w 1020, h 370, x 30, y 210/640/1070/1500 | coluna igual à grade, com links retos |
| 9:16 | 6 | w 500, h 470, x 30/550, y 210/700/1190 | zigue-zague (seção 1), links `{"route": "elbow"}` |
| 9:16 | 8 | w 500, h 380, x 30/550, y 210/610/1010/1410 | zigue-zague de 8: w 500, h 290, card i em x 30 (par) ou 550 (ímpar), y 210 + i × 195, links `elbow` |

**Importante:** as cenas tocam na ordem da lista `cards`. Na trilha, a lista precisa estar na ordem do caminho e os `links` ligam sempre o card i ao i+1. As setas escolhem o lado certo automaticamente. Diagramas `flow` em cards de h ≤ 260 devem ter uma linha só de nós.

## 1. Grades de cards prontas

Use uma destas. Elas já respeitam margens e espaçamentos.

**6 cards (padrão, 3 linhas):** linha 1 = um card largo + um estreito, linhas 2 e 3 = dois cards iguais.

| card | x | y | w | h |
|---|---|---|---|---|
| 1 | 30 | 200 | 640 | 360 |
| 2 | 690 | 200 | 360 | 360 |
| 3 | 30 | 580 | 500 | 360 |
| 4 | 550 | 580 | 500 | 360 |
| 5 | 30 | 960 | 500 | 360 |
| 6 | 550 | 960 | 500 | 360 |

**4 cards (2 × 2, cards altos):**

| card | x | y | w | h |
|---|---|---|---|---|
| 1 | 30 | 200 | 500 | 550 |
| 2 | 550 | 200 | 500 | 550 |
| 3 | 30 | 770 | 500 | 550 |
| 4 | 550 | 770 | 500 | 550 |

**4 cards (uma coluna, faixas largas)** — bom para fluxos longos e lineares:

| card | x | y | w | h |
|---|---|---|---|---|
| 1 | 30 | 200 | 1020 | 265 |
| 2 | 30 | 485 | 1020 | 265 |
| 3 | 30 | 770 | 1020 | 265 |
| 4 | 30 | 1055 | 1020 | 265 |

**5 cards:** linha 1 = um card de largura total (x 30, y 200, w 1020, h 360); linhas 2 e 3 iguais às linhas 2 e 3 da grade de 6.

**8 cards (4 linhas de 2):** w 500, h 265, x 30 e 550, y 200 / 485 / 770 / 1055. Com h 265 cabe só uma linha de nós ou um leque de 2 saídas, então use diagramas simples.

**1:1 — 4 cards:** w 500, h 405, x 30 e 550, y 200 e 625.
**1:1 — 6 cards:** w 330, h 275, x 30 / 375 / 720, y 200 e 495 (cards pequenos: diagramas simples, `stat`, `text` curto).

**9:16 — zigue-zague de 6 (passo a passo):** w 500, h 380; card 1 (30, 210), 2 (550, 480), 3 (30, 750), 4 (550, 1020), 5 (30, 1290), 6 (550, 1500). Ligue com `links` `{"route": "elbow"}`.
**9:16 — coluna de 5:** x 30, w 1020, h 280, y 210 / 530 / 850 / 1170 / 1490. Ligações retas entre cards consecutivos.
**9:16 — grade de 6:** w 500, h 470, x 30 e 550, y 210 / 700 / 1190 (+470 = 1660, sobra espaço para respirar).

Se o tema pede uma ordem (passo 1, 2, 3…), os cards são lidos e animados na ordem da lista `cards`, da esquerda para a direita e de cima para baixo.

## 2. Área útil dentro de um card

Vale para todos os tipos. `list`, `stat`, `bars`, `compare` e `text` se distribuem sozinhos na área útil; só `flow` exige coordenadas de nós.
Tamanhos que funcionam bem: `list` até 6 itens em h 360 (até 4 se tiver legenda); `compare` até 4 linhas por lado; `stat` com h ≥ 260; `text` com até ~20 palavras.

Coordenadas dos nós são relativas ao canto do card.

- Topo: y ≥ 52 (acima disso fica o selo e o título do card).
- Base: y + h ≤ altura do card − 48 (abaixo fica a legenda).
- Laterais: x ≥ 10 e x + w ≤ largura do card − 10.
- Centralize o diagrama: a sobra à esquerda e à direita deve ser parecida.
- Para um card de altura 360, a faixa útil vai de 52 a 312; o centro vertical fica em torno de y = 170.

## 3. Padrões de diagrama

Escolha o padrão que melhor representa a ideia do card. Coordenadas abaixo para um card de 500 × 360; para outras larguras, redistribua mantendo 20 a 35 px entre colunas.

**Cadeia linear (3 a 5 nós)** — etapas em sequência.
Nós de 100 × 64 em y 120 (ou centralizados), colunas a cada 125 px.
`[["a","b"],["b","c"],["c","d"]]`

**Leque de saída (1 → 3)** — classificar, rotear, distribuir.
Origem 95 × 60 em (40, 140). Destinos 100 × 50 em x 195, y 70 / 145 / 220.

**Leque de entrada (3 → 1)** — combinar, votar, consolidar.
Espelho do anterior: fontes em x 40, y 70 / 145 / 220; destino 105 × 66 em (355, 137).

**Losango (1 → 3 → 1)** — paralelizar e juntar. Colunas em x 40, 195, 355.
Com 4 colunas (origem → orquestrador → 3 workers → síntese) use x 12, 112, 250, 392 e larguras 80, 108, 112, 95.

**Desvio para baixo** — uma etapa pode bloquear/falhar. Nó principal na linha y 120; nó de desvio (`variant: "bad"`) logo abaixo, mesmo x, em y 228, com aresta `{"color": "bad"}`.

**Laço de feedback** — refazer até passar. Três nós de 110 × 64 em y 110 (x 40, 195, 350); aresta de volta `["b", "a", {"loop": true, "label": "refaz até passar", "drop": 70}]`. O laço desce `drop` px abaixo dos nós; não pode invadir a legenda.

**Ciclo em tempo real** — estado → decisão → ação, repetindo. Igual ao laço, com rótulo do tipo "a cada 300 ms".

Regras gerais:
- 3 a 6 nós por card. Mais que isso fica ilegível no feed.
- Exatamente um nó `core` por card: é o protagonista daquela ideia (a decisão, o classificador, o avaliador).
- Use `ok`, `bad` e `warn` só para resultados (aprovado, bloqueado, revisar).
- As setas são automáticas: horizontais quando o destino está mais ao lado que acima/abaixo, verticais no caso contrário.

## 4. Tamanhos de nó e texto

- Nó com ícone em cima do rótulo: h ≥ 58 (use 60 a 66). Com `sub`, use h 70 a 76.
- Nó com ícone ao lado do rótulo: h 50.
- Largura mínima ≈ 9 px por caractere do rótulo + 18; some 26 se o ícone fica ao lado.
- Rótulos: 1 ou 2 palavras, minúsculas, sem ponto ("classifica", "LLM 1", "aprovado").
- Legenda do card: até ~45 caracteres em cards de 500, ~40 em cards de 360, frase curta em minúsculas.
- Título do card: 1 a 3 palavras.

## 5. Paletas de categoria

Cada categoria tem `color` (borda, selo, título) e `tint` (fundo dos nós). Combinações testadas:

| nome | color | tint |
|---|---|---|
| azul | #2457d6 | #e7eefc |
| verde | #128a5e | #e3f3eb |
| âmbar | #c27a0e | #fbf0dc |
| roxo | #7a4be0 | #efe9fc |
| vermelho | #c8402f | #fbe6e2 |
| petróleo | #0f7c8c | #e0f2f4 |
| grafite | #3d3d46 | #ececee |

Use 2 a 4 categorias. Na referência original, a ordem foi azul, verde, âmbar, roxo.
