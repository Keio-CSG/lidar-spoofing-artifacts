# LiDAR spoofing — raw captures

Velodyne VLP-16 / VLP-32C and Hesai AT128 / XT32 packet captures (pcap) and videos from the physical experiments in

- *LiDAR Spoofing Meets the New-Gen: Capability Improvements, Broken Assumptions, and New Attack Strategies* (NDSS 2024) —
  Chosen Pattern Injection (CPI), the synchronized Physical Removal Attack (PRA) and High-Frequency Removal (HFR), in static and dynamic scenes
- *On the Realism of LiDAR Spoofing Attacks against Autonomous Driving Vehicle at High Speed and Long Distance* (NDSS 2025) —
  injection against a vehicle-mounted VLP-32C driving past the Moving Vehicle Spoofing (MVS) system, and adaptive HFR (A-HFR)
  against the pulse-fingerprinting Hesai AT128 / XT32, including an AT128 on a vehicle at 10–60 km/h
- *SLAMSpoof: Practical LiDAR Spoofing Attacks on Localization Systems Guided by Scan Matching Vulnerability Analysis* (ICRA 2025) —
  removal and fake-wall injection on a VLP-16, plus videos of the physical attack on a moving WHILL (separate page: `docs/icra25.html`)

Benign references are included where they were recorded.

## Layout

```
scripts/manifest.py        which pcap / video belongs to which experiment (source paths on the lab shared drive)
scripts/build.py           reads each pcap -> metadata + SHA-256, zips it into release/, renders a bird's-eye mp4,
                           transcodes recorded / camera videos into docs/media/
scripts/page.template.html page template; scripts/build_page.py injects docs/data.json -> docs/index.html
scripts/hesai.py           Hesai XT32 / AT128 packet decoding (AT128 uses its angle-correction file)
scripts/release_assets.py  per-paper SHA256SUMS / release notes
scripts/pcapinfo.py        quick pcap inspector (model, return mode, duration)
docs/                      static website (GitHub Pages-ready): index.html, data.json, media/
release/                   one zip per pcap (not in git; attached to the GitHub Release)
```

## Rebuild

```
pip install numpy pillow imageio-ffmpeg
python scripts/build.py                 # all experiments (or pass experiment ids)
python scripts/build_page.py --repo https://github.com/Keio-CSG/lidar-spoofing-artifacts --ga G-QYEN5RGBVF --papers ndss24,ndss25 --nav "SLAMSpoof (ICRA 2025) captures →=icra25.html"
python scripts/build_page.py --repo https://github.com/Keio-CSG/lidar-spoofing-artifacts --ga G-QYEN5RGBVF --papers icra25 --title "SLAMSpoof Captures" --out docs/icra25.html --nav "NDSS 2024 / 2025 captures →=index.html"
                                        # --repo enables download links (<repo>/releases/download/<tag>/<file>.zip)
```

Each zip contains a single unmodified pcap; the SHA-256 on the site is that of the pcap.

## Downloads

NDSS 2024 pcaps: [v1.0 release](https://github.com/Keio-CSG/lidar-spoofing-artifacts/releases/tag/v1.0). NDSS 2025 pcaps (and the AT128 angle-correction file): [ndss25-v1.0 release](https://github.com/Keio-CSG/lidar-spoofing-artifacts/releases/tag/ndss25-v1.0). ICRA 2025 pcaps: [icra25-v1.0 release](https://github.com/Keio-CSG/lidar-spoofing-artifacts/releases/tag/icra25-v1.0). Browse them with videos at https://keio-csg.github.io/lidar-spoofing-artifacts/.
