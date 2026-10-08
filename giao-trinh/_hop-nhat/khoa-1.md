# Nhật ký hợp nhất — Khóa 1 (đơn vị m-k1)

Ngày: 2026-10-08. Nguồn: `khoa-1-tu-zero-den-do-duoc.md` (gốc), `giao-trinh/khoa-1/*` (C = Claude), `giao-trinh-kiro/khoa-1/*` (K = Kiro). Bản cuối: `giao-trinh/khoa-1/` (5 file). Mọi khối Python `# [đã chạy]` của bản cuối đã chạy lại (13 khối, `MPLBACKEND=Agg`; script gate chạy trong một repo git thử). Giờ từng bài: Phần A 2/1.5/2.5 (C), Phần B 0.5/1.5/0.5/1.5/1 (K), Phần C 5/5/4 (K), Phần D 5/4/1.

## 00-tong-quan
- Bản nền: K (C không có).
- Đã ghép/sửa: đoạn ngân sách viết lại theo quy chuẩn mục 1 và `_KE-HOACH-K7.md` mục 3 (545h; K7 gốc → 885h > 650h; K7 mới lõi 561h → 1.106h ≈ 3,3 năm; đường lõi tối thiểu 885h); thêm đoạn "K7 C0 chạy song song ngay sau Phần B". Bảng giờ cập nhật theo bản cuối. Gate tiêu chí 3: ghi cách đọc (hiệu chuẩn Vin **và** R đo), ngưỡng giữ nguyên. Mục 7 viết lại phần C–D theo bản cuối. Bỏ emoji ✅❌⚠️ trong bảng dùng AI (quy chuẩn mục 5).
- Lỗi đã sửa: K tham chiếu "Bài 3 mục 5 câu 6" (đánh số theo Bài 3 của K, không còn) → Bài 3 câu 3 + Bài 13.

## Bài 1
- Bản nền: C — có đường tải + độ nhạy (+10% nguồn → +16% dòng; bỏ R → ×48), sửa V_f LED xanh lá InGaN.
- Ghép từ K: chuyện Ohm chuyển sang nguồn cặp nhiệt điện; câu dự đoán 12 V (LED và điện trở 1/4 W cùng quá tải, 0,30 W); bước Falstad (ampe kế trước/sau LED); hai dòng "Nếu ra khác".
- Mâu thuẫn: không. Lỗi: không phát hiện thêm.

## Bài 2
- Bản nền: C — chấm "GND là epoch" có phản ví dụ, phân biệt single-ended/vi sai (quan trọng cho K5), 80 mV "vô hại với bit, phá analog".
- Ghép từ K: mô phỏng Python sụt áp/lệch GND (đặt sau commit dự đoán), bước Falstad, chấm mô hình "chung laptop là chung GND", câu hỏi "nối luôn hai cực +", thuật ngữ earth vs signal ground.
- Lỗi đã sửa (C): hai chỗ hứa "K1 Bài 9 đo sụt áp/điện trở tiếp xúc" — Bài 9 không có bước đó → thay bằng phương pháp 4 dây/Kelvin (biết tên).

## Bài 3
- Bản nền: C — mô phỏng setup-time (vách đứng, biên 1,3×), clock nhúng, chấm mô hình K3 lượt 2/6/7 sâu hơn.
- Ghép từ K: chuyện Chaney & Molnar 1973; dự đoán FIFO hai thạch anh ±20 ppm (tràn sau ~67 s), aliasing 13→11 MHz/15→9 MHz, 5 V vào GPIO ESP32-S3; hàng cầu nối "queue không sửa được lệch ppm"; ghi chú I2S nhiều thiết bị chung BCK (MAX98357A). Mô phỏng aliasing của K chuyển sang Bài 7.
- Lỗi đã sửa (C): khung UART giải mã ghi nhãn ô cuối "P" (parity) cho định dạng 8N1 → "Sp" (stop).
- Mâu thuẫn: kỷ lục ép xung — C "1,5–2× [ước lượng]", K "~9 GHz, chưa tới 2×". Không mâu thuẫn thật; giữ C.

## Bài 4 (khung rút gọn)
- Bản nền: K — BOM đủ cho người mới (cáp dữ liệu, kẹp cá sấu, phụ kiện hàn, kính), an toàn khói rosin (HSE), FTDIgate, nối K7 C0.4.
- Ghép từ C: câu chuyện BOM đợt 1 trong repo thiếu ESP32/BME280; hai chấm mô hình (mua 2; LA vs oscilloscope); kiểm hàng trên Linux (`lsusb`, `/dev/ttyACM*`, nhóm `dialout`), dán nhãn module A/B, ghi giá vào `decisions.md`; câu tự kiểm "chưa có ESP32 làm được bài nào".

## Bài 5
- Bản nền: K — viết cho người mới thật: cầm que, quy trình 4 câu trước mỗi phép đo, bài tập đo dòng an toàn qua 1 kΩ, bảng lỗi phá đồng hồ, canary cầu chì, mô phỏng tải đồng hồ.
- Ghép từ C: câu chuyện GUM (loại A/B), mô phỏng bộ phân loại + guard band (false reject ~4,5%, false accept ~27% → 0,1%/19%), ba vùng PASS/FAIL/KHÔNG KẾT LUẬN thay cho "940–1060 Ω" cộng tuyến tính, bảng mã màu có hệ số nhân + 5 vòng, hàng cầu nối "script pass/fail/inconclusive", ILAC-G8.
- Mâu thuẫn sự thật: thang Ω UT33D+ — K "tới 20 MΩ", C "tới 200 MΩ". Kiểm web (trang nhà phân phối): 200 Ω…200 MΩ, ±(0,8%+2); một nhà bán ghi thang 200 MΩ ±(5%+10) → bản cuối ghi 200 MΩ, gắn `[spec, tự đo]`, nhắc thang cao nhất có thể kém hơn. Pin 2×AAA: hai bản khớp, nguồn web khớp.

## Bài 6
- Bản nền: C — bíp là bộ phân loại có ngưỡng, đo ngưỡng (~31 Ω theo review), sửa lỗi gốc "chế độ Ω kêu".
- Ghép từ K: mô phỏng "linter" lỗ→net, quy ước màu dây, ESP32 vắt khe (ghép 2 board), mẹo cắt chân, câu hỏi "breadboard lên robot K7". Giờ 1h → 0,5h để Phần B giữ 5h.

## Bài 7 (chỉ K có)
- Bản nền: K. Kiểm theo A–H.
- Bổ sung: mục "Nyquist cho tín hiệu số" (→ F5.5: tần số / xung hẹp / thời điểm cạnh là ba ngưỡng; "4–10×" không phải hệ quả trực tiếp của Nyquist); chuyển mô phỏng aliasing của K-Bài 3 vào đây (K-Bài 7 tham chiếu một hàm `sample_clock` không tồn tại); cài đặt Linux; câu dự đoán xung hẹp.
- Lỗi đã sửa (K): khẳng định "clock 4 MHz duty 10% → nhiều xung lọt" chưa từng chạy. Chạy thử: ở đúng 4 MHz (24/6 nguyên) pha cố định → bắt đủ 100% với pha ngẫu nhiên đầu; ở 3,9 MHz chỉ bắt ~62%. Sửa mô phỏng và đáp án.

## Bài 8 (chỉ K có)
- Bản nền: K. Đạt A–H; chỉ đổi tên file dự đoán cho thống nhất (`lab/00-dung-cu/bai08-prediction.md`). Xbox 360 RROD ghi đúng mức tin (khoản 1,15 tỉ USD [chuẩn], nguyên nhân [ước lượng]).

## Bài 9
- Bản nền: C — mô hình Thevenin, quy tắc Rth/RL, Monte Carlo trên chính các cặp của lab, kiểm KVL, suy ngược Rm, cách đọc tiêu chí 5% không nới ngưỡng.
- Ghép từ K: chuyện Kaplan & Irvin 2015 (preregistration 57% → 8%), chấm mô hình "±5% là nhiễu giữa các lần đo", điểm "cặp 1k/10k: 5% quá lỏng (1,2 kΩ vẫn lọt, −1,8%)", câu hỏi divider đo pin 4S K7, cấu trúc thư mục lab (đầu Phần C).
- Mâu thuẫn: K-Bài 9 và K-Bài 14 đổi tiêu chí gate 3 thành "dải tính riêng từng cặp"; K-tổng quan giữ "<5%". Giải: giữ tiêu chí gốc (yêu cầu đơn vị), đưa cách đọc của C (so với dự đoán tính từ Vin đo + R đo).

## Bài 10
- Bản nền: C — độ nhạy theo khoảng dư (3,3 V nhạy gấp đôi 5 V), burden qua hai thang, phân biệt ngưỡng 5%/10%.
- Ghép từ K: chế độ diode (V_f ở dòng nhỏ), phần fit tùy chọn 5 điểm (least squares), hàng cầu nối retry storm ↔ thermal runaway, liên kết TCP AIMD.
- Lỗi đã sửa (C, K phát hiện): "dòng đo ra 0 vì vượt thang" — vượt thang hiện `OL`/`1`; tách hai dòng. Giờ 4h → 5h.

## Bài 11
- Bản nền: C — ba tầng con số, săn ngữ nghĩa "staging/commit" (ctrl_hum) và "snapshot" (burst read/shadowing), điều cấm thứ tự cấp nguồn, đối chiếu module bằng đồng hồ.
- Ghép từ K: chuyện Challenger; câu dự đoán có số: thời gian đo forced mode typ/max (8/9,3 ms ở ×1; 98/112,8 ms ở ×16 — đã tính lại); bảng tham chiếu register map để chấm ≥90%; "bảng hợp đồng" min/typ/max; bước đo thời gian đo thật trên PulseView (tùy chọn); câu hỏi "chờ theo typical". Giờ 5h → 4h.
- Mâu thuẫn: mã tài liệu — C "BST-BME280-DS001-12 rev 1.3", K "DS002". Không kiểm lại PDF được → ghi "DS001 bản cũ, DS002 bản mới, đối chiếu revision bạn tải".

## Bài 12
- Bản nền: C — lưới Rp × Cb (t_r, Rp_min 967 Ω), pull-up nội ~45 kΩ giải thích "chạy ở bàn, hỏng khi dây dài", trigger vì WireScan chờ 5 s, sửa "thẳng LOW → thiếu pull-up".
- Ghép từ K: commit dự đoán **trước** khi chạy scanner; bảng thời gian byte/giao dịch/burst (90 µs, ~0,37–0,40 ms, ~1,0 ms, 65%), bước 400 kHz, thí nghiệm treo bus qua 1 kΩ, câu hỏi utilization bus K7, chuyện clock stretching trên Raspberry Pi, SMBus/PMBus trong datacenter, 117 NACK trước 0x76.
- Lỗi đã sửa (C): "đặt con trỏ cách nhau 9 cạnh lên… chia 9" — cạnh lên nhịp 1 tới nhịp 9 là **8** chu kỳ → chia 8. (K): giữ "cả hai thẳng LOW → thiếu pull-up" — sai trên ESP32; không đưa vào.

## Bài 13 (chỉ K có)
- Bản nền: K. Đạt A–H; mô phỏng lượng tử hóa và "tỉ số hai thạch anh" chạy đúng.
- Bổ sung theo yêu cầu: bảng "cấu hình nào analyzer 24 MHz bắt được" (16/32/44,1/48 kHz slot 16; 48 kHz slot 32: sát; 96 kHz slot 32: không tin; TDM 8×32 và MCLK 12,288 MHz: dưới Nyquist), đã tính lại.

## Bài 14 (chỉ K có, khung rút gọn)
- Bản nền: K (script kiểm thứ tự commit, ba trạng thái, câu hỏi về LLM chấm).
- Lỗi đã sửa (K): (1) tiêu chí 3 bị đổi khỏi gốc → trả về "<5% sau hiệu chỉnh Vin", cách đọc ghi riêng; tiêu chí 5 bị thêm "capture chip ID" và tiêu chí 6 "BCLK/LRCK phải đúng 32" → hạ thành khuyến nghị/ghi kèm. (2) Script quét cả `lab/00-*` (bài luyện không có `analysis.md`) → FAIL giả; thêm lọc tên. Đã chạy trong repo thử: PASS/CẢNH BÁO/FAIL đúng. (3) Nhãn Mermaid bọc ngoặc kép.

## Nhận xét chung
- C mạnh ở chiều sâu bản chất: chấm mô hình có phản ví dụ, mô phỏng sát câu hỏi của lab, đọc tiêu chí gốc mà không nới (Bài 9), lịch sử thật đúng chỗ. Yếu: bài dài (Bài 3 ~6.800 từ), vài lỗi tính nhỏ (9 cạnh/8 chu kỳ), hứa bước không tồn tại ở bài khác, và thiếu hẳn bài thực hành tay (7, 8, 13, 14).
- K mạnh ở thực hành cho người mới thật (cầm que, an toàn, lỗi phá đồng hồ, hàn), bắt lỗi bản gốc về quy trình (dự đoán sau scanner, LED 1 Hz với 1M mẫu, Bài 11 thiếu prediction), số có thể tính (thời gian giao dịch, measurement time). Yếu: tự đổi tiêu chí gate, một khẳng định mô phỏng chưa chạy (xung hẹp), tham chiếu chéo giữa bài lệch.
