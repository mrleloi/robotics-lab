# [đã chạy] Bài 8: lượng tử hóa một ma trận trọng số — scale, zero-point, per-tensor vs per-channel vs per-group
import numpy as np
rng = np.random.default_rng(5)
OUT, IN = 1024, 1024
# Trọng số giả: mỗi hàng (kênh ra) có độ lớn riêng (log-normal), vài kênh "ngoại lai" lớn gấp ~20 lần
row_scale = rng.lognormal(0, 0.5, OUT)[:, None]
row_scale[rng.choice(OUT, 8, replace=False)] *= 20
W = rng.normal(0, 0.02, (OUT, IN)) * row_scale
X = rng.normal(0, 1, (IN, 64))                         # 64 vector kích hoạt đầu vào

def q_sym(w, bits, axis=None, group=None):
    """Đối xứng: q = round(w/s), s = max|w| / (2^(b-1)-1); zero-point = 0."""
    qmax = 2 ** (bits - 1) - 1
    if group:                                            # per-group dọc chiều IN
        g = w.reshape(w.shape[0], -1, group)
        s = np.abs(g).max(axis=2, keepdims=True) / qmax
        return (np.clip(np.round(g / s), -qmax - 1, qmax) * s).reshape(w.shape)
    s = np.abs(w).max(axis=axis, keepdims=True) / qmax if axis is not None else np.abs(w).max() / qmax
    return np.clip(np.round(w / s), -qmax - 1, qmax) * s

def q_asym(x, bits):
    """Bất đối xứng: s = (max-min)/(2^b-1), z = round(-min/s); x ≈ s·(q - z)."""
    lo, hi = x.min(), x.max(); s = (hi - lo) / (2 ** bits - 1); z = np.round(-lo / s)
    q = np.clip(np.round(x / s) + z, 0, 2 ** bits - 1)
    return s * (q - z)

def report(name, Wq):
    ew = np.linalg.norm(W - Wq) / np.linalg.norm(W)
    Y, Yq = W @ X, Wq @ X
    ey = np.linalg.norm(Y - Yq) / np.linalg.norm(Y)
    print(f"{name:28s} sai số W {ew:7.2%}  sai số y=Wx {ey:7.2%}  SQNR(y) {-20*np.log10(ey):5.1f} dB")

report("int8 per-tensor", q_sym(W, 8))
report("int8 per-channel (hàng)", q_sym(W, 8, axis=1))
report("int4 per-tensor", q_sym(W, 4))
report("int4 per-channel", q_sym(W, 4, axis=1))
report("int4 per-group g=64", q_sym(W, 4, group=64))
report("int4 per-group g=32", q_sym(W, 4, group=32))

# Kích hoạt sau ReLU toàn dương: đối xứng phí một nửa dải mã, bất đối xứng (zero-point) dùng hết
A = np.maximum(rng.normal(0.5, 1.0, 100_000), 0)
for bits in (8, 4):
    es = np.linalg.norm(A - q_sym(A, bits)) / np.linalg.norm(A)
    ea = np.linalg.norm(A - q_asym(A, bits)) / np.linalg.norm(A)
    print(f"ReLU activations {bits}-bit: đối xứng {es:.2%} | bất đối xứng (zero-point) {ea:.2%}")
print(f"Bộ nhớ trọng số {OUT}x{IN}: fp32 {OUT*IN*4/2**20:.1f} MiB, int8 {OUT*IN/2**20:.2f} MiB (+scale), "
      f"int4 g=64 {OUT*IN/2/2**20 + OUT*IN/64*2/2**20:.2f} MiB (scale fp16)")
