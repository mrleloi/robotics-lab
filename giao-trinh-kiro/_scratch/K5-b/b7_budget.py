# [đã chạy] Ngân sách sai số thời gian: RSS vs cộng thẳng, kiểm bằng Monte Carlo
import numpy as np
rng = np.random.default_rng(0)
N = 200_000

# Mỗi nguồn: (tên, loại, tham số) — số MINH HỌA, thay bằng số của bạn
# "u" = đều trong [-a,+a] (lượng tử, pha không biết) ; "n" = Gauss sigma ; "b" = bias cố định
common = [
    ("ISR latency jitter",   "n", 3e-6),
    ("esp_timer 1 us",       "u", 0.5e-6),
    ("USB offset estimate",  "u", 250e-6),
    ("mid-exposure chua bu", "b", 5e-3),
]
scenarios = {
    "A: ghép theo frame index": common + [("frame index 30 fps", "u", 1/30/2)],
    "B: ghép theo hàng LED":    common + [("row method ±2 hàng", "u", 2*50e-6),
                                          ("IMU 1 kHz, đỉnh gõ", "u", 0.5e-3)],
}

def draw(kind, p):
    if kind == "n": return rng.normal(0, p, N)
    if kind == "u": return rng.uniform(-p, p, N)
    return np.full(N, p)

def std_of(kind, p):   # độ bất định chuẩn (GUM loại B): đều ±a -> a/sqrt(3)
    return {"n": p, "u": p/np.sqrt(3), "b": 0.0}[kind]

def bound_of(kind, p): # biên xấu nhất (Gauss: lấy 3 sigma)
    return {"n": 3*p, "u": p, "b": abs(p)}[kind]

for name, src in scenarios.items():
    total = sum(draw(k, p) for _, k, p in src)
    bias = sum(p for _, k, p in src if k == "b")
    rss = np.sqrt(sum(std_of(k, p)**2 for _, k, p in src))
    worst = sum(bound_of(k, p) for _, k, p in src)
    print(f"--- {name}")
    print(f"  bias (cộng thẳng)        : {bias*1e3:8.3f} ms")
    print(f"  RSS ngẫu nhiên (1 sigma) : {rss*1e3:8.3f} ms   MC std: {total.std()*1e3:8.3f} ms")
    print(f"  |bias| + 2.58*RSS        : {(abs(bias)+2.58*rss)*1e3:8.3f} ms   MC p99|lệch|: "
          f"{np.percentile(abs(total), 99)*1e3:8.3f} ms")
    print(f"  worst-case cộng thẳng    : {worst*1e3:8.3f} ms   MC max|lệch|: "
          f"{abs(total).max()*1e3:8.3f} ms")

# Quy đổi sai số thời gian -> sai số vị trí
for dt in (1e-3, 10e-3, 33e-3):
    print(f"dt={dt*1e3:5.1f} ms: tịnh tiến 0.5 m/s -> {0.5*dt*1e3:6.2f} mm ;"
          f" xoay 1 rad/s, điểm cách 2 m -> {2*dt*1e3:6.2f} mm ({dt*1e3:5.2f} mrad)")
