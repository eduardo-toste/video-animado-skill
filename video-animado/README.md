# video-animado

Transforma um assunto em um vídeo animado no estilo Jitter para LinkedIn, Instagram ou reels: cards com diagramas, listas, números e comparações, uma câmera que dá zoom em cada card e um botão que exporta o MP4 pronto.

## Como pedir

Escreva `/video-animado` e o assunto do post. Exemplo:

> /video-animado quero um post sobre como dar feedback difícil para o time

O Claude faz duas rodadas rápidas de perguntas com opções para clicar (veja abaixo), monta o vídeo e entrega a página com o player e o botão **Exportar MP4**.

Não quer responder perguntas? Diga "decide você" junto com o assunto e ele usa as escolhas padrão. Já sabe o que quer? Cole a ficha preenchida (no fim deste arquivo) e ele vai direto para o vídeo.

## As perguntas do briefing

**Rodada 1: estrutura e visual**

1. **Que tipo de post?** (o Claude oferece os 4 que mais combinam com o seu assunto)
2. **Qual formato?** Feed 4:5 · Quadrado 1:1 · Vertical 9:16
3. **Qual estilo?** Papel · Noturno · Técnico · Pastel

**Rodada 2: conteúdo**

4. **Quantos cards?** 4 · 6 · 8 · Você decide
5. **Para quem é o post?** (opções de público sugeridas a partir do assunto)
6. **O que a chamada final deve pedir?** Salvar e compartilhar · Comentar · Seguir o perfil · Conhecer um produto

Na segunda rodada, você também pode escrever pontos que precisam aparecer: dados, fontes, nomes, ferramentas.

## Tipos de post

![Exemplos de tipos de post](assets/exemplos/tipos.png)

| tipo | quando usar | como fica |
|---|---|---|
| **Passo a passo** | processos, tutoriais, jornadas | cards ligados por setas; a câmera segue o caminho e mostra "Passo 1, 2, 3…" |
| **Comparativo** | mito × verdade, antes × depois, certo × errado | colunas lado a lado em vermelho e verde, com frase de abertura e número de prova |
| **Casos de uso** | "onde X se aplica", padrões, arquiteturas | grade de diagramas de fluxo agrupados por categoria |
| **Lista de dicas** | "7 dicas", erros comuns, checklists | listas numeradas que entram item a item |
| **Números** | pesquisas, resultados, benchmarks | números grandes que contam e barras que crescem |
| **Framework** | explicar um método ou modelo mental | uma frase central e um card por componente |
| **Comparativo de opções** | ferramenta A × B × C, planos | barras por critério, prós e contras e um veredito |

Os tipos podem ser misturados: um passo a passo pode ter uma comparação no meio, por exemplo.

## Estilos

![Os quatro estilos aplicados ao mesmo post](assets/exemplos/estilos.png)

| estilo | visual | combina com |
|---|---|---|
| **Papel** | off-white pontilhado, bordas grossas, setas pretas | qualquer assunto; é o estilo de referência |
| **Noturno** | fundo escuro com cores luminosas | tecnologia, dados, segurança |
| **Técnico** | quadriculado de engenharia, cantos retos, fonte geométrica | arquitetura, engenharia, documentação |
| **Pastel** | creme quente, cantos arredondados, cores suaves | carreira, liderança, comportamento |

## Formatos

| formato | tamanho | onde usar |
|---|---|---|
| Feed 4:5 | 1080 × 1350 | LinkedIn e Instagram (ocupa mais tela no feed) |
| Quadrado 1:1 | 1080 × 1080 | qualquer rede, carrosséis |
| Vertical 9:16 | 1080 × 1920 | stories, reels, shorts, TikTok |

## Depois que o vídeo fica pronto

- **Exportar MP4:** gera o vídeo a 30 fps, sem som. Funciona melhor no Chrome ou no Edge.
- **Modo gravação:** esconde os controles e toca do zero, para quem prefere gravar a tela.
- **Ajustes:** peça em linguagem normal ("troca o estilo para noturno", "deixa mais lento", "muda o passo 3 para uma lista", "passa para 9:16"). O Claude altera só o conteúdo e gera de novo.
- **Legenda do post:** peça e o Claude escreve o texto para acompanhar o vídeo.
- Narração e trilha sonora entram depois, num editor como o CapCut.

## Ficha para pular as perguntas

Copie, preencha e envie junto com `/video-animado`. Deixe em branco o que quiser que o Claude decida.

```
Assunto:
Tipo: (passo a passo / comparativo / casos de uso / lista de dicas / números / framework / comparativo de opções)
Formato: (4:5 / 1:1 / 9:16)
Estilo: (papel / noturno / técnico / pastel)
Cards: (4 / 6 / 8)
Público:
Chamada final: (salvar e compartilhar / comentar / seguir / conhecer um produto)
Pontos obrigatórios:
```
