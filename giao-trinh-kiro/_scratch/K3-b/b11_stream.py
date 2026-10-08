# [đã chạy] Bài 11/13 — RTF trung bình < 1 có đủ để stream không? batch vs stream
import numpy as np
rng = np.random.default_rng(11)

def run(D=12.0, c=0.5, rtf=0.8, sig=0.0, first=0.6, pre=0, overhead=0.03):
    """D: độ dài câu (s); c: độ dài mỗi chunk (s); rtf: RTF trung vị; sig: độ phân tán log-normal;
    first: chi phí cố định cho chunk đầu (encode text, warm cache); pre: số chunk chờ trước khi phát."""
    n = int(np.ceil(D / c))
    g = c * rtf * np.exp(sig * rng.standard_normal(n)) + overhead
    g[0] += first
    ready = np.cumsum(g)                        # thời điểm chunk k sinh xong (s, tính từ lúc nhận text)
    t = ready[min(pre, n - 1)]                  # bắt đầu phát khi đủ 'pre' chunk đệm
    ttfa, gaps = t, 0
    for k in range(n):                          # phát tuần tự; chunk chưa xong ⇒ im lặng (underrun)
        if ready[k] > t:
            gaps += 1; t = ready[k]
        t += c
    batch_ttfa = ready[-1]                      # batch: đợi sinh xong cả câu
    return dict(rtf_tb=g.sum() / D, ttfa=ttfa, end=t, gaps=gaps,
                batch_ttfa=batch_ttfa, batch_end=batch_ttfa + D)

def show(tag, **kw):
    r = [run(**kw) for _ in range(500)]
    a = lambda k: np.array([x[k] for x in r])
    print(f"{tag:<34} RTF đo p50={np.median(a('rtf_tb')):.2f} | TTFA p50={np.median(a('ttfa')):.2f}s "
          f"| xong p50={np.median(a('end')):.1f}s | batch xong p50={np.median(a('batch_end')):.1f}s "
          f"| câu có đứt={np.mean(a('gaps') > 0):.0%}")

show("A. RTF 0.8, đều", rtf=0.8)
show("B. RTF 0.8, phân tán sig=0.5", rtf=0.8, sig=0.5)
show("C. như B, đệm trước 2 chunk", rtf=0.8, sig=0.5, pre=2)
show("D. RTF 1.2, không đệm", rtf=1.2)
show("E. RTF 1.2, đệm (RTF-1)*D ≈ 5 chunk", rtf=1.2, pre=5)
