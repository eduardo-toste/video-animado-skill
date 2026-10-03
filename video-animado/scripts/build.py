#!/usr/bin/env python3
"""Valida o JSON de conteúdo e gera o HTML do vídeo animado.

Uso:
    python3 build.py conteudo.json saida.html

Sai com código 1 se houver ERROS (o vídeo ficaria quebrado).
AVISOS indicam problemas prováveis de legibilidade; corrija sempre que puder.
"""
import json, re, sys, html
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "template.html"

FORMATS = {"4:5": (1080, 1350), "1:1": (1080, 1080), "9:16": (1080, 1920)}
HEADER_BOTTOM = 190
THEMES = ("papel", "noturno", "tecnico", "pastel")
KINDS = ("flow", "list", "stat", "bars", "compare", "text")
CARD_HEAD = 52      # faixa do selo + título do card
CARD_FOOT = 48      # faixa da legenda


def text_w(s, size, weight=700):
    """Estimativa conservadora da largura do texto em Inter Tight."""
    factor = {500: 0.53, 600: 0.55, 700: 0.57, 800: 0.6}[weight]
    wide = sum(1 for c in s if c in "mwMWOQGDH@%")
    narrow = sum(1 for c in s if c in "iljtfrI.,:;'| ")
    return size * (factor * len(s) + 0.25 * wide - 0.22 * narrow)


def main(src, out):
    errors, warns = [], []
    cfg = json.loads(Path(src).read_text(encoding="utf-8"))
    tpl = TEMPLATE.read_text(encoding="utf-8")
    icons = set(re.findall(r"^  ([a-z]+):'", tpl, re.M))

    fmt = cfg.get("format", "4:5")
    if fmt not in FORMATS:
        errors.append(f"format '{fmt}' inválido. Use 4:5, 1:1 ou 9:16.")
        fmt = "4:5"
    WORLD_W, WORLD_H = FORMATS[fmt]
    cats = cfg.get("categories") or {}
    if not cats:
        errors.append("Nenhuma categoria definida.")
    if cfg.get("theme", "papel") not in THEMES:
        errors.append(f"theme '{cfg.get('theme')}' inválido. Use: {', '.join(THEMES)}.")
    for k, c in cats.items():
        if "label" not in c:
            errors.append(f"Categoria '{k}' sem 'label'.")
        for key in ("color", "tint"):
            if key in c and not re.fullmatch(r"#[0-9a-fA-F]{6}", c[key]):
                errors.append(f"Categoria '{k}': '{key}' precisa ser hex de 6 dígitos (ex.: #2457d6). Omita para usar a paleta do tema.")

    # cabeçalho
    title = cfg.get("title")
    if not isinstance(title, list) or not title:
        errors.append("'title' precisa ser uma lista, ex.: [\"Como montar um\", {\"pill\": \"agente\"}, \"de IA\"].")
    else:
        tw = 34
        for p in title:
            tw += (text_w(p["pill"], 60, 800) + 48) if isinstance(p, dict) else text_w(p, 60, 800) + 16
        if tw > 1046:
            warns.append(f"Título longo demais (~{int(tw)}px de 1046). Encurte para caber numa linha.")
    leg = 36 + sum(25 + text_w(c.get("label", ""), 22) + 26 for c in cats.values())
    sub_w = text_w(cfg.get("subtitle", ""), 21, 600)
    if leg + sub_w + 30 > 1046:
        warns.append("Legenda + subtítulo se encostam no topo. Encurte o subtítulo ou os nomes das categorias.")

    cards = cfg.get("cards") or []
    if not 2 <= len(cards) <= 9:
        warns.append(f"{len(cards)} cards. O formato funciona melhor com 4 a 6.")

    rects = []
    for ci, c in enumerate(cards):
        tag = f"Card {ci+1} ('{c.get('title','?')}')"
        kind = c.get("kind", "flow")
        if kind not in KINDS:
            errors.append(f"{tag}: kind '{kind}' não existe. Use: {', '.join(KINDS)}.")
            continue
        for key in ("cat", "title", "x", "y", "w", "h"):
            if key not in c:
                errors.append(f"{tag}: falta '{key}'.")
        if any(k not in c for k in ("x", "y", "w", "h")):
            continue
        if c.get("cat") not in cats:
            errors.append(f"{tag}: categoria '{c.get('cat')}' não existe em 'categories'.")
        x, y, w, h = c["x"], c["y"], c["w"], c["h"]
        if x < 20 or y < HEADER_BOTTOM or x + w > WORLD_W - 20 or y + h > WORLD_H - 20:
            errors.append(f"{tag}: sai da área útil do formato {fmt} (x 20–{WORLD_W-20}, y {HEADER_BOTTOM}–{WORLD_H-20}).")
        for (j, r) in rects:
            if x < r[0] + r[2] + 10 and r[0] < x + w + 10 and y < r[1] + r[3] + 10 and r[1] < y + h + 10:
                errors.append(f"{tag}: encosta ou sobrepõe o card {j+1} (deixe pelo menos 20px entre cards).")
        rects.append((ci, (x, y, w, h)))

        cat_label = c.get("tag") or cats.get(c.get("cat"), {}).get("label", "")
        head_w = 18 + text_w(cat_label.upper(), 12, 800) + 12 + 18 + 12 + text_w(c.get("title", ""), 19)
        if head_w > w - 14:
            warns.append(f"{tag}: título do card longo demais para a largura ({int(head_w)}px de {w-14}).")
        if c.get("caption") and text_w(c["caption"], 15, 500) > w - 30:
            warns.append(f"{tag}: legenda longa demais para a largura do card (o texto será reduzido).")
        if c.get("scene") and text_w(c["scene"], 92, 800) > WORLD_W - 260:
            warns.append(f"{tag}: 'scene' longo; o título da cena será reduzido. Prefira 1 ou 2 palavras.")
        content_h = h - 54 - (50 if c.get("caption") else 20)
        CHECKS[kind](c, tag, w, h, content_h, icons, errors, warns)

    links = cfg.get("links") or []
    for L in links:
        if not isinstance(L, list) or len(L) < 2 or not all(isinstance(v, int) for v in L[:2]):
            errors.append(f"link inválido {L!r}; use [indice_origem, indice_destino] (começando em 0).")
            continue
        if not (0 <= L[0] < len(cards) and 0 <= L[1] < len(cards)):
            errors.append(f"link {L[:2]} cita card inexistente (os índices começam em 0).")

    cta = cfg.get("cta")
    if cta is not None and not cta.get("title"):
        errors.append("'cta' precisa de 'title' (ou remova 'cta' para terminar sem cartão final).")

    for wmsg in warns:
        print("AVISO:", wmsg)
    for e in errors:
        print("ERRO:", e)
    if errors:
        print(f"\n{len(errors)} erro(s). Nada foi gerado.")
        sys.exit(1)

    page_title = " ".join(p["pill"] if isinstance(p, dict) else p for p in title)
    out_html = tpl.replace("/*__CONFIG__*/", json.dumps(cfg, ensure_ascii=False, indent=1)) \
                  .replace("/*__TITLE__*/", html.escape(page_title))
    Path(out).write_text(out_html, encoding="utf-8")
    print(f"OK: {out} gerado ({len(cards)} cards, {len(warns)} aviso(s)).")



def check_flow(c, tag, w, h, content_h, icons, errors, warns):
    if "nodes" not in c or "edges" not in c:
        errors.append(f"{tag}: card 'flow' precisa de 'nodes' e 'edges'.")
        return
    bottom = h - (48 if c.get("caption") else 16)
    nodes = {}
    for n in c["nodes"]:
        nt = f"{tag}, nó '{n.get('id')}'"
        if any(k not in n for k in ("id", "x", "y", "w", "h", "label")):
            errors.append(f"{nt}: precisa de id, x, y, w, h e label.")
            continue
        if n["id"] in nodes:
            errors.append(f"{nt}: id repetido.")
        nodes[n["id"]] = n
        if n.get("icon") and n["icon"] not in icons:
            errors.append(f"{nt}: ícone '{n['icon']}' não existe. Disponíveis: {', '.join(sorted(icons))}.")
        if n.get("variant") not in (None, "", "core", "ok", "bad", "warn"):
            errors.append(f"{nt}: variant deve ser core, ok, bad ou warn.")
        if n["x"] < 10 or n["x"] + n["w"] > w - 10 or n["y"] < CARD_HEAD or n["y"] + n["h"] > bottom:
            errors.append(f"{nt}: fora da área de conteúdo (x 10–{w-10}, y {CARD_HEAD}–{bottom}).")
        col = bool(n.get("icon")) and n["h"] >= 58
        need = text_w(n["label"], 15) + 18 + (0 if col or not n.get("icon") else 26)
        if need > n["w"]:
            warns.append(f"{nt}: rótulo '{n['label']}' não cabe (precisa ~{int(need)}px, tem {n['w']}). Aumente w ou encurte.")
        if n.get("sub") and not col:
            warns.append(f"{nt}: 'sub' só aparece bem em nós com ícone e h >= 70.")
    ids = list(nodes)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = nodes[ids[i]], nodes[ids[j]]
            if a["x"] < b["x"] + b["w"] + 8 and b["x"] < a["x"] + a["w"] + 8 and a["y"] < b["y"] + b["h"] + 8 and b["y"] < a["y"] + a["h"] + 8:
                errors.append(f"{tag}: nós '{a['id']}' e '{b['id']}' se sobrepõem ou ficam colados.")
    graph = {k: [] for k in nodes}
    for e in c["edges"]:
        if not isinstance(e, list) or len(e) < 2:
            errors.append(f"{tag}: aresta inválida {e!r}.")
            continue
        f, t = e[0], e[1]
        opt = e[2] if len(e) > 2 else {}
        if f not in nodes or t not in nodes:
            errors.append(f"{tag}: aresta {f}→{t} cita nó inexistente.")
            continue
        if opt.get("color") not in (None, "bad", "ok"):
            errors.append(f"{tag}: aresta {f}→{t}: color deve ser 'bad' ou 'ok'.")
        a, b = nodes[f], nodes[t]
        if opt.get("loop"):
            ly = max(a["y"] + a["h"], b["y"] + b["h"]) + opt.get("drop", 50)
            if ly > bottom:
                errors.append(f"{tag}: o laço {f}→{t} desce até y={ly}, passando do limite {bottom}. Diminua 'drop' ou suba os nós.")
            continue
        graph[f].append(t)
        dx = (b["x"] + b["w"] / 2) - (a["x"] + a["w"] / 2)
        dy = (b["y"] + b["h"] / 2) - (a["y"] + a["h"] / 2)
        if abs(dx) >= abs(dy) * 0.8:
            gap = (b["x"] - (a["x"] + a["w"])) if dx > 0 else (a["x"] - (b["x"] + b["w"]))
        else:
            gap = (b["y"] - (a["y"] + a["h"])) if dy > 0 else (a["y"] - (b["y"] + b["h"]))
        if gap < 16:
            warns.append(f"{tag}: seta {f}→{t} curta demais ({gap}px). Deixe 20px ou mais entre os nós.")
    state = {}
    def dfs(u):
        state[u] = 1
        for v in graph[u]:
            if state.get(v) == 1 or (state.get(v) is None and dfs(v)):
                return True
        state[u] = 2
        return False
    if any(state.get(k) is None and dfs(k) for k in graph):
        errors.append(f"{tag}: há um ciclo. Marque a aresta de retorno com {{\"loop\": true}}.")


def check_list(c, tag, w, h, content_h, icons, errors, warns):
    items = c.get("items")
    if not items or not all(isinstance(i, dict) and i.get("text") for i in items):
        errors.append(f"{tag}: card 'list' precisa de 'items' como [{{\"text\": \"...\"}}, ...].")
        return
    if len(items) > 7:
        warns.append(f"{tag}: {len(items)} itens é muito; use até 6.")
    row = min(70, content_h / len(items))
    if row < 40:
        warns.append(f"{tag}: itens ficam baixos demais ({int(row)}px). Aumente h ou reduza itens.")
    for it in items:
        if it.get("icon") and it["icon"] not in icons:
            errors.append(f"{tag}: ícone '{it['icon']}' não existe.")
        if it.get("variant") not in (None, "", "ok", "bad", "warn"):
            errors.append(f"{tag}: variant de item deve ser ok, bad ou warn.")
        fs = min(17, (min(56, row - 10)) * 0.36)
        if text_w(it["text"], fs) > w - 36 - 28 - 36 - (text_w(it.get("note", ""), fs - 4, 600) + 10 if it.get("note") else 0):
            warns.append(f"{tag}: item '{it['text']}' longo; a fonte será reduzida. Encurte se puder.")


def check_stat(c, tag, w, h, content_h, icons, errors, warns):
    if not isinstance(c.get("value"), (int, float)):
        errors.append(f"{tag}: card 'stat' precisa de 'value' numérico (use prefix/suffix para símbolos, ex.: suffix \"%\").")
    if c.get("label") and text_w(c["label"], 24) > w - 46:
        warns.append(f"{tag}: label longo; a fonte será reduzida. Prefira até ~{int((w-46)/13)} caracteres.")
    if content_h < 150:
        warns.append(f"{tag}: card baixo para um número grande; use h >= 260.")


def check_bars(c, tag, w, h, content_h, icons, errors, warns):
    items = c.get("items")
    if not items or not all(isinstance(i, dict) and "label" in i and isinstance(i.get("value"), (int, float)) for i in items):
        errors.append(f"{tag}: card 'bars' precisa de 'items' como [{{\"label\": \"...\", \"value\": 10}}, ...].")
        return
    if len(items) > 7:
        warns.append(f"{tag}: {len(items)} barras é muito; use até 6.")
    if not any(i.get("highlight") for i in items):
        warns.append(f"{tag}: marque a barra principal com \"highlight\": true para ela ganhar a cor.")


def check_compare(c, tag, w, h, content_h, icons, errors, warns):
    for side in ("left", "right"):
        S = c.get(side)
        if not isinstance(S, dict) or not S.get("title") or not S.get("items"):
            errors.append(f"{tag}: card 'compare' precisa de '{side}' com 'title' e 'items'.")
            return
        if S.get("variant") not in (None, "", "ok", "bad", "warn"):
            errors.append(f"{tag}: {side}.variant deve ser ok, bad ou warn.")
        if S.get("icon") and S["icon"] not in icons:
            errors.append(f"{tag}: ícone '{S['icon']}' não existe.")
        col_w = (w - 36 - 18) / 2
        for txt in S["items"]:
            if text_w(txt, 16) > col_w - 52:
                warns.append(f"{tag}: '{txt}' longo para a coluna; a fonte será reduzida.")
    n = max(len(c["left"]["items"]), len(c["right"]["items"]))
    if n > 5:
        warns.append(f"{tag}: {n} linhas por coluna é muito; use até 4.")


def check_text(c, tag, w, h, content_h, icons, errors, warns):
    if not c.get("text"):
        errors.append(f"{tag}: card 'text' precisa de 'text'.")
        return
    words = len(c["text"].split())
    if words > 30:
        warns.append(f"{tag}: {words} palavras é muito para uma frase de impacto; use até ~20.")
    if c["text"].count("*") % 2:
        errors.append(f"{tag}: asteriscos desbalanceados em 'text' (use *trecho destacado*).")


CHECKS = {"flow": check_flow, "list": check_list, "stat": check_stat, "bars": check_bars, "compare": check_compare, "text": check_text}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
