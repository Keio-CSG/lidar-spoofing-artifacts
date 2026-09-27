#!/bin/sh
# Build the three GitHub Pages pages (one per paper) from docs/data.json.
cd "$(dirname "$0")/.."
R=https://github.com/Keio-CSG/lidar-spoofing-artifacts; GA=G-QYEN5RGBVF
N24="NDSS 2024 captures →=index.html"; N25="NDSS 2025 captures →=ndss25.html"; NI="SLAMSpoof (ICRA 2025) captures →=icra25.html"
python scripts/build_page.py --repo $R --ga $GA --papers ndss24 --nav "$N25" --nav "$NI"
python scripts/build_page.py --repo $R --ga $GA --papers ndss25 --title "High-Speed LiDAR Spoofing Captures" --out docs/ndss25.html --nav "$N24" --nav "$NI"
python scripts/build_page.py --repo $R --ga $GA --papers icra25 --title "SLAMSpoof Captures" --out docs/icra25.html --nav "$N24" --nav "$N25"
