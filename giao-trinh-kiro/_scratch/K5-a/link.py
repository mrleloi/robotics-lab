# [đã chạy] Đồ chơi: timestamp nguồn (ESP32) vs lúc host nhận, qua USB và WiFi. Mọi tham số là GIẢ ĐỊNH.
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(1)
fs, T = 200.0, 1800.0                        # 200 Hz, 30 phút
k = np.arange(int(fs * T))
t_src = k / fs                               # timestamp ESP32 ghi vào gói (giây từ lúc boot)
skew, off = 35e-6, 12.3                      # đồng hồ ESP32 nhanh 35 ppm; boot lúc host = 12.3 s
t_true = off + t_src / (1 + skew)            # thời điểm lấy mẫu thật, theo đồng hồ host (coi là chuẩn)

def usb(t):                                  # chờ tới ranh giới frame 1 ms của host + đôi khi bị gom + lịch host
    frame = np.ceil((t + 50e-6) / 1e-3) * 1e-3
    batch = (rng.random(t.size) < 0.02) * rng.integers(1, 8, t.size) * 1e-3
    return frame + batch + rng.exponential(40e-6, t.size), np.zeros(t.size, bool)

def wifi(t):                                 # trễ nền + đuôi lognormal + thỉnh thoảng retry/kênh bận + mất gói
    d = 1.5e-3 + rng.lognormal(np.log(1.0e-3), 0.9, t.size)
    d += (rng.random(t.size) < 0.01) * rng.exponential(30e-3, t.size)
    return t + d, rng.random(t.size) < 0.003

fig, ax = plt.subplots(2, 1, figsize=(8, 6))
for name, (recv, lost) in (("USB", usb(t_true)), ("WiFi", wifi(t_true))):
    keep = ~lost
    ts, d = t_src[keep], recv[keep] - t_src[keep]   # "latency" ngây thơ = trễ thật + offset + skew·t
    win = (ts // 10).astype(int)                    # đường bao dưới: min mỗi cửa sổ 10 s, rồi fit thẳng
    idx = [np.flatnonzero(win == w)[np.argmin(d[win == w])] for w in np.unique(win)]
    a, b = np.polyfit(ts[idx], d[idx], 1)
    res = (d - (a * ts + b)) * 1e3                  # ms: trễ vượt mức tối thiểu
    p = np.percentile(res, [50, 99, 99.9])
    print(f"{name:4s}: naive dải {np.ptp(d)*1e3:6.1f} ms | skew ước lượng {-a*1e6:5.1f} ppm | "
          f"p50 {p[0]:.3f} p99 {p[1]:.3f} p99.9 {p[2]:.3f} ms | mất {lost.mean()*100:.2f}%")
    ax[0].hist(res, bins=400, histtype="step", log=True, label=name)
    if name == "USB":
        sel = ts < 120
        ax[1].plot(ts[sel], res[sel], ",")
        lo = res < 1.2                               # bỏ các lần bị gom để thấy răng cưa
        cyc = np.corrcoef(ts[lo] % (1e-3 / skew), res[lo])[0, 1]
        print(f"USB : tương quan trễ với pha (t mod {1e-3/skew:.1f} s) = {cyc:+.2f}  -> jitter có cấu trúc")
ax[0].set_xlabel("trễ vượt tối thiểu (ms)"); ax[0].legend()
ax[1].set_xlabel("t ESP32 (s)"); ax[1].set_ylabel("USB trễ dư (ms)")
plt.tight_layout(); plt.savefig("link.png", dpi=80)
