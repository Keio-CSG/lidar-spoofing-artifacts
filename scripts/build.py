import os, re, sys, json, struct, hashlib, zipfile, subprocess, datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from manifest import SETS, SETUP_IMAGES, PAPERS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "docs"); MEDIA = os.path.join(SITE, "media")
REL = os.path.join(ROOT, "release")
FF = r"C:\Users\kyosh\miniconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
os.makedirs(MEDIA, exist_ok=True); os.makedirs(REL, exist_ok=True)

EL16 = np.deg2rad([-15, 1, -13, 3, -11, 5, -9, 7, -7, 9, -5, 11, -3, 13, -1, 15] * 2)
EL32 = np.deg2rad([-25, -1, -1.667, -15.639, -11.31, 0, -0.667, -8.843, -7.254, 0.333, -0.333, -6.148, -5.333, 1.333, 0.667, -4,
                   -4.667, 1.667, 1, -3.667, -3.333, 3.333, 2.333, -2.667, -3, 7, 4.667, -2.333, -2, 15, 10.333, -1.333])
MODEL = {0x22: "VLP-16", 0x28: "VLP-32C"}
RMODE = {0x37: "strongest", 0x38: "last", 0x39: "dual"}
REC = np.dtype([("d", "<u2"), ("i", "u1")])

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def read_pcap(path):
    raw = open(path, "rb").read()
    h = hashlib.sha256(raw).hexdigest()
    off = 24; ts = []; pls = []
    while off + 16 <= len(raw):
        s, us, incl, _ = struct.unpack_from("<IIII", raw, off); off += 16
        if incl == 1248: ts.append(s + us / 1e6); pls.append(raw[off + 42: off + 1248])
        off += incl
    return raw, h, np.array(ts), pls

def points(pl):
    pid, dual = pl[1205], pl[1204] == 0x39
    el = EL16 if pid == 0x22 else EL32; sc = 0.002 if pid == 0x22 else 0.004
    out = []
    for b in range(12):
        if dual and b % 2: continue
        o = b * 100
        az = np.deg2rad(struct.unpack_from("<H", pl, o + 2)[0] / 100)
        r = np.frombuffer(pl, REC, 32, o + 4)
        d = r["d"] * sc; m = d > 0.4
        out.append(np.stack([d * np.cos(el) * np.sin(az), d * np.cos(el) * np.cos(az), d * np.sin(el)], 1)[m])
    return np.concatenate(out) if out else np.zeros((0, 3))

def frame_points(ts, pls, t0, t1):
    i0, i1 = np.searchsorted(ts, t0), np.searchsorted(ts, t1)
    ps = [points(p) for p in pls[i0:i1]]
    return np.concatenate(ps) if ps else np.zeros((0, 3))

# height colormap: teal -> amber, VeloView-like on dark ground
CM = np.array([[40, 90, 200], [30, 170, 200], [90, 210, 140], [230, 210, 80], [245, 130, 60]], float)
def colorize(z):
    t = np.clip((z + 1.8) / 3.6, 0, 1) * (len(CM) - 1); i = np.minimum(t.astype(int), len(CM) - 2); f = (t - i)[:, None]
    return (CM[i] * (1 - f) + CM[i + 1] * f).astype(np.uint8)

FONT = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
W_, H_ = 800, 500
def render_bev(ts, pls, out_mp4, label, max_s=120):
    t0 = ts[0]; dur = min(ts[-1] - t0, max_s)
    # extent from first second of data
    P = frame_points(ts, pls, t0, t0 + 1.0); P = P[np.hypot(P[:, 0], P[:, 1]) < 22]
    x0, x1 = np.percentile(P[:, 0], [1.5, 98.5]); y0, y1 = np.percentile(P[:, 1], [1.5, 98.5])
    x0, x1, y0, y1 = min(x0, -1) - 1, max(x1, 1) + 1, min(y0, -1) - 1, max(y1, 1) + 1
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; sx, sy = x1 - x0, y1 - y0
    if sx / sy < W_ / H_: sx = sy * W_ / H_
    else: sy = sx * H_ / W_
    x0, y0 = cx - sx / 2, cy - sy / 2; ppm = W_ / sx
    base = Image.new("RGB", (W_, H_), (9, 14, 24)); d = ImageDraw.Draw(base)
    step = 1 if sx < 25 else 5
    for gx in np.arange(np.ceil(x0 / step) * step, x0 + sx, step):
        X = (gx - x0) * ppm; d.line([(X, 0), (X, H_)], fill=(22, 32, 48) if gx % 5 else (34, 48, 70))
    for gy in np.arange(np.ceil(y0 / step) * step, y0 + sy, step):
        Y = H_ - (gy - y0) * ppm; d.line([(0, Y), (W_, Y)], fill=(22, 32, 48) if gy % 5 else (34, 48, 70))
    sxp, syp = (0 - x0) * ppm, H_ - (0 - y0) * ppm
    d.ellipse([sxp - 5, syp - 5, sxp + 5, syp + 5], outline=(255, 255, 255))
    bl = 5 if sx > 12 else 1
    d.line([(16, H_ - 20), (16 + bl * ppm, H_ - 20)], fill=(200, 210, 225), width=2); d.text((16, H_ - 40), f"{bl} m", font=FONT, fill=(200, 210, 225))
    bg = np.asarray(base).copy()
    proc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W_}x{H_}", "-r", "10", "-i", "-",
                             "-c:v", "libx264", "-preset", "slow", "-crf", "30", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out_mp4], stdin=subprocess.PIPE)
    n = int(dur * 10)
    for k in range(n):
        P = frame_points(ts, pls, t0 + k * 0.1, t0 + (k + 1) * 0.1)
        img = bg.copy()
        if len(P):
            X = ((P[:, 0] - x0) * ppm).astype(int); Y = (H_ - (P[:, 1] - y0) * ppm).astype(int)
            m = (X >= 1) & (X < W_ - 1) & (Y >= 1) & (Y < H_ - 1); X, Y, C = X[m], Y[m], colorize(P[m, 2])
            o = np.argsort(P[m, 2]); X, Y, C = X[o], Y[o], C[o]
            for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)): img[Y + dy, X + dx] = C
        im = Image.fromarray(img); ImageDraw.Draw(im).text((16, 12), f"{label}   t = {k / 10:5.1f} s", font=FONT, fill=(225, 232, 242))
        proc.stdin.write(im.tobytes())
        if k == min(n - 1, int(n * 0.5)): im.save(out_mp4.replace(".mp4", ".jpg"), quality=82)
    proc.stdin.close(); proc.wait()

def transcode(src, dst, width, crf=31, max_s=None):
    vf = f"scale='min({width},iw)':-2,fps=30"
    args = [FF, "-v", "error", "-y", "-i", src] + (["-t", str(max_s)] if max_s else []) + ["-an", "-vf", vf, "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart", dst]
    subprocess.run(args, check=True)
    subprocess.run([FF, "-v", "error", "-y", "-ss", "3", "-i", dst, "-frames:v", "1", "-q:v", "4", dst.replace(".mp4", ".jpg")], check=True)

def main(only=None):
    dj = os.path.join(SITE, "data.json")
    prev = {s["id"]: s for s in json.load(open(dj, encoding="utf-8"))["sets"]} if only and os.path.exists(dj) else {}
    data = {"generated": datetime.date.today().isoformat(), "papers": PAPERS, "sets": []}
    for S in SETS:
        if only and S["id"] not in only:
            if S["id"] in prev:
                o = dict(prev[S["id"]], paper=S["paper"]); c = o.pop("camera", None)
                o.setdefault("cameras", [c] if c else []); data["sets"].append(o)
            continue
        sd = dict({k: v for k, v in S.items() if k not in ("caps", "camera")}, caps=[], cameras=[])
        cams = S.get("camera") or []
        for j, cam in enumerate([cams] if isinstance(cams, str) else cams):
            fn = f"{S['id']}__camera{j or ''}.mp4"; transcode(cam, os.path.join(MEDIA, fn), 720, crf=32)
            sd["cameras"].append({"video": "media/" + fn, "source": os.path.basename(cam)})
        os.makedirs(os.path.join(REL, S["id"]), exist_ok=True)
        for c in S["caps"]:
            name = os.path.splitext(os.path.basename(c["pcap"]))[0].strip().replace("&", "and").replace(" ", "_")
            print("->", S["id"], name, flush=True)
            raw, h, ts, pls = read_pcap(c["pcap"])
            info = dict(role=c["role"], label=c["label"], file=name + ".pcap", bytes=len(raw), sha256=h, packets=len(pls),
                        start=datetime.datetime.fromtimestamp(ts[0]).strftime("%Y-%m-%d %H:%M:%S"), duration=round(float(ts[-1] - ts[0]), 1),
                        model=MODEL.get(pls[0][1205], hex(pls[0][1205])), mode=RMODE.get(pls[0][1204], hex(pls[0][1204])),
                        source=os.path.relpath(c["pcap"], os.path.dirname(os.path.dirname(c["pcap"]))).replace("\\", "/"))
            zp = os.path.join(REL, S["id"], name + ".zip")
            if not os.path.exists(zp):
                with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z: z.writestr(name + ".pcap", raw)
            info["zip"] = f"{S['id']}/{name}.zip"; info["zip_bytes"] = os.path.getsize(zp)
            bev = f"{S['id']}__{slug(name)}__bev.mp4"
            render_bev(ts, pls, os.path.join(MEDIA, bev), f"{info['model']} · {c['label']}")
            info["bev"] = "media/" + bev
            if c.get("video"):
                fn = f"{S['id']}__{slug(name)}__rec.mp4"; transcode(c["video"], os.path.join(MEDIA, fn), 960)
                info["video"] = "media/" + fn; info["video_source"] = os.path.basename(c["video"])
            sd["caps"].append(info)
            del raw, pls
        data["sets"].append(sd)
    for i, s in enumerate(SETUP_IMAGES):
        im = Image.open(s).convert("RGB"); im.thumbnail((1200, 1200)); im.save(os.path.join(MEDIA, f"setup{i}.jpg"), quality=80)
    json.dump(data, open(os.path.join(SITE, "data.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main(sys.argv[1:] or None)
