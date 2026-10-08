# [đã chạy] Bài 2: p99 của 100 mẫu đáng tin tới đâu? Bootstrap CI cho p50/p99, n=100 vs n=10 000
import numpy as np
rng = np.random.default_rng(42)

def sample(n):
    # latency "đuôi dài": log-normal quanh 100 ms + 3% lần bị khựng (GC, swap, tenant khác) dài gấp 3–6 lần
    base = rng.lognormal(mean=np.log(100), sigma=0.15, size=n)
    stall = rng.random(n) < 0.03
    return np.where(stall, base * rng.uniform(3, 6, n), base)

truth = sample(5_000_000)
t50, t99 = np.percentile(truth, [50, 99])
print(f"SỰ THẬT (5e6 mẫu): mean={truth.mean():.1f}  p50={t50:.1f}  p99={t99:.1f} ms")

def boot_ci(x, q, B=2000):
    idx = rng.integers(0, len(x), (B, len(x)))
    est = np.percentile(x[idx], q, axis=1)
    return np.percentile(est, [2.5, 97.5])

for n in (100, 1000, 10_000):
    x = sample(n)
    lo50, hi50 = boot_ci(x, 50)
    lo99, hi99 = boot_ci(x, 99)
    print(f"n={n:6d}: p50={np.percentile(x,50):6.1f} CI95[{lo50:6.1f},{hi50:6.1f}] | "
          f"p99={np.percentile(x,99):6.1f} CI95[{lo99:6.1f},{hi99:6.1f}]  "
          f"(số mẫu nằm trên p99 thật: {(x > t99).sum()})")

# Lặp lại thí nghiệm 1000 lần: p99 ước lượng từ n=100 dao động bao nhiêu? CI bootstrap phủ đúng bao nhiêu lần?
for n in (100, 10_000):
    reps = 1000 if n == 100 else 200
    est, cover = [], 0
    for _ in range(reps):
        x = sample(n)
        est.append(np.percentile(x, 99))
        lo, hi = boot_ci(x, 99, B=500)
        cover += lo <= t99 <= hi
    est = np.array(est)
    print(f"n={n}: p99 ước lượng qua {reps} lần lặp: 5%..95% = [{np.percentile(est,5):.0f}, {np.percentile(est,95):.0f}] ms;"
          f" CI bootstrap phủ p99 thật {cover/reps:.0%}")

