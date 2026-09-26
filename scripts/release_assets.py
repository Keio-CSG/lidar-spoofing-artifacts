"""Write release/<paper>/{SHA256SUMS.txt, NOTES.md, files.txt} for one paper's GitHub release.
Usage: python scripts/release_assets.py ndss25"""
import hashlib, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
key = sys.argv[1]
d = json.load(open(os.path.join(ROOT, "docs", "data.json"), encoding="utf-8"))
paper = d["papers"][key]
out = os.path.join(ROOT, "release", key); os.makedirs(out, exist_ok=True)
sums = ["# SHA-256 of each pcap (inside its zip) and of the zip itself", "# pcap_sha256  zip_sha256  zip  experiment  role  label"]
notes = [f"Raw LiDAR captures from the physical experiments of *{paper['title']}* ({paper['short']}). Each zip holds one unmodified pcap (UDP 2368). "
         "Browse them with videos: https://keio-csg.github.io/lidar-spoofing-artifacts/", "",
         "| Experiment | Role | Capture | LiDAR | Length | File |", "|---|---|---|---|---|---|"]
files = []
for s in d["sets"]:
    if s["paper"] != key: continue
    for c in s["caps"]:
        z = os.path.join(ROOT, "release", c["zip"]); n = os.path.basename(z); files.append(os.path.relpath(z, ROOT).replace("\\", "/"))
        zh = hashlib.sha256(open(z, "rb").read()).hexdigest()
        sums.append(f"{c['sha256']}  {zh}  {n}  {s['id']}  {c['role']}  {c['label']}")
        notes.append(f"| {s['title']} | {c['role']} | {c['label']} | {c['model']} ({c['mode']}) | {c['duration']} s | `{n}` |")
notes += ["", "`SHA256SUMS.txt` lists the SHA-256 of every pcap and zip."]
if any(c["model"] == "AT128" for s in d["sets"] if s["paper"] == key for c in s["caps"]):
    notes.append("`AT128E2X_Angle_Correction_File.dat` is the angle-correction file of the AT128 used in these captures.")
with open(os.path.join(out, "SHA256SUMS.txt"), "w", encoding="utf-8", newline="\n") as f: f.write("\n".join(sums) + "\n")
with open(os.path.join(out, "NOTES.md"), "w", encoding="utf-8", newline="\n") as f: f.write("\n".join(notes) + "\n")
with open(os.path.join(out, "files.txt"), "w", encoding="utf-8", newline="\n") as f: f.write("\n".join(files) + "\n")
print(key, len(files), "zips")
