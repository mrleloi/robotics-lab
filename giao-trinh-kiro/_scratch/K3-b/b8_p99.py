# [đã chạy] Bài 8 — p99 của tổng có bằng tổng các p99 không?
import numpy as np
rng = np.random.default_rng(8)
N = 1_000_000
p99 = lambda x: np.percentile(x, 99)

def stages_lognormal(u=None):
    # 3 chặng trễ (ms), log-normal; u = biến ngẫu nhiên chung (nếu muốn chúng tương quan)
    meds, sig = [20.0, 5.0, 40.0], [0.5, 0.8, 0.3]
    out = []
    for m, s in zip(meds, sig):
        z = rng.standard_normal(N) if u is None else u
        out.append(m * np.exp(s * z))
    return out

def report(name, st):
    tot = sum(st)
    s99 = sum(p99(x) for x in st)
    print(f"{name:<22} tổng p99 các chặng = {s99:7.1f} ms | p99 của tổng = {p99(tot):7.1f} ms | "
          f"tổng trung bình = {sum(x.mean() for x in st):6.1f} vs trung bình tổng = {tot.mean():6.1f}")

# A. ba chặng độc lập
report("A. độc lập", stages_lognormal())
# B. ba chặng cùng chậm cùng lúc (một nguyên nhân chung: CPU hạ xung)
report("B. hoàn toàn tương quan", stages_lognormal(u=rng.standard_normal(N)))
# C. mỗi chặng nhanh đều, nhưng có 0.6% xác suất "khựng" 50 ms (GC, USB re-poll, swap...)
st = []
for base in [20.0, 5.0, 40.0]:
    x = base + rng.normal(0, 1, N)
    x += 50.0 * (rng.random(N) < 0.006)
    st.append(x)
report("C. đuôi hiếm (khựng)", st)
