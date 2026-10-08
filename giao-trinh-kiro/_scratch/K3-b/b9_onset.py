# [đã chạy] Bài 9 — tìm onset bằng ngưỡng vs bằng cross-correlation (F4.6, F5.6)
import numpy as np
from scipy.signal import lfilter, butter, correlate
rng = np.random.default_rng(91)
fs = 24000
burst = np.sin(2*np.pi*2000*np.arange(48)/fs) * np.hanning(48)    # 2 ms tone burst 2 kHz đã biết
x = np.zeros(4800); x[1000:1048] = burst                            # tín hiệu phát (lấy từ DOUT đã decode)
b, a = butter(2, [300/(fs/2), 6000/(fs/2)], btype="band")           # loa + mic ≈ một bộ lọc dải thông
true_delay = 37                                                     # mẫu (≈1,54 ms) — "sự thật" của kịch bản
for vol in [1.0, 0.3, 0.1]:
    est_thr, est_xc = [], []
    for _ in range(200):
        y = vol * lfilter(b, a, np.roll(x, true_delay)) + rng.normal(0, 0.01, x.size)
        k = np.argmax(np.abs(y) > 0.05)                            # ngưỡng cố định
        est_thr.append(k - 1000)
        c = correlate(y, x, mode="full"); lag = np.argmax(c) - (x.size - 1)
        est_xc.append(lag)
    t, xc = np.array(est_thr), np.array(est_xc)
    print(f"âm lượng {vol:>4}: ngưỡng → {t.mean():6.1f} ± {t.std():4.1f} mẫu | "
          f"xcorr → {xc.mean():6.1f} ± {xc.std():4.1f} mẫu | thật {true_delay}")
