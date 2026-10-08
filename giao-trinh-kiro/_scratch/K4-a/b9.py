# [đã chạy] Bài 9: mặt Pareto khi mỗi điểm có sai số — "bị chi phối" chắc tới đâu?
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
rng = np.random.default_rng(9)
# SỐ GIẢ ĐỊNH để luyện phương pháp, không phải số đo của model nào.
# tên: (p50 latency ms, độ lệch chuẩn p50 giữa các phiên A/A, số thành công, số episode)
cfg = {"fp32": (210, 6, 312, 400), "bf16": (120, 4, 310, 400), "fp16": (118, 4, 300, 400),
       "int8": (95, 5, 296, 400), "int8-noQAT": (97, 5, 270, 400), "int4-all": (70, 4, 120, 400),
       "int4-mixed": (80, 4, 284, 400)}
names = list(cfg)

def frontier(lat, sr):
    on = []
    for i in range(len(lat)):
        dom = any((lat[j] <= lat[i] and sr[j] >= sr[i]) and (lat[j] < lat[i] or sr[j] > sr[i])
                  for j in range(len(lat)) if j != i)
        on.append(not dom)
    return np.array(on)

lat0 = np.array([cfg[n][0] for n in names], float)
sr0 = np.array([cfg[n][2] / cfg[n][3] for n in names])
on0 = frontier(lat0, sr0)
R = 5000; hits = np.zeros(len(names))
for _ in range(R):   # lấy lại mẫu: latency theo nhiễu giữa phiên, success theo nhị thức
    lat = rng.normal(lat0, [cfg[n][1] for n in names])
    sr = rng.binomial([cfg[n][3] for n in names], sr0) / np.array([cfg[n][3] for n in names])
    hits += frontier(lat, sr)
for n, o, h, l, s in zip(names, on0, hits / R, lat0, sr0):
    print(f"{n:11s} p50={l:4.0f} ms  SR={s:.1%}  trên mặt Pareto (ước lượng điểm): {'CÓ' if o else 'không'}  "
          f"| xác suất nằm trên mặt khi tính nhiễu: {h:.0%}")

fig, ax = plt.subplots(figsize=(6, 4))
for n, l, s, o in zip(names, lat0, sr0, on0):
    k, N = cfg[n][2], cfg[n][3]
    ax.errorbar(l, s, xerr=1.96 * cfg[n][1], yerr=1.96 * np.sqrt(s * (1 - s) / N), fmt="o" if o else "x", capsize=3)
    ax.annotate(n, (l, s), textcoords="offset points", xytext=(5, 5))
idx = np.argsort(lat0[on0]); ax.plot(lat0[on0][idx], sr0[on0][idx], "--")
ax.set_xlabel("latency p50 (ms) — trái là tốt"); ax.set_ylabel("success rate — trên là tốt")
fig.tight_layout(); fig.savefig(r"c:\htdocs\physical\giao-trinh\_scratch\K4-a\pareto.png")
