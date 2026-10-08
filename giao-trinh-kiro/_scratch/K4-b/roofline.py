# [đã chạy] Roofline đồ chơi cho N100: ridge point và vị trí vài loại phép tính
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- Trần lý thuyết [ước lượng] — THAY bằng số bạn tự tính/đo ---
cores, f_ghz, flop_cyc = 4, 2.9, 16            # Gracemont: 2 FMA 128-bit = 2*4*2
cpu_peak = cores * f_ghz * flop_cyc            # GFLOP/s FP32
igpu_peak = 24 * 16 * 0.75                     # 24 EU * 16 FLOP/chu kỳ * 0.75 GHz
bw = 4800e6 * 8 / 1e9                          # 1 kênh 64-bit DDR5-4800, GB/s

def gemm_ai(M, K, N, b):                       # FLOP / byte DRAM tối thiểu
    flop = 2 * M * K * N
    byte = b * (K * N + M * K + M * N)         # đọc W, đọc X, ghi Y (mỗi thứ 1 lần)
    return flop / byte

def conv_ai(H, W, Ci, Co, k, b):
    flop = 2 * H * W * Ci * Co * k * k
    byte = b * (H * W * Ci + H * W * Co + k * k * Ci * Co)
    return flop / byte

# Kích thước GIẢ ĐỊNH — thay bằng config thật của model bạn đo
pts = {
    "GEMV decode M=1 fp32":      gemm_ai(1, 960, 3840, 4),
    "GEMV decode M=1 fp16":      gemm_ai(1, 960, 3840, 2),
    "expert chunk M=50 fp32":    gemm_ai(50, 720, 2880, 4),
    "LM prefix M=256 fp32":      gemm_ai(256, 960, 3840, 4),
    "ViT 1024 patch fp32":       gemm_ai(1024, 768, 3072, 4),
    "conv3x3 56x56x64 fp32":     conv_ai(56, 56, 64, 64, 3, 4),
}
print(f"CPU peak ~{cpu_peak:.0f} GFLOP/s, iGPU peak ~{igpu_peak:.0f}, BW ~{bw:.1f} GB/s")
print(f"Ridge CPU = {cpu_peak/bw:.1f} FLOP/B, ridge iGPU fp32 = {igpu_peak/bw:.1f}")
for name, ai in pts.items():
    att = min(cpu_peak, ai * bw)
    side = "memory-bound" if ai < cpu_peak / bw else "compute-bound"
    print(f"{name:26s} AI={ai:7.1f}  trần CPU={att:6.0f} GFLOP/s  {side}")

x = np.logspace(-1, 3, 200)
plt.loglog(x, np.minimum(cpu_peak, x * bw), label="N100 CPU FP32")
plt.loglog(x, np.minimum(igpu_peak, x * bw), "--", label="N100 iGPU FP32")
for name, ai in pts.items():
    plt.scatter(ai, min(cpu_peak, ai * bw)); plt.annotate(name, (ai, min(cpu_peak, ai * bw)), fontsize=7)
plt.xlabel("Arithmetic intensity (FLOP/byte)"); plt.ylabel("GFLOP/s"); plt.legend()
plt.savefig("roofline_n100.png", dpi=120)
