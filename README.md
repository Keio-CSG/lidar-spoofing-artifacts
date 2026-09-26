# New-Gen LiDAR Spoofing — raw captures

Velodyne VLP-16 / VLP-32C packet captures (pcap) and videos from the physical experiments in
*LiDAR Spoofing Meets the New-Gen: Capability Improvements, Broken Assumptions, and New Attack Strategies* (NDSS 2024):
Chosen Pattern Injection (CPI), the synchronized Physical Removal Attack (PRA), and High-Frequency Removal (HFR), in static and dynamic scenes, with benign references where they were recorded.

## Layout

```
scripts/manifest.py        which pcap / video belongs to which experiment (source paths on the lab shared drive)
scripts/build.py           reads each pcap -> metadata + SHA-256, zips it into release/, renders a bird's-eye mp4,
                           transcodes recorded / camera videos into docs/media/
scripts/page.template.html page template; scripts/build_page.py injects docs/data.json -> docs/index.html
scripts/pcapinfo.py        quick pcap inspector (model, return mode, duration)
docs/                      static website (GitHub Pages-ready): index.html, data.json, media/
release/                   one zip per pcap (not in git; attached to the GitHub Release)
```

## Rebuild

```
pip install numpy pillow imageio-ffmpeg
python scripts/build.py                 # all experiments (or pass experiment ids)
python scripts/build_page.py [BASE_URL] [--ga G-XXXX]  # BASE_URL + "<file>.zip" becomes each download link; --ga adds GA4
```

Each zip contains a single unmodified pcap; the SHA-256 on the site is that of the pcap.

## Downloads

All pcaps are attached to the [v1.0 release](https://github.com/Keio-CSG/lidar-spoofing-artifacts/releases/tag/v1.0). Browse them with videos at https://keio-csg.github.io/lidar-spoofing-artifacts/.
