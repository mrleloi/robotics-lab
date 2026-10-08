# Khóa 5 · Module 1 — Cảm biến và raw register (32h)

> Bốn bài: bắt tay với chip (Bài 3), tự tay biến raw thành đơn vị vật lý (Bài 4), chọn và đặc trưng hóa cảm biến thứ hai và thứ ba (Bài 5), đưa dữ liệu từ ESP32-S3 về mini PC và hiểu timestamp đi lạc ở đâu (Bài 6). Gate Module 1 ở cuối file.
>
> Nguồn: `khoa-5-sensor-timesync-platform.md` (Module 1), bản Gemini K5 Bài 3–6 (đã gặt, lỗi ghi ở phần 11 từng bài). Repo hiện chưa có driver cảm biến nào trong `src/` (chỉ có `src/proto/sensors/v1/imu.proto` từ K2), nên mọi driver ở đây bạn viết mới.

---

## Bài 3 — Quét bus và bắt tay với chip (5h)

> **Vị trí:** Bài 2 (kế hoạch đo) → **Bài 3** → Bài 4 (raw → đơn vị vật lý) · **Cần trước:** K1 Bài 12 (I2C và ACK trên logic analyzer), → F5.1 · **Sau bài này bạn quyết định được:** một lỗi đọc cảm biến nằm ở dây/nguồn/địa chỉ hay ở code — trước khi mở debugger.

### 1. Câu chuyện — ai đã khổ vì chuyện này

I2C do Philips làm ra đầu thập niên 1980 để nối các chip trong TV bằng hai dây thay vì cả chùm `[chuẩn — NXP UM10204, phần giới thiệu]`. Cái giá của hai dây là mọi thiết bị chung một đường: một chip treo giữ SDA ở mức thấp thì **cả bus** chết, và bus không có cơ chế nào báo "hai chip đang trùng địa chỉ". Thị trường module rẻ thêm một lớp khổ nữa: nhiều module bán dưới tên MPU6050 mang chip khác hoặc chip nhái, có con trả về `WHO_AM_I` khác giá trị datasheet (người dùng trên diễn đàn báo nhiều giá trị khác nhau) `[tự đo — đọc chip của bạn]`. Ai bỏ qua bước bắt tay sẽ debug code ba ngày cho một lỗi đấu dây, hoặc tệ hơn, thu dữ liệu một tuần từ một chip không phải thứ mình tưởng.

### 2. Mô hình tư duy

```
 3V3 ──┬──────────┬──────────── (pull-up Rp: mỗi module thường có sẵn một cặp)
       Rp         Rp
 SDA ──┴──┬───────┼───┬──────── mọi chip chỉ được KÉO XUỐNG (open-drain), không đẩy lên
 SCL ─────┼──┬────┴───┼──┬───── mức cao = "không ai kéo" → wired-AND
         ESP32   IMU     BME280   (+ điện dung dây/chân Cb: càng nhiều module, cạnh lên càng chậm)

 Đọc 1 thanh ghi (ví dụ BME280 id @0xD0):
 SCL  ‾‾\_/‾\_/‾ … ‾\_/‾‾‾‾\_/‾\_/‾ … ‾\_/‾‾‾\_/‾ … ‾\_/‾‾‾‾‾
 SDA  ‾\_[ 0x76 W ][A][  0xD0  ][A]‾\_[ 0x76 R ][A][ data ][N]_/‾
       S                          Sr                          P
 S=START  Sr=repeated START  A=ACK (slave kéo SDA xuống ở xung thứ 9)  N=NACK (master không kéo)  P=STOP
```

Bus I2C là một dây chung mà ai cũng chỉ được kéo xuống. Từ đó suy ra gần hết hành vi của nó: ACK là "có ai đó kéo SDA xuống ở xung thứ 9" (không nói *ai*); hai chip trùng địa chỉ cùng ACK và cùng trả dữ liệu, bus AND hai luồng bit lại thành rác mà không báo lỗi; cạnh lên do điện trở pull-up nạp điện dung bus, nên nhiều module (nhiều Cb, pull-up song song) thay đổi cả tốc độ cạnh lẫn dòng phải kéo. Thanh ghi nhận dạng (`WHO_AM_I`, `id`, Model ID) là phép thử rẻ nhất cho cả chuỗi: nguồn, dây, địa chỉ, logic số của chip. Nó **không** thử phần cảm biến (MEMS, màng áp suất, SPAD).

Hai giới hạn pull-up `[spec NXP UM10204, mục về điện trở kéo lên]`:
- Rp nhỏ nhất: `Rp_min = (VDD − V_OL,max) / I_OL` — dòng chip phải hút khi kéo xuống không được vượt mức chuẩn (với 3,3 V, tra V_OL và I_OL cho chế độ bạn dùng).
- Rp lớn nhất: `Rp_max = t_r / (0,8473 · C_b)` — cạnh lên phải đủ nhanh (t_r tối đa theo chế độ: Standard 100 kHz, Fast 400 kHz).

Hai giới hạn này có **hai cách sửa khác nhau**: Rp quá nhỏ thì phải tháo bớt pull-up; Rp quá lớn hoặc Cb quá lớn thì giảm tốc độ bus hoặc rút ngắn dây. Giảm tốc độ không chữa được Rp quá nhỏ.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Port scan (`nmap`) để thấy service nào đang nghe | I2C scanner: gửi địa chỉ, xem ai ACK | ACK không mang danh tính; hai chip trùng địa chỉ cùng ACK, bus không phát hiện xung đột như TCP RST | Tin scanner "thấy 0x68" nghĩa là đúng một IMU — trong khi hai IMU cùng 0x68 trả rác |
| Endpoint `/health` (so sánh của Gemini) | Đọc `WHO_AM_I` | `/health` tốt thường chạm logic app; `WHO_AM_I` chỉ chạm giao tiếp số, không chạm phần tử cảm biến | Coi chip "khỏe" trong khi màng MEMS hỏng, dữ liệu đơ |
| Một client treo không làm sập server | Một slave treo giữ SDA thấp làm sập **cả bus** | Không có timeout ở tầng vật lý; phải tự "bus recovery" (master nháy SCL tới khi slave nhả SDA) | Reset ESP32 giữa lúc đọc, bus treo, đổ lỗi cho firmware mới |
| Thêm instance sau load balancer là tuyến tính | Thêm module lên bus | Mỗi module thêm điện dung và pull-up song song; có ngưỡng gãy không tuyến tính | "Hai cái chạy thì ba cái cũng chạy" |

**Chấm mô hình:**

- *"Đọc đúng `WHO_AM_I` là cảm biến hoạt động đúng."* — **ĐÚNG MỘT PHẦN.** Nó chứng minh nguồn, dây, địa chỉ và lõi số của chip trả lời. Nó không chứng minh phần tử đo hoạt động, không chứng minh chip chính hãng (nhái có thể trả đúng ID), không chứng minh cấu hình đúng. Phản ví dụ: BME280 có cảm biến ẩm hỏng vẫn trả `id` đúng; kênh ẩm đọc một giá trị cố định mãi mãi. Bài 4–5 mới kiểm phần đo.
- *"I2C giống một mạng nhỏ có địa chỉ; cắm thêm thiết bị là được."* — **ĐÚNG MỘT PHẦN.** Có địa chỉ, có giao dịch, đúng. Nhưng không có phát hiện trùng địa chỉ, không có cô lập lỗi (một slave treo giết cả bus), và có ngân sách điện (Rp, Cb) giới hạn số module. Phản ví dụ: bạn mua hai IMU cùng loại (bản gốc khuyên vậy); cắm cả hai lên một bus khi cả hai chân AD0 cùng nối GND → cùng 0x68, scanner vẫn chỉ thấy một địa chỉ "khỏe".

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | Open-drain / wired-AND | Thiết bị chỉ kéo xuống; mức cao là do pull-up | "Chân đẩy lên 3,3 V" |
| 🟢 | ACK/NACK | Bên nhận kéo/không kéo SDA ở xung thứ 9 | Xác nhận dữ liệu *đúng* (chỉ là *đã nhận*) |
| 🟢 | Repeated START (Sr) | START mới mà không STOP, giữ quyền bus giữa ghi con trỏ và đọc | Hai giao dịch rời |
| 🟢 | Địa chỉ 7-bit vs byte địa chỉ 8-bit | 0x76 (7-bit) dịch trái 1 + bit R/W thành 0xEC/0xED | Hai chip khác nhau |
| 🟢 | Thanh ghi nhận dạng | Thanh ghi chỉ đọc chứa mã chip cố định | Số serial riêng từng con |
| 🟡 | Clock stretching | Slave giữ SCL thấp để xin thêm thời gian | Lỗi bus |
| 🟡 | Bus recovery | Master tạo tới 9 xung SCL để slave đang kẹt nhả SDA | Reset nguồn |
| 🟡 | Strapping pin (ESP32-S3) | Chân được đọc lúc boot để chọn chế độ | Chân thường dùng được cho I2C |
| 🔴 | I3C, SMBus PEC | Chuẩn kế thừa/biến thể | Cần cho khóa này |

### 5. Dự đoán

`lab/k5-03-bus/prediction.md`, commit trước khi cắm:

```markdown
| Module | Địa chỉ dự đoán (7-bit) | Chân chọn địa chỉ trên module nối đâu? | Thanh ghi ID | Giá trị dự đoán | Nguồn (datasheet, mục) |
|---|---|---|---|---|---|
| IMU #1 | | | | | |
| IMU #2 (cùng bus) | | | | | |
| BME280 | | | | | |
| VL53L1X | | | (địa chỉ thanh ghi 16-bit!) | | |

Pull-up: đọc mã điện trở trên từng module (ví dụ "472" = 4,7 kΩ, "103" = 10 kΩ).
- Rp tương đương khi cắm cả 3 (4 nếu cả hai IMU): ____ Ω (song song)
- Rp_min theo UM10204 ở 3,3 V: ____ Ω     - Rp_max ở 400 kHz với Cb ước lượng ____ pF: ____ Ω
- Áp SDA/SCL lúc idle: ____ V
- Có bao nhiêu module cùng loại cắm được trước khi vi phạm Rp_min?
```

Tra: datasheet từng chip (bảng địa chỉ, register map), UM10204 (bảng đặc tính chế độ Standard/Fast), mã điện trở SMD.

### 6. Làm

1. **Một cảm biến một lần.** 3,3 V từ chân 3V3 của ESP32-S3, **không phải 5 V**; GND chung. Chọn hai GPIO không phải strapping pin và không phải chân USB (tra bảng chân ESP32-S3 `[spec ESP32-S3 datasheet, mục Strapping Pins]`). Module BME280 có hai loại: chỉ 3,3 V, hoặc có ổn áp + level shifter cho 5 V `[tự đo — nhìn mạch module]`; ghi bạn có loại nào.
2. **Đo pull-up khi chưa cấp nguồn.** Multimeter thang Ω giữa SDA và 3V3 của module (và SCL–3V3). Sai số: UT33D+ thang Ω có độ chính xác ghi trong manual `[spec]`; đầu que và breadboard thêm vài phần mười Ω — không đáng kể ở kΩ.
3. **Scanner + đọc ID.** ESP-IDF v5 có driver I2C master mới; API đổi giữa các bản `[tự đo — kiểm theo phiên bản ESP-IDF bạn cài]`:

```c
// [chưa chạy] ESP-IDF v5.x, driver/i2c_master.h. Sửa GPIO theo bảng chân của bạn.
#include "driver/i2c_master.h"
#include <stdio.h>
void app_main(void) {
    i2c_master_bus_config_t cfg = {
        .i2c_port = I2C_NUM_0, .sda_io_num = 8, .scl_io_num = 9,
        .clk_source = I2C_CLK_SRC_DEFAULT, .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = false,      // dùng pull-up trên module; ghi rõ lựa chọn này
    };
    i2c_master_bus_handle_t bus;
    ESP_ERROR_CHECK(i2c_new_master_bus(&cfg, &bus));
    for (uint16_t a = 0x08; a < 0x78; a++)          // bỏ dải địa chỉ dành riêng
        if (i2c_master_probe(bus, a, 50) == ESP_OK) printf("ACK 0x%02x\n", a);

    i2c_device_config_t dc = { .dev_addr_length = I2C_ADDR_BIT_LEN_7,
                               .device_address = 0x76, .scl_speed_hz = 100000 };
    i2c_master_dev_handle_t bme;
    ESP_ERROR_CHECK(i2c_master_bus_add_device(bus, &dc, &bme));
    uint8_t reg = 0xD0, id = 0;                     // ghi con trỏ, Sr, đọc 1 byte
    ESP_ERROR_CHECK(i2c_master_transmit_receive(bme, &reg, 1, &id, 1, 50));
    printf("BME280 id = 0x%02x\n", id);
}
```

   VL53L1X dùng **địa chỉ thanh ghi 16 bit**: gửi 2 byte con trỏ (0x01, 0x0F) rồi đọc 2 byte. Gửi 1 byte như với BME280 sẽ đọc nhầm chỗ.
4. **Logic analyzer.** D0 → SCL, D1 → SDA, GND chung. PulseView, 24 MHz (dư ~60 mẫu/bit ở 400 kHz; phân giải thời gian 41,7 ns), decoder I²C. Chụp đúng giao dịch đọc ID, đánh dấu S, địa chỉ+W, A, con trỏ, A, Sr, địa chỉ+R, A, data, N, P. Lưu file `.sr` vào repo.
5. **Cả ba (hoặc bốn) trên một bus.** Thêm từng module, scan lại sau mỗi lần. IMU thứ hai: đổi chân chọn địa chỉ (AD0/SDO) lên 3,3 V để ra địa chỉ thứ hai. Đo lại Rp giữa SDA–3V3 khi tắt nguồn, so với tính toán.
6. **Bus treo, có chủ đích.** Trong vòng lặp đọc liên tục, bấm reset ESP32 nhiều lần. Có lần nào sau reset scanner không thấy gì? Đo áp SDA lúc đó. Viết hàm bus recovery (nháy SCL bằng GPIO tối đa 9 lần tới khi SDA lên cao, rồi tạo STOP) hoặc dùng hàm reset bus của driver nếu bản ESP-IDF của bạn có `[tự đo]`. Ghi kết quả.

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

| Kiểm | Kết quả đúng | Ghi chú |
|---|---|---|
| MPU6050 | ACK ở 0x68 (AD0 thấp) / 0x69 (AD0 cao); `WHO_AM_I` @0x75 = **0x68** cả hai trường hợp | Bit địa chỉ AD0 không phản ánh trong `WHO_AM_I` `[spec MPU-6000/6050 Register Map, WHO_AM_I]`. Giá trị khác (0x70, 0x72, 0x98…) → chip khác/nhái, ghi lại và đối chiếu ở Bài 5 |
| ICM-42688-P | 0x68/0x69; `WHO_AM_I` @0x75 = **0x47** | `[spec TDK DS-000347]` |
| BME280 | 0x76 (SDO→GND) / 0x77; `id` @0xD0 = **0x60** | 0x58 = BMP280 (không có ẩm) |
| VL53L1X | 0x29; đọc 16-bit @0x010F = **0xEACC** | Byte 0x010F = 0xEA (model), 0x0110 = 0xCC (module type) |
| Áp SDA/SCL idle | ≈ 3,3 V (trong sai số multimeter cỡ ±1%) | 0 V: thiếu pull-up hoặc chập; ~5 V: module kéo lên 5 V qua level shifter — nguy hiểm cho chân ESP32 |
| Rp tương đương | Ba module 10 kΩ → ~3,3 kΩ; ba module 4,7 kΩ → ~1,6 kΩ | Rp_min ở 3,3 V với V_OL 0,4 V, I_OL 3 mA ≈ 0,97 kΩ → cần cỡ 5–6 module 4,7 kΩ song song mới vi phạm. Với 3–4 module, "pull-up quá mạnh" ít khi là nguyên nhân |
| Rp_max (400 kHz, t_r 300 ns) | Cb = 50 pF → ~7 kΩ; Cb = 150 pF → ~2,4 kΩ | Một module 10 kΩ duy nhất + dây dài có thể cạnh lên quá chậm ở 400 kHz; 100 kHz an toàn hơn |
| Logic analyzer | ACK sau mọi byte, NACK chỉ ở byte đọc cuối, Sr giữa ghi con trỏ và đọc | Có NACK ở byte địa chỉ → sai địa chỉ / chip không trả lời |
| Bus treo sau reset | Thỉnh thoảng có (khi reset rơi đúng lúc slave đang xuất bit 0); SDA đo ≈ 0 V | Recovery bằng xung SCL đưa bus về sống mà không cần rút nguồn |

Lệch so với bảng không phải luôn là lỗi: module nhái là dữ liệu; bus treo không tái hiện được chỉ có nghĩa xác suất thấp với tần số đọc của bạn.

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Scanner không thấy gì | Thiếu pull-up, SDA/SCL đảo, chưa cấp nguồn, chọn strapping pin | Đo áp idle; đo Ω SDA–3V3 khi tắt nguồn | Thêm pull-up 4,7 kΩ ngoài; đổi chân |
| Thấy mọi địa chỉ 0x08–0x77 | SDA bị kéo thấp liên tục (bus treo, chập) | Áp SDA ≈ 0 V | Bus recovery; tìm chập |
| Code dùng 0xEC thay 0x76 | Lẫn địa chỉ 8-bit (datasheet/thư viện cũ) với 7-bit (ESP-IDF) | So với output scanner | Dùng 7-bit |
| Địa chỉ đúng, ID sai | Chip khác/nhái; đọc thanh ghi 16-bit bằng con trỏ 8-bit (VL53L1X) | Logic analyzer: số byte con trỏ | Đối chiếu bảng; ghi model thật |
| Hai IMU, scanner thấy một địa chỉ, dữ liệu vô lý | Trùng địa chỉ, wired-AND trộn hai luồng | Rút một IMU, đọc lại | Đổi AD0/SDO của một con |
| Thêm module thì bus chập chờn | Cạnh lên chậm (Cb lớn, Rp lớn, dây dài) — **giảm tốc độ** giúp được; hoặc Rp tổng quá nhỏ — giảm tốc độ **không** giúp | Đo Rp tương đương; so với Rp_min/Rp_max | Cạnh chậm: 100 kHz, dây ngắn, pull-up nhỏ hơn. Rp quá nhỏ: tháo pull-up trên bớt module |
| Lúc được lúc không | Dây Dupont lỏng, breadboard mòn | Lắc nhẹ dây khi đang đọc | Dây ngắn, hàn header (→ K1 Bài 8) |
| ESP32 nóng / chân hỏng | Module 5 V kéo SDA lên 5 V | Áp idle | Chỉ dùng module 3,3 V hoặc level shifter đúng |

### 9. Câu hỏi ngược

1. **[Failure mode]** Robot đang chạy, một cảm biến I2C bị rung lỏng chân và giữ SDA thấp. Những cảm biến nào khác "chết" theo, và firmware nên làm gì để phần còn lại của robot biết?
<details><summary>Hướng nghĩ</summary>

Mọi thứ trên cùng bus. Firmware cần timeout mỗi giao dịch, bus recovery tự động, và báo trạng thái lên host (topic chẩn đoán, → CONVENTIONS `/diagnostics`). Thiết kế thật thường tách cảm biến quan trọng sang bus riêng.

</details>

2. **[Vì sao không]** Vì sao không dùng pull-up nội của ESP32 cho gọn?
<details><summary>Hướng nghĩ</summary>

Tra giá trị pull-up nội trong datasheet ESP32-S3 (cỡ hàng chục kΩ) và đặt vào công thức Rp_max với Cb của breadboard. So với t_r cho phép ở 400 kHz.

</details>

3. **[Quy mô]** Một robot có 12 cảm biến I2C, ba cái cùng địa chỉ cố định không đổi được. Có những cách nào?
<details><summary>Hướng nghĩ</summary>

Nhiều bus (ESP32-S3 có hai bộ I2C), bộ chuyển kênh I2C (multiplexer), chân XSHUT để bật từng VL53L1X rồi đổi địa chỉ bằng phần mềm. Mỗi cách đổi lấy một chi phí: chân, độ trễ, độ phức tạp khởi động.

</details>

4. **[Liên ngành]** CAN bus trong ô tô cũng dùng một dây chung "kéo xuống thắng" (dominant/recessive). Nó biến điểm yếu của I2C thành tính năng thế nào?
<details><summary>Hướng nghĩ</summary>

CAN dùng wired-AND để **phân xử**: hai node cùng gửi, node nào gửi bit dominant (0) ở vị trí đầu tiên khác nhau thì thắng mà không hỏng khung. I2C multi-master cũng có phân xử tương tự, nhưng không có ID duy nhất cho mỗi thiết bị.

</details>

5. **[Phản biện]** "Logic analyzer thừa, scanner in ra ACK là đủ." Khi nào câu này sai?
<details><summary>Hướng nghĩ</summary>

Khi lỗi nằm ở thứ scanner không thấy: số byte con trỏ sai, thiếu Sr, clock stretching kéo dài, NACK ở byte giữa. Và ở Bài 19, tầng "bus" chỉ kiểm được bằng dụng cụ đo.

</details>

### 10. Liên kết ra ngoài

- **CAN và LIN trong ô tô:** cùng ý tưởng một dây chung, open-collector, nhưng CAN thêm phân xử theo ID, CRC và đếm lỗi để tự cô lập node hỏng (bus-off). I2C không có cơ chế cô lập nào — đó là lý do I2C ở trong một bo mạch, còn CAN đi khắp xe.
- **Ethernet 10BASE5 đời đầu (CSMA/CD):** môi trường chung, va chạm phải phát hiện. Ethernet hiện đại bỏ môi trường chung (switch, full-duplex); I2C giữ môi trường chung vì dây ngắn và rẻ.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| Địa chỉ và giá trị ID trong bảng | `[spec]` datasheet từng chip | Bước 3 |
| Công thức Rp_min, Rp_max | `[spec]` NXP UM10204 | Tra V_OL, I_OL, t_r cho chế độ bạn dùng |
| Module nhái trả ID khác | `[tự đo]` | Chỉ có báo cáo diễn đàn; đọc chip của bạn |
| Pull-up nội ESP32-S3 cỡ hàng chục kΩ | `[spec]` ESP32-S3 datasheet | Tra số |
| API `i2c_master_probe`, `i2c_master_transmit_receive` | `[tự đo]` ESP-IDF v5.x | Kiểm theo bản cài |

**Đã sửa:**
- Bản gốc (và Gemini) Bài 3, bảng "Nếu ra khác": "pull-up tổng quá mạnh → tháo bớt pull-up **hoặc giảm tốc độ bus**". Giảm tốc độ chỉ chữa cạnh lên chậm (Rp/Cb lớn), không chữa Rp quá nhỏ. Tách thành hai dòng. Với 3 module, Rp quá nhỏ ít khi xảy ra; nguyên nhân hay gặp hơn là trùng địa chỉ (hai IMU) hoặc cạnh chậm.
- Gemini: "đọc đúng ID chứng minh 4 điều kiện vật lý thông suốt" — đúng cho giao tiếp, nhưng bỏ qua việc ID không kiểm phần tử cảm biến; thêm chấm mô hình.
- Gemini tự kiểm tra: "AD0 lơ lửng → địa chỉ trôi ngẫu nhiên" — module GY-521 phổ biến thường có điện trở kéo AD0 xuống `[tự đo — xem mạch module]`, nên trên module thường không trôi; trên chip trần thì đúng là không được để lơ lửng.
- Thêm: địa chỉ thanh ghi 16-bit của VL53L1X, lẫn 7-bit/8-bit, hai IMU trùng địa chỉ, bus recovery.

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** NXP UM10204 *I²C-bus specification and user manual*; datasheet BME280 (Bosch BST-BME280-DS002), MPU-6000/6050 Product Specification + Register Map, ICM-42688-P (TDK DS-000347), VL53L1X (ST).
- **Giải thích:** NXP application note về bus I2C và điện trở kéo lên (tìm trên trang NXP theo từ khóa "I2C pull-up resistor" — kiểm tên tài liệu trước khi trích).
- **Đào sâu (tùy chọn):** ESP-IDF Programming Guide, mục I2C (bản đúng phiên bản bạn cài).
- **Tự kiểm tra:** (1) giải thích cho backend engineer khác trong 5 câu vì sao ACK không mang danh tính; (2) vẽ lại timing diagram ở phần 2; (3) câu hỏi:

*Bạn có bốn module, mỗi cái pull-up 4,7 kΩ, dây breadboard tổng Cb ≈ 120 pF. Ở 400 kHz (t_r ≤ 300 ns) và 3,3 V (V_OL 0,4 V, I_OL 3 mA), cấu hình này vi phạm giới hạn nào?*
<details><summary>Đáp án</summary>

Rp tương đương = 4,7/4 ≈ 1,18 kΩ > Rp_min ≈ 0,97 kΩ → chưa vi phạm dòng. Rp_max = 300 ns / (0,8473 × 120 pF) ≈ 2,95 kΩ → 1,18 kΩ < 2,95 kΩ → đạt. Cấu hình này ổn; thêm module thứ năm, thứ sáu sẽ tiến sát Rp_min.

</details>
