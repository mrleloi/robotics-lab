# Chặng 10 — An toàn và vận hành (60h + 16h tùy chọn)

> **Vị trí:** C8 (điều hướng; C9 nhận người chạy song song hoặc trước) → **C10** → C11 (sim twin, HIL, CI), C12 (sản phẩm) · **Cần trước:** C1 trọn (điểm cắt E-stop, cầu chì cuộn FD 1 A → K7 C1.3), C4 trọn (bảng chân, lease, kẹp tốc độ, ARM/DISARMED → K7 C4.4), C5.3 (E-stop tạm, teleop), C8.4 (Nav2 chạy A→B); K3 Bài 15–17 (kill switch, watchdog hai tầng, soak 72h); viên nang → F7.6, F5.3, F7.7, đọc lại → F5.7, F7.4, F1.4 · **Chạy song song với:** K6
> **Làm ra được:** chuỗi E-stop cứng (nút NC → cuộn relay → MOSFET "xung giữ"), bumper hai bên, watchdog phần cứng độc lập với firmware ESP32, đường đo trạng thái relay; state machine có bảng chuyển đầy đủ · bảng thời gian phản ứng từng tầng đo bằng logic analyzer kèm quãng dừng, bảng FMEA có S/O/D đã test bằng lỗi thật, soak 72h trong văn phòng với hợp đồng SLO, dashboard vận hành, báo cáo "Failure mode analysis for a small office robot" · **Sau chặng này bạn quyết định được:** cái gì cắt năng lượng motor và nó độc lập với những gì; E-stop của robot là dừng loại 0 hay loại 1 và vì sao; dòng FMEA nào sửa trước; robot đã được phép chạy trong văn phòng không người trông chưa.

C4 làm cho firmware **tự dừng** khi host im lặng hoặc gửi lệnh vô lý. C5 gắn một E-stop tạm. Cả hai vẫn có cùng một điểm yếu: chúng tin vào ESP32. C10 trả lời câu hỏi còn lại của K7: **khi chính bộ điều khiển hỏng, cái gì dừng robot?** Rồi nó đưa robot ra văn phòng có người thật 72 giờ, và đo xem toàn bộ hệ có giữ được lời hứa không.

**Phân bổ 60h** `[ước lượng]` (giữ giờ của K7 gốc Bài 15, 16, 17):

| Phần | Giờ |
|---|---|
| Bài C10.1 An toàn là một tầng phần cứng (K7 gốc Bài 15) | 16 |
| Bài C10.2 State machine và FMEA (K7 gốc Bài 16) | 18 |
| Bài C10.3 Soak 72h trong văn phòng thật (K7 gốc Bài 17) | 16 người + 72 treo máy |
| Lắp bước 1–7: bo an toàn, nút E-stop trên thân, bumper, watchdog ngoài, đường đo relay, nút RESET, kiểm trước khi chạy | 7 |
| Gate chặng 10 (gồm bài viết) | 3 |
| **Tổng lõi** | **60** |
| Bài C10.4 HRI đo được *(tùy chọn, K7 Phụ lục C)* | +16 |

Đường lõi tối thiểu của K7 (`_KE-HOACH-K7.md` mục 3) gồm C10.1–C10.2 (34h). C10.3 cần C8 chạy được; nếu đi đường tối thiểu, làm soak 72h ở chế độ teleop/tuần tra cố định thay cho Nav2 và ghi rõ trong báo cáo.

## 0. Bức tranh chặng

Robot sau chặng này. Khối **mới** đánh dấu `*`; còn lại đã có từ C1–C9.

```
                         ┌────────────────────────── MINI PC N100 ──────────────────────────┐
                         │ Nav2 (C8) · nhận người (C9) · *state machine* · MCAP sidecar (C7) │
                         │ *ops_exporter* (metrics soak) · ros2_control hardware interface    │
                         └───────────────┬────────────────────────────────────▲───────────┘
                                         │ CMD (seq, ω, lease) 50–100 Hz       │ STATE 100 Hz
                                         ▼                                     │ (+ fault_mask, estop, relay)
 ┌───────────────────────── ESP32-S3 (vòng 100 Hz, C4) ─────────────────────────────────────┐
 │ lease + kẹp tốc độ (C4.4) · *ISR bumper* · *đọc ESTOP_SENSE, RELAY_FB* · *RESET*        │
 │ *đảo RELAY_HOLD từ CHÍNH task điều khiển, chỉ khi mọi kiểm tra đạt*                       │
 └───────┬─────────────────────────┬────────────────────────────┬──────────────────────────┘
         │ RELAY_HOLD (xung)        │ PWM/DIR/DRV_EN              │ BUMPER_L/R (NC), ENC
         ▼                          ▼                             ▲
  *[MẠCH XUNG GIỮ]* ──► gate Q1     DRIVER ──► MOTOR L/R ─────────┘
                         │          ▲ VM
 PACK 4S ─FD 1A─[E-STOP NC]─[cuộn K1]─┘(Q1 hạ cuộn xuống GND)
     └──FA 10A──[tiếp điểm K1: 30→87]──► VM driver          30→87a (khi nhả) ──► *RELAY_FB*
```

Ba đường dừng **không chung điểm hỏng đơn** với nhau ở phía "dừng":
1. **Người nhấn nút** → chuỗi cuộn hở → relay nhả → mất VM. Không đi qua chip nào.
2. **ESP32 treo / reset / mất nguồn** → chân RELAY_HOLD ngừng đảo → mạch xung giữ xả → Q1 tắt → relay nhả. Không cần ESP32 "quyết định" gì.
3. **ESP32 sống, phát hiện lỗi** (bumper, lease hết hạn, tốc độ đo vượt, encoder vô lý) → hãm có điều khiển, DRV_EN thấp, và ngừng đảo RELAY_HOLD.

Mini PC không nằm trên đường dừng nào. Nó chỉ có thể **xin** dừng (tầng 3) hoặc **ngừng xin chạy** (lease hết hạn → tầng 2).

Dòng dữ liệu mới: sự kiện an toàn (`estop`, `bumper`, `wd_trip`, `relay_fb`) trong STATE → `/diagnostics` + topic sự kiện → MCAP; chuyển trạng thái của state machine → log JSONL có lý do; capture logic analyzer của mỗi lần đo phản ứng → `captures/c10/`; metric soak → dashboard.

## 1. An toàn của chặng

**Rủi ro cụ thể của C10** (theo mức nặng):
1. **Robot chạy khi bạn tin nó đã dừng.** Chặng này cố ý gây lỗi (rút encoder, treo ESP32, `kill` tiến trình) trên robot có động lực. Mỗi phép thử là một lần robot có thể chạy theo lệnh cũ.
2. **Va chạm người trong soak.** Robot 5 kg `[ước lượng — số cân ở C2.4]` chạy giữa đồng nghiệp 72 giờ. Người không biết thí nghiệm, trẻ em, người dùng gậy, người cúi buộc dây giày.
3. **Lật/rơi:** bậc cửa, cầu thang, mép bàn khi chạy thử trên bàn.
4. **Tiếp điểm relay dính** (hồ quang DC khi cắt dòng lớn): E-stop nhấn mà VM còn.
5. **Quá áp VM khi relay mở lúc motor đang quay** (motor thành máy phát, nạp tụ đầu vào driver qua diode thân MOSFET).
6. **Pin trong soak:** sạc ngoài giờ, robot nằm trong văn phòng ban đêm có pack lithium.

**Quy tắc cứng** (cộng thêm quy tắc C0, C1, C4, C5):
- KHÔNG gây lỗi (fault injection) nào khi E-stop cứng chưa PASS bước kiểm ở Lắp bước 7. Thứ tự là C10.1 trước C10.2, không đảo.
- KHÔNG thử lỗi lần đầu trên sàn. Lần đầu mỗi kịch bản: robot kê trên giá, **bánh không chạm đất**, tay kia đặt trên nút E-stop. Chỉ khi PASS trên giá mới thử trên sàn, tốc độ thấp trước.
- KHÔNG đứng trước hướng chạy của robot khi thử lỗi trên sàn. Đứng sau hoặc bên cạnh, cách ≥1 m, cầm nút E-stop không dây hoặc đứng cạnh nút trên thân.
- KHÔNG dựa vào "E-stop" phần mềm (nút trên app, topic ROS, kill switch MQTT của K3) làm đường dừng duy nhất trong bất kỳ phép thử nào.
- KHÔNG cắm nguồn ESP32 từ USB của mini PC làm nguồn **duy nhất** (C1 đã cấp buck 5 V riêng). Rút USB phải không làm ESP32 mất điện.
- KHÔNG để nhả nút E-stop làm robot chạy lại. Phải có hành động reset có chủ đích (Lắp bước 6).
- KHÔNG thay nút E-stop bằng công tắc thường mở (NO) hay nút nhấn nhả. Chỉ dùng nút nấm NC tự khóa, xoay/kéo để nhả.
- KHÔNG đưa robot vào soak khi chưa có: biển báo trên thân ("Robot thử nghiệm — nhấn nút ĐỎ để dừng — liên hệ <tên, số máy>"), sự đồng ý của người quản lý văn phòng, khu vực đã loại cầu thang/bậc (hoặc cảm biến vực đã test), và lịch sạc **có người** (C1.6).
- KHÔNG chạy soak qua đêm khi không có người trong tòa nhà nếu robot đang sạc. Robot đỗ, tắt công tắc chính, hoặc sạc có người trông.
- KHÔNG đo VM, cuộn relay hay chuỗi E-stop bằng logic analyzer mà không qua cầu phân áp hoặc opto. 14,6 V vào kênh logic analyzer là cháy kênh (và có thể cổng USB laptop).

**Khi sự cố xảy ra:**

| Tình huống | Làm ngay | KHÔNG làm |
|---|---|---|
| Robot không dừng khi nhấn E-stop | Công tắc chính OFF; nếu robot đang chạy về phía người: chặn bằng vật mềm (ghế có đệm, thùng carton), không bằng chân tay | Đuổi theo và túm bánh; giữ nút nhấn rồi nhìn |
| Robot chạm người trong soak | Nhấn E-stop; hỏi người có sao không; dừng soak; ghi near miss/sự cố với thời gian, tốc độ (từ log), khoảng cách | Tiếp tục soak "vì chỉ chạm nhẹ"; sửa log |
| Mùi khét, khói từ bo an toàn/relay | Công tắc chính OFF, rút XT60 (theo C1) | Nhấn E-stop rồi bỏ đi (E-stop không cắt compute và bo nguồn) |
| Relay dính (VM còn sau E-stop) | Công tắc chính OFF; đánh dấu relay hỏng; thay; ghi vào FMEA như một sự cố thật | Gõ relay cho nhả rồi dùng tiếp |

Sau mỗi sự cố hoặc near miss: postmortem không đổ lỗi một trang (→ F7.7), một dòng FMEA mới hoặc sửa dòng cũ, một test mới (hạt giống HIL cho C11.2).

## 2. BOM chặng

Phần lớn đã có (relay K1 và nút E-stop từ C1, opto từ C4, bumper nếu đã gắn ở C5). Giá `[ước lượng 10/2026]`, kiểm lại ở cửa hàng. Tổng K7 gốc cho đợt này: ~1tr.

| Món | Thông số phải chọn | Vì sao (bằng số) | Giá | Kiểm khi nhận hàng | Thay thế được bằng |
|---|---|---|---|---|---|
| Nút E-stop nấm **thứ hai** gắn trên thân (hoặc thay nút C1) | NC, **mở cưỡng bức** (positive opening, ký hiệu ⊝ trên khối tiếp điểm), tự khóa, xoay để nhả, đầu ≥30 mm màu đỏ trên nền vàng | Mở cưỡng bức: cơ cấu ép tiếp điểm NC tách ra kể cả khi tiếp điểm bị dính `[spec — IEC 60947-5-1 phụ lục K; kiểm ký hiệu trên khối tiếp điểm]` | 100–300k | Đo: chưa nhấn thông, nhấn hở, xoay thông lại; nhìn ký hiệu ⊝ | Nút C1 nếu đã đạt các thông số này |
| Relay K1 loại **5 chân (changeover)** | 12 V, tiếp điểm 30/87/87a, ≥30 A; datasheet ghi **thời gian nhả** và định mức tiếp điểm DC | Chân 87a cho tín hiệu "relay đã nhả" độc lập với VM (mục 4). Định mức DC thấp hơn AC `[chuẩn]` | 50–150k | Cấp 12 V vào cuộn: 30–87 thông; bỏ điện: 30–87a thông | Relay 4 chân của C1 + đo VM (kém hơn, mục 4) |
| Zener 18–24 V (1 W) + diode 1N4007 | Áp Zener + áp pack đầy < Vds max của Q1 | Diode + Zener cho dòng cuộn tắt nhanh hơn chỉ diode → relay nhả nhanh hơn `[chuẩn — app note coil suppression của hãng relay; tự đo]` | <20k | Đo chế độ diode | TVS hai chiều |
| MOSFET kênh N logic-level (Q1) | Vgs(th) ≤1,5 V, Rds(on) **ghi ở Vgs = 2,5 V**, Vds ≥40 V, gói SOT-23 hoặc TO-220 | Cổng chỉ được lái bằng mạch xung giữ (~2 V, mục 4); dòng cuộn relay ~100–200 mA `[spec — đo ở C1]` | 5–20k | Đo chế độ diode thân D–S | Transistor NPN + điện trở (tính lại mạch) |
| Linh kiện mạch xung giữ | 2 tụ 1 µF (gốm, ≥10 V), 2 diode Schottky (BAT54/1N5819), 100 kΩ, 10 kΩ kéo xuống | Mô phỏng ở Bài C10.1 phần 2 | <30k | — | IC supervisor có watchdog (phương án C, Bài C10.1) |
| MCU giám sát thứ hai *(phương án B, tùy chọn)* | ESP32-C3 hoặc RP2040 bo nhỏ, **nguồn LDO riêng** | Giám sát độc lập có thêm logic (tốc độ đo được) | 80–200k | Nạp blink | — |
| Bumper ×2 | Công tắc hành trình (microswitch có cần lăn) **dùng chân NC**, thanh cản mềm (xốp EVA/ống PU) phủ mặt trước | Đứt dây = "đã va" (hỏng về phía an toàn, bảng chân C4) | 50–150k | Đo NC thông khi chưa ấn; lực ấn để kích (cân hành lý C0) | Thanh cản + 2–3 công tắc song song logic (nối tiếp NC) |
| Cảm biến vực *(nếu khu soak có bậc)* | IR khoảng cách hướng xuống (ví dụ Sharp GP2Y0A41) hoặc ToF VL53L0X | Phát hiện mép bậc trước bánh trước | 100–250k ×2 | Đo trên sàn tối màu và sàn sáng | Loại khu có bậc khỏi bản đồ (Nav2 keepout) |
| Nút RESET | Nút nhấn NO nhỏ, gắn cạnh E-stop, có nắp hoặc lõm để không chạm nhầm | Khởi động lại là hành động có chủ đích, tại robot `[spec — IEC 60204-1 9.2.3.4 / ISO 13850: reset không tự khởi động lại]` | 20–50k | Đo NO | Nút trên app teleop (kém hơn: không tại máy) |
| Cầu phân áp đo | 47 kΩ / 10 kΩ ×3 (VM_SENSE, RELAY_FB, COIL_SENSE) + tụ 100 nF | 14,6 V → ≈2,6 V, an toàn cho ESP32 và logic analyzer | <20k | Đo tỉ số trên nguồn bàn | Opto PC817 |
| TVS trên VM driver | Đơn hướng, áp đánh thủng trên áp pack đầy (ví dụ dòng SMBJ 18–20 V; tra datasheet) | Kẹp xung khi relay mở lúc motor quay | 10–30k | Đúng cực | Tụ bulk lớn hơn (không thay được hoàn toàn) |
| Biển báo, dây buộc, băng dính sàn | In A5 ép plastic | Người lạ biết đây là gì và dừng nó thế nào | 30–50k | — | — |
| Nhiệt kế/ẩm kế log (tùy chọn) | BME280 đã có từ K1 | Soak ghi nhiệt độ môi trường | 0 | — | — |

**Tổng C10 `[ước lượng]`:** ~0,7–1,5tr (không tính MCU thứ hai, cảm biến vực).

## 3. Dụng cụ và kỹ năng tay

| Kỹ năng | Bài | Luyện trước | Đạt trông thế nào |
|---|---|---|---|
| Hàn mạch nhỏ trên bo đục lỗ (mạch xung giữ, cầu phân áp) | Lắp bước 1 | Một cầu phân áp thừa | Mối bóng; không cầu thiếc giữa hai lỗ; đo Ω từng nhánh trước khi cấp điện |
| Gắn nút E-stop trên thân: khoan lỗ 22 mm, chống xoay | Lắp bước 2 | Lỗ trên tấm phế liệu cùng vật liệu | Nút không xoay khi vặn nhả; đầu nấm cao hơn mọi thứ xung quanh; với được từ phía sau và hai bên |
| Cơ khí bumper: hành trình, điểm kích | Lắp bước 3 | Gá một công tắc trên tấm gỗ, ấn bằng cân | Kích ở lực nhỏ (ghi N) **trước** khi thân robot chạm vật; nhả về đúng vị trí |
| Logic analyzer 6 kênh, trigger theo cạnh, đọc thời gian giữa hai cạnh | C10.1 | K5 Bài 8, C4.2 | Biết sai số mỗi cạnh; biết định nghĩa "cạnh" khi tiếp điểm rung |
| Gây lỗi có kịch bản (fault injection) | C10.2 | — | Mỗi lần có: trạng thái robot, tay ở nút E-stop, ghi trước kết quả mong đợi |

**Đo trên chuỗi có tiếp điểm cơ khí:** khi nút E-stop mở, tiếp điểm **rung** (bounce) vài trăm µs tới vài ms `[ước lượng — đo]`. Logic analyzer 24 MHz thấy từng lần rung. Quy ước của chặng: thời điểm kích hoạt là **cạnh đầu tiên** chuỗi hở; thời điểm kết thúc là **cạnh đầu tiên** của tín hiệu đích sau đó ổn định ≥10 ms. Ghi quy ước này vào `captures/c10/README.md` để mọi số đo cùng nghĩa.

## 4. Sơ đồ đi dây

Mở rộng chuỗi cuộn của C1 (FD 1 A → nút E-stop NC → cuộn K1 → GND). Thay đổi: thêm Q1 ở phía thấp của cuộn, mạch xung giữ, ba đường đo. Màu theo C0.5; dây chuỗi E-stop có nhãn đỏ ở hai đầu (C0.5).

```
  THANH CÁI + ──[FD 1A]──┬──[E-STOP NC ⊝]──●COIL_SENSE──[cuộn K1 (85→86)]──┬── D Q1 (AO3400 hoặc tương đương)
  (VBAT 10–14,6 V)       │                  │                  ║ D1 1N4007    │   S ── GND sao
                         │                47k                  ║ nối tiếp     │   G ◄── mạch xung giữ
                         │                  ├──► ESTOP_SENSE   ║ Zener 20 V   │
                         │                10k  (GPIO41, qua    ║ (dập nhanh)  │
                         │                  ┴   100 nF)        ╚═════════════╝
                         │
  THANH CÁI + ──[FA 10A]──── 30 ●──────┐ K1
                                       ├──● 87 ──► VM driver ──[TVS]──[1000 µF]── driver ── motor L/R
                                       │           └─47k─┬─10k─┴ GND   → VM_SENSE (ADC1, ví dụ GPIO 1/2 nếu
                                       │                 └────────────    không dùng current sense; ghi PINS.md)
                                       └──● 87a ─47k─┬─10k─ GND         → RELAY_FB (cao = relay ĐÃ NHẢ)
                                                     └────────────────► logic analyzer D2 + GPIO rảnh

  MẠCH XUNG GIỮ (giữa ESP32 và gate Q1):
  RELAY_HOLD (GPIO42) ─[C1 1µF]─●a──[D2 BAT54 →]──●g──► gate Q1
       └─10k─ GND (kéo xuống)   │                  ├─[C2 1µF]─ GND
                                └──[D1 BAT54, anode GND]   └─[R2 100k]─ GND

  BUMPER_L/R: COM ─ GND ; NC ─ GPIO39/40 (kéo lên trong + 4,7k ngoài, 100 nF sát chân) — đứt dây = chân cao = "va"
  RESET: nút NO giữa GPIO rảnh và GND (kéo lên) — gán chân trong firmware/PINS.md
  Logic analyzer: D0 COIL_SENSE (qua cầu chia) · D1 RELAY_HOLD · D2 RELAY_FB · D3 DRV_EN · D4 ENC_L_A · D5 BUMPER_L
```

Đọc sơ đồ:
- **Nút E-stop và Q1 nối tiếp:** cuộn K1 có điện khi và chỉ khi nút chưa nhấn **và** Q1 đang dẫn. Q1 chỉ dẫn khi RELAY_HOLD **đang đảo** (Bài C10.1 phần 2). Một chân kẹt cao, kẹt thấp, thả nổi, hay ESP32 mất điện đều làm Q1 tắt.
- **Chân 87a cho biết relay đã nhả,** độc lập với VM. Không dùng "VM về 0" làm mốc kết thúc: khi relay mở lúc motor còn quay, motor phát ngược qua diode thân của driver và giữ VM trên tụ 1000 µF một lúc. VM_SENSE dùng để phát hiện **relay dính** (87a chưa lên mà VM vẫn còn sau khi cuộn mất điện, hoặc VM còn khi 87a đã lên).
- **Đồng thời 87 và 87a** không bao giờ cùng nối với 30. Nếu RELAY_FB cao và VM_SENSE cao kéo dài hơn thời gian xả tụ đã đo → tiếp điểm 87 dính hoặc đi dây sai.
- Relay 4 chân của C1 (không có 87a) vẫn dùng được: khi đó mốc "relay nhả" lấy bằng VM_SENSE **khi motor đứng yên** (không có back-EMF), và ghi giới hạn này.
- Chân GPIO cho VM_SENSE, RELAY_FB, RESET chưa có trong bảng chân đề xuất của C4: chọn chân rảnh không thuộc danh sách cấm của C4 (strapping, USB, flash/PSRAM, UART0), ADC1 cho VM_SENSE, và **sửa `firmware/PINS.md` trước khi sửa code** (quy tắc C4).

**Bảng dây bổ sung** vào `wiring/wires.csv`:

| wire_id | net | từ → tới | AWG | màu | cầu chì |
|---|---|---|---|---|---|
| W41 | ESTOP_CHAIN | nút E-stop thân → cuộn K1 (thay nút tạm C1/C5) | 22 | nhãn đỏ hai đầu | FD 1 A |
| W42 | COIL_LOW | cuộn K1 (86) → D Q1 | 22 | nhãn đỏ | FD |
| W43 | RELAY_HOLD | GPIO42 → mạch xung giữ | 26 | trắng, nhãn HOLD | — |
| W44 | RELAY_FB | 87a → cầu chia → GPIO | 22 → 26 | nhãn FB | FA (phía 87a) |
| W45 | VM_SENSE | VM → cầu chia → ADC1 | 26 | nhãn VMS | — (dòng µA) |
| W46/W47 | BUMPER_L/R | công tắc → GPIO39/40, xoắn với GND | 26 | xanh lá/GND đen | — |

## 5. Trình tự chặng

Thứ tự: hiểu → lắp phần cứng an toàn → kiểm trên giá → đo phản ứng → state machine → FMEA và gây lỗi → soak. Không đảo.

1. **Học Bài C10.1 phần 1–5.** Commit `prediction.md` trước khi mở 🔒.
2. **Lắp bước 1 — Bo an toàn trên bo đục lỗ** (mạch xung giữ, Q1, cầu phân áp, đế relay 5 chân)
   - Làm: hàn theo mục 4; nhãn từng điểm đo; chưa nối vào robot.
   - ✅ Checkpoint trước khi cấp điện (đồng hồ, không nguồn): Ω gate Q1 ↔ GND ≈ 100 kΩ (R2 có mặt, gate không thả nổi); Ω RELAY_HOLD ↔ GND ≈ 10 kΩ; tỉ số mỗi cầu chia đúng (cấp 12,0 V nguồn bàn, đo ra ≈ 2,1 V); diode và Zener đúng chiều (vạch diode về phía +).
   - ✅ Checkpoint trên nguồn bàn (I_set 0,3 A, 12 V cho chuỗi cuộn; 3,3 V từ máy phát xung hoặc ESP32 thứ hai cho RELAY_HOLD): không xung → relay **không** hút; xung 50 Hz → relay hút sau một khoảng (ghi ms); ngắt xung → relay nhả (ghi ms); chân kẹt 3,3 V liên tục → relay **không** giữ.
   - Nếu sai: relay hút khi không có xung → Q1 bị lái từ chỗ khác hoặc gate thả nổi; relay không bao giờ hút → Vg quá thấp so với Vgs(th) của Q1 (đo Vg bằng UT33D+ khi đang có xung, so với mô phỏng).
3. **Lắp bước 2 — Nút E-stop trên thân**: vị trí với được từ phía sau và hai bên, cao nhất trên robot; thay nút tạm của C5; dây W41 đi theo khung, có strain relief.
   - ✅ Checkpoint (không nguồn): công tắc chính OFF, đo thông mạch FD → cuộn K1: chưa nhấn thông, nhấn hở, xoay thông. Lắc mạnh dây ở hai đầu khi đo: số không chập chờn.
4. **Lắp bước 3 — Bumper**: gá hai công tắc NC sau thanh cản; đo lực kích bằng cân hành lý (ghi N); thanh cản chạm vật **trước** mọi phần cứng của thân.
   - ✅ Checkpoint: firmware đọc BUMPER_L/R = "chưa va" khi chưa ấn; rút giắc bumper → firmware báo "va" (đứt dây hỏng về phía an toàn).
5. **Lắp bước 4 — Nối bo an toàn vào robot**: chuỗi cuộn của C1 đi qua Q1; RELAY_HOLD, RELAY_FB, VM_SENSE, ESTOP_SENSE vào ESP32 theo `PINS.md` đã sửa.
   - ✅ Checkpoint trước khi cấp điện: Ω VM driver ↔ GND không gần 0 Ω; Ω mọi chân ESP32 ↔ VBAT: OL; cầu chì FD là 1 A, không lớn hơn.
6. **Lắp bước 5 — Firmware**: đảo RELAY_HOLD **trong task điều khiển** sau khi mọi kiểm tra của chu kỳ đạt (Bài C10.1 phần 6 bước 2); đọc ESTOP_SENSE, RELAY_FB, VM_SENSE vào STATE; chốt `ESTOP_LATCHED` (Bài C10.1).
7. **Lắp bước 6 — RESET có chủ đích**: robot chỉ đảo RELAY_HOLD lại khi (a) chuỗi E-stop đóng (ESTOP_SENSE), (b) nút RESET trên thân vừa được nhấn, (c) host gửi `ARM`. Nhả nút E-stop thôi thì relay không hút.
   - ✅ Checkpoint (trên giá, bánh không chạm đất): nhấn E-stop khi bánh quay → relay nhả; xoay nhả nút → **relay không hút**, bánh không quay; nhấn RESET + ARM → relay hút, bánh vẫn đứng (lệnh 0) tới khi có lệnh mới.
8. **Lắp bước 7 — Kiểm trước khi chạy** (làm lại trước mỗi buổi thử lỗi và mỗi ngày soak; in thành checklist 2 phút): nhấn E-stop trên giá → relay nhả (nghe "tách", RELAY_FB lên); giữ nút RESET của ESP32 (chân EN) khi bánh quay → relay nhả; rút USB mini PC khi bánh quay → bánh dừng trong thời gian lease (C4.4), relay vẫn giữ nếu ESP32 sống; ấn bumper → bánh dừng.
9. **Học Bài C10.1 phần 6–12**: đo thời gian phản ứng từng tầng, 20 lần E-stop, quãng dừng.
10. **Học Bài C10.2**: state machine; FMEA có S/O/D; gây lỗi từng dòng, trên giá rồi trên sàn.
11. **Học Bài C10.3**: hợp đồng soak, dashboard, 72h.
12. *(Tùy chọn)* **Bài C10.4** chạy cùng hoặc ngay sau soak.
13. **Gate chặng 10.**

## 6. Lỗi người mới hay gặp

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Relay "rè", hút nhả liên tục | Vg ở vùng giữa: Q1 dẫn một phần, dòng cuộn quanh ngưỡng giữ | Đo Vg khi đảo; so Vgs(th) | MOSFET Vgs(th) thấp hơn, hoặc tăng C1 / tần số đảo (mô phỏng C10.1) |
| Relay vẫn giữ khi ESP32 treo | RELAY_HOLD do LEDC/timer phần cứng phát; ngoại vi chạy tiếp khi CPU treo | Treo task điều khiển bằng lệnh debug, xem D1 | Đảo bằng ghi GPIO trong task điều khiển (C10.1) |
| Relay vẫn giữ khi task điều khiển treo nhưng ISR timer sống | Đảo RELAY_HOLD trong ISR timer | Như trên | Đảo trong task, sau khi tính xong lệnh |
| E-stop nhấn, relay nhả, nhưng bánh trôi xa | Bình thường với dừng loại 0 (trôi); bất thường nếu VM còn | RELAY_FB, VM_SENSE trên logic analyzer | Xem C10.1 (dừng loại 1, phanh) |
| Bumper kích khi motor tăng tốc | Nhiễu cảm ứng vào dây công tắc dài | D5 trên logic analyzer khi chạy | Xoắn với GND, 100 nF sát chân, kéo lên ngoài 4,7 kΩ, đi xa dây motor |
| Nhả E-stop, robot chạy lại | Thiếu chốt `ESTOP_LATCHED`, hoặc mạch xung giữ được đảo ngay khi ESTOP_SENSE đóng | Checkpoint Lắp bước 6 | Điều kiện reset ba phần |
| Cầu chì FD đứt khi nhấn E-stop nhiều lần | Hồ quang/điện áp cảm ứng cuộn không có đường xả khi tiếp điểm nút mở | Diode/Zener có đúng chỗ (song song cuộn) không | Lắp đúng; cầu chì giữ 1 A |
| Watchdog mini PC reboot máy trong soak | `RuntimeWatchdogSec` quá ngắn so với lúc tải nặng/IO kẹt | `journalctl -b -1`, `last -x` | Nới, hoặc tìm vì sao PID 1 không kịp ping (C10.3) |
| Dashboard xanh nhưng robot đứng yên hàng giờ | Metric chỉ báo "tiến trình sống", không báo tiến triển | So "quãng đường/giờ" với "nhiệm vụ đã giao" | Thêm SLI tiến triển (C10.3) |

Lỗi riêng của từng bài ở phần 8 của bài.

## 7. Lăng kính data infra

**Dữ liệu chặng này sinh ra:**

| Luồng | Nơi | Schema (rút gọn) | Tần số | Ghi chú |
|---|---|---|---|---|
| Sự kiện an toàn | topic `/safety/events` + MCAP; JSONL `logs/safety/*.jsonl` | `t_mcu_us, boot_count, seq, kind ∈ {estop, estop_release, reset, bumper_l, bumper_r, wd_trip, lease_expired, overspeed, relay_fb, relay_weld_suspect}, state, v_l, v_r, cmd_seq` | theo sự kiện | Một sự kiện = một dòng; không gộp |
| Chuyển trạng thái | `/state_machine/transitions` + JSONL | `t_mono_ns, t_wall, boot_id, from, event, to, accepted (bool), reason, source_node` | theo sự kiện | Chuyển bị chặn cũng ghi (`accepted=false`) |
| Đo phản ứng | `captures/c10/*.sr`, `build-log/measurements.jsonl` | `quantity ∈ {estop_relay_release_time, bumper_stop_time, wd_relay_release_time, lease_stop_time, coast_distance, brake_distance}`, `value`, `unit=s` hoặc `m`, `n`, `max`, `instrument` | theo lần đo | SI: `s`, `m`; báo max và n, không chỉ mean (→ F1.4) |
| Kết quả gây lỗi | `fmea/results.csv` | `fmea_id, trial, robot_state, speed, injected_at, detected_at, safe_state_at, observed, expected, pass` | theo lần thử | Mỗi dòng FMEA ≥1 lần thử, khuyến nghị ở ≥2 trạng thái |
| Metric soak | Prometheus/CSV `ops/metrics-*.csv` | counter: `estop_total{who}`, `bumper_total`, `wd_trip_total`, `interventions_total{kind}`, `recoveries_total`; gauge: `battery_v`, `cpu_temp_c`, `disk_free_pct`, `rss_bytes{node}` | 10–60 s | Counter cho sự kiện, gauge cho trạng thái (→ F7.5) |

**Test tự động sinh ra từ chặng này (hạt giống cho C11.2):**
- `test_fsm_table`: mọi cặp (trạng thái, sự kiện) có kết quả định nghĩa; property test chuỗi ngẫu nhiên (Bài C10.2) chạy trong CI, không cần phần cứng.
- `test_hold_circuit`: trên bàn HIL, ESP32 thứ hai giả lập "treo" (ngừng đảo, kẹt cao, kẹt thấp, high-Z) và đo RELAY_FB; oracle là bảng thời gian đã đo ở C10.1.
- `test_fmea_<id>`: mỗi dòng FMEA test được ở tầng nào (SIL, HIL, bàn, thực địa) thì có một test ở tầng đó (→ F2.7). Dòng chỉ test được trên robot thật ghi rõ "thực địa, thủ công", tần suất lặp lại.

**SLI vận hành** (C10.3): completeness và freshness theo luồng, can thiệp tay/72h, sự cố an toàn, E-stop theo người nhấn, quãng đường/giờ, thời gian ở mỗi trạng thái. **Không SLI nào cho chức năng E-stop**: nó là ràng buộc nhị phân kiểm trước mỗi ngày, không có error budget (→ F7.4).

**Vai trò nghề:** Test & Validation (fault injection có oracle, FMEA gắn test, phán quyết ba trạng thái); Data Platform (sự kiện an toàn là luồng dữ liệu có schema, audit được); "Fleet ops/SRE cho robot" (dashboard, alert, postmortem).

## 8. Nhật ký build

Copy vào `build-log/c10.md`, một mục mỗi buổi:

```markdown

## 2026-MM-DD — buổi N (giờ bắt đầu–kết thúc, giờ thực: _._ h)
- Trạng thái người: tỉnh táo / mệt (mệt → không gây lỗi trên robot có động lực)
- Firmware: git hash ____ ; bo an toàn rev ____ ; relay ____ (datasheet t_release ____ ms)
- Checklist trước khi chạy (Lắp bước 7): E-stop ☐  EN-reset ☐  rút USB ☐  bumper ☐
- Mục tiêu buổi:
- Đo (measurements.jsonl, số dòng __): t_release E-stop max/n ____ ; quãng trôi ____ ; ...
- Capture: captures/c10/...
- Gây lỗi (fmea_id → kết quả → pass/fail):
- Sự cố / near miss (ai, ở đâu, tốc độ, khoảng cách) → postmortem: ____
- Quyết định (→ decisions.md): dừng loại 0/1; phương án watchdog A/B/C; timeout ____
- Câu hỏi còn mở:
```

---

## Bài C10.1 — An toàn là một tầng phần cứng: E-stop, relay, bumper, watchdog độc lập, đo thời gian phản ứng (16h)

> **Vị trí:** C8.4 (Nav2 chạy được) → **C10.1** → C10.2 · **Cần trước:** → F5.7 (watchdog, brownout), → F5.3 (trường hợp xấu nhất), → F5.8 (trễ trong vòng), → F1.4 (quy tắc ba); K7 C1.3 (cầu chì cuộn), C4.4 (lease, kẹp tốc độ, ARM), C5.3 (E-stop tạm); K3 Bài 15–16 (kill switch, watchdog hai tầng) · **Sau bài này bạn quyết định được:** cái gì cắt năng lượng motor và nó độc lập với những gì; watchdog độc lập làm bằng mạch xung giữ, MCU thứ hai hay IC supervisor; E-stop của robot là dừng loại 0 hay loại 1; con số "thời gian phản ứng" nào được ghi vào README.

### 1. Câu chuyện — ai đã khổ vì chuyện này

Therac-25 là máy xạ trị của AECL. Từ 1985 đến 1987, ít nhất sáu bệnh nhân bị chiếu quá liều rất nặng; một số người chết `[chuẩn — Leveson & Turner, *An Investigation of the Therac-25 Accidents*, IEEE Computer, 1993]`. Thế hệ trước (Therac-6, Therac-20) có **interlock phần cứng**: công tắc và mạch độc lập ngăn chùm tia mạnh khi cấu hình cơ khí sai. Therac-25 bỏ phần lớn interlock đó và giao việc kiểm tra cho phần mềm. Hai lỗi được tìm ra: một race condition khi kỹ thuật viên sửa thông số nhanh, và một biến cờ một byte bị **cộng dồn** thay vì gán, cứ 256 lần thì tràn về 0 và bỏ qua một bước kiểm tra. Chi tiết đáng nhớ nhất trong báo cáo của Leveson: Therac-20 cũng có lỗi phần mềm tương tự, nhưng ở đó interlock phần cứng làm **đứt cầu chì** thay vì để bệnh nhân hứng tia. Phần mềm sai ở cả hai máy; chỉ một máy có tầng phần cứng đỡ.

Câu hỏi của bài: **khi phần mềm treo, cái gì dừng robot lại?** Nếu câu trả lời có chữ "code", "flag", "topic" hay "callback" thì chưa trả lời. Và câu hỏi khó hơn mà K7 gốc chỉ nêu trong một ô FMEA: **khi chính ESP32 treo, cái gì cắt relay?** Mini PC không có GPIO; ESP32 là bộ điều khiển duy nhất chạm vào motor. Bài này thiết kế thứ đó.

### 2. Mô hình tư duy

**Nguyên tắc 1 — cấp điện để chạy (energize-to-run).** Motor chỉ có năng lượng khi **mọi** điều kiện trong một chuỗi nối tiếp đang thỏa. Đứt dây, mất nguồn, rút giắc, chết chip — đều làm chuỗi hở, và trạng thái mặc định khi chuỗi hở là "motor không có năng lượng".

| | Cấp điện để chạy (đúng cho E-stop) | Cấp điện để dừng (sai cho E-stop) |
|---|---|---|
| Nhấn E-stop | Mở chuỗi → cuộn relay mất điện → VM mất | Đóng một tín hiệu → phần mềm đọc → phần mềm ra lệnh dừng |
| Đứt dây nút | Motor dừng, lỗi lộ ra ngay | **Không ai biết**, E-stop chết âm thầm |
| ESP32 treo | Xung giữ mất → relay nhả | Không ai đọc tín hiệu |
| Mất nguồn điều khiển | Motor dừng | Tùy may rủi |

**Nguyên tắc 2 — bốn tầng, hỏng độc lập.**

| Tầng | Cơ chế | Còn hoạt động khi nào | Kiểu dừng |
|---|---|---|---|
| 0 | E-stop: nút NC trong chuỗi cuộn K1 | Có pin. Không cần chip nào | Cắt năng lượng (loại 0) |
| 0b | Watchdog độc lập: mạch xung giữ trên Q1 | Không cần ESP32 *đúng*; ESP32 *sai* thì chuỗi hở | Cắt năng lượng (loại 0) |
| 1 | Bumper, cảm biến vực → ISR ESP32 | ESP32 sống | Hãm có điều khiển, rồi tắt driver |
| 2 | Lease/kẹp tốc độ/giám sát tốc độ đo (C4.4) | ESP32 sống | Hãm có điều khiển |
| 3 | Nav2: costmap, giới hạn tốc độ, state machine | Linux, ROS 2, USB, ESP32 sống | Giảm tốc theo kế hoạch |

Hai tầng cùng lấy điện từ một chỗ, cùng chạy trên một chip, là một tầng. Tầng 3 là tầng bạn giỏi nhất và **ít đáng tin nhất**.

**Nguyên tắc 3 — E-stop không phải "dừng mềm".** IEC 60204-1 định nghĩa ba loại dừng `[spec — IEC 60204-1, mục về chức năng dừng]`: **loại 0** cắt năng lượng tới bộ chấp hành ngay (dừng không điều khiển: robot trôi); **loại 1** hãm có điều khiển trong khi vẫn cấp năng lượng, rồi cắt năng lượng khi đã dừng; **loại 2** hãm và **giữ** năng lượng. ISO 13850 (thiết kế chức năng dừng khẩn cấp) chỉ cho phép E-stop là loại 0 **hoặc** 1, chọn theo đánh giá rủi ro; loại 2 không được; nút phải tự khóa, và **nhả/reset nút không được tự khởi động lại máy** `[spec — ISO 13850, IEC 60204-1 mục 9.2.3.4 theo trích dẫn của các hãng; đọc tóm tắt, không cần mua chuẩn]`. Vậy:
- Nút đỏ trên thân → loại 0 (mặc định của bài) hoặc loại 1 (phần 6 bước 7, tùy chọn).
- "Dừng" trên app teleop, nút `STOP` trong state machine, kill switch MQTT của K3, `cancel` goal Nav2 → **dừng mềm** (về bản chất là loại 2: driver vẫn có điện, chỉ lệnh bằng 0). Hữu ích, nên có, **không được gọi là E-stop** trong README, dashboard hay bài viết.

**Watchdog độc lập: mạch "xung giữ".** Một tín hiệu **tĩnh** (cao hay thấp) không chứng minh được gì về chip phát ra nó: chip treo vẫn giữ chân ở mức cuối. Một tín hiệu **động** (đang đảo) chứng minh có code đang chạy tới dòng đảo. Mạch bơm điện tích chỉ cho cổng Q1 đủ áp khi chân RELAY_HOLD đang đổi mức; kẹt ở bất kỳ mức nào thì tụ cổng xả qua R2 và relay nhả. Mô phỏng đồ chơi trước khi hàn:

```python
# [đã chạy] Mạch "xung giữ" (bơm điện tích): relay chỉ được giữ khi chân ESP32 ĐANG ĐẢO.
# Mô hình đồ chơi: u(t) -> C1 -> nút a; D1 (GND->a), D2 (a->g); C2 và R2 ở cổng MOSFET g.
import numpy as np
VDD, VF, RS = 3.3, 0.30, 150.0        # mức GPIO; Vf diode Schottky [ước lượng]; R nối tiếp + diode
C1, C2, R2 = 1e-6, 1e-6, 100e3        # [ước lượng] chọn để thử; thay bằng linh kiện của bạn
VTH = 1.0                             # Vgs dưới mức này coi như MOSFET tắt [spec: datasheet MOSFET của bạn]
dt = 2e-6

def run(signal, T):
    va = vg = 0.0; vc1 = 0.0          # vc1 = u - va (áp trên C1)
    out = []
    for k in range(int(T / dt)):
        t = k * dt
        u = signal(t)
        va = u - vc1
        i1 = max(0.0, (-VF - va) / RS)          # D1 dẫn khi va < -Vf (nạp C1 lúc u thấp)
        i2 = max(0.0, (va - VF - vg) / RS)      # D2 dẫn khi va > vg + Vf (đẩy điện tích sang C2)
        vc1 += (i2 - i1) * dt / C1              # KCL tại nút a
        vg += (i2 - vg / R2) * dt / C2
        if k % 500 == 0: out.append((t, vg))
    return np.array(out)

sq = lambda f: (lambda t: VDD if (t * f) % 1 < 0.5 else 0.0)
cases = {
    "đảo 50 Hz (vòng 100 Hz chạy)":           (lambda t: sq(50)(t) if t < 0.6 else 0.0),
    "đảo 50 Hz rồi KẸT CAO ở 0,6 s":         (lambda t: sq(50)(t) if t < 0.6 else VDD),
    "LEDC 1 kHz vẫn chạy khi CPU treo":       (lambda t: sq(1000)(t)),
    "chân kẹt cao từ đầu (thả nổi kéo lên)":  (lambda t: VDD),
}
for name, s in cases.items():
    r = run(s, 1.0)
    on = r[(r[:, 0] > 0.4) & (r[:, 0] < 0.6), 1]
    below = r[(r[:, 0] > 0.6) & (r[:, 1] < VTH), 0]
    t_off = f"{(below[0]-0.6)*1e3:.0f} ms sau 0,6 s" if below.size else "KHÔNG BAO GIỜ"
    print(f"{name:<40} Vg lúc chạy {on.min():.2f}–{on.max():.2f} V; Vg < {VTH} V: {t_off}")
```

Ba điều mô phỏng buộc bạn nghĩ (đáp án số ở phần 7): mạch phân biệt "đang đảo" với "kẹt" thế nào; vì sao **nguồn của xung** quan trọng hơn mạch (dòng thứ ba); và thời gian từ lúc ngừng đảo tới lúc Q1 tắt phụ thuộc linh kiện nào.

**Ba phương án watchdog độc lập** (kế hoạch K7 mục 5 cho phép "watchdog ngoài hoặc MCU thứ hai"):

| | A. Mạch xung giữ (mặc định) | B. MCU thứ hai | C. IC supervisor có watchdog (ví dụ TPS3823) |
|---|---|---|---|
| Phát hiện | ESP32 ngừng đảo / kẹt mức | Bất kỳ logic bạn viết: xung, tốc độ encoder, nhất quán lệnh | Không có cạnh WDI trong khoảng timeout |
| Thêm phần mềm | 0 dòng | Một firmware nữa, cần test, cần cập nhật | 0 dòng |
| Timeout | RC, chỉnh bằng linh kiện, trôi theo nhiệt/dung sai tụ | Đặt bằng code | Cố định theo datasheet; TPS3823 điển hình 1,6 s, tối thiểu 0,9 s `[spec — TI SLVS165; kiểm bảng thông số]` |
| Bẫy | Xung phải phát từ đúng chỗ (phần 3) | Nguồn chung với ESP32 = hỏng chung; tự nó cũng treo được | **WDI để hở có thể làm vô hiệu watchdog** `[spec — kiểm mục WDI của datasheet]`: ESP32 reset → chân cao trở → watchdog tắt. Phải kéo chân hoặc chọn IC khác |
| Hợp với | Người mới, robot một bo | Khi cần giám sát tốc độ độc lập (giống thang máy) | Khi timeout ~1 s chấp nhận được |

**Đo cái gì, chính xác:** "thời gian phản ứng" là một khoảng giữa **hai cạnh có định nghĩa** trên logic analyzer. Với tầng 0: cạnh đầu COIL_SENSE xuống (chuỗi hở) → cạnh đầu RELAY_FB lên (87a đóng). Không dùng "VM về 0": motor đang quay phát ngược vào tụ VM qua diode thân của driver. "Robot dừng" là một đại lượng khác: quãng từ kích hoạt tới khi encoder hết xung, đo bằng encoder (vẫn có điện từ buck 5 V khi VM mất).

```
 COIL_SENSE  ‾‾‾‾‾|_|‾|________________________________   (nút mở, tiếp điểm rung)
 dòng cuộn   ‾‾‾‾‾‾‾\______                                (tắt dần; chậm hơn nhiều nếu chỉ có diode)
 RELAY_FB    _____________|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾   ← 87a đóng: "đã nhả"
 VM          ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\‾‾‾‾\_______                  ← back-EMF giữ VM khi bánh còn quay
 ENC_L_A     |_|‾|_|‾|_|‾|_|‾|__|‾‾|___|‾‾‾‾|______        ← xung thưa dần: trôi (loại 0)
             |<- t_relay ->|<------- quãng trôi -------->|
```

**Quãng dừng = v · t_phản_ứng + v² / (2a).** Động năng ½mv²: robot 5 kg ở 0,5 m/s có 0,625 J; ở 1,5 m/s gấp 9 lần. Mô phỏng nhỏ để thấy một điều trái trực giác về loại 0:

```python
# [đã chạy] Quãng dừng theo tầng an toàn: d = v·t_phản_ứng + v²/(2a). Mọi số đầu vào là GIẢ ĐỊNH.
import numpy as np
m = 5.0                                  # kg [ước lượng] -> thay bằng số cân ở C2.4
v = np.array([0.3, 0.5, 1.0, 1.5])       # m/s; 0,5 là trần firmware (C4.4)
a_coast, a_brake = 0.8, 2.0              # m/s² [ước lượng]: trôi tự do (dừng loại 0) vs hãm có điều khiển
layers = {                               # (tên, t phản ứng giả định [s], kiểu dừng)
    "T0 E-stop -> relay": (0.015, "coast"),
    "T1 bumper -> ISR":   (0.005, "brake"),
    "T2 watchdog/lease":  (0.25,  "brake"),
    "T3 Nav2/costmap":    (0.30,  "brake"),
}
print("v (m/s) | KE (J) | " + " | ".join(layers))
for vi in v:
    cells = []
    for t, kind in layers.values():
        a = a_coast if kind == "coast" else a_brake
        cells.append(f"{100*(vi*t + vi**2/(2*a)):5.1f} cm")
    print(f"{vi:7.1f} | {0.5*m*vi**2:6.3f} | " + " | ".join(cells))
# Đổi một giả định một lần: a_coast thật của robot bạn là bao nhiêu? Đo ở Làm bước 7.
```

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Circuit breaker trong code | E-stop | Circuit breaker chạy **trong** tiến trình nó bảo vệ; tiến trình treo thì breaker treo theo | E-stop là một topic ROS → mini PC kẹt swap là E-stop chết |
| Liveness probe + restart (Kubernetes) | Watchdog độc lập | Backend phản ứng với "chết" bằng **khởi động lại**. Ở đây là **cắt năng lượng và chờ người** | ESP32 reset xong tự ARM, robot chạy tiếp theo lệnh cũ |
| Heartbeat do một thread riêng gửi | Xung RELAY_HOLD | Thread heartbeat sống khi phần việc chính đã treo. Xung phải đi ra từ **chính** chỗ làm việc, sau khi việc xong | Đảo bằng LEDC hoặc trong ISR timer → watchdog luôn "xanh" khi task điều khiển treo |
| Defense in depth | Bốn tầng | Các tầng backend hay dùng chung hạ tầng (cùng DNS, cùng cluster). Tầng an toàn phải khác nguồn, khác chip, khác dây | ESP32 ăn từ USB mini PC: mini PC mất nguồn kéo theo tầng 0b, 1, 2 |
| Fail closed | Fail-safe | "Closed" là từ chối request. "Safe" là một **trạng thái vật lý** phụ thuộc bối cảnh (sàn phẳng hay dốc) | Coi "mất điện motor" là an toàn cho mọi robot, kể cả trên dốc |
| Graceful shutdown (SIGTERM, drain) | Dừng loại 1 | Graceful shutdown phụ thuộc tiến trình còn chạy đúng. Loại 1 cũng vậy, nên phải có **bộ hẹn giờ phần cứng** cắt năng lượng dù việc hãm có xong hay không | Loại 1 viết bằng firmware thuần: ESP32 treo giữa lúc hãm thì không bao giờ cắt |

**Chấm mô hình:**
- *"Logic an toàn viết kỹ, test kỹ thì đặt ở phần mềm cũng được, lại linh hoạt hơn."* — **SAI** cho chức năng dừng khẩn cấp. Test cho thấy sự có mặt của lỗi, không chứng minh sự vắng mặt. **Phản ví dụ:** Therac-25: cùng lớp lỗi phần mềm, máy có interlock phần cứng làm đứt cầu chì, máy không có thì làm chết người.
- *Mô hình của bạn ở K3 lượt 12:* "dùng AI model kết hợp prediction để thay thế cho kết quả của tầng vật lý… kết quả vẫn đảm bảo" — **ĐÚNG MỘT PHẦN** cho hiệu năng, **SAI** cho an toàn. Dự đoán tốt làm robot hiếm khi cần dừng khẩn cấp; nó không thay được thứ dừng robot khi dự đoán sai hoặc khi máy chạy dự đoán treo. **Phản ví dụ:** model dự đoán quỹ đạo người chạy trên mini PC; mini PC kẹt vì swap. Không có dự đoán nào được tạo ra; chỉ tầng 0–2 còn làm việc.
- *"Dừng loại 0 là an toàn nhất vì không phụ thuộc phần mềm."* — **ĐÚNG MỘT PHẦN.** Đúng về **độ tin cậy** của việc dừng. Sai về **quãng dừng**: trôi tự do có gia tốc hãm nhỏ hơn hãm chủ động, nên ở cùng tốc độ robot có thể đi xa hơn so với khi tầng 2 hãm. **Phản ví dụ:** chạy mô phỏng quãng dừng ở trên với a_coast nhỏ hơn a_brake; rồi đo thật ở bước 7. Đây là lý do ISO 13850 cho phép loại 1.

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | E-stop | Thiết bị dừng khẩn cấp do người kích hoạt, cắt năng lượng nguy hiểm | Nút gọi `stop()` |
| 🟢 | Dừng loại 0 / 1 / 2 (IEC 60204-1) | 0: cắt năng lượng ngay; 1: hãm có điều khiển rồi cắt; 2: hãm, giữ năng lượng | Mọi kiểu dừng như nhau |
| 🟢 | Dừng mềm | Dừng bằng lệnh phần mềm, driver vẫn có điện | E-stop |
| 🟢 | Energize-to-run / fail-safe | Cần năng lượng để **duy trì** trạng thái nguy hiểm | Có code xử lý lỗi |
| 🟢 | Tiếp điểm NC / NO; 87 / 87a | Thường đóng / thường mở; chân thường mở / thường đóng của relay ô tô | — |
| 🟡 | Mở cưỡng bức (positive opening) | Cơ cấu ép tiếp điểm NC tách ra kể cả khi dính | NC thường |
| 🟢 | Tín hiệu động (xung giữ, charge pump) | Chỉ "đang đổi" mới giữ được trạng thái chạy | Tín hiệu mức cao |
| 🟢 | Common-cause failure | Một nguyên nhân làm hỏng nhiều tầng cùng lúc | Hai tầng là gấp đôi an toàn |
| 🟡 | Thời gian nhả relay, mạch dập cuộn | Relay mở chậm hơn khi cuộn chỉ có diode | Relay mở tức thì |
| 🟡 | Reset có chủ đích | Khởi động lại là một hành động riêng, sau khi nguy cơ đã xử lý | Nhả nút là xong |
| 🟡 | ISO 13850, ISO 13482, ISO 3691-4 | Thiết kế E-stop; an toàn robot chăm sóc cá nhân; xe tự hành công nghiệp | Bắt buộc cho dự án cá nhân |
| 🔴 | PL/SIL theo ISO 13849 / IEC 61508 | Định lượng mức an toàn chức năng | — |

### 5. Dự đoán

**Tham số cần tra:**
- Khối lượng robot: số cân ở C2.4 (kèm pin, mini PC).
- Thời gian nhả và dòng cuộn của K1: **datasheet relay** (ghi điều kiện đo, thường là cuộn **không** có mạch dập); dòng cuộn đo ở C1.
- Vgs(th) và đường Id–Vgs của Q1: **datasheet MOSFET**; có đủ dẫn dòng cuộn ở Vg mô phỏng không?
- Trạng thái chân ESP32-S3 khi reset và khi giữ nút EN: datasheet ESP32-S3 (mục về trạng thái chân lúc khởi động); kiểm theo revision.
- Gia tốc trôi a_coast: chưa có — đo ở bước 7. Gia tốc hãm a_brake: từ C4/C5 nếu đã đo, không thì đo.
- Timeout lease đã chọn ở C4.4: `firmware/config.h` của bạn.

**Đoán:**
1. Động năng ở 0,5 và 1,5 m/s với khối lượng thật.
2. Thời gian phản ứng từng tầng: E-stop → RELAY_FB; giữ EN ESP32 → RELAY_FB; treo task điều khiển → RELAY_FB; bumper → DRV_EN thấp; host im lặng → PWM = 0.
3. Quãng trôi sau E-stop ở 0,5 m/s; quãng hãm sau bumper ở 0,5 m/s.
4. Mô phỏng xung giữ: Vg khi đang đảo; thời gian Q1 tắt khi ngừng đảo; trường hợp LEDC.
5. Rút nguồn 5 V của ESP32 khi motor đang chạy (VM còn): motor làm gì, relay làm gì?
6. Relay chỉ có diode so với diode + Zener: nhả chậm hơn bao nhiêu lần?

```markdown
# prediction.md — C10.1   (commit: <hash>, ngày: <yyyy-mm-dd>)
- m = __ kg -> KE(0.5) = __ J, KE(1.5) = __ J
- K1: t_release datasheet = __ ms (điều kiện: __); đoán đo được: chỉ diode __ ms, diode+Zener __ ms
- Phản ứng: E-stop __ ms; EN giữ __ ms; treo task __ ms; bumper __ ms; lease __ ms (timeout C4.4 = __)
- Quãng trôi E-stop ở 0,5 m/s: __ cm (a_coast đoán __); quãng hãm bumper: __ cm
- Mô phỏng: Vg đảo = __ V; tắt sau __ ms; LEDC: __
- Rút 5 V ESP32 khi chạy: motor __, relay __ vì __
- Chọn: dừng loại __ ; watchdog phương án __ vì __
```

### 6. Làm

0. **Kiểm topology trước khi đo** (đã làm ở C1/C4, kiểm lại trên robot hoàn chỉnh): ESP32 ăn từ buck 5 V của bo nguồn, không chỉ từ USB mini PC; DRV_EN, PWM có kéo xuống ngoài; không chân điều khiển motor nào là chân strapping (bảng chân C4). Lý do: C10.2 sẽ rút nguồn từng khối, thiết kế phải sống sót trước khi test.
1. **E-stop vật lý cắt năng lượng motor** (Lắp bước 1–2, 4). Nút NC nối tiếp cuộn K1; tiếp điểm 30→87 trên VM. ESTOP_SENSE vào ESP32 để ghi log và **chốt**: `ESTOP_LATCHED` đặt PWM = 0, DRV_EN thấp, ngừng đảo RELAY_HOLD; chỉ xóa theo điều kiện reset ba phần (Lắp bước 6). **Test bằng cách rút cáp USB giữa mini PC và ESP32** — E-stop vẫn phải hoạt động. Thêm: test khi **rút nguồn 5 V của ESP32**.
2. **Watchdog độc lập** (phương án A mặc định). Firmware đảo RELAY_HOLD **trong task điều khiển 100 Hz** (C4.1), là dòng cuối của chu kỳ, chỉ khi: lease còn hạn, không có cờ lỗi, không `ESTOP_LATCHED`, tốc độ đo trong giới hạn. Ghi bằng `gpio_set_level` đảo trạng thái; **không** dùng LEDC/MCPWM/timer phần cứng cho chân này, **không** đảo trong ISR `[tự đo — kiểm API theo phiên bản ESP-IDF bạn cài]`. Kiểm ba cách "treo" bằng một lệnh debug chỉ có ở bản build thử (`FAULT_HANG_TASK`: task điều khiển vào vòng lặp vô hạn; `FAULT_HANG_ALL`: tắt ngắt rồi lặp vô hạn) và một cách vật lý (giữ nút EN). Nếu chọn phương án B hoặc C, viết lý do vào `decisions.md` và thay mạch tương ứng; phép đo giống hệt.
3. **Bumper** nối vào chân ngắt ESP32 (GPIO39/40 theo bảng chân C4), phản ứng ở **cạnh đầu**; debounce chỉ áp cho lúc nhả. Trong ISR chỉ làm việc tối thiểu, an toàn khi gọi từ ngắt: kéo DRV_EN xuống bằng ghi GPIO, đặt cờ; việc hãm có điều khiển và log để task làm `[tự đo — kiểm hàm nào gọi được từ ISR]`. Tùy chọn: chân NC thứ hai của bumper nối thêm vào chuỗi cuộn (khi đó bumper cũng là dừng loại 0, quãng dừng đổi: so ở bước 7).
4. **Giới hạn tốc độ cứng** là việc của C4.4 (kẹp từng bánh, kẹp gia tốc, giám sát tốc độ đo). Ở đây **kiểm lại trên robot hoàn chỉnh**: gửi `cmd_vel` 2 m/s và lệnh quay tại chỗ tối đa từ mini PC, ghi tốc độ đo từ encoder.
5. **Cảm biến vực** (nếu khu soak có bậc): IR/ToF hướng xuống, vào tầng 1 như bumper. Test trên mép bàn **có tấm chắn** bên dưới, tốc độ thấp.
6. **Đo thời gian phản ứng của từng tầng bằng logic analyzer** (kênh ở mục 4; 24 MHz → độ phân giải ~42 ns; sai số thật nằm ở định nghĩa cạnh khi tiếp điểm rung, không ở dụng cụ). Mỗi tầng ≥10 lần, ghi **max và n** (không ghi mean):
   - T0: cạnh đầu COIL_SENSE xuống → cạnh đầu RELAY_FB lên. Làm hai cấu hình dập cuộn: chỉ diode, diode + Zener.
   - T0b: cạnh cuối RELAY_HOLD → RELAY_FB lên, cho `FAULT_HANG_TASK`, `FAULT_HANG_ALL`, giữ EN, rút 5 V ESP32.
   - T1: cạnh đầu BUMPER_L → DRV_EN xuống (hoặc PWM = 0).
   - T2: `kill -STOP` tiến trình gửi lệnh trên mini PC (mô phỏng treo, khác `kill -9`); cạnh DBG_CMD cuối (C4) → PWM = 0. Lặp lại khi rút USB.
7. **Test E-stop 20 lần**, ≥5 lần ở tốc độ tối đa (0,5 m/s), trên sàn, đường thẳng có đánh dấu. Mỗi lần ghi: t_relay, **quãng trôi** (count encoder từ cạnh kích hoạt tới xung cuối × chu vi bánh / số count mỗi vòng, từ C6), và đo thước dây vết bánh (đối chứng: trượt bánh làm encoder đọc thiếu). Từ quãng trôi và v, tính a_coast. Làm 5 lần bumper ở cùng tốc độ để có quãng hãm.
8. **Tùy chọn — dừng loại 1.** Nếu quãng trôi ở bước 7 lớn hơn mức bạn chấp nhận (ghi tiêu chí trước, ví dụ theo khoảng trống trước bumper), làm loại 1: nút E-stop có **hai** khối tiếp điểm NC; khối 1 vào ESTOP_SENSE (ESP32 hãm ngay), khối 2 vào chuỗi cuộn **qua một bộ trễ nhả phần cứng** (relay trễ nhả hoặc RC trên mạch giữ, ví dụ 300 ms) → năng lượng bị cắt sau thời gian trễ **dù ESP32 hãm hay không**. Đo lại bước 7. Không bao giờ làm loại 1 mà thiếu bộ trễ phần cứng.
9. **Viết bảng "Bốn tầng"** vào `docs/safety.md`: tầng, cơ chế, phụ thuộc gì, max đo được (n), kiểu dừng, quãng dừng ở 0,5 m/s. Đây là tiêu chí gate 2.

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

**Mô phỏng xung giữ** (linh kiện trong code):

| Trường hợp | Vg khi chạy | Q1 tắt (Vg < 1 V) |
|---|---|---|
| Đảo 50 Hz rồi ngừng ở mức thấp | ~2,0–2,4 V (gợn theo chu kỳ) | ~70 ms sau khi ngừng |
| Đảo 50 Hz rồi kẹt cao | như trên | ~170 ms (lần sạc cuối nằm ở cạnh lên) |
| LEDC 1 kHz chạy tiếp khi CPU treo | ~2,7 V | **không bao giờ** — mạch đúng, nguồn xung sai |
| Kẹt cao từ đầu | ~0,1–0,2 V | relay không bao giờ hút |

Thời gian tắt tỉ lệ với R2·C2 (τ = 0,1 s) và phụ thuộc Vg lúc ngừng; dung sai tụ gốm (thường ±10–20%, giảm theo áp DC đặt lên) làm nó trôi `[chuẩn — kiểm datasheet tụ]`. Vg ~2 V là **sát** cho nhiều MOSFET: phải đọc đường Id–Vgs, không chỉ Vgs(th). Nếu Q1 không dẫn đủ: tăng C1, tăng tần số đảo, hoặc dùng mức 5 V qua mạch chuyển mức.

**Mô phỏng quãng dừng** (a_coast 0,8, a_brake 2,0 m/s², giả định): ở 0,5 m/s, T0 (trôi) ~16 cm, T1 (bumper hãm) ~7 cm, T2 ~19 cm, T3 ~21 cm. Ở 1,5 m/s, T0 ~143 cm. Đọc đúng: E-stop **chắc chắn** dừng nhất nhưng không phải **ngắn** nhất; khi a_coast thật nhỏ (hộp số trơn, bánh nhẹ ma sát) thì loại 1 đáng làm.

**Thí nghiệm thật** (tiêu chí gốc giữ nguyên, sửa cách đọc tầng 2):

| Tầng | Thời gian phản ứng đo được |
|---|---|
| E-stop vật lý | Giới hạn bởi relay: vài ms tới khoảng chục ms với diode + Zener; dài hơn rõ (có thể gấp vài lần) nếu cuộn chỉ có diode `[tự đo — so với datasheet]` |
| Watchdog độc lập (T0b) | ≈ thời gian xả mạch giữ (chục tới trăm ms theo linh kiện) + t_relay. Giữ EN và rút 5 V cho cùng cỡ số `[tự đo]` |
| Bumper | **< 10 ms** (gốc). Trễ ngắt ESP32 cỡ µs; phần lớn là cơ khí công tắc và chu kỳ PWM `[tự đo]` |
| Watchdog lease (T2) | **t(PWM = 0) − t(lệnh cuối) ≤ timeout + chu kỳ kiểm + một chu kỳ PWM.** Tiêu chí "< 500 ms" của gốc không đạt được nếu timeout là 500 ms; tiêu chí đúng là bất đẳng thức này với timeout bạn chọn ở C4.4 |
| Giới hạn tốc độ firmware | Không bao giờ vượt, kể cả khi mini PC gửi lệnh sai, kể cả quay tại chỗ |

| Kiểm tra | Kết quả đúng |
|---|---|
| E-stop 20 lần | **20/20 dừng.** Không có ngoại lệ |
| Rút cáp USB mini PC, bấm E-stop | Vẫn dừng |
| Rút 5 V ESP32 khi motor chạy | Relay nhả (T0b), driver tắt (kéo xuống); nếu motor chạy tiếp hoặc giật → sửa trước C10.2 |
| `FAULT_HANG_TASK`, `FAULT_HANG_ALL` | Relay nhả trong T0b đã đo; nếu không → xung đang phát từ ngoại vi hoặc ISR |
| Nhả E-stop | Motor **không** tự chạy lại; relay không hút khi chưa RESET + ARM |
| Gửi lệnh 2 m/s từ mini PC | Firmware kẹp về 0,5 m/s |

**Động năng:** 5 kg: 0,625 J ở 0,5 m/s, ≈5,6 J ở 1,5 m/s.

**20/20 nói được gì:** 0 lỗi trong 20 lần → cận trên 95% của xác suất hỏng mỗi lần ≈ 3/20 = 15% (quy tắc ba, → F1.4). Hai mươi lần **loại** thiết kế hỏng thường xuyên; độ tin cậy của E-stop đến từ **thiết kế** (NC, mở cưỡng bức, energize-to-run, không có chip trên đường), không từ số lần test.

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Bấm E-stop, RELAY_FB không lên | Nút đang cắt tín hiệu chứ không ở chuỗi cuộn; relay 4 chân đọc nhầm | Đo thông mạch nút ↔ cuộn | Đưa nút vào chuỗi cuộn; dùng relay 5 chân |
| RELAY_FB lên nhưng VM_SENSE còn lâu | Bình thường khi bánh còn quay (back-EMF); bất thường nếu bánh đã đứng | So với ENC_L_A | Bánh đứng mà VM còn → tiếp điểm 87 dính hoặc dây đi vòng: thay relay |
| Relay nhả chậm hơn datasheet nhiều | Diode flyback đơn thuần | Hai cấu hình dập | Diode + Zener (Q1 phải chịu V_pack + V_Z) |
| Relay giữ khi `FAULT_HANG_TASK` | Đảo từ LEDC, timer, hoặc ISR | Xem code nơi đảo | Đảo trong task điều khiển (bước 2) |
| Relay giữ khi giữ EN | Chân RELAY_HOLD lúc reset có xung (glitch) hoặc mạch xung giữ ăn từ chân khác | D1 lúc giữ EN | Kéo xuống 10 kΩ; chọn chân không glitch lúc boot (C4) |
| Bumper phản ứng > 50 ms | Polling trong task, hoặc debounce trước khi hành động | Đổi tín hiệu bumper với chân debug ISR | Ngắt cạnh; hành động ở cạnh đầu |
| Bumper tự kích khi motor tăng tốc | Nhiễu cảm ứng vào dây công tắc | D5 khi chạy | Pull-up ngoài, 100 nF, dây xoắn với GND, xa dây motor |
| Dừng oan theo lease liên tục | Timeout ngắn so với jitter lệnh thật của mini PC | Histogram khoảng cách lệnh (DBG_CMD) | Quay về C4.4: chọn timeout từ phân bố đo; chạy node gửi lệnh với `chrt -f` (→ F5.4) |
| VM vọt áp khi relay mở lúc chạy nhanh | Motor thành máy phát, không còn đường về pin | VM_SENSE ở 0,5 m/s | TVS + tụ bulk trên VM driver `[chuẩn]` |
| Quãng trôi encoder ngắn hơn thước dây | Bánh trượt khi dừng, encoder đếm bánh chứ không đếm sàn | So hai số | Báo cả hai; dùng số thước dây cho an toàn |
| Tiếp điểm relay dính | Dòng hãm/hồ quang DC vượt định mức | Thông mạch 30–87 khi cuộn mất điện | Relay định mức DC cao hơn; cân nhắc hai relay nối tiếp |

### 9. Câu hỏi ngược

1. **[Failure mode]** Tiếp điểm 87 dính. E-stop nhấn, cuộn mất điện, VM vẫn còn. Thiết kế hiện tại phát hiện được không, bằng tín hiệu nào, và phát hiện rồi thì làm gì?
   <details><summary>Hướng nghĩ</summary>

   Relay changeover có tiếp điểm gắn cơ khí: nếu 87 dính, 87a thường **không** đóng được, nên RELAY_FB không lên trong khi COIL_SENSE đã xuống — mâu thuẫn đo được. ESP32 vẫn tắt driver (tầng 1 đỡ tầng 0) và chặn ARM tới khi thay relay. Hai relay nối tiếp làm một lỗi dính đơn lẻ không đủ gây nguy hiểm; đó là ý tưởng dự phòng có giám sát trong các chuẩn an toàn máy.

   </details>
2. **[Nếu…thì]** Nếu robot đứng trên đoạn dốc (bãi xe tầng hầm, ram dốc cho xe lăn), "cắt năng lượng motor" còn là trạng thái an toàn không? Thiết kế đổi thế nào?
   <details><summary>Hướng nghĩ</summary>

   Trạng thái an toàn là thuộc tính của hệ trong bối cảnh. Thang máy, tay máy dùng phanh **lò xo đóng, điện mở**: mất điện thì phanh giữ. Hộp số trục vít tự hãm là phương án khác. Câu hỏi đi kèm: robot có được phép tới vùng dốc không — đó là quyết định ở bản đồ (C8), không ở relay.

   </details>
3. **[Vì sao không]** Vì sao không làm E-stop bằng topic ROS 2 QoS reliable, ưu tiên cao, gửi từ nút trên điện thoại?
   <details><summary>Hướng nghĩ</summary>

   Liệt kê mọi thứ phải còn sống để topic đó dừng được motor: điện thoại, WiFi, router, mini PC, DDS, node, USB, ESP32. So với chuỗi: nút → dây → cuộn. "E-stop từ xa" có giá trị như tầng 3; muốn từ xa thật thì dùng bộ phát vô tuyến chuyên dụng mà **mất sóng = dừng** (tín hiệu động, giống xung giữ).

   </details>
4. **[Quy mô]** 100 robot, mỗi robot có E-stop, watchdog độc lập, bumper. Sự kiện an toàn thành một luồng dữ liệu. Bạn ghi gì mỗi sự kiện, và chỉ số nào cho thấy một **thiết kế** (không phải một robot) có vấn đề?
   <details><summary>Hướng nghĩ</summary>

   Ai kích hoạt, robot ở trạng thái nào, tốc độ, khoảng cách người gần nhất, t_relay đo được (từ RELAY_FB), phiên bản firmware/bo. Chỉ số: phân bố t_relay theo lô relay (relay già nhả chậm dần là lỗi tích lũy → F7.6), tỉ lệ T0b kích hoạt theo phiên bản firmware (watchdog trip là firmware treo), tỉ lệ E-stop do người ngoài nhấn trên giờ chạy (HRI, C10.4).

   </details>
5. **[Liên ngành]** Thanh điều khiển lò phản ứng hạt nhân được giữ phía trên lõi bằng nam châm điện; mất điện thì rơi vào lõi nhờ trọng lực. So với mạch relay và mạch xung giữ của bạn.
   <details><summary>Hướng nghĩ</summary>

   Cùng nguyên lý: cần năng lượng để **giữ** trạng thái nguy hiểm, mất năng lượng thì về trạng thái an toàn bằng lực tự nhiên (trọng lực, lò xo relay). Khác: hệ dừng lò có nhiều kênh cảm biến độc lập và biểu quyết (ví dụ 2 trên 3) để vừa an toàn vừa tránh dừng oan; robot của bạn có một chuỗi.

   </details>

### 10. Liên kết ra ngoài

- **Đường sắt — thiết bị "người chết" (dead man's switch) và vigilance device.** Lái tàu phải tác động định kỳ lên một cần; không tác động thì tàu tự hãm. Giống mạch xung giữ: một trạng thái tĩnh (người ngủ gục đè lên cần) không đủ để giữ, phải có **thay đổi** định kỳ. Khác: thứ được giám sát là con người.
- **Thang máy — bộ khống chế vượt tốc (governor) và phanh an toàn.** Thang máy có cơ cấu cơ khí kích hoạt phanh an toàn khi cabin vượt tốc độ, độc lập với bộ điều khiển. Giống: giám sát **tốc độ đo được** độc lập với lệnh (phương án B của bạn). Khác: thang máy có trạng thái "đứng yên + phanh giữ"; robot của bạn trôi tự do sau khi cắt điện.
- **Hạt nhân — biểu quyết 2 trên 3.** Như câu 5: giải đánh đổi "dừng oan vs phát hiện chậm" bằng dự phòng thay vì nới timeout. Với robot một bo, bạn giải bằng chọn timeout (C4.4); với đội robot, bằng thống kê.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| Therac-25: ≥6 tai nạn quá liều 1985–1987, bỏ interlock phần cứng, race condition và tràn biến 1 byte | [chuẩn] | Leveson & Turner, IEEE Computer, 1993 |
| Dừng loại 0/1/2; E-stop chỉ loại 0 hoặc 1; reset không tự khởi động lại | [spec] | IEC 60204-1, ISO 13850 (qua tài liệu của các hãng như ABB, Kollmorgen); kiểm bản chuẩn nếu trích điều khoản |
| Mở cưỡng bức theo IEC 60947-5-1 phụ lục K | [spec] | Ký hiệu trên khối tiếp điểm nút |
| TPS3823: timeout điển hình 1,6 s, tối thiểu 0,9 s; WDI để hở có thể vô hiệu watchdog | [spec] | TI SLVS165; các nguồn thứ cấp mô tả hành vi WDI khác nhau — đọc datasheet bản mới |
| Relay nhả chậm hơn khi cuộn chỉ có diode | [chuẩn] | App note coil suppression của hãng relay; đo |
| LEDC/ngoại vi chạy tiếp khi CPU treo | [chuẩn] | Ngoại vi phần cứng chạy theo clock riêng; tự kiểm bằng `FAULT_HANG_ALL` |
| Kết quả mô phỏng xung giữ, quãng dừng | [đã chạy] | Linh kiện và gia tốc là giả định |
| Bumper < 10 ms; t_relay thật | [tự đo] | Logic analyzer |

**Đã sửa so với bản gốc / nguyên liệu cũ / Gemini:**
- Gốc: bảng bốn tầng ghi watchdog "~100 ms" nhưng bước làm là 5 nhịp ở 10 Hz và tiêu chí "< 500 ms" → phản ứng ≈ timeout + chu kỳ kiểm; tiêu chí là bất đẳng thức theo timeout chọn ở C4.4 (không đổi ngưỡng gate).
- Gốc: FMEA nói relay "phải do một đường độc lập điều khiển" nhưng Bài 15 không thiết kế đường đó → thêm watchdog độc lập (ba phương án), mặc định mạch xung giữ, cùng bẫy LEDC/ISR.
- Gốc: "VM về 0" ngầm làm mốc đo E-stop → dùng chân 87a (RELAY_FB); VM bị back-EMF giữ khi bánh còn quay.
- Gốc: không phân biệt E-stop với dừng mềm, không nói loại dừng → thêm loại 0/1/2 theo IEC 60204-1, ISO 13850; loại 1 chỉ với bộ trễ phần cứng.
- Bổ sung: E-stop NC mở cưỡng bức, energize-to-run, chốt và reset ba phần (gốc chỉ nói "cắt nguồn").
- Nguyên liệu cũ: phần heartbeat/timeout chuyển về C4.4 (firmware); bài này chỉ đo lại trên robot hoàn chỉnh.
- Gemini: "E-stop tức thì, 2–5 ms theo quán tính nhả tiếp điểm" không nhãn → `[tự đo]`, phụ thuộc relay và mạch dập.
- Gemini: "nice -20" cho node serial → `nice` chỉ đổi trọng số CFS; dùng `chrt -f` và đo lại.
- Gemini: "dừng khựng ngay lập tức" trong kết quả 20/20 → dừng loại 0 là **trôi**; tiêu chí là "dừng", quãng trôi là một số đo riêng.

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** Leveson & Turner, *An Investigation of the Therac-25 Accidents*, IEEE Computer, 1993. IEC 60204-1 (mục chức năng dừng, dừng khẩn cấp) và ISO 13850 — đọc tóm tắt của hãng thiết bị an toàn.
- **Giải thích:** Phil Koopman, *Better Embedded System Software* (2010), chương về watchdog timer.
- **Đào sâu (tùy chọn):** Nancy Leveson, *Engineering a Safer World* (MIT Press, 2011).
- **Tự kiểm tra:** (1) giải thích cho một backend engineer trong 5 câu vì sao xung giữ phải đi ra từ task điều khiển; (2) vẽ lại chuỗi FD → nút → cuộn → Q1 và mạch xung giữ từ trí nhớ; (3) hai câu dưới.

  a. Robot 6 kg chạy 1,0 m/s. Động năng gấp bao nhiêu lần ở 0,5 m/s? Thời gian phản ứng 0,5 s (lease) thì robot đi thêm bao xa trước khi bắt đầu giảm tốc?
  <details><summary>Đáp án</summary>

  Gấp 4 lần (3 J so với 0,75 J). Đi thêm 1,0 × 0,5 = 50 cm trước khi giảm tốc — lý do lease không phải tầng chống va chạm; bumper mới là.

  </details>

  b. Một bạn đề xuất: "bỏ mạch xung giữ, cho mini PC điều khiển relay qua một module relay USB". Chấm đề xuất.
  <details><summary>Đáp án</summary>

  **SAI** cho mục đích "cắt khi ESP32 treo": thêm mini PC, USB, driver, phần mềm vào đường dừng; mini PC treo thì module relay giữ trạng thái cuối (tín hiệu tĩnh). Nếu module chỉ giữ relay khi nhận lệnh định kỳ (tín hiệu động) thì thành một watchdog **tầng 3**, hữu ích nhưng không độc lập với Linux.

  </details>

---
