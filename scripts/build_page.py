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
ap.add_argument("--papers", default="", help="comma-separated paper keys to include (default: all)")
ap.add_argument("--title", default="")
ap.add_argument("--nav", action="append", default=[], help="PAPER_KEY=HREF (or LABEL=HREF) link to a sibling page, shown with the paper's badge and title (repeatable)")
a = ap.parse_args()
data = json.load(open(os.path.join(ROOT, "docs", "data.json"), encoding="utf-8"))
if a.papers:
    keep = a.papers.split(","); data["sets"] = [x for x in data["sets"] if x["paper"] in keep]
chk_path = os.path.join(ROOT, "docs", "attack_check.json")
chk = json.load(open(chk_path, encoding="utf-8")) if os.path.exists(chk_path) else {}
for x in data["sets"]:
    for c in x["caps"]:
        r = chk.get(c["file"][:-5])
        if r: c["check"] = {k: r[k] for k in ("attacked_pct", "longest_s", "p90_gap_deg")}
data["nav"] = [dict(label=n.split("=", 1)[0], href=n.split("=", 1)[1]) for n in a.nav]
html = open(os.path.join(ROOT, "scripts", "page.template.html"), encoding="utf-8").read()
if a.title: html = html.replace("<title>New-Gen LiDAR Spoofing Captures</title>", f"<title>{a.title}</title>", 1)
html = html.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False)).replace('/*REPO*/""', json.dumps(a.repo.rstrip("/")))
if a.ga:
    tag = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={a.ga}"></script>\n'
           f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{a.ga}');</script>\n")
    html = html.replace("</title>\n", "</title>\n" + tag, 1)
open(a.out, "w", encoding="utf-8").write(html)
print("wrote", a.out, len(html), "bytes")
