# Chặng 12 — Sản phẩm: robot confession (30h)

> **Vị trí:** C10 (an toàn, vận hành), C11.2 (HIL, CI) → **C12** → hết K7 · **Cần trước:** K3 trọn (chuỗi phát, moderation, kill switch, soak), K7 C9 (nhận người, hai lớp đồng ý), C10, C11.2; → F5.7, F7.4 · **Chạy song song với:** — (chặng cuối)
> **Làm ra được:** chuỗi audio K3 gắn trên robot (amp ăn từ pack qua cầu chì riêng, loa trên cột, đường tín hiệu chống nhiễu, kill switch NC), robot giao một confession đầu–cuối · bảng nhiễu audio theo cấu hình đo được, jitter vòng điều khiển trước/sau khi thêm audio, state machine sản phẩm có test bất biến, SLO đầu–cuối, demo, bài viết chính và bài tổng kết · **Sau chặng này bạn quyết định được:** amp ăn nguồn ở đâu và tín hiệu đi dây thế nào; audio chạy chung ESP32 với vòng điều khiển hay tách MCU; robot có được phát khi đang chạy không; câu chuyện phỏng vấn của bạn nói gì và **không** nói gì.

Đây là chỗ hai đường ray gặp nhau: chuỗi audio của K3 (cái loa đọc confession ẩn danh) và con robot của K7 (đi tìm một người). Ý định sản phẩm gốc là năm version: loa → giọng tự clone → camera chào hỏi → tự đi tới người được nhắc tên → tay máy (`docs/Claude-Xây dựng robot confession…md`). Bản review đầu tiên đã chấm V4 là bước nhảy ~10 lần độ khó so với V1–V3, và Phụ lục A chỉ ra V4 là **một sản phẩm khác về bản chất**: kênh nhắm cá nhân có khuếch đại. C12 ghép V1 + V2 + V3 + V4 thành một luồng có kiểm soát, đo được, và dừng được.

**Phân bổ 30h** `[ước lượng]`:

| Phần | Giờ | Trong đó lắp |
|---|---|---|
| Bài C12.1 Gắn chuỗi audio lên robot | 12 | ~5: lắp bước 1–4 |
| Bài C12.2 Luồng sản phẩm đầu–cuối và state machine sản phẩm | 10 | ~1: lắp bước 5 (chạy đầu–cuối) |
| Bài C12.3 Demo, bài tổng kết, câu chuyện phỏng vấn *(rút gọn)* | 8 | gồm Gate chặng 12 (= gate tổng K7 phần sản phẩm) |
| **Tổng** | **30** | |

## 0. Bức tranh chặng

Robot sau C12: trên cột (C9) thêm một loa nhỏ quay về phía trước; trong khung thêm một module amp class-D ăn thẳng từ pack qua cầu chì riêng; tín hiệu từ ESP32 đi I2S tới DAC rồi bằng cáp xoắn đôi tới amp. E-stop vẫn chỉ cắt động lực; audio có đường cắt riêng (kill switch NC của K3 Bài 15).

```
 PACK 4S ─[F0]─ SW ─ shunt ─ THANH CÁI + ─┬─[FA]─ relay E-stop ─ driver ─ motor   (C1, C10.1)
                                          ├─[FB]─ buck-boost 12 V ─ mini PC
                                          ├─[FC]─ buck 5 V ─ ESP32, DAC, mic
                                          ├─[FD]─ cuộn relay E-stop
                                          └─[FE mới]─ AMP class-D (8–26 V) ═══ loa (BTL, không cọc nào là GND)
                                                 ▲ IN+  IN−  (giả vi sai, cáp xoắn đôi)
 ESP32 ─I2S─► PCM5102A ─OUT ─────────────────────┘    │
            (XSMT) ◄── nút KILL NC (K3 Bài 15)        └── GND tham chiếu của DAC (dây thứ hai của cặp xoắn)
 GND: mọi đường về ĐIỂM SAO (C1); dòng motor KHÔNG đi qua đoạn GND mà DAC và amp cùng dùng.
```

Dòng dữ liệu sản phẩm: Google Form → ingest + state machine (K3 Bài 14) → moderation (K3 Bài 15) → kiểm lớp 2/DND/rate limit (C9.1) → task → Nav2 (C8.4) → dừng, nhận diện, nút xác nhận (C9.4) → kiểm lại server → streamer (K3 Bài 16) → loa → về.

## 1. An toàn của chặng

**Rủi ro:** nhánh nguồn mới từ pack (chập ở amp hoặc dây loa → dòng lớn); dây loa BTL bị nối xuống GND (hỏng tầng ra amp); âm lượng lớn sát tai người (robot đứng 1–1,5 m trước mặt); robot di chuyển khi đang phát, người nhận đi theo robot; nội dung nhạy cảm phát cho nhầm người (C9).

**Quy tắc cứng:**
- KHÔNG nối amp vào thanh cái khi chưa có cầu chì FE riêng và chưa thử trên nguồn bàn giới hạn dòng (C0.4).
- KHÔNG nối bất kỳ cọc loa nào xuống GND, kể cả kẹp GND của que đo hay logic analyzer (BTL, → K3 Bài 5).
- KHÔNG cắm/rút loa khi amp đang có điện.
- KHÔNG để robot chạy khi đang phát: trạng thái `SPEAKING` chỉ vào được từ `STOPPED` và giữ lệnh vận tốc bằng 0 (C12.2). Đây là quy tắc sản phẩm và an toàn cùng lúc.
- KHÔNG đặt âm lượng theo cảm giác: trần âm lượng nằm trong firmware/host, chọn bằng đo (C12.1), không có nút "to hơn" vượt trần.
- KHÔNG coi E-stop là nút tắt tiếng. E-stop cắt động lực; nút kill cắt audio (K3 Bài 15). Hai nút, hai đường, cả hai thử định kỳ.
- KHÔNG phát khi pack dưới ngưỡng điện áp đã đo cho amp (clipping và sụt áp kéo theo brownout, → K3 Bài 6).
- KHÔNG demo trước người chưa biết về dự án; người được nhắc tên trong demo phải là người đã bật lớp 2.

**Khi sự cố xảy ra:**

| Sự cố | Làm ngay | KHÔNG |
|---|---|---|
| Amp hoặc dây loa nóng, có mùi khét | Gạt công tắc chính (hoặc rút XT60 pack) → đợi → kiểm cầu chì FE và dây | Rút dây loa bằng tay trần khi còn điện |
| Loa phát nội dung cho nhầm người hoặc nội dung chưa duyệt | Bấm kill (L2: XSMT/mute phần cứng) → task `KILLED` → `incidents.md` | Tắt app rồi tin là đã im |
| Tiếng rú (feedback) khi bật mic | Kill → hạ gain mic/loa | Đứng che loa bằng tay rồi chạy tiếp |

## 2. BOM chặng

Giá `[ước lượng 10/2026]`. Món đã có từ K3 (PCM5102A, INMP441, loa 4 Ω, amp PAM8403, nút kill) dùng lại; chỉ mua thêm thứ cần cho robot.

| Món | Thông số phải chọn | Vì sao (bằng số) | Giá | Kiểm khi nhận | Thay thế được bằng |
|---|---|---|---|---|---|
| Module amp class-D ăn từ pack | Dải nguồn bao trọn pack (4S Li-ion 12–16,8 V `[chuẩn]`), **đầu vào vi sai**, có chân shutdown/mute; ví dụ họ TPA3110D2 (nguồn 8–26 V `[spec — datasheet TI, kiểm]`) | Không cần buck riêng; đầu vào vi sai cho phép nối giả vi sai (C12.1) | 80–200k | Đọc mã chip trên module; đo dòng nghỉ trên nguồn bàn | PAM8403/MAX98357A trên nhánh 5 V (nguồn 2,5–5,5 V `[spec]`): tăng tải buck 5 V và dùng chung rail với logic |
| Loa full-range có hộp | 4–8 Ω, 3–5 W, đường kính 50–80 mm | Robot đứng 1–1,5 m trước người; cần ~1 W thật `[ước lượng]` | 50–200k | Đo Ω DC (thấp hơn danh định, → K3 Bài 5) | Loa của K3 |
| Cầu chì FE + giá | Định mức theo dòng đỉnh amp đo được (C12.1), cỡ 2–3 A `[ước lượng]` | Bảo vệ dây nhánh amp (C1.3) | 20–50k | — | — |
| Tụ bulk sát amp | 470–1000 µF, ≥25 V | Gánh dòng đỉnh, giảm gợn từ nhánh motor (→ K3 Bài 6) | 10–30k | Cực tính, điện áp ghi trên vỏ | — |
| Cáp tín hiệu audio | Xoắn đôi có lưới chống nhiễu (cáp mic/cáp audio), 0,3–0,6 m | Tín hiệu line-level đi gần dây motor | 20–50k/m | Thông mạch, lưới không chạm lõi | Hai dây 26 AWG tự xoắn |
| Vòng ferrite kẹp | Cho dây 3–6 mm | Giảm nhiễu tần số cao trên dây motor/dây nguồn amp `[tự đo — hiệu quả phụ thuộc tần số]` | 10–30k/cái | — | — |
| (tùy chọn) ESP32-S3 thứ hai | DevKit như K1 | Nếu audio làm jitter vòng điều khiển vượt ngưỡng C4 (C12.1) | 150–250k | — | Dùng chung ESP32 nếu đo đạt |
| (tùy chọn) Bộ cách ly ground loop | Biến áp audio 3,5 mm | Cắt vòng đất khi không sửa được đi dây | 50–100k | — | Sửa đi dây (ưu tiên) |

**Tổng C12 `[ước lượng]`:** ~0,3–0,9tr.

## 3. Dụng cụ và kỹ năng tay

| Kỹ năng | Bài | Luyện trên phế liệu | Đạt trông thế nào |
|---|---|---|---|
| Đi dây tín hiệu xa dây công suất: tách bó, cắt ngang 90° | C12.1 | — | Cáp audio không chạy song song dây motor đoạn nào dài hơn vài cm; ảnh trước/sau |
| Hàn cáp có lưới chống nhiễu, nối lưới **một đầu** | C12.1 | 2 đầu cáp thừa | Lưới xoắn gọn, co nhiệt, không chạm lõi; đầu kia cắt và bọc |
| Đo nhiễu bằng mic + phổ (thay máy hiện sóng) | C12.1 | Ghi phòng yên tĩnh 30 s | Phổ có đơn vị dBFS, ghi gain, khoảng cách, vị trí mic |
| Gá loa trên cột, chống rung | C12.1 | — | Gõ nhẹ khung khi phát: không có tiếng lạch cạch; ốc có khóa (C2.3) |

## 4. Sơ đồ đi dây

```
 NHÁNH NGUỒN AMP (mới)                                      ĐƯỜNG TÍN HIỆU (giả vi sai)
 THANH CÁI + ─[FE 2–3 A]─ 20AWG đỏ ─┬─ AMP PVCC              PCM5102A OUT_L ───┐ cặp xoắn có lưới
                                    ═╪═ 1000 µF sát amp       PCM5102A AGND  ───┤ (lưới nối GND
 ĐIỂM SAO GND ───── 20AWG đen ──────┴─ AMP GND                                  │  CHỈ phía DAC)
                                                              ────────────────► AMP IN+  (L)
 AMP OUT+ ═══ 20AWG (cặp xoắn) ═══ LOA +                      ────────────────► AMP IN−  (L)
 AMP OUT− ═══                ═══ LOA −   (KHÔNG cọc nào về GND)
 AMP /SD ◄── GPIO ESP32 qua nút KILL NC (mức mất điện/đứt dây = shutdown) — theo K3 Bài 15 tầng L2
```

| wire_id | net | từ → tới | AWG | màu | dài (m) | cầu chì |
|---|---|---|---|---|---|---|
| W80/W81 | VIN_AMP / GND | FE → amp; về điểm sao | 20 | đỏ (nhãn AMP)/đen | ~0,3 | FE |
| W82 | SPK± | amp → loa | 20, xoắn | màu loa, nhãn SPK | ~0,6 (lên cột) | — |
| W83 | AUDIO_L± | DAC → amp IN± | cáp xoắn có lưới | nhãn AUD | ≤0,5 | — |
| W84 | AMP_SD | nút kill → amp /SD | 24 | nhãn đỏ hai đầu (đường an toàn audio) | ~0,5 | — |

Cập nhật `power/budget.csv` dòng `amp_audio` bằng số đo thật (C1.2 đã để sẵn dòng ước lượng; CI `test_power_budget` của C1 sẽ đỏ nếu quên).

## 5. Trình tự chặng

1. **Học Bài C12.1 phần 1–5**, commit `prediction.md`.
2. **Lắp bước 1 — Amp trên bàn, nguồn bàn.** V_set = 12,0 V rồi 16,8 V (hai đầu dải pack), I_set 1 A; loa nối; phát sin 1 kHz ở mức trần dự kiến.
   - ✅ Checkpoint trước khi cấp điện: Ω giữa PVCC và GND của amp không gần 0; Ω giữa từng cọc loa và GND: **hở** (BTL); cực tính tụ bulk đúng.
   - Nếu sai: không cấp điện; tìm chập.
3. **Lắp bước 2 — Nhánh FE trên robot.** Cầu chì FE, dây W80/W81 về điểm sao, amp gá trong khung xa driver motor.
   - ✅ Checkpoint: công tắc chính OFF; Ω thanh cái + → GND không gần 0; FE đã lắp đúng định mức; đo dòng nghỉ amp khi bật (INA226 hoặc UT33D+ thang A nối tiếp).
4. **Lắp bước 3 — Đo nhiễu ba cấu hình** (C12.1 phần 6): đơn cực → giả vi sai → giả vi sai + đi dây lại/ferrite. Bánh nhấc khỏi sàn.
5. **Lắp bước 4 — Kill switch và jitter.** Thử kill L2 trên robot khi đang phát; đo jitter vòng điều khiển C4 có/không có task audio.
   - ✅ Checkpoint: kill làm loa im trong thời gian đo được ở K3 Bài 15, kể cả khi daemon bị `SIGSTOP`; jitter p99 vẫn trong ngưỡng gate C4.
6. **Học Bài C12.2**, chạy test bất biến; **lắp bước 5 — một confession đầu–cuối** trên robot thật với người đã bật lớp 2.
7. **Bài C12.3**: demo, bài viết chính, bài tổng kết; **Gate chặng 12**.

## 6. Lỗi người mới hay gặp

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Tiếng rè theo tốc độ motor | GND tín hiệu đi chung đoạn với dòng motor; đầu vào đơn cực | So nhiễu khi motor chạy/không, amp mute/không | Giả vi sai; dời đường GND (C12.1) |
| Ù đều 50/100 Hz chỉ khi cắm sạc hoặc màn hình | Vòng đất qua sạc/HDMI/USB của laptop | Rút từng cáp ngoài | Chỉ đo khi robot chạy pin; nếu bắt buộc cắm, cách ly |
| ESP32 reset khi phát bass lớn lúc motor tăng tốc | Sụt áp nhánh chung (→ K3 Bài 6, F5.7) | `esp_reset_reason()`, log INA226 | Amp ăn từ pack qua FE, không từ buck 5 V; tụ bulk; không phát khi chạy |
| Tiếng bụp khi bật/tắt robot | Amp lên nguồn trước khi DAC ổn định | Nghe lúc bật | Giữ /SD thấp tới khi ESP32 sẵn sàng |
| Tiếng nhỏ dần khi pin cạn | Amp clip sớm hơn ở điện áp thấp | Phát sin ở 12 V và 16,8 V trên nguồn bàn | Trần âm lượng chọn ở 12 V |
| Loa lạch cạch khi phát | Cột/loa rung | Gõ khung | Đệm cao su, siết ốc khóa |

## 7. Lăng kính data infra

**Dữ liệu chặng này sinh ra:**

| Luồng | Nơi | Schema rút gọn | Ghi chú |
|---|---|---|---|
| Đo nhiễu audio | `lab/c12/noise-<cấu hình>.wav` + `measurements.jsonl` | `config`, `motor_pwm`, `amp_state`, `mic_gain`, `distance_m`, `noise_dbfs_band`, `instrument_id` | Ghi âm **im lặng số** (không có giọng người); mic đặt cố định |
| Sự kiện sản phẩm | MCAP `/product/event` + DB server | `confession_id` (không nội dung), `delivery_id`, `state_from`, `state_to`, `reason`, `t_event` (wall + mono + `boot_id`) | Nội dung confession KHÔNG vào MCAP |
| Jitter vòng điều khiển | như C4 | thêm cột `audio_active` | So hai phân bố |

**Test tự động (hạt giống cho C11.2):** `test_product_invariants` (C12.2: không phát khi lớp 2 tắt/DND tại thời điểm phát, không phát một tin hai lần, không phát khi đang chạy); `test_audio_noise_floor` (HIL: chạy motor theo lịch cố định, ghi mic, FAIL nếu nhiễu trong dải thoại vượt mức đã ghi ở gate C12); `test_jitter_with_audio`; `test_power_budget` (C1) với dòng amp thật.

**SLI/SLO đầu–cuối** (→ F7.4): từ lúc confession được duyệt tới lúc phát xong cho người nhận đã xác nhận; ghép từ SLI của K3 (ingest, TTS, phát) và C9 (thời gian tới quyết định, timeout theo người). Hợp đồng soak của K3 Bài 17 dùng lại cho luồng sản phẩm.

**Vai trò nghề:** Systems Architect (ghép hai state machine, chọn ranh giới MCU), Test & Validation (bất biến sản phẩm, HIL), Technical Writer (bài viết chính). Bản đồ đầy đủ ở C12.3.

## 8. Nhật ký build

Copy vào `build-log/c12.md`:

```markdown

## 2026-MM-DD — buổi N (giờ bắt đầu–kết thúc, giờ thực: _._ h)
- Trạng thái người: tỉnh táo / mệt (mệt → chỉ đọc, không đụng nhánh nguồn)
- Mục tiêu buổi:
- Cấu hình audio: amp __, nguồn amp __, đầu vào đơn cực/giả vi sai, ferrite có/không
- Pack: điện áp đầu buổi __ V, cuối buổi __ V
- Số đo (measurements.jsonl, số dòng: __); file ghi âm: __
- Jitter vòng điều khiển có audio: p99 __ µs (n = __)
- Confession chạy đầu–cuối: delivery_id __, kết thúc ở trạng thái __, lý do __
- Lỗi gặp (triệu chứng → nguyên nhân → sửa):
- Quyết định (decisions.md):
- Sự cố / suýt sự cố: không / có → incidents.md
- Câu hỏi còn mở:
```

---
