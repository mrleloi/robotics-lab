# [đã chạy] Bài 10 — dự đoán đường cong underrun theo độ sâu DMA, TRƯỚC khi đo
# Mô hình: host gửi theo credit (giữ ring đầy khi không bị khựng); task ESP32 chuyển ring → DMA.
#  - host khựng d giây  → underrun nếu d > (ring + DMA)   (ring + DMA cùng che)
#  - task ESP32 khựng d → underrun nếu d > DMA             (ring có dữ liệu nhưng không ai chuyển)
import numpy as np
rng = np.random.default_rng(10)
HOURS = 1.0

def stalls(rate_per_s, med_ms, sig):
    n = rng.poisson(rate_per_s * 3600 * HOURS)
    return med_ms * np.exp(sig * rng.standard_normal(n))      # độ dài mỗi lần khựng (ms)

def per_hour(d, cover_ms):
    return np.sum(d > cover_ms) / HOURS

RING = 100.0                                                   # ring buffer ESP32 (ms), cố định
FS = 24000
SCEN = {  # (host: lần/s, trung vị ms, sigma) , (esp32: lần/s, trung vị ms, sigma) — tham số GIẢ ĐỊNH
    "nhàn":       ((0.05, 3, 0.6), (0.5, 1.0, 0.5)),
    "tải host":   ((2.0, 15, 0.9), (0.5, 1.0, 0.5)),
    "tải ESP32":  ((0.05, 3, 0.6), (5.0, 4.0, 0.7)),
}
frames = [80, 160, 320, 640, 1000]                             # dma_frame_num (≤1023 ở 16-bit stereo)
print("DMA(ms) :", "  ".join(f"{3*f/FS*1000:6.1f}" for f in frames))
for name, (h, e) in SCEN.items():
    dh, de = stalls(*h), stalls(*e)
    row = [per_hour(dh, RING + 3*f/FS*1000) + per_hour(de, 3*f/FS*1000) for f in frames]
    print(f"{name:<9}:", "  ".join(f"{x:6.0f}" for x in row), " underrun/giờ")
print("Quy tắc 3: 0 sự kiện trong 10 phút ⇒ cận trên 95% ≈ 18/giờ; trong 60 phút ≈ 3/giờ")
