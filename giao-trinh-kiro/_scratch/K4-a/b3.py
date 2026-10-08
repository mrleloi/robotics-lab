# [đã chạy] Bài 3: coordinated omission — vòng đo "gọi xong mới gọi tiếp" giấu mất cú khựng
import numpy as np
rng = np.random.default_rng(1)

PERIOD = 100.0          # ms: lịch dự định, cứ 100 ms cần một lần inference (10 Hz)
DUR = 60_000.0          # ms: phiên đo 60 s
STALL_AT, STALL = 20_000.0, 3_000.0   # ở giây 20 hệ thống khựng 3 s (swap, throttle, GC...)

def service(t_start):
    s = rng.normal(40.0, 3.0)                     # ms, bình thường
    end_stall = STALL_AT + STALL
    if t_start + s > STALL_AT and t_start < end_stall:  # lần gọi chạm khoảng máy "đóng băng"
        s += end_stall - max(t_start, STALL_AT)          # công việc bị treo trong lúc khựng
    return s

# Cách 1 (ngây thơ): vòng lặp đóng, đo thời gian mỗi lần gọi, ghi đúng 1 mẫu cho cú khựng
t, naive, corrected = 0.0, [], []
k = 0
while k * PERIOD < DUR:
    intended = k * PERIOD
    start = max(t, intended)                      # không gửi sớm hơn lịch; trễ thì gửi ngay khi rảnh
    s = service(start)
    t = start + s
    naive.append(s)                               # đo từ lúc thực gửi
    corrected.append(t - intended)                # đo từ lúc LẼ RA phải gửi (lịch)
    k += 1

for name, x in (("ngây thơ", np.array(naive)), ("theo lịch", np.array(corrected))):
    p50, p99, p999 = np.percentile(x, [50, 99, 99.9])
    print(f"{name:9s}: n={len(x)}  p50={p50:6.1f}  p99={p99:7.1f}  p99.9={p999:7.1f}  max={x.max():7.1f} ms"
          f"  | số mẫu >100 ms: {(x > PERIOD).sum()}")
