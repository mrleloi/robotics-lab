# QUY CHUẨN SOẠN GIÁO TRÌNH — đọc trọn trước khi viết bất cứ dòng nào

Tài liệu này là hợp đồng chung cho mọi người soạn (người và agent). Mọi file trong `giao-trinh/` phải theo nó. Khi quy chuẩn và bản gốc mâu thuẫn, quy chuẩn thắng; khi quy chuẩn im lặng, dùng phán đoán và ghi lý do.

---

## 1. Người học là ai

- Backend/full-stack engineer **8 năm**, đang chuyển sang **robotics data infrastructure** (data platform, test & validation, sim & eval, MLOps nhẹ cho robot). Viết tiếng Việt, đọc tiếng Anh kỹ thuật tốt.
- Ngân sách ~6–7h/tuần, có tuần crunch chỉ đọc được 0–2h. Lộ trình 7 khóa chính (K1–K7). K1–K6 cộng lại 545h; K7 gốc 340h → tổng 885h, đã vượt ngân sách gốc 650h. K7 được thiết kế lại thành khóa build cho người mới (mục 4c), nặng hơn nữa. **Không giấu con số này** trong bất kỳ tổng quan nào.
- Phần cứng: mini PC **Beelink EQ12 Intel N100** (4 nhân E-core Gracemont, **không** hyperthreading, iGPU 24 EU, 2 cổng LAN Intel i225/i226 có PHC, nguồn 12 V DC), **ESP32-S3** làm I/O bridge (I2S, GPIO, encoder…), logic analyzer clone 24 MHz (fx2lafw), multimeter UT33D+, BME280, PCM5102A, MAX98357A/amp, mic I2S (INMP441), GPU thuê khi cần. Ubuntu 24.04 + ROS 2 Jazzy trong Docker. Quy ước dữ liệu: `CONVENTIONS.md` (REP-103/105, message chuẩn ROS 2, metadata ở channel MCAP).
- **Trình độ tay nghề phần cứng:** người mới hoàn toàn — đang học bật tắt mỏ hàn. Chưa từng đi dây nguồn công suất, chưa từng cầm pin lithium dung lượng lớn, chưa từng lắp cơ khí. Mọi bài có phần cứng phải viết cho người này, không phải cho người đã quen tay.
- **Đã tự làm (không bài bản) trong nghề backend:** dựng môi trường local tái tạo được các service; script chấm pass/fail/inconclusive vừa deterministic vừa có model AI review; pipeline agent tự chạy → test → sửa → deploy → báo cáo; hệ metrics để quan sát/eval; server mock để tự tạo bộ test chuẩn; đo trên host "yên tĩnh" để tránh test nhiễu. → Đây là **vốn để bắc cầu**. Dùng nó, gọi đúng tên chuẩn của những thứ đó, và chỉ ra chỗ còn thiếu (lý thuyết về tỉ lệ sai của chính dụng cụ kiểm tra, power analysis, hiệu chuẩn LLM-judge, Goodhart…).
- **Cách học hiệu quả với người này:** chủ động trừu tượng hóa nội dung, liên hệ với kiến thức cá nhân (backend, hệ phân tán, hàng đợi, proxy, Kafka…), rồi đặt câu hỏi ngược để làm rõ. Xem `_ref/cau-hoi-cua-ban-trong-gemini.md` để thấy giọng và kiểu câu hỏi thật. **Rủi ro lớn nhất của cách học này:** tích lũy mô hình đúng một nửa mà cảm giác rất hiểu (Gemini đã xác nhận "chính xác 100%" cho nhiều mô hình chỉ đúng một phần). Giáo trình phải **chấm** mô hình, không vuốt ve.
- Muốn: hiểu bản chất, đủ để **ra quyết định** và **đánh giá đúng / sai / chưa rõ** cho thứ mình đang đọc; nắm mindset đằng sau công cụ để tự biến thành của mình.

## 2. Nguồn sự thật và mức tin

Gốc repo `robotics-lab/` (máy Kiro: `c:\htdocs\physical\`; session Claude cloud: `/home/user/robotics-lab`). Mọi đường dẫn dưới đây tính từ gốc repo.

| Nguồn | Vai trò | Mức tin |
|---|---|---|
| `khoa-1-tu-zero-den-do-duoc.md` … `khoa-6-sim-eval-infra.md`, `khoa-7-robot-hoan-chinh.md`, `khoa-7-phu-luc.md`, `00-lo-trinh-tong.md`, `THAY-DOI-10-2026.md`, `CONVENTIONS.md`, `robotics-data-infra-roadmap.md` | Xương sống: mục tiêu, bài, giờ, gate, phần cứng | Cao, nhưng **có lỗi đã biết** (mục 7) và chưa kiểm phần cứng |
| `detail/Gemini-khóa N-*.md` (K3–K7) | Bản detail cũ. Chỉ để **gặt** ví dụ hay, câu hỏi hay, và để **liệt kê lỗi cần tránh** | Thấp. Mọi khẳng định kỹ thuật từ đây phải tự kiểm lại. Bỏ toàn bộ `[cite: N]` |
| `docs/Claude-Xây dựng robot confession…md`, `docs/lo-trinh-edge-physical-ai-final.md` | Ý định sản phẩm gốc (robot confession) và lịch sử lộ trình | Trung bình, dùng cho bối cảnh |
| `giao-trinh/_ref/` | `cau-hoi-cua-ban-trong-gemini.md` (giọng người học), `muc-luc-bai-goc.md` (số dòng từng bài để đọc theo offset), `danh-gia-ban-dau.md` (đánh giá, nguồn đọc gợi ý cho F) | Tham chiếu, không sửa |
| Kiến thức của bạn + tra cứu web | Bổ sung bản chất, lịch sử, liên kết | Gắn nhãn tin cậy cho từng khẳng định |

File gốc 50–75 KB, file Gemini 150–300 KB: **dùng grep tìm theo "Bài N"** hoặc đọc theo offset/limit (xem `_ref/muc-luc-bai-goc.md`), đừng đọc một lần.

## 3. Năm nguyên tắc bắt buộc

1. **Niêm phong đáp án.** Con số kỳ vọng, đáp án tự kiểm tra, kết luận thí nghiệm đặt trong khối gập:
   ```html
   <details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

   ...

   </details>
   ```
   (Để dòng trống sau `<summary>` và trước `</details>` để markdown bên trong render được.) Phần thân bài chỉ đưa **đề bài, tham số cần tra (tra ở đâu), công thức/phương pháp**. Không lộ số trong tiêu đề, bảng thuật ngữ hay câu chuyện mở đầu.
2. **Mọi phép so sánh với backend phải kèm "Gãy ở chỗ:"** và hậu quả nếu dùng nhầm phép so sánh.
3. **Gắn nhãn tin cậy** cho khẳng định kỹ thuật có thể sai:
   - `[spec]` — datasheet/chuẩn/tài liệu chính thức (ghi tên tài liệu, mục/trang nếu biết)
   - `[chuẩn]` — kiến thức giáo khoa ổn định
   - `[ước lượng]` — con số ước tính, kèm cách tính
   - `[tự đo]` — chưa kiểm chứng, người học phải đo/kiểm trên máy mình
   Không cần gắn cho câu hiển nhiên. Gắn cho mọi con số và mọi khẳng định về API/phiên bản/phần cứng/giá.
4. **Chấm mô hình, không vuốt ve.** Khi nêu một mô hình trực giác mà backend engineer dễ tự xây (kể cả mô hình thật của người học trong `_ref/`), chấm **ĐÚNG / ĐÚNG MỘT PHẦN / SAI**, chỉ chỗ gãy, đưa **một phản ví dụ**. Không mở đầu bằng lời khen.
5. **Mỗi khái niệm khó có ít nhất một dạng không phải chữ:** sơ đồ Mermaid, timing diagram (WaveDrom JSON hoặc ASCII), bảng số, hoặc **mô phỏng đồ chơi bằng Python** (≤60 dòng, numpy/matplotlib/scipy) chạy được trước khi đụng phần cứng; gợi ý capture PulseView/Foxglove/Falstad khi hợp. Nếu viết code, **chạy thử** trước khi đưa vào (xem mục 9); ghi `# [đã chạy]` hoặc `# [chưa chạy]` ở dòng đầu khối code.

## 4. Khung một bài (12 phần) — dùng đúng các tiêu đề này

```markdown
## Bài N — <Tên> (<giờ>h)

> **Vị trí:** <bài trước → bài này → bài sau> · **Cần trước:** <Fx.y, Bài …> · **Sau bài này bạn quyết định được:** <một quyết định cụ thể>

### 1. Câu chuyện — ai đã khổ vì chuyện này
<sự cố thật / lịch sử ngắn / vì sao người ta phải phát minh ra thứ này. 1–2 đoạn. Không bịa sự cố; nếu là kịch bản giả định thì nói rõ "kịch bản".>

### 2. Mô hình tư duy
<một hình (Mermaid/ASCII/WaveDrom/bảng) + 3–5 câu nói về bản chất. Có thể kèm mô phỏng đồ chơi.>

### 3. Cầu nối từ backend
| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|

**Chấm mô hình:** <1–3 mô hình trực giác, mỗi cái chấm ĐÚNG / ĐÚNG MỘT PHẦN / SAI + chỗ gãy + phản ví dụ>

### 4. Thuật ngữ
| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
(🟢 nắm · 🟡 biết tên · 🔴 bỏ — theo đúng tinh thần `robotics-data-infra-roadmap.md`)

### 5. Dự đoán
<đề bài, tham số cần tra (tra ở đâu), công thức/phương pháp. Mẫu `prediction.md` để copy. KHÔNG có đáp án.>

### 6. Làm
<các bước, kèm sai số của dụng cụ đo ở mỗi phép đo quan trọng. Giữ đủ bước của bản gốc, sửa chỗ sai.>

### 7. Số phải ra
<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

<bảng số, khoảng chấp nhận, vì sao lệch là bình thường>

</details>

### 8. Nếu ra khác
| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|

### 9. Câu hỏi ngược
<4–6 câu, mỗi câu gắn nhãn: [Nếu…thì] [Vì sao không] [Quy mô] [Failure mode] [Liên ngành] [Phản biện]. Ít nhất 1 [Quy mô] và 1 [Failure mode]. Mỗi câu có hướng nghĩ gập:>
<details><summary>Hướng nghĩ</summary>

<gợi ý 2–4 câu, không phải lời giải trọn>

</details>

### 10. Liên kết ra ngoài
<pattern này xuất hiện ở ngành/hệ thống khác thế nào (mạng, DB, tài chính, sinh học, hàng không…). 1–3 liên kết, mỗi cái 2–3 câu, có chỗ giống và chỗ khác.>

### 11. Độ tin cậy và sửa lỗi
| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
<+ danh sách chỗ đã sửa so với bản gốc hoặc bản Gemini, và lý do>

### 12. Đọc thêm và tự kiểm tra
- **Nguồn gốc:** <datasheet/spec/paper>
- **Giải thích:** <một nguồn giải thích tốt>
- **Đào sâu (tùy chọn):** <một nguồn>
- **Tự kiểm tra:** (1) giải thích lại cho một backend engineer khác trong 5 câu; (2) vẽ lại hình ở phần 2 từ trí nhớ; (3) <1–2 câu hỏi có đáp án gập>
```

**Khung rút gọn** cho bài thuần hậu cần (mua sắm, cài đặt công cụ, viết bài, đi tìm người reproduce, gate): giữ dòng Vị trí và phần 1, 2, 3, 6, 8, 9, 12; ghi `(khung rút gọn)` cạnh tiêu đề.

## 4b. Khung khóa nền F và viên nang

**Đầu file F** (trước viên nang đầu tiên):
- *Vì sao khóa nền này tồn tại* — thiếu nó thì đọc các bài chính sẽ hụt ở đâu (chỉ tên bài cụ thể).
- *Mindset cốt lõi* — 3–5 câu người trong nghề tin, kèm vì sao họ tin (họ đã khổ vì gì).
- *Bản đồ viên nang* (Mermaid) + *học đúng lúc*: bảng Viên nang → học trước bài chính nào → giờ.
- *Bạn đã làm cái này rồi* (nếu hợp): đối chiếu kinh nghiệm backend/AI-harness của người học với tên chuẩn và chỗ còn thiếu.

**Mỗi viên nang:**
```markdown
## Fx.y — <Tên> (<giờ>h)
> **Dùng cho:** <K? Bài ? / K7 Cn.m> · **Cần trước:** <…> · **Sau viên nang này bạn đánh giá được:** <loại khẳng định nào>

### 1. Câu chuyện
### 2. Mô hình tư duy            (+ ít nhất một dạng không phải chữ)
### 3. Cầu nối từ backend         (+ Chấm mô hình; + "tên chuẩn của thứ bạn đã làm")
### 4. Thuật ngữ                  (🟢🟡🔴)
### 5. Bài tập dự đoán            (làm được trên laptop trong ≤2h, ưu tiên Python; đáp án niêm phong)
### 6. Lăng kính đánh giá         (checklist câu hỏi để chấm một tài liệu/kết quả trong chủ đề này là ĐÚNG/SAI/CHƯA RÕ
                                  + 2–4 khẳng định mẫu — lấy từ bài chính hoặc bản Gemini khi có — để người học tự chấm, đáp án gập)
### 7. Câu hỏi ngược              (nhãn như mục 4, có hướng nghĩ gập)
### 8. Liên kết ra ngoài
### 9. Áp vào khóa chính          (bài nào, dùng thế nào, thay đổi quyết định gì)
### 10. Độ tin cậy
### 11. Đọc thêm và tự kiểm tra   (≤3 nguồn)
```

**Cuối file F:** *Tranh luận đang mở trong nghề* (2–4 chủ đề người trong nghề còn cãi nhau, mỗi phía nói gì) và *Bài kiểm tra cuối khóa nền* (một bài tập tổng hợp gắn vào dự án thật của người học).

## 4c. Khóa 7 — khóa build cho người mới

Khóa 7 được thiết kế lại hoàn toàn: từ "đặc tả dự án cho người đã PASS K1–K6" thành **khóa vừa build vừa học**, đi đúng thứ tự một người mới thực sự dựng robot. Kế hoạch chi tiết, mã chặng, giờ, file và phân công: **`khoa-7/_KE-HOACH-K7.md`** — mọi người soạn K7 và F phải đọc file đó. Mã bài K7 mới: `K7 Cn.m` (chặng n, bài khái niệm m), ví dụ `→ K7 C3.2`. Không dùng lại số "Bài 1–21" của K7 gốc khi liên kết chéo (trừ khi nói "K7 gốc Bài N").

## 5. Quy tắc văn phong

- Tiếng Việt, giữ thuật ngữ tiếng Anh nguyên gốc, giải thích ở lần đầu. Đơn vị SI, có khoảng trắng giữa số và đơn vị khi hợp.
- Thẳng, đặc, không độn. **Cấm:** `[cite: N]`, câu kết kiểu "Bạn đã sẵn sàng sang bài X chưa?", lời khen người học, emoji trang trí (chỉ dùng 🟢🟡🔴🔒 và ✅ ở checkpoint K7, có nghĩa).
- **Không bịa nguồn.** Chỉ đưa link/tên tài liệu bạn chắc chắn tồn tại. Không chắc URL thì ghi tên tài liệu + tác giả, không ghi URL. Có thể dùng web search/fetch để kiểm (khuyến khích cho phiên bản API, thông số datasheet, URL).
- **Không bịa sự cố.** Câu chuyện thật thì nêu tên (Mars Pathfinder, Mars Climate Orbiter, Therac-25, Knight Capital, Ariane 5, Patriot missile clock drift, Boeing 787 pin, Samsung Note 7…). Câu chuyện giả định ghi rõ "kịch bản".
- Độ dài mục tiêu: bài đầy đủ ~1.500–3.500 từ; bài rút gọn ~500–1.200 từ. Chất lượng hơn số lượng.
- Liên kết chéo: dùng mã viên nang nền `→ F4.5`, mã bài `→ K5 Bài 9`, mã K7 `→ K7 C3.2`.
- Code: ngắn, chạy được, có chú thích; API dễ đổi (LeRobot, Nav2, ESP-IDF, OpenVINO, mcap, ros2_control) ghi `[tự đo]` + "kiểm theo phiên bản bạn cài".
- Giá tiền VNĐ luôn là `[ước lượng]`, ghi tháng/năm tham chiếu (10/2026), khuyên người học kiểm lại ở cửa hàng.

## 6. Danh mục viên nang nền (mã cố định — dùng để liên kết chéo)

Mỗi viên nang 3–8h, học **đúng lúc** bài chính cần. Người soạn F được thêm nội dung nhưng **giữ nguyên mã và tên**.

**F1 — Khoa học đo lường và thống kê thực nghiệm** → `nen-tang/F1-do-luong-thong-ke.md`
- F1.1 Mọi con số là một ước lượng: độ bất định, sai số hệ thống vs ngẫu nhiên, resolution/accuracy/precision, chữ số có nghĩa, lan truyền sai số (GUM loại A/B)
- F1.2 Phân bố, không phải trung bình: histogram, percentile, đuôi dài, HDR histogram, vì sao p99 của 100 mẫu không đáng tin
- F1.3 Benchmark đúng cách: warmup, steady state, coordinated omission, cô lập nhiễu, active benchmarking, A/A test
- F1.4 Khoảng tin cậy và bootstrap: CI cho mean, percentile, tỉ lệ (Wilson)
- F1.5 So sánh hai thứ: kiểm định, effect size, power và cỡ mẫu, bội so sánh, bẫy "nhìn trộm" (peeking)
- F1.6 Fit mô hình vào số đo: hồi quy, residual, tương quan ≠ nhân quả, overfitting
- F1.7 Báo cáo trung thực: preregistration (= `prediction.md`), kết quả âm, bảng số có sai số

**F2 — Kỹ nghệ kiểm thử và đánh giá** → `nen-tang/F2-kiem-thu-danh-gia.md`
- F2.1 Bài toán oracle: test là một phép đo có dương tính giả/âm tính giả
- F2.2 Tái lập và hermetic: môi trường, lockfile, seed, nguồn phi tất định
- F2.3 Flaky test là một số đo: ước lượng tỉ lệ flake, quarantine, phán quyết ba trạng thái
- F2.4 Test khi không biết đáp án: property-based, metamorphic, differential, golden file
- F2.5 Kiểm tra chính bài test: mutation testing, fault injection, canary lỗi cố ý
- F2.6 Deterministic simulation testing và chaos (FoundationDB, TigerBeetle, Antithesis, Jepsen)
- F2.7 Các tầng X-in-the-loop: MIL/SIL/HIL, kim tự tháp test cho robot
- F2.8 Eval cho hệ ML/AI: tập giữ kín, Goodhart, LLM-as-judge và hiệu chuẩn (kappa), nhiễm benchmark

**F3 — Hệ thống dữ liệu và xử lý luồng** → `nen-tang/F3-du-lieu-xu-ly-luong.md`
- F3.1 Log là trung tâm: append-only, offset, segment, index (Kafka ↔ MCAP)
- F3.2 Encoding và schema evolution: Protobuf/CDR/Avro, quy tắc tương thích, file tự mô tả
- F3.3 Event time vs processing time: window, watermark, dữ liệu đến muộn
- F3.4 Ghép luồng khác tần số: as-of join, nội suy, resampling, sai số căn chỉnh
- F3.5 Idempotency, exactly-once, upload resumable, ngữ nghĩa object store
- F3.6 Lưu trữ phân tích: columnar (Parquet), partition, index, catalog, DuckDB
- F3.7 Chất lượng dữ liệu và data contract: validate theo schema vs theo vật lý
- F3.8 Lineage và provenance: hash nội dung, DAG, tái tạo mọi kết quả
- F3.9 Backpressure và drop policy: hàng đợi có giới hạn, load shedding, đếm cái đã drop

**F4 — Thời gian và đồng hồ** → `nen-tang/F4-thoi-gian-dong-ho.md`
- F4.1 Đồng hồ vật lý: thạch anh, ppm, nhiệt độ (tuning-fork 32 kHz vs AT-cut MHz), lão hóa; mô hình offset/skew/drift
- F4.2 Đo độ ổn định: Allan deviation, vì sao độ lệch chuẩn không đủ
- F4.3 Đồng hồ trong máy tính: wall/monotonic/raw, TSC, clocksource, timestamp ở kernel/driver/app
- F4.4 NTP: bốn timestamp, giả định đối xứng, giới hạn
- F4.5 PTP: hardware timestamping, PHC, ptp4l/phc2sys, servo, BMCA, transparent/boundary clock
- F4.6 Thời điểm của một phép đo cảm biến: source vs receive, giữa phơi sáng, rolling shutter, bù trễ, ước lượng offset bằng cross-correlation
- F4.7 Ngân sách sai số thời gian và trọng tài đo
- F4.8 Thứ tự không cần đồng hồ chung: Lamport, vector clock, TrueTime

**F5 — Nhúng, thời gian thực và tín hiệu số** → `nen-tang/F5-nhung-thoi-gian-thuc.md`
- F5.1 MCU vs Linux: hai thế giới, vì sao robot cần cả hai
- F5.2 Interrupt, DMA, buffer: dữ liệu chảy không qua CPU, double buffering, ring buffer
- F5.3 Lập lịch và trường hợp xấu nhất: RTOS, ưu tiên, priority inversion, WCET, jitter
- F5.4 Linux gần thời gian thực: PREEMPT_RT, cyclictest, isolcpus, IRQ affinity, tần số CPU
- F5.5 Lấy mẫu và lượng tử: Nyquist, aliasing, nhiễu lượng tử, SNR, dither
- F5.6 Phổ và lọc: FFT, cửa sổ, low-pass, trung bình trượt, cross-correlation
- F5.7 Nguồn điện và lỗi "phần mềm" giả: brownout, decoupling, ground, watchdog
- F5.8 Vòng điều khiển: PID, tần số lấy mẫu, trễ trong vòng, vì sao jitter phá ổn định

**F6 — Mô hình hóa, mô phỏng, V&V, nhận dạng hệ thống** → `nen-tang/F6-mo-hinh-mo-phong-vv.md`
- F6.1 Mô hình là gì: trừu tượng có miền hiệu lực
- F6.2 Verification vs Validation vs Calibration (NASA-STD-7009, ASME V&V)
- F6.3 Tích phân số: timestep, ổn định, sai số tích lũy, trôi năng lượng, vì sao tiếp xúc khó
- F6.4 Nhận dạng hệ thống: ước lượng tham số bằng least squares, thiết kế tín hiệu kích thích
- F6.5 Sim-to-real gap: định nghĩa đo được, gap theo kênh, domain randomization vs system ID
- F6.6 Độ nhạy và bất định của mô hình: sensitivity analysis, Monte Carlo
- F6.7 Ước lượng trạng thái: từ trung bình đến Kalman (trực giác), covariance
- F6.8 Hình học tối thiểu: frame, transform 4×4, quaternion (🟡)

**F7 — Hiệu năng và vận hành ở quy mô** → `nen-tang/F7-hieu-nang-van-hanh.md`
- F7.1 Hàng đợi: định luật Little, đầu gối utilization, trực giác M/M/1
- F7.2 Phần cứng tính toán: phân cấp bộ nhớ, băng thông vs compute, roofline, arithmetic intensity
- F7.3 Phương pháp USE/RED, profiling, flame graph, perf
- F7.4 SLI/SLO/error budget cho pipeline dữ liệu
- F7.5 Observability: metrics/logs/traces, cardinality, dashboard có chủ đích, alert
- F7.6 Soak test, chế độ hỏng, FMEA
- F7.7 Sự cố: bisect qua tầng, postmortem không đổ lỗi, runbook

## 7. Lỗi đã biết — phải sửa, không được lặp lại

| Chỗ | Sai | Đúng |
|---|---|---|
| K5 Bài 11 (rolling shutter) | số hàng sáng = t_pulse / t_row | ≈ (t_pulse + t_exposure) / t_row. Đo t_row bằng exposure tối thiểu, hoặc hai độ dài xung rồi lấy hiệu |
| K3 Bài 7 (SNR) | kiểm `6.02·bits + 1.76` dB trên giọng thật qua mic ở 16/12/8/4 bit, lệch <3 dB | Công thức giả định sin full-scale + nhiễu lượng tử đều. Kiểm trên **sin số tạo bằng code** (không qua mic); với giọng thật chỉ kiểm xu hướng ở 8 và 4 bit, nơi nhiễu lượng tử lấn nhiễu mic |
| K5 Bài 9 (Gemini) | `ptp4l ... -p /var/run/...` để tách socket | `-p` là thiết bị PHC. Hai instance cùng máy cần **file cấu hình riêng** (`uds_address`, interface, có thể `clockIdentity`/domain). Ghi `[tự đo]` |
| K5 Bài 10 (Gemini) | −0.04 ppm/°C² cho thạch anh 40 MHz | Đó là hệ số **tuning-fork 32.768 kHz** (parabol). AT-cut MHz có đường cong bậc ba, lệch nhỏ hơn nhiều trong dải phòng. Bắt người học tra datasheet thạch anh/TCXO thật hoặc đo |
| K4 Bài 12 (Gemini) | N100 ≈ 0.7 TFLOPS FP32 | Tự tính: 4 nhân × ~2.9–3.4 GHz × FLOP/chu kỳ của Gracemont (2 đơn vị FMA 128-bit → 16 FLOP FP32/chu kỳ) ≈ 0.19–0.22 TFLOPS CPU; iGPU 24 EU ~0.29 TFLOPS lý thuyết. Ghi `[ước lượng]`, bắt đo bằng micro-benchmark |
| K4 Bài 12 (Gemini) | "VLA batch 1 là compute-bound" như sự thật chung | Phụ thuộc số token/phase. Decode batch 1 ~1–2 FLOP/byte → memory-bound; prefix ảnh hàng trăm token có cường độ cao hơn. Phải tự đo |
| K6 Bài 8 (Gemini) | giải thích hyperthreading trên N100 | N100 không có HT (4C/4T) |
| K4 Bài 1 (Gemini) | import `lerobot.common.policies…` cố định | API LeRobot đổi nhanh (đã chuyển cấu trúc package). `[tự đo]` theo phiên bản cài |
| Hội thoại K3 (Gemini xác nhận sai) | "RAM sinh ra để làm buffer cho các thiết bị chạy theo clock"; "mạch chạy nhanh hơn 1000 lần được nhưng người ta cố tình giới hạn"; "flash là RAM" | RAM = bộ nhớ làm việc lớn hơn thanh ghi, nhanh hơn ổ đĩa; nối hai miền clock là việc của FIFO bất đồng bộ. Tần số tối đa bị chặn bởi critical path/setup time và công suất (P ∝ C·V²·f). Flash là bộ nhớ không mất khi tắt nguồn |
| Hội thoại K3 (bỏ lỡ) | công thức độ trễ DMA chỉ là "công thức" | Đó là **định luật Little** (L = λW) — phải chỉ ra |
| Tổng lộ trình | ngân sách 650h | Cộng các khóa = 885h (K7 gốc); với K7 mới còn cao hơn — xem `khoa-7/_KE-HOACH-K7.md`. Ghi rõ trong tổng quan, không giấu |
| K7 gốc toàn bộ | viết cho "người đã PASS Khóa 1–6", BOM một dòng, không có lắp ráp/đi dây/bring-up/an toàn pin | Thiết kế lại theo mục 4c |

Khi gặp thêm lỗi, sửa và ghi vào phần 11 của bài, đồng thời liệt kê trong báo cáo trả về.

## 8. Cấu trúc thư mục đầu ra

```
giao-trinh/
  _QUY-CHUAN.md            (file này)
  _ref/                    (tham chiếu, không sửa)
  README.md                (mục lục tổng — người điều phối viết)
  nen-tang/F1-do-luong-thong-ke.md … F7-hieu-nang-van-hanh.md   (tên ở mục 6)
  khoa-1/00-tong-quan.md, phan-a-nen.md, phan-b-dung-cu.md, phan-c-do-that.md, phan-d-du-lieu-tren-day.md
  khoa-2/00-tong-quan.md, m1-mcap-cong-cu.md, m2-dataset-audit.md
  khoa-3/00-tong-quan.md, m1-chuoi-phat.md, m2-do-tre.md, m3-tts-kien-truc.md, m4-he-thong-v1.md
  khoa-4/00-tong-quan.md, m1-nen-tang.md, m2-harness.md, m3-truc-chat-luong.md, m4-nhieu-target.md, m5-publish.md
  khoa-5/00-tong-quan.md, m0-chon-phan-cung.md, m1-cam-bien.md, m2-dong-bo-thoi-gian.md, m3-data-stack.md, m4-van-hanh.md
  khoa-6/00-tong-quan.md, m1-determinism.md, m2-kich-ban.md, m3-quy-mo.md, m4-danh-gia-regression.md, m5-sim-to-real.md, m6-ci-publish.md
  khoa-7/_KE-HOACH-K7.md, 00-tong-quan.md, c00-…md … c12-…md   (tên ở _KE-HOACH-K7.md)
```

Mỗi khóa có `00-tong-quan.md` gồm: bản đồ khóa (Mermaid), bảng *Bài → giờ → viên nang nền cần trước → quyết định ra được*, gate (giữ tiêu chí gốc, sửa chỗ sai, nói rõ đã sửa gì), lịch, bẫy đã biết, danh sách sửa lỗi so với bản gốc/Gemini, và **"Cách học khóa này"** (tuần thường/tuần crunch làm gì, dùng AI ở bước nào: không ở bước dự đoán; ở bước giải thích thì dùng prompt "chấm mô hình"). Gate của một module nằm cuối file module đó.

## 9. Quy tắc làm việc cho agent soạn

- **Chỉ ghi vào file được giao.** Không sửa file gốc, không sửa `_ref/`, không sửa file của agent khác.
- **Viết dần:** tạo file bằng một lần ghi (header + bài đầu), sau đó **nối thêm từng bài** (append). Đừng dồn cả file vào một lần ghi.
- **Chạy thử code:** Python có numpy, matplotlib, scipy (Kiro: `c:\htdocs\physical\.venv-giaotrinh\Scripts\python.exe`; Claude: `python3` hệ thống). Nháp đặt ở `giao-trinh/_scratch/<mã-agent>/` (thư mục bị gitignore), xóa khi xong. Matplotlib: dùng `matplotlib.use("Agg")` và `savefig` khi thử; trong giáo trình có thể để `plt.show()`.
- Kiro: shell là PowerShell trên Windows, đọc file tiếng Việt bằng tool đọc file, không dùng `cat`. Claude: bash trên Linux.
- **Hai nhóm soạn song song** (Claude trong `giao-trinh/`, Kiro trong `giao-trinh-kiro/`): đọc `giao-trinh/_PHOI-HOP.md` để biết ai làm phần nào và cách hợp nhất bản cuối.
- **Tự kiểm trước khi báo xong:** (a) mọi bài có đủ phần theo khung; (b) không còn `[cite`; (c) mọi con số kỳ vọng nằm trong khối 🔒; (d) mọi hàng "Cầu nối" có cột "Gãy ở chỗ"; (e) các lỗi ở mục 7 thuộc phạm vi của bạn đã được sửa.
- **Báo cáo trả về ≤250 từ:** file đã ghi, số bài, lỗi mới phát hiện trong bản gốc/Gemini (mỗi lỗi một dòng), chỗ còn nghi ngờ chưa kiểm được.
