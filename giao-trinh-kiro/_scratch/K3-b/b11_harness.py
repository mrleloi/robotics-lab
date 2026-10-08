# [đã chạy với TTS giả] Bài 11 — harness đo RTF + chunk; thay fake_tts bằng model thật (API [tự đo])
import time, json, platform, statistics as st
import numpy as np

def fake_tts(text, sr=24000, rtf=0.6, chunk_s=0.5):
    """Giả lập TTS streaming: yield từng chunk PCM int16. Thay bằng model thật."""
    dur = 0.35 * len(text.split())                        # ~0,35 s audio mỗi từ (giả định)
    n = max(1, int(np.ceil(dur / chunk_s)))
    for _ in range(n):
        time.sleep(chunk_s * rtf * np.random.lognormal(0, 0.3))
        yield np.zeros(int(sr * chunk_s), dtype=np.int16)

def measure(tts, text, sr=24000):
    t0 = time.perf_counter(); ready, played_s = [], 0.0
    for pcm in tts(text, sr=sr):
        ready.append(time.perf_counter() - t0)
        played_s += pcm.size / sr                          # mono; stereo thì chia thêm số kênh
        ready[-1] = (ready[-1], played_s)
    t_gen = ready[-1][0]
    # đệm tối thiểu để không đứt: max_k [ready_k − (ready_0 + audio đã có trước chunk k)]
    starts = [0.0] + [r[1] for r in ready[:-1]]
    need = max(0.0, max(r[0] - (ready[0][0] + s) for r, s in zip(ready, starts)))
    return dict(rtf=t_gen / played_s, ttfc=ready[0][0], audio_s=played_s, prebuffer_s=need)

def bench(tts, sentences, reps=10, warmup=3):
    for s in sentences[:1]:
        for _ in range(warmup): measure(tts, s)           # warm-up: không ghi
    rows = [dict(len=len(s.split()), rep=r, **measure(tts, s)) for s in sentences for r in range(reps)]
    meta = dict(cpu=platform.processor(), py=platform.python_version(), reps=reps, warmup=warmup)
    return meta, rows

if __name__ == "__main__":
    sents = ["xin chào mọi người"] * 3 + ["hôm nay trời đẹp quá " * 4] * 3
    meta, rows = bench(fake_tts, sents, reps=4, warmup=1)
    for L in sorted({r["len"] for r in rows}):
        v = [r for r in rows if r["len"] == L]
        q = lambda k: (st.median(x[k] for x in v), max(x[k] for x in v))
        print(f"{L:>3} từ n={len(v)}: RTF p50/max={q('rtf')[0]:.2f}/{q('rtf')[1]:.2f}  "
              f"TTFC p50={q('ttfc')[0]:.2f}s  đệm cần max={q('prebuffer_s')[1]:.2f}s")
    print(json.dumps(meta, ensure_ascii=False))
