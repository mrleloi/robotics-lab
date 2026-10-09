# Theo dõi mua sắm K3 (đợt 2b — chuỗi audio)

Nơi tập trung các món cho chuỗi audio của K3 (`00-tong-quan.md`, dòng **Chi phí**): link Shopee, phân loại cần chọn, giá lúc xem, việc phải kiểm khi nhận. Lý do chọn thông số nằm ở bài gốc. Đợt này chỉ mua khi **M0 PASS + M1 PASS** (mục 0.6 lộ trình tổng).

- Giá là giá hiển thị trên Shopee ngày **2026-10-09**, chưa trừ voucher, chưa tính ship.
- Mini PC N100 (đợt 2a): xem `khoa-2/_MUA-SAM-K2.md`. ESP32-S3, kit điện trở, nút nhấn, USB power meter: đã có từ K1 (`khoa-1/_MUA-SAM-K1.md`).
- Quy tắc của khóa: **mua 2** mọi module rẻ và quan trọng.

**Thực tế đã mua (người học báo 2026-10-09), mỗi món 1 cái:** INMP441, PCM5102A (GY-PCM5102), MAX98357A (bản EWL), TPA3110 2×15 W 8–18 V (thay PAM8403), loa 4 Ω 5 W Ø52 mm. Quy tắc "mua 2" chưa đạt: thiếu con dự phòng cho DAC, mic, loa. Thêm cầu chì, tụ, điện trở công suất theo bảng dưới khi tới K3.

**Trạng thái:** `đề xuất` · `hỏi shop` · `đã đặt` · `đã nhận` · `đạt` · `trả` · `bỏ`.

---

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| DAC PCM5102A × 2 | Module GY-PCM5102 (SAMIORE.vn) | https://shopee.vn/product/578443443/25609140309 | 2×60,1k | đề xuất | 4,95★/189, 1,2k+ lượt bán. Kiểm cầu hàn/jumper SCK xuống GND (bẫy số 3 của khóa). Đọc mã chip trên module |
| Amp PAM8403 × 2 | "Mạch Khuếch Đại Âm Thanh PAM8403 6W Hifi 2.0 Class D (Có Chỉnh Volume)" | https://shopee.vn/product/449067308/47559965794 | 2×20k | đề xuất | 4,92★/388. Đầu ra BTL: **không nối cọc loa nào xuống GND** (bẫy số 4). Bản không chiết áp: 31,9k https://shopee.vn/product/456730649/12230602220 |
| Loa 4 Ω × 2 | Cặp loa toàn dải 4 Ω 3 W Ø5 cm có tai bắt vít (giá cho 2 cái) | https://shopee.vn/product/61435118/7104357586 | 34,9k | đề xuất | 4,86★/937. Đo Ω DC khi nhận (thấp hơn danh định, Bài 5) |
| Mic INMP441 × 2 | Phân loại "INMP441 ĐÃ hàn" (mcu001) | https://shopee.vn/product/1796207716/50165748578 | 2×45k | đề xuất | 4,97★/87. Trên Shopee có listing ghi rõ "bản thay thế không có mã INMP441" → khi nhận, soi mã khắc trên vỏ mic; khác INMP441 thì ghi vào `decisions.md` và đối chiếu khung I2S ở Bài 7 |
| Điện trở công suất 10 Ω 5 W và 1 Ω | Trở sứ 5 W, chọn phân loại 10 Ω và 1 Ω | https://shopee.vn/product/85716713/2329322478 | 2×9,9k | đề xuất | 5★/52. 1 Ω 5 W thay cho 1 Ω 2 W của bài (dư công suất, không sao) |
| Tụ 470–1000 µF | Tụ hóa 35 V 1000 µF combo 5 con (iLinhkien) | https://shopee.vn/product/1046767853/23952516250 | 26,3k | đề xuất | 4,91★/116. Dùng cho Bài 6 |
| Amp TPA3110 *(nếu chọn thay PAM8403)* | Xem K7 C12 | — | — | | K7 C12 dùng TPA3110 ăn thẳng từ pack |

**Tạm tính K3 (chưa ship):** ~0,33tr, thấp hơn ước lượng 0,7–1tr của khóa.
