# KHÓA 5 — CẢM BIẾN, ĐỒNG BỘ THỜI GIAN, DATA PLATFORM

**Cho:** người đã PASS Khóa 2 (MCAP, schema) và Khóa 1 (đo được). Khóa 3 và 4 nên xong trước nhưng không bắt buộc.
**Thời lượng:** ~150h · **Trần:** 200h. Khoảng 22–26 tuần.
**Chi phí:** đợt 3, ~2–3tr ở cấu hình khuyến nghị.
**Tương ứng:** milestone **M7** — artifact ★ thứ ba, và là artifact nặng nhất.

**Xong khóa này bạn có:** artifact duy nhất trong toàn lộ trình mà kỹ năng dữ liệu gặp phần cứng thật, **với số đo đồng bộ thật**. Đây là chỗ hệ phân tán gặp vật lý, và là chỗ backend engineer 8 năm biến thành robotics data engineer.

---

## NGUYÊN TẮC SCOPE — ĐỌC TRƯỚC, ĐỌC LẠI GIỮA KHÓA

> **Số đo là deliverable. Platform là vỏ.**

Rủi ro lớn nhất của khóa này không phải là khó. Nó là: phần mềm — thế mạnh của bạn — xong nhanh và đẹp, còn phần khác biệt thật (số đo sync) thì mỏng. Bạn sẽ có một data platform bóng bẩy mà không ai quan tâm, vì ai cũng dựng được data platform.

**Đảo lại thứ tự làm: đo trước, dựng platform sau.** Module 2 (đồng bộ thời gian) đứng trước Module 3 (data stack) trong tài liệu này không phải ngẫu nhiên.

Nếu chạm trần 200h, cắt Module 3 xuống MVP và giữ nguyên Module 2. Không được làm ngược lại.

---

# MODULE 0 — CHỌN PHẦN CỨNG (8h)

---

## Bài 1 — Kiểm tra ràng buộc phần cứng trước khi mua gì (3h)

**Câu hỏi:** máy tôi đang có làm được những gì?

### Khái niệm

Khóa này cần bốn năng lực phần cứng, và chúng nằm ở các thiết bị khác nhau:

| Năng lực | Ai có |
|---|---|
| **GPIO + I2C/SPI + timer phần cứng** | MCU (ESP32-S3) hoặc SBC (Pi) |
| **PTP hardware timestamping** | NIC hỗ trợ IEEE 1588 — một số PC, Pi 5, **không phải** Pi 4 hay Pi 3B |
| **Chạy Linux, lưu trữ, database** | Bất kỳ PC/laptop nào |
| **Camera có thể điều khiển** | Webcam USB thường |

Điểm quan trọng: **PTP hardware timestamping là năng lực duy nhất bạn không thể thay thế bằng phần mềm.** Mọi thứ khác đều có đường vòng.

### Làm

**Bước 1 — kiểm tra NIC của máy bạn đang có. Tốn 0đ.**

```bash
ip link                    # tìm tên interface
ethtool -T <tên>           # ví dụ: ethtool -T enp3s0
ls /dev/ptp*               # có PTP clock device không
```

Đọc kết quả:

| Thấy gì | Nghĩa là |
|---|---|
| `PTP Hardware Clock: 0` + `hardware-transmit` + `hardware-receive` | ✅ Máy này làm được PTP thật. **Không cần mua Pi 5.** |
| `PTP Hardware Clock: none`, chỉ có `software-*` | ❌ Chỉ làm được software timestamping — độ chính xác gần NTP, không đủ cho thí nghiệm chính |

Làm trên **mọi** máy bạn có: laptop, PC, máy cũ trong tủ. Ghi kết quả vào `decisions.md`.

**Bước 2 — nếu không máy nào có, ba lựa chọn:**

| Lựa chọn | Giá | Ghi chú |
|---|---|---|
| Card mạng Intel PCIe cũ (i210, i350, I219) | 200–600k | Rẻ nhất nếu bạn có PC có khe PCIe. Kiểm tra model cụ thể trước khi mua |
| Raspberry Pi 5 | ~2.5tr + phụ kiện | Chắc chắn có PTP hardware clock |
| Bỏ PTP, chỉ làm hardware trigger | 0đ | **FAIL action đã cho phép.** Xem Bài 9 |

**Bước 3 — chọn tầng phần cứng.**

### Ba tầng phần cứng

| Tầng | Gồm | Giá thêm | Làm được PASS nào |
|---|---|---|---|
| **T0 — tối thiểu** | Laptop + ESP32-S3 ×2 + 3 cảm biến + 2 webcam USB | ~900k–1.2tr | 1, 3, 4, 5. PASS 2 chỉ ở dạng hardware-trigger |
| **T1 — khuyến nghị** | T0 + card mạng PTP (hoặc máy sẵn có đã hỗ trợ) | +0–600k | **Cả 5** |
| **T2 — đầy đủ** | T1 + Pi 5 | +3tr | Cả 5, cộng một target Linux ARM thật |

**Danh sách mua tầng T0/T1:**

| Món | Spec | Giá ~ |
|---|---|---|
| ESP32-S3 DevKit | **×2** — S3 chứ không phải ESP32 thường (có I2S, PSRAM) | 200k/cái |
| IMU | ICM-42688 tốt hơn, MPU6050 rẻ và nhiều tài liệu. **Mua 2** | 85–250k/cái |
| ToF | VL53L1X | ~150k |
| Nhiệt/ẩm/áp | BME280 | ~80k |
| Webcam USB | **×2, khác model** — khác model là có chủ đích, xem Bài 11 | 200–400k/cái |
| LED + điện trở | Đã có trong kit Khóa 1 | — |
| Cáp Ethernet Cat6 ×2 | Dùng LAN, không WiFi khi đo | 30–50k |
| Switch gigabit rẻ | Nếu cần nối 3 máy | 150–300k |
| (T1) Card mạng Intel PTP | Kiểm model trước khi mua | 200–600k |

**Không mua:** Jetson (Khóa 4 đã chứng minh có cần hay không), lidar, máy in 3D, GPU.

### Số phải ra

Sau bài này, `decisions.md` phải có:
- Bảng `ethtool -T` của mọi máy bạn có
- Tầng phần cứng đã chọn + lý do
- Nếu chọn T0: ghi rõ PASS 2 sẽ đạt bằng hardware trigger thay vì PTP, và tại sao điều đó vẫn hợp lệ

---

## Bài 2 — Kế hoạch đo trước, platform sau (5h)

**Câu hỏi:** deliverable thật của khóa này là gì?

### Khái niệm

Viết ra bây giờ, trước khi code dòng nào, để 22 tuần nữa bạn còn nhớ.

**Deliverable là bốn phân bố sai số thời gian**, mỗi cái kèm phương pháp đo và sai số của chính phép đo:

| Thí nghiệm | Đo cái gì | Độ lớn kỳ vọng |
|---|---|---|
| TN-1 | Lệch timestamp giữa 2 thiết bị khi cùng thấy một sự kiện GPIO | ms tới hàng chục ms |
| TN-2 | Offset clock trước/sau khi bật PTP | trước: ms · sau: µs hoặc nhỏ hơn |
| TN-3 | Drift của clock ESP32 theo nhiệt độ | ppm |
| TN-4 | Lệch giữa 2 camera + IMU, có và không có hardware trigger | ms tới hàng chục ms → xuống dưới ms |

Platform (Module 3) là thứ chứa các số đó và chứng minh bạn vận hành được ở quy mô. Nó **không** phải điểm khác biệt.

### Làm

1. Viết `GOALS.md` với bảng trên, và một câu ở đầu: *"Nếu chỉ làm được một thứ trong khóa này, đó là Module 2."*
2. Viết `prediction.md` cho cả bốn thí nghiệm. Dự đoán bằng số, có cách tính. Commit.
3. Đặt một ràng buộc giờ tự áp: **Module 3 không được vượt 55h.** Nếu vượt, cắt tính năng chứ không cắt Module 2.

---

# MODULE 1 — CẢM BIẾN VÀ RAW REGISTER (32h)

---

## Bài 3 — Quét bus và bắt tay với chip (5h)

**Câu hỏi:** làm sao biết chip còn sống trước khi đổ lỗi cho code?

### Khái niệm

Mọi chip I2C/SPI tử tế đều có một thanh ghi nhận dạng — `WHO_AM_I`, `CHIP_ID`, `MODEL_ID`. Đọc được đúng giá trị nghĩa là: dây đúng, nguồn đúng, địa chỉ đúng, bus hoạt động. Đây là bước "test thông mạch" của thế giới số, và bỏ qua nó là lý do người ta debug ba ngày một lỗi đấu dây.

**Bảng nhận dạng — dán cạnh bàn:**

| Chip | Địa chỉ I2C | Thanh ghi | Giá trị đúng |
|---|---|---|---|
| MPU6050 | 0x68 (AD0→GND) hoặc 0x69 | `WHO_AM_I` 0x75 | **0x68** |
| ICM-42688 | 0x68 hoặc 0x69 | `WHO_AM_I` 0x75 | **0x47** |
| BME280 | 0x76 (SDO→GND) hoặc 0x77 | `id` 0xD0 | **0x60** |
| VL53L1X | 0x29 | Model ID 0x010F–0x0110 | **0xEACC** |

BMP280 (không có ẩm) trả về 0x58 — nếu bạn mua nhầm, đây là cách phát hiện.

### Làm

1. Đấu từng cảm biến lên ESP32-S3, mỗi lần một cái. 3.3V, **không phải 5V**.
2. Chạy I2C scanner. Ghi địa chỉ tìm được.
3. Đọc thanh ghi nhận dạng. So với bảng.
4. **Cắm logic analyzer và xem giao dịch đó.** Bạn đã làm điều này ở Khóa 1 Bài 12 — làm lại, vì giờ bạn hiểu nhiều hơn. Nhìn thấy: START, địa chỉ, ACK, thanh ghi, repeated START, đọc, NACK, STOP.
5. Đấu **cả ba** cảm biến lên cùng một bus. Scan lại. Cả ba phải xuất hiện.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Scanner tìm thấy | Đúng địa chỉ trong bảng |
| WHO_AM_I | Đúng giá trị trong bảng |
| Ba cảm biến chung bus | Cả ba đều xuất hiện, không cái nào biến mất |
| Trên logic analyzer | ACK sau mỗi byte, không có NACK ngoài byte cuối |

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Scanner không thấy gì | Thiếu pull-up, hoặc SDA/SCL đảo, hoặc chưa cấp nguồn | Đo áp SDA và SCL lúc idle — cả hai phải ≈3.3V. Nếu 0V thì thiếu pull-up |
| Thấy địa chỉ nhưng WHO_AM_I sai | Mua nhầm chip, hoặc module nhái | So với bảng. Module nhái MPU6050 khá phổ biến |
| Thêm cảm biến thứ ba thì cái khác biến mất | Pull-up tổng quá mạnh (nhiều module mỗi cái có pull-up riêng) | Tháo pull-up trên bớt module, hoặc giảm tốc độ bus |
| Hoạt động lúc được lúc không | Dây dài, nhiễu, tiếp xúc kém | Rút ngắn dây, hàn thay vì cắm |

---

## Bài 4 — Raw register → đơn vị vật lý, tự tay (8h)

**Câu hỏi:** con số 16384 nghĩa là gì?

### Khái niệm

Lộ trình ghi rõ: **đọc raw register, không dùng thư viện wrapper.** Lý do giống hệt Khóa 2 (đọc parquet trực tiếp thay vì dùng `LeRobotDataset`): wrapper che giấu đúng thứ bạn đang đi tìm.

Cụ thể ở đây, wrapper che ba thứ bạn phải hiểu:
1. **Scale factor** phụ thuộc cấu hình dải đo — và nếu bạn đổi dải mà quên đổi scale, mọi số sai đúng một hệ số.
2. **Thứ tự byte và kiểu dữ liệu** — raw là `int16` bù hai, tách thành hai thanh ghi HIGH/LOW. Đọc nhầm dấu → giá trị nhảy từ +32767 sang -32768.
3. **Đơn vị** — chip trả về số không thứ nguyên. Đơn vị là do *bạn* gán. Trường `unit` trong schema tồn tại vì lý do này.

**Ví dụ MPU6050 (tra lại datasheet của chip bạn mua):**

| Dải đo | Scale factor |
|---|---|
| Accel ±2g | 16384 LSB/g |
| Accel ±4g | 8192 LSB/g |
| Gyro ±250 °/s | 131 LSB/(°/s) |
| Gyro ±500 °/s | 65.5 LSB/(°/s) |

Suy ra: đặt nằm yên trên bàn, trục Z phải đọc ra ≈16384 ở dải ±2g. Đó là **g**, tức gia tốc trọng trường — một hằng số vật lý bạn có thể tra.

**Và đây là chi tiết đắt giá:** g không phải 9.81 ở mọi nơi. Giá trị chuẩn quốc tế là 9.80665 m/s². Ở Hà Nội (vĩ độ ~21°N), g thực tế khoảng **9.787 m/s²**. Chênh lệch ~0.2% — nhỏ, nhưng nó là một phép kiểm tra chéo thật, và nó sẽ trở thành rule validation theo vật lý ở Bài 16.

### Làm

1. Đọc **trọn** datasheet IMU — không skim. Viết tay register map như đã làm ở Khóa 1 Bài 11.
2. Viết driver tối thiểu: đọc 6 thanh ghi accel + 6 gyro, ghép thành `int16`, nhân scale factor.
3. **Dự đoán trước, commit:** đặt nằm yên, mỗi trục đọc ra bao nhiêu? Rồi đo.
4. Lật cảm biến qua 6 hướng (mỗi trục hướng lên và hướng xuống). Với mỗi hướng, dự đoán rồi đo.
5. Tính `|a| = √(ax² + ay² + az²)` cho cả 6 hướng.
6. Đổi dải đo sang ±4g. **Dự đoán số raw sẽ đổi thế nào.** Đo lại.
7. Để yên 10 phút, ghi gyro. Tính **bias** (trung bình) và **nhiễu** (độ lệch chuẩn).
8. Tích phân gyro theo thời gian để thấy **drift** — góc trôi đi dù cảm biến không quay.

### Số phải ra

| Kiểm tra | Giá trị đúng |
|---|---|
| Accel Z nằm yên, dải ±2g | ≈ +16384 raw · ≈ **9.79 m/s²** ở Hà Nội |
| \|a\| ở **cả 6** hướng | Đều ≈ 9.79 m/s², lệch <2% giữa các hướng |
| Đổi sang ±4g | Raw giảm **một nửa**, giá trị vật lý **không đổi** |
| Gyro nằm yên, trung bình | Không phải 0 — có bias, thường vài °/s hoặc nhỏ hơn |
| Gyro nằm yên, độ lệch chuẩn | Có nhiễu. **Nếu σ = 0 chính xác, nghi ngờ kênh đơ** |
| Tích phân gyro 60 giây | Góc trôi đi rõ rệt dù không quay |

Ba điểm đáng dừng lại:

**\|a\| bằng nhau ở 6 hướng** là phép kiểm tra chéo mạnh nhất bạn có với IMU. Nếu nó lệch nhiều, cảm biến cần hiệu chuẩn (scale và offset từng trục khác nhau) — và đó chính là **intrinsic calibration**, khái niệm bạn đã đọc ở tài liệu nền, giờ gặp thật.

**Raw đổi mà giá trị vật lý không đổi** chứng minh bạn đã tách đúng tầng: raw thuộc về chip, giá trị vật lý thuộc về thế giới.

**Tích phân gyro trôi** là lý do tồn tại của sensor fusion. Bạn vừa tự tay chứng minh vì sao IMU đơn thuần không định vị được.

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Giá trị nhảy giữa +32767 và -32768 | Xử lý sai bù hai | Ép kiểu `int16` đúng cách, không dùng `uint16` |
| Trục Z đọc ≈ -16384 | Cảm biến úp ngược | Không phải lỗi. Ghi lại hướng lắp — đây là **extrinsic**, phần đầu tiên của bài toán frame |
| \|a\| lệch >5% giữa các hướng | Cần calibration | Ghi lại độ lệch. Đây là dữ liệu, không phải lỗi |
| Gyro bias rất lớn | Bình thường với chip rẻ | Ghi bias, trừ đi khi dùng. **Và ghi rằng bạn đã trừ** — provenance |
| Không có nhiễu chút nào | Đang đọc cache, hoặc kênh đơ | Kiểm tra xem có thực sự đọc mới không |

---

## Bài 5 — Cảm biến thứ hai và thứ ba (7h)

**Câu hỏi:** ba cảm biến khác nhau khác nhau ở chỗ nào, về mặt dữ liệu?

### Khái niệm

Ba cảm biến được chọn vì chúng đại diện ba **hình thái dữ liệu** khác nhau — đó là lý do dùng ba chứ không phải ba cái IMU:

| Cảm biến | Tần số | Hình thái | Vấn đề dữ liệu đặc trưng |
|---|---|---|---|
| **IMU** | 100–1000 Hz | Luồng liên tục, nhanh | Bias, drift, cần timestamp chính xác |
| **ToF (VL53L1X)** | 10–50 Hz | Đo theo yêu cầu, có thời gian tích lũy | Có trạng thái "không hợp lệ", có nhiễu phụ thuộc bề mặt |
| **BME280** | <1 Hz | Chậm, cần bù trừ phức tạp | **Hệ số hiệu chuẩn nằm trong chính chip** |

BME280 đáng chú ý: nó không trả về nhiệt độ, nó trả về một số raw cần đưa qua một công thức bù trừ dùng các hệ số hiệu chuẩn đọc từ chính chip (mỗi con chip một bộ khác nhau, nạp lúc sản xuất). Đây là ví dụ sạch nhất về **calibration data là dữ liệu hạng nhất** — nếu bạn không lưu `calibration_id` cùng phép đo, người khác không tái tạo được giá trị vật lý từ raw.

### Làm

1. VL53L1X: đọc khoảng cách. Đo thật bằng thước ở 5 khoảng cách (10, 30, 50, 100, 200 cm). Vẽ đo vs thật.
2. Thử trên 3 bề mặt khác nhau (giấy trắng, vải đen, kính). Ghi hiện tượng.
3. BME280: đọc hệ số hiệu chuẩn từ chip, in ra, lưu lại. Tự implement công thức bù trừ từ datasheet.
4. So nhiệt độ BME280 với nhiệt độ đọc từ IMU (hầu hết IMU có cảm biến nhiệt nội). Chúng sẽ **khác nhau** — giải thích tại sao.
5. Với cả ba, đo tần số cập nhật thật bằng cách đếm số mẫu mới trong 60 giây.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| VL53L1X vs thước | Sai lệch vài phần trăm ở khoảng cách trung bình; tệ hơn ở rất gần và rất xa |
| Bề mặt đen / kính | Sai số tăng rõ, hoặc trả về trạng thái không hợp lệ. **Đây là bài học: cảm biến có điều kiện hoạt động** |
| BME280 nhiệt độ | Gần nhiệt độ phòng, ±1°C |
| Nhiệt độ IMU vs BME280 | IMU **cao hơn** vài độ — nó đo nhiệt của chính die silicon đang phát nhiệt, không phải không khí |
| Tần số thật vs cấu hình | Có thể lệch. Ghi lại số thật, đừng tin config |

Điểm "nhiệt độ IMU cao hơn" là một ví dụ nhỏ nhưng rất đắt: hai cảm biến đo "cùng một đại lượng" ra hai số khác nhau, và **cả hai đều đúng** — chúng đo hai thứ khác nhau. Đây chính xác là loại nhầm lẫn phá hỏng sensor fusion, và bạn vừa gặp nó ở dạng vô hại.

---

## Bài 6 — ESP32-S3 làm node cảm biến: UART vs mạng (12h)

**Câu hỏi:** đưa dữ liệu từ MCU về máy chủ bằng đường nào?

### Khái niệm

Đây là bài đầu tiên bạn ở trên sân nhà — nhưng với một biến số mới: **cái gì đóng dấu thời gian, và ở đâu.**

Ba lựa chọn timestamp, hậu quả rất khác nhau:

| Đóng dấu ở đâu | Độ chính xác | Vấn đề |
|---|---|---|
| MCU, bằng timer phần cứng, tại lúc lấy mẫu | Tốt nhất | Clock MCU trôi so với clock máy chủ |
| Máy chủ, lúc nhận gói | Tệ | Bao gồm cả latency truyền + jitter |
| Máy chủ, ước lượng ngược từ số thứ tự mẫu | Trung bình | Cần biết tần số thật rất chính xác |

**Cách đúng: đóng dấu ở MCU, và đo riêng độ lệch giữa hai clock.** Đó chính là Module 2.

### Làm

1. Firmware ESP32-S3: đọc 3 cảm biến ở 3 tần số khác nhau, mỗi mẫu kèm timestamp từ timer phần cứng (µs từ lúc boot) và một **số thứ tự tăng dần**.
2. Số thứ tự là thứ cho phép bạn phát hiện mất gói mà không cần dựa vào timestamp. Đừng bỏ qua nó.
3. Gửi về máy chủ qua **hai đường**: UART (baud cao) và WiFi (UDP hoặc TCP).
4. Đo cho mỗi đường, trong 1 giờ:
   - **Latency**: từ timestamp MCU tới lúc máy chủ nhận
   - **Jitter**: phân bố của latency, không phải trung bình
   - **Packet loss**: dựa trên số thứ tự bị thiếu
   - **Reorder**: gói đến sai thứ tự (UDP)
5. Vẽ phân bố latency của hai đường chồng lên nhau, thang log.
6. **Ép nó hỏng:** bật tải WiFi nặng (tải file lớn), đo lại. Che ăng-ten. Kéo dài dây UART.

### Số phải ra

| Đường | Latency p50 | Jitter | Packet loss |
|---|---|---|---|
| UART 921600 baud | Sub-ms tới vài ms, rất ổn định | Nhỏ | ≈0 nếu không tràn buffer |
| WiFi UDP, mạng nhàn | Vài ms | **Đuôi dài** — p99 có thể gấp nhiều lần p50 | Nhỏ nhưng khác 0 |
| WiFi UDP, mạng tải nặng | Tăng | Đuôi rất dài | Tăng rõ |
| WiFi TCP | Cao hơn UDP | Có spike do retransmit | ≈0, nhưng đổi bằng latency |

Hình dạng quan trọng hơn con số: **UART cho phân bố hẹp, WiFi cho phân bố có đuôi.** Đó là toàn bộ lý do robot dùng bus có dây cho vòng điều khiển và mạng cho dữ liệu.

Bạn đã biết điều này ở tầng API. Điểm mới: ở đây đuôi phân bố không làm chậm một request — nó làm **sai một phép đo vật lý**, vì timestamp bị nhiễm latency.

### Nếu ra khác

| Triệu chứng | Nguyên nhân |
|---|---|
| UART mất gói đều đặn | Tràn buffer UART ở một trong hai đầu. Tăng buffer hoặc giảm tần số |
| WiFi p99 rất tệ | Bình thường. **Ghi lại, đây là kết quả** |
| Latency âm | Clock MCU và clock máy chủ chưa được so — đúng, và đó là Module 2 |

Triệu chứng cuối là cầu nối tự nhiên sang module tiếp theo. Nếu bạn gặp nó, tốt: bạn vừa tự phát hiện ra bài toán mà Module 2 tồn tại để giải.

---

# MODULE 2 — ĐỒNG BỘ THỜI GIAN (50h)

**Đây là module quan trọng nhất của khóa, và của cả lộ trình.** Time sync là một trong những kỹ năng khan hiếm nhất trong physical AI, và nó là kỹ năng hệ thống — không phải cơ điện tử. Đây là nơi 8 năm của bạn có giá trực tiếp.

---

## Bài 7 — Ngân sách sai số thời gian (6h)

**Câu hỏi:** hai phép đo "cùng lúc" lệch nhau bao nhiêu, và vì đâu?

### Khái niệm

Bạn đã làm latency budget ở Khóa 3. Đây là cùng một kỹ năng, đổi đại lượng. Khác biệt: latency budget cộng các **độ trễ**; time sync budget cộng các **sai số**, và sai số cộng theo căn bậc hai nếu độc lập.

**Các nguồn sai số, từ lớn tới nhỏ:**

| Nguồn | Độ lớn điển hình | Giảm được bằng |
|---|---|---|
| Không sync gì cả, hai clock tự do | Trôi vô hạn theo thời gian | Bất kỳ cơ chế sync nào |
| Clock drift do thạch anh | 20–50 ppm → **72–180 ms mỗi giờ** | Sync định kỳ |
| Drift thêm do nhiệt độ | Vài ppm nữa | Bù trừ nhiệt, hoặc sync thường xuyên hơn |
| NTP qua LAN | 1–10 ms | PTP |
| PTP software timestamping | Hàng chục tới hàng trăm µs | PTP hardware timestamping |
| PTP hardware timestamping | Sub-µs | Hardware trigger |
| Latency truyền + jitter (nếu đóng dấu ở đầu nhận) | Bằng chính jitter mạng | Đóng dấu ở nguồn |
| Thời gian phơi sáng camera | Nửa thời gian phơi sáng | Ghi lại exposure, bù trừ |
| Rolling shutter | Toàn bộ thời gian đọc frame, vài chục ms | Global shutter, hoặc bù theo hàng |

**Phép tính bạn phải tự làm được:** thạch anh 20 ppm nghĩa là mỗi giây trôi 20 µs. Một giờ = 3600 s → 72.000 µs = **72 ms**. Đó là lý do không thể "sync một lần lúc khởi động rồi thôi".

### Làm

1. Lập bảng ngân sách cho hệ của bạn: ESP32 ↔ máy chủ ↔ camera. Điền **dự đoán** cho mọi dòng. Commit.
2. Tra datasheet thạch anh của board ESP32-S3 bạn mua. Ppm là bao nhiêu? Tính ra ms/giờ.
3. Tra thông số camera: rolling hay global shutter? Thời gian đọc frame bao nhiêu?
4. Viết ra: **với ứng dụng nào thì sai số này chấp nhận được, với ứng dụng nào thì không?**

### Số phải ra

Không có số đúng — có **bảng dự đoán được commit trước**. Nhưng có một con số bạn phải tính ra và nhớ: ppm → ms/giờ. Nếu bạn không tự tính được, quay lại đọc phần Khái niệm.

---

## Bài 8 — TN-1: GPIO chung, sự kiện duy nhất (10h)

**Câu hỏi:** hai thiết bị cùng nhìn thấy một sự kiện. Timestamp của chúng lệch nhau bao nhiêu?

### Khái niệm

Đây là thí nghiệm nền tảng, và nó đẹp vì đơn giản: một chân GPIO được kéo lên, **cả hai thiết bị cùng thấy**. Không có mạng, không có phần mềm ở giữa. Chênh lệch timestamp giữa chúng là sai số sync thuần túy.

Sự kiện phải là **cạnh dốc** — cạnh lên của một tín hiệu số, không phải một cái gì mờ nhòe.

### Làm

1. Nối một chân GPIO của ESP32-S3 tới một chân GPIO của máy chủ (Pi) hoặc, nếu máy chủ là laptop không có GPIO, tới **ESP32-S3 thứ hai**. Đây là lý do mua 2 con.
2. Một bên phát xung định kỳ (ví dụ 1 Hz). Cả hai bên ghi timestamp của mọi cạnh lên mà chúng thấy.
3. Chạy **≥1 giờ**. Thu thập ≥3600 cặp timestamp.
4. Tính offset của từng cặp. Vẽ:
   - Histogram của offset
   - Offset **theo thời gian** ← quan trọng hơn histogram
5. Fit đường thẳng cho offset theo thời gian. **Độ dốc chính là drift, đơn vị ppm.**
6. Song song: cắm logic analyzer lên chính chân GPIO đó để có một trục thời gian thứ ba, độc lập. Đây là cách bạn đo **sai số của chính phép đo**.

### Số phải ra

| Đại lượng | Giá trị kỳ vọng |
|---|---|
| Offset ban đầu | Tùy ý — hai clock khởi động độc lập |
| Offset **theo thời gian** | Đường thẳng dốc lên hoặc xuống, không phẳng |
| Độ dốc (drift) | Vài chục ppm → hàng chục tới hàng trăm ms trôi sau 1 giờ |
| Nhiễu quanh đường thẳng | Vài µs tới vài chục µs — đây là jitter của interrupt |
| Sai số phép đo (từ logic analyzer) | Độ phân giải sample rate, ví dụ 41.7 ns ở 24 MHz |

**Nếu offset theo thời gian phẳng, có gì đó sai** — hoặc hai clock đã được sync ngầm, hoặc bạn đang đo cùng một clock hai lần.

Con số drift tính ra ở bước 5 phải **khớp với dự đoán từ ppm của thạch anh** ở Bài 7. Đây là kiểm tra chéo ba đường quen thuộc: tính từ datasheet, đo trực tiếp, đo bằng dụng cụ thứ ba.

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Jitter rất lớn (ms) | Đang xử lý cạnh trong userspace Linux có scheduler | Dùng interrupt, hoặc hardware capture. Ghi lại chênh lệch giữa hai cách — đó là bài học về determinism |
| Mất một số cạnh | Interrupt bị nghẽn, hoặc bounce | Kiểm tra debounce, giảm tần số |
| Drift không tuyến tính | Nhiệt độ thay đổi trong lúc đo | **Đây là Bài 10.** Ghi lại nhiệt độ song song |

---

## Bài 9 — TN-2: PTP, trước và sau (12h)

**Câu hỏi:** bật PTP lên thì sai số giảm bao nhiêu, đo bằng số?

Đây là tiêu chí PASS số 2: phân bố offset clock **trước/sau** khi bật PTP, **≥1 giờ dữ liệu**, có nêu phương pháp đo **và sai số của phép đo đó**.

### Khái niệm

PTP (IEEE 1588) đồng bộ clock qua mạng bằng cách trao đổi gói có đóng dấu thời gian. Điểm mấu chốt: **đóng dấu ở đâu quyết định độ chính xác.**

| Kiểu | Đóng dấu ở | Độ chính xác |
|---|---|---|
| Software timestamping | Kernel, khi gói đi qua stack mạng | Hàng chục–hàng trăm µs |
| Hardware timestamping | NIC, tại lúc bit đi qua dây | Sub-µs |

Đây là lý do Bài 1 bắt bạn chạy `ethtool -T` trước khi làm gì. Không có PTP hardware clock thì bạn vẫn chạy được PTP, nhưng bạn đang đo một thứ khác.

**Hai tầng clock cần đồng bộ, và người mới hay quên tầng thứ hai:**
1. `ptp4l` đồng bộ **PHC** (physical hardware clock trên NIC) giữa các máy
2. `phc2sys` đồng bộ giữa PHC và **system clock**

Bỏ bước 2 thì `date` trên máy bạn vẫn sai dù PTP đang chạy hoàn hảo.

### Làm

**Bước 1 — đo baseline (trước).** Với NTP thông thường hoặc không sync gì, đo offset giữa hai máy trong ≥1 giờ. Dùng chính phương pháp GPIO của Bài 8 — đó là trọng tài độc lập, không phụ thuộc vào mạng.

**Bước 2 — bật PTP.**
```bash
# máy chủ (grandmaster)
sudo ptp4l -i <iface> --masterOnly 1 -m
# máy con
sudo ptp4l -i <iface> --slaveOnly 1 -m
# rồi đồng bộ PHC ↔ system clock trên cả hai
sudo phc2sys -a -r
```
Ghi lại toàn bộ log của `ptp4l` — nó tự báo offset ước lượng, nhưng **đừng chỉ tin con số đó**.

**Bước 3 — đo lại bằng GPIO.** Đây là điểm quan trọng nhất của bài: `ptp4l` tự báo cáo offset của chính nó, và đó là **tự chấm điểm**. Phép đo GPIO là độc lập. Nếu hai con số khác nhau nhiều, con số độc lập đúng hơn.

**Bước 4 — ≥1 giờ dữ liệu.** Vẽ:
- Offset theo thời gian, trước và sau, **chồng lên nhau trên cùng trục log**
- Histogram của cả hai
- Con số so sánh: p50, p95, p99 của |offset|

**Bước 5 — ép nó hỏng.** Tạo tải mạng nặng. Rút dây rồi cắm lại. Xem PTP mất bao lâu để hội tụ lại. Ghi lại.

**Bước 6 — nêu sai số của phép đo.** Bạn đang đo lệch cỡ µs bằng dụng cụ có độ phân giải bao nhiêu? Logic analyzer 24 MHz cho 41.7 ns — đủ. Nhưng jitter interrupt ở phía phần mềm có thể lớn hơn nhiều, và **đó mới là giới hạn thật**. Đo nó và ghi ra.

### Số phải ra

| Cấu hình | \|offset\| kỳ vọng |
|---|---|
| Không sync, sau 1 giờ | Hàng chục–hàng trăm ms (drift tích lũy) |
| NTP qua LAN | 1–10 ms |
| PTP software timestamping | Hàng chục–hàng trăm µs |
| PTP hardware timestamping, mạng nhàn | Sub-µs tới vài µs |
| PTP hardware timestamping, mạng tải nặng | Xấu đi, nhưng vẫn tốt hơn NTP nhiều |

**Nếu PTP của bạn chỉ ngang NTP**, gần như chắc chắn đang chạy software timestamping. Kiểm tra lại `ethtool -T` và log `ptp4l`.

### FAIL action — cam kết trước

Lộ trình ghi rõ: **PTP không chạy được sau 60h → chuyển sang hardware-trigger-only sync**, đo lệch bằng GPIO chung. Kết quả vẫn publish được, vẫn trả lời được câu hỏi phỏng vấn. **Không đâm đầu vào `linuxptp`.**

Viết câu này vào `decisions.md` hôm nay.

---

## Bài 10 — TN-3: Clock drift theo nhiệt độ (8h)

**Câu hỏi:** thạch anh trôi bao nhiêu khi nóng lên?

### Khái niệm

Thạch anh có hệ số nhiệt. Robot chạy ngoài trời, trong nhà xưởng, gần motor nóng — nhiệt độ không cố định, nên drift cũng không cố định. Đây là lý do "sync một lần rồi thôi" thất bại, và là một chi tiết mà phần lớn người làm data pipeline không biết.

### Làm

1. Chạy TN-1 (GPIO chung) liên tục **6 tiếng**, đồng thời ghi nhiệt độ (dùng BME280 đặt cạnh ESP32, và nhiệt độ nội của chính ESP32 nếu có).
2. Trong 6 tiếng đó, **thay đổi nhiệt độ có chủ đích**: để bình thường 2h → hơ máy sấy 1h → để nguội 2h → làm lạnh bằng cách đặt gần quạt hoặc đá bọc túi 1h.
3. Tính drift tức thời bằng cách lấy đạo hàm của offset theo thời gian trong cửa sổ trượt.
4. **Vẽ drift (ppm) vs nhiệt độ (°C).** Đây là hình chính của thí nghiệm.
5. Fit một đường (tuyến tính hoặc bậc hai) và ghi hệ số.

### Số phải ra

| Kiểm tra | Kỳ vọng |
|---|---|
| Drift ở nhiệt độ phòng | Vài chục ppm |
| Drift đổi khi hơ nóng | **Phải đổi rõ rệt.** Nếu không đổi, hơ chưa đủ hoặc đo chưa đủ lâu |
| Quan hệ drift–nhiệt độ | Đơn điệu hoặc parabol, tùy loại cắt thạch anh |
| Sau khi nguội về nhiệt độ ban đầu | Drift quay về gần giá trị cũ — **nếu không, có hysteresis, và đó là phát hiện đáng ghi** |

**Cảnh báo an toàn:** máy sấy ở mức thấp, giữ khoảng cách, đừng vượt nhiệt độ tối đa trong datasheet (thường 85°C với linh kiện thương mại). Đây là lúc mục "Absolute Maximum Ratings" bạn học ở Khóa 1 có ích thật.

### Vì sao thí nghiệm này đáng 8 giờ

Rất ít người tự học từng đo cái này. Nó cho bạn một câu trả lời cụ thể cho câu hỏi phỏng vấn *"anh xử lý clock drift thế nào"* — và câu trả lời của bạn sẽ có một đồ thị kèm theo, không phải một định nghĩa từ Wikipedia.

---

## Bài 11 — TN-4: Hardware trigger và rig 2 camera + IMU (14h)

**Câu hỏi:** hai camera "chụp cùng lúc" thực sự lệch nhau bao nhiêu?

Đây là thí nghiệm đắt nhất về mặt bài học, và là chỗ bạn tạo ra **dataset của riêng mình** — trả lời trực tiếp câu hỏi "nguồn dữ liệu thật ở đâu" bạn đã hỏi.

### Khái niệm

Rig: **2 webcam USB khác model + 1 IMU trên ESP32-S3 + 1 LED**, tất cả nối vào một laptop.

Nghe tầm thường, nhưng nó hỏng ở **đúng những chỗ robot thật hỏng**:
- Hai webcam chia băng thông cùng một USB controller → rớt frame thật, không đều
- Rolling shutter → mỗi hàng ảnh có timestamp khác nhau
- Clock ESP32 trôi so với clock laptop (bạn đã đo ở Bài 8 và 10)
- Không có hardware trigger → ba luồng không bao giờ thực sự cùng thời điểm
- IMU 200 Hz, camera 30 fps → bài toán nội suy về cùng mốc

**Hardware trigger của người nghèo:** ESP32 nháy LED nằm trong khung hình của **cả hai** camera, tại một thời điểm nó tự ghi lại. LED xuất hiện trong video là một sự kiện chung, nhìn thấy được.

**Hai mức độ phân giải:**

*Thô — theo frame index.* Tìm frame đầu tiên có LED sáng trong mỗi luồng. Độ phân giải = 1 frame = 33 ms ở 30 fps. Đủ để thấy vấn đề, không đủ để đo tinh.

*Tinh — theo hàng rolling shutter.* Camera rolling shutter đọc từng hàng lần lượt. Nếu LED bật lên **giữa** lúc đọc frame, phần trên của ảnh tối và phần dưới sáng — hoặc ngược lại. Vị trí ranh giới cho bạn thời điểm bật LED **trong lòng một frame**.

```
t_bật_LED = t_đầu_frame + (số_hàng_trước_ranh_giới / tổng_số_hàng) × t_đọc_frame
```

Với 480 hàng và thời gian đọc ~25 ms, mỗi hàng ≈ **52 µs**. Độ phân giải tốt hơn ba bậc so với phương pháp thô — bằng đúng phần cứng bạn đã có.

Cần biết `t_đọc_frame` trước, và đó là một thí nghiệm con: nháy LED cực ngắn (vài trăm µs), đếm số hàng sáng, suy ra thời gian mỗi hàng.

### Làm

**Phần A — đo thời gian đọc frame (rolling shutter readout).**
1. ESP32 nháy LED trong đúng 200 µs, lặp lại mỗi 2 giây.
2. Ghi video, tìm frame có dải sáng. Đếm số hàng sáng.
3. `t_mỗi_hàng = 200µs / số_hàng_sáng`. Nhân với tổng số hàng → `t_đọc_frame`.
4. Làm với **cả hai** camera. Chúng sẽ khác nhau — đó là lý do mua khác model.

**Phần B — đo lệch giữa hai camera.**
1. Cả hai camera nhìn thấy LED. ESP32 nháy LED 5 ms, mỗi 3 giây, và ghi timestamp của chính nó.
2. Ghi đồng thời 10 phút.
3. Với mỗi lần nháy, tính thời điểm bật LED theo từng camera bằng phương pháp hàng.
4. Lệch giữa hai camera = hiệu hai giá trị đó. Vẽ phân bố.

**Phần C — đo lệch camera ↔ IMU.**
1. Gõ nhẹ vào mặt bàn có gắn cả IMU và camera. Cú gõ tạo đỉnh nhọn trên IMU và chuyển động thấy được trên video.
2. Đồng thời nháy LED. Dùng LED làm mốc chung.
3. Tính lệch giữa timestamp đỉnh IMU và timestamp chuyển động trên video.

**Phần D — ép nó hỏng.**
1. Cắm cả hai camera vào cùng một USB hub. Đo lại. Đếm frame drop.
2. Tăng độ phân giải/fps tới khi tràn băng thông. Ghi ngưỡng.
3. Chạy tải CPU nặng. Đo lại.

**Phần E — đóng gói thành dataset.** Ghi toàn bộ ra MCAP (Module 3), publish lên HF Hub với README ghi rõ phương pháp và sai số. Đây là dataset đầu tiên mang tên bạn.

### Số phải ra

| Đại lượng | Giá trị kỳ vọng |
|---|---|
| `t_đọc_frame` webcam USB thường | 10–30 ms |
| Độ phân giải theo hàng | Vài chục µs |
| Lệch giữa hai camera, không trigger | **Hàng chục ms, và biến thiên** |
| Lệch camera ↔ IMU, không trigger | Hàng chục ms |
| Frame drop khi chung USB controller, độ phân giải cao | Rõ rệt, hàng phần trăm |
| Sau khi dùng LED làm mốc chung | Lệch xác định được tới dưới 1 ms |

Con số quan trọng nhất: **lệch giữa hai camera "chụp cùng lúc" là hàng chục ms và nó biến thiên.** Nếu ai đó xây dataset từ rig như thế này mà không đo cái này, mọi phép fusion của họ sai một lượng không biết. Đó là lý do tồn tại của cả module này, và là một đoạn rất mạnh trong bài viết.

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Không thấy dải sáng, chỉ thấy frame sáng hoàn toàn | LED nháy quá dài, hoặc camera global shutter | Giảm thời gian nháy. Nếu là global shutter, ghi lại — bạn mất phương pháp tinh nhưng có một phát hiện |
| Ranh giới mờ chứ không sắc | Thời gian phơi sáng dài | Giảm exposure, tăng sáng môi trường |
| Lệch giữa hai camera rất nhỏ và ổn định | Nghi ngờ — có thể driver đang đóng dấu bằng cùng một clock lúc nhận | Kiểm tra xem timestamp đến từ đâu |
| Không tìm được đỉnh IMU khi gõ bàn | Gõ quá nhẹ, hoặc tần số IMU quá thấp | Tăng ODR của IMU lên 500–1000 Hz |

---

## Bài 12 — Tổng hợp ngân sách sai số (không tính giờ riêng, làm cùng Bài 7–11)

Quay lại bảng ở Bài 7 và **thay mọi dự đoán bằng số đo**. Mọi dòng phải là số đo, không dòng nào là ước tính — đúng như tiêu chí của Khóa 3 Bài 8, áp dụng cho miền thời gian.

Sau đó viết một đoạn trả lời: *"Với hệ này, hai phép đo từ hai cảm biến khác nhau, được gán cùng một timestamp, thực tế cách nhau không quá ___ µs, với độ tin cậy ___, đo bằng phương pháp ___, sai số của phép đo là ___."*

Đó là một câu bạn sẽ nói trong phỏng vấn, và rất ít ứng viên nói được.

---

# MODULE 3 — DATA STACK (50h, trần cứng 55h)

**Nhắc lại ràng buộc tự áp ở Bài 2:** module này không được vượt 55h. Nếu vượt, cắt tính năng. Đây là phần dễ nhất với bạn và cũng là phần ít khác biệt nhất — đừng để nó ăn giờ của Module 2.

---

## Bài 13 — Ingest nhiều luồng khác tần số vào MCAP (14h)

**Câu hỏi:** làm sao ghi ba luồng 200 Hz, 30 fps, 1 Hz vào một file mà vẫn truy vấn được?

### Khái niệm

Bạn dùng lại toàn bộ những gì đã làm ở Khóa 2 — MCAP, Protobuf schema có version, chunk index. Khác biệt: giờ dữ liệu đến từ phần cứng thật, **không đều**, và có thể mất.

**Ba trường bắt buộc trong mọi message, không thương lượng** (nguyên tắc số 5 của lộ trình):

| Trường | Vì sao |
|---|---|
| `timestamp_ns` (int64, nguồn nào ghi rõ) | Đã bàn cả Module 2 |
| `frame_id` | Phép đo này thuộc hệ tọa độ nào |
| `unit` | Chip trả số không thứ nguyên |
| `uncertainty` / `covariance` | Đây là trường phân biệt bạn với backend engineer chuyển ngành |
| `calibration_id` | Không có nó, raw không tái tạo được thành giá trị vật lý |
| `sequence` | Phát hiện mất gói độc lập với timestamp |

Và một trường ít ai nghĩ tới nhưng rất đáng có: **`clock_source`** — timestamp này đến từ clock nào (MCU timer, system clock đã PTP-sync, hay ước lượng). Sau Module 2 bạn biết ba nguồn này có sai số khác nhau vài bậc. Ghi nó vào schema.

### Làm

1. Thiết kế Protobuf schema cho 3 loại message. Version từ đầu.
2. Writer ghi cả 3 luồng vào một MCAP, mỗi luồng một channel.
3. **Đo chi phí ghi:** throughput tối đa, CPU, kích thước file/giờ, với và không có nén.
4. Truy vấn: đọc 10 giây bất kỳ mà không scan cả file (bạn đã làm ở Khóa 2 — xác nhận nó vẫn đúng với file lớn thật).
5. **Kill -9 giữa lúc ghi, 10 lần.** File còn đọc được không? Mất bao nhiêu dữ liệu?
6. Mở trong Foxglove. Chụp màn hình.
7. Đổi schema v1 → v2 (thêm một trường). Test reader cũ vẫn đọc được file mới.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| File mở được trong Foxglove | Không lỗi, 3 luồng hiện đúng tần số |
| Sau `kill -9` | File vẫn đọc được tới điểm gần cuối. MCAP append-only cho phép phục hồi file ghi dở |
| Kích thước/giờ | Tính ra trước, đo sau. IMU 200Hz × ~50 byte ≈ 36 MB/giờ thô |
| Nén | Giảm đáng kể với dữ liệu số; **video thì đã nén rồi, nén thêm vô ích** |
| Reader v1 đọc file v2 | Thành công |

---

## Bài 14 — Upload resumable và object store (10h)

**Câu hỏi:** làm sao đưa 24 GB/ngày lên storage qua một đường mạng hay đứt?

### Khái niệm

Phần này đúng nghề bạn nhất trong cả khóa. Tôi chỉ nêu ba chỗ khác với backend thường ngày:

1. **Robot mất mạng là trạng thái bình thường, không phải sự cố.** Thiết kế cho offline-first: ghi local trước, upload sau, và có hàng đợi bền.
2. **Không được xóa local trước khi xác nhận upload thành công và checksum khớp.** Dữ liệu cảm biến không tái tạo được — khác với log ứng dụng.
3. **Retention có ràng buộc vật lý:** thẻ nhớ có giới hạn số lần ghi. Log rotation và retention không phải tối ưu chi phí, mà là tránh hỏng phần cứng.

### Làm

1. MinIO local (hoặc S3). Upload resumable theo phần.
2. Checksum hai đầu. Chỉ xóa local sau khi khớp.
3. Hàng đợi bền qua restart.
4. **Ép hỏng:** ngắt mạng giữa lúc upload 5 lần. Rút điện 3 lần. Làm đầy đĩa 1 lần.
5. Đo: throughput upload, thời gian phục hồi sau đứt, dung lượng hàng đợi tối đa chịu được.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Ngắt mạng giữa upload | Tiếp tục từ chỗ dở, **không** upload lại từ đầu |
| Rút điện giữa upload | Sau khởi động lại, hàng đợi còn nguyên, không mất file |
| Checksum không khớp | File **không** bị xóa local, có alert |
| Đĩa đầy | Ghi dừng có kiểm soát, có alert, **không** crash |

---

## Bài 15 — Index và truy vấn (10h)

**Câu hỏi:** trả lời "cho tôi mọi lúc gia tốc vượt 2g trong tuần qua" mất bao lâu?

### Làm

1. ClickHouse hoặc TimescaleDB. Bạn đã có kinh nghiệm time-series ở quy mô — dùng lại.
2. Index metadata + downsample, **không** nhét raw vào DB. Raw sống trong MCAP trên object store; DB chỉ trỏ tới.
3. Thiết kế để trả lời được 5 câu hỏi cụ thể, viết ra trước:
   - Mọi lúc |a| vượt ngưỡng trong khoảng thời gian X
   - Khoảng thời gian nào có cảm biến Y thiếu dữ liệu
   - Phân bố dt của luồng Z theo ngày
   - Dữ liệu nào được ghi với calibration_id cũ
   - Session nào có sync error vượt ngưỡng
4. Đo latency truy vấn với 7 ngày dữ liệu.

### Số phải ra

Câu truy vấn điển hình trên 7 ngày dữ liệu phải trả về trong **dưới 2 giây**. Nếu chậm hơn, xem lại schema index — và đây là bài toán bạn đã giải nhiều lần.

Câu hỏi thứ 5 trong danh sách là câu đáng chú ý: nó nối Module 2 vào platform. Sai số sync là **một trường dữ liệu**, không phải một ghi chú trong README.

---

## Bài 16 — Validation theo vật lý, không chỉ theo schema (10h)

**Câu hỏi:** dữ liệu hợp lệ về schema nhưng sai về vật lý thì bắt bằng gì?

Đây là tiêu chí PASS số 3, và là phần thông minh nhất của module này.

### Khái niệm

Schema validation bắt được: thiếu trường, sai kiểu, sai đơn vị đo. Nó **không** bắt được: cảm biến đơ, cảm biến lệch, cảm biến đọc ra thứ không thể tồn tại.

Validation theo vật lý dùng **quy luật của thế giới** làm ràng buộc. Đây là kiểu kiểm tra mà chỉ người hiểu cả dữ liệu lẫn vật lý mới viết được — và đó chính là định vị nghề nghiệp của bạn.

**Bộ rule khởi đầu:**

| Rule | Cơ sở vật lý | Ngưỡng |
|---|---|---|
| \|a\| lúc đứng yên = g địa phương | Trọng trường | 9.787 m/s² ở Hà Nội, ±ngưỡng bạn đo được ở Bài 4 |
| Nhiệt độ không đổi >X°C trong 100 ms | Quán tính nhiệt | Nhiệt độ không khí đổi chậm |
| ToF không đọc giá trị âm | Khoảng cách không âm | Bất kỳ giá trị âm nào |
| Áp suất khí quyển trong dải hợp lý | Vật lý khí quyển | ~870–1085 hPa ở mặt đất |
| Gyro có phương sai > 0 | Mọi cảm biến thật đều có nhiễu | σ = 0 trong >1 s = kênh đơ |
| dt giữa hai mẫu ≈ 1/ODR | Cấu hình phần cứng | Lệch >10% là frame drop |
| Timestamp đơn điệu tăng | Thời gian một chiều | Bất kỳ vi phạm nào |
| Gia tốc và gyro cùng phát hiện một cú va | Tương quan vật lý | Va chạm phải thấy trên cả hai |

Rule cuối cùng là loại tinh vi nhất: **kiểm tra chéo giữa hai cảm biến độc lập.** Nếu IMU báo cú gõ mạnh mà camera không thấy gì rung, một trong hai sai.

### Làm

1. Implement ≥5 rule, mỗi rule kèm test case tổng hợp (bạn đã làm đúng kiểu này ở Khóa 2 — dùng lại phương pháp).
2. Chạy trên toàn bộ dữ liệu đã thu.
3. **Cố tình gây lỗi thật** và chứng minh rule bắt được:
   - Rút dây một cảm biến giữa lúc ghi → kênh đơ
   - Hơ nóng cảm biến đột ngột → vi phạm rule quán tính nhiệt
   - Chỉnh sai scale factor → |a| lúc đứng yên khác g
   - Làm nghẽn USB → frame drop
4. Với mỗi rule, ghi: tỉ lệ báo động giả trên dữ liệu lành.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Rule bắt được lỗi cố tình gây | **≥1 rule bắt được lỗi thật** ← tiêu chí PASS |
| Tỉ lệ báo động giả trên dữ liệu lành | Phải đo và ghi. Rule báo động liên tục là rule vô dụng |
| Rule \|a\| = g | Phát hiện được sai scale factor ngay lập tức |

**Điểm đáng viết vào bài:** rule "|a| phải bằng g địa phương" bắt được một lớp lỗi mà **không phép kiểm tra schema nào bắt được** — sai scale factor tạo ra dữ liệu hoàn toàn hợp lệ về cấu trúc và hoàn toàn sai về giá trị. Nếu dataset đó được dùng để train, model học sai và không ai biết vì sao.

---

## Bài 17 — Backpressure và drop policy (6h)

**Câu hỏi:** khi ghi không kịp, bỏ cái gì?

### Khái niệm

Bạn biết backpressure. Điểm mới: trong robot, drop một message **không phải là chậm — là mất vĩnh viễn một phép đo vật lý.** Không có retry vì thời điểm đó đã qua.

Nên quy tắc là: **được phép drop, nhưng phải ghi lại việc đã drop.** Một dataset có lỗ hổng và biết mình có lỗ hổng thì dùng được. Một dataset có lỗ hổng mà im lặng thì độc hại.

### Làm

1. Chính sách drop rõ ràng theo mức ưu tiên (ví dụ: giữ IMU, drop video trước).
2. Mỗi lần drop ghi một bản ghi: lúc nào, luồng nào, bao nhiêu message, vì sao.
3. Bản ghi drop được ghi vào **chính file MCAP**, không phải file log riêng — để nó đi cùng dữ liệu mãi mãi.
4. Ép tràn: tăng tần số cảm biến tới khi hệ không kịp. Đo ngưỡng.
5. Kiểm tra: tool audit của Khóa 2 chạy trên file này có phát hiện được lỗ hổng không? **Nếu có, tuyệt vời — bạn vừa khép vòng tròn.**

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Ngưỡng tràn | Một con số cụ thể (msg/s hoặc MB/s) |
| Mọi lần drop có bản ghi | 100%, không sót |
| Tool Khóa 2 chạy trên file này | Phát hiện đúng những lỗ hổng đã được ghi nhận |

Bước cuối là một trong những chi tiết mạnh nhất trong toàn bộ portfolio của bạn: **công cụ audit bạn viết ở Khóa 2 tìm ra lỗi trong dữ liệu do chính hệ thống bạn xây ở Khóa 5 tạo ra, và kết quả khớp với bản ghi drop.** Đó là một vòng khép kín chứng minh cả hai thứ đều hoạt động.

---

# MODULE 4 — VẬN HÀNH (10h người, 7 ngày treo máy)

---

## Bài 18 — Soak 7 ngày (6h)

Tiêu chí PASS số 4: chạy 7 ngày không can thiệp, completeness ≥99%, alert freshness **đã thực sự bắn** ≥1 lần khi cố tình ngắt một nguồn.

### Làm

1. Chạy toàn hệ 7 ngày liên tục.
2. Định nghĩa **completeness** chính xác trước khi đo: `số_message_nhận / số_message_kỳ_vọng`, trong đó kỳ vọng tính từ ODR × thời gian. Viết định nghĩa vào README.
3. Alert freshness: nếu một luồng không có dữ liệu mới trong N giây → bắn cảnh báo.
4. **Ngày thứ 4, cố tình rút một cảm biến.** Alert phải bắn. Ghi lại thời gian từ lúc rút tới lúc alert bắn.
5. Theo dõi suốt 7 ngày: nhiệt độ, dung lượng đĩa, RAM, offset PTP, tỉ lệ drop.
6. Vẽ dashboard. Trả lời được: *"3h sáng thứ Ba nó làm gì?"*

### Số phải ra

| Đại lượng | Ngưỡng |
|---|---|
| Completeness | **≥99%** ← tiêu chí PASS |
| Alert bắn khi ngắt nguồn | **≥1 lần thật** ← tiêu chí PASS |
| Thời gian phát hiện | Ghi lại. Dưới 1 phút là tốt |
| Số lần can thiệp tay | **0** |
| Offset PTP suốt 7 ngày | Vẽ ra. Có tăng theo nhiệt độ ngày/đêm không? ← nối với Bài 10 |

Câu hỏi cuối rất đáng theo dõi: nếu bạn thấy offset PTP dao động theo chu kỳ 24 giờ, bạn vừa quan sát được hệ số nhiệt của thạch anh **trong điều kiện thật**, không phải bằng máy sấy. Đó là một đồ thị rất đẹp cho bài viết.

---

## Bài 19 — Bisect qua bốn tầng (4h)

Tiêu chí PASS số 5: bisect được lỗi qua 4 tầng (pipeline → firmware → bus → sensor), có ghi lại ≥1 lần bisect thật.

### Khái niệm

Đây là tiêu chí ít người để ý nhưng nó chính là **thứ nhà tuyển dụng thực sự mua**. Ý nghĩa của nó: khi một con số sai xuất hiện ở dashboard, bạn xác định được lỗi nằm ở tầng nào, bằng phương pháp, không bằng đoán.

**Bốn tầng và cách kiểm tra từng tầng:**

| Tầng | Câu hỏi | Công cụ |
|---|---|---|
| **Pipeline** | Dữ liệu vào đúng, ra sai? | So input/output của từng bước xử lý |
| **Firmware** | MCU đọc đúng, gửi sai? | In giá trị ngay tại MCU qua serial |
| **Bus** | Chip trả đúng, MCU đọc sai? | **Logic analyzer** — đọc thẳng byte trên dây |
| **Sensor** | Chip trả sai? | Đổi sang module thứ hai (lý do mua 2) |

Tầng "bus" là tầng duy nhất chỉ có thể kiểm tra bằng dụng cụ đo. Đó là lý do Khóa 1 tồn tại, và đây là lúc nó trả nợ.

### Làm

1. **Nhờ ai đó (hoặc script) gây một lỗi mà bạn không biết là gì**, ở một trong bốn tầng. Ví dụ lỗi có thể gây: đổi scale factor trong pipeline, đảo byte order trong firmware, nới lỏng một dây SDA, thay bằng module hỏng.
2. Bisect. **Ghi lại từng bước, kèm thời gian.**
3. Lặp lại 3 lần với 3 lỗi ở 3 tầng khác nhau.
4. Viết `RUNBOOK.md`: cây quyết định để người khác bisect được.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Tìm đúng tầng | 3/3 |
| Thời gian mỗi lần | Ghi lại. Lần sau nhanh hơn lần trước |
| Runbook | Người khác đọc và làm theo được |

---

# GATE KHÓA 5

Đối chiếu 5 tiêu chí PASS của M7:

```
[ ] 1. 2 thiết bị, 3 sensor, ghi MCAP với Protobuf schema có version

[ ] 2. Sync đo được: phân bố offset clock TRƯỚC/SAU khi bật PTP,
       ≥1 giờ dữ liệu, có nêu phương pháp đo VÀ SAI SỐ CỦA PHÉP ĐO ĐÓ
       → nếu không có PTP: hardware-trigger-only, vẫn hợp lệ

[ ] 3. ≥1 rule validation theo vật lý bắt được dữ liệu xấu THẬT,
       chứng minh bằng một lần cố tình gây lỗi

[ ] 4. Chạy 7 ngày không can thiệp, completeness ≥99%,
       alert freshness ĐÃ THỰC SỰ BẮN ≥1 lần khi cố tình ngắt một nguồn

[ ] 5. Bisect được lỗi qua 4 tầng, có ghi ≥1 lần bisect thật trong notebook
```

**Stretch — KHÔNG phải gate, đừng làm nếu chưa PASS cả 5:** calibration registry có version, dashboard drift, mission registry, retention/review-for-deletion.

**Bài viết:** *"Time synchronization for multi-sensor robots: PTP vs hardware trigger, measured"*.

Đây là bài viết có tiềm năng lan xa nhất trong ba bài của bạn, vì nó trả lời một câu hỏi thực tế mà ít người đo và nhiều người cần. Cấu trúc giống Khóa 4 Bài 13, nhưng phần "What surprised me" ở đây có sẵn ứng viên rất mạnh: hai camera "chụp cùng lúc" lệch nhau hàng chục mili-giây, và không ai kiểm tra.

**FAIL → action (cam kết trước):**
- PTP không chạy sau 60h → hardware-trigger-only. Publish nguyên trạng.
- Chạm 200h chưa PASS → cắt Module 3 xuống MVP (chỉ MCAP + validation, bỏ object store và DB), giữ nguyên Module 2, publish.

---

# LỊCH 24 TUẦN

| Tuần | Giờ | Làm |
|---|---|---|
| 1 | 6 | Bài 1–2 · `ethtool -T`, chọn tầng, đặt hàng |
| 2–4 | 20 | Bài 3–4 · raw register, IMU tới đơn vị vật lý |
| 5–6 | 12 | Bài 5–6 · cảm biến 2, 3 · ESP32 node, UART vs WiFi |
| 7 | 6 | Bài 7 · ngân sách sai số, dự đoán |
| 8–9 | 10 | **Bài 8 · TN-1 GPIO chung** |
| 10–12 | 12 | **Bài 9 · TN-2 PTP** |
| 13–14 | 8 | **Bài 10 · TN-3 drift theo nhiệt độ** |
| 15–17 | 14 | **Bài 11 · TN-4 rig camera + IMU** ← dataset của riêng bạn |
| 18–19 | 14 | Bài 13 · MCAP ingest |
| 20 | 10 | Bài 14 · object store |
| 21 | 10 | Bài 15 · index |
| 22 | 10 | Bài 16 · validation vật lý |
| 23 | 6 | Bài 17 · backpressure |
| 24 | 10 | Bài 18–19 · soak 7 ngày (chạy nền) + bisect + bài viết |

**Tuần 8–17 là trái tim của khóa.** Nếu có tuần crunch MDP, hy sinh tuần 18–23 chứ đừng hy sinh tuần 8–17.

---

# NGUỒN HỌC KÈM KHÓA 5

| Nguồn | Dùng cho |
|---|---|
| **Datasheet IMU / BME280 / VL53L1X** | Nguồn thật duy nhất. Register map, scale factor, công thức bù trừ |
| **`linuxptp` docs + man page của `ptp4l`, `phc2sys`** | Bài 9. Đọc kỹ phần domain và transport |
| **`chrony` docs, phần hardware timestamping** | So sánh NTP vs PTP |
| **IEEE 1588 — đọc tổng quan, không đọc chuẩn đầy đủ** | Hiểu cơ chế trao đổi gói |
| **Jeff Geerling — bài về PTP và IEEE-1588 trên Raspberry Pi CM4** | Hướng dẫn thực hành PTP trên phần cứng Pi, bao gồm kiểm tra bằng `ethtool -T` và xuất PPS |
| **Austin's Nerdy Things — tutorial PTP grandmaster/client cho Raspberry Pi** | Quy trình đầy đủ ptp4l + phc2sys, có ví dụ Pi 5 |
| **Foxglove blog — loạt bài về thời gian trong robotics** | Góc nhìn thực hành từ ngành |
| **ROS 2 docs — About tf2, About QoS** | Frame và chính sách truyền |
| **MCAP spec** | Đã dùng ở Khóa 2, dùng lại |
| **ClickHouse / TimescaleDB docs** | Module 3 — bạn đã biết |
| **`v4l2-ctl` docs** | Điều khiển webcam: exposure, fps, format. Cần cho Bài 11 |

---

# BA ĐIỀU MANG ĐI

**1. Time sync là kỹ năng hệ thống, không phải kỹ năng cơ điện tử.** Danh sách kỹ năng khan hiếm nhất trong physical AI gồm calibration, sensor fusion, simulation realism, real-time control, và robot data pipeline — ba trong năm là kỹ năng hệ thống. Time sync nằm ngay giữa. Bạn không cạnh tranh với người học cơ điện tử 5 năm ở đây; bạn cạnh tranh với backend engineer chưa từng cắm que đo, và bạn đã cắm rồi.

**2. Rig 900 nghìn dạy đúng những bài học mà rig 900 triệu dạy.** Hai webcam USB rẻ tiền lệch nhau hàng chục mili-giây vì đúng những lý do khiến hệ camera công nghiệp lệch nhau: rolling shutter, tranh chấp băng thông, clock độc lập, không có trigger chung. Sự khác biệt là quy mô, không phải bản chất.

**3. Số đo là deliverable, platform là vỏ.** Nếu cuối khóa bạn có một platform đẹp và bốn đồ thị sai số mỏng, bạn đã làm sai khóa này. Nếu bạn có bốn đồ thị chắc chắn và một platform xấu xí nhưng chạy 7 ngày, bạn đã làm đúng.

---

# SAU KHÓA 5

Đến đây bạn có **ba artifact ★**: dataset audit tool (Khóa 2), VLA edge benchmark (Khóa 4), sensor data platform với số đo sync (Khóa 5). Cộng ba bài viết tiếng Anh và một dataset mang tên bạn trên HF Hub.

Đó là hồ sơ đủ mạnh cho vị trí robot data infrastructure — lộ trình gốc ghi rõ điều này ở kịch bản 5h/tuần: **M0–M7 vẫn là hồ sơ đủ mạnh, bỏ M8 cũng được.**

**Khóa 6 (SO-101, 120h, 7–13tr) là tùy chọn và có điều kiện.** Chỉ mở nếu M5 cho kết quả ≥2 phản hồi có nội dung. Nếu chưa, tiền và giờ đó có giá trị hơn khi dồn vào lặp lại Track D — apply, outreach, đo phản hồi.

**Và trước khi nghĩ tới Khóa 6, chạy lại M5.** Với ba artifact trong tay, tỉ lệ phản hồi của bạn bây giờ khác hẳn lần đầu. Apply là một phép đo, không phải bước cuối.
