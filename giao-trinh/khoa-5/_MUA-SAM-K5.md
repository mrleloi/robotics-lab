# Theo dõi mua sắm K5 (đợt 3 — tầng T0)

Nơi tập trung các món của "Danh sách mua tầng T0" (`m0-chon-phan-cung.md`, Bài 1): link Shopee, phân loại cần chọn, giá lúc xem, việc phải kiểm khi nhận. Thông số và lý do nằm ở bài gốc. Tầng T1/T2 (máy thứ hai, card NIC có chân PPS) chưa tra.

- Giá là giá hiển thị trên Shopee ngày **2026-10-09**, chưa trừ voucher, chưa tính ship.
- Các file mua sắm khác: `khoa-1/_MUA-SAM-K1.md`, `khoa-2/_MUA-SAM-K2.md`, `khoa-3/_MUA-SAM-K3.md`, `khoa-7/_MUA-SAM-K7.md`.
- Món mua ở đây được dùng lại ở K7: IMU và camera (C7), VL53L1X (C8).

**Trạng thái:** `đề xuất` · `hỏi shop` · `đã đặt` · `đã nhận` · `đạt` · `trả` · `bỏ`.

---

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| ESP32-S3 DevKit × 2 | Hai con đã mua ở K1 | — | 0 | có từ K1 | |
| IMU × 2 | MPU6050 GY-521 × 2 (PVN ĐIỆN TỬ) | https://shopee.vn/product/16504852/25071660729 | 2×57,1k | đề xuất | 4,95★/233, 2k+ lượt bán. **ICM-42688 không có module breakout giá hợp lý trên Shopee** (chỉ chip trần LGA-14, module có MCU riêng nói UART, hoặc module 880–960k); xem ghi chú K7 C7. MPU6050 là phương án "rẻ, nhiều tài liệu" của bài; hàng nhái nhiều → đọc `WHO_AM_I` (0x68) khi nhận. Rẻ hơn một chút và mới hơn: MPU6500 58k https://shopee.vn/product/107147748/10104475147 (5★/25) |
| ToF VL53L1X | CJMCU-531 (SAMIORE.vn) | https://shopee.vn/product/578443443/23266524871 | 106,5k | đề xuất | 5★/36. K7 C8 mua thêm 2 cùng link |
| BME280 | Một trong hai con mua ở K1 | — | 0 | có từ K1 | |
| Webcam USB × 2, **khác model** | (1) Logitech C270 (Trọng Ân Audio); (2) VOVOVA 1080p/720p | https://shopee.vn/product/1767144395/53407361100 · https://shopee.vn/product/1161750510/25907999183 | 461,2k + 94,1k | đề xuất | C270: 4,98★/540, chính hãng Logitech, UVC, 720p lấy nét cố định; dùng lại ở K7 C7/C8. VOVOVA: 4,85★/339, 50k+ lượt bán, thông số cảm biến không ghi → chính vì vậy mà đo thời gian đọc rolling shutter ở Bài 11 có ý nghĩa. Khi nhận: `v4l2-ctl --list-formats-ext` cho cả hai |
| LED + điện trở | Kit K1 | — | 0 | có từ K1 | |
| Cáp Ethernet Cat6 × 2 | Vention Cat6 bấm sẵn, chọn 1 m | https://shopee.vn/product/95236094/7742397896 | 2×26,8k | đề xuất | 4,94★/1.429 |

**Tạm tính K5 tầng T0 (chưa ship):** ~0,83tr.

**Không mua** (theo bài): Raspberry Pi, Jetson, lidar, máy in 3D, GPU.
