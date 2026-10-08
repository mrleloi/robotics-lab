# [đã chạy] Bài 9 — tách "trễ hệ thống" khỏi "trễ không khí" bằng cách đo ở nhiều khoảng cách
import numpy as np
rng = np.random.default_rng(9)
T_C = 29.0                                  # nhiệt độ phòng (°C) — đo, đừng giả định 20 °C
c = 331.3 + 0.606 * T_C                     # tốc độ âm thanh xấp xỉ (m/s)
lat_sys = 41.7                              # "sự thật" giả định của kịch bản (ms) — chính là thứ cần tìm
d_true = np.repeat([0.10, 0.20, 0.30, 0.50, 0.80], 10)       # khoảng cách định đặt (m), 10 lần mỗi mức
d_meas = d_true + rng.normal(0, 0.005, d_true.size)           # thước + vị trí lỗ mic: lệch ~5 mm
onset = rng.uniform(0, 1 / 24, d_true.size)                   # lượng tử hóa onset: 1 mẫu mic ở 24 kHz (ms)
y = lat_sys + 1000 * d_true / c + onset + rng.normal(0, 0.05, d_true.size)   # số đo (ms)

A = np.vstack([d_meas, np.ones_like(d_meas)]).T
(slope, icpt), res, *_ = np.linalg.lstsq(A, y, rcond=None)
sigma2 = res[0] / (len(y) - 2)
cov = sigma2 * np.linalg.inv(A.T @ A)
se_s, se_i = np.sqrt(np.diag(cov))
print(f"độ dốc = {slope:.3f} ± {2*se_s:.3f} ms/m  → c ≈ {1000/slope:.0f} m/s (thật {c:.0f})")
print(f"chặn   = {icpt:.3f} ± {2*se_i:.3f} ms     (thật {lat_sys + 1/48:.3f}, gồm nửa mẫu onset)")
# Cách "trừ 0,87 ms" của bản gốc, ở một khoảng cách duy nhất, với giả định 343 m/s và 30 cm:
m30 = y[d_true == 0.30]
print(f"chỉ đo ở 30 cm, trừ 0,87 ms: {np.median(m30) - 0.87:.3f} ms")
