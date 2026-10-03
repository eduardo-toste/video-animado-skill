---
name: "video-animado"
description: Cria vídeos animados explicativos no estilo Jitter/motion design — cards com diagramas de fluxo, listas, números, comparações e frases de impacto, câmera que dá zoom em cada card, setas que se desenham e um pulso percorrendo o conteúdo — prontos para LinkedIn, Instagram e reels (4:5, 1:1 ou 9:16), em 4 estilos visuais, com um briefing guiado por perguntas e botão para exportar MP4. Use sempre que a pessoa pedir um vídeo animado, vídeo explicativo, motion graphics, animação de diagrama, carrossel animado, "vídeo igual ao do Jitter", "vídeo desses do LinkedIn", vídeo para post ou reels, ou quiser transformar um assunto, processo, passo a passo, comparação, dados ou lista de dicas em vídeo, mesmo que não use a palavra "animação".
---

# Vídeo animado em cards

Esta skill gera uma página HTML que toca e exporta um vídeo explicativo. O motor de animação está pronto em `assets/template.html`; seu trabalho é **entender o assunto do post, escolher a estrutura e escrever um JSON** que descreve o vídeo. Não reescreva o motor: ele já resolve câmera, tempos, animações, formatos e a exportação para MP4, e alterá-lo costuma quebrar a exportação.

## Como o vídeo funciona

1. Abertura: título com uma palavra em destaque (pílula), subtítulo, legenda de categorias e todos os cards surgindo.
2. Uma cena por card, na ordem da lista: a câmera dá zoom no card, o nome da cena aparece grande no topo com "N de M" e o conteúdo se monta (caixas e setas, itens de lista, número contando, barras crescendo, colunas de comparação, frase linha a linha). Se houver `links` entre cards, a câmera passeia pela seta e um ponto percorre a ligação.
3. Fechamento: a câmera volta para a visão geral e surge um cartão final com a chamada (opcional).

Cada card precisa funcionar sozinho em zoom, porque é assim que a pessoa vai vê-lo.

## 1. Briefing do post

O briefing define tudo o que estrutura o vídeo. Ele tem uma ficha fixa e um jeito padrão de perguntar, para que todo post comece do mesmo lugar.

### A ficha

| campo | opções | padrão se a pessoa não escolher |
|---|---|---|
| **Assunto** | texto livre | obrigatório: pergunte |
| **Tipo de post** | passo a passo, comparativo, casos de uso, lista de dicas, números, framework, comparativo de opções (detalhes em `references/estruturas.md`) | o que melhor combina com o assunto |
| **Formato** | feed 4:5, quadrado 1:1, vertical 9:16 | 4:5 |
| **Estilo** | papel, noturno, técnico, pastel (exemplos em `assets/exemplos/estilos.png`) | papel |
| **Quantidade de cards** | 4, 6 ou 8 (5 também é possível) | 6 |
| **Público** | ex.: iniciantes, profissionais da área, liderança | profissionais da área do assunto |
| **Chamada final** | salvar e compartilhar, comentar, seguir o perfil, conhecer um produto | salvar e compartilhar |
| **Pontos obrigatórios** | dados, fontes, nomes, termos que precisam aparecer | nenhum |
| **Idioma e tom** | inferidos da conversa | idioma da pessoa, tom direto |

### Como perguntar

1. **Leia o pedido primeiro.** Preencha a ficha com tudo o que a pessoa já disse (inclusive se ela colou a ficha pronta do README). Nunca pergunte o que já está respondido.
2. **Modo rápido.** Se a pessoa disser "decide você", "rápido", "sem perguntas" ou algo equivalente, não pergunte nada além do assunto: use os padrões e diga, em uma linha, quais escolhas fez.
3. **Sem assunto:** pergunte só o assunto, em uma frase, e encerre a mensagem.
4. **Rodada 1 — estrutura e visual.** Pergunte, numa única chamada de `ask_user_input_v0`, as três primeiras perguntas que ainda faltarem entre:
   - *Que tipo de post?* Ofereça os 4 tipos que mais combinam com o assunto, com rótulos curtos (ex.: "Passo a passo", "Comparativo", "Casos de uso", "Lista de dicas"). A pessoa pode digitar outro.
   - *Qual formato?* "Feed 4:5", "Quadrado 1:1", "Vertical 9:16".
   - *Qual estilo?* "Papel", "Noturno", "Técnico", "Pastel".
   Se o estilo estiver entre as perguntas, mostre antes `assets/exemplos/estilos.png` com `present_files`; se o tipo estiver, mostre também `assets/exemplos/tipos.png`. Escreva uma frase curta antes das opções.
5. **Rodada 2 — conteúdo.** Depois das respostas, numa segunda chamada, pergunte o que faltar entre:
   - *Quantos cards?* Ofereça 3 quantidades que fazem sentido para o tipo (ex.: 4, 6, 8) e "Você decide".
   - *Para quem é o post?* 3 públicos plausíveis para o assunto.
   - *O que a chamada final deve pedir?* "Salvar e compartilhar", "Comentar", "Seguir o perfil", "Conhecer um produto".
   No texto que acompanha as opções, convide a pessoa a escrever pontos obrigatórios, dados ou fontes, se tiver.
6. **Sem `ask_user_input_v0`** (outros ambientes): faça as perguntas que faltam numa única mensagem curta, cada uma com as opções entre parênteses, e diga que ela pode responder "padrão" para qualquer uma.
7. **Depois do briefing, siga direto.** Em uma ou duas linhas, diga o plano (tipo, formato, estilo e os títulos dos cards) e já monte o vídeo. Só espere aprovação do roteiro se a pessoa pedir.

Guarde a ficha preenchida no campo `"briefing"` do JSON (o motor ignora esse campo), para facilitar ajustes e novas versões do mesmo post.

Se o post depende de dados, use só os que a pessoa forneceu ou que você confirmou em fonte; nunca invente estatísticas, e cite a fonte na legenda do card.

## 2. Escolher a estrutura

O tipo de post do briefing define a estrutura. Leia `references/estruturas.md`. Resumo:

- **Mapa de casos de uso:** grade de cards `flow` agrupados por categoria (o vídeo de referência).
- **Passo a passo:** um card por passo, ligados por `links`, com `scene: "Passo N"`.
- **Antes × depois / mito × verdade:** cards `compare`, abertos por um `text` e provados por um `stat`.
- **Números que importam:** `stat` e `bars`.
- **Framework explicado:** `text` com a ideia central e um card por componente.
- **Lista de dicas:** `list` numerada.
- **Comparativo de opções:** `bars` por critério, `compare` de prós e contras, `text` com o veredito.

As estruturas podem ser misturadas: escolha, para cada card, o tipo que mostra aquela ideia do jeito mais simples.

## 3. Escrever o conteúdo

- **4 a 6 cards** (até 8 se forem simples). Cada card responde uma pergunta só.
- **2 a 4 categorias**, com nomes curtos e fortes. Omita `color` e `tint` para usar a paleta do estilo escolhido (recomendado); defina só se a pessoa pedir cores específicas.
- **Título:** curto, com uma palavra-chave na pílula. **Subtítulo:** a tese do vídeo, em minúsculas.
- **Legendas dos cards:** o "e daí?" da ideia, em minúsculas, até ~45 caracteres. Opcionais.
- **Textos curtos:** rótulos de 1 a 2 palavras, itens de lista com até ~35 caracteres, frases de impacto com até ~20 palavras.
- **CTA:** título curto e uma frase útil, nada genérico. Omita `cta` para terminar sem cartão.

## 4. Montar o JSON

Pegue as posições dos cards na **tabela rápida** de `references/layouts.md` (seção 0), cruzando formato e quantidade: use a coluna "trilha" para passo a passo e "grade" para os demais. Os padrões de diagrama do tipo `flow` estão na seção 3. As cenas tocam na ordem da lista `cards`. Use os exemplos completos como modelo: `references/exemplo-agentes.json` (casos de uso, 4:5), `references/exemplo-copiloto.json` (passo a passo em trilha, 4:5), `references/exemplo-mitos.json` (comparativo, 1:1) e `references/exemplo-passo-a-passo.json` (passo a passo vertical, 9:16, todos os tipos de card).

```json
{
  "format": "4:5",
  "theme": "papel",
  "briefing": {"assunto": "...", "tipo": "passo a passo", "publico": "...", "chamada": "comentar"},
  "title": ["texto", {"pill": "destaque"}, "texto"],
  "subtitle": "tese curta",
  "legend": true,
  "counter": true,
  "pace": 1,
  "categories": {"chave": {"label": "Nome"}, "outra": {"label": "Outra"}},
  "links": [[0, 1], [1, 2, {"route": "elbow", "label": "opcional"}]],
  "cards": [ ... ],
  "cta": {"title": "Chamada final", "text": "Frase de apoio."}
}
```

Campos globais opcionais: `theme` (`papel`, `noturno`, `tecnico`, `pastel`); `legend: false` esconde a legenda de categorias; `counter: false` esconde o "N de M"; `pace` acima de 1 deixa as montagens mais lentas (1.3 = 30% mais lento); `links` liga cards pelo índice (começando em 0); `{"pill": "...", "color": "#hex"}` muda a cor da pílula do título.

Todo card tem: `kind`, `cat`, `title`, `x`, `y`, `w`, `h` e, opcionalmente, `caption`, `scene` (texto grande da cena; padrão = nome da categoria), `tag` (texto do selo; padrão = nome da categoria) e `duration` (segundos da cena; padrão automático).

Campos por tipo:

| kind | campos | observações |
|---|---|---|
| `flow` (padrão) | `nodes`, `edges` | nós com `id, x, y, w, h, label`, opcionais `icon`, `variant` (`core`, `ok`, `bad`, `warn`), `sub`. Arestas `["a","b"]`, `["a","b",{"color":"bad"}]`, `["b","a",{"loop":true,"label":"...","drop":60}]`. Um nó `core` por card. |
| `list` | `items: [{text, icon?, variant?, note?}]`, `numbered?` | até 6 itens; `numbered: true` mostra 1, 2, 3… |
| `stat` | `value` (número), `prefix?`, `suffix?`, `decimals?`, `label?`, `sub?` | o número conta de 0 até `value` |
| `bars` | `items: [{label, value, display?, highlight?}]` | marque a barra principal com `highlight: true`; `display` é o texto ao lado da barra (ex.: "46%") |
| `compare` | `left` e `right`: `{title, items: [texto], variant?, icon?}` | `bad` à esquerda e `ok` à direita para mito × verdade; até 4 linhas |
| `text` | `text`, `author?` | trechos entre `*asteriscos*` ganham a cor da categoria |

Ícones disponíveis: terminal, chip, check, ban, split, layers, code, eye, tool, spark, doc, user, users, cart, pencil, gauge, search, database, cloud, mail, chart, lock, clock, money, globe, phone, bolt, heart, star, flag, bell, question, target, refresh, sliders, image, calendar, message.

## 5. Gerar e validar

```bash
python3 scripts/build.py conteudo.json /mnt/user-data/outputs/<nome>.html
```

O script recusa o conteúdo se houver **ERROS** (card fora do formato, cards sobrepostos, nós sobrepostos, ícone inexistente, campo obrigatório faltando, ciclo sem `loop`) e mostra **AVISOS** de legibilidade (texto que não cabe, itens demais, seta curta). Corrija os erros e, sempre que possível, os avisos.

## 6. Conferir visualmente

Se houver Playwright disponível:

```bash
python3 scripts/preview.py /mnt/user-data/outputs/<nome>.html /tmp/preview
```

Veja `/tmp/preview/contact.png` (visão geral, cada cena e o fechamento). Procure texto cortado ou reduzido demais, conteúdo descentralizado, setas atravessando caixas e cards vazios demais. Ajuste e gere de novo. Se a fonte Inter Tight não estiver instalada, os textos parecem um pouco mais largos na prévia do que no navegador; dá para instalar baixando `https://raw.githubusercontent.com/google/fonts/main/ofl/intertight/InterTight%5Bwght%5D.ttf` para `~/.fonts/` e rodando `fc-cache -f`.

## 7. Entregar

- **No claude.ai, com a ferramenta Artifact:** publique o HTML com `capabilities: {"downloads": true}`; sem isso, o botão **Exportar MP4** não consegue salvar o arquivo dentro do visualizador. Para atualizar um vídeo já publicado, publique de novo passando o `url` dele.
- **Em outros ambientes:** entregue o arquivo HTML; aberto direto no navegador, o botão de exportar baixa o arquivo normalmente.

Diga à pessoa, em poucas linhas, quais escolhas você fez (estrutura, formato, número de cards) e como usar:
- **Exportar MP4** gera o vídeo no formato escolhido, a 30 fps e sem som. Funciona melhor no Chrome ou no Edge (H.264). Em navegadores sem suporte, grava em tempo real e pode sair em WebM.
- **Modo gravação** esconde os controles e toca do zero, para quem prefere gravar a tela.
- Narração e trilha entram depois, no CapCut ou similar.

### Texto do post (opcional)

Ofereça escrever a legenda do post para acompanhar o vídeo: um gancho na primeira linha, 3 a 6 linhas curtas que resumem os cards sem repetir o vídeo palavra por palavra, a chamada final e, se fizer sentido, 3 a 5 hashtags. Escreva no tom da pessoa.

## Ajustes depois da primeira versão

Mude só o JSON e gere de novo: trocar textos, reordenar cards, mudar o tipo de um card, cores, formato ou ritmo (`pace`). Para mudar de formato, reposicione os cards com a tabela do novo formato em `references/layouts.md`.

## Estilos visuais

| estilo | visual | fonte |
|---|---|---|
| `papel` | off-white pontilhado, bordas grossas, setas pretas (o vídeo de referência) | Inter Tight |
| `noturno` | fundo escuro, cores luminosas, bom para tecnologia e dados | Inter Tight |
| `tecnico` | branco com quadriculado de engenharia, cantos retos, ar de documentação | Space Grotesk |
| `pastel` | creme quente, cantos bem arredondados, cores suaves; bom para carreira e comportamento | Bricolage Grotesque |

Todos mantêm a mesma estrutura de cards, animação e câmera. Não crie estilos novos nem altere o motor; se a pessoa quiser outra paleta, defina `color` nas categorias.
