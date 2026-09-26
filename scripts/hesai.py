import struct, numpy as np
XT32_EL = np.deg2rad(15 - np.arange(32, dtype=float))
def load_at128_corr(path):
    b = open(path, 'rb').read()
    assert b[:2] == b'\xee\xff' and b[4] == 128
    nm = b[5]; o = 16
    start = np.array(struct.unpack_from(f'<{nm}H', b, o)); o += 2 * nm
    end = np.array(struct.unpack_from(f'<{nm}H', b, o)); o += 2 * nm
    az = np.array(struct.unpack_from('<128h', b, o)); o += 256
    el = np.array(struct.unpack_from('<128h', b, o))
    return dict(start=start, end=end, az=az, el=el)

def xt32_points(pl, first_return_only=True):
    unit = pl[9] * 1e-3
    out = []
    for blk in range(8):
        if first_return_only and pl[10] == 2 and blk % 2: continue
        o = 12 + blk * 130
        az = np.deg2rad(struct.unpack_from('<H', pl, o)[0] / 100)
        rec = np.frombuffer(pl, np.dtype([('d', '<u2'), ('r', 'u1'), ('x', 'u1')]), 32, o + 2)
        d = rec['d'] * unit; m = d > 0.4
        out.append(np.stack([d * np.cos(XT32_EL) * np.sin(az), d * np.cos(XT32_EL) * np.cos(az), d * np.sin(XT32_EL)], 1)[m])
    return np.concatenate(out)

def at128_points(pl, C, first_return_only=True):
    """AT128 protocol 4.3. Each mirror face sweeps +/-30 deg of encoder angle around the start_frame
    boundaries in the v1.3 correction file, giving a 120 deg optical field: az = 2*(raw - nearest start) - az_corr.
    Per-channel fine adjustment tables (azimuth/elevation offsets) are ignored (< ~0.5 deg)."""
    unit = pl[9] * 1e-3
    out = []
    for blk in range(1 if (first_return_only and pl[10] == 2) else 2):
        o = 12 + blk * 515
        raw = struct.unpack_from('<H', pl, o)[0]  # 0.01 deg
        rec = np.frombuffer(pl, np.dtype([('d', '<u2'), ('r', 'u1'), ('c', 'u1')]), 128, o + 3)
        diff = (raw - C['start'] + 18000) % 36000 - 18000     # signed distance to each start
        k = int(np.argmin(np.abs(diff)))
        azc = diff[k] * 2 - C['az']                              # 0.01 deg, 0 = straight ahead
        az = np.deg2rad(azc / 100.0); el = np.deg2rad(C['el'] / 100.0)
        d = rec['d'] * unit; m = d > 0.4
        out.append(np.stack([d * np.cos(el) * np.sin(az), d * np.cos(el) * np.cos(az), d * np.sin(el)], 1)[m])
    return np.concatenate(out)
