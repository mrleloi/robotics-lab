# [đã chạy] Bài 1: từ meta/info.json suy ra tensor đầu vào/đầu ra và cái bẫy select_action
import json, numpy as np
from pathlib import Path

ROOT = Path(r"c:\htdocs\physical")
for name in ["libero", "lerobotpusht"]:
    info = json.loads((ROOT / "data" / name / "meta" / "info.json").read_text())
    fps = float(info["fps"])
    print(f"== {name}: fps={fps}")
    for k, f in info["features"].items():
        if f["dtype"] == "video":
            h, w, c = f["shape"]
            print(f"  {k}: dataset HWC uint8 {h}x{w}x{c} = {h*w*c} B; "
                  f"vào policy (B=1) float32 (1,{c},{h},{w}) = {h*w*c*4} B")
        elif k in ("observation.state", "action"):
            print(f"  {k}: float32 {f['shape']}")
    # SmolVLA: chunk_size=50, resize_imgs_with_padding=(512,512), max_action_dim=32 (configuration_smolvla.py)
    chunk = 50
    print(f"  chunk 50 bước ở {fps:g} Hz phủ {chunk/fps:.1f} s tương lai")
    print(f"  ảnh sau resize-pad 512x512 float32: {3*512*512*4/1e6:.2f} MB mỗi camera")

# Bẫy: đo select_action trong vòng lặp. 1/50 lần gọi chạy model, 49/50 chỉ pop hàng đợi.
rng = np.random.default_rng(0)
n = 5000
heavy = rng.normal(180.0, 8.0, n)          # ms, lần gọi có forward thật (giả định)
light = rng.normal(0.03, 0.005, n)         # ms, chỉ popleft()
is_heavy = (np.arange(n) % 50) == 0
lat = np.where(is_heavy, heavy, light)
for q in (50, 95, 98, 99, 99.9):
    print(f"select_action p{q}: {np.percentile(lat, q):8.3f} ms")
print(f"mean: {lat.mean():.2f} ms  | tỉ lệ lần gọi nặng: {is_heavy.mean():.3f}")
