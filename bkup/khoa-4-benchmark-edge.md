# KHÓA 4 — ĐO HIỆU NĂNG INFERENCE TRÊN EDGE

**Cho:** người đã PASS Khóa 2 (biết MCAP, schema, đọc dataset robot). Khóa 1 và 3 **không phải điều kiện bắt buộc**.
**Thời lượng:** ~70h · **Trần:** 95h. Khoảng 10–12 tuần ở nhịp 6–7h/tuần.
**Chi phí:** thuê GPU ~500k–1.5tr. **Không mua phần cứng gì.**
**Tương ứng:** milestone **M6** — artifact ★ thứ hai.

**Xong khóa này bạn có:** một harness benchmark công khai, một báo cáo có số đo thật trên nhiều model và nhiều loại phần cứng, một bài viết tiếng Anh, và ít nhất một người lạ trên internet đã chạy lại và xác nhận số của bạn.

**Vì sao khóa này quan trọng hơn nó trông:** đây là khóa duy nhất bạn **làm đúng công việc 8 năm qua, chỉ đổi payload**. Benchmark, p99, thermal isolation, reproducibility — bạn đã làm những thứ này cả sự nghiệp. Khác biệt duy nhất là thay vì đo một API endpoint, bạn đo một policy điều khiển robot. ROI trên mỗi giờ cao nhất trong toàn lộ trình.

**Entry:** M2 PASS. Không cần phần cứng, không bị chặn bởi ship hàng, làm được trong tuần crunch.

---

## VỊ TRÍ TRONG BẢN ĐỒ

| Khóa | Tên | Giờ | Cần gì | Track |
|---|---|---|---|---|
| 1 | Từ zero đến đo được | 35 | Đợt 1 | C |
| 2 | Dữ liệu robot mà không cần robot | 80 | Không | **B** |
| 3 | Chuỗi audio | 90 | Đợt 2 | C |
| **4** | **Đo hiệu năng inference trên edge** | **70** | **Thuê GPU** | **B** |
| 5 | Cảm biến, đồng bộ thời gian, data platform | 150 | Đợt 3 | C |
| 6 | Robot learning với SO-101 | 120 | Đợt 4 | C |

Khóa 4 thuộc Track B cùng với Khóa 2 — nhanh ra artifact, không bị chặn bởi phần cứng. **Nếu bạn phải chọn giữa Khóa 3 và Khóa 4 vì thiếu giờ, chọn Khóa 4.**

---

## MỘT LƯU Ý VỀ THỜI ĐIỂM

Lĩnh vực này đang chuyển động rất nhanh. Mọi con số trong tài liệu này là **mốc đối chiếu tại thời điểm viết**, không phải chân lý. Việc đầu tiên bạn làm ở Bài 1 là kiểm tra lại chúng còn đúng không — và nếu chúng đã lỗi thời, đó là thông tin quý, không phải phiền toái.

Điều **không** thay đổi là phương pháp đo. Đó mới là thứ bạn đang mua bằng 70 giờ.

---

## CẤU TRÚC KHÓA

| Module | Nội dung | Giờ |
|---|---|---|
| **1** | Nền tảng: VLA là gì, đo cái gì, đo thế nào | 10 |
| **2** | Harness | 14 |
| **3** | Trục chất lượng — phần khiến benchmark của bạn khác người khác | 16 |
| **4** | Nhiều model, nhiều target | 18 |
| **5** | Publish và reproduce | 12 |

Giữ nguyên định dạng sáu phần: **Câu hỏi · Khái niệm · Làm · Số phải ra · Nếu ra khác · Tự kiểm tra**.

---

# MODULE 1 — NỀN TẢNG (10h)

---

## Bài 1 — VLA model là cái gì, ở mức tensor (3h)

**Câu hỏi:** khi người ta nói "chạy một VLA", chính xác là chạy cái gì?

### Khái niệm

Bỏ hết marketing đi. Ở mức bạn cần, một VLA (Vision-Language-Action model) là một hàm:

```
(ảnh từ N camera, vector trạng thái robot, câu lệnh ngôn ngữ) → chuỗi hành động
```

Ba chi tiết quyết định mọi thứ về hiệu năng:

**1. Nó không trả về một hành động, nó trả về một chunk.** Phần lớn VLA hiện đại xuất ra một *chuỗi* hành động cho nhiều bước tương lai (action chunking), ví dụ 30–50 bước. Điều này thay đổi hoàn toàn ý nghĩa của "latency": model chạy ở 4Hz vẫn có thể điều khiển robot ở 30Hz, vì mỗi lần chạy cho ra 50 bước để tiêu dần.

**Đây là điều đầu tiên phải hiểu**, vì nếu không, bạn sẽ báo cáo "model này chỉ 4 FPS, không dùng được" trong khi thực tế nó dùng được.

**2. Kiến trúc thường có hai phần chạy với chi phí rất khác nhau.** Một backbone vision-language (nặng, chạy một lần mỗi observation) và một action expert (nhẹ hơn, nhưng với model flow-matching/diffusion thì chạy **nhiều lần** — mỗi solver step một lần). Nghĩa là latency tổng = prefix một lần + expert × số solver step. Số solver step là một tham số bạn có thể vặn, và nó là một trục trong benchmark của bạn.

**3. Kích thước rất khác nhau.** SmolVLA là ~450M tham số, được thiết kế để chạy trên phần cứng tiêu dùng, nhỏ hơn khoảng một bậc so với các model tuyến đầu (thường 3–7B). Model 3B và model 450M không cùng một bài toán hạ tầng.

### Làm

1. Cài LeRobot, load `lerobot/smolvla_base`. **Chưa benchmark gì.**
2. Chạy inference một lần trên một observation giả. In ra **shape của mọi tensor đầu vào và đầu ra**. Ghi vào `notes/01-model-anatomy.md`.
3. Đọc config: `chunk_size` là bao nhiêu? Số solver step là bao nhiêu? Có bao nhiêu camera đầu vào?
4. Đọc danh sách policy hiện có trong docs LeRobot. Ghi lại tên và kích thước của ít nhất 6 model.
5. **Kiểm tra lại các con số mốc ở Bài 2 xem còn đúng không.** Lĩnh vực này đổi nhanh.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Shape ảnh đầu vào | Thường `(B, N_cam, 3, H, W)` hoặc tách riêng từng camera |
| Shape state | `(B, state_dim)` — với SO-101 6 khớp + gripper thì `state_dim` ≈ 6–8 |
| Shape action đầu ra | `(B, chunk_size, action_dim)` ← **phải là 3 chiều**. Nếu bạn thấy 2 chiều, model không chunking. |
| Số tham số SmolVLA | ~450M |

Nếu shape action chỉ có 2 chiều, dừng lại và đọc lại config — bạn đang hiểu sai model, và mọi benchmark sau đó sẽ đo sai thứ.

### Tự kiểm tra

1. *Model chạy 4Hz với chunk_size=50 điều khiển được robot ở tần số nào?* → Về lý thuyết tới 200Hz, nhưng thực tế bị giới hạn bởi việc chunk cũ trở nên lỗi thời khi thế giới thay đổi. Đó là lý do có replanning.
2. *Vì sao model flow-matching chậm hơn model xuất action trực tiếp dù cùng số tham số?* → Vì action expert phải chạy lại ở mỗi solver step.
3. *Giảm số solver step làm gì với latency và với chất lượng?* → Latency giảm gần tuyến tính; chất lượng giảm. Đây chính là một đường cong bạn sẽ đo ở Module 3.

---

## Bài 2 — Đo cái gì, và những con số hợp lý trông như thế nào (3h)

**Câu hỏi:** benchmark của tôi ra 800ms. Số đó tốt hay tệ?

### Khái niệm

Đây là câu hỏi bạn đã hỏi tôi từ đầu — "newbie không biết thế nào là đúng". Với benchmark, cách duy nhất để biết là **có mốc đối chiếu**. Dưới đây là các mốc công khai tại thời điểm viết. Nhiệm vụ của bạn ở Bài 1 là kiểm tra chúng còn đúng không.

**Bảng mốc đối chiếu — dán lên tường**

| Model | Phần cứng | Cấu hình | Số đo công bố |
|---|---|---|---|
| GR00T-N1.6-3B | Jetson AGX Orin | PyTorch eager | 3,3 FPS, latency p50 ≈ 306 ms |
| LiteVLA-Edge | Jetson Orin-class | 4-bit GGUF + llama.cpp | ~150 ms trung bình (≈6,6 Hz), chạy hoàn toàn offline trong pipeline ROS 2 |
| VLA-0 | RTX 5090 | PyTorch chuẩn, streaming action | 4 Hz |
| GR00T N1 với FAST decoding | — | parallel decoding | nhanh hơn tới ~2,5×, latency mỗi bước xuống dưới 5 ms, đánh đổi bằng độ mượt quỹ đạo |
| SmolVLM-256 | **Raspberry Pi 4** | FP32 | **~11 giây mỗi lần inference** |
| LiteVLA | **Raspberry Pi 4** | FP32 | **~18 phút mỗi forward pass** |
| LiteVLA | **Raspberry Pi 4** | 4-bit NF4 backbone + FP32 projection head | **~2 phút** (nhanh hơn ~9×) |
| BitVLA | — | ternary weights + INT8 activations | bộ nhớ giảm ~4,4× so với OpenVLA-OFT, chất lượng tương đương |
| BitVLA trên vla.cpp | Từ GPU tiêu dùng tới module nhúng 8GB | ternary | 100% thành công trên LIBERO-Object trong 1,3 GiB bộ nhớ |

**Ba điều phải rút ra từ bảng này trước khi viết dòng code nào:**

**Thứ nhất — độ trễ VLA nằm ở thang trăm mili-giây, không phải mili-giây.** Nếu bạn đo ra 5ms cho một model 3B trên phần cứng tiêu dùng, bạn đo sai (nhiều khả năng đang đo một phần của pipeline, hoặc đang đo cache).

**Thứ hai — Pi 5 chạy VLA sẽ ra số kinh khủng, và đó chính là kết quả.** Con số trên Pi 4 là 11 giây cho model nhỏ và tới 18 phút cho model lớn hơn ở FP32. Pi 5 nhanh hơn nhưng không nhanh hơn hai bậc. **Đừng coi đây là thất bại của thí nghiệm** — nó trả lời câu hỏi "có chạy VLA trên SBC 2 triệu được không" bằng một con số thay vì một ý kiến. Đó chính xác là giá trị của benchmark.

**Thứ ba — khoảng cách giữa phần cứng là vài bậc độ lớn, và quantization thu hẹp được một phần đáng kể.** Bậc độ lớn là bạn bè của bạn: khi khoảng cách lớn đến vậy, sai số 10% của phép đo không làm hỏng kết luận.

**Chỉ số phải báo cáo:**

| Chỉ số | Định nghĩa | Vì sao |
|---|---|---|
| **p50 / p95 / p99 latency** | Phân vị của thời gian một lần inference | Robot sống chết vì worst case, không vì trung bình |
| **RTF** hoặc Hz | Tần số inference bền vững | Nối với control loop rate |
| **VRAM / RAM peak** | Bộ nhớ đỉnh | Quyết định model có vừa phần cứng không |
| **Throughput** | Inference/giây ở batch > 1 | Cho kịch bản offline/simulation |
| **Nhiệt độ và trạng thái throttle** | Trong suốt phép đo | Nếu không cô lập, mọi số đều vô nghĩa |

**Không báo cáo mean.** Lộ trình ghi rõ điều này và nó đúng. Trung bình che giấu đuôi phân bố, và đuôi phân bố chính là thứ làm robot mất ổn định. Nếu bạn chỉ báo cáo mean, người đọc có kinh nghiệm sẽ biết ngay bạn chưa từng vận hành hệ thống thật.

### Làm

1. Tra lại từng dòng trong bảng mốc. Cập nhật cái nào đã lỗi thời. Ghi nguồn và ngày tra.
2. Với mỗi mốc, tính ngược: nếu một control loop cần 30Hz, model nào đáp ứng được ở dạng thô, model nào cần chunking, model nào không thể?
3. Viết `prediction.md` cho toàn khóa: **bạn dự đoán SmolVLA chạy bao nhiêu ms trên GPU thuê, và bao nhiêu trên Pi 5?** Commit trước khi đo bất cứ thứ gì.

### Tự kiểm tra

1. *Model p50 = 100ms nhưng p99 = 900ms. Vấn đề gì?* → Có một nguồn jitter lớn: có thể là thermal throttle, garbage collection, tranh chấp tài nguyên, hoặc swap. p99 gấp 9 lần p50 là dấu hiệu hệ thống chưa được cô lập.
2. *Vì sao báo cáo "trung bình 120ms" là không đủ với một robot?* → Vì robot có deadline. Nếu 1% số lần chạy mất 800ms và control loop cần 100ms, robot mất ổn định 1% thời gian — nghe thì nhỏ, nhưng ở 30Hz là 18 lần mỗi phút.

---

## Bài 3 — Methodology: phần quan trọng nhất của cả khóa (4h)

**Câu hỏi:** làm sao biết con số mình đo là của model chứ không phải của môi trường?

### Khái niệm

Đây là bài đáng giá nhất trong 70 giờ, và là tiêu chí PASS số 3 của M6. Lộ trình nói thẳng: **methodology là phần quan trọng nhất, không phải con số.**

Lý do rất thực tế: con số của bạn sẽ lỗi thời trong sáu tháng. Phương pháp của bạn thì không. Và khi một nhà tuyển dụng đọc repo của bạn, họ không kiểm tra xem 306ms có đúng không — họ kiểm tra xem bạn có biết 306ms nghĩa là gì không.

**Bốn nguồn nhiễu phải xử lý:**

**1. Warm-up.** Lần chạy đầu tiên bao gồm: nạp weight vào VRAM, biên dịch kernel CUDA, cấp phát bộ nhớ, có thể cả JIT. Nó có thể chậm gấp nhiều lần lần thứ hai. Quy tắc: bỏ N lần đầu, và **chứng minh N đủ lớn** bằng cách vẽ latency theo số thứ tự iteration — nó phải phẳng ra trước khi bạn bắt đầu đếm.

**2. Thermal throttling.** Chip giảm xung khi nóng. Trên Pi: `vcgencmd measure_temp` và `vcgencmd get_throttled` (bạn đã dùng ở Khóa 3, Bài 6 — cùng công cụ, khác ngữ cảnh). Trên GPU: `nvidia-smi` cho nhiệt độ, power draw, và clock. **Phải ghi nhiệt độ trong suốt phép đo, không chỉ trước và sau.**

Tiêu chí PASS đòi **số chứng minh đã cô lập được** — ví dụ nhiệt độ ổn định ±2°C xuyên suốt. Đây là chỗ phần lớn benchmark nghiệp dư trượt.

**3. Tần số CPU/GPU không cố định.** Governor có thể đổi xung giữa chừng. Ghim tần số nếu có thể; nếu không, ghi lại rằng bạn không ghim được và đo độ biến thiên.

**4. Tiến trình khác.** Chạy benchmark trên máy đang mở Chrome là vô nghĩa. Ghi lại tải nền và cách bạn kiểm soát nó.

**Một nguồn nhiễu thứ năm ít ai nói:** với model flow-matching/diffusion, **độ chính xác số học có thể im lặng làm sai kết quả**. Nhóm vla.cpp báo cáo rằng runtime của họ rất nhạy với cấu hình precision thấp trong các encoder đa phương thức — sai số làm tròn nhỏ ở vision tower có thể tích lũy qua các solver step và làm lệch hành động vật lý của robot, tới mức họ phải chặn ở tầng build. Nghĩa là: **một cấu hình có thể chạy nhanh hơn, không báo lỗi, và cho ra hành động sai.** Module 3 tồn tại vì lý do này.

### Làm

Viết `METHODOLOGY.md` trước khi viết harness. Nội dung bắt buộc:

```markdown
## Phần cứng
- CPU/GPU model, RAM/VRAM, driver version, CUDA version
- Hệ điều hành, kernel version
- Làm mát: thụ động / chủ động / loại nào

## Phần mềm
- Phiên bản của mọi thư viện liên quan (pin bằng lockfile)
- Commit hash của model checkpoint

## Quy trình đo
- Warm-up: N iteration, kèm bằng chứng N đủ (đồ thị)
- Số iteration đo: M, kèm lý do M đủ (khoảng tin cậy)
- Cách cô lập nhiệt: mô tả + số đo chứng minh
- Cách cố định tần số: mô tả hoặc thừa nhận không làm được
- Tải nền: cách kiểm soát và cách xác minh

## Sai số của phép đo
- Độ phân giải đồng hồ dùng để đo
- Overhead của chính code đo
- Độ biến thiên giữa các lần chạy lặp lại (chạy toàn bộ benchmark 3 lần, báo cáo độ lệch)

## Cái tôi KHÔNG đo và vì sao
```

Mục cuối cùng là mục làm bạn khác người khác. Một benchmark trung thực nói rõ giới hạn của nó.

### Số phải ra

| Kiểm tra | Ngưỡng chấp nhận |
|---|---|
| Nhiệt độ biến thiên trong suốt phép đo | **±2°C** ← tiêu chí PASS |
| Cờ throttle | Không bật lần nào trong lúc đo |
| Chênh lệch p50 giữa 3 lần chạy toàn bộ benchmark | <5% |
| Latency phẳng sau warm-up | Đồ thị cho thấy rõ điểm phẳng |

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Nhiệt độ tăng đều suốt phép đo | Đo quá lâu liên tục | Chèn nghỉ giữa các iteration, hoặc chia thành nhiều đợt ngắn có nghỉ, ghi rõ trong methodology |
| p50 lệch >5% giữa 3 lần chạy | Chưa cô lập đủ | Tìm nguồn nhiễu còn lại — thường là tiến trình nền hoặc governor |
| Latency giảm dần mãi không phẳng | Warm-up chưa đủ, hoặc có cache đang ấm dần | Tăng N, kiểm tra xem có cache nào không nên có |
| GPU thuê cho số khác nhau giữa các phiên | Máy ảo khác nhau, nhiễu từ tenant khác | **Ghi lại điều này.** Đây là giới hạn thật của GPU thuê và phải nêu trong báo cáo |

### Tự kiểm tra

1. *Vì sao phải chạy toàn bộ benchmark 3 lần chứ không chỉ tăng số iteration?* → Tăng iteration giảm nhiễu *trong* một phiên. Chạy lại toàn bộ phát hiện nhiễu *giữa* các phiên — thay đổi trạng thái máy, driver, tenant khác trên GPU thuê.
2. *Benchmark của bạn cho p50 = 95ms, của người khác cho 140ms cho cùng model cùng GPU. Ai đúng?* → Có thể cả hai. Câu hỏi đúng là: hai methodology khác nhau ở đâu? Đây là lý do METHODOLOGY.md tồn tại.

---

# MODULE 2 — HARNESS (14h)

---

## Bài 4 — Thiết kế harness (5h)

**Câu hỏi:** làm sao để người khác chạy lại được bằng một lệnh?

### Khái niệm

Đây là phần đúng nghề bạn nhất trong toàn bộ lộ trình. Tôi sẽ không dạy bạn viết code — tôi sẽ nêu các yêu cầu mà một harness benchmark tốt phải thỏa, vì đó là chỗ người ta hay làm hụt.

**Yêu cầu:**

1. **Một lệnh chạy được.** `python bench.py --config configs/smolvla_a100.yaml`. Không có bước thủ công nào.
2. **Cấu hình bằng file, không bằng flag.** File config được commit cùng kết quả. Người đọc biết chính xác bạn chạy gì.
3. **Output JSON có schema.** Không phải log người đọc. Kết quả phải parse được, so sánh được, vẽ được. Bạn đã làm schema versioning ở Khóa 2 — dùng lại tư duy đó.
4. **Ghi toàn bộ ngữ cảnh vào output**, không chỉ số đo: phiên bản thư viện, commit hash, nhiệt độ trước/trong/sau, tải nền, thời điểm chạy.
5. **Idempotent và resumable.** Benchmark dài có thể đứt. Chạy lại không được ghi đè kết quả cũ.
6. **Tách rõ ba tầng thời gian:**
   - `t_preprocess` — chuẩn bị đầu vào
   - `t_inference` — chỉ forward pass
   - `t_postprocess` — decode ra action
   
   Người ta hay báo cáo gộp rồi so sánh với số của người khác vốn chỉ đo tầng giữa. Tách ra, và báo cáo cả ba.

**Gợi ý schema output:**

```json
{
  "schema_version": "1.0",
  "run_id": "...",
  "timestamp_utc": "...",
  "model": {"name": "smolvla_base", "params": 450000000, "revision": "<commit>"},
  "target": {"device": "RTX 4090", "driver": "...", "cuda": "..."},
  "config": {"precision": "fp16", "batch_size": 1, "solver_steps": 10, "chunk_size": 50},
  "warmup_iters": 20,
  "measured_iters": 200,
  "latency_ms": {
    "preprocess": {"p50": 0.0, "p95": 0.0, "p99": 0.0},
    "inference":  {"p50": 0.0, "p95": 0.0, "p99": 0.0},
    "postprocess":{"p50": 0.0, "p95": 0.0, "p99": 0.0},
    "end_to_end": {"p50": 0.0, "p95": 0.0, "p99": 0.0}
  },
  "memory": {"peak_vram_mb": 0, "peak_ram_mb": 0},
  "thermal": {"temp_start_c": 0, "temp_max_c": 0, "temp_end_c": 0, "throttled": false},
  "quality": null,
  "notes": ""
}
```

Trường `quality` để `null` ở Module 2 và được điền ở Module 3. Đặt sẵn chỗ cho nó ngay từ đầu là một quyết định thiết kế có chủ đích — nó nhắc bạn rằng benchmark chưa xong.

### Làm

1. Viết harness theo yêu cầu trên.
2. Viết test: chạy với một model giả (một hàm `sleep` có phân bố biết trước) và kiểm tra harness báo cáo đúng phân vị.
3. Chạy harness trên chính máy của bạn với model giả 3 lần, kiểm tra tính ổn định.

### Số phải ra

Với model giả `sleep(0.1)` cộng nhiễu Gaussian σ=5ms, chạy 200 iteration:

| Chỉ số | Giá trị đúng |
|---|---|
| p50 | ≈ 100 ms |
| p95 | ≈ 108 ms |
| p99 | ≈ 112 ms |
| Overhead của chính harness | <1 ms, và **phải được đo và ghi lại** |

Bước test với model giả là bước hầu hết người ta bỏ qua, và nó là lý do nhiều benchmark báo cáo sai phân vị. Bạn không thể tin một công cụ đo chưa được hiệu chuẩn — đúng nguyên tắc của Khóa 1, chỉ đổi dụng cụ.

---

## Bài 5 — Đo model đầu tiên trên GPU thuê (5h)

**Câu hỏi:** SmolVLA chạy bao nhiêu ms trên một GPU thật?

### Khái niệm

**Không mua GPU.** Thuê vast.ai hoặc runpod theo giờ. Ngân sách 500k–1.5tr cho cả khóa là đủ nếu bạn kỷ luật: chuẩn bị mọi thứ ở local, thuê máy, chạy, tải kết quả về, tắt máy.

**Kỷ luật thuê GPU — viết thành checklist và dán cạnh màn hình:**

```
[ ] Dockerfile / script setup đã test ở local (dùng CPU) trước khi thuê
[ ] Config file đã viết xong và commit
[ ] Script chạy toàn bộ benchmark không cần tương tác
[ ] Kết quả tự động sync ra ngoài (S3/HF Hub) phòng khi máy bị thu hồi
[ ] Đặt hẹn giờ tự tắt máy
[ ] Ghi giờ thuê và chi phí vào hours.csv / costs.csv
```

Máy spot có thể bị thu hồi giữa chừng. Harness resumable ở Bài 4 tồn tại vì lý do này.

### Làm

1. Chọn một GPU phổ thông, dễ để người khác lặp lại (RTX 3090/4090 hoặc A10 — đừng chọn card hiếm).
2. Chạy SmolVLA qua harness: fp32, bf16, fp16. Mỗi cấu hình 200 iteration sau 20 warm-up.
3. Vẽ đồ thị latency theo iteration index để **chứng minh warm-up đủ**.
4. Quét `batch_size` 1, 2, 4, 8 — đo throughput.
5. Quét số solver step nếu model cho phép.
6. Ghi `nvidia-smi` mỗi giây trong suốt phép đo, vẽ nhiệt độ và power.

### Số phải ra

Với SmolVLA (~450M) trên GPU tiêu dùng hiện đại, batch 1:

| Cấu hình | Latency p50 kỳ vọng | Ghi chú |
|---|---|---|
| fp32 | thang 100–400 ms | Mốc tham chiếu |
| bf16 / fp16 | nhanh hơn fp32 đáng kể | Tăng tốc tùy kiến trúc và card |
| batch 8 | latency mỗi request tăng, throughput tổng tăng | Đường cong quen thuộc |

**Kiểm tra tỉnh táo bắt buộc:** so với mốc ở Bài 2. VLA-0 chạy 4 Hz trên RTX 5090 với PyTorch chuẩn — nghĩa là 250 ms. Nếu bạn đo SmolVLA (nhỏ hơn nhiều) ra 5 ms, bạn đang đo nhầm; nếu ra 3 giây, có gì đó chặn bạn. Cả hai trường hợp đều phải điều tra trước khi đi tiếp.

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| fp16 **không** nhanh hơn fp32 | Model chưa thực sự chạy fp16, hoặc bị bound bởi phần khác (preprocess, data transfer) | Xem lại tách ba tầng thời gian ở Bài 4 |
| Latency dao động mạnh | Chia sẻ GPU với tenant khác | Thử máy khác, và **ghi lại hiện tượng** — nó là dữ liệu về giới hạn của GPU thuê |
| VRAM peak lớn hơn nhiều so với kích thước model | Activation memory + KV cache + batch | Bình thường. Ghi lại tỉ lệ, nó hữu ích cho người khác |
| Batch lớn không tăng throughput | Bị bound bởi compute chứ không phải bandwidth | Đây là một phát hiện thật — xem Bài 12 |

---

## Bài 6 — Cô lập nhiệt và chứng minh bằng số (4h)

**Câu hỏi:** làm sao chứng minh được với người lạ rằng phép đo của bạn không bị nhiễu nhiệt?

### Khái niệm

Tiêu chí PASS số 3 đòi: methodology mô tả rõ warm-up và cách cô lập thermal throttling, **kèm số chứng minh đã cô lập được**.

"Tôi có để quạt" không phải bằng chứng. Một đồ thị nhiệt độ phẳng ±2°C trong suốt 200 iteration thì là.

### Làm

1. Ghi nhiệt độ mỗi giây trong suốt mọi phép đo. Lưu vào cùng file kết quả, không phải file riêng.
2. Vẽ ba đường chồng lên nhau theo thời gian: **latency**, **nhiệt độ**, **clock**. Nếu latency tăng đúng lúc nhiệt độ tăng, bạn chưa cô lập được.
3. **Cố tình tạo throttle để biết nó trông như thế nào.** Trên GPU thuê: chạy liên tục không nghỉ 15 phút. Trên Pi: bỏ tản nhiệt hoặc chạy trong hộp kín. Ghi lại đồ thị của trường hợp xấu.
4. So hai đồ thị — đã cô lập vs chưa cô lập — trong báo cáo. Đây là một hình rất thuyết phục.

### Số phải ra

| Kiểm tra | Đã cô lập | Chưa cô lập |
|---|---|---|
| Biến thiên nhiệt độ | ±2°C | Tăng đơn điệu hàng chục độ |
| Cờ throttle | Không bật | Bật |
| Tương quan latency–nhiệt độ | Không có | Rõ ràng |
| p99/p50 | Gần nhau | p99 tách xa |

---

# MODULE 3 — TRỤC CHẤT LƯỢNG (16h)

Đây là module khiến benchmark của bạn khác với 90% benchmark khác trên internet, và là module tôi khuyên bạn dành nhiều giờ nhất nếu phải cắt scope ở chỗ khác.

**Luận điểm của cả module, nói một lần cho rõ:** đo độ trễ mà không đo chất lượng là một tuyên bố nửa vời. Bất kỳ kỹ thuật nén nào cũng làm model nhanh hơn — và một policy đã hỏng thì chạy cực nhanh. Một benchmark chỉ có trục latency không phân biệt được "tối ưu tốt" với "làm hỏng model".

---

## Bài 7 — LIBERO: đo chất lượng mà không cần robot (5h)

**Câu hỏi:** làm sao biết model vẫn hoạt động sau khi nén, khi tôi không có robot?

### Khái niệm

Đây là câu trả lời trực tiếp cho lo lắng bạn nêu ở đầu: **bạn không cần robot để đo chất lượng policy.** LIBERO là benchmark mô phỏng phổ biến nhất cho VLA, chạy hoàn toàn trên máy, và cho ra một con số khách quan: **tỉ lệ thành công theo nhiệm vụ**.

Có các biến thể được thiết kế để đánh giá khắt khe hơn — LIBERO-PRO và LIBERO-Plus nhắm vào tính bền vững và tránh tình trạng model chỉ học thuộc. LeRobot cũng tích hợp sẵn nhiều benchmark khác (Meta-World, RoboCasa, RoboTwin...).

**Giới hạn phải nói rõ trong báo cáo:** LIBERO là mô phỏng. Thành công trong sim không đảm bảo thành công thật. Nhưng nó **đủ để so sánh tương đối giữa các cấu hình của cùng một model** — mà đó chính xác là thứ benchmark quantization cần.

Nêu giới hạn này trong bài viết là điểm cộng, không phải điểm trừ.

### Làm

1. Cài môi trường LIBERO qua tích hợp của LeRobot.
2. Chạy SmolVLA baseline (fp32 hoặc bf16) trên một suite LIBERO. Ghi tỉ lệ thành công **theo từng nhiệm vụ**, không chỉ trung bình.
3. Cố định seed. Chạy 3 lần với cùng seed → phải ra kết quả giống nhau. Nếu không, có nguồn ngẫu nhiên chưa kiểm soát.
4. Chạy với 3 bộ seed khác nhau → ghi độ biến thiên. Đây là sai số của phép đo chất lượng.
5. Thêm trường `quality` vào JSON output của harness.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Cùng seed, 3 lần chạy | Kết quả **giống hệt**. Nếu khác, tìm nguồn ngẫu nhiên |
| Khác seed | Biến thiên vài phần trăm — ghi lại làm sai số |
| Có nhiệm vụ luôn thất bại ở mọi cấu hình | **Bình thường và đáng ghi.** Đó là thất bại thật của model, không phải của runtime |

Điểm cuối quan trọng. Nhóm làm benchmark VLA trên Intel báo cáo rằng một nhóm seed thất bại trên **mọi** runtime — đó là thất bại thật của policy, độc lập với cách chạy. Tách nhóm đó ra trước khi so sánh các runtime, nếu không nó sẽ làm nhiễu kết luận.

---

## Bài 8 — Quantization: fp32 → 4-bit (6h)

**Câu hỏi:** nén model xuống thì được gì và mất gì, bằng số?

### Khái niệm

Thang precision bạn sẽ đi qua:

| Mức | Ghi chú |
|---|---|
| fp32 | Mốc chuẩn |
| bf16 / fp16 | Thường gần như miễn phí về chất lượng trên GPU hiện đại — **nhưng xem cảnh báo bên dưới** |
| int8 (PTQ) | Post-training quantization, nhanh và dễ |
| int8 (PTQ + QAT) | Thêm quantization-aware training để phục hồi độ chính xác |
| 4-bit (NF4, GGUF Q4) | Nén mạnh, thường cần giữ một số lớp ở precision cao |
| ternary / 1-bit | Cần model được huấn luyện cho nó từ đầu (như BitVLA), không phải nén model thường |

**Ba bài học từ tài liệu công khai, đáng đọc kỹ:**

**1. Trung bình không đổi không có nghĩa là không đổi.** Một bản GR00T-N1.6 nén INT8 (PTQ + QAT) trên Jetson AGX Orin cho tỉ lệ thành công trung bình **giống hệt** bản FP16 (61,07% cả hai) — nhưng từng nhiệm vụ thì dịch chuyển: có nhiệm vụ tăng gần 6 điểm, có nhiệm vụ `stack_cube` giảm từ 6,5% xuống 4,0%. Nếu chỉ báo cáo trung bình, bạn kết luận "INT8 miễn phí". Báo cáo theo nhiệm vụ, bạn thấy nó **dịch chuyển hành vi**, không phải bảo toàn nó.

Đây là phát hiện đáng để làm trọng tâm bài viết của bạn.

**2. Nén không phải lúc nào cũng làm giảm chất lượng, và đó là dấu hiệu cần cẩn thận.** Trong benchmark VLA trên Intel nêu trên, cấu hình INT8-CPU đạt tỉ lệ thành công **cao hơn** fp32 (75% vs 70%) — và nhóm tác giả nói rõ họ **không** tuyên bố INT8 "thắng". Khi mẫu nhỏ, chênh lệch vài phần trăm nằm trong nhiễu. Kỷ luật này là thứ phân biệt một báo cáo đáng tin với một bài marketing.

**3. Precision thấp có thể làm sai một cách im lặng.** Nhóm vla.cpp báo cáo runtime của họ nhạy với cấu hình precision thấp trong encoder đa phương thức: sai số làm tròn nhỏ ở vision tower tích lũy qua các solver step của flow-matching và làm lệch hành động vật lý — nghiêm trọng tới mức họ phải chặn ở tầng build.

Nghĩa là fp16 **không phải lúc nào cũng miễn phí**, và cách duy nhất biết được là đo trục chất lượng. Đây là toàn bộ lý do Module 3 tồn tại.

### Làm

1. Với SmolVLA, chạy ≥4 mức precision. Với mỗi mức, đo **cả hai trục**: latency (Module 2) và LIBERO success rate theo nhiệm vụ (Bài 7).
2. Dùng **cùng bộ seed** cho mọi cấu hình. Không so sánh được nếu seed khác.
3. Lập bảng: precision × (p50, p95, p99, VRAM, success rate tổng, success rate theo nhiệm vụ).
4. Vẽ đồ thị hai trục: latency trên trục X, success rate trên trục Y. Mỗi cấu hình là một điểm. **Đây là hình chính của bài viết.**
5. Tìm và ghi lại ít nhất một cấu hình thuộc dạng "nhanh hơn nhưng hỏng" — nếu không tìm được, nén sâu hơn cho tới khi tìm được.

### Số phải ra

| Kiểm tra | Kỳ vọng |
|---|---|
| VRAM giảm theo precision | Gần tuyến tính với số bit của weight |
| Latency giảm theo precision | Giảm, nhưng **không** tuyến tính — phụ thuộc kernel có hỗ trợ không |
| Success rate | Có thể giữ nguyên ở int8, **phải** giảm ở mức nén rất sâu nếu model không được huấn luyện cho nó |
| Chênh lệch success rate giữa các seed | Ghi lại — đây là ngưỡng để biết chênh lệch nào là thật |

**Quy tắc diễn giải, cam kết trước:** chênh lệch success rate nhỏ hơn độ biến thiên giữa các seed thì **không được gọi là cải thiện hay suy giảm**. Viết quy tắc này vào METHODOLOGY.md trước khi nhìn kết quả.

### Nếu ra khác

| Triệu chứng | Ý nghĩa |
|---|---|
| int8 không nhanh hơn fp16 | Kernel int8 không được dùng thực sự, hoặc bị bound ở chỗ khác. Kiểm tra bằng profiler |
| 4-bit nhanh hơn nhiều nhưng success rate sập | **Đây là kết quả bạn đang tìm.** Ghi lại và làm nó thành trọng tâm |
| Mọi mức precision cho success rate y hệt nhau | Nghi ngờ: có thể quantization chưa thực sự được áp dụng. Kiểm tra kích thước file weight |

---

## Bài 9 — Đường cong Pareto và bẫy "nhanh nhưng hỏng" (5h)

**Câu hỏi:** cấu hình nào thực sự tốt hơn?

### Khái niệm

Với hai trục, không có "tốt nhất" — có **mặt Pareto**. Một cấu hình chỉ bị loại nếu có cấu hình khác vừa nhanh hơn vừa tốt hơn. Phần còn lại là đánh đổi, và việc chọn điểm nào phụ thuộc ràng buộc của ứng dụng.

Bạn đã làm việc này ở tầng API. Đây là cùng một hình, đổi trục.

**Và đây là chỗ nối với Khóa 3:** ở Bài 10 của Khóa 3 bạn vẽ latency vs underrun rate và chọn điểm vận hành kèm lý do. Ở đây bạn vẽ latency vs success rate và làm điều tương tự. Cùng một kỹ năng, cùng một kỷ luật viết `decisions.md`. Khi phỏng vấn, hai hình này cạnh nhau kể một câu chuyện rất mạnh: **người này đo đánh đổi và quyết định bằng số, ở cả tầng hệ thống lẫn tầng model.**

### Làm

1. Vẽ mặt Pareto cho mọi cấu hình đã đo.
2. Đánh dấu các điểm bị loại (dominated) và giải thích tại sao.
3. Với ba ràng buộc giả định khác nhau, chọn ba điểm khác nhau và viết lý do:
   - *"Control loop 10Hz, chạy trên GPU workstation"*
   - *"Chạy trên module nhúng 8GB, chấp nhận 5Hz"*
   - *"Chạy offline để đánh giá hàng loạt, chỉ quan tâm throughput"*
4. Viết mục `decisions.md` cho từng ràng buộc.

### Số phải ra

Không có số đúng — có **lập luận đúng**. Mỗi lựa chọn phải nêu được: ràng buộc là gì, cấu hình nào thỏa, trong số thỏa thì cái nào tốt nhất theo tiêu chí nào, và **điểm bị loại gần nhất là gì và vì sao**.

Mục cuối là mục người phỏng vấn sẽ hỏi.

---

# MODULE 4 — NHIỀU MODEL, NHIỀU TARGET (18h)

Tiêu chí PASS số 1 đòi **≥3 model × ≥2 target**.

---

## Bài 10 — Model thứ hai và thứ ba (6h)

**Câu hỏi:** harness của tôi có thực sự tổng quát, hay chỉ chạy được với một model?

### Khái niệm

Đây là bài kiểm tra thật của thiết kế harness. Nếu Bài 4 làm tốt, thêm model thứ hai tốn vài giờ. Nếu làm hụt, bạn sẽ phải viết lại — và đó cũng là một bài học.

**Chọn model theo nguyên tắc phủ, không theo nguyên tắc nổi tiếng.** Ba model nên khác nhau ở ít nhất hai chiều:

| Chiều | Vì sao quan trọng |
|---|---|
| **Kích thước** | 450M vs 3B là hai bài toán hạ tầng khác nhau |
| **Kiểu action head** | Flow-matching/diffusion (nhiều solver step) vs autoregressive vs trực tiếp |
| **Backbone** | VLM khác nhau → đặc tính bộ nhớ khác nhau |

Gợi ý một bộ ba có độ phủ tốt: **SmolVLA** (~450M, flow-matching, nhẹ nhất — bắt đầu ở đây), một model **cỡ vài tỉ tham số** (OpenVLA, π₀, hoặc GR00T), và một model **được thiết kế cho edge** (dòng BitVLA/LiteVLA hoặc tương đương). Kiểm tra danh sách policy hiện có trong LeRobot docs khi bắt đầu, vì danh sách đó đổi nhanh.

**Cảnh báo phạm vi:** đừng cố chạy 6 model. Ba model đo kỹ có giá trị hơn sáu model đo hời hợt, và trần giờ là 95h.

### Làm

1. Thêm model thứ hai vào harness. **Đo thời gian bạn mất để thêm.** Nếu >4h, harness của bạn có vấn đề thiết kế — ghi lại và refactor.
2. Thêm model thứ ba.
3. Chạy toàn bộ ma trận model × precision trên GPU thuê.
4. Với mỗi model, ghi rõ cái gì **không** đo được và vì sao (ví dụ: model không hỗ trợ int8, hoặc không vừa VRAM).

### Số phải ra

| Kiểm tra | Kỳ vọng |
|---|---|
| Thời gian thêm model thứ ba | Ngắn hơn model thứ hai đáng kể |
| Model 3B vs 450M, cùng GPU | Chậm hơn nhiều lần, VRAM lớn hơn nhiều lần |
| Model flow-matching khi giảm solver step | Latency giảm gần tuyến tính |
| Bảng kết quả | Có ô trống, và mỗi ô trống có lý do ghi rõ |

Bảng có ô trống kèm lý do trung thực hơn bảng đầy số bịa. Đừng ngoại suy.

---

## Bài 11 — Target thứ hai: Pi 5, và con số gây sốc (6h)

**Câu hỏi:** có chạy được VLA trên một SBC 2 triệu không?

### Khái niệm

Chuẩn bị tinh thần trước: **số sẽ rất tệ, và đó là kết quả.**

Mốc công khai trên Raspberry Pi 4: một model vision-language nhỏ ở FP32 mất khoảng 11 giây cho một lần inference; một VLA lớn hơn ở FP32 mất tới khoảng 18 phút cho một forward pass; nén hybrid 4-bit (backbone NF4, giữ projection head ở FP32) kéo xuống còn khoảng 2 phút — nhanh hơn khoảng 9 lần.

Pi 5 nhanh hơn Pi 4, nhưng không nhanh hơn hai bậc độ lớn. Nghĩa là: **VLA cỡ lớn không chạy được real-time trên Pi 5, và bạn sẽ chứng minh điều đó bằng số.**

Vì sao điều này có giá trị:

1. Nó trả lời một câu hỏi nhiều người có mà ít người đo.
2. Nó biện minh (hoặc bác bỏ) kiến trúc phân tầng — cùng loại lập luận bạn đã làm với RTF ở Khóa 3, Bài 12.
3. Nó cho bạn một con số thật để nói khi ai đó hỏi "sao không chạy hết trên robot".
4. **Nó ngăn bạn mua Jetson.** Lộ trình ghi rõ: Jetson chỉ mua nếu M6 chứng minh được là cần. Bài này chính là phép chứng minh đó.

**Nếu bạn không có Pi 5** (chưa qua Khóa 3, chưa mua đợt 2), FAIL action đã viết sẵn: chạy toàn bộ trên GPU thuê ở **≥2 cấu hình khác nhau** — ví dụ 3090 vs 4090, hoặc cùng card khác batch size. Vẫn hợp lệ, vẫn publish được. Một lựa chọn khác rất tốt là thêm một target **CPU-only** (chính laptop của bạn), vì nó tạo được khoảng cách vài bậc độ lớn mà không tốn đồng nào.

### Làm

1. Chọn model nhỏ nhất trong bộ ba. Đừng bắt đầu bằng model 3B trên Pi — bạn sẽ ngồi chờ hàng chục phút mỗi iteration.
2. **Giảm số iteration.** Với latency thang giây, 200 iteration là vô lý. Dùng 20–30, và ghi rõ trong methodology rằng số mẫu nhỏ nên khoảng tin cậy rộng.
3. Theo dõi nhiệt độ và `vcgencmd get_throttled` suốt phép đo — trên Pi throttle gần như chắc chắn xảy ra.
4. Đo RAM peak. Nếu swap, ghi lại — swap làm số vô nghĩa và bạn phải nói rõ.
5. Thử một mức nén và đo lại. Ghi tỉ lệ tăng tốc.
6. **Tính con số quan trọng nhất:** nếu control loop cần 10Hz, Pi 5 chậm hơn yêu cầu **bao nhiêu lần**?

### Số phải ra

| Kiểm tra | Kỳ vọng |
|---|---|
| Latency trên Pi 5, model nhỏ, FP32 | Thang **giây**, không phải mili-giây |
| Latency trên Pi 5, model 3B | Có thể thang **phút**, hoặc không chạy nổi vì RAM |
| Tăng tốc nhờ nén 4-bit | Thang **vài lần tới một bậc** |
| Cờ throttle | Nhiều khả năng bật. Ghi lại, đừng che |
| Khoảng cách Pi 5 vs GPU thuê | **Vài bậc độ lớn** |

Nếu bạn đo ra Pi 5 chỉ chậm hơn GPU 3 lần, dừng lại — gần như chắc chắn đo nhầm (có thể đang đo cache, hoặc model không thực sự chạy).

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Pi hết RAM, process bị kill | Model quá lớn | **Đây là kết quả.** Ghi lại RAM cần vs RAM có |
| Latency biến thiên cực mạnh | Throttle + swap | Ghi cả hai, báo cáo phân bố chứ đừng báo cáo một số |
| Chạy được nhưng quá chậm để đo LIBERO | Bình thường | Đo latency trên Pi, đo chất lượng trên GPU, và **nói rõ trong báo cáo rằng hai trục đo trên hai target khác nhau** |

Điểm cuối là một giới hạn methodology thật. Nêu nó ra làm báo cáo của bạn đáng tin hơn, không kém đi.

---

## Bài 12 — Roofline: nút thắt nằm ở đâu (6h)

**Câu hỏi:** model chậm vì thiếu compute hay vì thiếu băng thông bộ nhớ?

### Khái niệm

Đây là bài nâng báo cáo của bạn từ "bảng số" lên "phân tích", và là phần khiến người đọc có kinh nghiệm dừng lại.

Mô hình roofline nói: hiệu năng của một phép tính bị chặn bởi **một trong hai** thứ — khả năng tính toán của chip (compute-bound) hoặc tốc độ đọc dữ liệu từ bộ nhớ (memory-bound). Biết mình ở phía nào quyết định tối ưu cái gì:

| Nếu | Thì tối ưu |
|---|---|
| **Memory-bound** | Giảm kích thước weight (quantization giúp nhiều), tăng batch |
| **Compute-bound** | Tăng hiệu suất sử dụng đơn vị tính (dùng đúng kernel, đúng tensor core), quantization giúp ít hơn nếu kernel không tận dụng được |

**Một kết quả công khai đáng biết:** phân tích roofline đa phần cứng của nhóm vla.cpp kết luận rằng inference VLA ở batch 1 là **compute-bound**, nên đòn bẩy triển khai là hiệu suất sử dụng chứ không phải băng thông. Họ chứng minh bằng cách viết lại kernel nhân ma trận ternary để chạy trên tensor core số nguyên thay vì CUDA core, cắt latency mỗi bước của BitVLA khoảng 4,5 lần — **cùng model, cùng weight, chỉ khác kernel.**

Bài học cho bạn: *"model này chậm"* không phải một chẩn đoán. *"Model này compute-bound và kernel hiện tại chỉ dùng 30% đơn vị tính"* mới là.

### Làm

1. Tính **arithmetic intensity** của model: số phép tính ÷ số byte đọc từ bộ nhớ. Ước lượng thô là đủ.
2. Tra thông số lý thuyết của GPU bạn thuê: peak FLOPS và peak memory bandwidth.
3. Vẽ roofline, đánh dấu vị trí của model.
4. **Kiểm chứng bằng thực nghiệm:** nếu roofline nói compute-bound, thì giảm precision weight (giảm byte đọc) sẽ **không** giúp nhiều; nếu memory-bound, nó sẽ giúp nhiều. Đối chiếu với số đo ở Bài 8. Hai đường phải gặp nhau.
5. Chạy profiler (`torch.profiler`, `nsys`) và xem đơn vị tính được dùng bao nhiêu phần trăm.
6. So vị trí trên roofline giữa GPU thuê và Pi 5 — hai phần cứng có thể nằm ở hai phía khác nhau.

### Số phải ra

| Kiểm tra | Kỳ vọng |
|---|---|
| Dự đoán từ roofline vs số đo ở Bài 8 | **Phải khớp về hướng.** Nếu roofline nói memory-bound mà quantization không giúp gì, một trong hai sai |
| Hiệu suất sử dụng đơn vị tính | Thường thấp hơn nhiều so với peak — đó là bình thường và là chỗ có dư địa |
| Vị trí Pi 5 vs GPU trên roofline | Có thể khác phía |

Đây chính là kiểu kiểm tra chéo ba đường của Khóa 1, áp dụng ở tầng cao hơn: tính từ nguyên lý đầu, đo trực tiếp, và đo bằng phương pháp thứ hai (profiler). Ba đường phải gặp nhau.

---

# MODULE 5 — PUBLISH VÀ REPRODUCE (12h)

Bốn tiêu chí PASS đầu của M6 do bạn kiểm soát. Tiêu chí thứ tư — **≥1 người ngoài reproduce được và xác nhận công khai** — do người khác chấm. Module này tồn tại để tiêu chí đó xảy ra chứ không phải để hy vọng nó xảy ra.

---

## Bài 13 — Viết bài tiếng Anh (5h)

**Câu hỏi:** ai sẽ đọc cái này, và họ muốn biết gì?

### Khái niệm

Tiêu đề gợi ý trong lộ trình: *"Benchmarking VLA inference on edge hardware"*.

**Người đọc mục tiêu:** kỹ sư ở công ty robotics đang phải quyết định chạy model ở đâu. Họ không cần bạn dạy VLA là gì. Họ cần số, methodology để tin số đó, và kết luận họ dùng được.

**Cấu trúc đề xuất:**

| Phần | Nội dung | Độ dài |
|---|---|---|
| TL;DR | 3–5 gạch đầu dòng, có số | Ngắn |
| Why this matters | Quyết định thực tế nào phụ thuộc vào số này | 1 đoạn |
| Setup | Model, target, cấu hình. Link config file | Ngắn, có bảng |
| **Methodology** | Warm-up, thermal isolation kèm bằng chứng, sai số | **Dài nhất** |
| Results | Bảng + hình Pareto + hình roofline | Nhiều hình |
| What surprised me | Phát hiện phản trực giác | 1–2 đoạn |
| Limitations | Cái gì không đo, giới hạn nào | Không được thiếu |
| Reproduce | Lệnh cụ thể | Ngắn |

**Phần "What surprised me" là phần được đọc nhiều nhất.** Ứng viên tốt cho phần này, dựa trên những gì tài liệu công khai đã ghi nhận: trung bình không đổi nhưng phân bố theo nhiệm vụ dịch chuyển; precision thấp làm sai im lặng; khoảng cách giữa SBC và GPU lớn tới mức nào; kernel quan trọng hơn weight.

**Ba quy tắc viết:**
1. **Mọi con số phải có link tới file kết quả thô.** Không có số nào trong bài mà không truy được về JSON trong repo.
2. **Không tuyên bố vượt quá dữ liệu.** Chênh lệch trong ngưỡng nhiễu thì gọi là "không phân biệt được", không gọi là "tốt hơn".
3. **Nêu giới hạn trước khi người khác nêu hộ.**

### Làm

1. Viết bài. Tiếng Anh.
2. Trước khi đăng, tự đọc lại và đánh dấu mọi câu tuyên bố. Với mỗi câu, hỏi: dữ liệu nào đỡ lưng cho câu này? Câu nào không có thì xóa hoặc hạ giọng.
3. Cross-post: r/robotics, Hacker News, LinkedIn, LeRobot Discord, Foxglove Discord.

---

## Bài 14 — Làm cho người khác chạy lại được (4h)

**Câu hỏi:** người lạ mất bao lâu từ lúc thấy repo tới lúc có số của riêng họ?

### Khái niệm

Mục tiêu: **dưới 30 phút, dưới 5 lệnh.** Mỗi phút ma sát thêm là một người bỏ cuộc, và bạn cần đúng một người không bỏ cuộc để đạt tiêu chí PASS số 4.

### Làm

**Checklist reproducibility:**

```
[ ] Dockerfile hoặc devcontainer chạy được từ máy sạch
[ ] Lockfile pin chính xác mọi phiên bản (uv.lock / requirements.txt có hash)
[ ] Commit hash hoặc revision của mọi model checkpoint
[ ] Một lệnh chạy phiên bản rút gọn (5 phút) để người ta thấy nó hoạt động
[ ] Một lệnh chạy phiên bản đầy đủ
[ ] Script tự động so kết quả của họ với kết quả của bạn, in ra bảng chênh lệch
[ ] Kết quả thô của bạn được commit trong repo để so
[ ] README nói rõ cần GPU gì, bao nhiêu VRAM, mất bao lâu, tốn khoảng bao nhiêu tiền thuê
[ ] Phần "expected output" có số thật để người ta biết mình chạy đúng
```

Mục "script tự động so kết quả" là mục biến một repo benchmark thành một **công cụ**. Nó cũng là thứ khiến người ta có động lực chạy: họ không chỉ chạy lại của bạn, họ có số của phần cứng họ.

**Tự kiểm tra khắc nghiệt:** thuê một máy GPU mới tinh, clone repo từ đầu, và bấm giờ. Không được dùng bất cứ thứ gì có sẵn trên máy cũ. Nếu mất hơn 30 phút, sửa.

### Số phải ra

| Kiểm tra | Ngưỡng |
|---|---|
| Từ máy sạch tới số đầu tiên | <30 phút |
| Số lệnh phải gõ | ≤5 |
| Kết quả chạy lại trên **cùng loại GPU** vs kết quả của bạn | Chênh <10% |

---

## Bài 15 — Đi tìm người reproduce (3h)

**Câu hỏi:** làm sao để một người lạ bỏ 30 phút và tiền thuê GPU cho repo của bạn?

### Khái niệm

Không tự xảy ra. Tiêu chí PASS số 4 là tiêu chí **do người ngoài chấm**, giống tiêu chí thứ 5 của Khóa 2 — và nó trượt vì cùng một lý do: kênh phân phối, không phải chất lượng công việc.

**Cái làm người ta muốn chạy:**
- Họ có phần cứng bạn **chưa** đo (Jetson, Apple Silicon, AMD, card đời khác). Bảng của bạn có ô trống là một lời mời.
- Chi phí thấp và rõ ràng: "chạy đầy đủ mất ~40 phút trên một 4090, khoảng 15 nghìn tiền thuê".
- Họ được ghi tên. Một bảng "contributed results" với tên và phần cứng người đóng góp là động lực thật.

**Cái làm người ta không chạy:** repo không có expected output (họ không biết mình chạy đúng chưa), setup lằng nhằng, hoặc bài viết nghe như quảng cáo.

### Làm

1. Thêm mục **"Wanted: results on hardware I don't have"** vào README, liệt kê cụ thể phần cứng đang thiếu.
2. Thêm bảng "Contributed results" trống, có sẵn định dạng và một dòng ví dụ.
3. Đăng vào LeRobot Discord với câu hỏi cụ thể, không phải lời mời chung chung. Ví dụ: *"tôi đo được X trên A; ai có Jetson Orin chạy giúp một lệnh được không, mất 10 phút và tôi có script so kết quả sẵn"*.
4. Trả lời mọi phản hồi trong 24h. Nếu ai đó gặp lỗi lúc setup, **đó là bug của bạn, không phải của họ** — sửa và cảm ơn.
5. Nếu sau 4 tuần không ai chạy: gửi trực tiếp cho 5 người cụ thể đang làm đúng lĩnh vực này (tác giả các repo/paper bạn đã đọc). Hỏi một câu kỹ thuật thật kèm link, đừng xin xỏ.

### Số phải ra

| Kết quả sau 60 ngày | Kết luận | Hành động |
|---|---|---|
| ≥1 người reproduce và xác nhận công khai | **PASS** | Tiếp tục |
| Có phản hồi nhưng không ai chạy | Ma sát setup còn cao | Quay lại Bài 14, giảm ma sát, thử lại một lần |
| Không phản hồi gì | Vấn đề kênh phân phối | Giống FAIL action của M3: cấp thêm giờ cho phân phối, vào Discord hỏi trực tiếp |

---

# GATE KHÓA 4

Đối chiếu đúng 5 tiêu chí PASS của M6:

```
[ ] 1. ≥3 model × ≥2 target

[ ] 2. Báo cáo p50/p95/p99, RTF, VRAM peak, throughput
       → KHÔNG báo cáo mean

[ ] 3. Methodology mô tả rõ warm-up và cách cô lập thermal throttling,
       KÈM SỐ CHỨNG MINH đã cô lập được
       (ví dụ: nhiệt độ ổn định ±2°C trong suốt phép đo)

[ ] 4. ≥1 người ngoài reproduce được và xác nhận công khai

[ ] 5. Bài viết tiếng Anh publish + repo public
```

**Hai thứ tôi thêm vào ngoài tiêu chí gốc**, vì tôi cho rằng chúng làm khác biệt lớn nhất và chi phí thấp:

```
[ ] 6. Trục chất lượng (LIBERO success rate) đo cùng bộ seed cho mọi cấu hình,
       báo cáo THEO NHIỆM VỤ chứ không chỉ trung bình

[ ] 7. Ít nhất một cấu hình "nhanh hơn nhưng hỏng" được tìm ra và ghi lại
```

Tiêu chí 6 và 7 là thứ phân biệt benchmark của bạn với phần lớn benchmark trên internet. Nếu phải cắt scope, cắt ở Module 4 (giảm còn 3 model × 2 target đúng mức tối thiểu) chứ đừng cắt Module 3.

**FAIL → action (cam kết trước):** không đủ target phần cứng → chạy toàn bộ trên GPU thuê ở ≥2 cấu hình khác nhau. Vẫn hợp lệ, vẫn publish được. Chạm 95h chưa PASS → publish nguyên trạng với số đã có, ghi rõ cái gì chưa làm, sang Khóa 5.

---

# LỊCH 11 TUẦN

| Tuần | Giờ | Làm | Xong thì có |
|---|---|---|---|
| 1 | 6 | Bài 1–2 · kiểm tra lại bảng mốc | Biết con số nào là hợp lý |
| 2 | 6 | Bài 3 · viết METHODOLOGY.md | **Nền của cả khóa** |
| 3 | 7 | Bài 4 · harness + test với model giả | Công cụ đo đã hiệu chuẩn |
| 4 | 7 | Bài 5–6 · GPU thuê, cô lập nhiệt | Số đầu tiên đáng tin |
| 5 | 7 | Bài 7 · LIBERO baseline | Trục chất lượng |
| 6 | 7 | Bài 8 · quantization hai trục | **Bảng chính của bài viết** |
| 7 | 6 | Bài 9 · Pareto + decisions.md | Lập luận chọn cấu hình |
| 8 | 7 | Bài 10 · model 2 và 3 | Ma trận đầy |
| 9 | 7 | Bài 11–12 · Pi 5 + roofline | Khoảng cách phần cứng + chẩn đoán |
| 10 | 6 | Bài 13–14 · viết bài + reproducibility | Publish |
| 11 | 4 | Bài 15 · đi tìm người chạy lại | Chờ tiêu chí 4 |

**Lưu ý:** tiêu chí PASS số 4 có độ trễ do người khác quyết. Đừng ngồi chờ — **bắt đầu Khóa 5 (hoặc quay lại đóng Khóa 3) ngay sau tuần 10**, và để Bài 15 chạy nền.

---

# NGUỒN HỌC KÈM KHÓA 4

| Nguồn | Dùng cho | Ghi chú |
|---|---|---|
| **LeRobot docs — mục Policies và Benchmarks** | Danh sách model hiện có, LIBERO, cách chạy | Nguồn chính. Kiểm tra lại khi bắt đầu vì danh sách đổi nhanh |
| **SmolVLA paper** (arXiv 2506.01844) | Kiến trúc, layer skipping, async inference | Đọc phần method, bỏ qua phần benchmark chất lượng |
| **vla.cpp** (arXiv 2606.08094) | Roofline cho VLA, runtime C++, bài học về precision | **Đọc kỹ phần limitations** — đó là nơi có nhiều bài học nhất |
| **BitVLA** (arXiv 2506.07530) | Quantization tích hợp vào huấn luyện | Cho biết ranh giới giữa "nén model có sẵn" và "huấn luyện model để nén" |
| **LiteVLA-Edge** (arXiv 2603.03380) | Pipeline triển khai trên Jetson, 4-bit GGUF + llama.cpp | Mẫu tốt cho cách trình bày kết quả |
| **Lite VLA on CPU-bound edge** (arXiv 2511.05642) | Số thật trên Raspberry Pi | Dùng làm mốc cho Bài 11 |
| **VLA survey** (arXiv 2505.04769) | Tổng quan kỹ thuật tăng tốc | Đọc mục inference acceleration và parameter-efficient methods |
| **Roofline** (Williams, Waterman, Patterson, CACM 2009) | Mô hình gốc | Bài báo kinh điển, ngắn, đáng đọc nguyên bản |
| **`torch.profiler` docs · Nsight Systems** | Profiling thực nghiệm | Bài 12 |
| **vast.ai / runpod docs** | Thuê GPU | Đọc phần spot instance và persistence |

Vẫn giữ quy tắc ba nguồn. Ở khóa này **paper là datasheet của bạn** — đọc phần method và limitations, bỏ qua phần abstract khoe kết quả.

---

# BA ĐIỀU MANG ĐI

**1. Khóa này không dạy bạn kỹ năng mới, nó chuyển kỹ năng cũ sang domain mới.** Benchmark, p99, thermal isolation, reproducibility, đường cong đánh đổi — bạn đã làm tám năm. Đừng học lại chúng; hãy đóng gói chúng cho một khán giả mới.

**2. Trục chất lượng là moat.** Ai cũng đo được latency. Rất ít người đo cả hai trục cùng lúc với cùng bộ seed và báo cáo theo nhiệm vụ. Đó là chỗ bạn khác biệt, và nó không tốn thêm phần cứng — chỉ tốn kỷ luật.

**3. Con số của bạn sẽ lỗi thời, methodology thì không.** Viết METHODOLOGY.md như thể nó là sản phẩm chính, vì với nhà tuyển dụng thì nó đúng là vậy.

---

# SAU KHÓA 4

**Khóa 5 — Cảm biến, đồng bộ thời gian, data platform (150h).** Khóa nặng nhất, cần đợt 3, và là nơi kỹ năng dữ liệu gặp phần cứng thật. Nguyên tắc scope của nó đáng nhắc trước: **số đo là deliverable, platform là vỏ.** Rủi ro lớn nhất là phần mềm (thế mạnh của bạn) xong nhanh và đẹp, còn phần khác biệt thật — số đo đồng bộ — thì mỏng. Đảo lại thứ tự làm: đo trước, dựng platform sau.

Và đây là lúc cái rig 2 webcam + IMU chúng ta nói tới trở nên hữu dụng.

**Trước khi sang Khóa 5, chạy M5 nếu chưa chạy.** Sau Khóa 2 và Khóa 4 bạn đã có hai artifact ★ để chỉ vào — đó là điều kiện vào M5. Apply là một phép đo, không phải bước cuối.
