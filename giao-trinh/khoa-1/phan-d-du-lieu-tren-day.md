# Khóa 1 — Phần D: Nhìn thấy dữ liệu trên dây (10h)

Phần C đo những đại lượng đứng yên (điện áp, dòng). Phần D đo những thứ **chạy theo thời gian**: các bit trên bus. Quy trình không đổi: dự đoán → commit → đo. Dụng cụ chính là logic analyzer clone 24 MHz (fx2lafw) + PulseView (Bài 7), và câu hỏi xuyên suốt là: *dụng cụ của tôi có đủ nhanh để thấy thứ tôi muốn thấy không* (→ F5.5).

| Bài | Giờ | Viên nang nền nên đọc cùng lúc |
|---|---|---|
| 12 — I2C và ACK | 5h | F5.5 (lướt: Nyquist, sample rate 4–10×), F2.1 (lướt) |
| 13 — I2S | 4h | F5.5, F4.1 (lướt: thạch anh, ppm) |
| 14 — Gate Khóa 1 | 1h | F1.7, F2.3 |

Bản gốc chỉ ghi Phần D = 10h, không chia theo bài; cách chia trên là đề xuất.

---

## Bài 12 — Cắm I2C và nhìn thấy ACK (5h)

> **Vị trí:** Bài 11 (datasheet) → **Bài 12** → Bài 13 (I2S) · **Cần trước:** Bài 3 (bus có clock vs không clock), Bài 7 (PulseView, nối GND), Bài 9 (Rth, điện trở + điện dung), Bài 11 (địa chỉ, chip ID, cấm kéo chân giao tiếp lên khi cảm biến tắt nguồn; bước 6: pull-up và SDO của module), F5.5 (lướt) · **Sau bài này bạn quyết định được:** chọn điện trở pull-up cho một bus I2C theo tốc độ và độ dài dây; cấu hình một capture (sample rate, trigger, số mẫu) đủ để chắc chắn bắt được giao dịch; và chẩn đoán "scanner không thấy gì" theo thứ tự đúng.

### 1. Câu chuyện — ai đã khổ vì chuyện này

Đầu thập niên 1980, Philips cần nối hàng chục con chip bên trong TV (bộ dò kênh, EEPROM, xử lý âm thanh) mà không kéo hàng chục đường song song trên mạch in. Họ tạo ra I²C (Inter-IC, 1982): **hai dây dùng chung cho mọi chip**, mỗi chip có một địa chỉ `[chuẩn]`. Cái giá của hai dây chung là mọi chip phải *chia nhau* cùng một sợi SDA mà không đánh nhau. Lời giải là **open-drain**: không ai được phép đẩy dây lên cao, chỉ được kéo xuống; một điện trở pull-up kéo dây lên khi không ai giữ. Nhờ vậy, khi hai chip "nói" cùng lúc, kết quả là AND logic của cả hai, không phải đoản mạch.

Cái giá thứ hai, đến nay vẫn làm người ta khổ: nếu bộ điều khiển (controller) bị reset giữa lúc một cảm biến đang gửi bit 0, cảm biến tiếp tục giữ SDA ở mức thấp, chờ một nhịp clock không bao giờ tới. **Cả bus treo**, mọi thiết bị khác trên bus cũng chết theo. Đặc tả I²C của NXP (UM10204) có hẳn một mục "bus clear" chỉ cách gỡ: phát 9 xung clock để thiết bị kia nhả dây `[spec — UM10204, mục Bus clear]`. Bài này cho bạn nhìn tận mắt cơ chế "kéo xuống / nhả ra" đó, ở nhịp clock thứ 9 sau địa chỉ: **ACK**.

### 2. Mô hình tư duy

**Điện: open-drain + pull-up = một mạch RC.**

```
 3.3 V ──[Rp]──┬───────────────┬───────────────┬──── SDA (hoặc SCL)
               │               │               │
           ESP32 (ctrl)    BME280 (target)   thiết bị khác     ═╪═ Cb: điện dung của dây + mọi chân
             ┤ công tắc       ┤ công tắc        ┤ công tắc          (vài pF/chân + dây)
               │ xuống GND      │                 │
 GND ──────────┴───────────────┴─────────────────┴────
  Bất kỳ ai đóng công tắc → dây = 0 (nhanh, qua transistor).
  Không ai đóng → dây lên 1 CHẬM, vì Rp phải nạp Cb: hằng số thời gian Rp·Cb.
```

**Giao thức: một giao dịch đọc thanh ghi** (byte-level, WaveDrom JSON — dán vào wavedrom.com/editor.html để xem):

```json
{"signal": [
  {"name": "SDA mang gì", "wave": "=============",
   "data": ["START", "ADDR 7 bit", "W=0", "ACK", "REG", "ACK", "Sr", "ADDR 7 bit", "R=1", "ACK", "DATA", "NACK", "STOP"]},
  {"name": "ai lái SDA", "wave": "=============",
   "data": ["ctrl", "ctrl", "ctrl", "target", "ctrl", "target", "ctrl", "ctrl", "ctrl", "target", "target", "ctrl", "ctrl"]}
]}
```

**Bit-level quanh ACK** (ASCII):

```
          bit 8 (R/W)   bit 9 (ACK)
SCL  ___/‾‾‾‾‾\_______/‾‾‾‾‾‾\________
SDA  ==X=======X______________X=======     ← controller NHẢ SDA sau bit 8;
                ↑ target kéo xuống trước cạnh lên của SCL
                  và giữ THẤP suốt lúc SCL cao = ACK.
                  Nếu không ai kéo, pull-up giữ SDA cao = NACK.
START = SDA xuống khi SCL đang cao · STOP = SDA lên khi SCL đang cao
(mọi lúc khác, SDA chỉ được đổi khi SCL thấp — vì vậy START/STOP không thể nhầm với dữ liệu)
```

1. **Một bit trên I2C là một phép AND của mọi thiết bị.** ACK không phải một "gói tin trả lời": nó là việc target *giữ dây ở mức thấp* trong đúng một nhịp. Controller biết có ai nghe hay không **ở từng byte**.
2. **Tốc độ tối đa của bus là chuyện điện, không phải chuyện phần mềm.** Cạnh lên dài `≈ 0.85·Rp·Cb` (30%→70%). Đặc tả I²C giới hạn thời gian cạnh lên cho mỗi chế độ; Rp quá lớn hoặc dây quá dài thì phải chậm lại.
3. **Rp có cả cận dưới:** transistor kéo xuống chỉ hút được một dòng giới hạn mà vẫn giữ mức thấp đủ thấp, nên Rp không được quá nhỏ. Pull-up là một bài toán chọn trong khoảng `[Rp_min, Rp_max]`, giống bài toán R của divider ở Bài 9.
4. Mô phỏng dưới đây tính cạnh lên cho một lưới Rp × Cb và vẽ SCL với hai pull-up khác nhau. Một trong hai là pull-up nội của ESP32 — driver Arduino-ESP32 bật nó mặc định `[spec — mã nguồn arduino-esp32, esp32-hal-i2c-ng.c: enable_internal_pullup = 1]`.

```python
# [đã chạy] I2C open-drain: cạnh xuống do transistor kéo (nhanh), cạnh lên do pull-up nạp tụ dây (chậm)
import numpy as np
import matplotlib.pyplot as plt

VDD = 3.3
# UM10204: t_r đo từ 30% tới 70% VDD. Nạp RC: V(t) = VDD(1 - e^(-t/RC)) -> t_r = RC*ln(0.7/0.3)
K = np.log(0.7 / 0.3)                 # = 0.8473
TR_MAX = {"Standard 100 kHz": 1000e-9, "Fast 400 kHz": 300e-9}
rp_list = [2.2e3, 4.7e3, 10e3, 45e3]  # 45 kΩ ~ pull-up nội của ESP32 [spec — tra datasheet ESP32-S3]
cb_list = [20e-12, 50e-12, 100e-12, 200e-12, 400e-12]

print("t_r (ns) = 0.8473*Rp*Cb ; S = đạt Standard, F = đạt cả Fast, x = trượt cả hai")
print("Rp \\ Cb  " + "".join(f"{c*1e12:>9.0f}pF" for c in cb_list))
for rp in rp_list:
    row = ""
    for cb in cb_list:
        tr = K * rp * cb
        tag = "F" if tr <= TR_MAX["Fast 400 kHz"] else ("S" if tr <= TR_MAX["Standard 100 kHz"] else "x")
        row += f"{tr*1e9:>9.0f} {tag} "
    print(f"{rp/1e3:>5.1f}k   " + row)

# Rp nhỏ nhất: transistor phải kéo được dây xuống dưới V_OL = 0.4 V khi chỉ "hút" được 3 mA
print(f"Rp_min = (VDD - 0.4 V) / 3 mA = {(VDD - 0.4) / 3e-3:.0f} Ω")

# Vẽ dạng sóng SCL 100 kHz qua hai pull-up khác nhau, Cb = 100 pF
t = np.linspace(0, 20e-6, 4000)
drive_low = (t % 10e-6) < 5e-6          # controller kéo thấp nửa đầu mỗi chu kỳ
fig, ax = plt.subplots(figsize=(7, 3))
for rp in (4.7e3, 45e3):
    v, out, dt = VDD, [], t[1] - t[0]
    for low in drive_low:   # nghiệm chính xác của mạch RC trên mỗi bước dt
        target, tau = (0.0, 50 * 100e-12) if low else (VDD, rp * 100e-12)  # kéo xuống qua ~50 Ω
        v = target + (v - target) * np.exp(-dt / tau)
        out.append(v)
    ax.plot(t * 1e6, out, label=f"Rp = {rp/1e3:g} kΩ")
ax.axhline(0.7 * VDD, ls=":", c="gray"); ax.axhline(0.3 * VDD, ls=":", c="gray")
ax.set_xlabel("t (µs)"); ax.set_ylabel("SCL (V)"); ax.legend()
fig.tight_layout(); plt.show()
```

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| HTTP: URL = địa chỉ, 200 = ACK, 404 = NACK (bản gốc, `robotics-data-infra-roadmap.md`) | Địa chỉ 7 bit, ACK/NACK từng byte | ACK là xác nhận **tầng liên kết, từng byte** (gần TCP ACK hơn HTTP 200); không có checksum nên ACK không nói dữ liệu đúng; NACK có nghĩa bình thường (controller NACK byte cuối khi đọc xong) | Coi NACK cuối giao dịch đọc là lỗi; coi ACK là "cảm biến chạy đúng" |
| Mở/đóng connection | START/STOP, repeated START (Sr) | Không có bắt tay, không có trạng thái phiên ở target ngoài con trỏ thanh ghi. Sr giống **giữ khóa bus** giữa hai thao tác (để không ai chen vào giữa ghi-con-trỏ và đọc) hơn là giữ connection | Tách ghi-con-trỏ và đọc thành hai giao dịch có STOP ở giữa trên bus nhiều controller → đọc nhầm thanh ghi |
| Khóa phân tán có lease/TTL | Bus treo khi target giữ SDA thấp | I2C chuẩn **không có timeout**: người giữ "khóa" (SDA thấp) chết hay quên thì không ai thu hồi. SMBus (một biến thể) thêm timeout cỡ vài chục ms — chính là lease | Reset ESP32 mà không reset cảm biến → bus vẫn treo; tưởng lỗi phần mềm |
| Service discovery / DNS | Địa chỉ cố định theo chân SDO | Không có cơ chế chống trùng: hai thiết bị cùng địa chỉ **cùng ACK**, dữ liệu đọc ra là AND của hai bên, không ai báo lỗi | Gắn hai BME280 cùng địa chỉ → số rác "hợp lệ" |
| `tcpdump` trên một interface | Logic analyzer trên SDA/SCL | `tcpdump` không bỏ sót gói khi máy đủ nhanh và có timestamp kernel; logic analyzer chỉ thấy **những gì rơi vào cửa sổ capture** với **độ phân giải 1/sample-rate**, và chỉ thấy mức logic, không thấy hình dạng cạnh | Capture xong thấy "không có gì" và kết luận bus im lặng, trong khi giao dịch xảy ra ngoài cửa sổ |

**Chấm mô hình:**

- *"ACK là 200 OK, NACK là 404."* (bản gốc, bảng dịch trong roadmap) — **ĐÚNG MỘT PHẦN.** Đúng cho NACK ngay sau byte địa chỉ khi không ai có địa chỉ đó. Gãy ở ba chỗ. Phản ví dụ: (a) byte cuối của một giao dịch đọc luôn được **controller** NACK để báo "đủ rồi" — đó là thành công, không phải 404; (b) nhiều EEPROM NACK địa chỉ của chính nó trong lúc đang ghi nội bộ — gần 503 Busy hơn 404; (c) một BMP280 ở cùng địa chỉ ACK y hệt BME280 — ACK nói "có ai đó ở đây", không nói "đúng thiết bị".
- *Mô hình của bạn ở K3 lượt 2:* "…cách đọc/ghi, schema thì còn phải dùng các dây/chân khác kết hợp phối hợp quy định, như clock… [ESP32] không cần biết có ai nhận ở cuối dây." — với I2C: **SAI ở vế sau, ĐÚNG MỘT PHẦN ở vế trước.** Vế sau: I2C là bus có xác nhận; controller biết ở từng byte có ai nhận không (ACK), và target còn có thể **giữ SCL** để bắt controller chờ (clock stretching). Vế trước: clock cho biết *khi nào* lấy mẫu SDA, nhưng *khung* (START/STOP) được mã hóa ngay trên SDA bằng một chuyển mức "vi phạm luật" khi SCL cao; còn *schema* (thanh ghi 0xD0 nghĩa là gì) không có trên dây — nó nằm trong datasheet. Phản ví dụ: một logic analyzer decode hoàn hảo bus I2C mà không có datasheet chỉ cho bạn chuỗi byte, không cho bạn nhiệt độ. Vế "không cần biết ai nhận" đúng với I2S (Bài 13).
- *"Pull-up là chi tiết nối dây, module có sẵn là xong."* — **SAI.** Pull-up quyết định cạnh lên, tức tốc độ tối đa và độ dài dây cho phép, và quyết định dòng tiêu thụ mỗi khi dây ở mức thấp. Phản ví dụ: bus chạy ổn ở 100 kHz với dây 10 cm, hỏng ở 400 kHz hoặc với dây 50 cm, **không đổi một dòng code**.

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | I²C (I2C) | Bus hai dây SDA/SCL, nhiều thiết bị, có địa chỉ, open-drain | Giao thức "chậm nên đơn giản" |
| 🟢 | Controller / target (cũ: master / slave) | Bên phát clock và khởi tạo giao dịch / bên được gọi theo địa chỉ. UM10204 bản mới dùng tên controller/target | Hai bên ngang hàng |
| 🟢 | START, STOP, repeated START (Sr) | Ba điều kiện không phải dữ liệu: SDA đổi mức khi SCL cao | Byte đặc biệt |
| 🟢 | ACK / NACK | Bit thứ 9 của mỗi byte: bên nhận kéo SDA thấp (ACK) hoặc để cao (NACK) | HTTP status |
| 🟢 | Open-drain + pull-up | Thiết bị chỉ kéo xuống; điện trở kéo lên khi không ai giữ | Push-pull như GPIO thường |
| 🟢 | Standard-mode / Fast-mode | 100 kHz / 400 kHz SCL tối đa, mỗi chế độ có giới hạn cạnh lên riêng | Chỉ là con số trong `setClock` |
| 🟡 | Bus capacitance (Cb) | Tổng điện dung của dây và mọi chân trên bus | Không đáng kể |
| 🟡 | Rise time (t_r) | Thời gian dây đi từ 30% lên 70% VDD; do Rp·Cb quyết định | Do phần mềm |
| 🟡 | Clock stretching | Target giữ SCL thấp để bắt controller chờ | Lỗi |
| 🟡 | Bus clear / stuck bus | Target giữ SDA thấp sau khi controller reset; gỡ bằng 9 xung SCL hoặc cắt nguồn target | Lỗi ngẫu nhiên |
| 🟢 | Địa chỉ 7 bit vs byte địa chỉ 8 bit | 7 bit địa chỉ + 1 bit R/W tạo thành byte đầu; có tài liệu ghi địa chỉ dạng 8 bit (đã dịch trái) | Hai thiết bị khác nhau |
| 🟢 | Trigger (logic analyzer) | Điều kiện bắt đầu ghi (ví dụ cạnh xuống của SDA) | Không cần, cứ capture thật dài |
| 🔴 | SMBus, 10-bit addressing, multi-controller arbitration, High-speed mode | Biến thể và tính năng nâng cao; biết tên | — |

### 5. Dự đoán

**Tham số cần tra:**

| Tham số | Lấy ở đâu |
|---|---|
| Địa chỉ BME280 trên module của bạn | Bài 11 bước 6.2 (SDO nối đâu) + bảng địa chỉ trong datasheet |
| Pull-up trên module | Bài 11 bước 6.1 (đo bằng thang Ω khi không cấp nguồn) |
| Pull-up nội của ESP32-S3 | Datasheet ESP32-S3, bảng đặc tính DC của GPIO (R_PU) |
| Tần số SCL mặc định của `Wire` | Mã nguồn arduino-esp32 (`Wire.begin` → tần số 0 được thay bằng giá trị mặc định trong `esp32-hal-i2c*.c`) hoặc tài liệu Arduino-ESP32; **ghi phiên bản core bạn cài** |
| Chân SDA/SCL mặc định | File `pins_arduino.h` của biến thể board ESP32-S3 bạn chọn trong Arduino IDE, và pinout board thật |
| Giới hạn cạnh lên Standard/Fast, công thức Rp_min/Rp_max | NXP UM10204 *I2C-bus specification and user manual*, mục về pull-up resistor sizing |
| Hành vi của sketch scanner | Đọc mã `WireScan.ino` (File → Examples → Wire → WireScan): nó gửi gì, mỗi lần quét cách nhau bao lâu |

**Công thức/phương pháp:**
- Chu kỳ SCL = 1/f. Một lần "dò" một địa chỉ ≈ START + 9 bit + STOP ≈ 10–11 chu kỳ SCL, cộng khoảng nghỉ phần mềm giữa hai lần dò (không biết → ghi khoảng đoán).
- Thời lượng một vòng quét = số địa chỉ dò × thời gian mỗi lần. So với **cửa sổ capture** = số mẫu / sample rate. Kết luận: cần trigger hay không?
- Byte đầu tiên trên dây = `(địa chỉ 7 bit << 1) | R/W`.
- Cạnh lên `t_r ≈ 0.8473·Rp·Cb`. Ước lượng Cb: vài pF mỗi chân × số chân trên bus + dây jumper (đoán một khoảng, ghi `[ước lượng]`).
- Độ phân giải thời gian của capture = 1/sample rate. Đo một chu kỳ SCL sai ±1 mẫu; đo N chu kỳ liên tiếp thì sai số chia cho N.

**Mẫu `lab/04-i2c/prediction.md`:**

```markdown
# Dự đoán — I2C
Core arduino-esp32 phiên bản: __ · Board chọn trong IDE: __
Địa chỉ dự đoán: 0x__ (vì SDO nối __, đo ở Bài 11) — 7 bit nhị phân: _______
Byte đầu trên dây khi ghi: 0x__  · khi đọc: 0x__
Tần số SCL: __ kHz (nguồn: __) → chu kỳ __ µs
Pull-up hiệu dụng: module __ kΩ // ESP32 nội __ kΩ = __ kΩ
Cb ước lượng: __–__ pF → t_r ≈ __–__ ns; đạt Standard-mode? __ Fast-mode? __

Scanner: dò địa chỉ từ 0x__ đến 0x__, mỗi lần ≈ __ µs → một vòng ≈ __ ms; lặp mỗi __ s
Capture: sample rate __ MHz, __ mẫu → cửa sổ __ ms → cần trigger? __ (trigger trên kênh __, cạnh __)

Chuỗi nhãn decoder tôi kỳ vọng cho SCANNER tại địa chỉ của BME280: __
Chuỗi nhãn decoder tôi kỳ vọng cho SKETCH ĐỌC CHIP ID: __
Ở nhịp clock thứ 9 sau địa chỉ: SDA __ (ai kéo?), SCL __
```

`git commit -m "lab04: prediction"`.

### 6. Làm

**Bước 1 — nối dây.** ESP32-S3 với BME280:

| BME280 | ESP32-S3 | Ghi chú |
|---|---|---|
| VCC | 3V3 | **Không phải 5V** (Bài 11) |
| GND | GND | |
| SDA | GPIO 8 (mặc định của biến thể ESP32-S3 trong arduino-esp32) | |
| SCL | GPIO 9 (mặc định) | |

Kiểm tra chân trên board thật, vì mỗi biến thể DevKit đánh số và in nhãn hơi khác. **Thứ tự cấp nguồn:** cắm VCC/GND của cảm biến trước hoặc cùng lúc với SDA/SCL; đừng để cảm biến mất nguồn trong khi ESP32 vẫn chạy và kéo SDA/SCL lên (Bài 11, điều cấm về thứ tự cấp nguồn).

**Bước 2 — chạy I2C scanner.** Cài Arduino IDE, thêm board support ESP32 (Espressif), nạp **File → Examples → Wire → WireScan**. Mở Serial Monitor ở 115200. Đọc mã trước khi chạy: nó chờ bao lâu giữa các vòng quét, dò dải địa chỉ nào, in gì khi tìm thấy.

**Bước 3 — dự đoán, commit** (phần 5), **trước khi cắm logic analyzer.**

**Bước 4 — cắm logic analyzer.**

| Logic analyzer | Nối vào |
|---|---|
| **GND** | GND của mạch ← **không được quên** |
| D0 | SCL |
| D1 | SDA |

**Bước 5 — capture scanner.**
1. PulseView → sample rate **4 MHz** (đủ: ≥ 40 mẫu/chu kỳ SCL ở 100 kHz). Độ phân giải thời gian là 250 ns — ghi con số này cạnh mọi phép đo thời gian.
2. Đặt **trigger**: kênh SDA (D1), cạnh xuống. Số mẫu đủ cho một vòng quét theo dự đoán của bạn (1M mẫu ở 4 MHz = 250 ms).
3. Bấm **Run**. PulseView chờ tới khi SDA có cạnh xuống đầu tiên — tức START đầu tiên của vòng quét — rồi mới ghi.
4. Bấm nút decoder (biểu tượng zigzag) → **I²C** → gán SCL = D0, SDA = D1.
5. Zoom vào lần dò trùng địa chỉ BME280.

**Bước 6 — capture một giao dịch đọc chip ID** (mới — scanner chỉ dò địa chỉ, không đọc thanh ghi nào). Nạp sketch dưới đây, điền địa chỉ bạn dự đoán:

```cpp
// [chưa chạy] cần ESP32-S3 + BME280; kiểm API Wire theo phiên bản arduino-esp32 bạn cài
#include <Wire.h>
const uint8_t ADDR = 0x00;      // ĐIỀN địa chỉ 7 bit bạn dự đoán ở phần 5
void setup() {
  Serial.begin(115200);
  Wire.begin();                 // chân SDA/SCL mặc định của biến thể board
  Wire.setClock(100000);        // ghi rõ tần số, không dựa vào mặc định
}
void loop() {
  Wire.beginTransmission(ADDR);
  Wire.write(0xD0);             // đặt con trỏ thanh ghi = chip ID
  uint8_t err = Wire.endTransmission(false);    // false: không phát STOP → repeated START
  uint8_t n = Wire.requestFrom(ADDR, (uint8_t)1);
  Serial.printf("err=%u n=%u id=0x%02X\n", err, n, n ? Wire.read() : 0);
  delay(1000);
}
```

Capture lại với cùng trigger. Lưu file `.sr` (**File → Save**) và chụp màn hình phần đã decode — đây là **tiêu chí số 5 của Gate** (Bài 14).

**Bước 7 — đo.**
1. Chu kỳ SCL: đặt hai con trỏ cách nhau **9 cạnh lên** liên tiếp trong một byte, chia 9. Sai số đo = ±1 mẫu / 9.
2. Zoom vào nhịp clock thứ 9 sau địa chỉ: SDA ở mức nào trong lúc SCL cao? Ai đang kéo nó?
3. Đếm: trong vòng quét, có bao nhiêu địa chỉ được ACK?

**Bước 8 (tùy chọn, 30 phút) — nhìn thấy pull-up bằng thời gian.** Chuyển sample rate lên 24 MHz (độ phân giải ~42 ns). Đo độ rộng mức cao và mức thấp của SCL. Gắn thêm một điện trở 4.7 kΩ từ SCL lên 3.3 V (song song với pull-up module; kiểm trước rằng tổng song song vẫn > Rp_min), đo lại. Logic analyzer không thấy hình dạng cạnh, nhưng thấy **thời điểm dây vượt ngưỡng logic** dịch đi khi cạnh lên nhanh/chậm hơn `[tự đo]`. Muốn thấy hình dạng thật phải có oscilloscope (🟡, chưa cần mua).

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

**Serial Monitor (scanner):** `I2C device found at address 0x76` (hoặc `0x77` nếu SDO nối VCC).

**Decoder — scanner:** mỗi địa chỉ là một lần dò ngắn:
```
START | Address write: 75 | NACK | STOP      ← không ai ở 0x75
START | Address write: 76 | ACK  | STOP      ← BME280
START | Address write: 77 | NACK | STOP
```
Không có byte dữ liệu nào: scanner chỉ hỏi "có ai ở địa chỉ này không".

**Decoder — sketch chip ID** (đây là chuỗi bản gốc đưa ra, nhưng nó chỉ xuất hiện với sketch đọc thanh ghi, không với scanner):
```
START | Address write: 76 | ACK | Data write: D0 | ACK | START (repeated) | Address read: 76 | ACK | Data read: 60 | NACK | STOP
```
Serial in `err=0 n=1 id=0x60`. NACK cuối là **controller** báo "đọc đủ một byte" — bình thường.

**Byte địa chỉ trên dây:** `0x76 = 1110110`; khi ghi byte đầu là `11101100 = 0xEC`, khi đọc là `0xED`. Một số tài liệu/thư viện gọi BME280 là "0xEC" — cùng một thiết bị, ghi kiểu 8 bit.

**Chu kỳ SCL ≈ 10 µs (100 kHz)**, đo trên 9 chu kỳ ở 4 MHz: sai số đo ±250 ns/9 ≈ ±0.3%. Thực tế có thể dài hơn 10 µs vài phần trăm: thời gian cạnh lên chậm có thể bị cộng vào chu kỳ, tùy cách bộ điều khiển I2C đếm `[tự đo]`. Nếu ra ≈ 2.5 µs: thư viện đang chạy 400 kHz — **không sai, sửa lại dự đoán và giải thích, đừng sửa số đo.**

**Nhịp thứ 9 sau địa chỉ:** SDA THẤP trong khi SCL cao — target (BME280) kéo xuống. Đó là ACK, nhìn tận mắt.

**Thời lượng vòng quét:** 126 lần dò × (~0.1 ms trên dây + khoảng nghỉ phần mềm) ≈ vài chục ms `[ước lượng — tự đo]`; WireScan chờ 5 s giữa hai vòng. Nếu "Run rồi bấm reset" như bản gốc, cửa sổ 250 ms gần như chắc chắn rơi vào khoảng chờ 5 s → capture trống. Trigger giải quyết việc này.

**Bảng cạnh lên** (từ mô phỏng; t_r tính bằng ns; F = đạt cả Fast-mode 300 ns, S = chỉ đạt Standard-mode 1000 ns, x = trượt cả hai):

| Rp \ Cb | 20 pF | 50 pF | 100 pF | 200 pF | 400 pF |
|---|---|---|---|---|---|
| 2.2 kΩ | 37 F | 93 F | 186 F | 373 S | 746 S |
| 4.7 kΩ | 80 F | 199 F | 398 S | 796 S | 1593 x |
| 10 kΩ | 169 F | 424 S | 847 S | 1695 x | 3389 x |
| 45 kΩ (pull-up nội ESP32) | 763 S | 1906 x | 3813 x | 7626 x | 15251 x |

Rp_min = (3.3 − 0.4) V / 3 mA ≈ 967 Ω. Đọc bảng: pull-up nội ~45 kΩ chỉ đạt Standard-mode khi bus cực ngắn — đó là lý do một bus **không có pull-up ngoài vẫn "chạy được" ở bàn** (driver bật pull-up nội) rồi hỏng khi dây dài ra hoặc lên 400 kHz. Breadboard + jumper + hai module thường rơi vào vùng vài chục tới ~100 pF `[ước lượng]`.

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Cả SCL và SDA thẳng HIGH, không có gì | Code chưa chạy; analyzer chưa nối GND; capture rơi vào khoảng chờ giữa hai vòng quét | Serial Monitor có in không; trigger đã đặt chưa | Nối GND; đặt trigger cạnh xuống SDA |
| Cả hai thẳng LOW | Chập SDA/SCL xuống GND; một target đang giữ bus; cảm biến mất nguồn còn chân bị kéo (Bài 11) | Đo áp SDA/SCL khi không chạy code; rút cảm biến ra xem dây có lên không | Gỡ chập; cắt nguồn cảm biến rồi cấp lại; "bus clear" 9 xung SCL |
| Thấy sóng nhưng decoder báo lỗi | Gán nhầm kênh SCL/SDA; sample rate quá thấp | Kênh nào đều đặn (là SCL)? | Đổi kênh trong decoder; tăng sample rate |
| **NACK** sau địa chỉ | Sai địa chỉ, hoặc cảm biến chưa được cấp nguồn | Thử địa chỉ còn lại; đo VCC của cảm biến (~3.3 V) | Sửa địa chỉ / nguồn |
| Scanner không tìm thấy gì | Nối nhầm SDA/SCL (lỗi phổ biến nhất); sai chân mặc định | Đảo hai dây; đối chiếu `pins_arduino.h` | Đảo dây hoặc `Wire.begin(sda, scl)` |
| Scanner báo thấy thiết bị ở **mọi** địa chỉ, hoặc lỗi timeout hàng loạt | SDA bị giữ thấp → mọi bit thứ 9 đều "ACK" (AND của dây) | Capture: SDA có lên cao lại không | Như dòng "thẳng LOW" |
| Chu kỳ SCL ≈ 2.5 µs thay vì 10 µs | Thư viện/cấu hình đang chạy 400 kHz | `Wire.getClock()` | **Sửa lại dự đoán và giải thích, đừng sửa số đo** |
| `id=0x58` (hoặc 0x56/0x57) | Module là **BMP280**, không phải BME280 | Bài 11, Table 17 | Ghi vào notebook; không có kênh độ ẩm |
| Decoder hiện địa chỉ 0x76, tài liệu khác ghi 0xEC | Cách ghi 7 bit vs 8 bit | `0x76 << 1 = 0xEC` | Không phải lỗi |
| Chạy ổn với dây ngắn, lỗi lác đác khi dây dài | Cạnh lên quá chậm (Rp·Cb) | Bước 8 | Pull-up ngoài nhỏ hơn (trong khoảng hợp lệ) hoặc giảm tốc độ |

Dòng "chu kỳ 2.5 µs" đáng đọc lại. Khi số đo khác dự đoán, thứ phải thay đổi là **hiểu biết của bạn**, không phải số đo.

### 9. Câu hỏi ngược

1. **[Nếu…thì]** Nếu gắn hai BME280 cùng địa chỉ lên một bus, scanner in gì, và dữ liệu đọc chip ID ra gì? Có lỗi nào được báo không?
   <details><summary>Hướng nghĩ</summary>Hai target cùng ACK (AND của hai lần kéo xuống vẫn là thấp). Dữ liệu là AND bit-wise của hai bên: chip ID giống nhau nên vẫn ra đúng; nhiệt độ thì ra rác "hợp lệ". Lời giải: chân SDO, bộ mux I2C, hoặc bus thứ hai. Đây là kiểu lỗi mà kiểm "health" bằng chip ID không bắt được.</details>
2. **[Quy mô]** Một cánh tay robot có 8 cảm biến I2C trải trên dây dài 50 cm, chạy cạnh dây motor. Cái gì gãy trước: tốc độ, nhiễu, hay địa chỉ? Bạn đổi gì đầu tiên?
   <details><summary>Hướng nghĩ</summary>Cộng Cb: 8 thiết bị + dây dài → tra bảng t_r. Nhiễu từ motor ghép vào dây single-ended có trở kháng cao lúc ở mức cao (chỉ có pull-up giữ). Từ đó hiểu vì sao robot thật dùng CAN (vi sai) hoặc đặt MCU sát cảm biến và gửi số qua bus khác.</details>
3. **[Failure mode]** ESP32 bị watchdog reset đúng lúc BME280 đang gửi bit 0 của byte dữ liệu. Sau reset, mọi lệnh I2C đều lỗi. Vì sao reset ESP32 không chữa được, và firmware nên làm gì lúc khởi động?
   <details><summary>Hướng nghĩ</summary>Target vẫn đang chờ clock để gửi nốt byte, nên giữ SDA. Lúc boot, kiểm SDA; nếu thấp, phát xung SCL thủ công tới khi SDA nhả, rồi phát STOP. So với lease: I2C chuẩn không có TTL, nên chính bạn phải làm việc thu hồi. Ở K3 Bài 16 bạn sẽ gặp watchdog hai tầng — tầng này là một ca cho nó.</details>
4. **[Vì sao không]** Vì sao I2C không dùng đầu ra push-pull như SPI để có cạnh lên nhanh?
   <details><summary>Hướng nghĩ</summary>Nghĩ tới ACK và clock stretching: ai lái dây đổi theo từng bit. Hai đầu ra push-pull lái ngược nhau là đoản mạch. Open-drain đổi tốc độ lấy khả năng chia dây an toàn. SPI tránh vấn đề bằng cách mỗi dây chỉ một bên lái và mỗi thiết bị một chân CS.</details>
5. **[Liên ngành]** CAN bus trong ô tô dùng bit "dominant" và "recessive". Giống open-drain của I2C ở đâu, và CAN dùng nó để làm gì mà I2C trong bài này không dùng?
   <details><summary>Hướng nghĩ</summary>Dominant thắng recessive y như mức thấp thắng mức cao. CAN dùng nó để **trọng tài không phá hủy** khi nhiều nút gửi cùng lúc: nút gửi recessive mà đọc lại thấy dominant thì biết mình thua và rút lui. I2C multi-controller cũng có trọng tài kiểu này (🔴), còn Ethernet đời đầu thì phát hiện va chạm và cả hai bên đều phải gửi lại.</details>
6. **[Phản biện]** "Thấy ACK là cảm biến chạy đúng." Bác bỏ bằng ít nhất hai phản ví dụ từ bài này và Bài 11.
   <details><summary>Hướng nghĩ</summary>Chip khác cùng địa chỉ; cấu hình chưa có hiệu lực (ctrl_hum); đọc rách vì không burst read; cảm biến hỏng vẫn trả lời bus. ACK là bằng chứng tầng liên kết; chất lượng dữ liệu cần kiểm ở tầng khác (→ F3.7, K5 Bài 16).</details>

### 10. Liên kết ra ngoài

- **CAN bus.** Giống: cùng ý tưởng "mức trội thắng" trên một dây chung, cho phép nhiều nút chia một môi trường mà không đoản mạch. Khác: CAN vi sai (chống nhiễu, chạy hàng chục mét), có CRC và cơ chế tự cô lập nút lỗi; I2C single-ended, không CRC, sinh ra cho khoảng cách vài chục cm trong một bo mạch.
- **Khóa phân tán có lease (Chubby, etcd).** Giống: một bên giữ tài nguyên chung (SDA thấp) chặn mọi bên khác. Khác: hệ phân tán học được từ đau khổ rằng người giữ khóa có thể chết, nên khóa có TTL; I2C nguyên bản không có, nên "bus treo" là lớp lỗi kinh điển. SMBus thêm timeout chính là thêm lease.
- **Ethernet đời đầu (CSMA/CD).** Giống: nhiều nút một môi trường. Khác: va chạm trên Ethernet phá hủy cả hai khung; trọng tài trên I2C/CAN giữ nguyên khung của bên thắng. Cùng bài toán chia sẻ môi trường, hai triết lý khác nhau về cái giá của xung đột.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| I²C do Philips tạo ra đầu thập niên 1980 | [chuẩn] | Lịch sử I²C; NXP là hậu thân mảng bán dẫn của Philips |
| Giới hạn t_r: 1000 ns (Standard), 300 ns (Fast); Cb tối đa 400 pF; t_r = 0.8473·Rp·Cb; Rp_min = (VDD − V_OL)/I_OL với V_OL 0.4 V ở 3 mA | [spec] | NXP UM10204, mục về đặc tính điện và chọn pull-up; kiểm theo revision bạn tải |
| Mục "Bus clear" — 9 xung SCL | [spec] | UM10204 |
| Arduino-ESP32: tần số mặc định 100 kHz, bật pull-up nội, SDA=8/SCL=9 cho ESP32-S3, scanner tên `WireScan`, dò địa chỉ 0x01–0x7E, chờ 5 s | [spec] | Mã nguồn repo `espressif/arduino-esp32` (nhánh master khi soạn bài); **kiểm theo phiên bản core bạn cài** |
| Pull-up nội ESP32-S3 ~45 kΩ | [spec] | Datasheet ESP32-S3, bảng DC characteristics (R_PU) — kiểm lại |
| Chu kỳ SCL đo được có thể dài hơn danh định vì cạnh lên | [tự đo] | Phụ thuộc bộ điều khiển I2C và Rp·Cb |
| Cb breadboard vài chục tới ~100 pF | [ước lượng] | Vài pF mỗi chân + dây jumper |
| SMBus timeout cỡ 25–35 ms | [spec] | SMBus specification (System Management Interface Forum), tham số t_TIMEOUT |

**Đã sửa so với bản gốc:**
- **Chuỗi decode kỳ vọng sai nguồn:** bản gốc hứa thấy `Data write: D0 … Data read: 60` khi chạy **scanner**; scanner chỉ dò địa chỉ (START, địa chỉ, ACK/NACK, STOP). Đã thêm bước 6 với sketch đọc chip ID, nơi chuỗi đó thật sự xuất hiện.
- **Cửa sổ capture:** bản gốc dùng 4 MHz × 1M mẫu (= 250 ms) và "Run rồi bấm reset"; WireScan chờ 5 s trước mỗi vòng quét → gần như chắc chắn bắt trượt. Đã thêm trigger cạnh xuống SDA.
- Tên ví dụ `Wire/i2c_scanner` → trong core arduino-esp32 là **WireScan**.
- "START … là dấu hiệu duy nhất không phải dữ liệu" → START, repeated START và STOP đều là điều kiện không phải dữ liệu.
- "ACK là 200 OK, NACK là 404" → chấm ĐÚNG MỘT PHẦN, kèm phản ví dụ (NACK cuối đọc là bình thường).
- "Pull-up thường 4.7 kΩ" → giá trị là một khoảng [Rp_min, Rp_max] theo Cb và tốc độ; thêm mô phỏng.
- "Cả hai thẳng LOW → thiếu pull-up": trên ESP32 driver bật pull-up nội nên thiếu pull-up ngoài thường **không** cho mức LOW mà cho cạnh lên chậm; LOW liên tục nghi chập hoặc bus treo trước.
- Đo chu kỳ SCL qua 9 chu kỳ thay vì một cặp cạnh, để sai số do độ phân giải 250 ns nhỏ hơn sai số cần kiểm.

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** NXP, *UM10204 — I2C-bus specification and user manual* (bản mới nhất); datasheet BME280 mục giao tiếp I2C (Bài 11).
- **Giải thích:** SparkFun tutorial "I2C"; sigrok/PulseView docs, phần protocol decoder và trigger.
- **Đào sâu (tùy chọn):** Ben Eater (YouTube), các video về bus; tài liệu ESP-IDF Programming Guide, mục I2C master driver (để thấy driver làm gì bên dưới `Wire`).
- **Tự kiểm tra:** (1) giải thích lại cho một backend engineer khác trong 5 câu vì sao I2C cần pull-up và vì sao ACK không phải HTTP 200; (2) vẽ lại hình open-drain + Cb và chuỗi một giao dịch đọc thanh ghi từ trí nhớ; (3) hai câu dưới.
  1. Bus 400 kHz, Cb ước lượng 150 pF. Rp lớn nhất là bao nhiêu? Pull-up 10 kΩ trên module có đủ không?
  2. Capture ở 4 MHz, bạn đo một chu kỳ SCL bằng hai con trỏ ra 10.25 µs. Kết luận "SCL chậm 2.5%" có đứng được không?

<details><summary>Đáp án</summary>

1. Rp_max = 300 ns / (0.8473 × 150 pF) ≈ 2.36 kΩ. 10 kΩ không đủ (t_r ≈ 1.27 µs); cần pull-up ngoài nhỏ hơn, song song với 10 kΩ, sao cho tổng trong khoảng ~1–2.3 kΩ.
2. Không. Độ phân giải 250 ns, nên một chu kỳ đo được là 10.00 ± 0.25 µs; 10.25 µs chỉ lệch đúng một mẫu. Đo trên 9 chu kỳ (hoặc hơn) trước khi kết luận.

</details>

---
