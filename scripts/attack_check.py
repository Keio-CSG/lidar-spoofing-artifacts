"""Quantify whether a removal attack actually removed points in each capture.

For every 0.1 s frame, returns are histogrammed over 1-degree azimuth bins inside the sensor's field of view.
A bin is "empty" when it holds under 10 % of that bin's median count (over the benign capture of the same
static scene, or over the capture itself; the stronger of the two is kept); the frame's
gap is the widest run of consecutive empty bins. A successful HFR / A-HFR attack shows up as a sustained gap
several degrees wide in the direction of the spoofer, which benign captures do not have.

Usage: python scripts/attack_check.py [set_id ...]   (default: every AT128 / XT32 set)
Writes docs/attack_check.json and prints a table.
"""
import json, os, struct, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from manifest import SETS, AT128_CORR
from hesai import load_at128_corr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAP_DEG = 8


def payloads(path, size):
    raw = open(path, "rb").read()
    off = 24; ts = []; pl = []
    while off + 16 <= len(raw):
        s, us, incl, _ = struct.unpack_from("<IIII", raw, off); off += 16
        if incl - 42 == size and raw[off + 42: off + 44] == b"\xee\xff":
            ts.append(s + us / 1e6); pl.append(raw[off + 42: off + incl])
        off += incl
    return np.array(ts), np.frombuffer(b"".join(pl), np.uint8).reshape(len(pl), size)


def at128_az_valid(P, C):
    """per-packet first-block azimuth (deg, per channel) and valid mask."""
    raw = P[:, 12].astype(np.int32) | (P[:, 13].astype(np.int32) << 8)
    diff = (raw[:, None] - C["start"][None, :] + 18000) % 36000 - 18000
    k = np.argmin(np.abs(diff), 1); d = diff[np.arange(len(raw)), k]
    az = (d[:, None] * 2 - C["az"][None, :]) / 100.0                       # (n, 128)
    rec = P[:, 15:15 + 512].reshape(-1, 128, 4)
    dist = (rec[:, :, 0].astype(np.int32) | (rec[:, :, 1].astype(np.int32) << 8)) * P[:, 9:10] * 1e-3
    return az, dist > 0.4


def xt32_az_valid(P):
    az_list, ok_list = [], []
    for blk in range(0, 8, 2 if P[0, 10] == 2 else 1):                     # first return only
        o = 12 + blk * 130
        az = (P[:, o].astype(np.int32) | (P[:, o + 1].astype(np.int32) << 8)) / 100.0
        rec = P[:, o + 2: o + 130].reshape(-1, 32, 4)
        dist = (rec[:, :, 0].astype(np.int32) | (rec[:, :, 1].astype(np.int32) << 8)) * P[:, 9:10] * 1e-3
        az_list.append(np.repeat(((az + 180) % 360 - 180)[:, None], 32, 1)); ok_list.append(dist > 0.4)
    return np.concatenate(az_list, 1), np.concatenate(ok_list, 1)


def histogram(path, model, C):
    if model == "AT128":
        ts, P = payloads(path, 1118); az, ok = at128_az_valid(P, C); lo, hi = -60, 60
    else:
        ts, P = payloads(path, 1080); az, ok = xt32_az_valid(P); lo, hi = -180, 180
    frame = ((ts - ts[0]) / 0.1).astype(int); nf = frame[-1] + 1
    bins = np.clip(((az - lo)).astype(int), 0, hi - lo - 1)
    H = np.zeros((nf, hi - lo))
    np.add.at(H, (np.repeat(frame[:, None], az.shape[1], 1)[ok], bins[ok]), 1)
    return H[1:-1]                                                          # drop partial first/last frame


def analyse(H, ref=None):
    """ref: histogram of the benign capture of a static scene; otherwise the capture is its own reference."""
    med = np.median(H if ref is None else ref, 0); active = med > 20        # bins that normally see returns
    empty = (H < 0.1 * med) & active
    gaps = np.zeros(len(H), int)
    for i, row in enumerate(empty):
        run = best = 0
        for v in row:
            run = run + 1 if v else 0; best = max(best, run)
        gaps[i] = best
    hit = gaps >= GAP_DEG
    streak = best = 0
    for v in hit:
        streak = streak + 1 if v else 0; best = max(best, streak)
    return dict(frames=int(len(H)), attacked_pct=round(100 * hit.mean(), 1), longest_s=round(best / 10, 1),
                median_gap_deg=int(np.median(gaps)), p90_gap_deg=int(np.percentile(gaps, 90)))


def main(ids):
    C = load_at128_corr(AT128_CORR)
    out_path = os.path.join(ROOT, "docs", "attack_check.json")
    res = json.load(open(out_path)) if os.path.exists(out_path) else {}
    for S in SETS:
        if ids and S["id"] not in ids: continue
        if not ids and S.get("lidar") not in ("AT128", "XT32"): continue
        static = "static" in S["scene"].lower()
        hists = {c["pcap"]: histogram(c["pcap"], S["lidar"], C) for c in S["caps"]}
        ref = next((hists[c["pcap"]] for c in S["caps"] if c["role"] == "benign"), None) if static else None
        for c in S["caps"]:
            name = os.path.splitext(os.path.basename(c["pcap"]))[0]
            cands = [dict(analyse(hists[c["pcap"]]), reference="self")]
            if ref is not None: cands.append(dict(analyse(hists[c["pcap"]], ref), reference="benign"))
            r = max(cands, key=lambda x: (x["longest_s"], x["attacked_pct"]))   # both references; keep the stronger evidence
            r.update(set=S["id"], role=c["role"], label=c["label"])
            res[name] = r
            print(f"{S['id']:24s} {c['role']:6s} {c['label']:28s} attacked {r['attacked_pct']:5.1f}%  longest {r['longest_s']:5.1f}s  "
                  f"gap med/p90 {r['median_gap_deg']:3d}/{r['p90_gap_deg']:3d} deg  ({r['frames']} frames)", flush=True)
            json.dump(res, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
