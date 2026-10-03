#!/usr/bin/env python3
"""Gera imagens de conferência do vídeo (visão geral + cada cena + fechamento).

Uso:
    python3 preview.py video.html pasta_saida/

Requer Playwright com Chromium. Saída: overview.png, cena-1.png ... e contact.png
(uma folha com todas as imagens lado a lado, para revisar de uma vez).
Fontes: se "Inter Tight" não estiver instalada, a prévia usa uma fonte substituta
e os textos podem parecer um pouco mais largos do que no navegador do usuário.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

src, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
MUXER = Path(__file__).resolve().parent.parent / "assets" / "mp4-muxer.js"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1450})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    # sem rede: serve a biblioteca localmente e ignora as fontes remotas
    pg.route("**/mp4-muxer.js", lambda r: r.fulfill(path=str(MUXER), content_type="application/javascript") if MUXER.exists() else r.abort())
    pg.route("**fonts.googleapis.com**", lambda r: r.abort())
    pg.goto(src.as_uri())
    pg.wait_for_timeout(700)
    pg.evaluate("setPlaying(false); document.body.classList.add('rec'); fit();")
    n = pg.evaluate("scenes.length")
    shots = [("overview", "INTRO-0.2")] + [(f"cena-{i+1}", f"scenes[{i}].start+0.7+cards[{i}].buildEnd+0.25") for i in range(n)] + [("fechamento", "TOTAL-0.2")]
    files = []
    for name, expr in shots:
        pg.evaluate(f"t={expr}; draw()")
        f = out / f"{name}.png"
        pg.locator("#stage").screenshot(path=str(f))
        files.append(f)
    b.close()

try:
    from PIL import Image
    ims = [Image.open(f) for f in files]
    th = 540
    ims = [im.resize((int(im.width * th / im.height), th)) for im in ims]
    cols = 4
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * ims[0].width, rows * th), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * ims[0].width, (i // cols) * th))
    sheet.save(out / "contact.png")
except ImportError:
    pass

print("Erros de JavaScript:", errs if errs else "nenhum")
print("Imagens em", out)
