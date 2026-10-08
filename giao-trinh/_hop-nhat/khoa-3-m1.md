# Nhật ký hợp nhất — Khóa 3 · m-k3a (`m1-chuoi-phat.md`, `00-tong-quan.md`)

Người hợp nhất: agent m-k3a, 2026-10-08. Nguồn: bản Claude (`giao-trinh/khoa-3/m1-chuoi-phat.md`, Bài 1–4), bản Kiro (`giao-trinh-kiro/khoa-3/m1-chuoi-phat.md`, Bài 1–7 + checkpoint; `00-tong-quan.md`), gốc `khoa-3-chuoi-audio.md` dòng 1–576 và 1004–1095, Gemini K3. Mọi khối Python `[đã chạy]` của bản cuối đã chạy lại trong `_scratch/m-k3a/` (5 khối, đều ra đúng số in trong bài).

## Header module
- Nền: K (34h, Mermaid, bảng viên nang). Ghép từ C: câu "chuỗi đi một chiều" và nhắc niêm phong. Thêm F4.1, F5.3, F2.5 vào cột viên nang. Bản C ghi 32h (theo gốc) — sai cộng; 2+5+5+6+4+5+7 = 34h.

## Bài 1
- Bản nền: **K**. Có chấm lượt 1, phép tính `int()` vs `round()`, câu tự kiểm UART 921 600 baud (dẫn thẳng sang chọn cổng ở Bài 4).
- Ghép từ C: câu chuyện Reeves/PCM; ý "OS giấu chứ không xóa các tầng" trong chấm lượt 1; mô hình "nhiều bit = to hơn" (SAI).
- Mâu thuẫn: C chấm "sample rate càng cao càng tốt" là SAI, K chấm ĐÚNG MỘT PHẦN → giữ K (sample rate cao thật sự nới bộ lọc chống alias; chỉ sai như quy tắc).
- Lỗi đã sửa: K ghi μ-law "~13-bit" → A-law ~13, μ-law ~14 bit. Kiểm lại: frame 1 stereo = (3766, 7482) hex `b6 0e 3a 1d`; lỗi `int()` 0,369 vs `round()` 0,083 LSB² (6,49 dB) — chạy lại, khớp.
- Bỏ: script đọc header của C (K đã có bước tự viết parser `struct.unpack` + cảnh báo chunk `LIST`).

## Bài 2
- Bản nền: **K**. Chấm cả lượt 2 và lượt 3 (C chỉ chấm lượt 1 và 3), bảng chân đầy đủ (flash 26–32, PSRAM 33–37, UART0), bảng sin 600 frame, timing ASCII.
- Ghép từ C: đoạn "kernel thường có đuôi trễ lập lịch tới ms → Linux không đánh nhịp dây" (+ liên kết K7 C4.3); ESP-ADF; dự đoán/đáp án hành vi auto-clear khi ngừng ghi; đo BCK bằng DC V (~1,6 V) ở "Nếu ra khác" và tự kiểm; câu hỏi [Failure mode] "host treo".
- Lỗi đã sửa: K viết khi SCK hở "DAC chờ một master clock không bao giờ tới" → cơ chế đúng: PCM5102A dùng PLL theo BCK khi không có SCK; chân thả nổi nhặt nhiễu, hành vi `[tự đo]`.
- Mâu thuẫn: C dùng "bảng 54 mẫu → 444,4 Hz", K "bảng 55 → 436,36 Hz" — cả hai đúng số học; giữ K.

## Bài 3
- Bản nền: **C**. Mô phỏng sai số trọng tài có bảng min/max và gộp 200 chu kỳ, thí nghiệm phá thêm (đổi khung MSB ở firmware để decoder sai thật), biến thể GND (cấp bằng sạc rời), clock nguồn 160 MHz/bộ chia phân số, nhiều chỗ sửa bản gốc hơn.
- Ghép từ K: chấm "resolution = accuracy" (SAI) và "decoder OK = chuỗi OK" (ĐÚNG MỘT PHẦN); ghi chú analyzer clone mất mẫu qua USB; `sigrok-cli` xuất CSV; câu [Phản biện] "đọc lại config là đủ". Chấm lượt 2 của C rút gọn thành một ý (UART/USB/Ethernet không có dây clock riêng) vì lượt 2 đã chấm ở Bài 2 (bản K).
- Mâu thuẫn sự thật: thí nghiệm FMT lên 3,3 V — K viết DAC đọc "giá trị gần ×2"; C viết bit đầu (LSB của từ trước) bị đọc như bit dấu, dấu gần như ngẫu nhiên. Tự kiểm: ở left-justified, DAC đọc [LSB_trước, b15…b1] → các bit dời xuống một vị trí (độ lớn ~½), dấu do LSB từ trước quyết. **C đúng, K sai.**
- Lỗi đã sửa (C): "ở 3,072 MHz một xung có thể bị nhìn thành 2 hoặc 3 mẫu" → 7,8 mẫu/chu kỳ nghĩa là 3–4 mẫu mỗi nửa chu kỳ.
- Bỏ để giữ ≤ ~4.500 từ: liên kết tcpdump, câu hỏi MiFID II. Thêm liên kết K7 C3.3 (encoder trên logic analyzer).

## Bài 4
- Bản nền: **C**. Pathfinder (priority inversion — đúng chỗ cho task nạp DMA), bảng chấm lượt 7 đầy đủ (RAM/flash/clock/1000×/frame) đúng mục 7 quy chuẩn, script đo jitter producer, câu hỏi push-vs-credit.
- Ghép từ K: bufferbloat; hệ quả "ring buffer không miễn phí độ trễ"; định cỡ ring theo p99 × tần suất (100 burst/s × 1% = ~3600 tách/giờ); **mô phỏng kiểm Little độc lập** (W đo trực tiếp vs L/λ, khớp ~0,5 ms) thay mô phỏng của C; bước chọn cổng USB; host streamer chờ credit; chấm "proxy" và "time.sleep trôi" ở lượt 6; FIFO I2S trên ESP32-S3 làm phản ví dụ lượt 7.
- Định luật Little: cả hai bản đã chỉ ra; bản cuối nói thẳng ở câu chuyện, mô hình (W = L/λ, DMA đầy là trường hợp riêng), mô phỏng, và mục 11.
- Mâu thuẫn sự thật: đáp án tự kiểm "vì sao cần ring khi đã có DMA" — C: "DMA phải nhỏ để trễ thấp"; K: "tổng trễ như nhau, tách quyền kiểm soát". Theo Little, với luồng liên tục và credit giữ ring gần đầy, trễ = (L_ring + L_dma)/fs → **K đúng**; sửa đáp án và câu hỏi "vì sao không DMA lớn".
- Cả hai bản cùng phát hiện lỗi gốc 3 × 1600 frame (6400 byte > trần 4092 → ~128 ms). Giữ; báo đơn vị Module 2 về điểm 1280 frame ở Bài 10.
- Thêm số đo của người hợp nhất cho jitter producer (máy ảo nhàn: p50 ≈ 0,11–0,12 ms, p99 ≈ 0,5–0,9 ms, max ≈ 4,4 ms; hai lần chạy).
- Độ dài: ~5.600 từ theo `wc -w` gồm ~1.000 từ code/mẫu dự đoán (văn xuôi ~4.650). Đã cắt các hàng/câu hỏi trùng; chưa cắt thêm vì bài phải chứa cả Little, lượt 6 và lượt 7.

## Bài 5
- Bản nền: **K** (bản C không có). Kiểm theo A–H: phép tính 0,4 mW / 8 mW, trần BTL 5/√2 ≈ 3,5 Vrms → ~3,1 W vào 4 Ω, dòng nguồn ~0,7 A/kênh, class-AB ≤ 78,5%, PAM8403 3 W ở THD 10% — đúng. Chấm lượt 9 có đủ.
- Lỗi đã sửa (K): câu chuyện "ba bậc độ lớn" giữa vài chục mW và vài W → cỡ hai bậc; câu hỏi quy mô mini PC "chạy liên tục" → khung 8 giờ, gắn `[ước lượng]`.

## Bài 6
- Bản nền: **K** (bản C không có). Mô hình Thevenin, sụt áp ≠ quá tải, BOD nhìn rail 3,3 V sau LDO, tụ bulk τ = R_s·C (kiểm: ωRC = 0,63 ở 200 Hz → giảm ~15%, đúng), đo R_s bằng hai điểm tải, ADC min-hold. → F5.7 có ở Vị trí, mô hình, cầu nối, câu hỏi.
- Thêm (bắt buộc theo đề): chấm **lượt 12–13** đặt ở đây (bản K đặt ở Bài 7). Viết lại theo ba trục: ĐÚNG ở ước lượng thay đo trực tiếp (Kalman, soft sensor, RNNoise, SDR, ADC min-hold của chính bài); SAI vì không vượt Nyquist/Shannon (C = B·log₂(1+S/N), kTB, không khôi phục được 16-bit từ 4-bit); SAI ở "công thức vật lý gần như hằng số" — tham số trôi, mô hình đúng trong phân bố, sai ngoài phân bố (phản ví dụ: mô hình học trên cấu hình 3 dự đoán sai cấu hình 1). Lượt 13: ĐÚNG / CHƯA RÕ / ĐÚNG MỘT PHẦN.
- Lỗi Gemini ghi thêm: lượt 12 coi mọi hệ vật lý là hỗn loạn; lượt 13 "DLSS giảm năng lượng một nửa" không nguồn. Sửa nhận xét của K: "75% điểm ảnh" không phải số bịa mà là phép tính 1080p → 4K (vẫn không phải số đo).
- Cắt để giữ ~4.500 từ: câu hỏi cáp 2 m/loa 8 Ω, câu hỏi datacenter, liên kết thundering herd, vài hàng thuật ngữ.

## Bài 7
- Bản nền: **K** (bản C không có). Sửa SNR đúng mục 7 quy chuẩn: Mô phỏng 1 kiểm 6,02·N + 1,76 trên sin số tạo bằng code (round/floor/bỏ DC/−20 dBFS/dither), Mô phỏng 2 cho thấy phương pháp "sàn nhiễu ở đoạn im lặng" của gốc gãy (∞ với round), phương pháp B (e = x_n − x_16) bám xu hướng ở 8 và 4 bit. Cả hai khối đã chạy lại, khớp từng số.
- Đổi: chấm lượt 12–13 chuyển sang Bài 6; thay bằng chấm "thêm bit là thêm chất lượng". Thêm bước kiểm dải sample rate INMP441 (không xác minh được dải WS từ datasheet gốc qua web — để `[spec: tra]`).
- Mâu thuẫn ngưỡng: K đặt tiêu chí gate "< 0,1 dB ở 16/12/8, < 1 dB ở 4 bit" (từ mô phỏng của chính nó); C (m4) giữ "< 3 dB" của gốc áp lên sin số. Giải: giữ ngưỡng gốc < 3 dB (không cắt xương sống), ghi kết quả thực tế < 0,1/< 1 dB trong khối 🔒 và bắt giải thích mọi lệch > 1 dB. Giọng thật: giảm ≈ 4 × 6,02 ± 3 dB từ 8 xuống 4 bit.
- Cắt: hai câu hỏi ngược (dither mọi tầng, ENOB), một liên kết, vài hàng thuật ngữ/"nếu ra khác". ~5.000 từ gồm ~1.000 từ code.

## Checkpoint cuối Module 1
- Nền: **K**. Hài hòa tiêu chí 7 với gate (< 3 dB trên sin số; xu hướng giọng).

## 00-tong-quan.md
- Nền: **K** (bản C chưa có file). Giữ: con số 545h / 885h / 1.106h (đã cộng lại: K7 lõi 561h = tổng giờ 13 chặng trong `_KE-HOACH-K7.md`), lịch 16 tuần khớp 92h (gốc 12 tuần chỉ cộng 83h), 10 bẫy, cách học, prompt chấm mô hình.
- Gate: hợp nhất bản C (`m4-he-thong-v1.md`, Gate cuối file) và bản K: thêm kiểm egress (tiêu chí 1), "Form → Sheet" (6), "thẻ → đĩa", bằng chứng "đúng lúc đang ghi" và cận trên 95% (7) từ C; "đọc lại dma_frame_num" (3), "đo qua nhiều chu kỳ" (2), R_s/ADC (4) từ K. Ngưỡng tiêu chí 2: C "≥ 1000 chu kỳ", K "≥ 100 LRCK, ≥ 32 BCK" — cả hai đủ cho 1% (100 LRCK = 100 000 mẫu analyzer); dùng bản K. Trỏ sang bài Gate trong m4 cho quy trình.
- **Ghi chú cho m-k3b (m4):** tiêu chí 5 trong Gate của m4 hiện ghi "< 3 dB trên sin số, giọng chỉ xu hướng" — khớp tổng quan; nên thêm "≈ 4 × 6,02 ± 3 dB từ 8 xuống 4 bit" và "giải thích lệch > 1 dB" cho thống nhất. Tiêu chí 2 m4 ghi "≥ 1000 chu kỳ" — không sai, nhưng tổng quan dùng "≥ 100 chu kỳ LRCK".
- Bản đồ chấm mô hình: lượt 12–13 trỏ Bài 6.

## Nhận xét hai bên
- **Claude** mạnh ở: phát hiện lỗi của chính bản gốc bằng thí nghiệm phản chứng (firmware khung MSB, GND đi vòng qua USB), lịch sử thật (Pathfinder, Reeves, USB Audio Class), bảng chấm lượt 7 chi tiết. Yếu: không liên kết K7; dài hơn; một đáp án mâu thuẫn Little ngay trong bài Little.
- **Kiro** mạnh ở: phủ đủ 7 bài, định lượng hóa (ring theo p99 × tần suất, R_s hai điểm, τ = RC, mô phỏng kiểm Little độc lập, phương pháp A/B cho SNR), liên kết K7 đúng mã. Yếu: một lỗi vật lý (FMT "×2"), vài câu cơ chế mơ hồ (SCK "chờ clock"), đặt chấm lượt 12–13 sai bài, Bài 7 quá dài.
