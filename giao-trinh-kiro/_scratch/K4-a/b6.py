# [đã chạy] Bài 6: đồ chơi PL1/PL2 + nhiệt — "nhiệt độ phẳng" không chứng minh "tần số phẳng"
import numpy as np
rng = np.random.default_rng(3)
# GIẢ ĐỊNH (không phải spec của máy bạn): P = k·f³; PL2 = 25 W, PL1 = 12 W, tau = 28 s; Rth = 2.5 °C/W, tau nhiệt = 40 s
F_MAX, PL1, PL2, TAU, K = 3.4, 12.0, 25.0, 28.0, 25.0 / 3.4**3
RTH, TAU_TH, T_AMB, P_IDLE, WORK = 2.5, 40.0, 30.0, 2.0, 0.6   # WORK: giga-chu kỳ mỗi inference
DT = 0.002

class Box:
    def __init__(s): s.ewma, s.T, s.t = P_IDLE, T_AMB + RTH * P_IDLE, 0.0
    def step(s, busy):
        f = F_MAX if busy else 0.8
        if busy and s.ewma >= PL1: f = min(F_MAX, (PL1 / K) ** (1 / 3))   # bị kẹp theo công suất
        P = K * f**3 if busy else P_IDLE
        s.ewma += (P - s.ewma) * DT / TAU
        s.T += ((T_AMB + RTH * P) - s.T) * DT / TAU_TH
        s.t += DT
        return f
    def idle(s, sec):
        for _ in range(int(sec / DT)): s.step(False)
    def session(s, n_iter, warm=20):
        lat, temp, freq = [], [], []
        for _ in range(n_iter + warm):
            done, el = 0.0, 0.0
            while done < WORK:
                f = s.step(True); done += f * DT; el += DT
            lat.append(el * 1e3 * rng.lognormal(0, 0.02)); temp.append(s.T); freq.append(f)
        return np.array(lat[warm:]), np.array(temp[warm:]), np.array(freq[warm:])

box = Box(); box.idle(600)
res = {}
res["S1 máy nguội"] = box.session(300)
res["S2 chạy ngay sau S1"] = box.session(300)
box.idle(300); res["S3 sau 5 phút nghỉ"] = box.session(300)
for name, (lat, T, f) in res.items():
    print(f"{name:20s}: p10={np.percentile(lat,10):4.0f} p50={np.median(lat):5.0f} ms  p99={np.percentile(lat,99):5.0f}  "
          f"T∈[{T.min():.1f},{T.max():.1f}] °C  f∈[{f.min():.2f},{f.max():.2f}] GHz  "
          f"50 lần đầu p50={np.median(lat[:50]):.0f} / 50 lần cuối p50={np.median(lat[-50:]):.0f}")
lat, T, f = res["S2 chạy ngay sau S1"]
print(f"S2: T dao động {T.max()-T.min():.1f} °C (đạt ±2 °C?) trong khi f bị kẹp ở {f.max():.2f} GHz thay vì {F_MAX}")

