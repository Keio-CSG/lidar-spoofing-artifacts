#!/bin/sh
# Build the three GitHub Pages pages (one per paper) from docs/data.json.
cd "$(dirname "$0")/.."
R=https://github.com/Keio-CSG/lidar-spoofing-artifacts; GA=G-QYEN5RGBVF
N24="ndss24=index.html"; N25="ndss25=ndss25.html"; NI="icra25=icra25.html"   # paper key=page
python scripts/build_page.py --repo $R --ga $GA --papers ndss24 --nav "$N25" --nav "$NI"
python scripts/build_page.py --repo $R --ga $GA --papers ndss25 --title "High-Speed LiDAR Spoofing Captures" --out docs/ndss25.html --nav "$N24" --nav "$NI"
python scripts/build_page.py --repo $R --ga $GA --papers icra25 --title "SLAMSpoof Captures" --out docs/icra25.html --nav "$N24" --nav "$N25"
