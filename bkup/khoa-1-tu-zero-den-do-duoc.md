# KHÓA 1 — TỪ ZERO ĐẾN ĐO ĐƯỢC

**Cho:** người viết phần mềm 8 năm, chưa từng cầm que đo, chưa biết điện trở là gì.
**Thời lượng:** ~35h. Bốn tuần ở nhịp 8–10h/tuần.
**Chi phí:** đợt 1, ~1.8–2.8tr.
**Xong khóa này bạn làm được:** cắm que đo vào một mạch và biết số đó đúng hay sai; nhìn thấy dữ liệu chạy trên dây bằng logic analyzer; đọc được một datasheet; và quan trọng nhất — biết khi nào mình đang tự lừa mình.

---

## BẢN ĐỒ 6 KHÓA

Toàn bộ lộ trình 24 tháng chia thành sáu khóa. Mỗi khóa là một milestone trong kế hoạch.

| Khóa | Tên | Giờ | Cần phần cứng? | Ra artifact gì |
|---|---|---|---|---|
| **1** | **Từ zero đến đo được** | 35 | Đợt 1 (~2.5tr) | Lab notebook 4 thí nghiệm |
| **2** | Dữ liệu robot mà không cần robot | 80 | **Không** | ★ Dataset audit tool + bài viết |
| **3** | Chuỗi audio: từ số nguyên đến áp suất không khí | 90 | Đợt 2 (~4tr) | V1 chạy được + 5 thí nghiệm |
| **4** | Đo hiệu năng inference trên edge | 70 | Thuê GPU | ★ VLA benchmark + bài viết |
| **5** | Cảm biến, đồng bộ thời gian, data platform | 150 | Đợt 3 (~2.5tr) | ★ Sensor platform + bài viết |
| **6** | Robot learning với SO-101 | 120 | Đợt 4 (~10tr) | Dataset + policy trên HF Hub |

**Khóa 1 và Khóa 2 chạy song song.** Khóa 2 không cần phần cứng gì cả và đúng thế mạnh hiện tại của bạn — làm nó vào những tuần bận, khi không có sức ngồi bàn hàn. Khóa 1 làm vào tuần rảnh.

**Thứ tự đúng:** 1+2 song song → 3 → 4 → 5 → 6.

Tài liệu này là **Khóa 1**.

---

## CÁCH DÙNG TÀI LIỆU NÀY

Mỗi bài có sáu phần cố định:

1. **Câu hỏi** — bài này trả lời cái gì
2. **Khái niệm** — giải thích từ số không, kèm phép so sánh với thứ bạn đã biết
3. **Làm** — từng bước, không bỏ bước
4. **Số phải ra** — con số đúng và sai số cho phép ← *phần quan trọng nhất*
5. **Nếu ra khác** — bảng triệu chứng → nguyên nhân → cách sửa
6. **Tự kiểm tra** — 2–3 câu, có đáp án

Phần 4 và 5 tồn tại vì lý do bạn nêu: newbie không biết thế nào là đúng. Từ giờ bạn sẽ biết, vì mỗi bài đều nói trước số phải ra.

**Quy tắc bất di bất dịch của cả khóa:** viết dự đoán bằng số vào file trước, commit, rồi mới cắm que đo. Không phải nghi thức. Đó là toàn bộ nội dung bạn đang mua.

---

## BA CÂU HỎI ĐỂ TỰ BIẾT MÌNH ĐO ĐÚNG

Newbie không có trực giác về "số này hợp lý không". Ba câu hỏi này thay thế trực giác cho tới khi bạn có nó:

1. **Số này có nằm trong khoảng vật lý hợp lý không?** Rail 5V không thể đo ra 12V. Điện trở không thể âm. Dòng qua LED không thể là 3A.
2. **Đo bằng cách khác có ra cùng số không?** Đo điện áp trên điện trở, rồi tính dòng bằng `I = V/R`. So với đo dòng trực tiếp. Hai đường phải gặp nhau.
3. **Có khớp với tính toán từ nguyên lý đầu không?** Nếu tính ra 9mA mà đo ra 9.3mA thì tốt. Nếu đo ra 90mA thì có gì đó sai — và tìm ra *cái gì* sai mới là bài học.

Nếu cả ba câu đều "có", số của bạn đúng. Nếu một câu "không", dừng lại, đừng đi tiếp.

---

# PHẦN A — NỀN (6h, không cần mua gì, làm được ngay tối nay)

---

## Bài 1 — Bốn đại lượng và một quy tắc

**Câu hỏi:** điện áp, dòng điện, điện trở, công suất là gì, và chúng liên hệ với nhau thế nào?

### Khái niệm

Bốn đại lượng. Học thuộc đơn vị và ký hiệu, vì cả khóa sẽ dùng.

| Đại lượng | Ký hiệu | Đơn vị | So sánh với thứ bạn đã biết |
|---|---|---|---|
| Điện áp | V (hoặc U) | Volt (V) | **Chênh lệch áp suất.** Luôn đo *giữa hai điểm*. |
| Dòng điện | I | Ampere (A) | **Throughput.** Lượng điện tích chảy qua một tiết diện mỗi giây. |
| Điện trở | R | Ohm (Ω) | **Rate limiter.** Cản dòng chảy. |
| Công suất | P | Watt (W) | **Nhiệt sinh ra.** Là chỗ mọi thứ cháy. |

**Ohm's law — quy tắc duy nhất bạn phải thuộc:**

```
V = I × R        I = V / R        R = V / I
P = V × I        P = I² × R       P = V² / R
```

Sáu công thức nhưng chỉ là hai công thức viết lại. Nhớ `V = I×R` và `P = V×I`, phần còn lại tự suy ra.

### Điểm mấu chốt về điện áp mà newbie luôn hiểu sai

**Không tồn tại "điện áp tại một điểm".** Chỉ tồn tại "điện áp giữa điểm A và điểm B". Khi ai đó nói "chân này 3.3V", họ đang ngầm hiểu là *so với GND*.

So sánh: timestamp. Không có "timestamp tuyệt đối" — luôn là số giây kể từ một epoch. GND chính là epoch của mạch điện. Đây là lý do khi bạn tháo dây GND chung giữa hai module, mọi thứ trở nên vô nghĩa: hai bên đang đếm từ hai epoch khác nhau.

**Hệ quả thực hành:** que đen của multimeter luôn cắm vào GND. Luôn. Nếu bạn không biết GND ở đâu, bạn chưa sẵn sàng đo.

### Ba hiểu nhầm chết người

**Hiểu nhầm 1: "Nguồn 5V 3A sẽ đẩy 3A vào mạch của tôi."**
Sai. Nguồn *cung cấp* điện áp. **Tải quyết định dòng.** "3A" là mức tối đa nguồn chịu được, không phải mức nó bơm ra. Cắm một điện trở 1kΩ vào nguồn 5V thì dòng là 5mA, dù nguồn có ghi 3A hay 100A.

So sánh: connection pool max=100 không có nghĩa là luôn có 100 connection đang mở.

**Hiểu nhầm 2: "LED cháy vì điện áp cao quá."**
Gần đúng nhưng sai cơ chế. LED cháy vì **dòng** quá lớn. LED không hành xử như điện trở — nó có điện áp thuận `V_f` gần như cố định (đỏ ~1.8–2.0V, xanh lá ~2.0–2.2V, xanh dương/trắng ~3.0–3.4V). Vượt qua ngưỡng đó, dòng tăng gần như không giới hạn theo điện áp. Không có gì cản → dòng chạy tới khi linh kiện chết.

Điện trở nối tiếp là **rate limiter**. Đó là toàn bộ lý do nó tồn tại.

**Hiểu nhầm 3: "Đo cái gì cũng cắm que như nhau."**
Sai, và đây là chỗ làm cháy cầu chì multimeter trong 10 phút đầu tiên.
- **Đo điện áp:** cắm **song song** — chạm hai que vào hai điểm, mạch vẫn nguyên.
- **Đo dòng:** cắm **nối tiếp** — phải **cắt mạch ra** và cho dòng chạy *qua* multimeter.

Nếu bạn để chế độ đo dòng rồi chạm hai que vào hai cực nguồn, bạn vừa tạo một đường ngắn mạch qua multimeter. Cầu chì đứt, và bạn may mắn nếu chỉ có thế.

### Tự kiểm tra

1. Nguồn 5V, điện trở 220Ω. Dòng bao nhiêu? Công suất tiêu tán trên điện trở bao nhiêu?
2. Tại sao không thể nói "chân GPIO này có điện áp 3.3V" mà không nói thêm gì?
3. Muốn đo dòng chạy qua một con LED, phải làm gì với mạch trước?

<details>
<summary>Đáp án</summary>

1. `I = 5/220 = 22.7mA`. `P = V²/R = 25/220 = 114mW`. Điện trở 1/4W (250mW) chịu được thoải mái.
2. Vì điện áp luôn là hiệu giữa hai điểm. Câu đầy đủ là "3.3V so với GND".
3. Cắt mạch tại một chỗ nào đó trên đường dòng đi qua LED, rồi nối multimeter (chế độ A) vào chỗ cắt để dòng chạy xuyên qua nó.
</details>

---

## Bài 2 — Mạch kín, GND, và tại sao dây nối là một giả định

**Câu hỏi:** vì sao mạch phải kín, và GND thật sự là gì?

### Khái niệm

**Dòng chỉ chảy trong vòng kín.** Từ cực dương của nguồn, qua linh kiện, về cực âm. Hở một chỗ = không có dòng = không có gì hoạt động. Đây là lỗi số một khi mới cắm breadboard: quên nối GND về nguồn.

**GND (ground, mass, 0V)** là điểm được chọn làm mốc. Nó không đặc biệt về mặt vật lý — nó đặc biệt vì mọi người đồng ý gọi nó là 0.

**Common ground:** khi hai module dùng nguồn khác nhau nhưng cần nói chuyện với nhau, GND của chúng **phải nối với nhau**. Không nối = hai hệ quy chiếu độc lập = tín hiệu "3.3V" của bên này có thể là bất cứ giá trị nào so với bên kia.

Đây chính xác là bug bạn sẽ gặp ở Khóa 3 khi tách nguồn cho amplifier. Biết trước sẽ tiết kiệm ba ngày.

**Dây nối không phải dây lý tưởng.** Trong phần mềm, gán `a = b` là chính xác. Trong mạch, một sợi dây có điện trở nhỏ, và khi dòng lớn chạy qua, có sụt áp trên chính sợi dây đó (`V = I×R`). Với dòng vài mA thì bỏ qua được. Với dòng 1A qua dây jumper mỏng thì không.

### Làm

Chưa cần dụng cụ. Vẽ tay ba mạch vào sổ:
1. Nguồn 5V → điện trở 330Ω → LED → về GND. Đánh dấu chiều dòng.
2. Cùng mạch nhưng LED cắm ngược. Điều gì xảy ra? (LED không dẫn, không sáng, không hỏng — LED chỉ dẫn một chiều.)
3. Hai module: một cấp nguồn từ USB, một cấp nguồn từ pin. Vẽ dây tín hiệu giữa chúng. Thiếu dây gì?

### Tự kiểm tra

1. Mạch có nguồn, có LED, có điện trở, LED không sáng, LED không hỏng. Ba nguyên nhân khả dĩ?
2. Vì sao "common ground" là điều kiện bắt buộc chứ không phải tuỳ chọn?

<details>
<summary>Đáp án</summary>

1. (a) mạch hở ở đâu đó — thiếu dây về GND · (b) LED cắm ngược chiều · (c) điện trở quá lớn nên dòng quá nhỏ để thấy sáng.
2. Vì "điện áp" là hiệu giữa hai điểm. Không có mốc chung thì hai bên không có ngôn ngữ chung để nói mức logic HIGH/LOW là bao nhiêu.
</details>

---

## Bài 3 — Tín hiệu số, bus, và clock

**Câu hỏi:** "dữ liệu chạy trên dây" nghĩa là gì về mặt vật lý?

### Khái niệm

**Analog vs digital.** Điện áp trên một sợi dây là một số thực, biến thiên liên tục. "Digital" là một *thoả thuận*: dưới 0.8V gọi là 0, trên 2.0V gọi là 1, khoảng giữa là vùng cấm. Không có gì "số" trong bản chất — chỉ có cách diễn giải.

**Bus** là giao thức chạy trên dây. So sánh trực tiếp:

| Bus | Số dây | So sánh | Dùng cho |
|---|---|---|---|
| **UART** | 2 (TX, RX) | Hai socket một chiều, không có clock chung — hai bên phải *hẹn trước* tốc độ (baud rate) | Log, debug, module GPS/GSM |
| **I2C** | 2 (SDA, SCL) | Bus dùng chung có địa chỉ, như HTTP trên một đường chia sẻ. Chậm nhưng gọn dây. | Cảm biến: IMU, nhiệt ẩm, ToF |
| **SPI** | 4 (MOSI, MISO, SCK, CS) | Kết nối riêng, nhanh, tốn dây | Màn hình, thẻ nhớ, ADC nhanh |
| **I2S** | 3 (BCK, LRCK, DIN) | Stream liên tục có clock, không có địa chỉ, không có ACK | **Audio.** Đây là bus của Khóa 3. |

**Clock là gì và tại sao nó quyết định tất cả.**

Trên một sợi dây chỉ có điện áp cao thấp theo thời gian. Làm sao bên nhận biết một bit kết thúc ở đâu và bit sau bắt đầu ở đâu? Hai cách:

- **Có clock riêng** (I2C, SPI, I2S): một dây khác đánh nhịp. Mỗi cạnh clock = "lấy mẫu dây dữ liệu ngay bây giờ". Tin cậy, tốn thêm dây.
- **Không có clock** (UART): hai bên hẹn trước tốc độ, bên nhận tự đếm giờ. Lệch tốc độ quá 2–3% là hỏng hết.

So sánh: có clock giống như message có delimiter rõ ràng. Không clock giống như fixed-width protocol — phải biết trước độ rộng, và lệch một byte là hỏng toàn bộ stream.

### Con số bạn sẽ dùng suốt Khóa 3

I2S có ba dây:
- **BCK** (bit clock) — mỗi cạnh là một bit
- **LRCK** (left-right clock, còn gọi WS) — báo bit này thuộc kênh trái hay phải. Tần số của nó **chính là sample rate**.
- **DIN** — dữ liệu

Công thức:

```
BCK = sample_rate × số_bit_mỗi_mẫu × số_kênh
```

Audio 24kHz, 16-bit, stereo → `BCK = 24000 × 16 × 2 = 768.000 Hz = 768 kHz`. LRCK = 24 kHz.

Đây là con số đầu tiên trong đời bạn ở tầng vật lý, và ở Bài 14 bạn sẽ nhìn thấy nó bằng mắt trên màn hình.

### Tự kiểm tra

1. Audio 48kHz, 24-bit, stereo. BCK bằng bao nhiêu?
2. Vì sao I2C cần địa chỉ mà I2S thì không?
3. Trên logic analyzer 24MHz, một tín hiệu BCK 768kHz sẽ có bao nhiêu mẫu cho mỗi chu kỳ bit?

<details>
<summary>Đáp án</summary>

1. `48000 × 24 × 2 = 2.304.000 Hz = 2.304 MHz`.
2. I2C là bus chia sẻ nhiều thiết bị trên cùng hai dây → cần địa chỉ để biết nói với ai. I2S là kết nối điểm-điểm một chiều tới đúng một DAC → không cần.
3. `24.000.000 / 768.000 ≈ 31` mẫu mỗi chu kỳ. Thừa sức nhìn rõ. Quy tắc chung: cần ít nhất 4×, lý tưởng 10× tần số tín hiệu.
</details>

---

# PHẦN B — DỤNG CỤ: MỖI MÓN LÀ GÌ VÀ CẦM THẾ NÀO (5h)

---

## Bài 4 — Mua gì, và mỗi món để làm gì

**Đợt 1 đã sửa** — bản cũ thiếu thứ để đo. Không thể học đo tín hiệu số khi trên bàn không có tín hiệu số nào.

| Món | Giá ~ | Nó là gì | Dùng để |
|---|---|---|---|
| **Multimeter UNI-T UT33D+** | 285k | Đồng hồ vạn năng | Đo điện áp, dòng, điện trở, thông mạch. Dụng cụ số một. |
| **Logic analyzer USB 8 kênh 24MHz** | 150–250k | Hộp nhỏ 8 dây kẹp | Nhìn thấy tín hiệu số theo thời gian. **Không** đo điện áp — chỉ nói HIGH/LOW. |
| **USB power meter** | 150–250k | Que cắm giữa sạc và thiết bị | Đo dòng và điện áp thiết bị đang tiêu thụ |
| **Breadboard 830 lỗ** | ~60k | Bảng cắm không cần hàn | Dựng mạch thử |
| **Bộ jumper M-M / M-F / F-F** | ~40k | Dây cắm sẵn đầu | Nối breadboard với module |
| **Kit điện trở + tụ + LED + nút** | 150–250k | Túi linh kiện cơ bản | Nguyên liệu mọi bài |
| **ESP32-S3 DevKit** ⭐ mới | ~200k | Vi điều khiển có WiFi | **Nguồn tín hiệu để đo.** Không có nó thì cả khóa không có gì để cắm que vào. |
| **BME280 (I2C)** ⭐ mới | ~80k | Cảm biến nhiệt/ẩm/áp suất | Thiết bị I2C thật để nhìn thấy ACK/NACK |
| **Mỏ hàn chỉnh nhiệt T12/936 + thiếc + flux** | 400–700k | | Hàn chân module. Chỉ cần từ Bài 8. |
| **Nguồn bench có giới hạn dòng** | 600k–1.5tr | Nguồn để bàn vặn được V và giới hạn A | *Tuỳ chọn nhưng rất nên có.* Giới hạn dòng = lưới an toàn, cứu bạn vài lần cháy linh kiện. |

**Tổng: ~1.8–2.8tr.**

**Mua ở Hà Nội:** Linh Kiện Điện Tử 3M (Số 9, Ngõ 40/2 Tạ Quang Bửu, Bách Khoa) có gần hết. Lập Trình Nhúng A-Z (Cầu Giấy) có module nhúng. Chợ Trời (Thịnh Yên, Hai Bà Trưng) cho linh kiện thụ động rẻ và có ngay.

**Nguyên tắc mua:** với mọi module rẻ và quan trọng, **mua 2 cái**. Không có cái thứ hai để so, bạn không phân biệt được "module chết" với "tôi cấu hình sai" — và sẽ mất nhiều ngày cho một câu hỏi trả lời được trong 30 giây.

### An toàn — đọc một lần rồi thôi

Mọi thứ trong khóa này chạy ở 3.3V/5V DC. **Không có nguy hiểm điện giật.** Ba rủi ro thật:

1. **Ngắn mạch** — nối trực tiếp + với −. Nguồn USB sẽ tự ngắt; pin LiPo thì không, nó sẽ phun lửa. Chưa dùng LiPo trong khóa này.
2. **Mỏ hàn 350°C** — bỏng. Đặt vào giá mỗi lần buông tay, không có ngoại lệ.
3. **Khói flux** — không độc cấp tính nhưng khó chịu. Mở cửa sổ, đừng cúi mặt vào.

Không có bài nào chạm vào điện lưới 220V. Nếu một hướng dẫn nào đó bảo bạn mở nguồn adapter ra, dừng lại.

---

## Bài 5 — Multimeter: cầm thế nào cho đúng

**Câu hỏi:** làm sao đo mà không làm hỏng đồng hồ?

### Khái niệm

Ba lỗ cắm que:
- **COM** — que **đen**, luôn ở đây, không bao giờ đổi
- **VΩmA** — que **đỏ**, cho điện áp / điện trở / dòng nhỏ
- **10A** — que **đỏ**, chỉ khi đo dòng lớn hơn 200mA

Núm xoay, các vị trí bạn cần:

| Ký hiệu | Nghĩa | Cách cắm |
|---|---|---|
| `V⎓` hoặc `DCV` | Điện áp một chiều | **Song song** — chạm hai que vào hai điểm |
| `Ω` | Điện trở | **Linh kiện phải rời mạch, và mạch phải tắt nguồn** |
| `A⎓` hoặc `mA` | Dòng một chiều | **Nối tiếp** — cắt mạch, cho dòng chạy xuyên qua đồng hồ |
| Biểu tượng sóng âm ))) | Thông mạch (kêu bíp) | Tắt nguồn. Chạm hai đầu, nối thông thì kêu. |

### Làm — bài tập 5 phút, không thể hỏng gì

1. Cắm que đen vào COM, que đỏ vào VΩmA.
2. Xoay về `V⎓`.
3. Chạm que đỏ vào cực **+** của một cục pin AA, que đen vào cực **−**.
4. Đọc số.
5. Đảo hai que. Đọc lại.

### Số phải ra

| Trường hợp | Số đúng |
|---|---|
| Pin AA mới | **1.5 – 1.65V** |
| Pin AA đã dùng | 1.2 – 1.4V |
| Pin AA hết | < 1.1V |
| Đảo hai que | **Cùng số nhưng có dấu trừ** (ví dụ −1.58V) |

Dấu trừ không phải lỗi. Nó cho biết bạn đang đo theo chiều ngược. Điện áp có dấu vì nó là *hiệu* giữa hai điểm — đổi thứ tự thì đổi dấu.

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Sửa |
|---|---|---|
| Hiện `0.00` | Que cắm sai lỗ, hoặc chưa chạm vào kim loại | Kiểm tra COM + VΩmA, chạm chắc vào cực pin |
| Hiện `OL` hoặc `1.` bên trái | Vượt thang đo (nếu là đồng hồ chỉnh tay) | Xoay lên thang cao hơn |
| Số nhảy loạn không đứng yên | Que chạm chập chờn | Ấn chắc hơn, hoặc dùng kẹp cá sấu |
| Không lên gì cả | Hết pin đồng hồ | Thay pin 9V trong đồng hồ |

### Bài tập 2 — đo điện trở và đọc mã màu

Điện trở có 4 vòng màu. Ba vòng đầu cho giá trị, vòng cuối cho sai số.

| Màu | Số | | Màu | Số |
|---|---|---|---|---|
| Đen | 0 | | Lục | 5 |
| Nâu | 1 | | Lam | 6 |
| Đỏ | 2 | | Tím | 7 |
| Cam | 3 | | Xám | 8 |
| Vàng | 4 | | Trắng | 9 |

Vòng 1 = chữ số thứ nhất · Vòng 2 = chữ số thứ hai · Vòng 3 = số con số 0 thêm vào · Vòng 4 = sai số (**vàng kim** = ±5%, **bạc** = ±10%, **nâu** = ±1%)

Ví dụ: nâu–đen–đỏ–vàng kim = `1`, `0`, thêm 2 số 0 → **1000Ω = 1kΩ, ±5%**

**Làm:** lấy 5 điện trở khác nhau. Đọc mã màu, ghi giá trị dự đoán vào sổ. Rồi mới đo bằng đồng hồ ở chế độ `Ω`.

**Số phải ra:** giá trị đo nằm trong khoảng sai số ghi trên vòng cuối. Điện trở ±5% ghi 1kΩ phải đo ra **950–1050Ω**.

**Nếu ra khác:**

| Triệu chứng | Nguyên nhân |
|---|---|
| Lệch 10–20% | Đọc nhầm màu — nâu và đỏ rất dễ nhầm dưới đèn vàng. Đọc dưới ánh sáng trắng. |
| Đo ra `OL` | Điện trở đứt, hoặc que không chạm |
| Lệch rất nhiều và không ổn định | Bạn đang cầm cả hai đầu điện trở bằng hai tay — cơ thể bạn là một điện trở song song. Chỉ cầm một đầu. |

Điểm cuối cùng đáng nhớ: **hành động đo làm thay đổi thứ được đo.** Bạn sẽ gặp lại khái niệm này ở dạng nghiêm túc hơn nhiều ở Khóa 5.

---

## Bài 6 — Breadboard: nó nối với nhau như thế nào

**Câu hỏi:** vì sao mạch cắm đúng sơ đồ mà vẫn không chạy?

### Khái niệm

Breadboard 830 lỗ có hai vùng nối khác nhau, và newbie hỏng ở đây nhiều hơn mọi chỗ khác.

```
  ┌─────────────────────────────────────────┐
  │ + + + + + + + + + + + + + + + + + + + + │ ← rail nguồn, nối DỌC theo chiều dài
  │ − − − − − − − − − − − − − − − − − − − − │ ← rail GND
  │                                         │
  │ a b c d e   │khe giữa│   f g h i j      │
  │ ●─●─●─●─●   │        │   ●─●─●─●─●      │ ← mỗi hàng 5 lỗ nối NGANG
  │ ●─●─●─●─●   │        │   ●─●─●─●─●      │
  │ ●─●─●─●─●   │        │   ●─●─●─●─●      │
  │                                         │
  │ + + + + + + + + + + + + + + + + + + + + │
  │ − − − − − − − − − − − − − − − − − − − − │
  └─────────────────────────────────────────┘
```

Ba luật:
1. **Hàng 5 lỗ nối ngang với nhau.** Cắm hai chân vào cùng hàng = chúng nối nhau.
2. **Khe giữa cắt đứt.** Lỗ `e` và lỗ `f` cùng hàng **không** nối nhau. Khe này để cắm chip DIP — mỗi bên một dãy chân.
3. **Rail nguồn nối dọc.** Nhưng **nhiều board có chỗ đứt ở giữa** — nhìn kỹ, thường có một khoảng trống trên vạch màu. Nếu có, phải nối hai nửa bằng dây.

### Làm — kiểm tra board trước khi tin nó

1. Xoay đồng hồ về chế độ thông mạch (biểu tượng `)))`).
2. Cắm hai đầu dây jumper vào hai lỗ **cùng hàng 5 lỗ**. Chạm que vào hai đầu dây. → **phải kêu bíp**
3. Cắm một đầu bên `e`, một đầu bên `f` cùng hàng. → **phải KHÔNG kêu**
4. Cắm hai đầu vào rail `+`, một ở đầu trái board, một ở đầu phải. → nếu **không kêu**, board của bạn có chỗ đứt ở giữa rail. Ghi lại điều đó.

Năm phút này sẽ tiết kiệm cho bạn nhiều giờ về sau.

### Nếu ra khác

| Triệu chứng | Nguyên nhân |
|---|---|
| Không kêu ở bước 2 | Lỗ breadboard bị rão (board rẻ), hoặc dây jumper đứt bên trong. Đổi hàng khác, đổi dây khác. |
| Kêu ở bước 3 | Board lỗi. Hiếm nhưng có. Trả lại. |
| Mọi thứ đều kêu | Đồng hồ vẫn ở chế độ Ω với thang thấp, không phải chế độ thông mạch |

---

## Bài 7 — Logic analyzer và PulseView

**Câu hỏi:** cái hộp 8 dây này thật sự làm gì?

### Khái niệm

Logic analyzer **không đo điện áp**. Nó chỉ trả lời một câu hỏi, rất nhanh, rất nhiều lần: *"ngay bây giờ, dây này đang HIGH hay LOW?"* — rồi vẽ kết quả theo trục thời gian.

So sánh: nó là `tcpdump` cho dây. Multimeter là `curl` — hỏi một câu, được một câu trả lời. Logic analyzer ghi lại toàn bộ lưu lượng.

**Giới hạn phải biết:** loại clone 24MHz lấy mẫu 24 triệu lần/giây. Muốn nhìn rõ một tín hiệu, cần ít nhất 4× tần số của nó, lý tưởng 10×. Vậy:
- BCK 768kHz → 31 mẫu/chu kỳ → rất rõ ✅
- I2C 400kHz → 60 mẫu/chu kỳ → rất rõ ✅
- SPI 8MHz → 3 mẫu/chu kỳ → không đủ, sẽ thấy sai ❌

**Biết giới hạn của dụng cụ đo cũng là một phần của việc đo.** Đây không phải câu triết lý — nó là lý do bạn sẽ không tin nhầm một kết quả sai.

### Làm — cài đặt

1. Tải **PulseView** (thuộc dự án sigrok) từ `sigrok.org`. Có bản Windows/Mac/Linux.
2. Cắm logic analyzer vào USB.
3. Mở PulseView → góc trên bên trái chọn thiết bị → chọn **fx2lafw** (đó là chip trong hầu hết clone).
4. Nếu không thấy thiết bị trên Windows: cần đổi driver sang WinUSB bằng công cụ **Zadig**. Đây là bước gần như chắc chắn phải làm, không phải lỗi của bạn.

### Làm — capture đầu tiên (chưa cần mạch gì)

1. Kẹp dây **GND** của logic analyzer vào GND của mạch. **Bước này không được quên** — thiếu GND thì mọi capture đều là rác, và đây là lỗi số một khi dùng logic analyzer.
2. Kẹp kênh D0 vào một chân bất kỳ đang có tín hiệu.
3. Đặt sample rate 24MHz, số mẫu 1M.
4. Bấm **Run**.

### Số phải ra

Với một chân đang nhấp nháy LED ở 1Hz, bạn thấy sóng vuông đổi mức mỗi 500ms. Rê chuột lên waveform, PulseView hiện thời gian giữa hai điểm.

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Sửa |
|---|---|---|
| Đường thẳng tắp ở HIGH | Chân không có tín hiệu, hoặc quên nối GND | Nối GND trước tiên |
| Đường thẳng tắp ở LOW | Thiết bị chưa được cấp nguồn, hoặc chân bị nối đất | Kiểm tra nguồn của mạch |
| Sóng nhiễu lởm chởm | Dây kẹp quá dài, hoặc thiếu GND | Rút ngắn dây, nối GND sát điểm đo |
| PulseView không thấy thiết bị | Driver | Zadig → WinUSB |

---

## Bài 8 — Mỏ hàn (chỉ cần khi module chưa hàn sẵn chân)

**Câu hỏi:** hàn thế nào để mối hàn dẫn điện thật?

### Khái niệm

Nhiều module (BME280, PCM5102A) bán kèm hàng chân rời — bạn phải tự hàn vào. Đó là toàn bộ nhu cầu hàn trong khóa này.

Mối hàn tốt là mối hàn mà **thiếc chảy loang ra cả hai bề mặt** — chân linh kiện và mặt đồng của board. Mối hàn xấu là giọt thiếc bám hờ lên chân mà không dính vào board — nó **trông giống mối hàn tốt** và đó là vấn đề.

### Làm

1. Đặt nhiệt độ **350°C** (thiếc có chì) hoặc **370°C** (không chì).
2. **Mạ đầu mỏ hàn:** chạm thiếc vào đầu mỏ cho phủ một lớp bóng. Đầu mỏ xỉn đen thì không truyền nhiệt được.
3. Chấm một chút flux lên chỗ cần hàn.
4. **Làm nóng cả chân lẫn mặt đồng cùng lúc** trong ~2 giây — chạm đầu mỏ vào cả hai.
5. Đưa thiếc vào **chỗ tiếp xúc giữa chân và board**, không đưa vào đầu mỏ hàn.
6. Thiếc chảy loang ra → rút thiếc → rút mỏ hàn. Tổng thời gian ~3–4 giây.

### Số phải ra

Mối hàn đúng: **hình nón bóng**, loang đều quanh chân, ôm sát mặt board.

Kiểm tra bằng đồng hồ ở chế độ thông mạch: chạm một que vào chân linh kiện, que kia vào đường mạch. **Phải kêu bíp.**

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Sửa |
|---|---|---|
| Giọt thiếc tròn như hạt, bám hờ | "Cold joint" — chưa đủ nóng | Hàn lại, giữ mỏ lâu hơn 1 giây |
| Thiếc không chảy, vón cục | Đầu mỏ xỉn, hoặc nhiệt thấp | Mạ lại đầu mỏ, tăng nhiệt |
| Hai chân dính vào nhau | Thừa thiếc | Dùng dây hút thiếc, hoặc quẹt đầu mỏ dọc khe |
| Không kêu bíp khi kiểm tra | Cold joint dù trông đẹp | Hàn lại. Đây là lý do phải kiểm tra bằng đồng hồ. |
| Miếng đồng bong khỏi board | Giữ mỏ quá lâu (>10s) | Không cứu được. Đây là lý do mua 2 module. |

---

# PHẦN C — ĐO THẬT (14h)

Từ đây trở đi, mỗi bài đều theo quy trình: **viết dự đoán → commit → rồi mới đo**.

---

## Bài 9 — Voltage divider: thí nghiệm đầu tiên có dự đoán

**Câu hỏi:** hai điện trở nối tiếp chia điện áp theo tỉ lệ nào?

### Khái niệm

Nối tiếp hai điện trở giữa nguồn và GND, điện áp ở điểm giữa là:

```
Vout = Vin × R2 / (R1 + R2)
```

Vì sao: dòng chạy qua cả hai điện trở là như nhau (mạch nối tiếp, không có chỗ nào cho dòng rẽ). `I = Vin/(R1+R2)`. Điện áp rơi trên R2 là `I × R2`. Thay vào là ra công thức.

Đây là mạch phổ biến nhất trong điện tử. Nó là cách hạ 5V xuống 3.3V cho một chân tín hiệu, cách đọc giá trị biến trở, cách đo mức pin.

### Làm

**Bước 1 — dự đoán, trước khi cắm gì.** Tạo file `lab/01-voltage-divider/prediction.md`:

```markdown
Vin = 5.00V (sẽ đo lại giá trị thật)

| R1     | R2     | Vout dự đoán | Cách tính              |
|--------|--------|--------------|------------------------|
| 10kΩ   | 10kΩ   | 2.50V        | 5 × 10/(10+10)         |
| 10kΩ   | 1kΩ    | 0.4545V      | 5 × 1/(10+1)           |
| 1kΩ    | 10kΩ   | 4.545V       | 5 × 10/(1+10)          |
```

`git commit`. **Bắt buộc trước khi sang bước 2.**

**Bước 2 — dựng mạch.** Trên breadboard: 5V → R1 → (điểm giữa) → R2 → GND. Nguồn 5V lấy từ chân 5V của ESP32 đang cắm USB.

**Bước 3 — đo.**
1. Đo Vin thật (giữa chân 5V và GND). Ghi lại — nó hiếm khi đúng 5.00V.
2. Đo Vout (giữa điểm giữa và GND).
3. Lặp cho cả ba cặp điện trở.

**Bước 4 — ghi vào `analysis.md`:** bảng dự đoán / đo / chênh lệch %.

### Số phải ra

| Cặp | Vout dự đoán (với Vin=5.00) | Chấp nhận được |
|---|---|---|
| 10k / 10k | 2.500V | **2.38 – 2.63V** (±5%) |
| 10k / 1k | 0.455V | 0.43 – 0.48V |
| 1k / 10k | 4.545V | 4.32 – 4.77V |

Nếu Vin đo được là 4.92V thay vì 5.00V, tính lại dự đoán với 4.92 trước khi so. **Sai lệch phải <5% sau khi hiệu chỉnh Vin.**

Vì sao vẫn còn sai lệch nhỏ: điện trở ±5%, cộng sai số của chính đồng hồ. Đây là mức sai lệch **đúng**, không phải lỗi.

### Nếu ra khác

| Triệu chứng | Nguyên nhân |
|---|---|
| Vout = Vin | R2 hở mạch — cắm nhầm hàng breadboard, hoặc chân không tiếp xúc |
| Vout = 0 | R1 hở, hoặc điểm giữa bị nối thẳng xuống GND |
| Vout lệch >20% | Đọc nhầm mã màu điện trở. Đo lại từng con bằng chế độ Ω. |
| Số nhảy liên tục | Que đo chạm chập chờn |

### Thí nghiệm phá — làm cái này, nó dạy nhiều nhất

Đổi cả hai điện trở sang **1MΩ** (nâu–đen–xanh lục). Tỉ lệ vẫn 1:1, nên về lý thuyết Vout vẫn phải là 2.50V.

Đo. Bạn sẽ thấy số **thấp hơn rõ rệt**.

Vì sao: multimeter có điện trở đầu vào khoảng 10MΩ. Khi bạn cắm que vào, nó trở thành một điện trở 10MΩ song song với R2. Với R2 = 10kΩ thì 10MΩ song song không đáng kể. Với R2 = 1MΩ thì nó kéo giá trị xuống thấy rõ.

**Bài học:** dụng cụ đo là một phần của mạch. Phép đo làm thay đổi thứ được đo. Ghi câu này vào notebook — bạn sẽ gặp lại nó ở dạng khó hơn nhiều khi đo đồng bộ thời gian ở Khóa 5.

---

## Bài 10 — LED và điện trở: tại sao, bằng số

**Câu hỏi:** vì sao LED cần điện trở, và giá trị bao nhiêu là đúng?

### Làm

**Bước 1 — dự đoán.** Tạo `lab/02-led-current/prediction.md`:

```markdown
LED đỏ, tra datasheet (hoặc giả định): V_f ≈ 2.0V
Nguồn: 5.00V
Muốn dòng: 10mA = 0.010A

R cần = (5.00 − 2.0) / 0.010 = 300Ω
Giá trị chuẩn gần nhất: 330Ω

Với R = 330Ω thực tế:
  I = (5.00 − 2.0) / 330 = 9.09mA
  V trên điện trở = 3.00V
  V trên LED      = 2.00V
  P trên điện trở = 3.00 × 0.00909 = 27mW  (điện trở 1/4W: an toàn)
```

`git commit`.

**Bước 2 — dựng.** 5V → điện trở 330Ω → chân dài của LED (anode, +) → chân ngắn (cathode, −) → GND.

Chân dài là +. Nếu chân bị cắt bằng nhau, tìm cạnh vát phẳng trên vành nhựa — cạnh đó là cathode (−).

**Bước 3 — đo ba thứ:**
1. Điện áp trên điện trở (hai đầu điện trở)
2. Điện áp trên LED (hai chân LED)
3. Dòng: **cắt mạch**, chuyển đồng hồ sang `mA`, nối tiếp vào chỗ cắt

**Bước 4 — kiểm tra chéo.** Lấy điện áp trên điện trở chia cho 330. So với dòng đo trực tiếp. Hai số phải khớp — đây chính là câu hỏi số 2 trong "Ba câu hỏi để tự biết mình đo đúng".

### Số phải ra

| Đại lượng | Dự đoán | Chấp nhận được |
|---|---|---|
| V trên điện trở | 3.00V | 2.7 – 3.3V |
| V trên LED (V_f thật) | 2.00V | **1.8 – 2.1V** cho LED đỏ |
| Dòng | 9.09mA | **8 – 10mA** |
| V_R / 330 vs dòng đo | khớp | lệch <5% |

**Tổng kiểm:** `V_điện_trở + V_LED` phải bằng `V_nguồn`, sai lệch <2%. Đây là định luật Kirchhoff — tổng điện áp rơi trên một vòng kín bằng điện áp cấp. Nếu không khớp, một trong ba số đo sai.

### Giải thích chênh lệch — đây mới là bài học

V_f đo được gần như chắc chắn **không đúng 2.00V**. Thường 1.85–1.95V ở 9mA.

Vì sao: **V_f không phải hằng số.** Nó phụ thuộc dòng. Datasheet ghi V_f tại một dòng cụ thể (thường 20mA). Bạn đang chạy 9mA nên V_f thấp hơn.

Đây là lần đầu bạn gặp một thứ mà phần mềm không có: **một tham số không phải hằng số mà là một đường cong.** Trong code, `const V_F = 2.0` là đúng. Trong mạch, `V_f = f(I, nhiệt độ, từng con LED một)`.

Ghi câu giải thích đó vào `analysis.md` bằng lời của bạn. Đó là tiêu chí PASS số 3 của Khóa 1.

### Nếu ra khác

| Triệu chứng | Nguyên nhân |
|---|---|
| LED không sáng, không nóng | Cắm ngược chiều. Đảo LED lại. |
| LED sáng rất mờ | Điện trở quá lớn — đo lại giá trị, có thể là 33kΩ chứ không phải 330Ω |
| LED sáng chói rồi tắt hẳn, có mùi khét | Quên điện trở. LED chết. Đây là lý do mua nhiều LED. |
| Dòng đo ra 0 khi chuyển sang mA | Que đỏ vẫn ở lỗ VΩmA nhưng dòng vượt thang, hoặc cầu chì đã đứt từ lần trước |
| Đồng hồ đo dòng làm mạch tắt hẳn | Chưa nối tiếp đúng — mạch vẫn hở |

---

## Bài 11 — Đọc trọn một datasheet

**Câu hỏi:** tài liệu 60 trang này, đọc phần nào?

### Khái niệm

Datasheet là hợp đồng của con chip. Tutorial nói bạn *gõ gì*; datasheet nói con chip *làm gì*. Nguyên tắc số 3 của cả lộ trình: datasheet > tutorial.

Lấy datasheet **BME280** của Bosch (Google "BME280 datasheet bosch", file PDF chính hãng). Đọc theo thứ tự này, không đọc tuần tự từ trang 1:

| Mục | Tìm gì | Vì sao quan trọng |
|---|---|---|
| **Absolute Maximum Ratings** | Điện áp tối đa | Vượt là chết chip. Đọc đầu tiên, luôn luôn. |
| **Electrical Characteristics** | VDD hoạt động, dòng tiêu thụ | Cấp 5V vào chip 3.3V là hỏng |
| **Pin Description** | Từng chân làm gì | Biết cắm vào đâu |
| **Register Map** | Địa chỉ và ý nghĩa từng thanh ghi | **Đây là API của chip** |
| **Timing Diagram** | Thứ tự tín hiệu theo thời gian | Cần ở Khóa 3 và 5 |
| Package / Soldering | Kích thước vật lý | Bỏ qua, bạn dùng module có sẵn |

**Register map là API.** Mỗi thanh ghi là một địa chỉ 8-bit, đọc/ghi qua I2C. Ví dụ với BME280: `0xD0` là chip ID và luôn trả về `0x60`. Đó là endpoint `/health` của con chip.

### Làm

1. Tải datasheet BME280.
2. Đọc từ đầu tới cuối. **Không skim.** Chỗ nào không hiểu thì ghi lại chỗ đó chứ đừng bỏ qua — cuối khóa nhìn lại danh sách này rất có ích.
3. **Viết tay ra giấy** register map: địa chỉ, tên, ý nghĩa, đọc hay ghi. Ít nhất 8 thanh ghi.
4. Chụp ảnh trang giấy, commit vào `lab/03-datasheet/`.

Viết tay, không copy-paste. Việc chép tay ép mắt bạn đi qua từng dòng.

### Số phải ra

Register map bạn viết đối chiếu đúng **≥90%** với datasheet. Có ít nhất `0xD0` (chip ID, giá trị `0x60`), một thanh ghi cấu hình, và một thanh ghi dữ liệu.

Và bạn trả lời được ba câu:
1. BME280 chạy ở điện áp nào? Cấp 5V trực tiếp có sao không?
2. Địa chỉ I2C của nó là gì, và làm sao đổi được?
3. Đọc thanh ghi nào để biết chip còn sống?

### Nếu ra khác

| Triệu chứng | Sửa |
|---|---|
| Không tìm thấy register map | Bạn đang đọc trang bán hàng của module, không phải datasheet của chip. Tìm PDF từ Bosch. |
| Quá tải, không hiểu gì | Bình thường. Đọc lượt hai chỉ nhắm 4 mục trong bảng trên, bỏ qua phần compensation formula. |
| Module ghi 3.3V nhưng bán kèm "5V tolerant" | Module có sẵn mạch hạ áp. Chip vẫn 3.3V. Đọc kỹ mô tả module, khác với chip. |

---

# PHẦN D — NHÌN THẤY DỮ LIỆU TRÊN DÂY (10h)

---

## Bài 12 — Cắm I2C và nhìn thấy ACK

**Câu hỏi:** khi code gọi `sensor.read()`, chuyện gì xảy ra trên hai sợi dây?

### Khái niệm

I2C dùng hai dây dùng chung cho nhiều thiết bị:
- **SCL** — clock, do master (ESP32) phát
- **SDA** — dữ liệu, hai chiều

Một giao dịch đọc gồm:
1. **START** — SDA xuống thấp trong khi SCL đang cao. Đây là dấu hiệu duy nhất không phải dữ liệu.
2. **7 bit địa chỉ** + 1 bit R/W
3. **ACK** — slave kéo SDA xuống thấp ở nhịp clock thứ 9. **Đây là cái bạn cần nhìn thấy.** Nó nghĩa là "có tôi ở đây".
4. Byte dữ liệu, mỗi byte theo sau một ACK
5. **STOP** — SDA lên cao trong khi SCL đang cao

**NACK** (SDA vẫn cao ở nhịp thứ 9) nghĩa là không ai trả lời địa chỉ đó.

So sánh: START/STOP là mở/đóng connection. Địa chỉ là routing. ACK là 200 OK. NACK là 404.

**Pull-up resistor:** cả hai dây I2C không được đẩy lên cao bởi thiết bị nào — chúng chỉ được *kéo xuống*. Muốn có mức cao, cần điện trở kéo lên VCC (thường 4.7kΩ). Hầu hết module breakout đã có sẵn. Nếu bạn thấy cả hai dây luôn ở mức thấp và không có gì xảy ra, thiếu pull-up là nghi phạm số một.

### Làm

**Bước 1 — nối dây.** ESP32-S3 với BME280:

| BME280 | ESP32-S3 | Ghi chú |
|---|---|---|
| VCC | 3V3 | **Không phải 5V** |
| GND | GND | |
| SDA | GPIO 8 (mặc định) | |
| SCL | GPIO 9 (mặc định) | |

Kiểm tra chân trên board thật, vì mỗi biến thể DevKit đánh số hơi khác. Tra pinout của đúng board bạn mua.

**Bước 2 — chạy I2C scanner.** Cài Arduino IDE, thêm ESP32 board support, nạp sketch scanner (mẫu `Wire/i2c_scanner` có sẵn trong thư viện Wire). Mở Serial Monitor ở 115200.

**Bước 3 — dự đoán trước khi cắm logic analyzer.** File `lab/04-i2c/prediction.md`:

```markdown
Địa chỉ BME280 dự đoán: 0x76 (chân SDO nối GND) hoặc 0x77 (SDO nối VCC)
Tần số SCL dự đoán: 100 kHz (mặc định của thư viện Wire)
→ chu kỳ SCL = 10 µs

Sau START, tôi kỳ vọng thấy:
  7 bit địa chỉ = 1110110 (0x76)
  1 bit R/W = 0 (ghi)
  ACK ở nhịp clock thứ 9: SDA bị kéo xuống THẤP
```

`git commit`.

**Bước 4 — cắm logic analyzer.**

| Logic analyzer | Nối vào |
|---|---|
| **GND** | GND của mạch ← **không được quên** |
| D0 | SCL |
| D1 | SDA |

**Bước 5 — capture.**
1. PulseView → sample rate **4MHz**, số mẫu **1M**
2. Bấm **Run**, rồi bấm reset trên ESP32 để nó chạy scanner
3. Bấm nút **decoder** (biểu tượng zigzag) → chọn **I²C**
4. Gán: SCL = D0, SDA = D1
5. Zoom vào chỗ có hoạt động

### Số phải ra

PulseView hiện một dải nhãn dưới waveform:

```
START | Address write: 76 | ACK | Data write: D0 | ACK | START | Address read: 76 | ACK | Data read: 60 | NACK | STOP
```

Ba thứ phải nhìn thấy:
1. **START** ở đầu
2. **ACK** (không phải NACK) ngay sau địa chỉ `0x76` hoặc `0x77`
3. **Chu kỳ SCL ≈ 10µs**, tức 100kHz — rê chuột đo giữa hai cạnh lên liên tiếp

Serial Monitor phải in ra `I2C device found at address 0x76`.

Zoom sát vào nhịp clock thứ 9 sau địa chỉ: **SDA bị kéo xuống thấp trong khi SCL đang cao.** Đó là ACK, tận mắt. Cảm biến vừa nói "có tôi đây" và bạn vừa nhìn thấy nó bằng điện áp trên một sợi dây.

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Sửa |
|---|---|---|
| Cả SCL và SDA đều thẳng HIGH, không có gì | Code chưa chạy, hoặc analyzer chưa nối GND | Nối GND. Kiểm tra Serial Monitor có output không. |
| Cả hai thẳng LOW | Thiếu pull-up, hoặc chập SDA/SCL xuống GND | Kiểm tra dây. Thêm 4.7kΩ từ mỗi dây lên 3.3V nếu module không có sẵn. |
| Thấy sóng nhưng decoder báo lỗi | Gán nhầm kênh SCL/SDA | Đổi chỗ hai kênh trong cấu hình decoder |
| **NACK** sau địa chỉ | Sai địa chỉ, hoặc cảm biến chưa được cấp nguồn | Thử `0x77`. Đo điện áp chân VCC của cảm biến — phải ~3.3V. |
| Scanner không tìm thấy gì | Nối nhầm chân SDA/SCL | Đảo hai dây thử. Đây là lỗi phổ biến nhất. |
| Chu kỳ SCL ≈ 2.5µs thay vì 10µs | Thư viện đang chạy 400kHz | Không sai — chỉ là cấu hình khác. **Sửa lại dự đoán và giải thích**, đừng sửa số đo. |

Dòng cuối cùng đáng đọc lại. Khi số đo khác dự đoán, thứ phải thay đổi là **hiểu biết của bạn**, không phải số đo.

---

## Bài 13 — Nhìn thấy I2S

**Câu hỏi:** sample rate trông như thế nào trên dây?

### Khái niệm

Bài này nối trực tiếp sang Khóa 3. Bạn chưa có DAC PCM5102A (đợt 2), nhưng ESP32-S3 **tự phát được I2S** — nó có sẵn ngoại vi I2S. Không cần thiết bị nhận; bạn chỉ cần nhìn tín hiệu ESP32 phát ra.

### Làm

**Bước 1 — dự đoán.** File `lab/05-i2s/prediction.md`:

```markdown
Cấu hình: 16 kHz, 16-bit, stereo

LRCK = sample rate           = 16.000 Hz     → chu kỳ 62.5 µs
BCK  = 16000 × 16 × 2        = 512.000 Hz    → chu kỳ 1.95 µs
Số chu kỳ BCK trong một chu kỳ LRCK = 32

Sau khi đổi sang 32 kHz:
LRCK = 32.000 Hz    → chu kỳ 31.25 µs
BCK  = 1.024.000 Hz → chu kỳ 0.98 µs
```

`git commit`.

**Bước 2 — nạp code.** Dùng ví dụ I2S trong ESP-IDF hoặc thư viện `ESP_I2S` của Arduino, cấu hình master TX, 16kHz, 16-bit, stereo, phát sine wave. Gán ba chân bất kỳ cho BCK, LRCK (WS), DOUT.

**Bước 3 — capture.** Logic analyzer: GND + D0=BCK, D1=LRCK, D2=DOUT. Sample rate **24MHz**.

**Bước 4 — đo.** Rê chuột đo chu kỳ LRCK và chu kỳ BCK. Đếm số cạnh BCK trong một nửa chu kỳ LRCK.

**Bước 5 — đổi sang 32kHz.** Dự đoán lại (đã viết ở bước 1), nạp lại, đo lại.

### Số phải ra

| Đại lượng | 16kHz | 32kHz | Chấp nhận được |
|---|---|---|---|
| Chu kỳ LRCK | 62.5 µs | 31.25 µs | **±1%** |
| Chu kỳ BCK | 1.95 µs | 0.98 µs | ±1% |
| Số chu kỳ BCK / chu kỳ LRCK | 32 | 32 | **chính xác 32** |

Sai số 1% là chặt hơn nhiều so với các bài trước. Lý do: clock được tạo bởi thạch anh, và thạch anh chính xác. Nếu bạn lệch 10%, đó không phải sai số đo — đó là cấu hình khác với bạn nghĩ.

Con số **32** phải chính xác tuyệt đối: 16 bit × 2 kênh. Đếm được đúng 32 nghĩa là bạn đã hiểu cấu trúc frame I2S.

### Nếu ra khác

| Triệu chứng | Nguyên nhân |
|---|---|
| LRCK đúng, BCK gấp đôi dự đoán | Cấu hình 32-bit chứ không phải 16-bit. Kiểm tra `bits_per_sample`. |
| Số BCK mỗi LRCK là 64 | Cùng nguyên nhân — 32-bit stereo |
| Số BCK mỗi LRCK là 16 | Đang chạy mono |
| LRCK lệch vài % | Thạch anh không chính xác tuyệt đối, hoặc bộ chia không ra đúng số nguyên. Ghi lại — **đây chính là clock drift**, và nó là chủ đề chính của Khóa 5. |
| DOUT thẳng đơ | Chưa có dữ liệu được ghi vào buffer I2S |

Dòng áp chót đáng chú ý. Nếu bạn thấy LRCK ra 15.987kHz thay vì 16.000kHz, bạn vừa tự tay quan sát lý do vì sao đồng bộ thời gian giữa nhiều thiết bị là một bài toán khó. Ghi con số đó lại.

---

## Bài 14 — Gate Khóa 1

Đây là checklist PASS. Kiểm được bởi người khác đọc repo của bạn, không phải bởi cảm giác.

**PASS khi đủ cả 6:**

| # | Tiêu chí | Cách kiểm |
|---|---|---|
| 1 | Repo public có `hours.csv` ≥14 ngày và cấu trúc `/lab/` | Mở repo |
| 2 | 5 thư mục lab, mỗi cái có `prediction.md` **commit trước** `analysis.md` | `git log --format="%ci %f"` — kiểm thứ tự timestamp |
| 3 | Voltage divider: 3 tỉ lệ, sai lệch **<5%** sau khi hiệu chỉnh Vin | Bảng trong `analysis.md` |
| 4 | LED: dòng tính vs đo sai lệch **<10%**, kèm **giải thích bằng lời** vì sao V_f không phải hằng số | Đoạn văn trong `analysis.md` |
| 5 | File capture `.sr` của bus I2C thật, decode ra **ACK**, kèm ảnh chụp PulseView | File trong repo |
| 6 | Register map viết tay chụp ảnh, đúng ≥90%; đo được LRCK/BCK sai lệch **<1%** | Ảnh + bảng số |

**Ngân sách:** 35h. **Trần:** 55h.

**Nếu chạm 55h chưa xong:** không phải thiếu kiến thức mà sai cách học. Mua một khóa có cấu trúc (EEVblog Fundamentals hoặc Ben Eater xem hết theo thứ tự), cấp thêm 15h, thử lại đúng một lần. Chạm 70h → dừng Khóa 1, dồn toàn bộ giờ vào Khóa 2 (không cần phần cứng) và xem lại sau 3 tháng.

---

# LỊCH 4 TUẦN

| Tuần | Giờ | Làm | Xong thì có |
|---|---|---|---|
| **1** | 8h | Bài 1–3 (đọc, không cần dụng cụ) · đặt mua đợt 1 · tạo repo, `hours.csv`, CI check | Nền khái niệm + repo |
| **2** | 9h | Bài 4–8 khi hàng về · Bài 9 (voltage divider) | Biết dùng đồng hồ, breadboard, PulseView |
| **3** | 10h | Bài 10 (LED) · Bài 11 (datasheet) · hàn chân BME280 nếu cần | 3 thí nghiệm có dự đoán |
| **4** | 8h | Bài 12 (I2C + ACK) · Bài 13 (I2S) · Bài 14 (gate) | **Khóa 1 PASS** |

**Tuần bận không ngồi bàn được:** chuyển sang Khóa 2 (MCAP, Foxglove, dataset audit) — thuần phần mềm, làm được ở bất cứ đâu có laptop. Đừng cố ép một thí nghiệm phần cứng vào tuần 14h/ngày.

---

# NGUỒN HỌC KÈM THEO KHÓA 1

Xem có chọn lọc, đừng lướt.

| Nguồn | Xem phần nào | Cho bài nào |
|---|---|---|
| **Ben Eater** (YouTube) | Series điện tử cơ bản, phần về bus và clock | Bài 1–3, 12 |
| **EEVblog Fundamentals** (Dave Jones) | Tập về multimeter, tập về đọc datasheet | Bài 5, 11 |
| **SparkFun tutorials** | "How to Use a Multimeter", "How to Use a Breadboard", "I2C" | Bài 5, 6, 12 |
| **sigrok/PulseView docs** | Getting started + decoder | Bài 7, 12, 13 |
| **Making Embedded Systems** — Elecia White | Chương đầu | Tư duy embedded cho người từ software |
| **Espressif ESP-IDF Programming Guide** | I2C driver, I2S driver | Bài 12, 13 |

Không cần sách điện tử dày ở giai đoạn này. *The Art of Electronics* để dành làm từ điển tra cứu về sau, đừng đọc tuần tự.

---

# SAU KHÓA 1

Hai hướng đi song song:

**Khóa 2 — Dữ liệu robot mà không cần robot (80h).** MCAP, Protobuf schema có version, Foxglove, LeRobot dataset format, và xây dataset audit tool. Không cần phần cứng, không cần tiền, đúng thế mạnh hiện tại. Đây là khóa tạo ra artifact công khai đầu tiên và tín hiệu phỏng vấn đầu tiên. **Bắt đầu song song với Khóa 1, đừng chờ.**

**Khóa 3 — Chuỗi audio (90h).** Mua đợt 2 (Pi 5, DAC I2S, amp, loa, mic). Đi hết chuỗi từ số nguyên tới áp suất không khí, với 5 thí nghiệm có số đo. Chỉ mở sau khi Khóa 1 PASS — vì nếu chưa đo được thì mua Pi về cũng chỉ để chạy tutorial.

Điều kiện mở Khóa 3: Khóa 1 PASS + `hours.csv` cho thấy median ≥5h/tuần.
