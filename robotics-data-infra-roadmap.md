# HỆ THỐNG KIẾN THỨC NỀN + ROADMAP
## Robotics Data Infrastructure Engineer — cho người đến từ backend

**Dùng cho:** full-stack/backend engineer 8 năm, chưa từng cầm que đo, đang ở Khóa 1.
**Mục đích của tài liệu này:** thay thế việc "đụng đâu google đấy" bằng một danh sách hữu hạn, có ngưỡng dừng.
**Không phải:** giáo trình điện tử. Là bản đồ để biết cái gì cần biết, cái gì chỉ cần biết tên, cái gì bỏ.

---

## CÁCH DÙNG

### Ba mức độ, dán vào đầu trước khi đọc bất cứ dòng nào

| Ký hiệu | Nghĩa | Kiểm chứng bằng |
|---|---|---|
| 🟢 **NẮM** | Phải giải thích được cho người khác, tính được bằng số, đo được | Làm được bài tập tương ứng |
| 🟡 **BIẾT TÊN** | Nghe thấy phải biết nó là gì và ở tầng nào. Không cần tự làm được | Đọc một đoạn kỹ thuật không bị đứng |
| 🔴 **BỎ** | Không học trong 24 tháng. Nếu cần thì tra lúc đó | — |

**Tỉ lệ mục tiêu:** khoảng 35% 🟢, 45% 🟡, 20% 🔴. Nếu bạn thấy mình đang học một thứ 🟡 tới mức làm bài tập, đó là rabbit hole — dừng lại.

### Quy tắc scanning (làm trước khi học sâu)

Đọc lướt toàn bộ Phần 1–3 trong **một buổi 2–3h**, không dừng lại để hiểu kỹ. Mục tiêu của buổi đó không phải hiểu, mà là **xây bản đồ tên gọi**. Sau buổi đó, khi gặp một từ trong datasheet hay tutorial, bạn sẽ biết nó nằm ở tầng nào và có cần quan tâm không. Đây chính là thứ bạn đang thiếu và gọi là "cảm giác hụt kiến thức" — không phải thiếu chiều sâu, mà thiếu bản đồ.

### Định dạng mỗi mục từ

> **Tên** — nó là gì · nó đại diện cho gì · số điển hình · sai lầm kinh điển

---

# PHẦN 1 — TỪ ĐIỂN ĐIỆN TỬ

Toàn bộ phần này phục vụ đúng một mục đích: **cắm que đo vào một điểm và biết số đó đúng hay sai**. Không phải để thiết kế mạch.

## 1.1 Bốn đại lượng và các định luật

| Mức | Thuật ngữ | Là gì / đại diện cho gì | Số điển hình | Sai lầm kinh điển |
|---|---|---|---|---|
| 🟢 | **Voltage (V, điện áp)** | Chênh lệch thế năng giữa **hai điểm**. Luôn là một phép trừ. | 3.3V, 5V, 12V | Nói "điện áp tại chân này" mà không nói so với đâu. Không có GND thì không có điện áp. |
| 🟢 | **Current (I, dòng điện)** | Lượng điện tích chảy qua **một mặt cắt** trong 1s. Đo bằng cách **cắt mạch và chen đồng hồ vào**. | LED 5–20mA, ESP32 ~80–240mA, servo stall 0.5–1A | Đo dòng bằng cách cắm song song → chập nguồn, đứt cầu chì đồng hồ |
| 🟢 | **Resistance (R, điện trở)** | Mức cản dòng. Đo **khi mạch đã ngắt điện**. | 220Ω, 1k, 4.7k, 10k | Đo điện trở khi mạch đang có điện → số vô nghĩa hoặc hỏng đồng hồ |
| 🟢 | **Power (P, công suất)** | `P = V × I`. Nhiệt tỏa ra. Quyết định linh kiện có cháy không. | Điện trở cắm board: 1/4W | Chọn điện trở đúng Ω nhưng sai W → nóng, trôi giá trị, cháy |
| 🟢 | **Ohm's law** | `V = I × R`. Ba biến, biết hai suy ra một. | — | Áp dụng cho LED. LED **không** tuân theo Ohm — nó là diode. |
| 🟢 | **GND / reference / mass** | Điểm gốc quy ước = 0V. | — | Hai thiết bị không chung GND thì mọi phép đo giữa chúng đều rác. **Nguyên nhân số 1 của "số lạ".** |
| 🟢 | **Series / parallel (nối tiếp / song song)** | Nối tiếp: cùng dòng, chia áp. Song song: cùng áp, chia dòng. | — | Nhầm hai cái khi đọc sơ đồ |
| 🟢 | **Voltage divider (cầu phân áp)** | `Vout = Vin × R2/(R1+R2)`. Hạ áp tín hiệu. | 5V → 3.3V dùng 1k/2k | Dùng để hạ áp **nguồn**. Sai — nó sụp ngay khi có tải. Chỉ dùng cho tín hiệu. |
| 🟡 | **Kirchhoff (KCL/KVL)** | Tổng dòng vào nút = tổng dòng ra. Tổng áp quanh vòng kín = 0. | — | — |
| 🟡 | **Short circuit / open circuit** | Chập (R≈0) / hở (R≈∞) | — | — |
| 🟡 | **DC / AC** | Một chiều / xoay chiều | — | — |
| 🔴 | **RMS, phasor, trở kháng phức, Thevenin/Norton** | Phân tích mạch AC | — | Không cần cho tầng này |

## 1.2 Linh kiện thụ động

| Mức | Thuật ngữ | Là gì / dùng khi nào | Số điển hình | Sai lầm kinh điển |
|---|---|---|---|---|
| 🟢 | **Resistor** | Hạn dòng, phân áp, pull-up | Mã màu 4/5 vạch; sai số ±1% (nâu) hoặc ±5% (vàng kim) | Đọc mã màu ngược chiều. Quy tắc: vạch sai số (vàng kim/nâu) nằm cách xa các vạch kia hơn. |
| 🟢 | **LED** | Diode phát sáng. Có **V_f** (forward voltage), không phải điện trở. | V_f đỏ ~1.8–2.2V, xanh dương/trắng ~3.0–3.4V; I ~5–20mA | Cắm thẳng vào 5V không điện trở → cháy. Và: V_f **không phải hằng số**, nó tăng theo dòng — đây là lý do phép đo lệch ~10% so với tính toán. |
| 🟢 | **Capacitor (tụ)** | Kho điện nhỏ, đáp ứng nhanh. Hai vai trò bạn sẽ gặp: **decoupling** (100nF sát chân IC, dập nhiễu tần cao) và **bulk** (10–100µF, gánh dòng đỉnh) | 100nF ceramic + 10µF | Không có tụ decoupling → MCU reset ngẫu nhiên khi servo/wifi bật. Rất khó debug nếu không biết trước. |
| 🟡 | **Electrolytic vs ceramic** | Điện phân có cực (cắm ngược → nổ), gốm không cực | — | Cắm ngược tụ điện phân |
| 🟡 | **Diode** | Van một chiều. Chống cắm ngược nguồn, chống dòng ngược khi tắt motor (flyback) | V_f silicon ~0.7V, Schottky ~0.3V | — |
| 🟡 | **Inductor (cuộn cảm)** | Cản thay đổi dòng. Có trong mạch buck/boost | — | — |
| 🟡 | **Potentiometer (biến trở)** | Cầu phân áp xoay được | 10k | — |
| 🔴 | **Transistor bias, op-amp, mạch tương tự** | Khuếch đại, lọc analog | — | Bỏ. Nếu cần khuếch đại mic thì **mua module** đã có sẵn. |

## 1.3 Nguồn — nơi 70% lỗi phần cứng của người mới nằm ở đây

| Mức | Thuật ngữ | Là gì | Số điển hình | Sai lầm kinh điển |
|---|---|---|---|---|
| 🟢 | **Common ground** | Mọi thứ trong hệ phải nối chung GND | — | Logic analyzer không nối GND vào mạch → waveform rác. **Lỗi số 1 khi dùng logic analyzer lần đầu.** |
| 🟢 | **Brownout** | Điện áp tụt dưới ngưỡng → MCU tự reset | ESP32 brownout ~2.8V | Servo/motor quay → sụt áp → MCU reset. Bạn tưởng code lỗi. Không phải, là nguồn. |
| 🟢 | **Current budget** | Tổng dòng tải phải nhỏ hơn khả năng cấp của nguồn | USB 2.0 port: 500mA. Pi 5 cần 5V/5A. | Cấp Pi 5 bằng sạc điện thoại → chạy được vài phút rồi treo |
| 🟢 | **Decoupling** | Tụ đặt sát chân nguồn IC | 100nF + 10µF | Xem 1.2 |
| 🟡 | **LDO regulator** | Hạ áp tuyến tính (5V→3.3V). Đơn giản, phần dư biến thành nhiệt. | AMS1117 | — |
| 🟡 | **Buck / boost converter** | Hạ/nâng áp kiểu switching. Hiệu suất cao, có nhiễu switching. | — | — |
| 🟡 | **Inrush current** | Dòng vọt lúc khởi động | — | — |
| 🟡 | **Ground loop** | Hai đường GND khác trở kháng → chênh thế → nhiễu | — | Thường gặp khi audio + nguồn chung |
| 🟡 | **Absolute maximum ratings** | Ngưỡng trong datasheet, vượt là hỏng vĩnh viễn | — | Nhầm "absolute max" với "recommended operating". Chúng khác nhau và đều nằm trong datasheet. |

## 1.4 Tín hiệu số — cầu nối sang phần mềm

| Mức | Thuật ngữ | Là gì / đại diện cho gì | Số điển hình | Sai lầm kinh điển |
|---|---|---|---|---|
| 🟢 | **Logic level** | Ngưỡng áp quy ước 0/1 | 3.3V logic: V_IH ≥ ~2.0V là "1", V_IL ≤ ~0.8V là "0" | Cắm tín hiệu 5V vào chân 3.3V → hỏng chân. ESP32, Pi đều **3.3V**, Arduino Uno là **5V**. Đây là bẫy lớn nhất khi trộn hai board. |
| 🟢 | **Level shifter** | Mạch chuyển 5V ↔ 3.3V | — | Nối thẳng Uno (5V) vào ESP32/Pi (3.3V) |
| 🟢 | **Pull-up / pull-down** | Điện trở ghim mức mặc định khi không ai lái | I2C: 4.7k (dải 2.2k–10k) | Thiếu pull-up trên I2C → bus im lìm, scanner không thấy gì |
| 🟢 | **Floating pin** | Chân không nối gì → đọc ra giá trị ngẫu nhiên | — | Nút bấm không có pull-up/down → đọc loạn |
| 🟢 | **Open-drain** | Thiết bị chỉ kéo được xuống thấp, không đẩy lên cao. Đây là lý do I2C **cần** pull-up. | — | — |
| 🟢 | **Debounce** | Nút bấm cơ tạo ra hàng chục xung nhiễu trong ~1–20ms | 5–50ms | Đếm 1 lần bấm thành 7 lần |
| 🟢 | **Clock, chu kỳ, tần số** | `f = 1/T`. Trên logic analyzer bạn đo T rồi suy ra f. | I2C 100kHz → T = 10µs | — |
| 🟡 | **Rise/fall time** | Thời gian chuyển mức. Pull-up quá lớn → cạnh bo tròn → lỗi ở tốc độ cao. | — | — |
| 🟡 | **Duty cycle / PWM** | Tỉ lệ thời gian mức cao. Dùng điều khiển servo, độ sáng, motor. | Servo: xung 1–2ms trong chu kỳ 20ms | — |
| 🟡 | **Noise margin, crosstalk, signal integrity** | Biên an toàn, nhiễu xuyên kênh | — | — |
| 🟡 | **Baud rate** | Tốc độ bit của UART | 115200 → 1 bit ≈ 8.68µs | Sai baud → Serial Monitor ra ký tự rác. Triệu chứng rất đặc trưng. |

## 1.5 Đo lường — phần quan trọng nhất với bạn

| Mức | Thuật ngữ | Là gì | Số điển hình / lưu ý | Sai lầm kinh điển |
|---|---|---|---|---|
| 🟢 | **Multimeter (DMM)** | Đo V (song song), I (nối tiếp), R (ngắt điện), continuity | — | Để nguyên que ở cổng đo dòng rồi đi đo áp → chập |
| 🟢 | **Continuity test** | Kiểm tra thông mạch, kêu bíp | Dây tốt < 1Ω | Bỏ qua bước này rồi debug 2 tiếng vì một dây jumper đứt ngầm. **Luôn test dây trước.** |
| 🟢 | **Logic analyzer** | Ghi lại mức 0/1 của nhiều kênh theo thời gian, có decoder giao thức | Sample rate ≥ **4–10×** tần số tín hiệu | Sample rate quá thấp → bỏ sót cạnh, decode sai. Và: quên nối GND. |
| 🟢 | **Sampling rate & Nyquist** | Muốn tái tạo tín hiệu f, phải lấy mẫu > 2f. Thực tế digital cần 4–10f. | I2C 100kHz → capture ở 4MHz | — |
| 🟢 | **Aliasing** | Lấy mẫu quá thưa → tín hiệu giả xuất hiện | — | Nhìn thấy tần số không có thật |
| 🟢 | **Sai số của phép đo** | Bản thân dụng cụ có sai số. Phải ghi vào lab notebook. | DMM rẻ: ±(0.5% + 2 digit) | Ghi "đo được 3.2847V" từ đồng hồ chỉ chính xác tới ±0.02V → giả vờ chính xác |
| 🟢 | **Resolution vs accuracy** | Số chữ số hiển thị ≠ độ đúng | — | Xem trên |
| 🟡 | **Burden voltage** | Đồng hồ đo dòng tự làm sụt áp một chút | — | — |
| 🟡 | **Probe loading** | Que đo tự thay đổi mạch khi cắm vào | — | — |
| 🟡 | **Oscilloscope** | Đo dạng sóng **tương tự** theo thời gian. Logic analyzer chỉ thấy 0/1; scope thấy hình dạng thật. | — | Chưa cần mua. Khi nào cần nhìn rise time hay nhiễu analog mới cần. |

**Ba câu hỏi tự kiểm tra mọi phép đo** (đã có trong Khóa 1, nhắc lại vì đây là thứ thay thế trực giác):
1. Số này có nằm trong khoảng vật lý hợp lý không?
2. Đo bằng cách khác có ra cùng số không?
3. Có khớp với tính toán từ nguyên lý đầu không?

---

# PHẦN 2 — TỪ ĐIỂN NHÚNG

## 2.1 Bộ não

| Mức | Thuật ngữ | Là gì | Ghi chú cho người từ backend |
|---|---|---|---|
| 🟢 | **MCU vs MPU/SoC** | MCU (ESP32, STM32): không OS hoặc RTOS, chạy một firmware, deterministic. MPU/SoC (Pi 5, Jetson): chạy Linux, có scheduler, **không deterministic**. | Đây là ranh giới quan trọng nhất trong toàn bộ tài liệu. Robot thật luôn có cả hai: MCU lo control loop cứng, Linux lo perception/data. Bạn sẽ sống ở phía Linux. |
| 🟢 | **GPIO** | Chân vào/ra số | Dòng tối đa mỗi chân ~20–40mA. Không lái motor trực tiếp. |
| 🟢 | **ADC** | Analog → số. Có **resolution** (bit) và **Vref**. | 12-bit, Vref 3.3V → 1 LSB = 3.3/4096 ≈ 0.8mV. Đây là giới hạn vật lý của phép đo, không phải bug. |
| 🟢 | **DAC** | Số → analog | Chuỗi audio của Khóa 3 chính là cái này |
| 🟢 | **Interrupt / ISR** | Ngắt: dừng việc đang làm để xử lý sự kiện | Tương tự event handler, nhưng ISR **phải cực ngắn**, không được alloc, không được blocking I/O. Vi phạm → jitter. |
| 🟢 | **Timer** | Bộ đếm phần cứng. Nguồn của mọi thứ đúng giờ. | Nếu timestamp lấy từ phần mềm thay vì timer/hardware, sai số của bạn là sai số của scheduler |
| 🟢 | **Flash vs RAM vs NVS/EEPROM** | Chương trình / biến chạy / lưu cấu hình | ESP32-S3: ~512KB RAM. Buffer 1MB là không khả thi. |
| 🟡 | **DMA** | Chuyển dữ liệu không qua CPU | Lý do I2S có thể stream audio liên tục mà CPU vẫn rảnh |
| 🟡 | **Watchdog** | Đếm ngược, không được "vỗ" thì reset board | — |
| 🟡 | **Bootloader, flashing, toolchain, cross-compile** | Nạp code | — |
| 🟡 | **JTAG / SWD** | Debug phần cứng | Chưa cần. `printf` qua serial là đủ lâu. |

## 2.2 Bus — phần bạn sẽ đo bằng logic analyzer

| Mức | Bus | Số dây | Đặc điểm | Số phải thấy trên logic analyzer |
|---|---|---|---|---|
| 🟢 | **UART** | 2 (TX, RX) | Không có clock chung, hai bên phải thỏa thuận baud trước | 115200 8N1 → mỗi bit 8.68µs, khung 10 bit |
| 🟢 | **I2C** | 2 (SDA, SCL) | Có địa chỉ, nhiều thiết bị chung bus, open-drain + pull-up | START → 7-bit addr + R/W → **ACK** → data → STOP. SCL 100kHz → T=10µs |
| 🟢 | **SPI** | 4 (MOSI, MISO, SCK, CS) | Nhanh, full-duplex, mỗi thiết bị một chân CS | Mode 0–3 = tổ hợp (CPOL, CPHA). Sai mode → đọc ra rác nhưng không báo lỗi. |
| 🟢 | **I2S** | 3 (BCLK, LRCK/WS, SD) | Chuyên audio. LRCK **chính là sample rate**. | 48kHz, 32-bit, stereo → BCLK = 48000×32×2 = 3.072MHz |
| 🟡 | **CAN / CAN-FD** | 2 (differential) | Bus chuẩn của ô tô và robot công nghiệp. Có arbitration, chống nhiễu tốt. | Đáng biết tên vì nó xuất hiện nhiều trong JD robotics |
| 🟡 | **Ethernet / PoE / TSN** | — | TSN (Time-Sensitive Networking) là Ethernet có bảo đảm thời gian — liên quan trực tiếp tới nghề bạn nhắm | — |
| 🟡 | **USB** | — | Phức tạp, không tự implement | — |

**Bảng so sánh để dịch sang thứ bạn đã biết:**

| Bus | Tương tự trong backend |
|---|---|
| UART | TCP socket không có handshake, hai bên phải cùng cấu hình |
| I2C | HTTP có routing: địa chỉ = URL, ACK = 200, NACK = 404 |
| SPI | Kết nối point-to-point tốc độ cao, CS = chọn peer |
| Pub/sub (ROS) | Kafka topic |

## 2.3 Đọc datasheet — kỹ năng có ROI cao nhất trong phần nhúng

Một datasheet luôn có các mục này. Biết đọc theo thứ tự là toàn bộ kỹ năng:

| Mục | Nội dung | Đọc để làm gì |
|---|---|---|
| **Features / Description** | Tóm tắt | Lướt |
| **Pin configuration** | Sơ đồ chân | Đấu dây |
| 🟢 **Absolute Maximum Ratings** | Ngưỡng gây hỏng vĩnh viễn | **Đọc đầu tiên.** Để không đốt linh kiện |
| 🟢 **Recommended Operating Conditions** | Dải hoạt động bình thường | Khác với mục trên. Thiết kế theo mục này |
| 🟢 **Electrical Characteristics** | Bảng min/typ/max | Thiết kế theo **max**, đừng theo typ |
| 🟢 **Timing Diagram** | Biểu đồ thời gian, có t_setup, t_hold | Đây là thứ bạn đối chiếu với capture của logic analyzer |
| 🟢 **Register Map** | Bảng thanh ghi, địa chỉ + ý nghĩa từng bit | Đây là "API reference" của con chip |
| 🟡 **Errata** | Lỗi đã biết của chip, thường ở file riêng | Khi có thứ vô lý xảy ra, đọc errata trước khi nghi ngờ bản thân |

**Quy tắc:** typ = giá trị đẹp trong phòng lab. max = giá trị bạn phải sống chung. Người mới thiết kế theo typ rồi ngạc nhiên.

## 2.4 Real-time — ranh giới thật giữa bạn và robotics

Đây là phần lộ trình gọi là "thứ đầu tiên nên học lại, không phải điện trở". Với 8 năm backend, bạn biết cột trái. Cột phải là cái phải học.

| Mức | Thuật ngữ | Là gì | Vì sao khác với backend |
|---|---|---|---|
| 🟢 | **Latency vs Throughput** | Độ trễ một request vs số request/giây | Bạn đã biết |
| 🟢 | **Jitter** | **Phương sai** của latency | Trong backend p99 30ms là tốt. Trong control loop 1kHz, một lần jitter 5ms có thể làm robot mất ổn định. Jitter quan trọng hơn latency trung bình. |
| 🟢 | **Determinism** | Cùng đầu vào → cùng thời gian thực thi, mọi lần | Backend tối ưu throughput trung bình. Real-time tối ưu **worst case**. Hai mục tiêu ngược nhau. |
| 🟢 | **Hard vs soft real-time** | Hard: trễ deadline = hệ thống sai. Soft: trễ = giảm chất lượng | Control loop = hard. Logging = soft. |
| 🟢 | **Control loop rate** | Tần số vòng điều khiển | 100Hz–1kHz điển hình. 1kHz → mỗi chu kỳ 1ms, ngân sách jitter thường <100µs |
| 🟢 | **Backpressure** | Khi consumer chậm hơn producer | Bạn đã biết. Nhưng trong robot, drop message ≠ chậm — nó có thể là mất một frame cảm biến vĩnh viễn. |
| 🟡 | **WCET** (Worst-Case Execution Time) | Thời gian tệ nhất có thể | Khái niệm trung tâm của real-time |
| 🟡 | **RTOS, preemptive scheduling, priority inversion** | Hệ điều hành thời gian thực | Biết tên. FreeRTOS chạy sẵn trong ESP32. |
| 🟡 | **PREEMPT_RT** | Patch làm Linux gần real-time hơn | Xuất hiện trong JD robotics khá nhiều |
| 🔴 | **Rate-monotonic analysis, schedulability proof** | Toán chứng minh lịch khả thi | Bỏ |

---

# PHẦN 3 — TỪ ĐIỂN DỮ LIỆU ROBOT

**Đây là phần bạn sẽ sống trong đó.** Nếu phải chọn một phần để học kỹ nhất trong cả tài liệu, là phần này — và nó gần như không cần điện tử.

## 3.1 Thời gian — bài toán trung tâm của robot data

| Mức | Thuật ngữ | Là gì | Số / lưu ý |
|---|---|---|---|
| 🟢 | **Wall clock vs monotonic clock** | Wall (UTC, có thể nhảy khi NTP sync) vs monotonic (chỉ tăng, không nhảy) | Dùng wall để timestamp dữ liệu, monotonic để đo khoảng thời gian. Nhầm hai cái → timestamp âm, duration âm. |
| 🟢 | **Epoch, ns vs µs vs ms** | Gốc thời gian và đơn vị | Robotics mặc định **nanosecond từ UNIX epoch**. `int64` ns hết tràn năm 2262. `float64` giây **mất độ chính xác** — chỉ còn ~µs ở thời điểm hiện tại. Đây là lỗi thật, gặp nhiều. |
| 🟢 | **Clock drift / skew** | Hai đồng hồ chạy lệch nhau dần | Thạch anh thường 20–50 ppm → 20–50µs lệch mỗi giây → **72–180ms mỗi giờ**. Đây là lý do phải sync. |
| 🟢 | **Timestamp at source vs at receive** | Đóng dấu lúc cảm biến lấy mẫu hay lúc máy chủ nhận | Khác nhau bằng đúng latency của đường truyền. Dataset không ghi rõ dùng cái nào = dataset không dùng được cho fusion. **Đây là một lớp lỗi trong audit tool của bạn.** |
| 🟢 | **NTP** | Sync qua mạng | Độ chính xác ~1–10ms trong LAN. **Không đủ** cho sensor fusion. |
| 🟢 | **PTP (IEEE 1588) / gPTP** | Sync có hỗ trợ phần cứng | Sub-microsecond. Đây là cái robot dùng. Cần NIC hỗ trợ hardware timestamping. |
| 🟢 | **Hardware trigger** | Một xung điện kích nhiều cảm biến cùng lúc | Cách duy nhất để hai camera chụp *thực sự* cùng thời điểm. Phần mềm không làm được. |
| 🟢 | **Time sync error budget** | Ngân sách sai số thời gian toàn hệ | Viết ra thành bảng, cộng từng nguồn sai số. Kỹ năng này y hệt latency budget bạn đã làm. |
| 🟡 | **Leap second, TAI vs UTC** | — | Biết là có tồn tại |

## 3.2 Tín hiệu, số, và sự thật về cảm biến

| Mức | Thuật ngữ | Là gì | Lưu ý |
|---|---|---|---|
| 🟢 | **Sampling rate** | Số mẫu/giây | IMU 100–1000Hz, camera 30–60fps, LiDAR 10–20Hz. Ba tốc độ khác nhau = bài toán đồng bộ. |
| 🟢 | **Quantization** | Rời rạc hóa giá trị | ADC 12-bit → sai số lượng tử ±0.5 LSB. Không thể nhỏ hơn. |
| 🟢 | **Noise** | Nhiễu ngẫu nhiên | IMU đứng yên vẫn có nhiễu ~0.02 m/s². Nếu dữ liệu **không** có nhiễu, hãy nghi ngờ — có thể kênh bị đơ. |
| 🟢 | **Bias** | Sai lệch hệ thống, không ngẫu nhiên | Gyro đứng yên đọc ra 0.01 rad/s thay vì 0. Tích phân bias → drift. |
| 🟢 | **Drift** | Sai số tích lũy theo thời gian | Lý do IMU đơn thuần không định vị được |
| 🟢 | **Frozen channel** | Cảm biến trả về đúng một giá trị lặp lại | Dấu hiệu hỏng phổ biến nhất và dễ bỏ sót nhất. Một lớp lỗi trong audit tool. |
| 🟢 | **Calibration** | Hiệu chuẩn. **Intrinsic** = tham số nội tại (tiêu cự, méo ống kính). **Extrinsic** = vị trí/hướng giữa các cảm biến. | Dữ liệu không kèm calibration state = dữ liệu không dùng được. Nguyên tắc số 5 của lộ trình. |
| 🟢 | **Units & SI** | Đơn vị | Mars Climate Orbiter cháy vì lẫn đơn vị. Trường `unit` phải nằm trong schema. |
| 🟢 | **Uncertainty / covariance** | Độ không chắc chắn của một phép đo | Đây là trường dữ liệu hạng nhất phân biệt bạn với backend engineer thường |
| 🟡 | **Low-pass filter, moving average** | Lọc nhiễu | — |
| 🟡 | **Kalman filter / EKF** | Hợp nhất nhiều cảm biến có nhiễu | **Biết nó làm gì và cần đầu vào gì** (covariance, timestamp đồng bộ). Không cần tự cài đặt. |
| 🟡 | **Rolling shutter vs global shutter** | Cách camera đọc pixel | Rolling shutter → mỗi dòng ảnh có timestamp khác nhau. Quan trọng khi fusion. |
| 🟡 | **Exposure time, gain** | Tham số camera | — |

## 3.3 Cảm biến — biết chúng sinh ra dữ liệu gì

| Mức | Cảm biến | Sinh ra gì | Tốc độ | Vấn đề dữ liệu đặc trưng |
|---|---|---|---|---|
| 🟢 | **IMU** (accel + gyro [+ mag]) | 6–9 số float/mẫu | 100–1000Hz | Bias, drift, cần timestamp chính xác |
| 🟢 | **Camera RGB** | Ảnh/video | 30–60fps | Nén, frame drop, số frame video ≠ số dòng metadata |
| 🟢 | **Encoder** | Vị trí/vòng quay của khớp | 100Hz–1kHz | Wrap-around, quantization |
| 🟡 | **Depth camera** (RealSense, ToF) | Ảnh + độ sâu | 30fps | Cần căn chỉnh với RGB |
| 🟡 | **LiDAR** | Point cloud | 10–20Hz | Dữ liệu lớn, mỗi điểm có timestamp riêng |
| 🟡 | **Force/torque sensor** | 6 số | Cao | — |
| 🟡 | **GNSS/GPS** | Vị trí + thời gian | 1–10Hz | Là nguồn thời gian tốt (PPS) |

## 3.4 Tầng dữ liệu — chỗ bạn có lợi thế sẵn

| Mức | Thuật ngữ | Là gì | Tương tự trong backend |
|---|---|---|---|
| 🟢 | **Pub/sub, topic, message** | Mô hình giao tiếp của ROS | Kafka |
| 🟢 | **Schema** | Định nghĩa cấu trúc message | Protobuf/Avro schema — bạn đã biết |
| 🟢 | **Serialization: Protobuf / CDR / JSON** | Cách mã hóa message. ROS 2 dùng **CDR** trên dây. | — |
| 🟢 | **MCAP** | Container file cho log robot. Tự chứa schema, append-only, có index. | Giống một segment file của Kafka nhưng có index + schema nhúng |
| 🟢 | **Chunk / index / summary** | Cấu trúc bên trong MCAP cho phép random access | Lý do đọc 10 giây giữa file 50GB không cần scan cả file |
| 🟢 | **rosbag** | Định dạng log cũ của ROS. ROS 2 từ bản Iron trở đi ghi MCAP mặc định. | — |
| 🟢 | **Parquet** | Định dạng cột. LeRobot dùng cho state/action. | Bạn đã biết |
| 🟢 | **Schema evolution / backward compatibility** | Đổi schema mà reader cũ vẫn đọc được | Bạn đã biết. Đây là lợi thế. |
| 🟢 | **Provenance / lineage** | Dữ liệu này đến từ đâu, qua những bước xử lý nào | Nguyên tắc số 5 |
| 🟢 | **Data contract** | Cam kết giữa bên sinh và bên dùng dữ liệu | — |
| 🟢 | **Frame / TF tree** | Mỗi phép đo gắn với một hệ tọa độ (`base_link`, `camera_optical_frame`...). TF là cây biến đổi giữa chúng. | Giống một cây phụ thuộc, nhưng có thời gian: transform tại t≠ transform tại t' |
| 🟡 | **QoS (ROS 2)** | Chính sách độ tin cậy: reliable/best-effort, durability, deadline | Gần với cấu hình Kafka producer |
| 🟡 | **DDS** | Middleware dưới ROS 2 | Biết tên |
| 🟡 | **Lossless vs lossy compression** | — | Video robot thường nén lossy → không dùng để training được nếu nén quá tay |

## 3.5 Toán vừa đủ

| Mức | Chủ đề | Cần tới mức nào |
|---|---|---|
| 🟢 | **Thống kê mô tả** | mean, std, percentile, histogram. Đủ để viết report của audit tool. |
| 🟢 | **Vector, hệ tọa độ** | Hiểu 3 trục, quy tắc bàn tay phải |
| 🟢 | **Nội suy (interpolation)** | Hai stream khác tần số → phải nội suy về cùng mốc thời gian. Đây là code bạn sẽ viết. |
| 🟡 | **Ma trận xoay, homogeneous transform 4×4** | Hiểu nó biểu diễn gì, nhân theo thứ tự nào |
| 🟡 | **Quaternion** | Biết vì sao dùng nó thay Euler (gimbal lock), biết SLERP là nội suy quaternion |
| 🟡 | **Đại số tuyến tính cơ bản** | Nhân ma trận, nghịch đảo |
| 🔴 | **Lie groups, SE(3) manifold optimization** | Bỏ |
| 🔴 | **Kinematics, dynamics, MPC, control theory** | Bỏ. Chỉ đủ từ vựng. |

---

# PHẦN 4 — ROADMAP

Không có roadmap.sh cho mảng này. Các roadmap robotics công khai đều đi hướng robotics engineer (kinematics → control → planning → RL). Đây là bản đồ cho **tầng dữ liệu**, dựng theo cùng định dạng.

## Bản đồ tổng

```
                        ┌─────────────────────────┐
                        │  L0 · NỀN ĐO LƯỜNG      │  35h · Khóa 1
                        │  điện tử vừa đủ         │  → mở L3, L5
                        └───────────┬─────────────┘
                                    │
   ┌────────────────────────────────┼────────────────────────────────┐
   │                                │                                │
┌──┴──────────────────┐   ┌─────────┴───────────┐   ┌────────────────┴─────┐
│ L1 · ĐỊNH DẠNG      │   │ L3 · ROS 2 &        │   │  TRACK NGANG         │
│ DỮ LIỆU ROBOT       │   │ HỆ PHÂN TÁN RT      │   │  Viết · Publish ·    │
│ 20h · không HW ★rẻ  │   │ 40h · song song     │   │  Cộng đồng · Apply   │
└──┬──────────────────┘   └─────────┬───────────┘   │  chạy suốt 24 tháng  │
   │                                │               └──────────────────────┘
┌──┴──────────────────┐             │
│ L2 · CHẤT LƯỢNG     │             │
│ DỮ LIỆU ★ARTIFACT   │◄────────────┘
│ 60h · không HW      │
└──┬──────────────────┘
   │
   ├──────────────────────────┬──────────────────────────┐
┌──┴──────────────────┐  ┌────┴────────────────┐  ┌──────┴──────────────┐
│ L4 · EDGE INFERENCE │  │ L5 · SENSOR +       │  │ L6 · ROBOT LEARNING │
│ ★ARTIFACT           │  │ TIME SYNC ★ARTIFACT │  │ (tùy chọn)          │
│ 70h · thuê GPU      │  │ 150h · cần HW       │  │ 120h · cần SO-101   │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

**Đường đi ngắn nhất tới tín hiệu thị trường đầu tiên:** L1 → L2 → publish. Khoảng 80h, **không cần phần cứng, không cần tiền**. Đây là đường bạn nên chạy song song ngay từ tuần này.

---

## L0 — NỀN ĐO LƯỜNG · 35h

**Mục tiêu:** cắm que đo vào một tín hiệu và biết vấn đề nằm trên hay dưới mình.
**Trạng thái của bạn:** ~80% xong. Còn phần logic analyzer.

```
L0
├── 🟢 Bốn đại lượng · Ohm's law · GND                    [Phần 1.1]
├── 🟢 Cầu phân áp — dự đoán trước, đo sau, lệch <5%
├── 🟢 LED + điện trở — lệch <10%, giải thích được vì sao lệch
├── 🟢 Multimeter — V song song, I nối tiếp, R ngắt điện  [Phần 1.5]
├── 🟢 Breadboard — test thông mạch TRƯỚC khi tin nó
├── 🟢 Mức logic 3.3V vs 5V · pull-up · open-drain        [Phần 1.4]
├── 🟢 Đọc trọn một datasheet — viết tay register map     [Phần 2.3]
├── 🟢 Logic analyzer + PulseView                          ← BẠN ĐANG Ở ĐÂY
│   ├── nối GND (lỗi số 1)
│   ├── sample rate ≥ 4× tần số tín hiệu
│   ├── decoder I2C → nhìn thấy START / addr / ACK / STOP
│   └── đo chu kỳ SCL → tính ngược ra 100kHz
└── 🟢 I2S → tính ngược sample rate từ LRCK, lệch <1%
```

**GATE L0 (= M1 PASS):** 5 tiêu chí trong Khóa 1. Tất cả đều là số hoặc file, không chấm bằng cảm giác.

**Bài tập bổ sung dùng bộ kit Arduino** — chỉ 4 cái này, không làm hết kit:

| Linh kiện | Bài tập | Học được gì |
|---|---|---|
| LCD1602 + module I2C | Cắm logic analyzer, decode I2C, tìm địa chỉ (thường 0x27 hoặc 0x3F) | Đúng GATE L0 mục 1 |
| DHT11 | **Không có decoder sẵn.** Đọc timing diagram trong datasheet, tự giải mã bit từ độ rộng xung | Bài tập giá trị nhất trong kit. Đây là kỹ năng thật. |
| Servo SG90 | Đo áp nguồn khi servo đứng yên vs khi quay. Dự đoán mức sụt trước. | Brownout — hiểu tại sao "code lỗi" thực ra là nguồn |
| Biến trở + ADC | Xoay biến trở, đọc ADC, vẽ đồ thị áp vs giá trị ADC | Quan hệ analog ↔ số, sai số lượng tử |

Còn lại của kit: **bỏ**. Không có bài học mới.

---

## L1 — ĐỊNH DẠNG DỮ LIỆU ROBOT · 20h · không cần phần cứng

**Mục tiêu:** đóng ba gap có tên riêng trong JD với chi phí ~0đ.
**Đây là milestone có tỉ lệ đổi-giờ-lấy-tín-hiệu cao nhất toàn lộ trình. Bắt đầu ngay, không chờ L0.**

```
L1
├── 🟢 Robot sinh ra dữ liệu gì — nhiều stream, khác tần số  [Phần 3.3]
├── 🟢 Timestamp trong robotics                              [Phần 3.1]
│   ├── monotonic vs wall clock
│   ├── int64 ns vs float64 s  ← float64 mất độ chính xác
│   ├── timestamp at source vs at receive
│   └── clock drift 20–50ppm
├── 🟢 Frame & TF tree — mọi phép đo gắn một hệ tọa độ
├── 🟢 Protobuf schema cho message cảm biến
│   └── BẮT BUỘC có: timestamp · frame_id · unit · uncertainty · calibration_id
├── 🟢 MCAP
│   ├── cấu trúc: header · schema · channel · chunk · index · summary
│   ├── viết file MCAP đầu tiên từ dữ liệu tổng hợp
│   ├── random access: đọc 10s giữa file mà không scan hết
│   └── cắt cụt file → điều gì xảy ra, recover được không
├── 🟢 Schema versioning — v1 → v2, reader cũ vẫn đọc được
└── 🟢 Foxglove + Rerun — mở file, biết khi nào dùng cái nào
```

**GATE L1:** repo public đọc ≥2 dataset công khai → ghi MCAP hợp lệ có schema versioned · test chứng minh v1→v2 backward compatible · file mở được trong Foxglove, có ảnh trong README · README trả lời được: chunk index làm gì, vì sao nó quan trọng với file 50GB, chuyện gì xảy ra nếu process bị kill giữa lúc ghi.

---

## L2 — CHẤT LƯỢNG DỮ LIỆU ★ · 60h · không cần phần cứng

**Mục tiêu:** artifact công khai đầu tiên. Chưa ai làm tốt việc này — đó là chỗ nổi bật.

```
L2
├── 🟢 LeRobotDataset format
│   ├── v3.0: parquet theo chunk + mp4 hợp nhất + meta/episodes
│   ├── episode · observation · state · action
│   └── ⚠️ v2.1 → v3.0 đã đổi cấu trúc. Tool phải xử lý được cả hai,
│       hoặc nêu rõ hỗ trợ bản nào. Đây cũng là một nguồn lỗi thật.
├── 🟢 Kiểm tra bằng tay TRƯỚC khi tự động hóa
├── 🟢 Các lớp lỗi — mỗi lớp cần một định nghĩa toán học
│   ├── L1 timestamp không đơn điệu
│   ├── L2 frame drop & jitter (so với kỳ vọng 1/fps)
│   ├── L3 số frame video ≠ số dòng parquet
│   ├── L4 frozen channel (phương sai = 0 quá lâu)
│   ├── L5 lệch pha giữa hai stream
│   ├── L6 outlier độ dài episode
│   └── L7 desync action/state
├── 🟢 Mỗi detector kèm một test case tổng hợp (tự tạo dữ liệu hỏng)
├── 🟢 Report generator — HTML/markdown, có biểu đồ phân bố
└── 🟢 Tìm lỗi THẬT → script reproduce tối giản → báo cáo ra ngoài
```

**GATE L2:** chạy ≥5 dataset công khai bằng một lệnh · ≥4 lớp lỗi có test case · tìm được ≥1 lỗi thật có script reproduce · đã báo cáo ra ngoài · trong 60 ngày có ≥1 phản hồi có nội dung từ maintainer/người dùng HOẶC ≥10 star.

Tiêu chí cuối do người ngoài chấm. Đó là định nghĩa của không-cảm-tính.

---

## L3 — ROS 2 & HỆ PHÂN TÁN REAL-TIME · 40h · chạy song song từ sau L1

**Mục tiêu:** đủ từ vựng và trực giác để nói chuyện với roboticist mà không bị lộ là người ngoài.

```
L3
├── 🟢 node · topic · service · action · parameter
├── 🟢 ros2 bag record/play → ra MCAP (mặc định từ bản Iron)
├── 🟢 QoS: reliable vs best-effort · durability · deadline · liveliness
│   └── dịch sang thứ bạn biết: gần với cấu hình producer của Kafka
├── 🟢 tf2 — cây biến đổi, lookup theo thời gian, vì sao lookup sai thời điểm là bug
├── 🟢 Determinism vs throughput                              [Phần 2.4]
│   ├── đo jitter của một node đơn giản
│   ├── control loop 1kHz → ngân sách jitter
│   └── vì sao p99 không phải chỉ số đúng ở đây
├── 🟡 DDS, RMW, discovery
├── 🟡 launch file, colcon, workspace
└── 🟡 rosbag2 storage plugin
```

**Chọn bản nào:** Jazzy Jalisco (LTS, hỗ trợ tới 5/2029, nhiều package và tutorial nhất) hoặc Lyrical Luth (LTS mới ra 5/2026). Với người mới, Jazzy an toàn hơn vì hệ sinh thái đã đầy đủ. Chạy trong Docker để không phá máy chính.

**GATE L3:** dựng được một hệ 3 node publish/subscribe, ghi ra MCAP, mở trong Foxglove · đo và ghi lại được phân bố jitter của một topic · giải thích được bằng chữ vì sao đổi QoS làm thay đổi hành vi khi mạng nghẽn.

---

## L4 — EDGE INFERENCE & BENCHMARK ★ · 70h · thuê GPU

```
L4
├── 🟢 Benchmark harness: cold start · warm · p50/p95/p99 · throughput
├── 🟢 Quantization: fp32 → fp16 → int8, đánh đổi độ chính xác vs tốc độ
├── 🟢 ONNX / TensorRT / llama.cpp — pipeline chuyển đổi và bẫy
├── 🟢 Đo trên phần cứng thật: Pi 5 vs Jetson vs x86, có bảng số
├── 🟢 Memory bandwidth là nút cổ chai thường gặp hơn compute
├── 🟡 VLA models (ACT, π0, OpenVLA) — biết chúng ăn gì và trả ra gì
└── 🟡 Thermal throttling — đo nhiệt trong lúc benchmark
```

**GATE L4:** repo public + bài viết có bảng số đo thật trên ≥2 loại phần cứng, có phương pháp đo và sai số ghi rõ.

---

## L5 — SENSOR + TIME SYNC + PLATFORM ★ · 150h · cần phần cứng

```
L5
├── 🟢 Đọc raw register của ≥2 cảm biến khác nhau qua I2C/SPI
├── 🟢 PTP setup thật, đo residual error
├── 🟢 Hardware trigger — một xung kích nhiều cảm biến
├── 🟢 Time sync error budget — bảng cộng từng nguồn sai số
├── 🟢 Ingest pipeline: nhiều stream khác tần số → MCAP → truy vấn
├── 🟢 Backpressure & drop policy — drop cái gì, ghi lại việc đã drop
├── 🟡 Sensor fusion cơ bản (EKF) — dùng thư viện, không tự viết
└── 🟡 Calibration intrinsic/extrinsic
```

**GATE L5:** platform chạy 72h không người trông, có dashboard, có báo cáo sai số đồng bộ bằng số đo thật.

---

## L6 — ROBOT LEARNING · 120h · tùy chọn, chỉ mở nếu L4 đã có phản hồi thị trường

```
L6
├── SO-101 lắp ráp + calibration
├── LeRobot: record dataset → train policy → deploy
├── Dataset của chính mình lên HF Hub
└── Dùng chính audit tool của L2 lên dataset của mình ← vòng tròn khép kín, rất đắt giá khi phỏng vấn
```

---

## TRACK NGANG — chạy suốt, không có gate mở

| Việc | Nhịp | Vì sao |
|---|---|---|
| Lab notebook mỗi thí nghiệm | Mỗi lần đo | Là sản phẩm, không phải ghi chú |
| `hours.csv` | Mỗi ngày | Không có nó thì mọi gate vô nghĩa |
| Bài viết tiếng Anh | Sau mỗi ★ artifact | Repo là kênh phân phối duy nhất |
| Đọc JD thật | 2 tuần/lần | Biết thị trường đang gọi kỹ năng này bằng tên gì |
| Apply như một phép đo | Từ tháng 5–6 | Apply là phép đo, không phải bước cuối |

---

# PHẦN 5 — NGUỒN HỌC

Nguyên tắc chọn nguồn: **một nguồn chính có cấu trúc + một nguồn tra cứu + datasheet**. Không quá ba. Thêm nguồn thứ tư là dấu hiệu đang trốn việc làm bài tập.

## 5.1 Điện tử cơ bản (L0)

| Nguồn | Link | Dùng cho | Ghi chú |
|---|---|---|---|
| **CircuitBread — Circuits 1** | circuitbread.com | Nguồn chính có cấu trúc | Có cả bài viết và video theo chuỗi, kèm calculator và glossary. Đây là thứ thay thế việc google lung tung. |
| **SparkFun Learn** | learn.sparkfun.com | Tra cứu theo chủ đề | "How to Use a Multimeter", "How to Use a Breadboard", "I2C", "Serial Communication". Ngắn, chính xác, có sơ đồ. |
| **Ben Eater** | eater.net + YouTube | Bus, clock, tín hiệu số | Chất lượng cao nhất internet cho tầng này. Xem chọn lọc các tập về SPI, clock, logic. |
| **EEVblog Fundamentals** | youtube.com/@EEVblog | Cách dùng multimeter, cách đọc datasheet | Tập "How to read a datasheet" đáng xem 2 lần |
| **All About Circuits** | allaboutcircuits.com | Từ điển tra cứu | Bộ "Lessons in Electric Circuits" 6 tập, miễn phí. Tra, đừng đọc tuần tự. |
| **Adafruit Learning System** | learn.adafruit.com | Guide theo linh kiện cụ thể | — |
| 🔴 **The Art of Electronics** | — | Không đọc tuần tự | Để làm từ điển về sau |

## 5.2 Nhúng & bus (L0–L3)

| Nguồn | Link | Dùng cho |
|---|---|---|
| **sigrok / PulseView docs** | sigrok.org/wiki/PulseView | Logic analyzer, decoder |
| **ESP-IDF Programming Guide** | docs.espressif.com | I2C driver, I2S driver, timer, DMA |
| **Making Embedded Systems** — Elecia White | sách (O'Reilly) | **Cuốn đúng nhất cho người từ software sang.** Đọc chương đầu trước, phần còn lại khi cần. |
| **Embedded.fm** | embedded.fm | Podcast, tư duy embedded |
| **Datasheet của chính linh kiện bạn cầm** | — | Nguồn thật duy nhất. Tutorial có thể sai, datasheet thì không. |

## 5.3 Dữ liệu robot (L1–L2) — nhóm quan trọng nhất

| Nguồn | Link | Dùng cho |
|---|---|---|
| **MCAP spec + docs** | mcap.dev · github.com/foxglove/mcap | Nguồn gốc. Đọc spec, không đọc tutorial về spec. |
| **Foxglove docs** | docs.foxglove.dev | Visualization, kết nối dữ liệu |
| **Foxglove blog** | foxglove.dev/blog | Bài về MCAP, về data infrastructure cho robotics — đúng nghề bạn nhắm |
| **Rerun** | rerun.io | So sánh với Foxglove |
| **LeRobot docs** | huggingface.co/docs/lerobot | Dataset format v3.0, porting datasets |
| **LeRobot repo** | github.com/huggingface/lerobot | Đọc source `lerobot/datasets/` — đọc kiến trúc, không chỉ chạy |
| **HF Hub — org `lerobot`** | huggingface.co/lerobot | Dataset công khai để audit |
| **Protobuf docs** | protobuf.dev | Bạn có thể đã biết |

## 5.4 ROS 2 & real-time (L3)

| Nguồn | Link | Ghi chú |
|---|---|---|
| **docs.ros.org** | docs.ros.org/en/jazzy | Nguồn chính thức. Concepts trước Tutorials. |
| **ROS 2 Concepts → About QoS, About tf2** | docs.ros.org | Hai trang đáng đọc kỹ nhất với bạn |
| **ROS Discourse** | discourse.ros.org | Xem ngành đang tranh luận gì |
| **Articulated Robotics** (YouTube) | — | Giải thích ROS 2 rõ ràng, thực tế |
| **Steve Macenski** — bài báo ROS 2 Science Robotics 2022 | — | Đọc để hiểu thiết kế, không chỉ API |

## 5.5 Cộng đồng — nơi tín hiệu thị trường xuất hiện

| Nơi | Dùng để |
|---|---|
| **LeRobot Discord** (link trong repo HF) | Báo lỗi dataset, hỏi maintainer. Đây là nơi GATE L2 tiêu chí 5 sẽ xảy ra. |
| **Foxglove Discord** | Hỏi về MCAP |
| **ROS Discourse** | Theo dõi ngành |
| **r/robotics** | Cross-post bài viết |
| **Hacker News** | Cross-post artifact |

---

# PHẦN 6 — CÁCH HỌC CHO NGƯỜI TỪ BACKEND

Bạn nói đúng một điều quan trọng: *"một người nhảy từ thuần lý thuyết backend sang đo lường thực tế sẽ chưa quen được ngay"*. Dưới đây là cái khác biệt cụ thể, và cách xử lý.

## 6.1 Khác biệt căn bản

| Backend | Phần cứng |
|---|---|
| Lỗi có stack trace | Lỗi không có gì cả. Nó chỉ "không chạy", hoặc tệ hơn, **chạy nhưng ra số sai** |
| Đọc log để biết chuyện gì xảy ra | Thông tin chỉ tồn tại **trên đầu que đo**. Không đo thì không có dữ liệu. |
| Thử lại miễn phí | Thử sai có thể đốt linh kiện |
| Đúng/sai rõ ràng | Có dải chấp nhận được. "Lệch 7% so với tính toán" có thể là **đúng**. |
| Abstraction đáng tin | Mọi abstraction đều rò rỉ xuống tầng vật lý |

**Hệ quả thực tế:** thói quen "chạy thử xem sao" — thứ hiệu quả nhất trong backend — là thói quen tệ nhất ở đây. Thay bằng: dự đoán → đo → giải thích chênh lệch.

## 6.2 Vòng lặp học — dùng cho mọi thứ, từ điện trở tới MCAP

```
1. CÂU HỎI      viết ra một câu hỏi trả lời được bằng một con số
2. DỰ ĐOÁN      tính con số kỳ vọng + cách tính. commit. KHÔNG hỏi AI ở bước này.
3. THIẾT LẬP    sơ đồ đấu nối / cấu hình / dụng cụ
4. ĐO           kèm sai số của chính phép đo
5. CHÊNH LỆCH   đo − dự đoán = ?
6. GIẢI THÍCH   tự viết giả thuyết TRƯỚC, rồi mới tra cứu/hỏi AI
7. CÂU HỎI TIẾP
```

Bước 2 và bước 6 là toàn bộ giá trị. Bỏ chúng thì bạn đang xem tutorial, không phải học.

## 6.3 Quy tắc chống rabbit hole

Đây là cách chữa đúng bệnh "đụng đâu google đấy":

| Quy tắc | Cụ thể |
|---|---|
| **Không mở YouTube khi chưa có một con số** | Xem video để hiểu "điện trở là gì" = lướt. Xem vì "tính ra 9mA mà đo 12mA" = học. |
| **Timebox 25 phút** | Một thắc mắc phụ được tối đa 25 phút. Hết giờ → ghi vào `later.md`, quay lại việc chính. |
| **File `later.md`** | Mọi câu hỏi nảy ra giữa chừng đi vào đây. Mỗi cuối tuần đọc lại: 80% sẽ không còn quan trọng. Đó là bằng chứng chúng là rabbit hole. |
| **Quy tắc ba nguồn** | Một nguồn chính + một tra cứu + datasheet. Nguồn thứ tư = đang trốn việc. |
| **Dịch sang thứ đã biết** | Mỗi khái niệm mới, viết một dòng "cái này giống ... trong backend, khác ở chỗ ...". Nếu không viết được, bạn chưa hiểu. |
| **Đọc spec, không đọc tutorial về spec** | MCAP spec ngắn hơn và đúng hơn mọi bài blog về MCAP |

## 6.4 Mẫu lab notebook — copy vào mỗi thư mục `/lab/NN-*/`

```markdown
# NN — <tên thí nghiệm>

## Câu hỏi
<một câu, trả lời được bằng số>

## Dự đoán            ← commit file này TRƯỚC khi đo
Giá trị kỳ vọng: <số> <đơn vị>
Cách tính:
  <công thức, nguồn tham số (datasheet trang mấy)>
Khoảng chấp nhận: ±<x>%
Tôi KHÔNG chắc về: <liệt kê giả định yếu nhất>

## Thiết lập
Dụng cụ: <tên, model>
Sơ đồ đấu nối: <ảnh hoặc mô tả>
Cấu hình: <sample rate, baud, ...>

## Phương pháp đo và sai số của phép đo
Cách đo: <...>
Sai số dụng cụ: ±<...>     ← phần hầu hết người tự học bỏ qua
Nguồn sai số khác: <nhiệt độ, tiếp xúc, tải của que đo...>

## Số đo
<bảng hoặc file capture>

## Chênh lệch
Dự đoán <a> vs đo <b> → lệch <c>%

## Giải thích            ← tự viết giả thuyết TRƯỚC khi tra cứu
<...>

## Thí nghiệm tiếp theo
<...>
```

## 6.5 Nhịp tuần đề xuất

| Loại tuần | Giờ | Làm gì |
|---|---|---|
| Tuần rảnh (10–12h) | Bàn hàn + que đo | L0, sau này L5 |
| Tuần thường (5–8h) | Chia đôi | L1/L2 buổi tối + một thí nghiệm cuối tuần |
| Tuần crunch MDP (0–2h) | **Chỉ đọc, không build** | Đọc MCAP spec, docs.ros.org, source lerobot |

Đừng ép một thí nghiệm phần cứng vào tuần đang go-live. Sẽ hỏng cả hai.

---

# PHẦN 7 — CHECKLIST TỰ CHẤM

Tick khi **làm được**, không phải khi **đã đọc**.

## L0 — Nền đo lường

```
[ ] Giải thích được vì sao "điện áp tại chân này" là câu nói thiếu nghĩa
[ ] Đo được V, I, R đúng cách, không làm đứt cầu chì đồng hồ
[ ] Test thông mạch toàn bộ dây jumper trước khi dùng
[ ] Dự đoán rồi đo cầu phân áp 3 tỉ lệ, lệch <5%
[ ] Dự đoán rồi đo dòng LED, lệch <10%, giải thích được vì sao lệch
[ ] Biết board nào 3.3V, board nào 5V, và chuyện gì xảy ra khi trộn
[ ] Giải thích được vì sao I2C cần pull-up
[ ] Đọc trọn một datasheet, viết tay register map, đối chiếu đúng ≥90%
[ ] Phân biệt được Absolute Maximum vs Recommended Operating
[ ] Nối GND của logic analyzer vào mạch (không quên)
[ ] Chọn được sample rate đúng cho một tín hiệu đã biết tần số
[ ] Nhìn thấy START / address / ACK / STOP trên PulseView
[ ] Đo chu kỳ SCL và tính ngược ra 100kHz
[ ] Tự giải mã DHT11 từ timing diagram, không dùng decoder có sẵn
[ ] Đo được mức sụt áp khi servo quay, giải thích brownout
[ ] Ghi được "sai số của phép đo" trong mọi entry lab notebook
```

## L1 — Định dạng dữ liệu

```
[ ] Phân biệt monotonic vs wall clock, biết dùng cái nào khi nào
[ ] Giải thích được vì sao float64 giây là lựa chọn sai cho timestamp ns
[ ] Tính được clock drift từ ppm ra ms/giờ
[ ] Phân biệt timestamp at source vs at receive, biết vì sao nó quan trọng
[ ] Vẽ được cấu trúc file MCAP từ trí nhớ
[ ] Viết được file MCAP từ dữ liệu tổng hợp
[ ] Đọc được 10 giây giữa file lớn mà không scan toàn bộ
[ ] Biết chuyện gì xảy ra với file MCAP khi process bị kill giữa chừng
[ ] Thiết kế schema có timestamp + frame_id + unit + uncertainty + calibration_id
[ ] Chứng minh được v1 → v2 backward compatible bằng test tự động
[ ] Mở file trong cả Foxglove và Rerun, nói được khác biệt
```

## L2 — Chất lượng dữ liệu

```
[ ] Mô tả được cấu trúc LeRobotDataset v3.0 (và khác gì v2.1)
[ ] Định nghĩa được ≥4 lớp lỗi bằng công thức toán, không bằng lời
[ ] Tự tạo được dữ liệu hỏng để test detector
[ ] Chạy được trên ≥5 dataset công khai bằng một lệnh
[ ] Tìm được ≥1 lỗi THẬT, có script reproduce tối giản
[ ] Đã báo cáo lỗi đó ra ngoài (issue hoặc Discord)
[ ] Đã viết và publish bài tiếng Anh
[ ] Có ≥1 phản hồi có nội dung từ người ngoài
```

## L3 — ROS 2 & real-time

```
[ ] Giải thích được khác biệt determinism vs throughput bằng một ví dụ số
[ ] Đo được phân bố jitter của một topic, không chỉ giá trị trung bình
[ ] Giải thích được vì sao p99 không phải chỉ số đúng cho control loop
[ ] Dựng được 3 node, ghi MCAP, mở trong Foxglove
[ ] Nói được QoS reliable vs best-effort thay đổi hành vi thế nào khi nghẽn
[ ] Giải thích được vì sao tf2 lookup phải kèm thời điểm
```

---

# PHẦN 8 — BA ĐIỀU DÁN LÊN TƯỜNG

**1. Cảm giác "hụt kiến thức" không phải do thiếu chiều sâu, mà do thiếu bản đồ.** Chiều sâu điện tử bạn cần là hữu hạn và đã liệt kê hết ở Phần 1 — khoảng 40 mục 🟢. Không có mục thứ 41 đang ẩn nấp đâu đó.

**2. Bạn không thiếu kiến thức nền, bạn thiếu thói quen đo.** Backend 8 năm là nền rất mạnh — pipeline, latency budget, schema evolution, backpressure đều là thứ ngành robotics đang thiếu người. Cái mới duy nhất là: thông tin phải được **tạo ra bằng phép đo** trước khi có thể suy luận trên nó.

**3. Đường tới việc làm đi qua L1 → L2, không qua L0.** L0 khiến bạn không bị loại trong 10 phút phỏng vấn. L2 khiến bạn được gọi phỏng vấn. Thứ tự đó không đảo được, và L2 không cần một con điện trở nào.
