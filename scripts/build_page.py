"""Inject docs/data.json into the page template -> docs/index.html.
Usage: python scripts/build_page.py [RELEASE_BASE_URL]
RELEASE_BASE_URL is the prefix each zip file name is appended to, e.g.
https://github.com/Keio-CSG/lidar-spoofing-artifacts/releases/download/v1.0/"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(ROOT, "docs", "data.json"), encoding="utf-8"))
tpl = open(os.path.join(ROOT, "scripts", "page.template.html"), encoding="utf-8").read()
base = sys.argv[1] if len(sys.argv) > 1 else ""
html = tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False)).replace('/*RELEASE_BASE*/""', json.dumps(base))
open(os.path.join(ROOT, "docs", "index.html"), "w", encoding="utf-8").write(html)
print("wrote docs/index.html", len(html), "bytes")
