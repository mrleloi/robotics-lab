# [đã chạy] Micro-benchmark: trần compute (GEMM) và trần băng thông (copy) thật trên máy bạn
import time, os
import numpy as np

def best_of(fn, reps=7):
    fn()                                         # warm-up: cấp phát, nạp thư viện BLAS
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter(); fn(); ts.append(time.perf_counter() - t0)
    return min(ts), np.median(ts)

# 1) GEMM FP32: 2*n^3 FLOP. n đủ lớn để intensity >> ridge, đủ nhỏ để không swap
for n in (512, 1024, 2048):
    A = np.random.rand(n, n).astype(np.float32); B = np.random.rand(n, n).astype(np.float32)
    C = np.empty_like(A)
    tmin, tmed = best_of(lambda: np.matmul(A, B, out=C))
    print(f"GEMM fp32 n={n:5d}: best {2*n**3/tmin/1e9:7.1f} GFLOP/s, median {2*n**3/tmed/1e9:7.1f}")

# 2) GEMV FP32 (M=1): intensity ~0.5 FLOP/byte -> phải chạm trần băng thông, không phải compute
K, N = 4096, 16384                               # ma trận 256 MB >> cache L3
W = np.random.rand(K, N).astype(np.float32); x = np.random.rand(K).astype(np.float32)
tmin, _ = best_of(lambda: x @ W)
print(f"GEMV fp32 {K}x{N}: {2*K*N/tmin/1e9:6.1f} GFLOP/s, ~{W.nbytes/tmin/1e9:5.1f} GB/s đọc W")

# 3) Copy băng thông: đếm đọc + ghi (thực tế có thể thêm write-allocate -> số này là cận dưới)
a = np.ones(64 * 2**20 // 8); b = np.empty_like(a)   # 64 MB mỗi mảng
tmin, _ = best_of(lambda: np.copyto(b, a))
print(f"Copy 64 MB: ~{2*a.nbytes/tmin/1e9:5.1f} GB/s (1 luồng, đọc+ghi)")
print("OMP/OPENBLAS threads:", os.environ.get("OMP_NUM_THREADS"), os.environ.get("OPENBLAS_NUM_THREADS"))
