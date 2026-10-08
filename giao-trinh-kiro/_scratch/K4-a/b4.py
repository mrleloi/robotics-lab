# [đã chạy] Bài 4: hiệu chuẩn harness bằng model giả + phán quyết ba trạng thái
import time, numpy as np
rng = np.random.default_rng(7)

# (a) Dải hợp lý của p50/p95/p99 khi n=200 mẫu từ N(100, 5) ms — "dung sai" của chính phép thử
est = np.percentile(rng.normal(100, 5, (20000, 200)), [50, 95, 99], axis=1)
for q, e in zip((50, 95, 99), est):
    print(f"p{q}: lý thuyết {100 + 5*{50:0, 95:1.645, 99:2.326}[q]:.1f}  | 95% số lần thử rơi trong "
          f"[{np.percentile(e, 2.5):.1f}, {np.percentile(e, 97.5):.1f}] ms")

# (b) time.sleep có đúng không? Đo độ vượt (overshoot) trên chính máy này
over = []
for _ in range(50):
    t0 = time.perf_counter(); time.sleep(0.010); over.append((time.perf_counter() - t0) * 1e3 - 10.0)
print(f"sleep(10 ms) vượt: p50={np.percentile(over,50):.3f}  p99={np.percentile(over,99):.3f} ms")
t0 = time.perf_counter_ns(); [time.perf_counter_ns() for _ in range(100000)]
print(f"chi phí một lần đọc perf_counter_ns: {(time.perf_counter_ns()-t0)/1e5:.0f} ns")

# (c) Phán quyết ba trạng thái: B có chậm hơn A quá 3% (ngưỡng cam kết trước) không?
def verdict(a, b, margin=0.03, B=3000):
    ia = rng.integers(0, len(a), (B, len(a))); ib = rng.integers(0, len(b), (B, len(b)))
    r = np.median(b[ib], axis=1) / np.median(a[ia], axis=1) - 1
    lo, hi = np.percentile(r, [2.5, 97.5])
    if hi < margin and lo > -margin: v = "PASS (tương đương trong ±3%)"
    elif lo > margin: v = "FAIL (chậm hơn >3%)"
    else: v = "INCONCLUSIVE (cần thêm mẫu)"
    return f"Δp50 CI95 [{lo:+.1%}, {hi:+.1%}] → {v}"

for n, shift in ((30, 1.00), (300, 1.00), (300, 1.04), (2000, 1.00), (2000, 1.03), (2000, 1.06)):
    a = rng.lognormal(np.log(100), 0.15, n); b = rng.lognormal(np.log(100 * shift), 0.15, n)
    print(f"n={n:3d}, B thật chậm hơn {shift-1:.0%}: {verdict(a, b)}")

