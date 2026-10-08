# Chặng 4 — Firmware ESP32 (40h)

> **Vị trí:** C3 (bring-up trên bàn) → **C4** → C5 (lắp hoàn chỉnh lần đầu) · **Cần trước:** C3 trọn (motor, driver, encoder chạy riêng từng cái; đường cong PWM→vận tốc và vùng chết ở C3.4), K3 M1 (ESP-IDF, I2S, giao thức credit ở K3 Bài 4), K5 Bài 8 (GPIO marker + logic analyzer); → F5.2, F5.3, F5.8 · **Chạy song song với:** K4
> **Làm ra được:** firmware ESP32-S3 chạy vòng điều khiển 100 Hz từ timer phần cứng, đếm encoder bằng PCNT, xuất PWM bằng MCPWM, nói chuyện với host qua một giao thức có khung, CRC, số thứ tự và lease, có failsafe đã thử bằng lỗi thật · bảng chân đã commit, log jitter vòng lặp 10 phút (không tải và có tải), bộ test tự động trên bàn (fuzz giao thức, kịch bản failsafe) là hạt giống HIL cho C11 · **Sau chặng này bạn quyết định được:** chân nào làm gì và vì sao không dùng chân kia; task điều khiển ở core nào, ưu tiên bao nhiêu; timeout lệnh bao nhiêu ms; firmware được phép tin host tới đâu, và khi nào nó tự dừng motor bất kể host nói gì.

C3 cho bạn từng khối chạy riêng, mỗi lần một motor, lệnh gõ tay. C4 biến các khối đó thành **một chương trình chạy liên tục mà không cần bạn nhìn**: nó đọc encoder, tính lệnh, xuất PWM 100 lần mỗi giây, nhận vận tốc đặt từ mini PC, và tự đưa motor về 0 khi có gì sai. Chặng này vẫn ở trên bàn: motor kẹp vào đồ gá, bánh quay tự do, động lực từ **nguồn bàn có giới hạn dòng**, chưa có pin. Robot hoàn chỉnh chạy bằng pin là việc của C5.

**Phân bổ 40h** `[ước lượng]`:

| Phần | Giờ |
|---|---|
| Bài C4.1 Kiến trúc firmware: timer, ISR, task, MCPWM/LEDC, PCNT | 6 |
| Bài C4.2 PID vận tốc bánh và jitter vòng lặp (K7 gốc Bài 3) | 14 |
| Bài C4.3 Giao thức host↔MCU: framing, CRC, sequence, heartbeat → `ros2_control` | 8 |
| Bài C4.4 Failsafe trong firmware: watchdog, timeout, kẹp tốc độ, trạng thái an toàn mặc định | 6 |
| Lắp bước 1–6: bảng chân, đồ gá bàn, dây tín hiệu, mạch kéo xuống, đo boot glitch, chạy test tự động | 4 |
| Gate chặng 4 | 2 |
| **Tổng** | **40** |

K7 gốc Bài 3 có 14h; giữ nguyên ở C4.2. Phần failsafe phía firmware lấy từ K7 gốc Bài 15 (bước 3, 4); phần phần cứng của Bài 15 (relay, E-stop cắt động lực, watchdog độc lập) ở lại → K7 C10.1.

## 0. Bức tranh chặng

Sau chặng này bàn thử trông như sau. Khối mới so với C3: **giao thức với host**, **vòng 100 Hz chạy từ timer**, **failsafe**, và các đường cảm nhận (E-stop sense, bumper) dù E-stop thật chưa lắp.

```
   MINI PC N100 (hoặc laptop lúc đầu)                     ESP32-S3 DevKitC-1
  ┌──────────────────────────────┐   USB (native,     ┌────────────────────────────────────────────┐
  │ host_bench.py (C4.3, C4.4)   │   GPIO19/20)       │ gptimer 100 Hz ─ISR─notify─► control_task  │
  │  - gửi CMD(seq, ωL, ωR,      │◄══════════════════►│   (core 1, ưu tiên cao)                    │
  │    lease_ms) 50–100 Hz       │  khung COBS + CRC  │   đọc PCNT ×2 + esp_timer (Δt thật)        │
  │  - nhận STATE 100 Hz         │                    │   failsafe: lease, kẹp, giám sát tốc độ    │
  │  - fuzz, kịch bản lỗi        │                    │   PI ×2 + feedforward vùng chết (C3.4)     │
  │  - ghi JSONL/CSV             │                    │   MCPWM ──► PWM/DIR ×2, DRV_EN             │
  └──────────────────────────────┘                    │ comm_task (core 0, ưu tiên thấp hơn)       │
                                                       │ GPIO47 marker vòng · GPIO21 marker lệnh    │
                                                       └───┬───────────┬──────────────┬────────────┘
                                   logic analyzer ◄────────┘           │ PWM/DIR/EN   │ ENC A/B ×2 (3,3 V)
                                   (D0 marker, D1 PWM_L,               ▼              │
                                    D2 heartbeat, D3 EN)        ┌────────────┐   ┌────┴──────────┐
                                                                │ DRIVER     │──►│ MOTOR + ENC   │ ×2, kẹp vào
   NGUỒN BÀN (CC) ──đỏ── VM driver   (OUTPUT là "E-stop bàn")   │ (C3)       │   │ đồ gá, bánh   │ đồ gá, bánh
   I_set theo C3     ──đen── GND driver ── điểm sao ── GND ESP32└────────────┘   │ quay tự do    │ không chạm bàn
                                                                                  └───────────────┘
```

Dòng điện: nguồn bàn → driver → motor (dòng lớn, dây đỏ/đen to, về điểm sao); ESP32 ăn từ USB của host trong chặng này. Dòng dữ liệu: encoder → PCNT (phần cứng, không qua CPU) → task điều khiển → PWM; mỗi chu kỳ một bản ghi STATE đi lên host; host gửi CMD xuống. Thời gian: **một** nguồn nhịp là timer phần cứng của ESP32; host không đặt nhịp cho vòng điều khiển.

## 1. An toàn của chặng

**Rủi ro của C4:** bánh/motor quay bất ngờ (lúc nạp firmware, lúc boot, lúc bug đổi dấu lệnh); motor kẹt kéo dòng hãm làm nóng dây và driver; đưa điện áp 5 V của encoder hoặc 12–16 V của nhánh động lực vào chân ESP32 (chết chip, có khi chết cả cổng USB của host); tóc, dây đo, ống tay áo cuốn vào bánh hoặc hộp số. Năng lượng ở đây nhỏ hơn C1 (chưa có pin), nhưng motor có hộp số kẹp ngón tay đủ đau `[ước lượng]`.

**Quy tắc cứng:**
- KHÔNG cấp động lực (bật OUTPUT nguồn bàn cho driver) khi chưa nạp xong firmware và chưa thấy firmware báo trạng thái `DISARMED`. Nạp firmware luôn với OUTPUT **tắt**.
- KHÔNG để bánh chạm bàn khi chạy test tốc độ hoặc test lỗi. Motor kẹp vào đồ gá; bánh quay tự do trong không khí.
- KHÔNG đặt `I_set` của nguồn bàn cao hơn mức C3 đã ghi cho một motor chạy không tải cộng biên; test có dòng hãm làm riêng, ngắn, có người đứng cạnh.
- KHÔNG nối dây encoder vào chân ESP32 khi chưa đo điện áp mức cao của dây tín hiệu bằng UT33D+ (phải ≤ 3,3 V; xem mục 4).
- KHÔNG dùng chân strapping (GPIO0, 3, 45, 46), chân USB (19, 20), chân flash/PSRAM (26–32, và 33–37 nếu module có PSRAM octal) cho PWM, DIR, EN `[spec — ESP-IDF GPIO, ESP32-S3]`.
- KHÔNG để chân EN/STBY của driver thả nổi: luôn có điện trở kéo xuống ngoài, để ESP32 reset hay rút ra thì driver tắt.
- KHÔNG thử failsafe bằng cách "đợi xem nó có dừng không" với tay đặt gần bánh. Tay ở nút OUTPUT nguồn bàn.
- KHÔNG đeo dây đeo cổ, khăn, tóc dài thả khi làm cạnh bánh đang quay.

**Khi sự cố xảy ra:**

| Sự cố | Làm ngay | KHÔNG |
|---|---|---|
| Bánh quay khi không ra lệnh, hoặc không dừng | Bấm OUTPUT OFF nguồn bàn (đây là E-stop của bàn thử) | Rút USB ESP32 trước (driver có thể giữ trạng thái cuối nếu EN không có kéo xuống) |
| Driver/motor nóng, mùi khét | OUTPUT OFF; không chạm 1 phút; ghi near miss | Chạm tản nhiệt để "xem nóng cỡ nào" |
| ESP32 nóng, cổng USB host báo lỗi quá dòng | Rút USB, kiểm dây 5 V/VM có chạm chân ESP32 không | Cắm lại ngay để thử |
| Ngón tay kẹt bánh/hộp số | OUTPUT OFF trước, gỡ tay sau | Giật tay ra khi motor còn điện |

## 2. BOM chặng

Phần lớn đã có (ESP32-S3, logic analyzer, motor + driver + encoder từ C3, nguồn bàn từ C0). Giá `[ước lượng 10/2026]`, kiểm lại ở cửa hàng.

| Món | Thông số phải chọn | Vì sao (bằng số) | Giá | Kiểm khi nhận hàng | Thay thế được bằng |
|---|---|---|---|---|---|
| ESP32-S3 DevKitC-1 **thứ hai** | Cùng model, cùng module (ví dụ WROOM-1 N8R8) với con chính | Dự phòng khi cháy chip; về sau làm bàn HIL ở C11.2 | 200–300k | Nạp blink, đọc `esptool.py chip_id` và loại flash/PSRAM | Bất kỳ dev board S3 nào, nhưng bảng chân phải làm lại |
| Bo breakout cầu đấu cho DevKit | Ra chân bằng cầu đấu vít hoặc JST-XH | Dupont lỏng khi rung; ở C5 robot rung thật | 60–150k | Thông mạch từng chân | Bo đục lỗ tự hàn header + JST |
| Điện trở 10 kΩ, 1 kΩ, 100 Ω | Gói các loại | Kéo xuống EN/PWM (10 kΩ); nối tiếp chân tín hiệu dài (100 Ω); cầu phân áp | 20–50k | Đo bằng UT33D+ | — |
| Opto (PC817) hoặc cầu phân áp cho E-stop sense | Opto 4 chân + điện trở | Tách đường 12–16 V khỏi chân 3,3 V (C10.1 dùng lại) | 10–30k | Đo bằng chế độ diode | Cầu phân áp có zener 3,3 V |
| Mạch chuyển mức (nếu encoder chỉ chạy 5 V) | 4 kênh, MOSFET (BSS138) hoặc 74LVC | ESP32-S3 không chịu 5 V trên chân `[spec — datasheet ESP32-S3, Absolute Maximum Ratings]` | 20–40k | Đo mức ra 3,3 V | Cầu phân áp 10k/20k (chỉ khi tần số xung thấp, kiểm cạnh bằng logic analyzer) |
| Dây USB-C ngắn có lõi ferrite | ≤ 0,5 m, loại có dây dữ liệu (không phải dây chỉ sạc) | Dây dài mỏng + nhiễu motor = mất kết nối (C5.1) | 50–120k | `lsusb` thấy thiết bị | — |
| Đồ gá kẹp motor | Kẹp chữ C, ke nhôm, hoặc khung C2 nếu đã xong | Motor có mô-men giật khi đổi chiều; tuột khỏi bàn | 50–150k | Lắc tay không xê dịch | Khung robot C2 lật ngửa, bánh lên trời |
| Vật quán tính cho bánh (tùy chọn) | Đĩa/kẹp gắn bánh | PID chỉnh trên bánh không tải quá "nhẹ" so với robot thật (C4.2) | 0–50k | — | Tinh chỉnh lại ở C5 khi chạm đất |

**Tổng C4 `[ước lượng]`:** ~0,5–1tr.

## 3. Dụng cụ và kỹ năng tay

| Kỹ năng | Bài | Luyện trước | Đạt trông thế nào |
|---|---|---|---|
| Đo mức điện áp tín hiệu trước khi cắm vào MCU | Lắp bước 2 | Đo dây encoder khi quay tay chậm | Ghi được V_high, V_low; không cắm khi V_high > 3,6 V |
| Bấm JST-XH cho dây tín hiệu 4–6 chân, đánh nhãn hai đầu | Lắp bước 3 | Đã luyện ở C0.3 | Mỗi dây có `wire_id` trong `wiring/wires.csv` |
| Gắn kênh logic analyzer vào điểm đo có GND chung, chọn sample rate | C4.2 | K5 Bài 8 | Capture 10 phút không rớt mẫu; biết sai số mỗi cạnh |
| Nạp firmware, đọc log boot, đọc `esp_reset_reason` | C4.1 | K3 M1 | Biết chip vừa reset vì gì (brownout, WDT, nút, panic) |
| Đọc datasheet tìm bảng strapping, bảng chân có glitch lúc cấp điện | C4.1 | — | Bảng chân có cột "vì sao chân này" |

Kỹ năng tay mới ít; kỹ năng mới của chặng là **đo phần mềm bằng dụng cụ phần cứng**: đặt marker GPIO và đọc thời gian bằng logic analyzer thay vì tin `printf`.

## 4. Sơ đồ đi dây

**Bảng chân (pin budget) đề xuất** cho ESP32-S3-DevKitC-1 với module WROOM-1 N8R8 (8 MB flash, 8 MB PSRAM octal) `[tự đo — đọc chữ trên vỏ module; nếu module không có PSRAM octal thì GPIO33–37 dùng được]`. "Encoder ×4" và "PWM/DIR ×4" trong kế hoạch là 4 **tín hiệu** cho robot 2 bánh (A/B × 2; PWM/DIR × 2). Robot 4 bánh cần gấp đôi và dùng hết 4 unit PCNT của S3.

| Chức năng | GPIO | Ngoại vi | Hướng / kéo | Vì sao chân này |
|---|---|---|---|---|
| ENC_L_A / ENC_L_B | 4 / 5 | PCNT unit 0, kênh 0 và 1 | vào, kéo lên trong (+ lọc glitch PCNT) | Chân thường, không strapping. S3 có 4 unit PCNT, mỗi unit 2 kênh `[spec — ESP-IDF soc_caps ESP32-S3]` |
| ENC_R_A / ENC_R_B | 6 / 7 | PCNT unit 1 | vào | như trên |
| PWM_L / DIR_L | 15 / 16 | MCPWM0 operator 0 / GPIO | ra, **kéo xuống 10 kΩ ngoài** | Không strapping, không USB, không flash |
| PWM_R / DIR_R | 17 / 18 | MCPWM0 operator 1 / GPIO | ra, kéo xuống 10 kΩ ngoài | như trên |
| DRV_EN (STBY/nSLEEP) | 8 | GPIO | ra, **kéo xuống 10 kΩ ngoài** | Một chân tắt cả driver; ESP32 reset → chân cao trở → kéo xuống tắt driver |
| ISENSE_L / ISENSE_R | 1 / 2 | ADC1 CH0 / CH1 | vào analog | ADC2 dùng chung với Wi-Fi trên ESP32-S3; dùng ADC1 cho thứ cần đọc lúc Wi-Fi bật `[spec — ESP-IDF ADC]`. Chỉ dùng nếu driver C3 có chân current sense |
| I2C SDA / SCL | 10 / 11 | I2C0 | kéo lên 4,7 kΩ (nếu bo cảm biến chưa có) | INA226 (C1.5), IMU (C7). Dây xanh dương / vàng (Qwiic) |
| I2S BCLK / WS / DOUT / DIN | 12 / 13 / 14 / 9 | I2S0 | — | Để dành cho C12 (amp + mic); khai báo từ bây giờ để không bị chiếm |
| BUMPER_L / BUMPER_R | 39 / 40 | GPIO ngắt | vào, kéo lên; công tắc NC xuống GND | Đứt dây = chân lên cao = "đã va" (hỏng về phía an toàn). Chân JTAG pad, rảnh khi dùng JTAG qua USB |
| ESTOP_SENSE | 41 | GPIO ngắt + (tùy chọn) MCPWM fault | vào qua opto | Đọc trạng thái chuỗi E-stop (C5 tạm, C10.1 thật) |
| RELAY_HOLD | 42 | GPIO/LEDC | ra, kéo xuống ngoài | Xung giữ cho mạch relay ở C10.1; để dành |
| DBG_LOOP | 47 | GPIO | ra | Marker đầu/cuối mỗi chu kỳ điều khiển (C4.2) |
| DBG_CMD | 21 | GPIO | ra | Đảo mỗi khi nhận lệnh hợp lệ (C4.3, C4.4) |
| **Không dùng** | 0, 3, 45, 46 | strapping | — | Mức lúc reset quyết định chế độ boot `[spec — ESP-IDF GPIO ESP32-S3]` |
| **Không dùng** | 19, 20 | USB Serial/JTAG | — | Đường nói chuyện với host |
| **Không dùng** | 26–32; 33–37 với PSRAM octal | SPI flash/PSRAM | — | `[spec — ESP-IDF GPIO ESP32-S3]` |
| **Không dùng** | 43, 44 | UART0 | — | Log boot của ROM và console |
| Kiểm theo bo | 38 hoặc 48 | LED RGB trên DevKitC-1 | — | Tùy revision bo `[tự đo — xem sơ đồ nguyên lý đúng revision]` |

Ngoài bảng trên: datasheet ESP32-S3 có mục liệt kê **chân có glitch lúc cấp điện** (xung ngắn trước khi firmware chạy) `[spec — datasheet ESP32-S3, tra mục về trạng thái chân lúc khởi động; kiểm theo revision]`. Đối chiếu với PWM/DIR/EN. Dù chân nào, thiết kế phải chịu được: điện trở kéo xuống + **DRV_EN chỉ lên cao sau khi firmware ARM** (C4.4) nghĩa là glitch trên PWM không làm motor quay vì driver đang tắt. Lắp bước 5 kiểm điều đó bằng logic analyzer.

**Sơ đồ dây bàn thử** (màu theo C0.5):

```
 NGUỒN BÀN (+) ──đỏ 18 AWG──────────────► VM driver
 NGUỒN BÀN (−) ──đen 18 AWG──► ĐIỂM SAO (ốc trên đồ gá) ◄──đen 18 AWG── GND driver (phía công suất)
                                   │
                                   └──đen 22 AWG──► GND ESP32 (một dây, không đi vòng qua motor)
 Motor L ◄══ dây motor (xoắn đôi, xa dây encoder ≥ 3 cm) ══ driver OUT_L     (tương tự motor R)

 ESP32 3V3 ──trắng "3V3"──► Vcc encoder L, R   (nếu encoder chạy 3,3 V — kiểm ở Lắp bước 2)
 ESP32 GND ──đen──────────► GND encoder
 ENC_L_A ◄──xanh lá── encoder L A        ENC_L_B ◄──xám── encoder L B     (giữ màu nhà sản xuất nếu có sẵn,
 ENC_R_A ◄──xanh lá── encoder R A        ENC_R_B ◄──xám── encoder R B      ghi vào wires.csv)
 GPIO15 ─[100 Ω]─┬─► PWM_L driver        GPIO8 ─[100 Ω]─┬─► EN/STBY driver
                 └[10 kΩ]─ GND                           └[10 kΩ]─ GND
 GPIO47 ──► logic analyzer D0 ;  GPIO15 ──► D1 ;  GPIO21 ──► D2 ;  GPIO8 ──► D3 ;  GND LA ── GND ESP32
```

Tiết diện: dây động lực bàn thử 18 AWG đủ cho dòng không tải và các lần thử dòng hãm ngắn có `I_set` giới hạn `[ước lượng — C1.3 tính lại cho robot]`; dây tín hiệu 22–26 AWG. Không có cầu chì riêng ở bàn thử: `I_set` của nguồn bàn đóng vai giới hạn dòng.

## 5. Trình tự chặng

1. **Học Bài C4.1** (commit `prediction.md` trước khi mở 🔒).
2. **Lắp bước 1 — Bảng chân**
   - Làm: chép bảng ở mục 4 vào `firmware/PINS.md`, sửa theo bo thật (đọc chữ trên module, sơ đồ nguyên lý DevKit đúng revision). Mỗi chân một dòng "vì sao". Commit. Từ nay đổi chân phải đổi file này trước, code sau.
   - ✅ Checkpoint: script nhỏ (hoặc `grep`) đối chiếu mọi `#define PIN_` trong firmware với `PINS.md`, và với danh sách cấm (0, 3, 19, 20, 26–37, 43–46). Không có chân nào trong danh sách cấm.
   - Nếu sai: đổi chân trong `PINS.md` trước, rồi code.
3. **Lắp bước 2 — Đo mức tín hiệu encoder trước khi cắm**
   - Làm: cấp Vcc cho encoder bằng nguồn bàn (chế độ CV, `I_set` 50 mA), lần lượt 3,3 V rồi 5 V nếu datasheet cho phép. Quay bánh thật chậm bằng tay; đo dây A so với GND bằng UT33D+ ở hai vị trí (mức cao, mức thấp).
   - ✅ Checkpoint trước khi cắm vào ESP32: V_high ≤ 3,6 V và V_low ≤ 0,4 V `[ước lượng — ngưỡng logic ESP32-S3 theo datasheet, VIH/VIL tỉ lệ VDD]`. Encoder chạy được ở 3,3 V thì cấp 3,3 V từ ESP32; nếu không, chèn mạch chuyển mức.
   - Nếu sai: không cắm. Ghi V_high vào sổ; đặt mạch chuyển mức.
4. **Lắp bước 3 — Dây tín hiệu và mạch kéo xuống**
   - Làm: đi dây theo mục 4, bấm JST, đánh nhãn, ghi `wiring/wires.csv`. Hàn 10 kΩ kéo xuống cho PWM_L, PWM_R, DRV_EN và 100 Ω nối tiếp.
   - ✅ Checkpoint trước khi cấp điện (USB rút, nguồn bàn tắt): đo Ω giữa GPIO8 và GND trên bo breakout: ≈ 10 kΩ (kéo xuống có mặt). Đo Ω giữa 3V3 và GND của ESP32: không gần 0 Ω. Đo Ω giữa VM driver và bất kỳ chân ESP32 nào: **OL** (hở).
   - Nếu sai: tìm chỗ chạm trước khi cắm USB.
5. **Học Bài C4.2**, làm phần 6 của bài (đo jitter, tinh chỉnh trên bàn).
6. **Lắp bước 4 — Đồ gá và lần quay đầu tiên dưới firmware mới**
   - Làm: kẹp motor; bánh không chạm gì. Nạp firmware với OUTPUT nguồn bàn tắt; mở log, thấy `DISARMED`. Bật OUTPUT. Gửi `ARM` rồi lệnh 1 rad/s cho bánh trái trong 2 s.
   - ✅ Checkpoint: bánh trái quay **đúng chiều** quy ước (tiến = dương theo REP-103 khi bánh lắp trên robot; ghi trong `PINS.md`), bánh phải đứng yên; STATE báo count tăng **dương**. Sai dấu ở encoder hoặc DIR là lỗi số 1 của chặng này.
   - Nếu sai: đảo dấu trong cấu hình (một chỗ duy nhất, `config.h`), không đảo dây "cho nhanh" mà không ghi lại.
7. **Học Bài C4.3**; chạy fuzz giao thức trên bàn.
8. **Học Bài C4.4**; chạy kịch bản failsafe (phần 6 của bài).
9. **Lắp bước 5 — Boot glitch**
   - Làm: logic analyzer D1 = PWM_L, D3 = DRV_EN, trigger theo cạnh lên của 3V3 ESP32 (qua cầu phân áp nếu cần) hoặc bắt đầu capture rồi cắm USB. Cấp nguồn ESP32 20 lần, mỗi lần 3 s; nhấn nút RST 10 lần; nạp firmware 3 lần, tất cả với **VM đang có điện** và bánh tự do.
   - ✅ Checkpoint: DRV_EN không có cạnh lên nào khi firmware chưa nhận `ARM`. Có glitch trên PWM là chấp nhận được **chỉ khi** DRV_EN thấp suốt lúc đó. Bánh không nhúc nhích lần nào.
   - Nếu sai: đổi chân EN, tăng kéo xuống (4,7 kΩ), kiểm firmware không cấu hình EN là output-high trước khi ARM.
10. **Lắp bước 6 — Chạy bộ test tự động** (`tests/bench/`: fuzz, failsafe, jitter) một lượt sạch, ghi kết quả vào sổ.
11. **Gate chặng 4.**

## 6. Lỗi người mới hay gặp

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Đọc encoder ra số nhảy lung tung khi motor chạy, đúng khi quay tay | Nhiễu PWM motor cảm ứng vào dây encoder; thiếu lọc glitch | Logic analyzer trên dây A khi motor chạy | Lọc glitch PCNT, dây encoder xa dây motor, xoắn dây motor, GND một điểm |
| Count đúng vài giây rồi nhảy một khoảng rất lớn | PCNT về 0 khi chạm `high_limit`, code trừ hai lần đọc không xử lý | Chạy liên tục > 30.000 count, so tổng | `flags.accum_count` + watch point ở hai limit (Bài C4.1) |
| Bánh quay một cái lúc nạp firmware hoặc lúc cắm USB | Chân EN/PWM thả nổi hoặc là chân có glitch, thiếu kéo xuống | Lắp bước 5 | Kéo xuống ngoài; EN chỉ lên sau ARM |
| ESP32 reset mỗi lần mở cổng serial trên host | Mở cổng đổi DTR/RTS, mạch tự reset của DevKit/USB Serial/JTAG hiểu là lệnh reset | Đếm `boot_count` trong STATE trước/sau khi mở cổng | Cấu hình host không đụng DTR/RTS (Bài C4.3) `[tự đo]` |
| Vòng điều khiển chậm dần khi host không đọc serial | Ghi serial blocking trong task điều khiển, buffer TX đầy | Marker GPIO: độ rộng tăng khi đóng chương trình host | Task điều khiển không bao giờ ghi USB; ghi vào ring buffer, task khác gửi, đầy thì bỏ và đếm |
| `printf` "chạy ổn" nhưng jitter p99 hàng ms | Log trong vòng | Bỏ log, đo lại | Ring buffer + task log ưu tiên thấp |
| Bánh trái chạy khi ra lệnh bánh phải | Đổi chéo dây hoặc chân | Lệnh từng bánh riêng | Sửa `PINS.md`, rồi code |

Lỗi riêng của từng bài ở phần 8 của bài.

## 7. Lăng kính data infra

**Dữ liệu chặng này sinh ra:**

| Luồng | Nơi | Schema (rút gọn) | Tần số | Đơn vị / ghi chú |
|---|---|---|---|---|
| STATE từ firmware | `logs/bench/state-*.jsonl` (C4), về sau `/joint_states` + `/diagnostics` qua `ros2_control` (C5) | `t_mcu_us, seq, boot_count, enc_l, enc_r (count tích lũy, int32+), w_l, w_r (rad/s), u_l, u_r (duty −1..1), state, fault_mask, last_cmd_seq, loop_overrun, jitter_max_us_1s` | 100 Hz | rad/s, s; count giữ nguyên dạng nguyên để tái tính được |
| Lệnh từ host | `logs/bench/cmd-*.jsonl` | `t_host_ns, seq, w_l_cmd, w_r_cmd, lease_ms` | 50–100 Hz | — |
| Capture marker | `captures/c04/*.sr` + bảng chu kỳ `.csv` | `k, t_rise_s, period_s, width_s` | 100 Hz trong 10 phút | s |
| Kết quả test bàn | `build-log/measurements.jsonl` (schema C0.5) | `quantity` = `loop_jitter_p99`, `fuzz_wrong_applied`, `failsafe_stop_time`… | theo lần chạy | SI: `s`, không `us` trong dữ liệu |

`clock_source` của `t_mcu_us` là `esp32_timer`; của `t_host_ns` là `host_unsynced` cho tới C7.2 (→ `CONVENTIONS.md` mục 4). `firmware_version` = git hash nhúng lúc build, có trong gói STATE đầu tiên sau boot và trong metadata.

**Test tự động sinh ra từ chặng này (hạt giống HIL cho C11.2):**
- `test_jitter`: chạy 10 phút, đọc capture logic analyzer, chấm p99 < 100 µs, ba trạng thái (pass / fail / inconclusive khi rớt mẫu hoặc < 10.000 chu kỳ).
- `test_protocol_fuzz`: host bơm 10⁵ khung có lỗi cố ý; firmware không áp dụng lệnh sai nào; bộ đếm `bad_crc` khớp số khung hỏng (sai lệch giải thích được).
- `test_failsafe_*`: mỗi kịch bản ở Bài C4.4 là một test có oracle là mô hình Python `s5_failsafe.py`. Ở C11.2 cùng test chạy trên bàn HIL, chỉ thay "bánh thật" bằng tín hiệu giả.

**SLI của firmware:** jitter p99 và max theo cửa sổ 1 s (gửi trong STATE), `loop_overrun` (chu kỳ bị lỡ), tỉ lệ khung hỏng, số lần failsafe theo lý do, `boot_count` và lý do reset. Đây là metric như mọi service; điểm khác là **ngưỡng của nó suy ra từ vật lý** (Bài C4.2), không từ SLO kinh doanh.

**Vai trò nghề:** Test & Validation (bench test có oracle, fuzz, fault injection — → F2.4, F2.5); Data Platform (schema STATE có số thứ tự, đơn vị, phiên bản firmware — thứ làm cho dữ liệu robot audit được ở C7).

## 8. Nhật ký build

Copy vào `build-log/c04.md`, một mục mỗi buổi:

```markdown

## 2026-MM-DD — buổi N (giờ bắt đầu–kết thúc, giờ thực: _._ h)
- Trạng thái người: tỉnh táo / mệt (mệt → chỉ đọc, không bật động lực)
- Firmware: git hash ____ ; ESP-IDF ____ ; bo ____ (module ____)
- Mục tiêu buổi:
- Đã làm:
- Số đo (measurements.jsonl, số dòng: __): jitter p50/p99/max ____ ; utilization ____ ; ...
- Capture: captures/c04/...
- Lỗi gặp (triệu chứng → nguyên nhân → sửa):
- Reset lạ của ESP32? lý do (esp_reset_reason): ____
- Quyết định (→ decisions.md nếu ảnh hưởng chặng sau; ví dụ timeout lệnh, core của task):
- Near miss (bánh quay bất ngờ, chạm dây động lực vào chân logic…):
- Câu hỏi còn mở:
```

---
