# Theo dõi mua sắm K1 (đợt 1)

Nơi tập trung các món đã chọn cho "Danh sách đợt 1" ở Bài 4 (`phan-b-dung-cu.md`, mục 2): link Shopee, phân loại cần chọn, giá lúc xem, việc phải hỏi shop hoặc kiểm khi nhận. Thông số phải chọn và lý do nằm ở bài gốc; file này chỉ ghi **mua ở đâu** và **đang ở trạng thái nào**.

- Giá là giá hiển thị trên Shopee ngày **2026-10-09**, chưa trừ voucher, chưa tính ship. Giá đổi theo ngày.
- Link dạng `shopee.vn/product/<shop>/<item>`. Khi bấm vào, chọn đúng **phân loại** ghi ở cột "Chọn".
- Các file mua sắm khác: `khoa-2/_MUA-SAM-K2.md` (mini PC), `khoa-3/_MUA-SAM-K3.md`, `khoa-5/_MUA-SAM-K5.md`, `khoa-7/_MUA-SAM-K7.md`. K4 và K6 không phải mua gì (K4 thuê GPU theo giờ).

**Thực tế đã mua (người học báo 2026-10-09)** — khác bảng dưới, bảng giữ làm tham chiếu:
- Kit Arduino Upgraded Learning Kit 36 món (UNO R3, breadboard MB-102, jumper đực–đực 65 + đực–cái 10, LCD1602 I2C, LED RGB, 15 LED, còi, SG90, 28BYJ-48 + ULN2003, relay 1 kênh, joystick, bàn phím, IR, RC522 + 2 thẻ, RTC, DHT11, LM35DZ, 3 LDR, biến trở 10k, 5 nút, 74HC595, 30 điện trở…).
- Mỏ hàn 926, một mũi nhọn, thiếc, bọt biển, nhựa thông; đồng hồ vạn năng (model chưa ghi); breadboard; adapter 9 V SM0920 + mạch nguồn breadboard 5 V/3,3 V.
- Logic analyzer 24 MHz 8 kênh **loại "ARM FPGA" của Lập Trình Nhúng A-Z [102]** (202,5k): đúng loại bảng dưới khuyên tránh. Kiểm `lsusb` / PulseView `fx2lafw` trước Bài 9.
- ESP32-S3 N16R8 G182 **×1** (175,6k); USB tester KWS-X1 60 W (thay J7-C).
- **Chưa mua** (K7 vẫn cần): kính bảo hộ, kìm cắt, kit điện trở, cáp USB-C dữ liệu, ESP32-S3 thứ hai, BME280. Đưa vào `khoa-7/_MUA-SAM-K7.md` mục 0.3 (trừ BME280: K7 không dùng).

**Trạng thái:** `đề xuất` (đã chọn, chưa mua) · `hỏi shop` (phải nhắn shop trước khi đặt) · `đã đặt` · `đã nhận` · `đạt` (qua phép kiểm khi nhận, Bài 4 bước 2) · `trả` · `bỏ`.

---

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| Multimeter UNI-T UT33D+ | "Đồng hồ đo điện vạn năng UT33D+ (đã có pin)" | https://shopee.vn/product/445288039/21076029442 | 280k | đề xuất | 4,93★/442. Kiểm model in trên mặt; ghi định mức cầu chì cổng mA/10A. Shop ghi rõ "chính hãng Uni-Trend": 295k https://shopee.vn/product/827280094/19751817079 |
| Logic analyzer 8 kênh 24 MHz | "Mạch USB Saleae Logic Analyzer 8 kênh 24Mhz" (Thế Giới Module) | https://shopee.vn/product/951399259/28117810150 | 248k | **hỏi shop** | 5★/11. Mô tả không ghi chip → hỏi có phải CY7C68013A (FX2) không. Khi nhận: `lsusb` ra VID:PID (bản sao Saleae thường 0925:3881), đọc chip trên board. **Tránh** loại ghi "ARM FPGA" (vd. Lập Trình Nhúng A-Z 220k): không chắc chạy `fx2lafw` |
| Móc kẹp test (test hook) | "Combo 2 Chiếc Móc Kẹp Test Logic" × 4 (Lập Trình Nhúng A-Z) | https://shopee.vn/product/107147748/19521424188 | 4×10k | đề xuất | 4,94★/18. Chỉ mua nếu logic analyzer không kèm kẹp |
| Dây kẹp cá sấu hai đầu | Bó 10 dây 5 màu 50 cm | https://shopee.vn/product/27117857/853772494 | 39k | đề xuất | 4,87★/1.650 |
| USB power meter | Juwei J7-C, màn hình màu (KSS) | https://shopee.vn/product/1187472145/24118670213 | 124,5k | đề xuất | 4,93★/640. Có cổng USB-A và USB-C. Tần số cập nhật thấp, xem "Gãy ở chỗ" ở Bài 4 |
| Breadboard 830 lỗ × 2 | MB-102 830 lỗ (PVN ĐIỆN TỬ) | https://shopee.vn/product/16504852/12314365791 | 2×32,1k | đề xuất | 4,94★/453. Kiểm thông mạch ở Bài 6 |
| Jumper M-M / M-F / F-F | Bó 40 sợi 7 màu 21 cm, chọn đủ 3 loại đầu | https://shopee.vn/product/301053603/17986569505 | từ 31,4k/bó | đề xuất | 4,90★/2.207 |
| Dây cứng lõi đơn 22 AWG | Dây đồng 1 lõi 0,6 mm, 2 m × 3 cuộn (Lập Trình Nhúng A-Z) | https://shopee.vn/product/107147748/28528882292 | 3×15k | đề xuất | 4,87★/142. 0,6 mm ≈ 22 AWG (0,64 mm) `[chuẩn]`. Mua 3 màu nếu shop có |
| Kit điện trở | Set 600 điện trở 1/4 W 1% 30 giá trị, có hộp | https://shopee.vn/product/770245757/16467277984 | 59,8k | đề xuất | 4,88★/439. Kiểm có 1 MΩ; set 30 giá trị thường **không có 10 MΩ** → dòng dưới |
| Điện trở 1 MΩ, 10 MΩ | Gói 20 con 1/4 W, chọn phân loại 1M và 10M | https://shopee.vn/product/301053603/14495614205 | 2×13k | đề xuất | 4,90★/1.309. Cần cho thí nghiệm Bài 5, 9 |
| Tụ hóa các loại | Túi 5 con 25 V, chọn 100 µF, 470 µF, 1000 µF | https://shopee.vn/product/404478549/18061040054 | từ 18k/túi | đề xuất | 4,86★/491 |
| Tụ gốm 100 nF | Xem K7 C5 (cùng listing, phân loại "10 CON 104") | https://shopee.vn/product/404478549/21161544154 | 11,4k | đề xuất | Mua luôn ở đợt này |
| LED | Gói 50 LED đục 5 mm, chọn màu đỏ (và xanh lá) | https://shopee.vn/product/404478549/22408935276 | 23,7k/gói | đề xuất | 4,90★/101. LED đỏ dùng lại ở K7 C9 |
| Nút nhấn | Nút 4 chân 12×12 mm, túi 10 con | https://shopee.vn/product/67030960/17660202913 | 22,5k | đề xuất | 4,90★/103. Nút kill của K3 Bài 15 dùng luôn |
| ESP32-S3 DevKit × 2 | Phân loại "N16R8 (Đã Hàn)" × 2 (Lập Trình Nhúng A-Z, mã G23) | https://shopee.vn/product/107147748/25387897633 | 2×220k | đề xuất | 4,81★/21, 321 lượt bán. Board 44 chân kiểu DevKitC-1, hai cổng USB-C. Phân loại "Đế ESP32-S3" (65k) là **đế ra chân**, không phải board. Bản N16R8 dùng PSRAM octal → GPIO35–37 không dùng được `[spec — datasheet ESP32-S3, kiểm]`. Hai con này dùng tiếp ở K3, K5, K7 C4/C11 |
| Cáp USB có dây dữ liệu × 2 | Ugreen USB-A → USB-C, phân loại "2.0-60116-1 mét" (vitinh123.) | https://shopee.vn/product/81256369/40167900821 | 2×65k | đề xuất | 4,91★/183. Kiểm: truyền file với điện thoại được thì là cáp dữ liệu |
| BME280 × 2 | Phân loại "BME280-3.3V" (aitexm.vn) | https://shopee.vn/product/770245757/17768057005 | 2×187k | đề xuất | 4,95★/22. Mô tả kiểu board Bosch/Mikroe, có jumper địa chỉ I2C. Đọc chip ID ở Bài 11 (0x60 BME280, 0x58 BMP280). Module 37–46k trên Shopee thường ghi lẫn "BMP280" trong tên → rủi ro nhận BMP280 cao |
| Mỏ hàn chỉnh nhiệt | Trạm hàn kiểu Hakko 936, 60 W (Linh Kiện 024) | https://shopee.vn/product/395600519/8639420195 | 440k | đề xuất | 4,86★/570, bảo hành 6 tháng. Hàng kiểu 936 (không phải Hakko chính hãng). Mũi dẹt 900M-T-3.2D: xem K7 C0. Hàng hãng Quick 936A 1.200k https://shopee.vn/product/161859607/2427780801 (4,90★/101, BH 12 tháng) |
| Giá đỡ mỏ hàn | Trạm 936 thường kèm giá; thiếu thì mua đế gác lò xo (iLinhkien) | https://shopee.vn/product/1046767853/23361074358 | 16,8k | đề xuất | 4,95★/120 |
| Bùi nhùi đồng | Bùi nhùi đồng cho mũi 936/907 (iLinhkien) | https://shopee.vn/product/67030960/23083496673 | 40k | đề xuất | 4,98★/49 |
| Thiếc 0,8 mm lõi flux | Thiếc 63% 0,8 mm | https://shopee.vn/product/27117857/387375674 | 64,2k | đề xuất | 4,88★/2.092. Thiếc có chì: rửa tay sau khi hàn (Bài 4, mục an toàn) |
| Flux dạng gel | Mỡ trợ hàn (paste) | https://shopee.vn/product/752771657/14187691115 | 25k | đề xuất | 4,89★/1.318. Bút flux đúng nghĩa: chưa tìm được hàng nhiều đánh giá |
| Dây hút thiếc | Goot Wick (Gootwick) | https://shopee.vn/product/21613238/10855108646 | 52k | đề xuất | 4,97★/397 |
| Cồn IPA ≥ 90 % | IPA 500 ml/1 L | https://shopee.vn/product/1810398513/49162068159 | từ 62,3k | đề xuất | 4,95★/258 |
| Kìm cắt chân linh kiện | Plato 170 | https://shopee.vn/product/118645835/27719279594 | 25,5k | đề xuất | 4,92★/1.889 |
| Kính bảo hộ | 3M Tour-Guard V, đeo được cùng kính cận | https://shopee.vn/product/315348085/8820075173 | 78,5k | đề xuất | 4,92★/2.305 |
| Quạt hút khói hàn | Quạt hút khói hàn 5 W | https://shopee.vn/product/111078417/16382060865 | 226,8k | **hỏi shop** | 4,93★/73. Hỏi có tấm lọc than hoạt tính không. Không có lọc thì đặt quạt thổi khói **ngang ra xa mặt**, mở cửa sổ |
| Nguồn bàn giới hạn dòng | Xem K7 C0 (DF-3010DS) | — | — | | Bắt buộc trước K7 C1; ghi lý do mua/chưa mua vào `decisions.md` |

**Tạm tính K1 (chưa ship, không kể nguồn bàn):** ~3,1tr. Cao hơn ước lượng 2,3–2,9tr của bài chủ yếu vì BME280 loại tốt (2×187k thay vì 2×80k) và quạt hút khói.
