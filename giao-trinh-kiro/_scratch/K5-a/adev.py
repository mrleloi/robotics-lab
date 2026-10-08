# [đã chạy] Allan deviation cho gyro đứng yên: nhiễu trắng + bias random walk (số giả định)
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(0)
fs = 200.0                     # Hz, ODR giả định
T = 2 * 3600                   # 2 giờ đứng yên
n = int(fs * T)
ND = 0.005                     # °/s/√Hz — noise density (cỡ MPU6050, tra datasheet chip của bạn)
sigma_w = ND * np.sqrt(fs / 2) # σ mỗi mẫu nếu băng thông = fs/2
K = 0.0005                     # °/s/√s — bias random walk (giả định)
bias0 = 1.2                    # °/s — bias tĩnh (giả định)
w = rng.normal(0, sigma_w, n)
rw = np.cumsum(rng.normal(0, K / np.sqrt(fs), n))
omega = bias0 + rw + w         # °/s

def adev(x, fs, taus):
    """Overlapping Allan deviation từ chuỗi tốc độ x (lấy mẫu đều fs)."""
    theta = np.cumsum(x) / fs  # tích phân thành góc
    out = []
    for tau in taus:
        m = int(tau * fs)
        d = theta[2 * m:] - 2 * theta[m:-m] + theta[:-2 * m]
        out.append(np.sqrt(np.mean(d ** 2) / (2 * tau ** 2)))
    return np.array(out)

taus = np.logspace(-2, np.log10(T / 10), 40)
ad = adev(omega, fs, taus)
print("std toàn chuỗi      : %.4f °/s" % omega.std())
print("ADEV(τ=1 s)         : %.4f °/s  (so với ND/√2 = %.4f)" % (np.interp(1, taus, ad), ND / np.sqrt(2)))
i = np.argmin(ad)
print("đáy ADEV (bias instability-ish): %.5f °/s tại τ ≈ %.0f s" % (ad[i], taus[i]))
print("góc trôi sau 60 s nếu không trừ bias: %.1f °" % (bias0 * 60))
plt.loglog(taus, ad, ".-"); plt.xlabel("τ (s)"); plt.ylabel("σ_A(τ) (°/s)")
plt.grid(True, which="both"); plt.savefig("adev.png", dpi=80)
