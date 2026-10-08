# [đã chạy] Bài 13 — ghép IMU 200 Hz với camera 30 Hz: as-of, nearest, nội suy, và offset đồng hồ
import numpy as np
rng = np.random.default_rng(13)

T = 60.0                                   # giây mô phỏng
A, f = 3.0, 2.0                            # gyro z thật: 3 rad/s, 2 Hz (lắc tay nhanh)
w = lambda t: A * np.sin(2 * np.pi * f * t)

# IMU: 200 Hz, timestamp ở MCU có jitter nhỏ, nhiễu đo 0,005 rad/s
t_imu = np.arange(0, T, 1 / 200) + rng.normal(0, 0.1e-3, int(T * 200))
t_imu.sort()
y_imu = w(t_imu) + rng.normal(0, 0.005, t_imu.size)

# Camera: 30 Hz, thời điểm chụp THẬT có jitter 2 ms; stamp ghi ra lệch offset so với clock IMU
t_cam_true = np.arange(0.5, T - 0.5, 1 / 30) + rng.normal(0, 2e-3, int((T - 1) * 30))

def align(t_query, method):
    i = np.searchsorted(t_imu, t_query)            # chỉ số mẫu IMU đầu tiên >= t_query
    if method == "asof":                           # mẫu cuối cùng <= t (backward as-of)
        return y_imu[i - 1]
    if method == "nearest":
        left_closer = (t_query - t_imu[i - 1]) < (t_imu[i] - t_query)
        return np.where(left_closer, y_imu[i - 1], y_imu[i])
    if method == "linear":
        t0, t1 = t_imu[i - 1], t_imu[i]
        a = (t_query - t0) / (t1 - t0)
        return (1 - a) * y_imu[i - 1] + a * y_imu[i]

truth = w(t_cam_true)
print(f"{'offset, jitter stamp':>20} | {'as-of':>7} | {'nearest':>7} | {'linear':>7}  (RMS sai số, rad/s)")
for off_ms, jit_ms in [(0, 0), (2, 0), (7, 0), (33.3, 0), (0, 2)]:
    # stamp camera = thời điểm thật + offset cố định + jitter của chính stamp
    t_stamp = t_cam_true + off_ms * 1e-3 + rng.normal(0, jit_ms * 1e-3, t_cam_true.size)
    errs = [np.sqrt(np.mean((align(t_stamp, m) - truth) ** 2)) for m in ("asof", "nearest", "linear")]
    print(f"{off_ms:>8.1f} ms, {jit_ms:>3.0f} ms   | " + " | ".join(f"{e:7.4f}" for e in errs))

# Quy đổi: sai số giá trị ↔ sai số thời gian tương đương, RMS(dω/dt) = A·2πf/√2
rms_slope = A * 2 * np.pi * f / np.sqrt(2)
print(f"RMS(dω/dt) = {rms_slope:.1f} rad/s² → 1 ms lệch ≈ {rms_slope*1e-3:.4f} rad/s RMS")

# Watermark: nội suy cần mẫu IMU SAU t_cam đã đến. IMU qua USB-serial trễ ~1-3 ms,
# camera qua UVC trễ ~30-80 ms (giả định). Bao nhiêu frame ghép được ngay khi frame tới?
lat_imu = rng.uniform(1e-3, 3e-3, t_imu.size)
lat_cam = rng.uniform(30e-3, 80e-3, t_cam_true.size)
arr_imu = t_imu + lat_imu
i_next = np.searchsorted(t_imu, t_cam_true)         # mẫu IMU ngay sau t_cam
ready_at = np.maximum.accumulate(arr_imu)[i_next]   # lúc mẫu đó (và mọi mẫu trước) đã tới
wait = ready_at - (t_cam_true + lat_cam)            # >0: frame phải chờ IMU
print(f"frame phải chờ IMU để nội suy: {np.mean(wait > 0)*100:.1f}%  (chờ max {max(wait.max(),0)*1e3:.1f} ms)")
# Đảo vai: nếu camera tới TRƯỚC (vd IMU qua WiFi trễ 20-150 ms) thì sao?
arr_imu_wifi = t_imu + rng.lognormal(np.log(30e-3), 0.6, t_imu.size)
ready_w = np.maximum.accumulate(arr_imu_wifi)[i_next]
wait_w = ready_w - (t_cam_true + lat_cam)
print(f"IMU qua WiFi: frame phải chờ {np.mean(wait_w > 0)*100:.1f}%, p99 chờ {np.percentile(wait_w,99)*1e3:.0f} ms")
