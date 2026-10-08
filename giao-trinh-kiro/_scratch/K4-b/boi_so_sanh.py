# [đã chạy] Bội so sánh: 12 cấu hình CÙNG chất lượng thật, so từng cặp → bao nhiêu "khác biệt có ý nghĩa"?
import numpy as np
from itertools import combinations
from scipy.stats import norm

rng = np.random.default_rng(0)
K = 12          # 3 model × 4 precision (chất lượng đo trên GPU)
N = 50          # episode LIBERO mỗi cấu hình
P_TRUE = 0.70   # mọi cấu hình có CÙNG tỉ lệ thành công thật
ALPHA = 0.05
TRIALS = 2000

def p_two_prop(k1, k2, n):
    p = (k1 + k2) / (2 * n)
    se = np.sqrt(max(p * (1 - p), 1e-12) * 2 / n)
    z = (k1 - k2) / n / se
    return 2 * norm.sf(abs(z))

def holm(pvals, alpha):
    order = np.argsort(pvals)
    m = len(pvals)
    rejected = 0
    for i, idx in enumerate(order):
        if pvals[idx] <= alpha / (m - i):
            rejected += 1
        else:
            break
    return rejected

raw_any, holm_any, raw_count = 0, 0, []
for _ in range(TRIALS):
    k = rng.binomial(N, P_TRUE, size=K)
    pv = np.array([p_two_prop(k[i], k[j], N) for i, j in combinations(range(K), 2)])
    n_sig = int((pv < ALPHA).sum())
    raw_count.append(n_sig)
    raw_any += n_sig > 0
    holm_any += holm(pv, ALPHA) > 0

print(f"Số cặp so sánh: {K*(K-1)//2}")
print(f"Trung bình số cặp 'có ý nghĩa' (không hiệu chỉnh): {np.mean(raw_count):.2f}")
print(f"P(ít nhất 1 cặp 'có ý nghĩa'), không hiệu chỉnh: {raw_any/TRIALS:.2f}")
print(f"P(ít nhất 1 cặp 'có ý nghĩa'), Holm: {holm_any/TRIALS:.3f}")
k = rng.binomial(N, P_TRUE, size=K)
print("Một lần chạy mẫu, success rate (%):", (100 * k / N).round(0))
