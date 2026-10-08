# Nhật ký hợp nhất — Khóa 3, đơn vị m-k3b (m2, m3, m4)

Người hợp nhất: agent m-k3b, 2026-10-08. Nguồn: `khoa-3-chuoi-audio.md` dòng 577–1095, `detail/Gemini-khóa 3-*.md`, bản C (`giao-trinh/khoa-3/`), bản K (`giao-trinh-kiro/khoa-3/`). Mọi khối Python `# [đã chạy]` của bản cuối đã chạy lại trong `_scratch/m-k3b/` (MPLBACKEND=Agg); `soak_monitor.py` chạy thử 2 s với tham số dòng lệnh.

## m2-do-tre.md

### Bài 8 — Latency budget
- Bản nền: **C**. Giữ đúng 8 chặng của gốc (K gộp ring + DMA thành 7), có bảng hình dạng phân bố từng chặng, tham số tra cụ thể (Form timestamp 1 s, group delay PCM5102A), câu chuyện PERT/Polaris.
- Ghép từ K: trường hợp đồng biến (comonotonic: cộng p99 đúng bằng p99 tổng) thêm thành một dòng vào mô phỏng; Little W = L/λ (mức đầy, không phải dung lượng) thành câu bản chất 4 và một mục chấm mô hình; ý "mỗi chỉ số độ trễ một nút thắt" (độ trễ dừng khi kill chỉ gồm ⑤–⑧) vào khối 🔒; câu [Phản biện] "DMA 40 ms chẳng đáng"; câu tự kiểm tra Little; phép thử 0,006 → 0,012.
- Mâu thuẫn: không.
- Lỗi: K tự kiểm tra câu 2 viết p99 tổng "có thể 20 hoặc 120 ms tùy mẫu" (1 − 0,995² = 0,9975% < 1% nên p99 lý thuyết là 20 ms): không đưa vào bản cuối.

### Bài 9 — TN-2
- Bản nền: **C**. Ngân sách sai số đầy đủ hơn, hai chế độ đo (khởi động lạnh / trạng thái dừng) với lập luận độ dốc (desc − 1), số mô phỏng niêm phong, OPERA/HFT.
- Ghép từ K: kênh D4–D6 phía DAC (tách GPIO→DOUT khỏi DOUT→mic), Bước 0 đo dụng cụ (skew giữa kênh, chi phí toggle), hồi quy 5 khoảng cách thay "trừ 0,87 ms" (C chỉ có 2 khoảng cách), lỗ âm đáy INMP441, phương pháp dự phòng bằng chỉ số frame + hiệu chuẩn một lần, chấm mô hình "độ phân giải ≠ độ chính xác", câu hỏi "b âm", lỗi gốc "1M mẫu ở 8 MHz = 125 ms vẫn không đủ", lỗi Gemini "click 10 mẫu".
- Mâu thuẫn: độ trễ giữa luồng: C "≈ (desc − 1) descriptor", K "≈ tổng frame trừ 0–1 descriptor". Không mâu thuẫn thật (cùng khoảng); giữ C, nhãn `[ước lượng]`, kiểm bằng độ rộng xung marker.
- Lỗi kỹ thuật: **K** khối hồi quy ghi `[đã chạy với dữ liệu tổng hợp]` nhưng là đoạn rời, chạy báo `NameError: np` → viết lại khối đầy đủ có dữ liệu tổng hợp, đã chạy.

### Bài 10 — Latency vs underrun
- Bản nền: **C**. Mô hình CCDF "đuôi × số cơ hội", thí nghiệm hog H ms (WCET) kiểm mô hình, quy tắc ba với cảnh báo 10 phút chỉ đủ vẽ hình dạng.
- Ghép từ K: telemetry mức đầy ring + DMA để kiểm Little, ≥ 60 phút ở hai điểm sát vách, khoảng Poisson chính xác qua χ² (đã kiểm: 2 sự kiện/1 h → [0,24; 7,2]/h), WiFi gây sụt áp lẫn với underrun, chấm mô hình "10 phút 0 underrun" (e⁻¹ ≈ 37%), câu [Quy mô] K7 C4.1/C12.1, hai SLI (số lần vs thời lượng im lặng), tự kiểm tra slot 32-bit (511 frame) và so A/B có CI.
- Mâu thuẫn: khe dư cho khựng phía ESP32: C dùng (desc − 1)·T, K dùng cả DMA. Giữ C (cận dưới đúng hơn khi task vừa nạp xong một descriptor).
- Lỗi: cả hai đã sửa 1280 frame > 4092 byte → 1000.

## m3-tts-kien-truc.md

### Bài 11 — RTF
- Bản nền: **K**. Hình hai đường lũy kế, mô phỏng A–E (RTF < 1 không đủ, RTF > 1 không cấm), chính sách chuyển chế độ có hysteresis, ODD; Bài 13 dựa trên mô phỏng này.
- Ghép từ C: bảng "ba cách nhìn" (ρ = RTF, RTF(L) = a/L + b, Gazebo ngược), mô phỏng p99 của 17 mẫu, known-answer test cho harness, câu dự đoán RTF(L). Harness viết lại: gộp K (đo từng chunk, đệm cần) với C (đếm theo số mẫu, ghi MHz, JSONL), giữ lần lạnh có cờ `cold` thay vì vứt (đúng lời của chính K mà code K lại vứt).
- Mâu thuẫn: không về sự thật.
- Lỗi: **K** harness bỏ warm-up khỏi dữ liệu trong khi thân bài yêu cầu "ghi riêng lần lạnh" → sửa.

### Bài 12 — TTS tiếng Việt trên N100
- Bản nền: **C**. Bảng ứng viên đã kiểm (VieNeu v3 Turbo 48 kHz/Nano 24 kHz/v2 deprecated, RTF tác giả trên i5 Gen12; VietTTS code Apache-2.0 nhưng trọng số CC BY-NC, Docker cần GPU NVIDIA): người hợp nhất kiểm lại README hai repo 10/2026, khớp. Cây quyết định, cận dưới roofline.
- Ghép từ K: luận điểm "thêm thread không miễn phí" + chấm mô hình, quét thread 1–4, A/A, chạy offline + rút mạng làm bằng chứng Gate 1, phiên bền vững 30 phút (C: 10) và lặp với tải nền thật đếm underrun, nghe mù, phương án đổi I2S lên 48 kHz, câu hỏi "đọc sai số" (Goodhart), tự kiểm tra A/A.
- Mâu thuẫn: **GPU thuê.** Gốc (và C) cho "pre-render hoặc GPU thuê theo lô"; K: GPU thuê vi phạm Gate tiêu chí 1 và quyền riêng tư. Giải theo K: GPU thuê chỉ là điểm so sánh; cây quyết định và mẫu `decisions.md` đã sửa.

### Bài 13 — Streaming chunk đầu
- Bản nền: **K** (C không có). Kiểm A–H: cầu nối TTFB/HTTP chunked/SSE có "Gãy ở chỗ" audio phải liên tục; sửa lỗi gốc "stream total-time ≈ batch" (stream xong sớm hơn ≈ G − g₁; thứ không đổi là thời gian CPU) và "RTF > 1 thì phải đứt" (không đứt nếu đệm P ≈ (RTF − 1)·D). Đối chiếu Gemini Bài 13: lỗi tương tự, K đã sửa. Brutlag 2009, Stivers PNAS 2009 có thật. Không sửa thêm.

## m4-he-thong-v1.md

### Bài 14 — Ingest, dedupe, state machine
- Bản nền: **C** (mô phỏng ba chính sách khôi phục, checkpoint, `boot_id`, lõi SQLite CAS). Cắt chữ độn: 5557 → ~5400 từ wc (gồm ~800 từ code).
- Ghép từ K: trạng thái `INTERRUPTED` (C dùng `FAILED(interrupted)`) vào sơ đồ, bảng khôi phục và code ALLOWED; retry chỉ cho lỗi trước khi phát; đối soát định kỳ, HMAC webhook; property test hai bất biến + kiểm chính bài test bằng bản ngây thơ; Gemini "SQLite không hỏng nhờ WAL" (sai nguyên nhân); double-click Approve.
- Niêm phong: bốn kết luận của mô phỏng nằm ngoài khối 🔒 ở C → chuyển vào mục 7, thêm câu dự đoán P5.

### Bài 15 — Moderation và kill switch
- Bản nền: **C** (bốn tầng L0–L3, XSMT qua nút NC, Therac-25, bất biến + đột biến).
- Ghép từ K: tầng L3 cắt nguồn amp và chân mute amp vào bước làm, thử trạng thái an toàn mặc định, `KILLED` không xóa dòng (giữ audit), CHECK `approver_id`, không log định danh người gửi, Hawaii 2018 (liên kết), câu hỏi "approve nhầm", tự kiểm tra 490 ms + REARM.
- Mâu thuẫn: khung pháp lý. C: Luật 91/2025/QH15 + Nghị định 356/2025/NĐ-CP thay NĐ 13/2023, hiệu lực 01/01/2026; K: chỉ "Luật BVDLCN" `[tự đo]`. Người hợp nhất kiểm qua tóm tắt EY/PwC/trang pháp luật: C đúng; nâng nhãn `[spec]`, giữ khuyên đọc toàn văn.
- Bỏ chấm mô hình lượt 6 (đã chấm ở Bài 10) để tránh trùng.

### Bài 16 — Daemon, watchdog hai tầng
- Bản nền: **C** (K không có). Kiểm A–H: số mặc định systemd/journald/ESP-IDF TWDT có nhãn; Clementine/NEAR, Pathfinder, Waterfall có thật. Cắt: viết lại mục 5, gộp liên kết tàu vũ trụ vào Erlang, bỏ vài dòng bảng; thêm → K7 C4.4. Thêm câu "dự đoán P2 trước khi chạy" cho mô phỏng watchdog.

### Bài 17 — Soak 72h
- Bản nền: **C** (K không có). Theo yêu cầu điều phối: nối soak ↔ SLO (→ F7.4, F7.6): hợp đồng soak là bảng SLI/SLO viết trước; liên kết K7 sang mã mới (C10.3 soak, C1.2 power budget, C1.4 DC-DC, C12 sản phẩm). Cắt: 7037 → ~6400 từ wc (gồm ~1000 từ code): viết lại mục 5, 6, 11, bỏ liên kết burn-in, bỏ vài dòng thuật ngữ/nếu-ra-khác.
- Niêm phong: kết luận mô phỏng rò rỉ ("hồi quy không phân biệt A/B") chuyển vào khối 🔒.
- Đã kiểm: GAO IMTEC-92-26, FAA AD 2015-09-07, Zheng FAST 2013, Pillai OSDI 2014, Hanley & Lippman-Hand JAMA 1983.

### Gate Khóa 3
- Bản nền: **C** (quy trình gate). Theo ghi chú điều phối, khối tiêu chí chép nguyên từ `00-tong-quan.md` (đơn vị m-k3a): tiêu chí 2 "≥ 100 chu kỳ LRCK" (thay "≥ 1000 chu kỳ" của C), 3 "giá trị đọc lại", 5 "< 3 dB trên sin số, giọng chỉ xu hướng 8/4 bit ≈ 4 × 6,02 ± 3 dB", 6 dòng "không khí". Số thực tế (< 0,1 / < 1 dB) để trong 🔒 của tổng quan và Bài 7, không lặp ra ngoài. Thêm bằng chứng tiêu chí 1 ba lớp (CI grep, offline + rút mạng Bài 12, egress soak).

## Nhận xét hai bản
- **C** mạnh ở: tra cứu và kiểm sự thật (README model, license trọng số, mặc định systemd/journald, pháp lý mới), câu chuyện có thật, mô phỏng có số niêm phong, phân tích thống kê (rule of three, cỡ mẫu). Yếu: dài, có kết luận mô phỏng lộ ngoài 🔒 (Bài 14, 17), đôi chỗ trùng chấm mô hình giữa các bài.
- **K** mạnh ở: thiết kế thí nghiệm thực hành (kênh DAC riêng, hồi quy nhiều khoảng cách, telemetry kiểm Little, quét thread, offline proof), bám Gate và an toàn sản phẩm (GPU thuê vs tiêu chí 1, HMAC, audit, L3). Yếu: một khối code `[đã chạy]` là đoạn rời không chạy được; harness lệch với lời dặn của chính bài; một đáp án tự kiểm tra nói mập mờ ở mép 1%.
