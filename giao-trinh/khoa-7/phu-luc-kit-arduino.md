# Phụ lục K7 — Tận dụng kit Arduino: bài tập phụ gắn vào chặng (tùy chọn, ~14h)

> **Vị trí:** song song C1–C10, mỗi bài gắn vào một chặng · **Cần trước:** C0 (bàn an toàn, đo trước khi cấp điện), K1 Phần D (logic analyzer) · **Sau phụ lục này bạn quyết định được:** linh kiện nào của kit đáng lên robot, linh kiện nào chỉ để tập trên bàn, và linh kiện nào **không bao giờ** được làm chức năng an toàn.

Kit Arduino Upgraded Learning Kit 36 món đã mua ở K1 (danh sách ở `khoa-1/_MUA-SAM-K1.md`). Phần lớn không nằm trên đường găng của K7, nhưng có sáu thứ làm được việc thật: tập trước một phép đo nguy hiểm trên mạch 5 V an toàn, ghi thêm một kênh dữ liệu, hoặc cho robot một cách "nói" trạng thái. Không bài nào ở đây thay một checkpoint hay một tiêu chí gate của chặng. Giờ **không** tính vào 561h lõi `[ước lượng — cộng giờ từng bài dưới đây]`.

| Bài | Linh kiện kit | Gắn vào | Giờ | Thêm phải mua |
|---|---|---|---|---|
| P1 Diễn tập đo thời gian nhả relay | Relay 1 kênh, UNO, MB102 + adapter 9 V | Trước C10.1 | 2 | Zener 10 V, 1N4007 (đã có trong danh sách C10) |
| P2 Ghi nhiệt độ bằng LM35 | LM35DZ, DHT11 | C1.5, Gate C1 | 2 | — |
| P3 Núm lệnh PWM có khóa "khởi động ở 0" | Biến trở 10k | C3.4 | 1 | — |
| P4 Đèn trạng thái + còi báo chạy | Module RGB, còi | C5.3, C10.2 | 3 | NPN C1815 (đã có trong danh sách C10) |
| P5 Màn trạng thái LCD1602 trên bus 3,3 V | LCD1602 I2C | C5.4 | 3 | Mạch chuyển mức BSS138 (33k, `_MUA-SAM-K7.md` mục 0.4) |
| P6 Bàn xoay kiểm hệ số gyro | 28BYJ-48 + ULN2003, UNO | C7.1–C7.2 | 3 | — |
| — RC522 + thẻ, LED đỏ | RC522, thẻ, LED | C9 (FAIL action NFC, LED camera) | — | — (thay dòng C9 trong bảng mua) |

**Thứ tự gợi ý:** P2 cùng lúc với tải giả của C1.5 → P3 khi làm C3.4 → P4, P5 sau C5.3 → P6 khi gá IMU ở C7.1 → P1 ngay trước khi học C10.1.

---

## Không dùng làm chức năng an toàn — đọc trước

Mấy món trong kit trông như đồ an toàn nhưng không phải. Dùng chúng thay cho thiết bị của C1/C10 là vi phạm quy tắc an toàn của khóa (`00-tong-quan.md` mục 10).

| Món kit | Trông giống | Vì sao không | Dùng vào việc gì thay vào |
|---|---|---|---|
| Relay 1 kênh 5 V | Relay E-stop | Cuộn lái từ GPIO qua transistor của module: phần mềm giữ được relay, kẹt chân cao là relay không nhả. Định mức tiếp điểm in trên vỏ thường ghi cho AC, DC thấp hơn nhiều `[tự đo — đọc chữ trên vỏ relay]`; không có 87a để giám sát | P1: tập đo trên mạch 5 V |
| Remote + mắt thu hồng ngoại | Nút dừng từ xa | Là E-stop phần mềm: mất tầm nhìn, hết pin remote, firmware treo đều làm nó im lặng | Không dùng |
| Công tắc nghiêng dạng bi | Cảm biến lật | Bi rung khi robot chạy, tín hiệu nảy liên tục; IMU đo góc nghiêng tốt hơn nhiều | Không dùng |
| Cảm biến lửa | Báo cháy pin | Photodiode hồng ngoại thấy cả nắng và đèn sợi đốt; không có mô hình lỗi nào đáng tin cho pin | Không dùng. An toàn pin là quy trình C1.6 + bình chữa cháy |
| Joystick | Tay cầm teleop | Không có deadman đúng nghĩa, dây kéo từ robot ra tay người | Không dùng cho teleop. Tay cầm có nút giữ ở C5 |

---

## P1 — Diễn tập đo thời gian nhả relay: chỉ diode so với diode + Zener (2h)

**Gắn vào:** ngay trước C10.1 phần 6 bước 6 (đo hai cấu hình dập cuộn). **Quyết định được:** cách bố trí kênh, trigger và quy ước "cạnh đầu tiên" đã chạy đúng trên một relay rẻ, nên lần đo relay ô tô 12 V trên robot chỉ còn là đo, không còn là thử dụng cụ.

**Vì sao làm trên relay kit trước:** cùng hiện tượng (dòng cuộn cần đường xả; đường xả quyết định relay nhả nhanh hay chậm), nhưng 5 V, ~70 mA `[spec — datasheet relay Songle SRD-05VDC, kiểm mã trên vỏ]`, không có pack, không có motor. Sai ở đây chỉ mất một module 20k.

**An toàn:**
- KHÔNG bỏ hẳn diode dập cuộn khi cuộn đang được transistor lái. Không có đường xả, điện áp cảm ứng ở collector có thể vượt xa V_CEO của transistor trên module `[chuẩn]`.
- Đỉnh điện áp ở collector khi có Zener ≈ 5 V + V_Z + 0,7 V. Đọc mã transistor trên module, tra V_CEO. Với Zener 10 V, đỉnh ~16 V phải nhỏ hơn V_CEO và còn dư `[tự đo — mã transistor]`.
- Chân tín hiệu vào logic analyzer ≤ 5 V `[spec — logic analyzer 24 MHz, ngưỡng 5,25 V]`. Tiếp điểm relay chỉ nối với 3,3 V qua 10k, không nối với 9 V của adapter.

**Mạch:**

```
  MB102 5V ──┬── VCC module relay          UNO D7 ── IN module ── CH0 logic analyzer
             │                              GND chung: UNO, MB102, logic analyzer
  Tiếp điểm:  COM ── GND
              NO  ──┬── 10k ── 3,3 V (MB102)
                    └── CH1 logic analyzer     (CH1 thấp = tiếp điểm đóng)
  Cuộn: gỡ diode trên module (bài luyện dây hút thiếc), hàn ra hai dây để gắn
        cấu hình A: 1N4007 song song cuộn (vạch về phía +)
        cấu hình B: 1N4007 nối tiếp Zener 10 V, song song cuộn (Zener ngược chiều diode)
```

**Dự đoán (commit `lab/kit/p1/prediction.md` trước khi đo):** thời gian nhả (cạnh xuống của IN → cạnh đầu tiên CH1 lên) ở cấu hình A và B; tỉ số B/A; số lần nảy của tiếp điểm khi đóng. Tra thời gian nhả tối đa trong datasheet relay theo mã in trên vỏ.

**Làm:**
1. Kiểm nguội: đo Ω giữa VCC và GND của module (không gần 0); đo diode và Zener bằng chế độ diode.
2. UNO đảo D7 với chu kỳ 500 ms, 20 lần. PulseView 1 MHz trở lên, trigger cạnh xuống CH0.
3. Cấu hình A: 20 lần. Cấu hình B: 20 lần. Ghi từng lần vào `measurements.jsonl` (`config`, `t_release_ms`, `n_bounce`).
4. Áp đúng quy ước của C10 mục 3: thời điểm kết thúc là cạnh đầu tiên của tín hiệu đích sau đó ổn định ≥ 10 ms.

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

- Cấu hình B nhả **nhanh hơn rõ** cấu hình A, thường vài lần `[tự đo]`. Lý do: dòng cuộn tắt nhanh hơn khi phải đẩy ngược qua điện áp lớn hơn (V_Z + V_diode thay vì chỉ V_diode).
- Thời gian nhả ở A có thể vượt con số tối đa trong datasheet. Datasheet relay thường đo **không** có diode song song cuộn `[tự đo — đọc điều kiện đo trong datasheet]`.
- Đóng tiếp điểm thấy vài lần nảy trong khoảng dưới vài ms `[tự đo]`. Đó là lý do phải có quy ước "cạnh đầu tiên".

</details>

**Nếu ra khác:** B không nhanh hơn A → Zener lắp xuôi chiều (nó dẫn như diode thường), hoặc diode trên module chưa gỡ hết. CH1 không đổi → kiểm COM/NO bằng thông mạch khi relay hút.

**Dữ liệu ra:** `lab/kit/p1/` với `.sr`, `measurements.jsonl`, một bảng hai cấu hình (trung vị, min, max). Đem bảng này vào C10.1 làm "dự đoán có căn cứ" cho relay ô tô.

---

## P2 — Ghi nhiệt độ bằng LM35: một kênh dữ liệu chậm, có trễ nhiệt (2h)

**Gắn vào:** C1.5 (tải giả) và phép chạy 30 phút trên pin ở Gate C1. Nhiệt kế hồng ngoại vẫn là dụng cụ chính của gate; LM35 thêm **chuỗi thời gian** mà súng hồng ngoại không cho. **Quyết định được:** điểm nào trên bo nguồn nóng nhất và nóng nhanh tới đâu khi tải tăng.

**Thông số cần tra trong datasheet TI LM35:** dải nguồn, hệ số mV/°C, sai số của bản **D** ở 25 °C và trên toàn dải, mục về tải điện dung (dây dài làm LM35 dao động) `[spec — TI LM35, kiểm bảng cho đúng hậu tố DZ]`.

**Mạch:** LM35 nuôi từ buck 5 V của C1 (không từ 3,3 V: dưới dải nguồn). Chân OUT vào một chân ADC1 của ESP32-S3 theo `firmware/PINS.md`. Ra 10 mV/°C nên ở 100 °C chỉ ~1 V, nằm trong dải ADC mà không cần chia áp `[spec — LM35]`. Dây dài thì làm theo mạch chống dao động trong datasheet.

**Dán cảm biến:** băng keo nhôm hoặc keo tản nhiệt lên thân điện trở nhôm 10 Ω 50 W, hoặc lên vỏ buck-boost. DHT11 đặt cách bo ~30 cm làm nhiệt độ môi trường (DHT11 sai số lớn, chỉ dùng để thấy xu hướng `[spec — datasheet DHT11, kiểm]`).

**Dự đoán:** nhiệt độ ổn định của điện trở 10 Ω 50 W khi cấp 12,8 V **không** tản nhiệt và **có** tản nhiệt; thời gian tới 63% mức tăng cuối (hằng số thời gian nhiệt).

**Làm:**
1. Hiệu chuẩn hai điểm trước khi tin số: nước đá đang tan (≈0 °C `[chuẩn]`) trong túi nilon và nhiệt độ phòng so với nhiệt kế hồng ngoại. Dùng hàm hiệu chuẩn ADC của ESP-IDF, không dùng số đọc thô `[tự đo — ADC ESP32-S3 phi tuyến ở hai đầu dải]`.
2. Log 1 Hz, cùng timestamp với log INA226 (C1.5). Mỗi dòng có `sensor_id` và `calibration_id`.
3. Bật tải giả, chờ ổn định, tắt tải. Vẽ nhiệt độ và công suất trên cùng trục thời gian.

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

- Đường nhiệt độ có dạng hàm mũ và **trễ** sau bậc công suất vài phút `[tự đo]`. Súng hồng ngoại chụp một điểm và một lúc, không thấy được hằng số thời gian này.
- LM35 dán trên bề mặt thường đọc **thấp hơn** điểm nóng thật vài độ, vì nó cũng tỏa nhiệt ra không khí `[ước lượng]`. Đây là sai số của cách gắn, không phải của chip.

</details>

**Lăng kính data infra:** đây là kênh có **trễ vật lý**. Timestamp là lúc ADC lấy mẫu, nhưng giá trị là nhiệt độ của vài phút trước ở điểm nóng. Khi C7.4 viết data contract, ghi trễ này vào metadata của kênh, giống như ghi trễ của camera.

---

## P3 — Núm lệnh PWM có khóa "khởi động ở 0" (1h)

**Gắn vào:** C3.4 (PWM → vận tốc, vùng chết), trên bàn, motor kẹp, nguồn bàn có `I_set`. **Quyết định được:** cách viết một đầu vào lệnh mà khi bật máy, reset hay hết lỗi, motor **không** tự quay theo vị trí núm còn để sẵn.

**Mạch:** biến trở 10k giữa 3,3 V và GND, chân giữa vào ADC1. Không nối 5 V.

**Luật firmware (viết trước, test sau):**
- Sau boot và sau mọi lần thoát FAULT, duty = 0 cho tới khi núm được thấy ở dưới 2% trong ≥ 0,5 s. Đây là cùng ý với "nhả nút E-stop không làm robot chạy lại" ở C10.1, ở quy mô một núm vặn.
- Kẹp duty tối đa trên bàn (ví dụ 30%, ghi vào `decisions.md`); giới hạn tốc độ thay đổi duty.

**Test tự động (hạt giống cho HIL ở C11.2):** ba ca: boot khi núm ở 50% → duty phải giữ 0; vặn về 0 rồi lên → duty theo núm; giả FAULT khi núm ở 40% → sau khi xóa lỗi duty phải giữ 0. Kiểm bằng logic analyzer trên chân PWM.

---

## P4 — Đèn trạng thái và còi báo trước khi chạy (3h)

**Gắn vào:** C5.3 (teleop) và C10.2 (state machine). **Quyết định được:** người đứng cạnh robot biết nó đang ở trạng thái nào mà không cần laptop, và bạn đo được là việc báo hiệu không làm xấu vòng điều khiển.

**Mạch:**
- Module RGB: đo xem trên module đã có điện trở hạn dòng chưa (đo Ω từ chân màu tới chân LED). Chưa có thì thêm 220–330 Ω mỗi màu; tính dòng từ 3,3 V − V_f (đo V_f bằng chế độ diode) `[tự đo]`. Lái bằng LEDC, không dùng MCPWM (motor đang dùng).
- Còi: thử còi chủ động hay bị động bằng cách cấp 5 V qua MB102 trong 1 s: kêu liên tục là chủ động. Lái phía thấp bằng NPN C1815 (điện trở base 1–4,7k) từ 5 V. Còi bị động thì phải phát PWM vài kHz.

**Bảng trạng thái (đồng bộ với state machine C10.2, sửa ở đó trước):**

| Trạng thái firmware | Đèn | Còi |
|---|---|---|
| IDLE (động lực ngắt) | Xanh lá chậm | — |
| ARMED / TELEOP | Xanh dương | 2 tiếng ngắn khi ARM |
| AUTO (Nav2) | Vàng (đỏ + xanh lá) | 1 tiếng/giây trong 2 s trước khi bắt đầu chạy |
| FAULT | Đỏ nháy nhanh | 3 tiếng |
| ESTOP_LATCHED | Đỏ liên tục | — |

**Luật:** đèn và còi là **thông tin**, không phải chức năng an toàn. Đèn hỏng không được làm robot dừng hay chạy. Chỉ đọc STATE, không ghi.

**Kiểm:** đo jitter p99 của vòng 100 Hz như C4.2 khi đèn và còi tắt, rồi khi đang nháy. So bằng kiểm tương đương có δ như C7.3. Không đạt thì chuyển cập nhật đèn sang task ưu tiên thấp hơn.

---

## P5 — Màn trạng thái LCD1602 trên bus 3,3 V (3h)

**Gắn vào:** C5.4 (vận hành không màn hình). Robot chạy headless; một dòng chữ trên thân cho biết IP, điện áp pack, trạng thái, mã lỗi gần nhất mà không cần SSH. **Quyết định được:** một thiết bị I2C 5 V có được nối vào ESP32 3,3 V không, và nếu có thì nối thế nào.

**Bẫy cần tự thấy trước:** module I2C sau LCD (PCF8574) chạy 5 V và thường có điện trở kéo lên tới 5 V trên SDA/SCL `[tự đo — đo Ω từ SDA tới VCC của module]`.
- Nối thẳng vào ESP32-S3 → chân ESP32 bị kéo lên 5 V, vượt giới hạn tuyệt đối `[spec — datasheet ESP32-S3, Absolute Maximum Ratings]`.
- Chạy PCF8574 ở 3,3 V → chữ LCD mờ hoặc không hiện, vì LCD cần ~5 V để có tương phản `[tự đo]`.
- Gỡ điện trở kéo lên rồi để ESP32 kéo lên 3,3 V → mức cao 3,3 V nằm dưới ngưỡng V_IH = 0,7·VDD ≈ 3,5 V của PCF8574 ở 5 V `[spec — datasheet PCF8574]`. Chạy được trên bàn không có nghĩa là đúng spec. Đây là cùng loại lỗi với mạch đệm 74HC244 của module BTS7960 (`_MUA-SAM-K7.md`, dòng driver C3).

**Cách đúng:** mạch chuyển mức BSS138 hai chiều giữa bus 3,3 V và bus 5 V. Đặt LCD trên **cổng I2C thứ hai** của ESP32-S3, tách khỏi bus IMU `[spec — ESP32-S3 có hai bộ điều khiển I2C, kiểm TRM]`.

**Dự đoán:** thời gian ghi lại toàn bộ 32 ký tự ở 100 kHz (đếm byte I2C cho mỗi ký tự ở chế độ 4 bit qua PCF8574); ảnh hưởng lên jitter p99 nếu ghi trong task điều khiển.

**Làm:**
1. Đo Ω SDA/SCL → VCC của module; ghi giá trị điện trở kéo lên.
2. Nối qua BSS138, `i2cdetect` từ firmware: địa chỉ 0x27 hoặc 0x3F `[tự đo — tùy phiên bản chip]`.
3. Logic analyzer giải mã I2C: đo thời gian lên của cạnh ở cả hai phía chuyển mức; đo thời gian một lần cập nhật màn hình.
4. Cập nhật màn hình trong task ưu tiên thấp, 2 Hz. Đo jitter p99 như P4.

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

- Mỗi ký tự qua PCF8574 ở chế độ 4 bit tốn vài byte I2C (hai nửa byte, mỗi nửa cần xung EN lên/xuống). Một lần ghi lại cả màn hình vào cỡ chục ms ở 100 kHz `[ước lượng — đếm byte; tự đo trên logic analyzer]`. Gấp nhiều lần chu kỳ 10 ms của vòng điều khiển, nên **không** được gọi trong task điều khiển.
- Ghi đúng chỗ (task ưu tiên thấp, bus riêng), jitter p99 không đổi đáng kể `[tự đo]`. Đây là bản nhỏ của tiêu chí "sidecar không ảnh hưởng vòng điều khiển" ở C7.

</details>

---

## P6 — Bàn xoay kiểm hệ số gyro bằng 28BYJ-48 (3h)

**Gắn vào:** C7.1–C7.2 (IMU gá trên robot, timestamp). Số ra được dùng tiếp ở C11.1 (model sim lấy tham số từ số đo). **Quyết định được:** hệ số thang của gyro trục z sai bao nhiêu phần trăm, và tin "tham chiếu" của mình tới đâu.

**Mạch:** UNO + ULN2003 + 28BYJ-48, nuôi từ USB của UNO (không từ MB102: ổn áp tuyến tính trên đó nóng khi hạ 9 V xuống 5 V ở dòng motor) `[tự đo — sờ ổn áp sau 1 phút]`. IMU dán băng keo xốp lên một đĩa bìa cứng gắn trục motor. Dây IMU → ESP32 để chùng; chỉ quay **+1 vòng rồi −1 vòng** để dây không xoắn.

**Bẫy tham chiếu:** tài liệu bán hàng hay ghi "2048 bước/vòng". Tỉ số hộp số thật của 28BYJ-48 không phải đúng 64:1 `[tự đo]`. Trước khi dùng motor làm chuẩn, đo tỉ số thật: đánh dấu đĩa, chạy N = 10 vòng "danh nghĩa" (10 × 2048 bước), đo góc lệch của vạch so với điểm xuất phát.

**Dự đoán:**
1. Sau 10 vòng danh nghĩa, vạch lệch bao nhiêu độ và lệch về phía nào.
2. Gyro z tích phân qua +1 vòng thật ra bao nhiêu độ (đoán sai số thang của IMU bạn dùng từ datasheet).

**Làm:**
1. Đo tỉ số thật như trên (ít nhất 3 lần). Tính số bước cho đúng 1 vòng.
2. ESP32 ghi gyro z ở ≥ 200 Hz kèm timestamp theo cách đã chốt ở C7.2. Đứng yên 10 s (đo bias), quay +1 vòng chậm (~10 s), đứng yên 10 s, quay −1 vòng.
3. Trừ bias, tích phân; so với 360°. Lặp 5 lần; báo trung bình và độ lệch chuẩn của sai số thang.

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

- Tỉ số hộp số 28BYJ-48 thường đo được khoảng 63,68:1 thay vì 64:1, tức khoảng 2038 bước/vòng thay vì 2048 `[tự đo — con số hay được báo cho dòng motor này; motor của bạn có thể khác]`. Sau 10 vòng danh nghĩa, vạch đi **quá** điểm xuất phát vài chục độ. Nếu tin con số 2048, bạn sẽ gán sai số của motor cho gyro.
- Bias chưa trừ làm góc tích phân trôi tuyến tính theo thời gian. Vì vậy phải đứng yên trước và sau, rồi so +1 và −1 vòng: sai số thang đổi dấu theo chiều quay, bias thì không.

</details>

**Lăng kính data infra:** đây là `calibration_id` đầu tiên của IMU (C7.4): bản ghi gồm tỉ số motor đo được, bias, hệ số thang, nhiệt độ lúc đo (P2), firmware hash. Bài học chung: **một tham chiếu chưa được kiểm thì không phải là tham chiếu**, giống ground truth gán nhãn sai trong eval.

---

## Để sau đường tối thiểu

- **RC522 + thẻ** của kit: FAIL action NFC của C9 (không cần mua module mới).
- **SG90:** nắp che ống kính camera nhận mặt ở C9: tín hiệu "camera không nhìn" mà người xung quanh thấy được, bổ sung cho LED nối cứng. Không thay được việc cắt nguồn camera (C9.3).
- **DHT11:** nhiệt độ môi trường trong log soak 72h (C10.3).
- **Không dùng trong K7:** 7 đoạn, ma trận LED, 74HC595, bàn phím, cảm biến mực nước, cảm biến âm thanh, LDR, RTC của kit. Chúng không thêm phép đo nào K7 cần. Để luyện tay ở K1 hoặc bỏ.
