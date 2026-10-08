# KHÓA 7 — ROBOT DI ĐỘNG HOÀN CHỈNH
## Từ mạch điện tới CI khép kín, một sản phẩm chạy thật

**Cho:** người đã PASS Khóa 1–6. **Không có ngoại lệ cho Khóa 6** — không có harness đánh giá thì đây chỉ là một con robot hobby nữa.
**Thời lượng:** ~340h · **Trần:** 450h. Ở nhịp 6h/tuần là **13–17 tháng**.
**Chi phí:** 8–15tr, chia làm 4 đợt theo từng khóa con.
**Vị trí:** dự án tích hợp, không phải khóa học. Đây là chỗ mọi thứ đã học phải cùng chạy một lúc.

---

## ĐỌC TRƯỚC — BA ĐIỀU PHẢI QUYẾT TRƯỚC KHI MUA GÌ

### 1. Thời điểm

340 giờ ở nhịp hiện tại là **13 tháng**. Đó là một dự án dài bằng cả Khóa 1–4 cộng lại.

Tôi vẫn khuyên: **apply sau Khóa 6, có việc, rồi chạy Khóa 7 nền.** Lúc đó bạn có thu nhập robotics trả cho phần cứng, có đồng nghiệp để hỏi, có ngữ cảnh thật để thiết kế. Con robot làm trong hoàn cảnh đó sẽ tốt hơn nhiều so với phiên bản làm trong cô lập.

Nhưng bạn đã nói nó quan trọng hơn cả việc có job. Đó là một lý do hợp lệ — dream product là dream product. Chỉ cần ghi vào `decisions.md` hôm nay rằng bạn chọn nó **có ý thức**, kèm ngày tháng, để 8 tháng nữa bạn không tự hỏi vì sao mình chưa đi làm.

Và một gợi ý dung hòa mà tôi nghĩ là tốt nhất: **chạy 7A song song với M5 (apply).** 7A là 60h phần cứng thuần, không cần não cho việc viết CV. Hai việc không tranh nhau.

### 2. Năm khóa con, mỗi cái publish độc lập

| | Nội dung | Giờ | Chi phí | Publish được gì |
|---|---|---|---|---|
| **7A** | Chassis, motor, encoder, odometry, vòng điều khiển | 60 | 2–3tr | Bài về hiệu chuẩn odometry có số |
| **7B** | Định vị và điều hướng | 80 | 1–3tr | Bài về độ lặp lại điều hướng |
| **7C** | Nhận người on-device, privacy-first | 60 | 0–3tr | Bài về FAR/FRR và privacy-by-design |
| **7D** | Tích hợp, an toàn, state machine | 60 | ~1tr | Bài về failure mode analysis |
| **7E** | **Full test flow: sim + HIL + data + finetune** | 80 | ~0đ | **Bài chính — vòng CI khép kín cho robot thật** |

Mỗi khóa con có gate riêng và artifact riêng. Nếu đứt gánh giữa chừng, bạn vẫn có thứ để chỉ vào. **Đó là thiết kế có chủ đích** — dự án 13 tháng phải chịu được việc bị dừng.

### 3. Thứ tự không đảo được

7E là thứ biến bốn phần trước từ "con robot" thành "hệ thống có thể vận hành và nâng cấp". Nhưng 7E cần 7A–7D đã chạy, và cần Khóa 5 (data infra) + Khóa 6 (sim & eval) đã xong.

**Nếu chỉ làm được một phần, làm 7A và 7E.** Một robot đi thẳng được, có sim khớp với thực tế, có CI phán quyết được — đó đã là câu chuyện phỏng vấn hoàn chỉnh, kể cả khi nó không biết nhận mặt ai.

---

## KIẾN TRÚC HỆ THỐNG

```
                        ┌──────────────────────────────┐
                        │  LAPTOP / SERVER (nhà)       │
                        │  ├ Ingest + MCAP store  (K5) │
                        │  ├ Audit + validation   (K2) │
                        │  ├ Sim + eval CI        (K6) │
                        │  ├ Foxglove                  │
                        │  └ Fine-tune (GPU thuê) (K4) │
                        └──────────────┬───────────────┘
                                       │ WiFi, resumable upload
                        ┌──────────────┴───────────────┐
                        │  PI 5 (trên robot)           │
                        │  ├ ROS 2 · Nav2         (K3) │
                        │  ├ Perception on-device (7C) │
                        │  ├ MCAP sidecar         (K5) │
                        │  └ State machine + mod  (K3) │
                        └──────────────┬───────────────┘
                                       │ UART / USB, 100 Hz
                        ┌──────────────┴───────────────┐
                        │  ESP32-S3 (vòng điều khiển)  │
                        │  ├ PID bánh trái/phải        │
                        │  ├ Đọc encoder quadrature    │
                        │  ├ Watchdog + failsafe       │
                        │  └ Timestamp nguồn      (K5) │
                        └──────────────┬───────────────┘
                                       │ PWM + DIR
                        ┌──────────────┴───────────────┐
                        │  PHẦN CỨNG                   │
                        │  motor · encoder · driver    │
                        │  ═══ E-STOP VẬT LÝ ═══       │
                        │  (cắt nguồn động lực)        │
                        └──────────────────────────────┘
```

**Ba quyết định kiến trúc phải tự bảo vệ được:**

**Vì sao tách MCU khỏi Pi.** Vòng điều khiển bánh xe cần deterministic ở 100–200 Hz. Linux có scheduler; ESP32 không. Đây chính là ranh giới MCU/MPU bạn đã học ở tài liệu nền Phần 2.1, giờ áp dụng thật. Và nó cho bạn một câu trả lời phỏng vấn rất cụ thể khi người ta hỏi "vì sao không chạy hết trên Pi".

**Vì sao Pi 5 lần này thực sự cần.** Ở Khóa 3–5 tôi khuyên bỏ Pi vì laptop + ESP32 làm được. Ở đây khác: robot phải mang theo compute, chạy perception on-device, và chạy ROS 2. Đây là lúc mua Pi 5 — và nếu `ethtool -T` của nó có PTP hardware clock thì bạn được thêm một target cho các thí nghiệm Khóa 5.

**Vì sao E-stop nằm ở tầng thấp nhất.** An toàn không phải một cờ phần mềm. Chi tiết ở 7D.

---

# 7A — CHASSIS, MOTOR, ENCODER, ODOMETRY (60h)

**Mua đợt này:** khung xe 2 bánh + caster, 2 motor DC có hộp số và encoder, driver motor, pin + BMS + sạc, công tắc E-stop. ~2–3tr.

---

## Bài 1 — Motor, encoder, driver: ba thứ phải hiểu trước khi cấp điện (8h)

**Câu hỏi:** một lệnh PWM biến thành bao nhiêu vòng quay?

### Khái niệm

**Motor DC có hộp số + encoder** là ba bộ phận trong một vỏ, và bạn phải tách chúng ra trong đầu:

| Bộ phận | Đặc trưng | Số phải biết |
|---|---|---|
| Motor DC | Tốc độ ~tỉ lệ điện áp, mô-men ~tỉ lệ dòng | Điện áp danh định, dòng không tải, **dòng hãm (stall current)** |
| Hộp số | Giảm tốc, tăng mô-men | Tỉ số truyền, ví dụ 1:34 |
| Encoder | Đếm xung theo góc quay | PPR trên trục motor |

**Công thức bạn phải tự dẫn được:**

```
counts_mỗi_vòng_bánh = PPR × tỉ_số_truyền × 4
```

Nhân 4 vì **quadrature decoding**: hai kênh A và B lệch pha 90°, mỗi kênh có cạnh lên và cạnh xuống → 4 sự kiện đếm được mỗi chu kỳ. Bỏ hệ số 4 là lỗi phổ biến nhất, và nó làm odometry của bạn sai đúng 4 lần.

Ví dụ điển hình: PPR = 11, tỉ số 1:34 → `11 × 34 × 4 = 1496` counts mỗi vòng bánh.

Bánh đường kính 65mm → chu vi `π × 65 = 204.2 mm` → **một count = 0.136 mm**. Đó là độ phân giải odometry của bạn, và nó rất tốt — vấn đề không bao giờ nằm ở độ phân giải, nó nằm ở sai số hệ thống. Bài 4 sẽ chứng minh.

**Dòng hãm là số nguy hiểm nhất trong datasheet.** Motor bị kẹt rút dòng gấp nhiều lần lúc chạy bình thường. Driver phải chịu được, nguồn phải chịu được, và bạn phải có bảo vệ. Đây đúng là bài học TN-3 của Khóa 3 (servo làm Pi brownout), nhưng ở quy mô lớn hơn nhiều lần.

### Làm

1. Đọc trọn datasheet motor và driver. Ghi: điện áp, dòng không tải, dòng hãm, PPR, tỉ số truyền.
2. Tính `counts_mỗi_vòng_bánh` và `mm_mỗi_count`. **Commit vào `prediction.md`.**
3. Cấp điện motor **không tải**, đo dòng bằng multimeter. So với datasheet.
4. **Giữ trục motor bằng tay cho tới khi nó ngừng quay** (rất nhanh, 1–2 giây, đừng giữ lâu) và đọc dòng. Đó là dòng hãm thật.
5. Cắm logic analyzer vào hai kênh encoder. Quay bánh **bằng tay đúng một vòng**. Đếm số cạnh.
6. Lặp bước 5 với 10 vòng. Chia trung bình.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Counts đếm được cho 10 vòng | Gần `10 × 1496 = 14.960`, lệch <1% |
| Dạng sóng encoder trên logic analyzer | Hai kênh vuông, **lệch pha 90°**. Đảo chiều quay → thứ tự cạnh đảo lại |
| Dòng không tải | Khớp datasheet trong ±30% |
| Dòng hãm | **Gấp nhiều lần dòng không tải.** Ghi con số thật, nó quyết định chọn driver và nguồn |

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Counts bằng 1/4 dự đoán | Đang đếm 1x thay vì 4x | Bật quadrature 4x trong cấu hình |
| Counts bằng 1/2 | Đếm 2x, hoặc mất một kênh | Kiểm dây kênh B |
| Hai kênh không lệch 90° mà trùng pha | Đấu nhầm, hoặc encoder hỏng | Đổi dây. Nếu trùng pha thật thì không xác định được chiều quay |
| Counts nhảy lung tung khi quay nhanh | Mất xung do interrupt không kịp | **Dùng module PCNT phần cứng của ESP32-S3**, đừng đếm bằng interrupt phần mềm |

Triệu chứng cuối là bài học quan trọng: encoder ở tốc độ cao sinh hàng chục nghìn xung mỗi giây. Đếm bằng phần mềm sẽ mất xung, và mất xung thì odometry trôi vĩnh viễn — không có cơ chế nào sửa lại được. ESP32-S3 có bộ đếm xung phần cứng; dùng nó.

---

## Bài 2 — Đường cong PWM → vận tốc, và vùng chết (8h)

**Câu hỏi:** lệnh 20% PWM cho ra bao nhiêu m/s?

### Khái niệm

Câu trả lời ngây thơ: 20% của tốc độ tối đa. Câu trả lời thật: **có thể là 0**.

Motor có **vùng chết (deadband)**: dưới một ngưỡng PWM nào đó, mô-men không thắng nổi ma sát tĩnh và bánh đứng yên. Ngưỡng này khác nhau giữa hai motor, khác nhau giữa hai chiều quay, và thay đổi theo tải và nhiệt độ.

Không bù vùng chết, bộ điều khiển PID của bạn sẽ tích lũy sai số rồi giật cục khi vượt ngưỡng. Đây là nguyên nhân số một của robot "đi giật giật".

### Làm

1. Nâng bánh lên khỏi mặt đất. Quét PWM từ 0% tới 100%, bước 2%, mỗi bước giữ 2 giây và đo vận tốc từ encoder.
2. Lặp cho **chiều ngược lại**. Lặp cho **cả hai motor**. Bốn đường cong.
3. Vẽ cả bốn lên một đồ thị.
4. Đánh dấu: vùng chết ở đâu, vùng tuyến tính ở đâu, bão hòa ở đâu.
5. Lặp lại với **bánh chạm đất, có tải** (đặt vật nặng lên robot). So sánh.
6. Chạy motor liên tục 10 phút rồi đo lại. Đường cong có dịch không?

### Số phải ra

| Kiểm tra | Kỳ vọng |
|---|---|
| Vùng chết | Thường **10–20% PWM**. Khác nhau giữa hai motor |
| Vùng tuyến tính | Phần giữa, tuyến tính khá tốt |
| Hai motor cùng lệnh PWM | **Vận tốc khác nhau vài phần trăm.** Đây là lý do cần PID riêng cho mỗi bánh, không dùng open-loop |
| Có tải vs không tải | Vùng chết rộng ra, độ dốc giảm |
| Sau 10 phút chạy | Đường cong dịch nhẹ — motor nóng, ma sát đổi |

Dòng thứ ba là phát hiện quan trọng nhất của bài. Nếu bạn gửi cùng một PWM cho hai bánh và mong robot đi thẳng, nó sẽ đi cong. Luôn luôn.

---

## Bài 3 — PID vận tốc bánh xe và jitter vòng lặp (14h)

**Câu hỏi:** vòng điều khiển chạy đúng 100 Hz hay chỉ gần đúng?

### Khái niệm

Đây là lần đầu bạn viết một vòng điều khiển thật, và nó nối thẳng vào mọi thứ bạn học về determinism.

**Cấu trúc:**
```
mỗi 10ms:
    đọc encoder → tính vận tốc thực
    sai số = vận tốc mong muốn − vận tốc thực
    PWM = bù_vùng_chết + Kp·e + Ki·∫e + Kd·de/dt
    giới hạn PWM, chống windup
    xuất PWM
```

**Ba chi tiết mà tutorial hay bỏ:**

*Bù vùng chết đứng ngoài PID.* Nếu để PID tự vượt vùng chết, nó phải tích lũy sai số trước — chậm và giật. Cộng thẳng offset vùng chết vào đầu ra.

*Chống windup.* Khi PWM đã bão hòa, thành phần tích phân vẫn cộng dồn và robot sẽ vọt lố nặng khi thoát bão hòa. Kẹp tích phân.

*Tính vận tốc từ encoder cần lọc.* Ở tốc độ thấp, số count mỗi chu kỳ nhỏ nên lượng tử hóa gây nhiễu lớn. Ví dụ ở 10ms và 0.05 m/s với 0.136 mm/count: chỉ 3–4 count mỗi chu kỳ → độ phân giải vận tốc rất thô. Dùng cửa sổ trượt hoặc đo khoảng thời gian giữa các xung thay vì đếm xung trong khoảng thời gian.

**Và phần quan trọng nhất: đo jitter của chính vòng lặp.** Bạn đã làm đúng phép đo này ở Khóa 5 Bài 8 — GPIO + logic analyzer. Giờ đối tượng là chu kỳ vòng điều khiển.

### Làm

1. Implement PID trên ESP32-S3, chạy từ timer phần cứng (không phải `delay()` trong vòng lặp).
2. **Kéo GPIO lên/xuống ở đầu mỗi chu kỳ.** Đo bằng logic analyzer trong 10 phút.
3. Vẽ phân bố chu kỳ thật. Báo cáo p50/p95/p99 và giá trị tệ nhất.
4. Đo **thời gian thực thi** của vòng lặp (GPIO cao trong lúc tính, thấp lúc rảnh) → tỉ lệ sử dụng.
5. Tinh chỉnh PID: đáp ứng bước, đo vọt lố, thời gian xác lập, sai số xác lập.
6. Ép hỏng: thêm tải nặng lên CPU ESP32 (ví dụ gửi log qua WiFi liên tục), đo lại jitter.

### Số phải ra

| Đại lượng | Ngưỡng |
|---|---|
| Chu kỳ vòng lặp p50 | Đúng bằng chu kỳ đặt (10ms cho 100Hz) |
| **Jitter p99** | **<100 µs** với timer phần cứng trên MCU |
| Tỉ lệ sử dụng CPU trong vòng lặp | <50%, để còn dư địa |
| Vọt lố sau tinh chỉnh | <10% |
| Thời gian xác lập | <200 ms |
| Sai số xác lập | ~0 (nhờ thành phần tích phân) |
| Jitter khi có tải WiFi | Tăng — **ghi lại con số.** Đây là lý do tách MCU khỏi Pi |

Dòng jitter p99 là con số bạn sẽ nói trong phỏng vấn. Một ứng viên nói "tôi chạy PID ở 100Hz" là một ứng viên bình thường. Một ứng viên nói "tôi chạy PID ở 100Hz với jitter p99 dưới 80µs đo bằng logic analyzer, và nó tăng lên 4ms khi tôi cố tình cho stack WiFi chạy cùng core" là một ứng viên khác hẳn.

---

## Bài 4 — Odometry và hiệu chuẩn UMBmark (16h)

**Câu hỏi:** robot nghĩ nó đang ở đâu, và nó sai bao nhiêu?

**Đây là bài quan trọng nhất của 7A.**

### Khái niệm

**Động học vi sai (differential drive):**

```
v = (v_phải + v_trái) / 2          vận tốc tiến
ω = (v_phải − v_trái) / B          vận tốc quay,  B = khoảng cách hai bánh
```

Tích phân theo thời gian cho ra vị trí. Đơn giản — và **sai một cách có hệ thống**.

**Hai loại sai số, phải phân biệt:**

| Loại | Nguồn | Sửa được không |
|---|---|---|
| **Hệ thống** | Sai đường kính bánh, sai khoảng cách bánh B, hai bánh không bằng nhau | **Có — bằng hiệu chuẩn** |
| **Phi hệ thống** | Trượt bánh, mặt sàn không đều, va chạm | Không. Phải dùng cảm biến ngoài (7B) |

Sai số hệ thống là loại lớn hơn và nó **sửa được gần hết**, nhưng gần như không ai làm. Con số để hình dung: sai đường kính bánh 1% tạo ra sai lệch 10cm sau 10m. Sai B 2% làm mọi phép quay lệch 2%.

**UMBmark** là phương pháp chuẩn để tách và sửa hai sai số hệ thống chính (Borenstein & Feng). Ý tưởng đẹp: chạy một hình vuông **theo chiều kim đồng hồ**, đo sai lệch cuối; chạy lại **ngược chiều kim đồng hồ**, đo sai lệch cuối. Sai số đường kính bánh và sai số khoảng cách bánh gây ra sai lệch theo hai kiểu khác nhau dưới hai chiều chạy, nên từ hai bộ số bạn **giải ra được từng cái riêng**.

### Làm

**Phần A — đo tay trước.**
1. Đo đường kính hai bánh bằng thước cặp. Chúng **sẽ khác nhau**.
2. Đo B (khoảng cách giữa hai điểm tiếp xúc bánh–sàn). Khó hơn bạn nghĩ — bánh có bề rộng, điểm tiếp xúc không phải một điểm.
3. Ghi vào `prediction.md`: bạn nghĩ robot đi 10m sẽ lệch ngang bao nhiêu?

**Phần B — đường thẳng.**
4. Dán băng dính làm đường thẳng 10m. Cho robot chạy dọc theo, đo **sai lệch ngang** ở cuối và **sai lệch chiều dài** odometry báo so với thực đo.
5. Lặp 10 lần. Báo cáo trung vị và độ lệch chuẩn.

**Phần C — UMBmark.**
6. Chạy hình vuông 2m × 2m, 5 lần theo chiều kim đồng hồ. Đánh dấu điểm dừng thật trên sàn mỗi lần.
7. Lặp 5 lần ngược chiều kim đồng hồ.
8. Vẽ 10 điểm dừng lên một đồ thị. **Hai cụm sẽ tách nhau** — đó là dấu hiệu của sai số hệ thống.
9. Tính hệ số hiệu chỉnh cho đường kính bánh và cho B theo công thức UMBmark.
10. Nạp hệ số vào firmware. **Chạy lại toàn bộ.**

**Phần D — trượt bánh.**
11. Chạy trên 3 mặt sàn khác nhau (gạch, thảm, sàn gỗ). So sai lệch.
12. Cho robot đâm nhẹ vào tường và tiếp tục chạy. Odometry sai bao nhiêu? **Nó không biết mình vừa đâm.**

### Số phải ra

| Kiểm tra | Trước hiệu chuẩn | Sau hiệu chuẩn |
|---|---|---|
| Sai lệch ngang sau 10m | Thường **0.3–1.0 m** | **<0.5 m, mục tiêu <5% quãng đường** |
| Sai lệch chiều dài | Vài phần trăm | <1% |
| Hai cụm UMBmark | Tách rõ | **Xích lại gần nhau** |
| Độ lặp lại (độ lệch chuẩn 10 lần) | Nhỏ hơn sai lệch trung bình | Không đổi nhiều — đó là sai số phi hệ thống |
| Trên thảm | Tệ hơn rõ rệt | Vẫn tệ hơn — hiệu chuẩn không sửa được trượt |
| Sau khi đâm tường | Odometry lệch hẳn, **và không tự biết** | Y hệt |

Ba điểm cuối là lý do tồn tại của 7B. Bạn vừa tự chứng minh bằng số rằng odometry một mình không đủ — đó là cách đúng để bước sang bài toán định vị, chứ không phải vì đọc được ở đâu đó.

### Nếu ra khác

| Triệu chứng | Nguyên nhân |
|---|---|
| Hiệu chuẩn xong vẫn lệch nhiều | Còn sai số phi hệ thống lớn: bánh caster kẹt, sàn nghiêng, bánh bị méo |
| Hai cụm UMBmark trùng nhau ngay từ đầu | Sai số hệ thống đã nhỏ. Hiếm, nhưng tốt. Ghi lại |
| Độ lặp lại rất kém (std lớn) | Trượt bánh nhiều, hoặc PID chưa ổn định. Quay lại Bài 3 |

---

## Bài 5 — Ghi dữ liệu và nối vào hạ tầng Khóa 5 (14h)

**Câu hỏi:** robot chạy xong, dữ liệu đi đâu?

### Làm

Đây là chỗ Khóa 5 vào việc. Không có khái niệm mới, chỉ có tích hợp:

1. **Sidecar trên Pi** ghi MCAP song song với vòng điều khiển. Kiến trúc y hệt mô tả công việc bạn đã viết: subscribe topic, ghi đầy đủ trường, backpressure, buffer local khi mất mạng.
2. Các luồng ghi: encoder counts + vận tốc (100Hz), lệnh PWM (100Hz), IMU (200Hz), pose odometry (50Hz), trạng thái pin, camera (10–30fps).
3. **Timestamp:** ESP32 đóng dấu ở nguồn, Pi đóng dấu lúc nhận, **ghi cả hai** và ghi cả `clock_source`. Đo offset giữa hai clock bằng phương pháp GPIO của Khóa 5 Bài 8.
4. Schema Protobuf có version, đủ trường bắt buộc: `frame_id`, `unit`, `uncertainty`, `calibration_id` (chính là hệ số UMBmark!), `sequence`.
5. Upload resumable lên server khi về tầm WiFi.
6. **Chạy tool audit Khóa 2** lên dữ liệu robot thật. Nó tìm thấy gì?
7. Mở trong Foxglove, dựng layout: pose 2D, vận tốc hai bánh, PWM, IMU.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Sidecar ảnh hưởng jitter vòng điều khiển | **0** — nó chạy trên Pi, vòng điều khiển chạy trên ESP32. Chứng minh bằng đo lại Bài 3 |
| Offset clock ESP32 ↔ Pi | Vài chục ms nếu không sync, và **trôi theo thời gian** |
| Tool Khóa 2 chạy trên dữ liệu robot | **Tìm thấy lỗi thật** — rớt gói WiFi, rớt frame camera, có thể lệch pha |
| Dữ liệu mỗi giờ chạy | Tính trước, đo sau |

Dòng thứ ba là một khoảnh khắc đáng ghi: công cụ bạn viết ở Khóa 2 để audit dataset người khác, giờ tìm ra lỗi trong dữ liệu do chính robot bạn tạo ra. Vòng tròn khép lại.

---

## GATE 7A

```
[ ] 1. Robot đi thẳng 10m, sai lệch ngang <5% quãng đường, đo 10 lần,
       báo cáo trung vị + độ lệch chuẩn

[ ] 2. UMBmark đầy đủ: 5 lần CW + 5 lần CCW trước và sau hiệu chuẩn,
       đồ thị 20 điểm dừng, hệ số hiệu chỉnh tính ra bằng số

[ ] 3. Jitter vòng điều khiển đo bằng logic analyzer, p99 <100µs,
       kèm số liệu khi có tải để so sánh

[ ] 4. Đường cong PWM→vận tốc cho 2 motor × 2 chiều, vùng chết xác định bằng số

[ ] 5. Dữ liệu ghi ra MCAP, upload được, mở được trong Foxglove,
       tool Khóa 2 chạy được và tìm ra ≥1 lỗi thật

[ ] 6. Bài viết: "Calibrating differential drive odometry: UMBmark with numbers"
```

**FAIL action:** chạm 80h chưa PASS → bỏ tiêu chí 5 (ghi dữ liệu), giữ 1–4, publish, sang 7B. Phần ghi dữ liệu gắn lại sau ở 7E.

---

# 7B — ĐỊNH VỊ VÀ ĐIỀU HƯỚNG (80h)

**Mua đợt này:** tùy đường bạn chọn — marker gần như miễn phí, lidar 2D khoảng 1–3tr.

---

## Bài 6 — Chọn đường: marker hay lidar (6h)

**Câu hỏi:** robot biết mình ở đâu bằng cách nào?

### Khái niệm

Bạn đã chứng minh ở 7A rằng odometry trôi và không tự biết mình trôi. Cần một nguồn thông tin **tuyệt đối** để neo lại.

| | Marker (AprilTag/ArUco) | Lidar 2D |
|---|---|---|
| Chi phí | ~0đ (in giấy + camera đã có) | 1–3tr |
| Cần sửa môi trường | **Có** — dán tag lên tường/trần | Không |
| Độ chính xác | Rất tốt khi thấy tag, **vô dụng khi không thấy** | Đều, liên tục |
| Dùng trong công nghiệp | **Có** — AGV dùng phản quang và marker rộng rãi | Có |
| Dạy bạn gì | Camera pose estimation, hiệu chuẩn nội tại | SLAM, scan matching |

**Khuyến nghị: bắt đầu bằng marker.** Ba lý do: rẻ, buộc bạn học hiệu chuẩn camera (kỹ năng nằm trong danh sách khan hiếm), và nó là bài toán định vị **tuyệt đối** sạch sẽ để đo. Thêm lidar sau nếu 7B còn dư giờ.

Và một lý do thứ tư ít ai nói: marker cho bạn **ground truth**. Khi tag đã được đo vị trí chính xác bằng thước, bạn có chân lý để chấm điểm mọi thứ khác — kể cả lidar sau này. Không có ground truth thì không đo được gì, đúng tinh thần cả lộ trình.

### Làm

1. Quyết định, ghi lý do vào `decisions.md`.
2. Nếu marker: in bộ AprilTag, đo và ghi kích thước thật bằng thước cặp (in ra thường sai vài phần trăm so với thiết kế — và sai số đó đi thẳng vào sai số khoảng cách).
3. Khảo sát văn phòng: vẽ sơ đồ, chọn vị trí dán tag, đo vị trí từng tag bằng thước. Đây là bản đồ ground truth của bạn.

---

## Bài 7 — Hiệu chuẩn camera và độ chính xác pose từ marker (16h)

**Câu hỏi:** tag ở cách 2m, camera nói nó cách bao nhiêu, và sai bao nhiêu?

### Khái niệm

Ước lượng pose từ marker cần **hiệu chuẩn nội tại** camera: tiêu cự, tâm ảnh, hệ số méo ống kính. Đây chính là từ "intrinsic calibration" bạn đã đọc ở tài liệu nền Phần 3.2 — giờ bạn làm thật.

Sai hiệu chuẩn → sai khoảng cách theo tỉ lệ. Và nó **sai một cách có hệ thống**, tức là không thể lọc bằng cách lấy trung bình nhiều mẫu.

### Làm

1. Hiệu chuẩn camera bằng bàn cờ (OpenCV). ≥20 ảnh ở nhiều góc và khoảng cách.
2. Ghi lại **reprojection error** — đây là chỉ số chất lượng hiệu chuẩn.
3. Lưu kết quả hiệu chuẩn thành artifact có `calibration_id` và version. Mọi phép đo sau đều tham chiếu nó.
4. **Đo độ chính xác pose:** đặt tag ở khoảng cách đo bằng thước (0.5, 1, 2, 3, 4m) × góc (0°, 20°, 40°, 60°). Với mỗi cấu hình, ghi 100 mẫu.
5. Lập bảng: sai số vị trí và sai số góc theo khoảng cách và góc nhìn.
6. **Ép hỏng:** ánh sáng yếu, tag bị che một phần, robot đang chuyển động (nhòe).

### Số phải ra

| Kiểm tra | Kỳ vọng |
|---|---|
| Reprojection error sau hiệu chuẩn | **<0.5 pixel.** Nếu >1 pixel, hiệu chuẩn lại |
| Sai số vị trí ở 1m, chính diện | Cỡ **1–2 cm** |
| Sai số ở 4m | Tệ hơn đáng kể — sai số thường tăng theo bình phương khoảng cách |
| Sai số góc yaw | Xấu hơn sai số vị trí. **Ước lượng góc từ tag phẳng vốn kém** |
| Góc nhìn 60° | Tệ hơn nhiều so với chính diện |
| Khi robot chuyển động | Nhòe → mất phát hiện hoặc sai số vọt |

Dòng "sai số góc xấu hơn sai số vị trí" là một đặc tính quan trọng và hay bị bỏ qua. Nó có nghĩa là bạn nên tin khoảng cách từ tag hơn là tin hướng từ tag — và điều đó phải thể hiện trong **ma trận hiệp phương sai** bạn đưa vào bộ lọc ở Bài 8. Đây chính là lúc trường `uncertainty` trong schema có ý nghĩa vận hành, không chỉ là một trường đẹp.

---

## Bài 8 — Hợp nhất odometry và marker (20h)

**Câu hỏi:** hai nguồn, một cái trôi liên tục, một cái chính xác nhưng gián đoạn — kết hợp thế nào?

### Khái niệm

Đây là sensor fusion thật đầu tiên của bạn, và bạn **dùng thư viện**, không tự viết EKF. Nhắc lại từ tài liệu nền: biết nó làm gì và cần đầu vào gì (hiệp phương sai, timestamp đồng bộ) là đủ ở mức 🟡.

Nhưng có ba thứ bạn **phải** tự làm đúng, và chúng đều là thứ bạn đã học:

| Việc | Từ đâu |
|---|---|
| Timestamp đồng bộ giữa odometry và camera | Khóa 5 Module 2 |
| Ma trận hiệp phương sai đúng cho từng nguồn | Bài 7 vừa đo được |
| Cây TF đúng: `map → odom → base_link → camera` | Khóa 3 Bài L3 |

Cây TF là chỗ dễ sai nhất. Quy ước ROS: `odom → base_link` là biến đổi liên tục nhưng trôi; `map → odom` là hiệu chỉnh nhảy bậc do định vị tuyệt đối. Hiểu sai chỗ này là nguồn của cả một lớp bug khó chịu.

### Làm

1. Dựng ROS 2 trên Pi, publish odometry từ ESP32 lên topic.
2. Node phát hiện tag, publish pose với **hiệp phương sai lấy từ bảng Bài 7**, không phải số bịa.
3. Dùng `robot_localization` (EKF) để hợp nhất.
4. **Đo:** chạy 20 phút quanh văn phòng, so pose ước lượng với ground truth (dừng ở các điểm đã đo trước).
5. So ba đường: odometry thuần, marker thuần, và fusion.
6. **Ép hỏng:** che hết tag trong 2 phút. Pose trôi bao nhiêu? Khi tag xuất hiện lại, nó nhảy bao xa?

### Số phải ra

| Cấu hình | Sai số sau 20 phút |
|---|---|
| Odometry thuần | **Trôi liên tục**, hàng mét |
| Marker thuần | Chính xác khi thấy tag, **không có gì khi không thấy** |
| Fusion | Giữ trong vài chục cm |
| Sau 2 phút mất tag | Trôi theo tốc độ odometry, rồi **nhảy về** khi thấy tag lại |

Cú nhảy khi tag xuất hiện lại là hành vi **đúng**, không phải bug — đó chính là `map → odom` được hiệu chỉnh. Nhưng nó gây khó cho bộ điều khiển chuyển động, và cách xử lý (làm mượt cú nhảy) là một quyết định thiết kế phải ghi vào `decisions.md`.

---

## Bài 9 — Nav2: từ A tới B (24h)

**Câu hỏi:** robot tự đi từ bàn của tôi tới bàn của đồng nghiệp, 20 lần liên tiếp, được không?

### Khái niệm

Nav2 là stack lớn. **Đừng học hết.** Bốn thành phần bạn cần hiểu:

| Thành phần | Làm gì | Tham số đáng vặn |
|---|---|---|
| **Costmap** | Bản đồ chi phí, đánh dấu chướng ngại và vùng đệm | `inflation_radius`, `obstacle_range` |
| **Planner** | Đường đi toàn cục từ A tới B | Thuật toán, `tolerance` |
| **Controller** | Bám đường, sinh lệnh vận tốc | `max_vel`, `lookahead`, các trọng số |
| **Recovery** | Làm gì khi kẹt | Thứ tự hành vi, số lần thử |

Và một thứ bạn phải tự thêm vì Nav2 không lo: **giới hạn tốc độ vì an toàn**. Chi tiết ở 7D, nhưng đặt nó ngay từ bây giờ: **≤0.5 m/s trong văn phòng**.

### Làm

1. Dựng bản đồ văn phòng. Với đường marker: bản đồ có thể vẽ tay từ số đo, không cần SLAM.
2. Cấu hình Nav2. Bắt đầu bằng config mặc định, đổi **từng tham số một** và ghi lại ảnh hưởng.
3. **Thí nghiệm độ lặp lại:** cùng điểm A, cùng điểm B, 20 lần liên tiếp. Đo pose cuối thật bằng thước.
4. Vẽ phân bố 20 điểm dừng. Báo cáo trung vị và p95 của sai lệch.
5. Đo thời gian mỗi lần, phân bố.
6. **Ép hỏng, bốn kịch bản:** đặt hộp chắn giữa đường; có người đi ngang; đặt robot sai vị trí ban đầu (kidnapped robot); đặt đích vào chỗ không tới được.
7. Ghi lại hành vi phục hồi cho từng kịch bản.

### Số phải ra

| Kiểm tra | Ngưỡng |
|---|---|
| Tỉ lệ tới đích thành công, 20 lần | **≥19/20** |
| Sai lệch vị trí cuối, p95 | Trong dung sai đã đặt (thường 0.25m) |
| Thời gian, độ biến thiên | Ghi lại. Biến thiên lớn = đang phải phục hồi nhiều |
| Chắn đường | Lập lại đường đi hoặc phục hồi, **không đâm** |
| Kidnapped robot | Phát hiện được khi thấy tag, hoặc thất bại **một cách rõ ràng** — không được im lặng đi lung tung |
| Đích không tới được | Từ bỏ sau N lần, báo lỗi. **Không lặp vô hạn** |

Kịch bản kidnapped là kịch bản đáng giá nhất. Một hệ thống thất bại rõ ràng tốt hơn nhiều so với một hệ thống thất bại im lặng — nguyên tắc này bạn đã gặp ở Khóa 2 (dữ liệu hỏng mà không ai biết) và nó lặp lại y hệt ở tầng vật lý.

---

## Bài 10 — Ghi và phân tích session điều hướng (14h)

### Làm

1. Mở rộng sidecar MCAP: thêm pose ước lượng, pose ground truth khi có tag, costmap (giảm tần số), đường đi toàn cục, lệnh vận tốc, sự kiện phục hồi.
2. Layout Foxglove: bản đồ 2D + vị trí robot + đường đi + timeline sự kiện.
3. **Thêm rule validation vật lý** vào tool Khóa 5 cho miền robot:
   - Vận tốc không vượt giới hạn an toàn
   - Vị trí không nhảy quá `v_max × dt` (trừ khi có hiệu chỉnh định vị, và lúc đó phải có cờ)
   - Tổng quãng đường odometry ≈ quãng đường theo pose fusion, trong ngưỡng
   - Pin giảm đơn điệu
4. Chạy trên 20 session của Bài 9. Rule nào bắn?

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| ≥4 rule vật lý cho miền robot | Có, mỗi cái có test tổng hợp |
| Chạy trên 20 session thật | **Bắt được ≥1 bất thường thật** |
| Dashboard | Trả lời được "lần chạy thứ 13 vì sao lâu hơn" chỉ bằng cách nhìn |

---

## GATE 7B

```
[ ] 1. Hiệu chuẩn camera có reprojection error <0.5px, lưu thành artifact có version

[ ] 2. Bảng độ chính xác pose từ marker: ≥5 khoảng cách × ≥3 góc, ≥100 mẫu mỗi ô

[ ] 3. So sánh ba đường (odom / marker / fusion) trên 20 phút chạy thật, có ground truth

[ ] 4. A→B 20 lần liên tiếp, ≥19 thành công, phân bố pose cuối có p95

[ ] 5. 4 kịch bản ép hỏng, mỗi cái có hành vi xác định và được ghi log

[ ] 6. ≥4 rule validation vật lý, bắt được ≥1 bất thường thật trong 20 session

[ ] 7. Bài viết: "Measuring navigation repeatability on a $200 robot"
```

**FAIL action:** chạm 110h chưa PASS → bỏ tiêu chí 5 và 6, giữ 1–4, publish, sang 7C.

---

# 7C — NHẬN NGƯỜI ON-DEVICE, PRIVACY-FIRST (60h)

**Mua đợt này:** có thể 0đ nếu Pi 5 đủ. Nếu cần tăng tốc: Coral USB hoặc Hailo-8L, ~1.5–3tr — **và chỉ mua sau khi Bài 12 chứng minh là cần**, đúng kỷ luật của Khóa 4.

---

## Bài 11 — Thiết kế quyền riêng tư trước khi viết dòng code nào (10h)

**Câu hỏi:** hệ thống này có được phép tồn tại không?

### Khái niệm

Đọc kỹ phần này. Nó không phải thủ tục, nó là thiết kế — và nó là phần khiến hồ sơ của bạn khác hẳn một dự án hobby.

Nghị định 13/2023 xếp **dữ liệu sinh trắc học vào nhóm dữ liệu cá nhân nhạy cảm**. Một robot **di động** quét mặt mọi người trong văn phòng có bề mặt rủi ro lớn hơn nhiều so với một thiết bị cố định — nó đi vào nhiều không gian, gặp người không biết nó tồn tại, và ghi hình liên tục.

**Bảy ràng buộc thiết kế, không thương lượng:**

| # | Ràng buộc | Vì sao |
|---|---|---|
| 1 | **Chỉ nhận diện người đã đăng ký opt-in**, có đồng ý bằng văn bản | Cơ sở pháp lý |
| 2 | Người chưa đăng ký chỉ được phát hiện là **"một người"**, không phải "ai" | Giảm thu thập tới mức tối thiểu |
| 3 | **Chỉ lưu embedding, không lưu ảnh thô** sau khi đăng ký xong | Embedding khó đảo ngược hơn ảnh |
| 4 | Embedding lưu **local trên thiết bị, mã hóa**, không lên cloud | Giảm bề mặt rò rỉ |
| 5 | Nút **"xóa dữ liệu của tôi"** hoạt động thật, có test tự động | Quyền của chủ thể dữ liệu |
| 6 | **Log mọi sự kiện nhận diện**, và log việc ai xem log | Truy vết |
| 7 | Có **dấu hiệu vật lý** trên robot khi camera đang hoạt động | Người xung quanh có quyền biết |

Ràng buộc 2 là ràng buộc thông minh nhất và ít ai nghĩ ra: pipeline chạy detect → embed → so với gallery, và **nếu không khớp ai trong gallery thì embedding bị hủy ngay, không lưu, không log nội dung**. Robot biết "có người ở đây" nhưng không biết và không thể biết đó là ai.

Viết được đoạn **"privacy-by-design under Vietnamese Decree 13/2023"** trong README, kèm bảy ràng buộc này và test chứng minh từng cái, là thứ gần như không hồ sơ hobby nào có. Nó nói với nhà tuyển dụng rằng bạn hiểu ràng buộc **vận hành**, không chỉ ràng buộc kỹ thuật — và đó là khác biệt giữa một kỹ sư và một người biết code.

### Làm

1. Viết `PRIVACY.md` với bảy ràng buộc, mỗi cái kèm: cơ chế kỹ thuật thực thi nó, và test chứng minh.
2. Soạn mẫu đồng ý bằng tiếng Việt: thu gì, để làm gì, lưu ở đâu, bao lâu, cách rút lại.
3. Thiết kế luồng đăng ký: ai chạy, ở đâu, xác nhận thế nào.
4. Thiết kế sơ đồ dữ liệu: cái gì lưu ở đâu, mã hóa bằng gì, xóa thế nào.
5. **Xin phép quản lý lần hai** — B2 ở Khóa 3 là cho loa cố định. Robot di động có camera là phạm vi khác. Bằng văn bản.

### Số phải ra

Không có số. Có `PRIVACY.md`, mẫu đồng ý, và câu trả lời bằng văn bản. **Không được bước sang Bài 12 nếu thiếu bất kỳ cái nào.**

---

## Bài 12 — Pipeline nhận diện và đo FAR/FRR (24h)

**Câu hỏi:** ngưỡng nhận diện đặt ở đâu, và tại sao?

### Khái niệm

Pipeline bốn bước: **detect → align → embed → match**. Bạn dùng model có sẵn cho ba bước đầu; giá trị của bạn nằm ở bước bốn và ở việc **đo**.

Match là so sánh embedding với gallery bằng độ tương tự cosine, và lấy ngưỡng. Chọn ngưỡng là một bài toán đánh đổi — **đúng loại đường cong bạn đã vẽ ba lần** rồi:

| Ngưỡng | FAR (nhận nhầm người khác) | FRR (không nhận ra người đúng) |
|---|---|---|
| Cao (chặt) | Thấp | Cao |
| Thấp (lỏng) | Cao | Thấp |

**Với ứng dụng này, FAR nguy hiểm hơn FRR rất nhiều.** Nhận nhầm nghĩa là robot đọc confession của người A cho người B nghe. Không nhận ra chỉ nghĩa là phải đứng lại một lát. Đánh đổi này phải được ghi vào `decisions.md` bằng lời rõ ràng, và ngưỡng chọn theo nó.

**Và một hiệu ứng quan trọng:** FAR **tăng theo kích thước gallery**. Với gallery N người, xác suất ít nhất một người khác vượt ngưỡng lớn hơn nhiều so với so sánh một–một. Đo FAR trên gallery 5 người rồi triển khai cho 30 người là một sai lầm định lượng nghiêm trọng.

### Làm

**Phần A — dựng gallery.**
1. Đăng ký ≥10 người tình nguyện, có đồng ý bằng văn bản. Mỗi người ≥10 ảnh ở nhiều góc và điều kiện sáng.
2. **Giữ lại tập kiểm tra riêng** — ảnh không dùng để đăng ký. Đây là kỷ luật cơ bản mà dự án hobby hay bỏ.
3. Xóa ảnh thô sau khi tạo embedding. Giữ đúng embedding.

**Phần B — đo ROC.**
4. Với mỗi ngưỡng từ 0 tới 1, bước 0.01: tính FAR và FRR trên tập kiểm tra.
5. Vẽ ROC. Đánh dấu điểm vận hành đã chọn.
6. **Áp dụng Khóa 6 Bài 12:** với n cặp kiểm tra, khoảng tin cậy của FAR là bao nhiêu? Nếu FAR đo được là 0/500 cặp, bạn **không** kết luận được FAR = 0 — bạn kết luận được FAR < ~0.6% ở mức tin cậy 95%. Viết đúng như vậy.
7. Lặp với gallery 5, 10, 20 người. Vẽ FAR theo kích thước gallery.

**Phần C — điều kiện thật.**
8. Đo lại trong bốn điều kiện: robot đứng yên vs đang chạy; sáng tốt vs sáng yếu; chính diện vs góc 45°; đeo kính/khẩu trang vs không.
9. Lập bảng FRR theo điều kiện.

**Phần D — hiệu năng.**
10. Dùng **harness benchmark của Khóa 4**, đổi payload. Đo p50/p95/p99 của từng bước pipeline, RAM peak, nhiệt độ.
11. Thử quantization như Khóa 4 Bài 8: đo **cả hai trục** — latency và FAR/FRR. Tìm cấu hình "nhanh hơn nhưng hỏng".

### Số phải ra

| Kiểm tra | Kỳ vọng |
|---|---|
| FRR ở điểm vận hành, điều kiện tốt | Vài phần trăm |
| FAR ở điểm vận hành | **Rất thấp — và báo cáo kèm khoảng tin cậy, không báo cáo 0** |
| FAR theo kích thước gallery | **Tăng.** Ngoại suy ra gallery 30 người |
| FRR khi robot đang chạy | **Tệ hơn rõ rệt** do nhòe chuyển động |
| FRR trong sáng yếu | Tệ hơn |
| Latency toàn pipeline trên Pi 5 | Thang **hàng chục tới hàng trăm ms**, tùy model |
| Quantization | Nhanh hơn; **có mức làm FAR xấu đi** — tìm ra và ghi lại |

Kết quả "FRR khi đang chạy tệ hơn nhiều" dẫn thẳng tới một quyết định thiết kế: **robot dừng lại rồi mới nhận diện.** Đó là một quyết định sản phẩm được ra bởi một phép đo, và đó chính xác là loại câu chuyện bạn muốn kể trong phỏng vấn.

---

## Bài 13 — Đăng ký, xóa dữ liệu, và audit log (12h)

### Làm

1. Luồng đăng ký: giao diện web đơn giản, chụp ảnh, tạo embedding, xác nhận đồng ý, **xóa ảnh thô**.
2. Lưu embedding mã hóa trên thiết bị.
3. **Nút xóa dữ liệu**, và test tự động chứng minh: sau khi xóa, người đó không còn được nhận diện, và không còn dấu vết trong bất kỳ kho nào — gồm cả backup và MCAP đã ghi.
4. Audit log: mỗi lần nhận diện ghi ai, lúc nào, độ tin cậy bao nhiêu. Log này cũng là dữ liệu nhạy cảm — có retention riêng.
5. Đèn LED sáng khi camera hoạt động, nối phần cứng chứ không phải do phần mềm điều khiển.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Test xóa dữ liệu đầu-cuối | **PASS.** Grep toàn bộ hệ thống không còn dấu vết |
| Ảnh thô sau đăng ký | Không tồn tại. Chứng minh bằng test |
| Người chưa đăng ký | Được phát hiện là "một người", **không có embedding nào được lưu** |
| LED camera | Sáng khi và chỉ khi camera cấp điện |

---

## Bài 14 — Tích hợp nhận diện vào điều hướng (14h)

### Làm

1. Robot đi tới vùng có người → dừng → nhận diện → hành động.
2. Xử lý: nhiều người trong khung hình; người quay lưng; người đi ngang qua.
3. Timeout: không nhận ra ai sau N giây thì đi tiếp, không đứng mãi.
4. Ghi toàn bộ vào MCAP: sự kiện nhận diện, độ tin cậy, quyết định. **Không ghi ảnh.**
5. Đo đầu-cuối: từ lúc thấy người tới lúc ra quyết định, p50/p95/p99.

### Số phải ra

| Kiểm tra | Ngưỡng |
|---|---|
| Thời gian từ thấy người tới quyết định, p95 | <3 giây |
| Nhiều người trong khung | Hành vi xác định, được ghi rõ trong tài liệu |
| Không nhận ra ai | Đi tiếp sau timeout, **không kẹt** |

---

## GATE 7C

```
[ ] 1. PRIVACY.md với 7 ràng buộc, mỗi ràng buộc có cơ chế và test chứng minh

[ ] 2. Đồng ý bằng văn bản của ≥10 người, và văn bản cho phép của quản lý

[ ] 3. Đường ROC đo trên tập kiểm tra riêng, điểm vận hành chọn có lý do ghi rõ,
       FAR báo cáo KÈM KHOẢNG TIN CẬY (không báo cáo 0)

[ ] 4. FAR theo kích thước gallery (5/10/20), có ngoại suy

[ ] 5. Bảng FRR theo ≥4 điều kiện thật, gồm robot đang chuyển động

[ ] 6. Latency p50/p95/p99 trên thiết bị, ≥2 mức precision, đo cả hai trục

[ ] 7. Test xóa dữ liệu đầu-cuối PASS

[ ] 8. Bài viết: "Privacy-by-design face recognition on a mobile robot: FAR, FRR, and the law"
```

**FAIL action:** nếu không xin được phép, hoặc không đủ người tình nguyện → **bỏ hoàn toàn nhận diện mặt**, thay bằng nhận diện bằng thẻ NFC hoặc mã QR mỗi người tự cầm. Robot vẫn hoạt động đầy đủ, portfolio mất một bài viết nhưng không mất khóa con. Ghi rõ lý do đổi trong README — và thành thật mà nói, **quyết định không thu thập sinh trắc học vì không có cơ sở pháp lý vững cũng là một câu chuyện phỏng vấn tốt.**

---

# 7D — TÍCH HỢP, AN TOÀN, STATE MACHINE (60h)

**Mua đợt này:** công tắc E-stop, relay công suất, công tắc va chạm, cảm biến vực. ~1tr.

---

## Bài 15 — An toàn là một tầng phần cứng (16h)

**Câu hỏi:** khi phần mềm treo, cái gì dừng robot lại?

### Khái niệm

Đây là bài mà một người từ nền phần mềm dễ làm sai nhất, vì bản năng là giải quyết bằng code.

**Nguyên tắc: E-stop phải cắt nguồn động lực bằng phần cứng.** Không phải một cờ, không phải một lời gọi hàm, không phải một message ROS. Một công tắc nối tiếp với đường nguồn motor, hoặc điều khiển một relay. Khi bấm, motor mất điện — kể cả khi Pi treo, kể cả khi ESP32 chết, kể cả khi firmware có bug.

**Bốn tầng an toàn, từ dưới lên:**

| Tầng | Cơ chế | Thời gian phản ứng |
|---|---|---|
| 0 | **E-stop vật lý** — cắt nguồn motor | Tức thì |
| 1 | **Công tắc va chạm** (bumper) — nối cứng vào chân ESP32, ngắt ưu tiên cao nhất | <10 ms |
| 2 | **Watchdog trên ESP32** — Pi không gửi heartbeat trong N ms → dừng motor | ~100 ms |
| 3 | Logic phần mềm trên Pi — costmap, giới hạn tốc độ | ~100 ms |

Mỗi tầng bảo vệ cho tầng trên nó hỏng. Tầng 3 là tầng bạn giỏi nhất và là tầng **ít đáng tin nhất**.

**Giới hạn tốc độ, tính bằng số:** robot 5 kg ở 0.5 m/s có động năng `½ × 5 × 0.5² = 0.625 J`. Nhỏ, nhưng không phải không. Ở 1.5 m/s con số thành 5.6 J — gấp 9 lần, vì động năng tỉ lệ bình phương vận tốc. **Giới hạn 0.5 m/s trong văn phòng**, và đặt giới hạn đó ở ESP32 chứ không chỉ ở Nav2.

Và tính quãng đường dừng: ở 0.5 m/s với thời gian phản ứng 100 ms, robot đi thêm 5 cm trước khi bắt đầu giảm tốc, cộng quãng đường giảm tốc. Đó là lý do bumper phải ở tầng 1, không phải tầng 3.

### Làm

1. Lắp E-stop vật lý cắt nguồn motor. **Test bằng cách rút dây tín hiệu Pi** — E-stop vẫn phải hoạt động.
2. Công tắc va chạm nối vào chân ngắt của ESP32, ưu tiên cao nhất, dừng motor trong ISR.
3. Watchdog: Pi gửi heartbeat 10 Hz. Mất 5 nhịp → ESP32 dừng motor.
4. Giới hạn tốc độ cứng trong firmware ESP32 — không nhận lệnh vượt ngưỡng dù Pi gửi gì.
5. Cảm biến vực (nếu có cầu thang): IR hướng xuống, cũng ở tầng 1.
6. **Đo thời gian phản ứng của từng tầng** bằng logic analyzer: từ lúc kích hoạt tới lúc PWM về 0.
7. Test E-stop **20 lần**, trong đó ≥5 lần đúng lúc robot đang chạy tốc độ cao nhất.

### Số phải ra

| Tầng | Thời gian phản ứng đo được |
|---|---|
| E-stop vật lý | Tức thì (giới hạn bởi relay, thường vài ms) |
| Bumper | **<10 ms** |
| Watchdog | <500 ms |
| Giới hạn tốc độ firmware | Không bao giờ vượt, kể cả khi Pi gửi lệnh sai |

| Kiểm tra | Kết quả đúng |
|---|---|
| E-stop 20 lần | **20/20 dừng.** Không có ngoại lệ |
| Rút dây Pi, bấm E-stop | Vẫn dừng |
| Gửi lệnh vận tốc 2 m/s từ Pi | Firmware kẹp về 0.5 m/s |

---

## Bài 16 — State machine và phân tích chế độ hỏng (18h)

**Câu hỏi:** mỗi thành phần chết thì chuyện gì xảy ra?

### Khái niệm

State machine ở đây rộng hơn Khóa 3 rất nhiều vì có chuyển động.

```
IDLE → CHARGING → READY → NAVIGATING → APPROACHING_PERSON
                                     → IDENTIFYING → SPEAKING → RETURNING
       mọi trạng thái → EMERGENCY_STOP → (cần reset tay) → IDLE
       mọi trạng thái → LOW_BATTERY → RETURNING_TO_CHARGE
```

**Và bảng FMEA** — phân tích chế độ hỏng. Đây là công cụ chuẩn trong kỹ thuật an toàn, và có nó trong repo là một tín hiệu mạnh:

| Thành phần hỏng | Hậu quả nếu không xử lý | Phát hiện bằng | Hành vi thiết kế |
|---|---|---|---|
| Mất WiFi | Không upload được, không điều khiển từ xa | Heartbeat | Chạy tiếp, buffer local, về sạc khi hết nhiệm vụ |
| Pi treo | Robot chạy mù | Watchdog ở ESP32 | Dừng motor trong 500ms |
| ESP32 treo | Mất điều khiển motor | Pi mất dữ liệu encoder | Pi cắt relay nguồn motor |
| Encoder một bên chết | Robot quay vòng | Vận tốc hai bánh lệch bất thường | Dừng, báo lỗi |
| Camera chết | Mất định vị tuyệt đối và nhận diện | Không có frame mới | Dừng khi độ bất định pose vượt ngưỡng |
| Pin yếu | Chết giữa đường | Điện áp | Về trạm sạc ở ngưỡng đã đặt |
| Motor kẹt | Cháy driver | Dòng vượt ngưỡng | Cắt PWM, báo lỗi |
| Mất định vị | Đi lung tung | Hiệp phương sai pose lớn | Dừng, chờ thấy tag |

### Làm

1. Implement state machine, mọi chuyển trạng thái có log kèm timestamp và lý do.
2. Implement mọi cơ chế phát hiện trong bảng FMEA.
3. **Test từng dòng bằng cách gây lỗi thật:** rút dây encoder, ngắt WiFi, `kill -9` tiến trình Pi, chặn bánh xe, che camera, mô phỏng pin yếu.
4. Ghi lại hành vi thực tế cho từng cái. So với cột "hành vi thiết kế".
5. Sửa những chỗ thực tế khác thiết kế.
6. Moderation queue và kill switch từ Khóa 3 — dùng lại nguyên vẹn.

### Số phải ra

| Kiểm tra | Ngưỡng |
|---|---|
| Mỗi dòng FMEA | Test được, hành vi khớp thiết kế |
| Chuyển trạng thái không hợp lệ | Bị chặn, có log |
| Sau mọi lỗi | Robot ở trạng thái **an toàn**, không phải trạng thái không xác định |

---

## Bài 17 — Soak 72 giờ trong văn phòng thật (16h người, 72h treo máy)

### Làm

1. Chạy 72 giờ trong văn phòng, có người qua lại thật.
2. Yêu cầu: 0 sự cố an toàn, 0 lần can thiệp tay cho việc vận hành bình thường (được phép can thiệp cho sạc nếu chưa có trạm tự động).
3. Theo dõi: quãng đường, số lần phục hồi, số lần E-stop bị bấm và bởi ai, pin, nhiệt độ, completeness dữ liệu.
4. **Hỏi đồng nghiệp phản hồi.** Họ thấy nó thế nào? Có ai thấy khó chịu không? Đây là dữ liệu thật và nó thuộc về báo cáo.
5. Ghi toàn bộ ra MCAP, chạy audit, dựng dashboard.

### Số phải ra

| Đại lượng | Ngưỡng |
|---|---|
| Sự cố an toàn | **0** |
| Can thiệp tay | 0 (ngoài sạc) |
| Completeness dữ liệu | ≥99% |
| E-stop bị người khác bấm | Ghi lại **và hỏi vì sao** — đây là dữ liệu về thiết kế tương tác |
| Phản hồi định tính | Thu thập, đưa vào báo cáo |

---

## GATE 7D

```
[ ] 1. E-stop vật lý cắt nguồn động lực, test 20/20, hoạt động cả khi Pi chết

[ ] 2. Bốn tầng an toàn, thời gian phản ứng từng tầng đo bằng logic analyzer

[ ] 3. Giới hạn tốc độ cứng ở firmware, chứng minh bằng cách gửi lệnh vượt ngưỡng

[ ] 4. Bảng FMEA ≥8 dòng, MỖI DÒNG đã test bằng cách gây lỗi thật

[ ] 5. Soak 72h trong văn phòng, 0 sự cố an toàn, 0 can thiệp, completeness ≥99%

[ ] 6. Bài viết: "Failure mode analysis for a small office robot"
```

---

# 7E — FULL TEST FLOW (80h)

**Không mua gì. Đây là khóa con quan trọng nhất, và nó gần như hoàn toàn là phần mềm.**

Đây là chỗ Khóa 5 và Khóa 6 được trả nợ, và là chỗ vòng đời công việc bạn tự viết ra trở thành thứ bạn tự vận hành — với bạn đóng cả sáu vai.

---

## Bài 18 — Dựng mô hình sim khớp với robot thật (20h)

**Câu hỏi:** sim của robot này sai bao nhiêu?

### Khái niệm

Bạn có mọi thứ cần: MJCF/URDF dựng từ **số đo thật** của 7A (đường kính bánh sau hiệu chuẩn UMBmark, khoảng cách bánh, khối lượng, đường cong PWM→vận tốc, vùng chết), và phương pháp đo gap từ Khóa 6 Module 5.

Con lắc ở Khóa 6 là bài tập. Đây là bài thật.

### Làm

1. Dựng model robot trong MuJoCo từ số đo 7A. **Mọi tham số phải truy được về một phép đo**, không có số nào bịa.
2. Implement cùng bộ điều khiển (PID, vùng chết) trong sim.
3. **Ba đường như Khóa 6 Bài 16**, cho bốn hiện tượng:

| Hiện tượng | Tính | Đo thật | Sim |
|---|---|---|---|
| Đi thẳng 5m: thời gian, sai lệch ngang | Từ vận tốc đặt | 7A Bài 4 | Chạy sim |
| Quay tại chỗ 360°: thời gian, sai lệch góc | Từ B và vận tốc | Đo bằng thước đo góc | Chạy sim |
| Quãng đường dừng từ 0.5 m/s | Từ giảm tốc | Đo bằng thước | Chạy sim |
| Đáp ứng bước vận tốc: vọt lố, thời gian xác lập | Từ tham số PID | 7A Bài 3 | Chạy sim |

4. **System identification:** chỉnh ma sát, quán tính, độ trễ actuator trong sim cho tới khi khớp thực đo.
5. **Kiểm tra chéo (phần G của Khóa 6 Bài 16):** sau khi fit ở 0.3 m/s, **dự đoán** hành vi ở 0.5 m/s rồi mới đo. Khớp không?
6. Lập **bảng miền hiệu lực**: sim đúng ở đâu, sai ở đâu, chưa kiểm ở đâu.

### Số phải ra

| Kiểm tra | Ngưỡng sau khi fit |
|---|---|
| Đi thẳng: thời gian | Lệch <5% |
| Quay 360°: thời gian | Lệch <5% |
| Quãng đường dừng | Lệch <15% — **ma sát là chỗ khó khớp nhất** |
| Đáp ứng bước | Hình dạng khớp, vọt lố lệch <20% |
| Ngoại suy sang tốc độ chưa fit | Lệch nhỏ nếu mô hình đúng; **lệch lớn là một phát hiện đáng viết** |
| Trên thảm vs sàn cứng | Sim với một bộ tham số **không khớp được cả hai** — đó là giới hạn, ghi vào bảng hiệu lực |

Dòng cuối rất đáng chú ý. Nó là phiên bản robot của bài học con lắc: một mô hình có miền hiệu lực, và việc của bạn là **đo ranh giới đó** chứ không phải giả vờ nó không tồn tại.

---

## Bài 19 — HIL và CI cho hành vi robot (24h)

**Câu hỏi:** đổi một tham số Nav2, làm sao biết nó tốt hơn?

### Khái niệm

Đây là câu hỏi bạn đặt ra từ đầu cuộc trò chuyện — *"phải có nơi để environment show ra lỗi, metric, đúng và sai"* — và đây là chỗ nó thành hiện thực.

**Ba mức test, mỗi mức nhanh và rẻ hơn mức dưới:**

| Mức | Chạy gì | Tốc độ | Bắt được gì |
|---|---|---|---|
| **Sim thuần** | Toàn bộ trong MuJoCo | 1000 episode/giờ | Lỗi logic điều hướng, regression hành vi |
| **HIL** | Firmware thật trên ESP32 thật, thế giới mô phỏng | Thời gian thực | Lỗi firmware, lỗi timing, lỗi giao tiếp |
| **Thật** | Robot thật, văn phòng thật | Vài lần/giờ | Mọi thứ còn lại |

HIL là mức ít người tự làm và nó rẻ: ESP32 thật chạy PID thật, nhưng thay vì đọc encoder thật thì nó nhận số đếm giả lập từ sim qua UART, và thay vì xuất PWM ra motor thì PWM được sim đọc. Firmware không biết mình đang ở trong ma trận.

Giá trị: bắt được đúng lớp lỗi mà sim thuần bỏ sót (timing firmware, tràn buffer, lỗi số học trên MCU) mà không cần robot chạy.

### Làm

1. Cổng HIL: ESP32 chạy ở chế độ mà nguồn encoder và đích PWM được chuyển hướng qua UART.
2. Bộ kịch bản điều hướng, dùng schema kịch bản của Khóa 6 Bài 5: điểm bắt đầu, điểm đích, vị trí chướng ngại, ma sát sàn, người di động.
3. Sinh 1000 biến thể theo Khóa 6 Bài 6.
4. Tiêu chí thành công định nghĩa bằng toán theo Khóa 6 Bài 11: tới đích trong dung sai, trong giới hạn thời gian, **không va chạm**, không vi phạm giới hạn tốc độ.
5. **CI:** mỗi thay đổi → 1000 episode sim → verdict ba trạng thái (Khóa 6 Bài 13) → nếu PASS thì 20 lần chạy HIL → nếu PASS thì đề xuất chạy thật.
6. Power analysis: với tỉ lệ thành công kỳ vọng của bạn, cần bao nhiêu episode để phát hiện sụt 5 điểm? Đặt N theo đó.

### Số phải ra

| Kiểm tra | Ngưỡng |
|---|---|
| 1000 episode sim | <1 giờ |
| Canary: chỉnh một tham số Nav2 làm xấu đi rõ rệt | **CI bắt được** |
| Canary: thay đổi nhỏ hơn ngưỡng phát hiện | **INCONCLUSIVE**, không phải PASS |
| HIL bắt được lớp lỗi sim bỏ sót | ≥1 ví dụ thật, có ghi lại |

---

## Bài 20 — Sim có dự đoán được thực tế không (16h)

**Câu hỏi:** phán quyết của CI có đúng ngoài đời không?

**Đây là gate cuối cùng và là câu hỏi hay nhất của cả Khóa 7.**

### Khái niệm

Toàn bộ giá trị của hạ tầng đánh giá nằm ở một giả định: **kết quả sim dự đoán được kết quả thật.** Hầu như không ai kiểm giả định đó. Bạn sẽ kiểm.

### Làm

1. Chọn **6 cấu hình** khác nhau đáng kể (tham số Nav2, giới hạn tốc độ, tham số controller).
2. Với mỗi cấu hình: chạy 1000 episode sim → ghi tỉ lệ thành công và khoảng tin cậy.
3. Với mỗi cấu hình: chạy **20 lần thật** trong văn phòng → ghi tỉ lệ thành công và khoảng tin cậy (rộng, vì n=20 — và bạn biết chính xác nó rộng bao nhiêu nhờ Khóa 6 Bài 12).
4. **Vẽ: tỉ lệ thành công sim (trục X) vs thật (trục Y), 6 điểm, có thanh sai số.**
5. Tính tương quan hạng. Câu hỏi quan trọng không phải "sim có đúng giá trị tuyệt đối không" mà là **"sim có xếp hạng đúng thứ tự không"**.
6. Nếu xếp hạng sai ở đâu, điều tra: cấu hình nào, vì sao, có phải vì nó nằm ngoài miền hiệu lực ở Bài 18 không?

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Tỉ lệ tuyệt đối sim vs thật | **Sim thường lạc quan hơn.** Bình thường, ghi lại độ lệch |
| Thứ hạng | **Nên tương quan mạnh.** Đây là điều thực sự quan trọng |
| Cấu hình bị xếp hạng sai | Nếu có, kiểm tra nó có nằm ngoài miền hiệu lực không |
| Tương quan yếu | **Đây vẫn là kết quả, và là kết quả quan trọng** — nó nói sim của bạn chưa dùng được để ra quyết định, và nói rõ điều đó có giá trị hơn giả vờ ngược lại |

Nếu tương quan mạnh, bạn có một câu để nói mà rất ít người nói được: *"Tôi đo được rằng phán quyết CI trong sim của tôi dự đoán đúng thứ hạng kết quả thực tế trên 6 cấu hình, với ngần này khoảng tin cậy."*

Nếu tương quan yếu, bạn có một câu còn hiếm hơn: *"Tôi đo được rằng nó không dự đoán được, và đây là lý do."* Cả hai đều là kết quả. Chỉ có "tôi không đo" là thất bại.

---

## Bài 21 — Vòng đời dữ liệu đầy đủ và fine-tune (20h)

**Câu hỏi:** vòng đời sáu bước bạn viết — chạy được từ đầu tới cuối chưa?

### Khái niệm

Đây là chỗ bạn tự đóng cả sáu vai trong vòng đời mình đã mô tả. Đó không phải trùng lặp — nó là điều khiến bạn hiểu vì sao mỗi vai cần gì từ vai trước.

**Về "train on edge" — một điều chỉnh kỳ vọng thành thật:** huấn luyện thật sự trên thiết bị biên gần như không khả thi với phần cứng này; bạn đã tự chứng minh ở Khóa 4 Bài 11 rằng ngay cả *inference* trên SBC đã là thang giây. Luồng thực tế và cũng là luồng công nghiệp: **thu dữ liệu trên biên → huấn luyện trên GPU thuê → nén → triển khai xuống biên**. Đó không phải thỏa hiệp, đó là kiến trúc đúng. Ghi nó vào `decisions.md` kèm số đo đỡ lưng.

### Làm

Chạy đủ vòng đời sáu bước của bạn, có bấm giờ từng bước:

1. **Chuẩn bị:** khai báo metadata thí nghiệm, deploy config lên robot qua OTA
2. **Chạy:** robot thực hiện nhiệm vụ, sidecar ghi MCAP không ảnh hưởng vòng điều khiển
3. **Upload:** đóng file, checksum, resumable upload
4. **Backend:** audit tự động, gắn metadata, index, đánh dấu usable, sinh link Foxglove
5. **Xem lại:** mở Foxglove, so với cảm nhận lúc chạy
6. **Dataset:** chọn session đạt chất lượng, chuyển sang định dạng training, audit lần cuối, version

Rồi **fine-tune một thứ có thật**. Ứng viên tốt theo thứ tự khả thi:
- Model nhận diện người, fine-tune trên dữ liệu văn phòng thật (ánh sáng, góc, nhòe chuyển động) → đo lại FRR theo bảng Bài 12
- Bộ dự đoán quãng đường dừng học từ dữ liệu thật thay vì hằng số
- Bộ phân loại "vùng này hay kẹt" từ lịch sử phục hồi

Với bất kỳ cái nào: **đo trước/sau bằng đúng kỷ luật thống kê của Khóa 6 Bài 12.** Cải thiện phải vượt khoảng tin cậy, nếu không thì báo cáo INCONCLUSIVE.

Rồi **triển khai lại** và đóng vòng: model mới → sim CI → HIL → thật → dữ liệu mới.

### Số phải ra

| Kiểm tra | Ngưỡng |
|---|---|
| Toàn vòng đời từ kết thúc thí nghiệm tới link Foxglove | <10 phút, tự động |
| Sidecar ảnh hưởng jitter vòng điều khiển | 0, đo lại và chứng minh |
| Fine-tune: cải thiện | **Vượt khoảng tin cậy**, hoặc báo cáo INCONCLUSIVE trung thực |
| Vòng khép kín | Chạy được ít nhất **một vòng đầy đủ** |

---

## GATE 7E — VÀ GATE KHÓA 7

```
[ ] 1. Model sim dựng từ số đo thật, MỌI tham số truy được về một phép đo

[ ] 2. Bảng sim-to-real ≥4 hiện tượng, ba đường mỗi hiện tượng,
       kèm bảng miền hiệu lực có cột "chưa kiểm"

[ ] 3. Cổng HIL chạy được, bắt được ≥1 lớp lỗi mà sim thuần bỏ sót

[ ] 4. CI: 1000 episode <1 giờ, verdict ba trạng thái,
       canary regression bị bắt, canary dưới ngưỡng cho INCONCLUSIVE

[ ] 5. ★ TƯƠNG QUAN SIM–THẬT: 6 cấu hình × (1000 sim + 20 thật),
       đồ thị có thanh sai số, tương quan hạng báo cáo bằng số

[ ] 6. Vòng đời dữ liệu đầy đủ chạy đầu-cuối <10 phút tự động

[ ] 7. Một vòng fine-tune khép kín, cải thiện đo bằng kỷ luật thống kê

[ ] 8. Bài viết chính: "Does your sim predict reality? Closing the loop on a $300 office robot"
```

**Tiêu chí 5 là tiêu chí ★.** Nếu chỉ làm được một thứ trong 7E, làm nó.

**FAIL action:** chạm 450h tổng → dừng ở khóa con đang làm, publish nguyên trạng, viết một bài tổng kết nói rõ cái gì xong cái gì chưa. Bốn khóa con đã publish vẫn là bốn artifact.

---

# NGÂN SÁCH

| Đợt | Khi nào | Mua gì | Tiền |
|---|---|---|---|
| 7A | Bắt đầu | Khung, 2 motor+encoder, driver, pin+BMS+sạc, bánh | 2–3tr |
| 7A | Cùng lúc | Pi 5 8GB + nguồn + thẻ + tản nhiệt | 3–3.5tr |
| 7B | Sau gate 7A | Marker (~0đ) hoặc lidar LD19 | 0–1.5tr |
| 7C | **Chỉ sau Bài 12** | Coral/Hailo nếu Pi 5 không đủ | 0–3tr |
| 7D | Sau gate 7C | E-stop, relay, bumper, cảm biến vực | ~1tr |
| — | Rải rác | Dây, đầu nối, in 3D/cắt laser, dự phòng | 1–2tr |
| **Tổng** | | | **7–14tr** |

**Kỷ luật mua:** mỗi đợt chỉ mở sau khi gate trước PASS. Đợt 7C chỉ mở nếu phép đo chứng minh là cần — đúng nguyên tắc "Jetson chỉ mua nếu M6 chứng minh được là cần" của lộ trình gốc.

---

# LỊCH 60 TUẦN

| Tuần | Khóa con | Mốc |
|---|---|---|
| 1–10 | **7A** | Robot đi thẳng được, có số |
| 11–24 | **7B** | Tự đi A→B, 20 lần |
| 25–34 | **7C** | Nhận người, có ROC, có PRIVACY.md |
| 35–44 | **7D** | An toàn, FMEA, soak 72h |
| 45–58 | **7E** | Vòng CI khép kín |
| 59–60 | — | Bài tổng kết, video demo |

**Chạy song song:** 7A (tuần 1–10) chạy cùng M5 (apply). Chúng không tranh nhau — một cái dùng tay, một cái dùng đầu.

**Điểm thoát an toàn:** sau mỗi gate. Nếu có việc làm ở tuần 20, bạn dừng ở 7B với hai artifact và không mất gì.

---

# BA ĐIỀU MANG ĐI

**1. Con robot không phải sản phẩm. Vòng lặp mới là.** Bất kỳ ai đủ kiên nhẫn cũng lắp được một robot chạy. Rất ít người xây được hệ thống nơi một thay đổi đi qua sim CI, qua HIL, ra thực tế, và quay về thành dữ liệu — **với số đo chứng minh phán quyết sim dự đoán đúng thực tế.** Đó là 7E, và nó là lý do Khóa 7 đáng làm.

**2. Mỗi khóa con là một artifact độc lập.** Thiết kế này có chủ đích vì dự án 13 tháng sẽ bị gián đoạn — bởi công việc, bởi cuộc sống, bởi một offer. Khi bị gián đoạn, bạn phải còn thứ để chỉ vào.

**3. Câu chuyện phỏng vấn bạn muốn không phải "tôi làm được con robot".** Nó là: *"Tôi hiệu chuẩn odometry bằng UMBmark và giảm sai lệch từ ngần này xuống ngần này. Tôi đo jitter vòng điều khiển ở p99 và biết vì sao phải tách MCU khỏi Linux. Tôi đo FAR kèm khoảng tin cậy thay vì báo cáo số không. Tôi đo được sim của tôi dự đoán đúng thứ hạng thực tế trên sáu cấu hình. Và đây là chỗ nó **không** đúng, cùng lý do."*

Không ai cần bạn kể rằng nó chạy được. Họ cần biết bạn **đo được** nó chạy tốt đến đâu, và biết chỗ nó chưa tốt.
