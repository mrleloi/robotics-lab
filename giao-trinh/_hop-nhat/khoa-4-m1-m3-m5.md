# Nhật ký hợp nhất + review — Khóa 4, đơn vị K4-tq (m1, m3, m5, 00-tong-quan)

Phạm vi: hợp nhất `khoa-4/m1-nen-tang.md` (Claude Bài 1–3 × Kiro Bài 1); review A–H `m3-truc-chat-luong.md` (Bài 7–9) và `m5-publish.md` (Bài 13–15 + Gate); viết `00-tong-quan.md`. Không đọc/sửa `m2-harness.md`, `m4-nhieu-target.md` (agent khác viết song song); các dòng về Bài 4–6, 10–12 trong tổng quan chỉ dựa trên `khoa-4-benchmark-edge.md`, quy chuẩn mục 7 và `ghi-chu-cho-K4-K5.md`.

## m1 — Bài 1

- **Bản nền: C.** Sâu hơn ở bản chất: mô phỏng sync/async với tuổi observation, chấm ba mô hình của người học (K3 lượt 6, 12) có phản ví dụ, năm câu hỏi ngược sắc, ba liên kết ngoài. Bản K gọn, đúng, nhưng chiều sâu chấm mô hình kém hơn.
- **Ghép từ K:** bảng `info.json` libero/pusht (Đề 1b + 🔒; đã đối chiếu file thật trong `data/`: libero 2 cam 256×256, state 8, action 7, fps 10; pusht 1 cam 96×96, state/action 2, fps 10, codebase v3.0); mô phỏng 10 dòng percentile của `select_action`; bước 4b (nhiễu cố định → nguồn ngẫu nhiên cho Bài 7) và 4c (quét `num_steps`, fit affine); ba dòng "Nếu ra khác" (reset mỗi lần, thiếu `.eval()`, thiếu `data/`); bản đồ module + bảng bài ở đầu file.
- **Mâu thuẫn:** vị trí `make_pre_post_processors` — C ghi `lerobot.policies.factory`, K ghi `lerobot.policies`. Kiểm `src/lerobot/policies/__init__.py` nhánh main: định nghĩa ở `factory`, re-export ở `policies` → cả hai đúng; code thử cả hai. Default config SmolVLA (chunk 50, n_action_steps 50, num_steps 10, 512×512, pad 32, 16 layer VLM) kiểm lại trên `configuration_smolvla.py` main: khớp cả hai bản.
- **Lỗi đã sửa:** C cố định import `lerobot.policies.smolvla.modeling_smolvla` và `SystemExit` nếu hỏng (vẫn là import cố định, quy chuẩn mục 7) → hàm thử nhiều đường dẫn, in đường đã chạy, `[tự đo]`. C lộ đáp án Đề 4 trong câu chuyện ("khựng 14% thời gian") → bỏ số. Thêm vào phần 11 các sửa của K về bản gốc (affine theo solver step, shape ảnh theo key, SO-101 6 motor).

## m1 — Bài 2

- **Bản nền: C** (chỉ có một bản). Review A–H.
- **Lỗi đã sửa (ghi chú K4 Bài 2):** bản gốc "1% số lần chậm → mất ổn định 1% thời gian, 18 lần/phút ở 30 Hz" lẫn đếm theo lần với theo thời gian và theo tick; **bản C lặp lại lỗi** ở câu chuyện và bảng cầu nối. Sửa câu chuyện, hàng cầu nối, thêm chấm mô hình SAI với phản ví dụ tính số (99%×120 ms + 1%×800 ms → ~6,3% thời gian, ~4,7 lần/phút, ~24 tick đói mỗi lần), viết lại đáp án tự kiểm 2 cho nhất quán (theo lần ≈ 5–6/phút, theo tick ≈ 45–50/phút, ~8% thời gian).
- **Niêm phong:** phần 11 nêu "p99 cần n ≥ 368" ngoài 🔒 → chuyển thành tham chiếu.

## m1 — Bài 3

- **Bản nền: C.** Không lỗi kỹ thuật mới. Chạy lại 4 khối Python của m1 + 1 khối ghép từ K: số khớp các bảng 🔒 (A/A ra khác vì máy khác — bài đã ghi là minh họa).

## m3 — Bài 7–9 (review)

- Chạy lại 4 khối: Wilson/cỡ mẫu, SQNR + solver, McNemar, Pareto + winner's curse — đều khớp 🔒.
- **Niêm phong (3 chỗ):** Bài 7 chấm mô hình nêu "5–10 điểm" (đáp án Q3); Bài 8 đoạn sau mô phỏng nói sẵn kết luận outlier (Q4); Bài 9 câu dự đoán 2 đã được phần 2 trả lời → đổi câu hỏi sang dữ liệu Bài 8 của người học.
- **Chiều sâu:** mô phỏng McNemar sinh suy giảm đều mọi task nhưng output có một task "sụp" (task 7: 0,70→0,48) → thêm cảnh báo bội so sánh (Holm/Bonferroni) và xác nhận trên init state mới.
- **Nhãn:** RAM N100 "16 GB" → `[tự đo]`. Nguồn "benchmark VLA trên Intel 75% vs 70%" vẫn chưa truy được (web search không thấy).
- Kiểm: Wilson, χ² 2 bậc tự do [0,16; 1,92], McNemar 12/20 p≈0,50, rule of three, byte weight SmolVLA, ECMWF single precision 2021, Recht 2019 — đúng.

## m5 — Bài 13–15 + Gate (review)

- Chạy lại 5 khối; `compare.py` cần tham số → viết 5 file JSON giả, ra đúng INCONCLUSIVE/INCONCLUSIVE/NEW DATAPOINT/FAIL/PASS; thêm dòng hướng dẫn chạy. `nondet.py` ra 13 giá trị tổng (bài ghi 8) do khác CPU/numpy → sửa 🔒 ghi cả hai, nói rõ phụ thuộc nền tảng.
- **Niêm phong:** hình truy vết Bài 13 dùng đúng cặp 37/50 vs 35/50 kèm phán quyết (đáp án tự kiểm) → placeholder.
- **Nhãn:** "Intel INT8 75% vs 70%" `[spec theo bản gốc]` → "chưa kiểm nguồn", khớp m3.
- **Khung:** Gate phần 12 tên "Tự kiểm tra" → "Đọc thêm và tự kiểm tra" + 3 nguồn.
- **Gate:** đối chiếu `khoa-4-benchmark-edge.md` mục GATE KHÓA 4 và `00-lo-trinh-tong.md` M6: 7 tiêu chí, ±2°C, FAIL action (kể cả ví dụ 3090 vs 4090), "cắt Module 4 không cắt Module 3" khớp nguyên văn; không đổi ngưỡng.
- Nguồn kiểm qua web: slide Gregg IntelON2021 "Processor Benchmarking" tồn tại.

## 00-tong-quan.md (mới)

Theo mẫu K6: vị trí + ngân sách (545 / 885 / 1.106h ≈ 3,3 năm / lõi tối thiểu 885h), Mermaid 5 module, bảng 15 bài → giờ (70h) → F → quyết định, bản đồ chấm mô hình, gate tóm tắt trỏ m5, lịch 13 tuần ≤ 7h (bản gốc 11 tuần lệch giờ bài ở tuần 4, 9, 10), 10 bẫy có câu hỏi ngược gập, bảng sửa lỗi niêm phong, cách học, sau K4.

## Nhận xét hai bên (m1 Bài 1)

- **Claude:** mạnh về bản chất và chấm mô hình người học, mô phỏng có hệ quả vận hành (tuổi observation), liên kết ngoài. Yếu: vẫn để lọt một import cố định và một con số đáp án trong câu chuyện; lặp lại lỗi đếm "1%" của bản gốc.
- **Kiro:** mạnh về kiểm dữ liệu thật (`info.json`), bước thực hành đo được (nhiễu cố định, fit affine), bảng "Nếu ra khác" thực dụng. Yếu: ít chấm mô hình của chính người học, câu hỏi ngược ít sắc hơn.
