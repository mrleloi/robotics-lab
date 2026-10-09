# Khóa 4 — Module 4: Nhiều model, nhiều target (18h)

Bài 10 (6h) · Bài 11 (6h) · Bài 12 (6h). Nguồn xương sống: `khoa-4-benchmark-edge.md`, Module 4.

Tiêu chí PASS số 1 của M6 đòi **≥3 model × ≥2 target**. Module này có ba câu hỏi. Harness có thật sự tổng quát không (Bài 10)? Trên chính chiếc N100 sẽ nằm trên robot, chạy được gì (Bài 11)? Và vì sao các con số ra như vậy (Bài 12)? Bài 12 là bài biến bảng số thành phân tích. Nó cũng sửa một lỗi của bản Gemini: con số "0.7 TFLOPS" cho N100 và câu "VLA batch 1 là compute-bound" được nói như một sự thật chung.

```mermaid
flowchart LR
  B9["K4 Bài 9<br/>Pareto + sàn chất lượng"] --> B10["Bài 10<br/>3 model: adapter, ô trống có lý do"]
  B10 --> B11["Bài 11<br/>N100: ORT CPU / OV CPU / OV iGPU"]
  B11 --> B12["Bài 12<br/>roofline: tự tính trần, đo trần, đặt từng pha"]
  B12 --> B13["K4 Module 5<br/>viết, publish, reproduce"]
  F24["F2.4 differential test"] -.-> B10
  F16["F1.6 fit, residual"] -.-> B10
  F54["F5.4 tần số CPU"] -.-> B11
  F12["F1.2 phân vị, n nhỏ"] -.-> B11
  F72["F7.2 roofline"] -.-> B12
  F73["F7.3 profiling"] -.-> B12
```

---

## Bài 10 — Model thứ hai và thứ ba (6h)

> **Vị trí:** K4 Bài 9 (chọn cấu hình) → **Bài 10** → K4 Bài 11 (N100) · **Cần trước:** K4 Bài 4 (thiết kế harness), F2.4 (differential test, golden file), F1.6 (fit mô hình vào số đo, residual), F3.2 (schema evolution, cho JSON output) · **Sau bài này bạn quyết định được:** chọn bộ ba model theo độ phủ (kích thước × kiểu action head × backbone), và quyết định harness có cần refactor không, dựa trên số giờ đo được và kết quả contract test, không dựa trên cảm giác.

### 1. Câu chuyện — ai đã khổ vì chuyện này

Trước 2018, mỗi hãng phần cứng tự công bố số "inference/giây" theo cách đo của mình: model khác, batch khác, precision khác, độ chính xác không ai kiểm. Không con số nào so được với con số nào. MLPerf (nay thuộc MLCommons) ra đời để chấm dứt việc đó. Vòng inference đầu tiên (v0.5, 2019) cố định model tham chiếu, ràng buộc chất lượng, và tách bốn kịch bản đo: SingleStream, MultiStream, Server, Offline `[spec: luật MLPerf Inference]`. Bài học họ trả giá để có: **một benchmark chỉ chạy được trên một cấu hình thì không phải benchmark, mà là một phép đo.**

Ở cấp độ code, nghề phần mềm có một kinh nghiệm cũ: lần đầu viết thì cứ viết, lần thứ hai thấy lặp thì nhăn mặt nhưng vẫn viết, lần thứ ba thì refactor. Martin Fowler ghi lại "rule of three" này trong *Refactoring* và ghi công cho Don Roberts `[chuẩn]`. Model thứ hai là lúc mọi giả định ngầm về model thứ nhất lộ ra: shape cố định, chuẩn hóa action viết cứng, số camera viết cứng, "inference" mặc định là một lần forward. Model thứ ba là lúc bạn biết abstraction của mình có đúng không.

### 2. Mô hình tư duy

```mermaid
flowchart TB
  CFG["config YAML<br/>(model, precision, target, steps, batch)"] --> CORE
  subgraph CORE["Harness core — không biết model nào"]
    T["timer 3 tầng<br/>pre / infer / post"] --- TH["thermal + freq logger"] --- J["JSON writer<br/>(schema_version)"]
  end
  CORE --> AD{"Adapter interface<br/>preprocess · infer · postprocess<br/>+ metadata: chunk_size, action_dim,<br/>action_space, norm_stats, n_steps"}
  AD --> A1["SmolVLA<br/>~450M · flow-matching · chunk"]
  AD --> A2["model vài tỉ tham số<br/>(OpenVLA: autoregressive token;<br/>π0: flow-matching)"]
  AD --> A3["model cho edge<br/>(ternary / 4-bit gốc)"]
  CORE --> M["ma trận kết quả: mỗi ô = số đo HOẶC<br/>status + reason (oom, unsupported_op, ...)"]
```

Bốn ý bản chất:
1. **Interface bắt được lỗi kiểu, không bắt được lỗi nghĩa.** Hai model có thể cùng trả `(1, chunk, 7)` float32. Nhưng một cái trả action đã khử chuẩn hóa theo radian, cái kia trả giá trị chuẩn hóa trong [−1, 1], hoặc delta thay vì tuyệt đối. Harness vẫn chạy, latency vẫn đo, và trục chất lượng sẽ sập mà không ai biết vì sao. Thứ bảo vệ bạn là **differential test** với script inference gốc của từng model (→ F2.4).
2. **"Inference" không cùng một hình dạng tính toán giữa các họ model.** Có ba kiểu cơ bản. *Autoregressive* (OpenVLA): prefill ảnh + lệnh, rồi giải mã tuần tự từng token action. *Flow-matching/diffusion* (SmolVLA, π0): prefix một lần, rồi action expert chạy N bước. *Hồi quy trực tiếp có chunking* (ACT): một lần forward. Latency có cấu trúc khác nhau, và Bài 12 cho thấy chúng nằm ở chỗ khác nhau trên roofline.
3. **Latency là một mô hình affine, không phải một con số.** Với flow-matching: L(N) ≈ t_prefix + N·t_step. Quét N rồi fit, bạn có hai tham số có nghĩa vật lý thay vì một bảng. Residual có cấu trúc nghĩa là mô hình thiếu một thành phần (→ F1.6).
4. **Ô trống là dữ liệu.** `oom`, `unsupported_op`, `unsupported_dtype` là phát hiện về độ chín của tooling. Chúng phải có schema như mọi số đo khác.

Hai mô phỏng. Thứ nhất, contract test bắt một lỗi ngữ nghĩa mà kiểu dữ liệu không bắt được:

```python
# [đã chạy] Adapter cho nhiều model + contract test: kiểu đúng chưa đủ, phải kiểm NGỮ NGHĨA
from dataclasses import dataclass
import numpy as np

@dataclass
class Cell:                       # một ô của ma trận model × precision × target
    status: str                   # ok | oom | unsupported_op | unsupported_dtype | too_slow | not_attempted
    reason: str = ""

class Adapter:                    # harness chỉ biết interface này
    name = "base"; chunk_size = 1; action_dim = 7
    def preprocess(self, obs): raise NotImplementedError
    def infer(self, batch): raise NotImplementedError          # trả action ĐÃ chuẩn hóa của model
    def postprocess(self, raw): raise NotImplementedError       # trả action ĐƠN VỊ VẬT LÝ (rad, m)

class FakeFlow(Adapter):          # giả lập model chunking, action chuẩn hóa theo mean/std của dataset
    name, chunk_size = "fake_flow", 50
    mean, std = np.full(7, 0.1), np.full(7, 0.5)
    def preprocess(self, obs): return {"img": obs["img"] / 255.0, "state": obs["state"]}
    def infer(self, b): return np.tanh(b["state"].mean()) * np.ones((1, self.chunk_size, 7))
    def postprocess(self, raw): return raw * self.std + self.mean

class FakeAR(FakeFlow):           # giả lập model khác: QUÊN khử chuẩn hóa — vẫn đúng shape, đúng dtype
    name, chunk_size = "fake_ar", 1
    def postprocess(self, raw): return raw

def contract(ad, obs, ref_action=None, tol=1e-3):
    out = ad.postprocess(ad.infer(ad.preprocess(obs)))
    errs = []
    if out.shape != (1, ad.chunk_size, ad.action_dim): errs.append(f"shape {out.shape}")
    if not np.isfinite(out).all(): errs.append("NaN/inf")
    if ref_action is not None and np.abs(out[0, 0] - ref_action).max() > tol:   # differential test (→ F2.4)
        errs.append(f"lệch so với script tham chiếu: {np.abs(out[0, 0] - ref_action).max():.3f}")
    return Cell("ok") if not errs else Cell("contract_fail", "; ".join(errs))

obs = {"img": np.zeros((224, 224, 3)), "state": np.full(8, 0.3)}
ref = np.tanh(0.3) * 0.5 + 0.1          # action mà script inference GỐC của model trả ra (đơn vị vật lý)
for ad in (FakeFlow(), FakeAR()):
    print(ad.name, contract(ad, obs, ref))
```

Thứ hai, tách latency thành hai tham số và ước lượng bộ nhớ weight (chạy *sau* khi ghi dự đoán):

```python
# [đã chạy] Tách latency = t_prefix + N_step * t_step bằng hồi quy, và ước lượng bộ nhớ weight
import numpy as np
rng = np.random.default_rng(0)
# Dữ liệu GIẢ ĐỊNH: quét số solver step, mỗi mức 30 mẫu (thay bằng JSON harness của bạn)
steps = np.repeat([1, 2, 5, 10, 20], 30)
lat = 60 + 9.0*steps + 4*(steps >= 10) + rng.normal(0, 3, steps.size)   # có một "bậc" ẩn ở >=10 bước
A = np.column_stack([np.ones_like(steps), steps])
coef, *_ = np.linalg.lstsq(A, lat, rcond=None)
res = lat - A @ coef
print(f"t_prefix ≈ {coef[0]:.1f} ms, t_step ≈ {coef[1]:.2f} ms/step")
for s in np.unique(steps):                       # residual theo nhóm: phải quanh 0 nếu mô hình tuyến tính đúng
    print(f"  steps={s:2d}: residual trung bình {res[steps == s].mean():+5.2f} ms")
# Bộ nhớ weight theo precision (chỉ weight! chưa tính activation, KV cache, CUDA context, allocator)
models = {"SmolVLA ~0.45B": 0.45e9, "model ~3B": 3e9, "OpenVLA ~7B": 7e9}
bytes_per = {"fp32": 4, "bf16": 2, "int8": 1, "4-bit": 0.5}
print(f"{'':16s}" + "".join(f"{k:>9s}" for k in bytes_per))
for m, n in models.items():
    print(f"{m:16s}" + "".join(f"{n*b/2**30:8.1f}G" for b in bytes_per.values()))
```

Đọc residual theo nhóm, không đọc R². Nhóm nào lệch khỏi 0 có hệ thống là dấu vết của một thành phần mà mô hình affine không có (dữ liệu giả định ở trên cố ý cài một "bậc"; tìm nó trước khi mở 🔒 ở phần 7). Ở dữ liệu thật, bậc kiểu này có thể là một lần cấp phát bộ nhớ mới, một lần đổi kernel, hoặc cache bị tràn.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Adapter/plugin, interface + nhiều implementation | Adapter cho từng model | Ở backend, contract chủ yếu là kiểu và mã lỗi. Ở đây contract gồm cả **ngữ nghĩa số**: đơn vị, chuẩn hóa, khung tọa độ, delta hay tuyệt đối, thứ tự camera. | Bảng latency đẹp, trục chất lượng của model thứ hai bằng 0 mà không ai hiểu vì sao |
| ORM hỗ trợ nhiều DB | Harness hỗ trợ nhiều model | ORM thường chọn mẫu số chung nhỏ nhất. Ở đây mẫu số chung nhỏ nhất (một lần forward, batch 1) xóa mất thứ quan trọng nhất của từng model: số bước solver, KV cache, decode tuần tự. | So "một forward" của OpenVLA với "một forward" của SmolVLA, trong khi chúng không làm cùng một việc |
| Contract test giữa service (consumer-driven) | Differential test với script gốc của model | Giống về tinh thần. Khác ở chỗ "đúng" không phải bằng nhau tuyệt đối mà là trong dung sai số học. Dung sai phải chọn có lý do (fp32 vs bf16 khác nhau). | Dung sai quá lỏng nuốt lỗi chuẩn hóa; quá chặt thì fail vì nhiễu số học |
| Load test endpoint mới, so baseline | Thêm model, chạy cùng ma trận | Endpoint mới cùng giao thức. Model mới có thể không chạy được một nửa ma trận (dtype, op), và đó là kết quả chứ không phải sự cố. | Ngoại suy để lấp ô trống |
| Schema migration | `schema_version` của JSON khi thêm trường cho model mới | Giống (→ F3.2). Khác: kết quả cũ phải còn đọc được để so sánh. Đổi nghĩa một trường là phá lịch sử benchmark. | So số mới với số cũ khác định nghĩa |

**Chấm mô hình:**

- *"Thời gian thêm model đo chất lượng thiết kế harness: > 4h là harness có vấn đề"* (bản gốc). **ĐÚNG MỘT PHẦN.** Nó đo tổng của ba thứ: thiết kế harness, độ chín hệ sinh thái của model (có script inference chuẩn không, có trong LeRobot không), và đường cong học của bạn. **Phản ví dụ:** OpenVLA cần tải checkpoint 7B, cài phụ thuộc riêng và xử lý tokenizer action. Việc đó có thể mất hơn 4h dù harness hoàn hảo. Ghi tách: giờ cho môi trường, giờ cho adapter, giờ cho debug ngữ nghĩa. Chỉ giờ adapter mới nói về harness.
- *"Model 3B chậm hơn 450M khoảng tỉ lệ tham số"*. **ĐÚNG MỘT PHẦN.** Với pha bị chặn bởi băng thông, thời gian tỉ lệ với byte weight. Nhưng kiểu action head, số token ảnh và số bước quyết định ngang hoặc hơn số tham số. **Phản ví dụ:** model autoregressive phải đọc toàn bộ weight một lần *mỗi token action*. Model flow-matching đọc weight của expert nhỏ mỗi bước nhưng xử lý cả chunk một lượt. Cùng số tham số, hai họ có latency rất khác nhau.
- *"Model flow-matching: giảm solver step thì latency giảm gần tuyến tính"* (bản gốc). **ĐÚNG MỘT PHẦN.** Latency giảm **affine**: phần prefix không đổi. **Phản ví dụ:** nếu t_prefix = 60 ms và t_step = 9 ms, giảm từ 10 xuống 5 bước làm latency đi từ 150 ms xuống 105 ms (−30%), không phải −50%. Nếu prefix chiếm phần lớn, giảm bước gần như không giúp gì.

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | Action head: autoregressive / flow-matching / direct | Cách sinh action: token tuần tự / khử nhiễu N bước / một lần forward | Chi tiết kiến trúc không ảnh hưởng hạ tầng |
| 🟢 | Prefix / prefill | Lần xử lý ảnh + lệnh (+ state) để tạo ngữ cảnh | Toàn bộ inference |
| 🟢 | KV cache | Kết quả trung gian của prefix được giữ lại cho các bước sau | Cache ứng dụng |
| 🟢 | Solver step | Một lần chạy action expert trong flow-matching/diffusion | Một iteration benchmark |
| 🟢 | Differential test | Chạy hai implementation trên cùng đầu vào, so đầu ra | Unit test |
| 🟢 | Ma trận có ô trống + status | Mỗi ô là số đo hoặc lý do không đo được | Bảng thiếu sót |
| 🟢 | Norm stats | Mean/std hoặc min/max dùng chuẩn hóa state/action | Tham số của model |
| 🟡 | Backbone VLM (SmolVLM2, PaliGemma, Prismatic/Llama 2) | Phần vision-language được tiền huấn luyện | Một tên khác của model |
| 🟡 | Action tokenization (bin, FAST) | Biến action liên tục thành token rời rạc | Lượng tử weight |
| 🟡 | Parallel decoding (ví dụ OpenVLA-OFT) | Sinh nhiều token action một lượt thay vì tuần tự | Batch |
| 🔴 | Chi tiết huấn luyện từng model | | Thứ cần cho benchmark inference |

### 5. Dự đoán

**Tham số cần tra:**
- Danh sách policy LeRobot hiện hành: LeRobot docs, mục Policies (đổi nhanh) `[tự đo]`. Với model ngoài LeRobot (OpenVLA, openpi): README repo chính chủ.
- Với mỗi model: tổng tham số và tham số của từng phần (in từ code); kiểu action head; `chunk_size`; số solver step mặc định; số token ảnh mỗi camera (từ config processor); action space (delta/tuyệt đối, đơn vị).
- VRAM GPU thuê bạn định dùng.

**Câu hỏi:**
1. Giờ để thêm model 2 và model 3, tách theo môi trường / adapter / debug ngữ nghĩa.
2. Bảng weight bytes cho 3 model × 4 precision. Ô nào không vừa VRAM của GPU thuê *chỉ tính weight*? Ô nào có thể không vừa khi tính cả activation/KV?
3. Tỉ lệ latency p50 (model lớn / SmolVLA) cùng GPU, cùng precision. Lập luận theo byte weight và theo cấu trúc tính toán: hai lập luận cho cùng một số không?
4. t_prefix và t_step của SmolVLA trên GPU thuê. Phần trăm latency mặc định nằm ở prefix là bao nhiêu?
5. Ô nào trong ma trận sẽ trống, và vì lý do nào?

```markdown
# prediction.md — K4 Bài 10
- Bộ ba: (1) ___ [cỡ, head, backbone] (2) ___ (3) ___ — các chiều khác nhau: ___
- Giờ thêm model 2: môi trường ___ / adapter ___ / debug ___ ; model 3: ___ / ___ / ___
- Weight bytes (GiB): bảng 3×4 ___ ; ô không vừa VRAM ___ GB: ___
- Tỉ lệ p50 model lớn / SmolVLA: ___ (lập luận byte: ___ ; lập luận cấu trúc: ___)
- SmolVLA: t_prefix ___ ms, t_step ___ ms, % prefix ở cấu hình mặc định ___
- Ô trống dự đoán + lý do: ___
```

### 6. Làm

1. **Thêm model thứ hai vào harness, đo thời gian thêm.** Ghi vào `hours.csv` theo ba cột: môi trường, adapter, debug ngữ nghĩa. Nếu riêng phần adapter > 4h, harness có vấn đề thiết kế: ghi lại và refactor (giữ ngưỡng của bản gốc, áp đúng chỗ).
2. **Contract test cho mọi adapter, trước khi đo gì.** Gồm: shape `(B, chunk, action_dim)`; finite; dải action hợp lý so với norm stats; và **differential test** với script inference gốc của model trên 5 observation cố định (golden file), với dung sai ghi rõ theo precision. Không qua contract test thì ô đó là `contract_fail`, không được có số.
3. **Thêm model thứ ba.** Kỳ vọng thời gian adapter ngắn hơn rõ. Nếu không, xem lại interface.
4. **Chạy toàn bộ ma trận model × precision trên GPU thuê.** Dùng kỷ luật thuê GPU của Bài 5: script không tương tác, sync kết quả ra ngoài, hẹn giờ tắt.
5. **Với mỗi model, ghi rõ cái gì không đo được và vì sao**: `oom` (kèm peak trước khi chết), `unsupported_dtype`, `unsupported_op`, `too_slow` (kèm ước lượng thời gian), `not_attempted` (kèm lý do phạm vi). Mỗi ô trống là một dòng trong JSON, không phải một chỗ thiếu.
6. **Quét solver step cho model flow-matching** (ít nhất 5 mức), fit L(N) = t_prefix + N·t_step, báo cáo hai tham số kèm residual theo nhóm. Với model autoregressive, quét số token sinh nếu có thể (thường cố định bằng action_dim) và đo riêng thời gian prefill vs decode bằng profiler.
7. **Cảnh báo phạm vi (giữ từ bản gốc):** đừng cố chạy 6 model. Ba model đo kỹ có giá trị hơn sáu model đo hời hợt, và trần giờ của khóa là 95h.

**Gợi ý bộ ba theo nguyên tắc phủ (bản gốc, kiểm lại khi bắt đầu):** SmolVLA (~450M, flow-matching, nhẹ nhất: bắt đầu ở đây); một model vài tỉ tham số (OpenVLA ~7B autoregressive, hoặc π0 ~3B flow-matching, hoặc GR00T); một model thiết kế cho edge (dòng BitVLA hoặc tương đương). Chọn sao cho ít nhất **hai chiều** khác nhau. Ví dụ: SmolVLA + π0 cùng là flow-matching, nên cặp này chỉ khác kích thước và backbone.

**Sai số dụng cụ:** khi so model, latency mỗi ô có CI (Bài 5, Bài 6). Tỉ lệ latency giữa hai model là tỉ số của hai số có sai số. Bậc độ lớn thì an toàn, chênh lệch 10–20% giữa hai model thì phải kèm CI.

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

**Mô phỏng (đã chạy):** contract test bắt `fake_ar`: đúng shape, đúng dtype, nhưng lệch 0.046 so với script tham chiếu vì quên khử chuẩn hóa. Fit giả định ra t_prefix ≈ 60.0 ms, t_step ≈ 9.23 ms/step. Residual theo nhóm: −0.64, +0.32, −0.67, **+1.65**, −0.66 ms. Nhóm `steps=10` nổi lên, đúng chỗ có bậc ẩn.

**Weight bytes (chỉ weight, GiB):**

| | fp32 | bf16 | int8 | 4-bit |
|---|---|---|---|---|
| ~0.45B | 1.7 | 0.8 | 0.4 | 0.2 |
| ~3B | 11.2 | 5.6 | 2.8 | 1.4 |
| ~7B | 26.1 | 13.0 | 6.5 | 3.3 |

(Số tham số danh nghĩa; số thật: tự in từ checkpoint.) Một model ~7B ở fp32 không vừa GPU 24 GB chỉ riêng weight. bf16 vừa weight nhưng sát nút khi cộng activation và context.

**Kỳ vọng thực nghiệm `[tự đo]`:**

| Kiểm tra (bản gốc) | Kỳ vọng | Ghi chú |
|---|---|---|
| Thời gian thêm model thứ ba | Phần adapter ngắn hơn model thứ hai rõ | Phần môi trường có thể không ngắn hơn |
| Model vài tỉ vs 450M, cùng GPU | Chậm hơn nhiều lần, VRAM lớn hơn nhiều lần | Tỉ lệ latency không nhất thiết bằng tỉ lệ tham số |
| Flow-matching giảm solver step | Latency giảm **affine**: gần tuyến tính theo N với hệ số góc t_step, có tung độ gốc t_prefix | Bản gốc viết "gần tuyến tính", đúng theo nghĩa affine |
| Bảng kết quả | Có ô trống, mỗi ô có status + lý do | Bảng có ô trống kèm lý do trung thực hơn bảng đầy số bịa. Đừng ngoại suy |

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Model mới chạy, latency hợp lý, success rate ≈ 0 | Lỗi ngữ nghĩa: chuẩn hóa, action space, thứ tự camera, kích thước ảnh | Differential test với script gốc; vẽ action dự đoán vs action trong dataset | Sửa adapter; thêm trường ngữ nghĩa vào metadata adapter |
| Adapter model 3 vẫn mất lâu như model 2 | Interface bị may đo cho model 1 | Đếm dòng `if model == ...` trong core | Refactor: đẩy khác biệt vào adapter + metadata |
| OOM ở bf16 dù weight vừa | Activation của nhiều camera × độ phân giải; KV cache; workspace kernel | `torch.cuda.memory_summary()` ở điểm peak | Ghi `oom` + phân rã bộ nhớ; thử batch 1, ít camera hơn (ghi rõ đó là cấu hình khác) |
| Residual có cấu trúc khi quét step | Thành phần ngoài mô hình affine (cấp phát, đổi kernel, CPU sync) | Profiler ở hai mức step hai bên bậc | Báo cáo mô hình hai đoạn, hoặc nêu bậc như một phát hiện |
| t_step âm hoặc t_prefix âm | Ít mức step quá, hoặc nhiễu lớn, hoặc thermal trôi theo thứ tự đo | Xáo thứ tự đo các mức step; kiểm nhiệt (Bài 6) | Đo xen kẽ ngẫu nhiên, thêm mức step |

### 9. Câu hỏi ngược

1. **[Quy mô]** Đội của bạn phải benchmark 30 model mỗi quý, mỗi model ra phiên bản mới hàng tháng. Thiết kế adapter nào còn đứng được, và thứ gì phải tự động hóa trước tiên?
   <details><summary>Hướng nghĩ</summary>Contract test + golden file chạy trong CI cho mỗi model mới, giống hệt kiểm thử tương thích API. Metadata ngữ nghĩa (action space, chuẩn hóa) phải là dữ liệu khai báo, không phải code. Nghĩ tới chuẩn hóa từ phía nhà phát hành model: một "model card cho inference".</details>
2. **[Failure mode]** Hai model cùng được đo "batch 1, 10 solver step". Một model mặc định dùng 2 camera, model kia 3 camera. Bảng so sánh của bạn sai ở đâu, và schema JSON cần trường nào để không ai lặp lại lỗi này?
   <details><summary>Hướng nghĩ</summary>Đầu vào khác thì công việc khác. Số token ảnh là một biến điều khiển của latency. Schema cần ghi cấu hình đầu vào thực tế (số camera, độ phân giải, số token) chứ không chỉ tên model.</details>
3. **[Vì sao không]** Vì sao không export mọi model sang một định dạng chung (ONNX) rồi đo bằng một runtime duy nhất, cho "công bằng"?
   <details><summary>Hướng nghĩ</summary>Công bằng với ai? Bạn sẽ đo độ chín của exporter thay vì đo model. Vòng lặp solver, KV cache và op tùy biến thường export kém (Bài 11). Nhưng có một mặt đúng: một runtime chung loại bỏ một biến. Hỏi: câu hỏi của benchmark là "model nào nhanh" hay "model nào nhanh *trong stack người ta thật sự dùng*"?</details>
4. **[Liên ngành]** Trong hóa phân tích, một phương pháp đo mới phải được thẩm định (method validation) trên mẫu chuẩn đã biết nồng độ trước khi dùng cho mẫu thật. Differential test với script gốc tương ứng với bước nào, và còn thiếu bước nào?
   <details><summary>Hướng nghĩ</summary>Script gốc giống mẫu chuẩn tham chiếu. Thẩm định còn có độ lặp lại, độ tái lập giữa phòng lab, và dải tuyến tính. Ánh xạ: tỉ lệ lật (Bài 7), người reproduce (Module 5), quét solver step.</details>
5. **[Phản biện]** "Ô trống trong bảng làm báo cáo trông chưa xong" (đồng nghiệp ở bản Gemini). Viết câu trả lời bằng ngôn ngữ của người vận hành, không phải của người làm nghiên cứu.
   <details><summary>Hướng nghĩ</summary>Người vận hành cần biết cấu hình nào *không deploy được* và vì sao, trước khi họ thử. Một ô `oom` kèm số GB cần là thông tin mua phần cứng. Một ô bị ngoại suy là một sự cố đang chờ xảy ra.</details>

### 10. Liên kết ra ngoài

- **SPEC CPU và MLPerf.** Benchmark công nghiệp ghi kèm mọi cấu hình (compiler flag, firmware) và có quy trình duyệt bài nộp. Giống: kỷ luật "mọi số kèm cấu hình". Khác: họ có ủy ban duyệt. Bạn có một người lạ trên Discord. Vì vậy cấu hình của bạn phải đủ để người đó tự tái lập mà không cần hỏi.
- **Kiểm thử tương thích trình duyệt.** Web cùng một chuẩn nhưng mỗi engine hỗ trợ một phần, và bảng "caniuse" là ma trận có ô trống với lý do. Ma trận model × runtime × dtype của bạn là đúng loại bảng đó. Khác: tính năng web là có/không. Ở đây "hỗ trợ" còn có mức: chạy được nhưng chậm, chạy được nhưng sai số lớn.
- **Thẩm định phương pháp trong hóa phân tích.** Xem câu hỏi ngược 4. Điểm chung: một phương pháp đo chỉ được tin sau khi kiểm trên mẫu chuẩn. Điểm khác: mẫu chuẩn hóa học có giấy chứng nhận. "Mẫu chuẩn" của bạn là script của tác giả model, và chính nó cũng có thể sai.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| MLPerf Inference v0.5 (2019) với 4 kịch bản SingleStream/MultiStream/Server/Offline | [spec: tài liệu MLCommons] | |
| Rule of three trong Fowler *Refactoring*, ghi công Don Roberts | [chuẩn] | |
| SmolVLA ~450M, flow-matching, backbone SmolVLM2 | [spec: bài báo SmolVLA, Hugging Face 2025] | In số tham số thật từ checkpoint |
| OpenVLA ~7B, backbone Prismatic (SigLIP + DINOv2, Llama 2), action rời rạc thành token, sinh tuần tự | [spec: Kim và cộng sự 2024, OpenVLA] | |
| π0 ~3B (PaliGemma + action expert), flow-matching, chunk 50 | [spec: Black và cộng sự 2024, π0] — kiểm lại khi dùng | Phiên bản openpi/LeRobot có thể khác |
| Danh sách policy trong LeRobot | [tự đo] | Đổi nhanh |
| Bảng weight bytes | [ước lượng] | Chỉ weight; số tham số danh nghĩa |

**Đã sửa so với bản gốc / Gemini:**
- Bản gốc: "giảm solver step → latency giảm gần tuyến tính". Đã chính xác hóa thành affine (có t_prefix), kèm cách fit và đọc residual.
- Bản gốc: ngưỡng "> 4h thêm model" áp cho tổng giờ. Đã tách giờ môi trường / adapter / debug; ngưỡng chỉ áp cho adapter.
- Gemini: "< 2 giờ là đạt chuẩn" là con số tự đặt, không có cơ sở. Đã bỏ.
- Gemini tự kiểm tra 1: "7B FP32 trên 24 GB → OOM, ghi status". Đúng hướng. Đã thêm phân rã bộ nhớ và các status khác.
- Thêm (không có ở cả hai bản): contract test ngữ nghĩa + differential test trước khi đo; trường cấu hình đầu vào (số camera, token) trong JSON.

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** Reddi và cộng sự, *MLPerf Inference Benchmark*, ISCA 2020 (lý do và thiết kế các kịch bản). Bài báo của từng model bạn chọn (SmolVLA, OpenVLA, π0).
- **Giải thích:** LeRobot docs, mục Policies và hướng dẫn thêm policy/benchmark (đọc bản đúng phiên bản bạn cài).
- **Đào sâu (tùy chọn):** McKeeman, *Differential Testing for Software*, Digital Technical Journal, 1998.
- **Tự kiểm tra:** (1) Giải thích cho một backend engineer khác trong 5 câu: vì sao interface đúng kiểu chưa đủ để thêm model. (2) Vẽ lại sơ đồ harness/adapter từ trí nhớ, có metadata ngữ nghĩa. (3) Hai câu:
  - a) Quét SmolVLA được L(5) = 110 ms và L(10) = 155 ms. Ước lượng t_prefix, t_step, và L(2). Giảm từ 10 xuống 2 bước cắt bao nhiêu % latency?
  - b) Model A autoregressive sinh 7 token action, mỗi token đọc 14 GB weight bf16. Băng thông thực đo 800 GB/s. Cận dưới thời gian decode?

  <details><summary>Đáp án</summary>
  a) t_step = (155 − 110)/5 = 9 ms; t_prefix = 110 − 45 = 65 ms; L(2) = 83 ms. Từ 155 xuống 83 ms là −46%, không phải −80%.
  b) Mỗi token ≥ 14 GB / 800 GB/s = 17.5 ms; 7 token ≥ 122.5 ms, chưa tính prefill. Đây là cận dưới kiểu roofline (Bài 12): nhanh hơn số này thì bạn đang đo sai, hoặc runtime không đọc toàn bộ weight.
  </details>

---

## Bài 11 — Target thứ hai: CPU N100 (ONNX Runtime CPU, OpenVINO CPU, OpenVINO iGPU) (6h)

> **Vị trí:** K4 Bài 10 (ma trận 3 model trên GPU thuê) → **Bài 11** → K4 Bài 12 (roofline) · **Cần trước:** F7.2 (tự tính peak, băng thông, roofline), F5.4 (tần số CPU, governor), F1.2 + F1.3 (n nhỏ, warm-up, cô lập nhiễu), K4 Bài 1 (so latency với thời lượng chunk được thực thi), Bài 2 (bao nhiêu iteration thì p95 có nghĩa), Bài 6 (thermal), Bài 8 (quantization) · **Sau bài này bạn quyết định được:** policy của robot K7 chạy on-device trên N100, chạy trên N100 với điều kiện (runtime nào, precision nào, chunk bao nhiêu), hay phải offload/mua Jetson. Quyết định dựa trên một con số "chậm hơn ngân sách k lần" có sai số, đo trên đúng chiếc máy sẽ nằm trên robot.

### 1. Câu chuyện — ai đã khổ vì chuyện này

Năm 2017 Microsoft và Facebook công bố ONNX, một định dạng đồ thị trung gian chung cho model học sâu `[chuẩn]`. Năm 2018 Intel phát hành bộ công cụ OpenVINO và Microsoft mở mã ONNX Runtime `[chuẩn]`. Cả ba sinh ra từ cùng một nỗi khổ: model được huấn luyện trên PyTorch + GPU NVIDIA, nhưng phải chạy trên camera, PC công nghiệp, điện thoại, CPU Intel/AMD/ARM. Mỗi loại phần cứng cần thư viện kernel riêng: oneDNN cho CPU Intel, kernel OpenCL cho iGPU Intel, MLAS trong ONNX Runtime. Mỗi framework lại xuất đồ thị theo kiểu riêng. Lời giải là tách thành tầng: framework → đồ thị trung gian → runtime (tối ưu đồ thị, chọn kernel) → phần cứng. Cái giá là mỗi tầng có thể làm hỏng: op không export được, op export được nhưng không có kernel nhanh, kernel nhanh nhưng đổi precision ngầm.

Bản gốc gọi bài này là "con số gây sốc", và giữ ý đó. Lộ trình ghi rõ: **Jetson chỉ mua nếu M6 chứng minh được là cần.** Bài này là phép chứng minh. Bạn đo trên đúng chiếc N100 sẽ lên khung xe ở K7, với ba runtime miễn phí trên cùng một hộp. Kết quả âm ở đây vẫn là kết quả: "N100 chậm hơn ngân sách k lần, đã thử ba runtime và INT8" là một câu có giá trị mua sắm. Con số cụ thể nằm trong 🔒 ở phần 7. Ghi dự đoán trước.

### 2. Mô hình tư duy

```mermaid
flowchart TB
  PT["PyTorch policy<br/>(chạy được trên GPU thuê, Bài 10)"] --> EX{"export theo PHA<br/>vision+prefix · expert 1 bước"}
  EX -->|"torch.onnx.export"| ONNX["đồ thị ONNX"]
  EX -.->|"op không export được"| FB["chạy bằng PyTorch CPU<br/>(ghi status, là cấu hình khác)"]
  ONNX --> ORT["ONNX Runtime<br/>CPU Execution Provider"]
  ONNX --> OVC["OpenVINO<br/>convert_model → IR"]
  OVC --> OVCPU["plugin CPU<br/>(mặc định fp32 trên N100)"]
  OVC --> OVGPU["plugin GPU<br/>(mặc định fp16, biên dịch kernel lần đầu)"]
  ORT --> C["4 nhân Gracemont<br/>AVX2, không HT"]
  OVCPU --> C
  OVGPU --> G["iGPU 24 EU"]
  C --> R[("1 kênh DDR5<br/>+ một ngân sách công suất PL1/PL2")]
  G --> R
```

Năm ý bản chất:

1. **Runtime là một trình biên dịch đồ thị cộng một thư viện kernel.** Cùng file weight, ba runtime cho ba con số. Chênh lệch đo độ chín của *kernel và các phép biến đổi đồ thị* (fusion, layout, chọn đường AVX2 hay VNNI), không đo model. Đó là lý do phải có ba target trên một hộp: nó cô lập biến "runtime" trong khi giữ phần cứng cố định.
2. **Tính trần trước khi đo.** Mỗi pha có cận dưới thời gian t ≥ max(FLOP/π, byte/β) (→ F7.2). Số đo nhanh hơn cận dưới nghĩa là bạn đo sai: model không chạy thật, chạy ít bước hơn, hoặc đếm sai byte. Số đo chậm hơn cận dưới 10 lần là chỗ có dư địa.
3. **CPU và iGPU không độc lập.** Chúng chung một kênh RAM và chung một ngân sách công suất của gói chip. "Target thứ ba" chạy song song với ROS 2 trên CPU sẽ không cho con số của lúc chạy một mình.
4. **Tần số là một biến, không phải hằng số.** N100 tăng tốc lên turbo trong khi công suất còn dưới PL2, rồi tụt về mức PL1 do hãng máy đặt trong BIOS. Latency đo trong 10 giây đầu và sau 5 phút có thể khác nhau. Ghi tần số thật song song với mỗi mẫu latency.
5. **Con số cần ra không phải latency, mà là latency chia cho ngân sách.** Ngân sách là thời lượng phần chunk được thực thi (K4 Bài 1). Với vòng chặn (đồng bộ), tần số action thực thi là f_exec ≈ S / (L + S·Δt), trong đó S là số action thực thi mỗi chunk, Δt là chu kỳ điều khiển, L là latency khứ hồi `[spec: vla.cpp, arXiv 2606.08094, phương trình (6)]`.

**Tự tính peak N100 (bắt buộc, không chép).** Cùng công thức với F7.2, nhắc lại để bạn kiểm số trên máy mình:

```
CPU fp32  = 4 nhân × f × 16 FLOP/chu kỳ           (2 đơn vị FMA 128-bit × 4 lane fp32 × 2 FLOP/FMA)
          = 4 × (2,9…3,4) GHz × 16 ≈ 0,19…0,22 TFLOPS                      [ước lượng]
iGPU fp32 = 24 EU × 8 lane × 2 (FMA) × 0,75 GHz ≈ 0,29 TFLOPS              [ước lượng]
iGPU fp16 ≈ 2 × fp32 ≈ 0,58 TFLOPS  (Xe-LP chạy fp16 gấp đôi fp32)          [ước lượng]
β         = 4800 MT/s × 8 byte (một kênh 64-bit) = 38,4 GB/s lý thuyết      [ước lượng từ spec]
```

Tần số đồ họa tối đa 750 MHz và 24 EU lấy từ Intel ARK `[spec]` (đối chiếu Notebookcheck ghi 450–750 MHz). f của CPU khi cả 4 nhân bận lâu thường thấp hơn 3,4 GHz `[tự đo: turbostat]`.

**Micro-benchmark: đo hai trần thật.** Chạy trên laptop để làm quen, rồi chạy lại trên N100. Số của N100 là `[tự đo]`; Bài 12 dùng chúng thay cho số lý thuyết.

```python
# [đã chạy] microbench.py — đo trần TÍNH (GEMM) và trần BĂNG THÔNG (kiểu STREAM) của máy đang chạy
# Chạy trên laptop để làm quen; chạy lại trên N100 (không tải nền, đã warm-up) để lấy số [tự đo] cho Bài 12.
import os, time, json, platform
import numpy as np

def best_and_median(f, rep=7):
    f()                                               # warm-up: cấp phát, page fault, nạp thư viện BLAS
    ts = []
    for _ in range(rep):
        t0 = time.perf_counter(); f(); ts.append(time.perf_counter() - t0)
    return min(ts), float(np.median(ts))              # min = "máy làm được bao nhiêu"; median = "thường ra bao nhiêu"

out = {"host": platform.processor() or platform.machine(), "cpu_count": os.cpu_count(),
       "numpy": np.__version__}

# 1) Trần tính: GEMM fp32 n×n, FLOP = 2n³. Dùng mọi luồng BLAS (OMP/OPENBLAS_NUM_THREADS quyết định).
for n in (1024, 2048):
    A = np.random.rand(n, n).astype(np.float32); B = np.random.rand(n, n).astype(np.float32)
    tmin, tmed = best_and_median(lambda: A @ B)
    out[f"gemm{n}_gflops_best"] = round(2 * n**3 / tmin / 1e9, 1)
    out[f"gemm{n}_gflops_med"] = round(2 * n**3 / tmed / 1e9, 1)

# 2) Trần băng thông kiểu STREAM: mảng 64 Mi phần tử fp32 = 256 MB mỗi mảng, lớn hơn mọi cache.
#    Đếm byte theo quy ước STREAM: copy/scale = 2 mảng, add/triad = 3 mảng (KHÔNG đếm write-allocate).
N = 64 * 2**20
a = np.ones(N, np.float32); b = np.ones(N, np.float32); c = np.empty(N, np.float32); s = np.float32(3.0)
kernels = {
    "copy":  (lambda: np.copyto(c, a), 2),
    "scale": (lambda: np.multiply(a, s, out=c), 2),
    "add":   (lambda: np.add(a, b, out=c), 3),
    "triad": (lambda: (np.multiply(b, s, out=c), np.add(c, a, out=c)), 3),  # numpy: 2 lượt qua c → đếm thiếu byte
}
for k, (f, narr) in kernels.items():
    tmin, _ = best_and_median(f)
    out[f"stream_{k}_GBps"] = round(narr * a.nbytes / tmin / 1e9, 1)

# 3) GEMV fp32 8192² (= decode batch 1): đọc mỗi trọng số một lần → bị chặn bởi băng thông
W = np.random.rand(8192, 8192).astype(np.float32); x = np.random.rand(8192).astype(np.float32)
tmin, _ = best_and_median(lambda: W @ x)
out["gemv8192_gflops"] = round(2 * W.size / tmin / 1e9, 1)
out["gemv8192_weight_GBps"] = round(W.nbytes / tmin / 1e9, 1)

print(json.dumps(out, indent=1, ensure_ascii=False))
with open("microbench.json", "w") as fh:            # commit file này cùng kết quả Bài 11
    json.dump(out, fh, indent=1)
```

Hai điều cần biết trước khi đọc số. Phép toán từng phần tử của numpy chạy **một luồng**, nên bốn dòng `stream_*` đo băng thông mà *một nhân* kéo được. GEMV đi qua BLAS đa luồng nên gần với băng thông cả kênh hơn. Muốn số STREAM chuẩn đa luồng, biên dịch `stream.c` của John McCalpin với OpenMP (`gcc -O3 -fopenmp -DSTREAM_ARRAY_SIZE=80000000 stream.c`) `[chuẩn]`.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Cùng container chạy trên mọi máy x86 | Cùng model, ORT vs OpenVINO, CPU vs iGPU | Container đóng gói user-space, không đóng gói kernel tính. Runtime dò cờ ISA (`avx2`, `avx_vnni`) **lúc chạy** và chọn đường kernel khác nhau trên máy khác nhau | Lấy số từ laptop i7 (có thể có AVX-VNNI, nhiều nhân P) rồi "điều chỉnh" sang N100 |
| JIT warm-up của JVM | OpenVINO GPU biên dịch kernel ở lần `compile_model` đầu tiên | Warm-up JVM mất vài giây và tự lặp lại mỗi lần khởi động. Biên dịch kernel GPU có thể lâu hơn nhiều, và chỉ tránh được bằng model cache trên đĩa | Gộp thời gian biên dịch vào p50 (số sai), hoặc bỏ hẳn nó và robot K7 mất hàng chục giây mỗi lần boot mà không ai lường trước |
| Load test trên VM cloud | Benchmark trên mini PC | VM giấu tần số nhưng thường ổn định trong phiên. Mini PC tăng turbo khi công suất còn dưới PL2 rồi tụt về PL1, theo giây chứ không theo phút | Benchmark 30 s báo số của chế độ turbo, robot chạy cả giờ ở chế độ PL1 |
| Thêm thread worker để tăng throughput | `intra_op_num_threads`, `INFERENCE_NUM_THREADS` | 4 nhân, không HT, chung L2 và một kênh RAM. Quá 4 luồng là tranh chấp; ROS 2 node trên robot cũng cần nhân | Đo với 4 luồng trên máy rảnh, deploy cạnh 3 node ROS và latency tăng gấp rưỡi |
| Fallback khi feature không có | Phần không export được chạy bằng PyTorch CPU | Fallback ở backend thường cùng hiệu năng. Ở đây ranh giới hai runtime có copy tensor và mất fusion; đó là một **cấu hình khác** | Báo "OpenVINO: x ms" trong khi 40% thời gian là PyTorch |

**Chấm mô hình:**

- *"N100 nhanh hơn Pi 4 vài lần ở CPU, nhưng không nhanh hơn hai bậc"* (bản gốc). **ĐÚNG MỘT PHẦN.** Hướng đúng, nhưng "vài lần" không có đơn vị. Tỉ lệ giữa hai máy **khác nhau theo pha**: pha bị chặn bởi tính tỉ lệ với π, pha bị chặn bởi băng thông tỉ lệ với β, và tỉ lệ π khác tỉ lệ β. **Phản ví dụ:** Pi 4 dùng LPDDR4-3200 bus 32 bit (12,8 GB/s lý thuyết `[ước lượng từ spec]`). Một pha decode đọc weight sẽ tăng tốc theo tỉ lệ β, còn prefix ảnh tăng tốc theo tỉ lệ π. Tự tính π của Cortex-A72 bằng cùng công thức (nhân × f × FLOP/chu kỳ, tra tài liệu ARM), rồi so hai tỉ lệ.
- *"iGPU là GPU, nên sẽ nhanh hơn CPU"*. **ĐÚNG MỘT PHẦN.** Trần tính fp16 của iGPU cao hơn trần tính fp32 của CPU, nhưng **cùng β**. Pha memory-bound có cùng trần trên cả hai. Thêm ba khác biệt không nằm trên roofline: plugin GPU mặc định chạy fp16 (số học khác, phải qua contract test), thời gian biên dịch kernel, và độ chín kernel cho từng op. **Phản ví dụ:** một GEMV decode fp16 trên iGPU và một GEMV int8 trên CPU đọc cùng số byte mỗi weight ở mức 2 so với 1. Cái int8 trên CPU có trần cao hơn dù "không phải GPU".
- *Bản Gemini, tự kiểm 1:* "850 ms < 2,5 s (chunk 50 ở 20 Hz) nên chạy được bằng suy luận bất đồng bộ; độ trễ phản ứng tối thiểu 850 ms". **ĐÚNG MỘT PHẦN.** Điều kiện throughput đúng, với hai sửa: ngân sách là số action **thực thi** mỗi chunk (`n_action_steps`), không phải `chunk_size`; và so với đuôi (max, p95), không phải p50. Phần độ trễ phản ứng sai: quan sát được chụp trước khi suy luận, và chunk mới chỉ thay chunk cũ ở ranh giới. Một sự kiện xảy ra ngay sau lúc chụp quan sát chỉ được phản ánh sau chu kỳ suy luận kế tiếp. Trễ phản ứng xấu nhất cỡ L cộng thời lượng một đoạn thực thi, không phải L. **Phản ví dụ:** với S·Δt = 2,5 s, vật bị đẩy lệch ngay sau lúc chụp có thể chưa được phản ứng sau hơn 3 s.

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | ONNX / OpenVINO IR | Đồ thị trung gian độc lập framework / định dạng riêng của OpenVINO (`.xml` + `.bin`) | Một runtime |
| 🟢 | Execution Provider (ORT), device plugin (OV) | Phần nối runtime với một loại phần cứng và thư viện kernel của nó | Driver |
| 🟢 | Peak (tự tính) vs sustained (micro-benchmark) | Trần lý thuyết vs trần đo được | Số trên spec sheet là số đạt được |
| 🟢 | PL1 / PL2 | Giới hạn công suất dài hạn / ngắn hạn của gói chip, hãng máy đặt trong BIOS | Giới hạn nhiệt |
| 🟢 | `Bzy_MHz` (turbostat) | Tần số trung bình trong lúc nhân bận | `scaling_cur_freq` (là tần số được yêu cầu, có thể khác tần số thật) |
| 🟢 | Weight-only INT8 vs W8A8 | Chỉ nén weight / nén cả weight lẫn activation, cần dữ liệu hiệu chuẩn | Cùng một thứ "INT8" |
| 🟢 | Ngân sách chunk, f_exec | Thời lượng phần chunk được thực thi; số action thực thi mỗi giây đồng hồ | Chu kỳ điều khiển |
| 🟡 | `INFERENCE_PRECISION_HINT`, `PERFORMANCE_HINT` | Thuộc tính OpenVINO chọn precision tính và chế độ latency/throughput | Tham số model |
| 🟡 | Model cache (`CACHE_DIR`) | Lưu kernel/đồ thị đã biên dịch để lần sau khỏi biên dịch lại | Cache kết quả inference |
| 🟡 | NNCF | Thư viện nén của OpenVINO (weight compression, post-training quantization) | Một runtime |
| 🟡 | AVX2, AVX-VNNI | Lệnh vector 256-bit; lệnh tích vô hướng int8 tăng tốc INT8 | Có trên mọi CPU x86 |
| 🔴 | Chi tiết oneDNN/MLAS, OpenCL kernel tuning | | Thứ cần cho bài này |

### 5. Dự đoán

**Tham số cần tra:**
- Intel ARK trang "Intel Processor N100": số nhân, Max Turbo Frequency, cache, Max Memory Channels, Graphics Max Dynamic Frequency, số EU. RAM thật: `sudo dmidecode -t memory` (tốc độ cấu hình, số khe dùng). Cờ ISA: `lscpu | grep -o 'avx2\|fma\|avx_vnni'`.
- PL1/PL2 thật của máy bạn: `cat /sys/class/powercap/intel-rapl:0/constraint_*_power_limit_uw` và `constraint_*_name` `[tự đo: đường dẫn có thể khác theo kernel]`.
- Với model nhỏ nhất của bộ ba (Bài 10): tham số từng phần, số token ảnh mỗi camera, độ phân giải ảnh vào encoder (trong config của policy), số camera, `num_steps`, `chunk_size`, `n_action_steps`.
- Bảng mốc của K4 Bài 2 (Pi 4, CPU desktop). t_prefix và t_step trên GPU thuê (Bài 10).

**Câu hỏi:**
1. π CPU (khi 4 nhân bận), π iGPU fp32/fp16, β lý thuyết.
2. Micro-benchmark trên N100: GEMM đạt bao nhiêu % π? GEMV đạt bao nhiêu GB/s, tức bao nhiêu % β? `stream_copy` một luồng so với GEMV đa luồng?
3. Cận dưới latency của model nhỏ nhất, fp32, trên N100 CPU: ước FLOP của từng pha (≈ 2 × tham số × số token xử lý, cộng attention nếu đáng kể), chia cho π *đo được*. Pha nào chiếm phần lớn?
4. p50 cho ba runtime (ORT CPU, OV CPU, OV iGPU). Xếp hạng. Tỉ lệ N100 / GPU thuê ở cùng model.
5. INT8 tăng tốc bao nhiêu lần trên mỗi runtime, và pha nào được lợi?
6. `Bzy_MHz` sau 5 phút chạy liên tục so với 3,4 GHz. `PkgWatt` so với PL1.
7. Con số gây sốc: latency / 100 ms (10 Hz, gốc), và latency / ngân sách chunk. Theo quy tắc Jetson của lộ trình, kết luận của bạn là gì?

```markdown
# prediction.md — K4 Bài 11
- Peak: CPU ___ TFLOPS (f = ___ GHz) ; iGPU fp32 ___ / fp16 ___ ; β ___ GB/s ; ridge CPU ___
- Micro-benchmark N100: GEMM ___ GFLOP/s (___% π) ; GEMV ___ GB/s (___% β) ; copy 1 luồng ___ GB/s
- Cận dưới latency fp32 CPU: vision ___ s + prefix ___ s + expert×steps ___ s = ___ s ; pha lớn nhất ___
- p50: ORT CPU ___ ; OV CPU ___ ; OV iGPU ___ ; xếp hạng ___ ; N100/GPU ≈ ___ lần
- INT8: ORT ___× ; OV CPU ___× ; OV iGPU ___× ; pha được lợi ___
- Bzy_MHz sau 5 phút ___ ; PkgWatt ___ W vs PL1 ___ W
- Chậm hơn 10 Hz ___ lần ; so với ngân sách chunk ___ lần ; kết luận Jetson: ___
```

### 6. Làm

**Bước 0 — Chuẩn bị máy (30 phút).** Ghi môi trường bằng script `capture_env` của K4 Bài 14. Governor: `cpupower frequency-info`, đặt `performance` nếu được (ghi lại nếu không). Kiểm iGPU: `ls /dev/dri` phải có `renderD128`; trong Docker cần `--device /dev/dri` và user thuộc nhóm `render` `[tự đo]`. Tắt mọi tải nền, kể cả ROS 2, cho phép đo "một mình". Phép đo "cạnh ROS 2" là một cấu hình riêng, làm sau nếu còn giờ.

**Bước 1 — Micro-benchmark (30 phút).** Chạy `microbench.py` ba lần, commit `microbench.json`. Tùy chọn: STREAM C đa luồng. Sai số: perf_counter có độ phân giải dưới 1 µs, không đáng kể so với phép đo cỡ ms. Biến thiên giữa các lần chạy đến từ tần số, nhiệt và vị trí trang bộ nhớ. Báo min và median kèm số lần chạy (→ F1.3).

**Bước 2 — Chọn model nhỏ nhất trong bộ ba** (gốc). Đừng bắt đầu bằng model 3B: mỗi iteration có thể mất hàng chục giây đến hàng phút.

**Bước 3 — Export theo pha** (gốc, sửa cách làm). Đừng cố export cả vòng solver thành một đồ thị. Export hai đồ thị: (a) vision + prefix, (b) **một bước** action expert. Chạy vòng `num_steps` bằng Python. Cách này vừa tránh lỗi export vòng lặp, vừa cho thời gian từng pha mà Bài 12 cần. Nếu một phần export thất bại, **ghi op nào thất bại** (status `unsupported_op` + tên op + phiên bản torch/onnx). Chạy phần đó bằng PyTorch CPU, và đánh dấu ô là cấu hình lai.

```python
# [chưa chạy] cần N100 + onnxruntime + openvino; API đổi theo phiên bản — [tự đo], kiểm theo bản bạn cài
import numpy as np, onnxruntime as ort, openvino as ov

so = ort.SessionOptions()
so.intra_op_num_threads = 4                                   # 4 nhân, không HT
so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
s_ort = ort.InferenceSession("expert_step.onnx", so, providers=["CPUExecutionProvider"])

core = ov.Core()
print(core.available_devices)                                 # mong thấy ['CPU', 'GPU']
core.set_property({"CACHE_DIR": "ov_cache"})                  # tránh biên dịch lại kernel GPU mỗi lần
m = core.read_model("expert_step.onnx")                       # hoặc ov.convert_model(...)
for dev in ("CPU", "GPU"):
    cm = core.compile_model(m, dev, {"PERFORMANCE_HINT": "LATENCY"})
    print(dev, cm.get_property("INFERENCE_PRECISION_HINT"))   # GHI vào JSON: precision thật đang chạy
    req = cm.create_infer_request()
    # req.infer({...}) trong vòng đo; lần compile đầu tiên ghi riêng làm t_cold
```

**Bước 4 — Contract test trên từng runtime (thêm so với gốc).** Dùng golden file của Bài 10: 5 observation cố định, so action của mỗi runtime với PyTorch CPU fp32. Dung sai ghi theo precision: iGPU chạy fp16 phải có dung sai riêng. Không qua thì ô là `contract_fail`, không có số. Lý do: một runtime "nhanh" vì tính sai thì không phải runtime nhanh (→ K4 Bài 8, chuyện encoder nhạy precision).

**Bước 5 — Ít iteration hơn, báo cáo đúng với n nhỏ** (gốc). Latency thang giây thì 200 iteration là vô lý: 5 warm-up, 20–30 lần đo. Theo K4 Bài 2: với n = 30, báo p50, max và n. Chỉ báo p95 khi n ≥ 72. Ghi trong `METHODOLOGY.md` rằng n nhỏ nên khoảng tin cậy rộng. Với OV GPU, thời gian `compile_model` lần đầu (không cache) và lần có cache ghi thành hai trường cold-start riêng.

**Bước 6 — Tần số và công suất thật suốt phép đo** (gốc, sửa công cụ). Chạy song song với benchmark:

```bash
# [chưa chạy] cần N100 + linux-tools; tên cột đổi theo phiên bản turbostat — [tự đo]
sudo turbostat --quiet --interval 1 --show Time_Of_Day_Seconds,Busy%,Bzy_MHz,PkgTmp,PkgWatt,GFXWatt,GFXMHz \
     --out turbostat.log &
python bench_n100.py --runtime ov --device CPU --iters 30 --warmup 5 --out results/smolvla_fp32_n100_ov.json
```

`scaling_cur_freq` là tần số governor *yêu cầu*. `Bzy_MHz` của turbostat tính từ bộ đếm chu kỳ thật, nên dùng nó. Ghép hai log theo timestamp: latency từng mẫu và `Bzy_MHz`/`PkgWatt` của giây đó. Bản Gemini đưa cột `RAMWatt`. Trên chip client như N100, miền RAPL DRAM thường không có. Thiếu cột không phải lỗi `[tự đo]`. Không chỉ nhìn `dmesg`: hạ xung do giới hạn công suất không để lại dòng log nào.

**Bước 7 — RAM peak và swap** (gốc). `/usr/bin/time -v` cho "Maximum resident set size". Chạy `vmstat 1` song song: cột `si`/`so` khác 0 là đang swap, và số latency lúc đó vô nghĩa, phải nói rõ. Với iGPU, bộ nhớ GPU lấy từ RAM hệ thống và có thể không hiện trong RSS. Xem thêm `free -m` trước/sau.

**Bước 8 — Một mức nén** (gốc). ORT: `onnxruntime.quantization.quantize_dynamic` (weight int8, activation lượng tử động). OpenVINO: `nncf.compress_weights` (weight-only) hoặc `nncf.quantize` với tập hiệu chuẩn vài chục observation (W8A8) `[tự đo: API theo phiên bản]`. Đo lại, ghi tỉ lệ tăng tốc **theo pha**. Kiểm INT8 có chạy thật không: OV có thống kê từng layer (`PERF_COUNT`, xem kiểu kernel và precision thực thi). Lại contract test.

**Bước 9 — Con số quan trọng nhất** (gốc). Nếu control loop cần 10 Hz, N100 chậm hơn yêu cầu bao nhiêu lần: tính `p50/100 ms` và `max/100 ms`. Thêm phép so đúng hơn (K4 Bài 1, Bài 9): latency so với ngân sách chunk = `n_action_steps × Δt`, và f_exec cho vòng chặn. Áp quy tắc của lộ trình: Jetson chỉ mua nếu sau khi đã thử INT8, OpenVINO và iGPU, cấu hình tốt nhất trên N100 vẫn không vào ngân sách chunk với sàn chất lượng của Bài 9.

**Bước 10 — Ghi kết quả.** Mỗi runtime × precision là một JSON trong `results/`, theo schema Bài 10. Nếu chạy được nhưng quá chậm để đo LIBERO thì: latency đo trên N100, chất lượng đo trên GPU, và **báo cáo ghi rõ hai trục đo trên hai target khác nhau** (gốc). Contract test ở bước 4 là bằng chứng hai target tính cùng một hàm.

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

**Peak tự tính `[ước lượng]`:** CPU 0,19 TFLOPS ở 2,9 GHz, 0,22 ở 3,4 GHz. iGPU 0,29 TFLOPS fp32, ~0,58 fp16. β 38,4 GB/s. Ridge CPU ≈ 5 FLOP/byte.

**Micro-benchmark trên máy soạn giáo trình** (laptop i7-13700H, 14 nhân / 20 luồng, numpy 2.2.6, Windows, **không phải N100**; ba lần chạy):

| | Lần 1 | Lần 2 | Lần 3 |
|---|---|---|---|
| GEMM 2048² fp32, best | 487 GFLOP/s | 328 | 433 |
| GEMV 8192² fp32 | 18 GFLOP/s (37 GB/s) | 19 (38) | 22 (44) |
| stream copy, 1 luồng | 28 GB/s | 22 | 25 |
| stream triad, 1 luồng (đếm thiếu) | 13 GB/s | 12 | 14 |

Đọc: GEMM/GEMV chênh hơn 20 lần trên cùng máy, cùng thư viện. Lần 2 thấp hơn lần 1 tới 30% trên laptop (tần số, nhiệt, nền), đúng lý do phải báo nhiều lần chạy. Triad numpy báo thấp vì đi hai lượt qua `c` nhưng chỉ đếm 3 mảng.

**Kỳ vọng trên N100 `[ước lượng — tự đo]`:** GEMM cỡ 50–80% π nếu BLAS dùng đủ 4 nhân và đường AVX2/FMA. GEMV/STREAM đa luồng cỡ 60–80% của 38,4 GB/s. Một luồng thấp hơn rõ, vì một nhân E-core không đủ yêu cầu bộ nhớ treo để lấp kênh.

**Cận dưới latency (ví dụ SmolVLA, chỉ để kiểm cách tính `[ước lượng]`):** nếu encoder ảnh là SigLIP-B/16 ở 512×512 (1024 patch, ~86M tham số trong transformer), một camera ≈ 2·86M·1024 ≈ 0,18 TFLOP, cộng attention ~0,04 TFLOP. Tức là **riêng vision ≈ 1 s mỗi camera ở π lý thuyết của N100 CPU**. Prefix LM và expert × 10 bước cộng thêm vài trăm GFLOP. Với 2 camera, cận dưới fp32 cỡ **3 s**. Số thật cao hơn vì không kernel nào đạt 100% π. Đối chiếu bảng mốc Bài 2 (CPU desktop i5-8500T ~7 s cho SmolVLA). Kiểm lại độ phân giải và số camera trong config của bạn: mọi thứ tỉ lệ với hai số đó.

**Bảng kỳ vọng của bản gốc (giữ nguyên):**

| Kiểm tra | Kỳ vọng |
|---|---|
| Latency N100 CPU, model nhỏ, FP32 | Nhiều khả năng thang **trăm ms tới giây** (theo cận dưới ở trên, nghiêng về **giây**) |
| Latency N100, model 3B | Có thể thang **chục giây tới phút**, hoặc không chạy nổi vì RAM |
| iGPU vs CPU qua OpenVINO | Có thể nhanh hơn, có thể không: **đo, đừng đoán** |
| Tăng tốc nhờ INT8 | Thang **vài lần** (sau Bài 12: chỉ ở pha memory-bound; pha compute-bound chỉ nhanh nếu có kernel int8 thật, ví dụ AVX-VNNI) |
| Hạ xung | Có khả năng khi chạy liên tục. Ghi lại, đừng che |
| Khoảng cách N100 vs GPU thuê | **Một tới vài bậc độ lớn** |

**Con số gây sốc:** với latency thang giây và 10 Hz, N100 chậm hơn yêu cầu **hàng chục lần** nếu chạy đồng bộ mỗi tick. So với ngân sách chunk (ví dụ 50 action × 50 ms = 2,5 s), khoảng cách nhỏ hơn nhiều, có thể vào được. Nhưng phải trả bằng phản ứng chậm (phần 3, chấm mô hình 3) và chất lượng có thể giảm khi thực thi cả chunk không quan sát lại. vla.cpp báo SmolVLA trên LIBERO-Object tụt rõ khi S = H = 50 so với S nhỏ hơn `[spec: arXiv 2606.08094, Hình 5]`.

**Kiểm tra tỉnh táo (gốc):** nếu N100 chỉ chậm hơn GPU 2–3 lần với model lớn, dừng lại. Gần như chắc chắn đo nhầm: đo cache, model không thực sự chạy, hoặc chạy ít bước solver hơn. Thêm: nếu số đo nhanh hơn cận dưới FLOP/π, phép đo sai.

**Mốc Pi 4 (bản gốc dẫn, chưa truy nguồn `[tự đo]`):** SmolVLM-256 fp32 ~11 s mỗi lần inference; LiteVLA fp32 ~18 phút mỗi forward; NF4 backbone + projection head fp32 ~2 phút.

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Hết RAM, process bị kill | Model quá lớn | `dmesg` có OOM killer; RSS peak | **Đây là kết quả** (gốc): ghi RAM cần vs RAM có, status `oom` |
| Latency biến thiên cực mạnh | Hạ xung, swap (gốc) | Ghép latency với `Bzy_MHz`, `PkgWatt`, `vmstat si/so` | Báo phân bố, không báo một số; tách cửa sổ turbo và PL1 |
| Phân bố hai đỉnh, đỉnh nhanh ở đầu phiên | Turbo dưới PL2 rồi tụt về PL1 | `PkgWatt` theo thời gian | Warm-up đủ lâu để vào trạng thái dừng, hoặc báo cả hai chế độ |
| ONNX export thất bại | Op chưa hỗ trợ, vòng lặp solver (gốc) | Thông báo lỗi exporter | Ghi op; export theo pha; chạy phần lỗi bằng PyTorch CPU và nói rõ |
| `available_devices` không có `GPU` | Thiếu driver compute (Level Zero/OpenCL), thiếu quyền `/dev/dri` | `ls -l /dev/dri`, `clinfo` | Cài runtime GPU của Intel, thêm nhóm `render`; trong Docker `--device /dev/dri` `[tự đo]` |
| iGPU lần đầu cực chậm, lần sau nhanh | Biên dịch kernel | Đo `compile_model` riêng | `CACHE_DIR`; ghi cold-start riêng |
| iGPU qua contract test với fp32 nhưng lệch lớn ở fp16 | Precision mặc định của plugin GPU | `INFERENCE_PRECISION_HINT` | Ghi; thử ép f32 làm cấu hình riêng |
| ORT chậm hơn OV nhiều lần | Số luồng mặc định, thiếu fusion, đường kernel khác | ORT profiling (`enable_profiling`), so số luồng thật | Đặt luồng = 4; ghi phiên bản; đó có thể là kết quả thật |
| INT8 không nhanh hơn | Pha compute-bound không có kernel int8; hoặc lượng tử không được áp | `PERF_COUNT` từng layer: precision thực thi | Ghi theo pha; xem Bài 12 |
| GEMM micro-benchmark rất thấp | BLAS một luồng hoặc bản numpy không tối ưu | `np.show_config()`, biến `OPENBLAS_NUM_THREADS` | Đặt luồng; ghi bản BLAS vào JSON |
| Quá chậm để đo LIBERO | Bình thường (gốc) | | Latency trên N100, chất lượng trên GPU, nói rõ hai trục hai target |

### 9. Câu hỏi ngược

1. **[Quy mô]** Đội 100 robot, mỗi con một N100, cùng chạy policy on-device. So với một GPU server chung qua Wi-Fi, cái gì gãy trước ở mỗi kiến trúc, và con số nào từ bài này quyết định ranh giới?
   <details><summary>Hướng nghĩ</summary>

   On-device: không cần mạng, nhưng chậm, và mỗi lần đổi model là deploy 100 máy. Server: nhanh, gom batch được (Bài 12: tăng I), nhưng latency đuôi của Wi-Fi và hàng đợi (→ F7.1). Ranh giới là khi `L_n100` vượt ngân sách chunk trong khi `L_server + RTT_p99` thì không. Thêm câu hỏi: robot làm gì khi mất mạng?

   </details>
2. **[Failure mode]** Ở K7, TTS (K3) chạy trên CPU trong khi policy chạy trên iGPU. Mỗi cái chạy riêng đều vào ngân sách. Chạy cùng lúc thì hỏng theo cách nào, và bạn đo trước bằng cách nào ngay trong bài này?
   <details><summary>Hướng nghĩ</summary>

   Chung β và chung PL1. Pha memory-bound của cả hai chia nhau kênh RAM; công suất iGPU ăn vào ngân sách của CPU nên `Bzy_MHz` tụt. Thí nghiệm: chạy `microbench.py` (GEMV) trên CPU song song với benchmark iGPU, so với chạy riêng. Ghi đó là một cấu hình.

   </details>
3. **[Vì sao không]** Vì sao không mua luôn Jetson rồi đo trên đó, cho nhanh, thay vì tốn 6 giờ chứng minh N100 không đủ?
   <details><summary>Hướng nghĩ</summary>

   Mua trước thì không bao giờ biết N100 có đủ không, và không có lý do định lượng cho quyết định. Hỏi ngược: nếu Jetson nhanh hơn 5 lần mà N100 chậm hơn ngân sách 20 lần thì Jetson cũng không cứu được. Con số của bài này nói phải tìm cải thiện *bao nhiêu lần*, và đó là tiêu chí chọn phần cứng.

   </details>
4. **[Nếu…thì]** Nếu bạn vào BIOS nâng PL1 từ mức mặc định lên gấp đôi, số nào trong bảng đổi, số nào không, và cái giá nằm ở đâu trên robot?
   <details><summary>Hướng nghĩ</summary>

   Pha compute-bound nhanh lên nếu f tăng; pha memory-bound gần như không đổi (β không đổi). Cái giá: nhiệt trong hộp kín trên khung xe, dòng từ nguồn 12 V, thời lượng pin (→ K7). Chỉ kết luận khi đã đo `Bzy_MHz` ở trạng thái dừng.

   </details>
5. **[Liên ngành]** Trong hàng không, chuẩn DO-178C đòi một phần kiểm thử chạy trên phần cứng đích, không chỉ trên máy phát triển. Ngành game mobile duy trì "device farm" máy cấu hình thấp. Hai ngành này giống và khác bài của bạn ở đâu?
   <details><summary>Hướng nghĩ</summary>

   Giống: hành vi trên máy đích không suy ra được từ máy phát triển. Khác: hàng không quan tâm tính đúng và thời gian xấu nhất (WCET, → F5.3); game quan tâm phân bố khung hình trên hàng nghìn loại máy. Bạn có một máy đích, nên vấn đề của bạn là độ biến thiên theo trạng thái (nhiệt, PL1), không theo loại máy.

   </details>
6. **[Phản biện]** Đồng nghiệp: "Benchmark VLA trên N100 vô nghĩa, ai cũng biết nó chậm. Cứ chọn model nhỏ hơn là xong." Trả lời bằng số.
   <details><summary>Hướng nghĩ</summary>

   "Ai cũng biết" không có đơn vị. Model nhỏ hơn nhỏ hơn bao nhiêu? Cận dưới FLOP/π cho biết cần giảm FLOP bao nhiêu lần (ít camera hơn, độ phân giải thấp hơn, ít bước hơn) để vào ngân sách, và trục chất lượng (Bài 9) cho biết cái giá.

   </details>

### 10. Liên kết ra ngoài

- **Hàng không: kiểm thử trên phần cứng đích.** DO-178C phân biệt kiểm thử trên máy chủ với kiểm thử tích hợp trên máy tính đích `[chuẩn]`. Giống: số trên máy phát triển không phải bằng chứng cho máy đích. Khác: hàng không đòi cận trên thời gian thực thi (WCET) có chứng minh. Bạn chỉ có phân bố thực nghiệm với n = 30, nên viết "max trong 30 lần", không viết "trường hợp xấu nhất".
- **Phát triển app mobile cho máy cấu hình thấp.** Đội Android tối ưu cho máy RAM ít, CPU yếu, và đo trên máy thật vì giới hạn nhiệt của điện thoại thay đổi hiệu năng theo phút. Giống: turbo ngắn hạn và giới hạn công suất dài hạn. Khác: app có thể giảm chất lượng hình ảnh để giữ FPS. Policy robot giảm "chất lượng" (ít bước, ít camera) là thay đổi hành vi điều khiển, phải đo lại trục chất lượng.
- **HPC: performance portability.** Khi một mã khoa học chuyển sang kiến trúc mới, người ta đo cùng mã trên nhiều backend (OpenMP, CUDA, SYCL) và báo cáo hiệu suất so với trần của từng máy, không so thời gian tuyệt đối. Giống: ba runtime trên một hộp. Khác: HPC có thời gian tối ưu hàng tháng; bạn có 6 giờ, nên mục tiêu là đo đúng, không phải tối ưu xong.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| ONNX (2017, Microsoft + Facebook); OpenVINO và mã nguồn ORT (2018) | [chuẩn] | |
| N100: 4 nhân/4 luồng, turbo 3,4 GHz, 6 MB cache, 1 kênh RAM; iGPU 24 EU, tối đa 750 MHz | [spec: Intel ARK] | ARK chặn tải tự động khi soạn; số EU/tần số đối chiếu Notebookcheck (450–750 MHz) |
| Gracemont 16 FLOP fp32/chu kỳ; peak CPU 0,19–0,22 TFLOPS; iGPU ~0,29 fp32, ~0,58 fp16 | [ước lượng] | Nhất quán với F7.2; kiểm bằng micro-benchmark |
| EQ12 một khe SO-DIMM DDR5-4800, β 38,4 GB/s | [spec, nguồn thứ ba] + [ước lượng] | `dmidecode` |
| Pi 4 LPDDR4-3200 bus 32 bit → 12,8 GB/s | [ước lượng từ spec] | Tra tài liệu Raspberry Pi |
| Plugin OV CPU mặc định fp32 trên N100, GPU mặc định fp16 | [tự đo] | `INFERENCE_PRECISION_HINT` |
| API ORT/OV/NNCF trong bài | [tự đo] | Đổi theo phiên bản |
| Cột turbostat, đường dẫn powercap | [tự đo] | Đổi theo kernel/phiên bản |
| f_exec ≈ S/(L + S·Δt); SmolVLA tụt chất lượng ở S = H = 50 | [spec: vla.cpp, arXiv 2606.08094] | Đã đọc đoạn liên quan; điều kiện thí nghiệm của họ khác |
| Cận dưới vision SmolVLA (🔒) | [ước lượng] | Phụ thuộc độ phân giải, số camera trong config |
| Mốc Pi 4 (🔒) | [tự đo] | Bản gốc dẫn, chưa truy nguồn |
| Micro-benchmark (🔒) | [đã chạy] | Trên laptop i7-13700H, không phải N100 |

**Đã sửa so với bản gốc / Gemini:**
- Bản gốc: "N100 nhanh hơn Pi 4 vài lần" → chấm ĐÚNG MỘT PHẦN; tỉ lệ khác nhau theo pha (π vs β), bắt tự tính.
- Bản gốc: "theo dõi `scaling_cur_freq`" ngang hàng với turbostat → `scaling_cur_freq` là tần số yêu cầu; dùng `Bzy_MHz` (theo ghi chú hợp nhất: kiểm throttle bằng turbostat, không chỉ `dmesg`).
- Gemini: lệnh turbostat có `RAMWatt`, `Bclk` → bỏ; miền RAPL DRAM thường không có trên chip client `[tự đo]`.
- Gemini tự kiểm 1: dùng `chunk_size` và p50 làm ngân sách; "độ trễ phản ứng tối thiểu = L" → sửa thành `n_action_steps × Δt`, so với đuôi, trễ phản ứng xấu nhất ≈ L + một đoạn thực thi.
- Gemini: "máy 3 triệu", "Jetson 8–10 triệu" → bỏ giá; giá không phải dữ kiện của bài.
- Thêm (không có ở cả hai bản): tự tính peak + micro-benchmark làm trần; export theo pha; contract test trên từng runtime (iGPU fp16); cold-start biên dịch GPU tách riêng; quy tắc báo cáo n = 30 theo Bài 2; quy tắc Jetson viết thành điều kiện kiểm được.

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** Intel ARK "Intel Processor N100"; OpenVINO documentation, mục Performance Hints và GPU Device; ONNX Runtime documentation, mục Threading và Quantization (đọc bản đúng phiên bản).
- **Giải thích:** John D. McCalpin, STREAM benchmark (trang chính thức của STREAM, Đại học Virginia) cho cách đếm byte và luật chạy. Trang man `turbostat(8)`.
- **Đào sâu (tùy chọn):** vla.cpp: *A Unified Inference Runtime for Vision-Language-Action Models*, arXiv 2606.08094 (có backend CPU và phần chunk/execution horizon).
- **Tự kiểm tra:** (1) Giải thích cho một backend engineer trong 5 câu vì sao ba runtime trên cùng một máy cho ba con số, và con số nào trong ba số là "của N100". (2) Vẽ lại sơ đồ stack ở phần 2 từ trí nhớ, đánh dấu chỗ CPU và iGPU dùng chung tài nguyên. (3) Hai câu:
  - a) Một pha có 120 GFLOP. Micro-benchmark GEMM trên N100 đo được 130 GFLOP/s. Harness báo pha đó mất 0,6 s. Bạn kết luận gì?
  - b) Policy cần 2,8 s mỗi chunk trên N100, `n_action_steps = 25`, Δt = 50 ms, vòng chặn. f_exec bằng bao nhiêu? Chạy bất đồng bộ thì có vào ngân sách không?

  <details><summary>Đáp án</summary>

  a) Cận dưới = 120/130 ≈ 0,92 s > 0,6 s. Số đo nhanh hơn trần đo được: đếm FLOP thừa (ví dụ đếm 2 camera nhưng chạy 1), model chạy ít bước hơn cấu hình, hoặc đồng hồ bấm sai chỗ. Không phải "runtime giỏi".
  b) f_exec ≈ 25 / (2,8 + 25 × 0,05) = 25 / 4,05 ≈ 6,2 action/s, so với 20 Hz danh nghĩa. Bất đồng bộ: ngân sách 25 × 50 ms = 1,25 s < 2,8 s, nên **không** vào, kể cả ở p50.

  </details>

---
