# [đã chạy] Bài 9 — coordinated omission khi đo round-trip USB dưới tải (F1.3)
import numpy as np
rng = np.random.default_rng(93)
T = 600_000.0                                  # 10 phút (ms)
def service(t):                                # trễ round-trip nếu gửi lúc t: ~1 ms, nhưng host khựng 200 ms mỗi 10 s
    phase = t % 10_000
    stall = max(0.0, 200.0 - phase) if phase < 200 else 0.0
    return 1.0 + rng.exponential(0.2) + stall
# Đóng vòng: gửi ping, chờ trả lời, rồi mới gửi ping tiếp theo sau 10 ms
t, closed = 0.0, []
while t < T:
    r = service(t); closed.append(r); t += r + 10.0
# Mở vòng: lịch gửi cố định mỗi 10 ms, đo từ thời điểm LẼ RA phải gửi
opened = [service(s) for s in np.arange(0, T, 10.0)]
for name, v in [("đóng vòng", closed), ("mở vòng", opened)]:
    v = np.array(v)
    print(f"{name:<10} n={v.size:6d}  p50={np.percentile(v,50):5.2f}  p99={np.percentile(v,99):6.1f}  "
          f"p99.9={np.percentile(v,99.9):6.1f} ms")
