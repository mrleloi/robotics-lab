# [đã chạy] Bài 7: success rate là một tỉ lệ — Wilson CI, "biến thiên giữa seed", và cỡ mẫu
import numpy as np
from scipy.stats import norm
rng = np.random.default_rng(11)

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d; h = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h

for k, n in ((9, 10), (10, 10), (35, 50), (320, 400), (0, 10)):
    lo, hi = wilson(k, n); print(f"{k}/{n}: p̂={k/n:.0%}  Wilson95 [{lo:.1%}, {hi:.1%}]")

# Một suite 10 task, 50 episode/task, policy KHÔNG ĐỔI (p thật mỗi task cố định). Chỉ đổi seed.
p_true = np.array([0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.6, 0.5, 0.3, 0.0])
runs = rng.binomial(50, p_true, size=(3, 10)) / 50          # 3 nhóm seed
print("tổng 3 nhóm seed:", np.round(runs.mean(axis=1), 3), "| p thật trung bình", p_true.mean())
print("task 'p=0.7' qua 3 seed:", runs[:, 5], "→ chênh max-min:", np.ptp(runs[:, 5]))
sim = rng.binomial(50, p_true, size=(20000, 10)) / 50
print(f"độ lệch chuẩn tổng suite giữa các seed: {sim.mean(axis=1).std():.3f}; của task p=0.7: {sim[:,5].std():.3f}")

# Cỡ mẫu (mỗi cấu hình) để phân biệt 70% vs 75%, alpha=0.05 hai phía, power 0.8
def n_two_prop(p1, p2, a=0.05, pw=0.8):
    za, zb = norm.ppf(1 - a/2), norm.ppf(pw); pb = (p1 + p2) / 2
    return ((za*np.sqrt(2*pb*(1-pb)) + zb*np.sqrt(p1*(1-p1) + p2*(1-p2)))**2) / (p1 - p2)**2
for p1, p2 in ((0.70, 0.75), (0.70, 0.80), (0.90, 0.95), (0.61, 0.61 + 0.06)):
    print(f"{p1:.0%} vs {p2:.0%}: cần ≈ {np.ceil(n_two_prop(p1, p2)):.0f} episode MỖI cấu hình")

# Power thực khi chỉ có 200 episode/cấu hình và chênh thật 5 điểm (Monte Carlo, kiểm định z hai tỉ lệ)
k1 = rng.binomial(200, 0.70, 20000); k2 = rng.binomial(200, 0.75, 20000)
p1, p2 = k1/200, k2/200; pb = (k1 + k2) / 400
z = (p2 - p1) / np.sqrt(pb*(1-pb)*2/200)
print(f"n=200/cấu hình, chênh thật 5 điểm: phát hiện được {np.mean(np.abs(z) > 1.96):.0%} số lần")
