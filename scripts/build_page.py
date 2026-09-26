"""Inject docs/data.json into the page template -> docs/index.html.
Usage: python scripts/build_page.py [--repo https://github.com/OWNER/REPO] [--ga G-XXXXXXX] [--out PATH]
--repo turns on download links: <repo>/releases/download/<paper release tag>/<file>.zip
--ga adds a Google Analytics 4 tag (GitHub Pages build only; the claude.ai artifact CSP blocks it)."""
import argparse, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("--repo", default="")
ap.add_argument("--ga", default="")
ap.add_argument("--out", default=os.path.join(ROOT, "docs", "index.html"))
a = ap.parse_args()
data = json.load(open(os.path.join(ROOT, "docs", "data.json"), encoding="utf-8"))
html = open(os.path.join(ROOT, "scripts", "page.template.html"), encoding="utf-8").read()
html = html.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False)).replace('/*REPO*/""', json.dumps(a.repo.rstrip("/")))
if a.ga:
    tag = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={a.ga}"></script>\n'
           f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{a.ga}');</script>\n")
    html = html.replace("</title>\n", "</title>\n" + tag, 1)
open(a.out, "w", encoding="utf-8").write(html)
print("wrote", a.out, len(html), "bytes")
