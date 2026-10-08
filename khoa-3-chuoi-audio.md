# KHÓA 3 — CHUỖI AUDIO: TỪ SỐ NGUYÊN ĐẾN ÁP SUẤT KHÔNG KHÍ

**Cho:** người đã PASS Khóa 1, biết cầm que đo và đọc logic analyzer.
**Thời lượng:** ~90h · **Trần:** 140h. Khoảng 12–14 tuần ở nhịp 6–7h/tuần.
**Chi phí:** chuỗi audio ~0.7–1tr (DAC, amp, loa, mic). Mini PC N100 đã mua riêng (mục 0.7 lộ trình tổng). ESP32-S3 đã có từ Khóa 1. **Không mua Raspberry Pi.**
**Tương ứng:** milestone **M4** trong lộ trình 24 tháng.

**Xong khóa này bạn làm được:** đi hết chuỗi từ một số nguyên trong RAM tới sóng áp suất trong không khí, và **có số đo ở mọi chặng**. Đó là câu chuyện bạn kể trong phỏng vấn khi người ta hỏi "anh đã thực sự chạm phần cứng chưa".

**Điều kiện mở khóa — cả ba:**
1. Khóa 1 PASS (5 tiêu chí của M1)
2. `hours.csv` cho thấy median ≥5h/tuần trong 4 tuần gần nhất
3. Đã có mini PC + đã mua chuỗi audio (đợt 2a + 2b)

**Điều kiện mở Module 4 (deploy ở công ty):** B2 đã có câu trả lời **bằng văn bản** từ quản lý. Đồng ý hay từ chối đều được — chỉ cần có câu trả lời. Nếu từ chối: chạy V1 ở nhà, bỏ hoàn toàn phần nhận diện mặt, portfolio không mất gì.

---

## VỊ TRÍ TRONG BẢN ĐỒ 7 KHÓA

| Khóa | Tên | Giờ | Trạng thái |
|---|---|---|---|
| 1 | Từ zero đến đo được | 35 | Gần xong |
| 2 | Dữ liệu robot mà không cần robot | 80 | **Chạy song song — đừng dừng** |
| **3** | **Chuỗi audio** | **90** | ← tài liệu này |
| 4 | Đo hiệu năng inference trên edge | 70 | Sau |
| 5 | Cảm biến, đồng bộ thời gian, data platform | 150 | Sau |
| 6 | Simulation & evaluation infrastructure | 120 | Sau |
| 7 | Robot di động hoàn chỉnh | 340 | Sau |

**Nhắc quan trọng:** Khóa 3 là Track C (chiều sâu phần cứng), chậm và tốn giờ nhất. Khóa 2 là Track B, tạo artifact và tín hiệu phỏng vấn nhanh nhất. **Tuần bận thì chạy Khóa 2, tuần rảnh thì chạy Khóa 3.** Đừng để Khóa 3 nuốt hết giờ — nó là thứ khiến bạn không bị loại, không phải thứ khiến bạn được gọi.

---

## CẤU TRÚC KHÓA

| Module | Nội dung | Giờ |
|---|---|---|
| **1** | Chuỗi phát: số nguyên → áp suất không khí | 32 |
| **2** | Đo độ trễ thật | 16 |
| **3** | TTS và quyết định kiến trúc | 14 |
| **4** | Hệ thống V1 | 22 |
| **Gate** | Đóng gói, đối chiếu 7 tiêu chí M4 | 6 |

Mỗi bài giữ nguyên sáu phần như Khóa 1: **Câu hỏi · Khái niệm · Làm · Số phải ra · Nếu ra khác · Tự kiểm tra**.

**Quy tắc bất di bất dịch:** viết dự đoán bằng số vào `prediction.md`, commit, rồi mới cắm que đo. Ở khóa này quy tắc đó còn quan trọng hơn Khóa 1, vì âm thanh có một đặc tính nguy hiểm: **nó "nghe có vẻ đúng" ở rất nhiều cấu hình sai.** Tai người tha thứ cho sai số 5% ở tần số lấy mẫu, nhưng logic analyzer thì không.

---

## MỘT LỜI CẢNH BÁO VỀ PHẠM VI

Tài liệu M4 gốc ghi: chạm 140h chưa PASS → **cắt scope, không gia hạn**. Bỏ điều kiện 5 và 7, chỉ giữ "phát được audio ổn định 24h", publish nguyên trạng kèm ghi chú rõ cái gì chưa làm được, sang Khóa 4.

Ghi cái này vào đầu `decisions.md` ngay hôm nay, trước khi bắt đầu. Đây là cam kết trước, không phải quyết định lúc nản.

---

# MODULE 1 — CHUỖI PHÁT (32h)

---

## Bài 1 — Audio số thực sự là cái gì (2h)

**Câu hỏi:** một file audio là gì, ở mức byte?

### Khái niệm

Bỏ hết khái niệm "file nhạc" đi. Ở tầng bạn sắp làm việc, audio là **một mảng số nguyên**, và ba tham số quyết định ý nghĩa của mảng đó:

| Tham số | Là gì | Giá trị của V1 |
|---|---|---|
| **Sample rate** | Bao nhiêu số mỗi giây, mỗi kênh | 24.000 |
| **Bit depth** | Mỗi số bao nhiêu bit | 16 (signed, little-endian) |
| **Channels** | Bao nhiêu kênh | 2 (stereo) |

**Bit rate** = sample_rate × bit_depth × channels. Với V1: `24000 × 16 × 2 = 768.000 bit/s = 96 KB/s`.

**Frame vs sample — chỗ hay nhầm.** Trong ngôn ngữ ALSA, một **frame** = một sample cho *mỗi* kênh. Stereo 16-bit → 1 frame = 4 byte. Khi ALSA nói `buffer_size = 4800`, nó nói 4800 *frame*, tức 9600 sample, tức 19200 byte. Nhầm frame với sample là nguồn của rất nhiều bug độ trễ tính sai gấp đôi.

**Interleaving.** Stereo thường lưu xen kẽ: `L R L R L R...`. Không phải `LLLL...RRRR`. Đọc nhầm layout → hai kênh lệch nhau một sample và âm thanh nghe như bị lệch pha.

**Nyquist và vì sao 24kHz đủ cho giọng nói.** Tần số lấy mẫu f cho phép tái tạo tín hiệu tối đa f/2. 24kHz → tối đa 12kHz. Giọng người có F0 (tần số cơ bản) 85–255Hz, nhưng phụ âm xát (s, x, sh) có năng lượng tới 8–10kHz. 12kHz đủ cho giọng nói rõ ràng; không đủ cho nhạc. Đây là lý do TTS thường dùng 22.05 hoặc 24kHz chứ không phải 44.1kHz — và là một quyết định kỹ thuật bạn phải bảo vệ được, không phải một con số copy từ tutorial.

**Quan hệ bit depth ↔ nhiễu.** Mỗi bit thêm vào cho ~6dB dải động:

```
SNR_lý_thuyết ≈ 6.02 × bits + 1.76  (dB)
```

16-bit → 98.1 dB · 12-bit → 74.0 dB · 8-bit → 49.9 dB · 4-bit → 25.8 dB

Nhớ công thức này. Bài 7 sẽ đo nó.

### Làm

1. Tạo một file WAV 1 giây chứa tone sin 440Hz, 24kHz, 16-bit, mono, bằng Python thuần (`struct` + `math`, **không dùng thư viện audio**).
2. Mở file bằng hex editor. Tìm header RIFF. Đếm byte. Xác minh số byte dữ liệu.
3. Đổi sang stereo, xen kẽ L/R. Đếm lại.
4. In ra 20 giá trị sample đầu tiên dưới dạng số nguyên.

### Số phải ra

| Kiểm tra | Giá trị đúng |
|---|---|
| Số sample của 1s mono @24kHz | 24.000 |
| Số byte dữ liệu (mono, 16-bit) | 48.000 |
| Số byte dữ liệu (stereo, 16-bit) | 96.000 |
| Kích thước file WAV | 48.000 (hoặc 96.000) + 44 byte header |
| Số sample trong một chu kỳ 440Hz @24kHz | 24000/440 ≈ **54,5** — không phải số nguyên |
| Giá trị đỉnh nếu biên độ đầy | ±32767 |

Chi tiết cuối cùng đáng dừng lại: 54,5 sample mỗi chu kỳ nghĩa là tone 440Hz **không lặp lại chính xác** sau mỗi chu kỳ ở 24kHz. Đây là gốc rễ của rất nhiều hiện tượng trong xử lý tín hiệu số.

### Tự kiểm tra

1. *Một file 30 giây, 48kHz, 24-bit, stereo nặng bao nhiêu?* → 48000 × 3 × 2 × 30 = 8.640.000 byte ≈ 8,24 MiB
2. *Vì sao 24-bit audio thường được truyền trong khung 32-bit?* → Vì phần cứng và bus làm việc theo bội số của 8/16/32 bit; 24-bit được đệm vào khung 32-bit cho gọn. Bạn sẽ thấy chính xác điều này trên logic analyzer ở Bài 7.
3. *Buffer 4800 frame ở 24kHz stereo 16-bit là bao nhiêu ms và bao nhiêu byte?* → 200ms, 19.200 byte

---

## Bài 2 — Dựng mini PC, ESP32-S3 và DAC I2S (5h)

**Câu hỏi:** làm sao để một máy tính Linux đẩy bit ra ba sợi dây — khi máy đó không có chân GPIO nào?

### Khái niệm

**Kiến trúc của khóa này** (quyết định ở mục 0.7 lộ trình tổng):

```
Mini PC N100 (Ubuntu) ──USB-CDC──► ESP32-S3 ──I2S──► PCM5102A ──► amp ──► loa
   TTS, ring buffer host            ring buffer MCU
                                    I2S DMA, GPIO marker
```

Máy Linux **không bao giờ** trực tiếp chạm dây tín hiệu thời gian thực — đó là việc của MCU. Đây đúng là cách robot thật được thiết kế, và nó cho bạn thêm một chặng (host → MCU qua USB) phải đo, giống hệt chặng mini PC → bộ điều khiển motor ở Khóa 7.

**Vì sao I2S chứ không phải USB sound card.** Bạn muốn **nhìn thấy tín hiệu số trước khi nó thành analog**. Với I2S bạn cắm logic analyzer và thấy từng bit sample chạy trên dây. Với USB sound card, toàn bộ chuỗi bị giấu trong firmware và bạn không học được gì.

**Ba dây của I2S:**

| Dây | Tên khác | Là gì |
|---|---|---|
| **BCK** | BCLK, SCK, PCM_CLK | Bit clock — mỗi cạnh đánh nhịp một bit |
| **LRCK** | WS, LRCLK, PCM_FS | Word select — mức thấp = kênh trái, cao = kênh phải. **Tần số của nó chính là sample rate.** |
| **DIN** | SD, DATA, DOUT (phía ESP32) | Dữ liệu |

Cộng GND. Luôn luôn cộng GND.

### Làm

**Bước 1 — mini PC.** Ubuntu 24.04 LTS. Cắm Ethernet, không dùng WiFi trong lúc dev (một biến số ít đi). Ghi `ethtool -T` của cả hai cổng vào `decisions.md` ngay bây giờ — Khóa 5 cần nó.

**Bước 2 — ESP-IDF, không Arduino.** Từ khóa này trở đi dùng **ESP-IDF v5.x**, driver I2S "standard mode" (`i2s_new_channel`, `i2s_channel_init_std_mode`). Lý do: cấu hình DMA buffer chính là bài học của Module 2, và Arduino giấu nó đi — đúng như `aplay` giấu ALSA buffer.

**Bước 3 — đấu dây PCM5102A.** Kiểm tra ba lần trước khi cấp điện:

| PCM5102A | ESP32-S3 | Ghi chú |
|---|---|---|
| VCC | 5V (VBUS) hoặc 3V3 — **kiểm module của bạn** | Module có regulator riêng thường nhận 5V |
| GND | GND | |
| BCK | GPIO tự chọn, ví dụ 4 | |
| LCK / LRCK | GPIO tự chọn, ví dụ 5 | |
| DIN | GPIO tự chọn, ví dụ 6 | |
| **SCK** | **GND** | ← **Chỗ giết người.** Không nối, DAC im lặng và bạn sẽ nghĩ nó hỏng. |

**Tránh các chân:** strapping (0, 3, 45, 46), USB (19, 20), và chân flash/PSRAM của board bạn mua. Tra pinout đúng biến thể DevKit.

Các chân jumper trên module (thường đã set sẵn, kiểm tra lại):

| Chân | Nối vào | Nghĩa |
|---|---|---|
| FMT | GND | Định dạng I2S chuẩn |
| XSMT | 3.3V (HIGH) | Unmute. LOW = câm. |
| FLT | GND | Bộ lọc bình thường |
| DEMP | GND | Tắt de-emphasis |

**Bước 4 — tiếng đầu tiên, chưa cần host.** Firmware tự sinh sine 440Hz, 24kHz, 16-bit, stereo, đẩy vào I2S. Cắm tai nghe vào line-out của DAC.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Log khởi động ESP-IDF | I2S channel tạo thành công, không lỗi |
| Line-out | Nghe tone 440Hz |
| Đo áp VCC của module lúc chạy | Đúng bằng áp bạn cấp, sai lệch <5% |
| Đo áp chân XSMT | ≥2.0V (mức HIGH) |
| `ethtool -T` hai cổng mini PC | Đã ghi vào `decisions.md` |

### Nếu ra khác

| Triệu chứng | Nguyên nhân nghi ngờ | Cách sửa |
|---|---|---|
| Hoàn toàn im lặng | **SCK chưa nối GND** | Nối SCK xuống GND. Đây là nguyên nhân số 1. |
| Im lặng, SCK đã nối | XSMT đang LOW | Kéo XSMT lên 3.3V |
| ESP32 không boot sau khi đấu dây | Dùng nhầm chân strapping | Đổi chân |
| Mất cổng USB sau khi nạp firmware | Dùng nhầm GPIO 19/20 | Đổi chân, giữ BOOT khi cắm để nạp lại |
| Có tiếng nhưng rè, méo | Sai FMT, dây quá dài, hoặc thiếu GND chắc | Kiểm FMT=GND, rút ngắn dây, thêm một dây GND thứ hai |
| Có tiếng ở một kênh | Sai layout stereo trong buffer | Sang Bài 3 đo bằng logic analyzer thay vì đoán |

**Nguyên tắc đã học ở Khóa 1, nhắc lại:** mua **2 cái** cho mọi module rẻ và quan trọng. Không có module thứ hai để so, bạn không phân biệt được "module chết" với "cấu hình sai", và sẽ mất nhiều ngày.

---

## Bài 3 — TN-1: Nhìn thấy âm thanh trên dây (5h)

**Câu hỏi:** với audio 24kHz, 16-bit, stereo, BCK và LRCK phải là bao nhiêu?

Đây là thí nghiệm bắt buộc số 1 và là tiêu chí PASS số 2 của M4.

### Khái niệm

I2S không nén, không đóng gói, không có header. Mỗi chu kỳ LRCK truyền đúng một frame. Trong mỗi nửa chu kỳ LRCK, BCK đánh nhịp đủ số bit của một sample.

Suy ra hai công thức bạn phải tự dẫn được, không phải nhớ:

```
LRCK (Hz) = sample_rate
BCK  (Hz) = sample_rate × bit_depth × channels
```

Nghĩa là **số BCK trong một chu kỳ LRCK = bit_depth × channels**. Đó là thứ bạn sẽ đếm bằng mắt trên màn hình.

### Làm

**Bước 1 — viết dự đoán, commit trước.** File `lab/05-i2s-playback/prediction.md`:

```markdown
## Cấu hình A: 24 kHz, 16-bit, stereo
LRCK = 24.000 Hz        → chu kỳ = 41,67 µs
BCK  = 24000×16×2 = 768.000 Hz → chu kỳ = 1,302 µs
Số cạnh BCK trong 1 chu kỳ LRCK = 32
Data rate = 768 kbit/s

## Cấu hình B: 48 kHz, 16-bit, stereo
LRCK = 48.000 Hz        → chu kỳ = 20,83 µs
BCK  = 1.536.000 Hz     → chu kỳ = 0,651 µs
Số cạnh BCK trong 1 chu kỳ LRCK = 32

## Giới hạn dụng cụ đo
Logic analyzer 24 MHz → độ phân giải thời gian 41,7 ns
Ở BCK 768 kHz: 24e6/768e3 ≈ 31 mẫu mỗi chu kỳ BCK → dư sức
Ở BCK 1,536 MHz: ≈ 15,6 mẫu mỗi chu kỳ → vẫn ổn
Ở BCK 3,072 MHz (48k/32-bit): ≈ 7,8 mẫu → SÁT GIỚI HẠN, decode có thể lỗi
```

Mục cuối cùng quan trọng: **biết giới hạn của dụng cụ đo cũng là một phần của việc đo.** Người phỏng vấn ở vị trí này nhìn vào mục đó đầu tiên.

**Bước 2 — cắm logic analyzer.**

| Kênh | Nối vào |
|---|---|
| **GND** | GND của mạch ← không được quên |
| D0 | BCK |
| D1 | LRCK |
| D2 | DIN |

**Bước 3 — capture.** PulseView, sample rate **24MHz**, số mẫu 1M (≈42ms — đủ cho ~1000 frame ở 24kHz). Bấm Run rồi phát tone.

**Bước 4 — decode.** Thêm decoder **I²S**: Clock = D0, Word select = D1, Data = D2.

**Bước 5 — đo tay, không tin decoder ngay.** Rê chuột đo khoảng cách giữa hai cạnh lên LRCK liên tiếp. Rồi hai cạnh lên BCK liên tiếp. Đếm bằng mắt số cạnh BCK trong một nửa chu kỳ LRCK.

**Bước 6 — lặp ở 48kHz.** Đổi cấu hình trong firmware, dự đoán lại, đo lại.

**Bước 7 — rồi phá nó.** Ba thí nghiệm phá, mỗi cái ghi lại hiện tượng:
- Đổi sang mono. LRCK có đổi không? DIN có đổi không?
- Nối chân FMT sang 3.3V (chế độ left-justified thay vì I2S). Decoder I2S của PulseView nói gì? Tai nghe thấy gì?
- Rút dây GND của logic analyzer. Nhìn waveform.

### Số phải ra

| Đại lượng | Cấu hình A (24k) | Cấu hình B (48k) | Sai số cho phép |
|---|---|---|---|
| Chu kỳ LRCK | 41,67 µs | 20,83 µs | **<1%** |
| Chu kỳ BCK | 1,302 µs | 0,651 µs | **<1%** |
| Cạnh BCK / chu kỳ LRCK | 32 | 32 | chính xác |
| Giá trị sample decode ra | Khớp với giá trị bạn ghi vào buffer | | |

Thí nghiệm phá phải cho ra:

| Phá gì | Hiện tượng đúng |
|---|---|
| Mono | LRCK vẫn chạy (phần cứng vẫn stereo), DIN lặp cùng dữ liệu ở cả hai nửa, hoặc nửa phải toàn 0 |
| FMT sai | Decoder ra giá trị vô nghĩa, dữ liệu lệch 1 bit. Tai nghe: méo nặng hoặc nhiễu trắng |
| Rút GND | Waveform nhiễu loạn, mức logic bập bênh, decode thất bại |

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| BCK đo được gấp đôi dự đoán | DAC chạy 32-bit frame thay vì 16 | Đếm lại cạnh BCK/LRCK. Nếu ra 64 thì frame là 32-bit — sửa dự đoán, đừng sửa phép đo |
| LRCK lệch vài phần trăm so với cấu hình | Bộ chia clock không ra đúng số nguyên — driver chọn tần số gần nhất | Ghi tần số thật vào lab notebook, dùng nó cho mọi tính toán. **Đây là clock drift**, chủ đề của Khóa 5 |
| Decoder I2S không ra gì | Gán nhầm kênh, hoặc sai polarity | Thử đảo Word select polarity trong tùy chọn decoder |
| Waveform trông giống răng cưa | Sample rate capture quá thấp | Tăng lên 24MHz |

**Ghi chú về "config nói dối":** sample rate bạn ghi trong code là thứ bạn *xin*, không phải thứ phần cứng *chạy*. Clock I2S được chia từ một PLL; nếu tỉ lệ chia không chẵn, driver chọn giá trị gần nhất mà không báo lỗi. Logic analyzer là trọng tài. Thói quen này đi theo bạn tới mọi driver sau này — ALSA `plughw` resample ngầm cũng là cùng một loại nói dối.

### Tự kiểm tra

1. *Nếu đếm được 64 cạnh BCK trong một chu kỳ LRCK ở stereo, bit depth là bao nhiêu?* → 32-bit
2. *BCK 3.072 MHz tương ứng cấu hình nào?* → 48kHz × 32 bit × 2 kênh
3. *Vì sao logic analyzer 24MHz vẫn đọc được BCK 768kHz mà không vi phạm Nyquist?* → Nyquist đòi >2× cho tín hiệu tương tự. Với tín hiệu số ta cần đủ mẫu để xác định vị trí cạnh, thực tế cần 4–10×. 24/0,768 ≈ 31× nên rất an toàn.

---

## Bài 4 — DMA buffer, ring buffer, underrun: từ dưới lên (6h)

**Câu hỏi:** độ trễ audio nằm ở đâu, và ai quyết định nó?

### Khái niệm

Đây là bài nối trực tiếp 8 năm backend của bạn vào thế giới vật lý, nên đọc chậm.

Dữ liệu đi qua **ba vùng đệm** trước khi thành tín hiệu trên dây:

```
[ring buffer host] ──USB-CDC──► [ring buffer ESP32] ──► [I2S DMA buffer] ──► dây I2S
   Python/Rust                    FreeRTOS task           phần cứng đọc thẳng
```

Vùng cuối là vùng quyết định. Driver I2S của ESP-IDF có hai tham số — chúng là **đúng cặp period/buffer của ALSA**, chỉ khác tên:

| ESP-IDF | Tương đương ALSA | Là gì | Tương tự backend |
|---|---|---|---|
| **`dma_frame_num`** | period_size | Số frame mỗi descriptor DMA — phần cứng đọc hết một descriptor rồi báo "cần thêm" | Batch size |
| **`dma_desc_num`** | periods | Số descriptor xoay vòng | Độ sâu queue |

**Độ trễ tối đa do DMA buffer gây ra:**

```
latency_dma (giây) = dma_desc_num × dma_frame_num / sample_rate
```

Ở 24kHz: 3 × 1600 = 4800 frame → 200ms. 3 × 400 → 50ms. 3 × 80 → 10ms.

**Underrun** xảy ra khi phần cứng đòi dữ liệu mà không ai nạp kịp. Driver sẽ phát lại descriptor cũ hoặc phát số 0 (tùy cấu hình `auto_clear`). Failure mode là **một tiếng "tách" nghe được bằng tai** — không phải một dòng log. Đây chính là đường cong bạn đã tối ưu ở tầng API cả sự nghiệp, chỉ đổi đơn vị đo của sự cố.

**Backpressure qua USB.** USB-CDC full-speed thừa băng thông cho 96 KB/s, nhưng nó **không phải thời gian thực**: host có scheduler, USB có polling. Thiết kế giao thức tối thiểu: mỗi gói có **số thứ tự** và **độ dài**; ESP32 định kỳ báo **còn trống bao nhiêu byte** (credit-based flow control). Host chỉ gửi khi có credit. Bạn đã làm thứ này ở tầng message queue — giờ làm trên một sợi cáp USB.

### Làm

**Bước 1 — firmware.** Task nhận USB → ghi vào ring buffer ESP32 (ví dụ `xRingbuffer` của FreeRTOS). Task phát → đọc ring buffer → `i2s_channel_write`. Cấu hình **tường minh** `dma_desc_num`, `dma_frame_num`, sample rate, bit width.

**Bước 2 — đếm underrun bằng chính code của bạn**, không chỉ tin driver: mỗi lần task phát thấy ring buffer rỗng, tăng một bộ đếm và gửi lên host. ESP-IDF cũng có callback sự kiện cho I2S (kiểm `i2s_event_callbacks_t` trong đúng phiên bản docs bạn dùng) — dùng làm nguồn thứ hai để kiểm chéo.

**Bước 3 — host streamer.** Python (`pyserial`) hoặc Rust. Đọc file PCM raw, đóng gói, gửi theo credit. **Đọc lại** cấu hình thật từ ESP32 (firmware trả về khi khởi động) và in ra. Thói quen chung: đừng tin thứ mình set, hãy đọc lại thứ thiết bị chấp nhận.

**Bước 4 — cố tình gây underrun.** Chèn `time.sleep()` vào vòng gửi của host. Nghe. Đếm.

**Bước 5 (tùy chọn, 3h, không thuộc gate) — chạm ALSA thật.** Nếu muốn có cả từ vựng ALSA cho phỏng vấn: trên mini PC, `sudo modprobe snd-aloop`, viết player nhỏ bằng `pyalsaaudio` mở `hw:Loopback`, set period/buffer, đọc lại giá trị thật, đếm XRUN khi cố tình ngủ. 3 giờ là đủ để biết `snd_pcm_hw_params` trông thế nào.

### Số phải ra

| Cấu hình (24kHz stereo, `dma_desc_num`=3) | DMA buffer | Độ trễ lý thuyết | Hiện tượng |
|---|---|---|---|
| `dma_frame_num` = 1600 | 4800 frame | 200 ms | Rất ổn định, không underrun |
| 800 | 2400 | 100 ms | Ổn định |
| 400 | 1200 | 50 ms | Ổn định nếu ring buffer ESP32 đủ lớn |
| 160 | 480 | 20 ms | Bắt đầu nhạy với jitter USB/host |
| 80 | 240 | 10 ms | Underrun khi host có tải |

**Lưu ý giới hạn phần cứng:** mỗi descriptor DMA của ESP32 có kích thước tối đa (cỡ 4092 byte); driver có thể ép `dma_frame_num` về giá trị khác. **Giá trị bạn xin phải bằng giá trị đọc lại** — nếu không, mọi tính toán độ trễ của bạn sai.

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Underrun liên tục ngay cả với buffer lớn | Ring buffer ESP32 quá nhỏ, hoặc flow control sai | Đo mức đầy của ring buffer theo thời gian, gửi lên host |
| Không nghe thấy gì nhưng không lỗi | Sai bit width (16 vs 32) hoặc sai layout stereo | Đo bằng logic analyzer (Bài 3) |
| Độ trễ đo được gấp đôi tính toán | Nhầm **frame** với **sample** | Xem lại Bài 1: 1 frame stereo = 2 sample = 4 byte |
| Gói USB đến sai thứ tự hoặc mất | Bug giao thức — USB-CDC không mất gói, nhưng code của bạn có thể | Kiểm số thứ tự ở ESP32, đếm lỗ hổng |

### Tự kiểm tra

1. *DMA buffer 3 × 341 frame ở 48kHz gây trễ bao nhiêu?* → 1023/48000 ≈ 21,3 ms
2. *Vì sao giảm `dma_frame_num` lại làm CPU ESP32 bận hơn?* → Mỗi descriptor xong là một ngắt và một lần đánh thức task. Descriptor nhỏ = nhiều ngắt/giây.
3. *Vì sao cần ring buffer ở ESP32 khi đã có DMA buffer?* → DMA buffer phải nhỏ để độ trễ thấp; ring buffer hấp thụ jitter của chặng USB/host. Hai vùng đệm tách hai mục tiêu — đúng như tách queue và batch ở backend.

---

## Bài 5 — DAC → amp → loa: trở kháng và công suất (4h)

**Câu hỏi:** vì sao không nối thẳng loa vào DAC?

### Khái niệm

**Line-out của DAC** xuất tín hiệu điện áp nhỏ (~1–2 V_rms) với dòng rất hạn chế. Nó thiết kế để lái **tải trở kháng cao** — đầu vào của một amplifier khác (hàng chục kΩ).

**Loa 4Ω** là tải trở kháng **thấp**. Nối thẳng vào DAC: DAC không đủ dòng, tín hiệu sụp, và có thể làm chết DAC. Đây là một trong những bẫy đã ghi rõ trong lộ trình.

**Amplifier class-D** đứng giữa: nhận tín hiệu áp nhỏ, dùng nguồn riêng, xuất ra dòng lớn đủ lái cuộn dây loa.

**Trở kháng ≠ điện trở.** "4Ω" ghi trên loa là trở kháng danh định ở tần số nào đó. Nếu bạn đo điện trở DC bằng multimeter, số sẽ **nhỏ hơn** — thường 3.0–3.4Ω cho loa 4Ω. Đó không phải loa hỏng, đó là hai đại lượng khác nhau. Nhiều người mới tưởng đo sai.

**Công suất:**

```
P = V_rms² / R
```

Loa 4Ω cần 3W → `V_rms = √(3 × 4) = 3,46 V`.

### Làm

1. Đấu chuỗi đầy đủ: ESP32-S3 → PCM5102A → line-out → PAM8403/TPA3110 → loa 4Ω. Amp dùng **nguồn riêng**, nhưng **chung GND** với ESP32.
2. Đo điện trở DC của loa bằng multimeter (loa tháo rời khỏi mạch). Ghi lại.
3. Phát tone sin 100Hz. Đặt multimeter ở chế độ **V AC**, đo trên hai đầu loa.
4. Tính `P = V²/R`. So với công suất công bố của amp.
5. Tăng âm lượng dần, đo lại ở 3 mức. Lập bảng.
6. **Chạm nhẹ tay vào màng loa trong lúc phát tone 100Hz.** Cảm nhận rung.

### Số phải ra

| Kiểm tra | Giá trị đúng |
|---|---|
| Điện trở DC của loa 4Ω | 3,0–3,4 Ω |
| V_AC trên loa ở mức trung bình | 1–2 V_rms |
| V_AC ở mức gần tối đa (PAM8403, nguồn 5V) | 2,5–3,5 V_rms |
| Công suất tính ra ở mức tối đa | 1,5–3 W — **phải nhỏ hơn** công suất công bố |

Nếu công suất tính ra **lớn hơn** công bố, hoặc bạn đo sai, hoặc amp đang clip (méo), hoặc thông số công bố là thổi phồng — cả ba đều đáng ghi vào lab notebook.

**Bước 6 là bước quan trọng nhất của cả bài.** Bạn vừa đi hết chuỗi: số nguyên → điện áp → dòng qua cuộn dây → lực từ → chuyển động màng loa → áp suất không khí → rung dưới ngón tay. Ghi cảm nhận đó vào lab notebook. Nghe có vẻ ủy mị, nhưng nó là thời điểm trừu tượng biến thành vật lý, và nó đáng được ghi lại.

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| V_AC đo được rất nhỏ và tiếng yếu | Chưa qua amp, hoặc amp chưa có nguồn | Kiểm nguồn amp, kiểm chiều tín hiệu |
| Tiếng méo ở mọi mức âm lượng | Line-out vào amp bị quá biên, hoặc thiếu GND chung | Giảm gain, kiểm GND |
| Đo V AC ra số nhảy loạn | Multimeter rẻ đo AC không chính xác ở dạng sóng phức tạp | Dùng tone sin thuần, không dùng nhạc. Ghi rõ giới hạn này vào phần "sai số của phép đo". |
| Amp nóng nhanh | Sai trở kháng loa, hoặc đang clip liên tục | Kiểm trở kháng loa, giảm âm lượng |

---

## Bài 6 — TN-3: Cố tình làm hỏng nó bằng nguồn (5h)

**Câu hỏi:** điều gì xảy ra khi amp và vi điều khiển tranh nhau một nguồn?

Đây là thí nghiệm bắt buộc số 3 và là tiêu chí PASS số 4 của M4. Nó cũng là bài học sẽ cứu bạn ba ngày debug ở Khóa 7, khi motor làm ESP32 reset.

### Khái niệm

Amplifier tiêu thụ dòng **theo nhịp nhạc**, không đều. Một đoạn bass mạnh có thể kéo dòng gấp nhiều lần lúc nghỉ. Nếu amp lấy dòng từ chính rail 5V của DevKit — tức là từ **cổng USB của mini PC** — dòng vọt đó gặp hai giới hạn: cổng USB chỉ cấp được ~500–900mA, và dây USB có điện trở. Rail sụt, và ESP32 phản ứng.

ESP32 có **brownout detector** phần cứng: khi áp dưới ngưỡng, chip tự reset. Sau khi khởi động lại, firmware đọc được lý do:

```c
esp_reset_reason_t r = esp_reset_reason();   // ESP_RST_BROWNOUT nếu do sụt áp
```

Ghi lý do reset vào một bộ đếm trong NVS và gửi lên host mỗi lần khởi động. Đó là "cờ nhớ sự kiện đã qua" của bạn — bằng chứng cho điều mà tai chỉ nghe thấy mơ hồ.

Phía host cũng có dấu vết: `dmesg` sẽ ghi lại cổng USB bị ngắt rồi kết nối lại.

### Làm

Bốn cấu hình, mỗi cấu hình chạy cùng một đoạn audio có bass mạnh ở âm lượng tối đa:

**Cấu hình 1 — tệ nhất, cố tình.** Amp lấy 5V từ chân 5V của DevKit (nguồn USB từ mini PC).
**Cấu hình 2 — tháo GND chung** giữa DAC và amp (giữ nguyên nguồn chung). Nghe. Đo. *Rồi nối lại ngay.*
**Cấu hình 3 — nguồn riêng cho amp**, giữ common ground.
**Cấu hình 4 — như 3, thêm tụ 470µF–1000µF sát chân nguồn amp.**

Với mỗi cấu hình, ghi:
- V rail 5V lúc **nghỉ** (multimeter tại chân nguồn của amp)
- V rail lúc **đang phát bass mạnh**
- Số lần brownout reset của ESP32 sau 2 phút phát
- Số lần USB ngắt/kết nối lại trong `dmesg`
- Mô tả tiếng bằng lời

**Trước khi làm: viết dự đoán.** Rail sụt bao nhiêu ở cấu hình 1? Commit trước.

### Số phải ra

| Cấu hình | V rail nghỉ | V rail lúc phát | Brownout / USB reset | Tiếng |
|---|---|---|---|---|
| 1 — chung nguồn USB | ~4.9–5.0V | Sụt rõ rệt, thường 4.5–4.8V hoặc thấp hơn | Khả năng cao **≥1** | Méo theo nhịp bass, lạo xạo, có thể mất tiếng hẳn |
| 2 — mất GND chung | — | — | — | Ù, nhiễu, hoặc im hẳn |
| 3 — nguồn riêng | ~5.0V | Sụt rất ít, <0.1V | 0 | Sạch |
| 4 — thêm tụ | ~5.0V | Sụt ít hơn nữa | 0 | Sạch, bass chắc hơn |

Nếu cấu hình 1 **không** gây sụt áp đáng kể, tăng âm lượng, dùng loa trở kháng thấp hơn, cắm qua USB hub không cấp nguồn, hoặc dùng dây USB dài mỏng. Thí nghiệm chỉ có giá trị khi bạn **thực sự tạo được lỗi**, rồi sửa nó.

### Nếu ra khác

| Triệu chứng | Ý nghĩa |
|---|---|
| ESP32 reset liên tục, lý do `ESP_RST_BROWNOUT` | Chính xác là thứ bạn đang cố tạo ra |
| Không tạo được sụt áp ở cấu hình 1 | Cổng USB quá khỏe hoặc amp quá nhỏ. Vẫn ghi lại — "không tái hiện được" cũng là kết quả, nhưng ghi rõ điều kiện |
| Mini PC báo lỗi cổng USB (over-current) | Thí nghiệm thành công quá mức. Chụp `dmesg`, chuyển ngay sang cấu hình 3 |

**Bài học để mang đi:** bạn vừa tự tay tạo lỗi rồi tự tay sửa. Ở Khóa 7, khi ESP32 reset lúc motor quay, bạn sẽ nhận ra triệu chứng trong 30 giây thay vì mất ba ngày nghi ngờ code.

---

## Bài 7 — TN-4: Từ không khí thành số nguyên, và ngược lại (7h)

**Câu hỏi:** giọng của chính bạn, bằng số, là cái gì?

Thí nghiệm bắt buộc số 4, tiêu chí PASS số 5 của M4.

### Khái niệm

INMP441 là mic MEMS có **I2S đầu ra** — nó tự chuyển đổi sang số bên trong, nên bạn nhận thẳng PCM, không cần ADC ngoài. Nó xuất 24-bit dữ liệu trong khung 32-bit (xem lại câu hỏi tự kiểm tra Bài 1 — giờ bạn sẽ nhìn thấy nó thật trên logic analyzer).

**F0 (fundamental frequency)** là tần số rung cơ bản của dây thanh quản. Đây là một thông số vật lý của chính cơ thể bạn:

| Nhóm | F0 điển hình |
|---|---|
| Nam trưởng thành | 85–180 Hz |
| Nữ trưởng thành | 165–255 Hz |

**Clipping** xảy ra khi tín hiệu vượt quá giá trị lớn nhất biểu diễn được. Waveform bị cắt phẳng đầu, và trong miền tần số xuất hiện **hài bậc cao** không có trong tín hiệu gốc. Đây là lý do âm thanh clip nghe "rè" chứ không chỉ "to".

### Làm

**7a — Ghi giọng mình.**
1. Đấu INMP441 vào **bộ I2S thứ hai** của ESP32-S3 (chip có hai bộ I2S, nên phát và ghi chạy đồng thời được): VDD 3.3V, GND, SD/SCK/WS vào ba GPIO tự chọn, L/R→GND (chọn kênh trái). Stream PCM ghi được lên mini PC qua USB để phân tích bằng Python.
2. Ghi 3 giây "aaaaa" giọng đều, 24kHz, lưu raw PCM.
3. Vẽ waveform. Vẽ FFT. Tìm đỉnh tần số thấp nhất có năng lượng đáng kể — đó là F0 của bạn.
4. **Ghi con số đó vào `decisions.md`.** Đó là một hằng số vật lý của chính bạn.

**7b — So giọng thật với giọng máy.**
1. Cho TTS đọc đúng câu bạn vừa nói (Module 3 sẽ dựng TTS; nếu chưa có, dùng tạm bất kỳ TTS offline nào).
2. Ghi lại bằng **chính mic đó, chính vị trí đó**.
3. FFT cả hai. Đặt chồng lên nhau.
4. Đo khoảng cách: F0 lệch bao nhiêu? Phân bố năng lượng theo dải tần khác nhau chỗ nào?

Đây là **đường cơ sở (baseline) trước khi V2 bắt đầu**. Sau này khi fine-tune giọng mình, bạn có số để so trước-sau.

**7c — Clipping.**
1. Ghi âm rất gần mic, nói to, đến mức waveform bị cắt phẳng.
2. Vẽ waveform — nhìn thấy đỉnh phẳng.
3. Vẽ FFT — nhìn thấy hài bậc cao xuất hiện, thứ không có ở bản ghi bình thường.

**7d — Giảm bit depth và đo SNR.**
1. Lấy bản ghi sạch 16-bit. Giảm xuống 12, 8, 4 bit bằng cách dịch bit (`x >> (16-n) << (16-n)`).
2. Nghe từng mức.
3. Với mỗi mức, đo **noise floor** trên phổ (mức năng lượng trung bình ở vùng không có tín hiệu) và tính SNR đo được.
4. Vẽ đồ thị: SNR đo được vs `6.02 × bits + 1.76`.

**7e — Đi hết chuỗi ngược lại.** Đã làm ở Bài 5 (đo V AC trên loa, tính công suất, chạm màng loa).

### Số phải ra

| Kiểm tra | Giá trị đúng |
|---|---|
| F0 giọng bạn | Nằm trong dải của nhóm, và **ổn định** giữa các lần ghi (lệch <10%) |
| Khung I2S của INMP441 trên logic analyzer | 32 bit mỗi kênh, trong đó 24 bit có nghĩa |
| SNR ở 16-bit | Gần 98 dB nếu ghi sạch — thực tế thường thấp hơn nhiều vì nhiễu môi trường và nhiễu của chính mic |
| SNR đo vs lý thuyết, 4 mức bit depth | Sai lệch **<3 dB** ← tiêu chí PASS |
| Sau clipping | Hài bậc cao rõ ràng ở bội số của F0 |

**Lưu ý quan trọng về SNR ở 16-bit:** đừng ngạc nhiên nếu đo ra 50–60 dB thay vì 98 dB. Giới hạn thực tế không phải bit depth mà là nhiễu của chính mic và của phòng. Bit depth chỉ là *trần lý thuyết*. Điều bạn cần chứng minh là **quan hệ tuyến tính** giữa số bit và SNR khi bit depth trở thành yếu tố giới hạn — tức là ở 8 và 4 bit. Ghi rõ điều này trong phần giải thích, vì nó cho thấy bạn hiểu phép đo chứ không chỉ chạy công thức.

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Mic ghi ra toàn 0 | L/R chưa nối, hoặc sai kênh | Nối L/R→GND, thử đọc kênh trái |
| Giá trị sample rất nhỏ | Đang đọc 24-bit như 32-bit mà không dịch bit | Dịch phải 8 bit, hoặc đọc đúng vị trí bit có nghĩa |
| FFT không có đỉnh rõ | Nói không đủ đều, hoặc cửa sổ FFT quá ngắn | Nói "aaaaa" giữ đều 2 giây, dùng cửa sổ ≥4096 mẫu |
| SNR đo lệch >3dB ở mọi mức | Đang đo noise floor ở vùng vẫn có tín hiệu | Chọn vùng im lặng thật trong bản ghi để đo noise floor |
| Phát và ghi cùng lúc bị nhiễu nhau | Dùng chung một bộ I2S, hoặc dây hai bộ quá sát nhau | Tách hai bộ I2S (I2S0 phát, I2S1 ghi), tách dây, chung GND |

### Tự kiểm tra

1. *SNR lý thuyết của 20-bit?* → 6.02 × 20 + 1.76 = 122 dB
2. *Vì sao clipping tạo ra hài bậc cao?* → Cắt phẳng đỉnh làm sóng sin biến dạng về phía sóng vuông; sóng vuông có phổ chứa hài bậc lẻ.
3. *Giọng bạn F0 = 120Hz, hài bậc 3 ở đâu?* → 360Hz

---

# MODULE 2 — ĐO ĐỘ TRỄ THẬT (16h)

Đây là module có giá trị nghề nghiệp cao nhất trong cả Khóa 3. Nó lấy đúng kỹ năng bạn đã có — latency budget, p99, đánh đổi độ trễ vs độ tin cậy — và đặt nó vào một hệ có tầng vật lý. Trong phỏng vấn robotics, đây là phần bạn kể.

---

## Bài 8 — Latency budget: dự đoán trước (3h)

**Câu hỏi:** từ lúc ai đó bấm Submit tới lúc âm thanh chạm tai, mất bao lâu, và mất ở đâu?

### Khái niệm

Bạn đã làm việc này hàng trăm lần ở tầng API. Khác biệt duy nhất: có hai chặng bạn **không kiểm soát được** và một chặng **là vật lý thuần túy**.

### Làm

Điền bảng này bằng **dự đoán**, commit, trước khi đo bất cứ thứ gì:

| Chặng | Dự đoán của bạn | Kiểm soát được? | Cách sẽ đo |
|---|---|---|---|
| Submit form → Sheet có dữ liệu | | Không | Timestamp trong Sheet vs đồng hồ |
| Phát hiện record mới | | Có | Log của ingest |
| TTS sinh audio | | Có | RTF × độ dài (Module 3) |
| Host → ESP32 qua USB | | Có | Round-trip/2 (Bài 9) |
| Ring buffer ESP32 | | Có | mức đầy / rate |
| I2S DMA buffer | | **Có — bài học chính** | desc_num × frame_num / rate |
| DAC + amp + loa | | Không | Đo ở Bài 9 |
| Âm thanh truyền trong không khí | | Không | khoảng cách / 343 m/s |

Chặng cuối: tốc độ âm thanh ~343 m/s ở 20°C. 1m = 2,92ms. Mic đặt cách loa 30cm = 0,87ms. Con số này nhỏ nhưng **phải trừ ra** khi đo ở Bài 9, nếu không bạn đang tính thời gian truyền trong không khí vào độ trễ phần mềm.

### Số phải ra

Không có số đúng ở bài này — chỉ có **dự đoán được commit trước**. Giá trị của bài nằm ở chỗ so sánh dự đoán với thực tế ở Bài 9 và 10.

Nhưng có một dự đoán tôi muốn bạn viết ra và ký tên: **bạn nghĩ nút thắt nằm ở đâu?** Ghi vào `prediction.md`. Phần lớn người có nền backend sẽ đoán là TTS hoặc DMA buffer. Kết quả thật thường làm họ ngạc nhiên.

---

## Bài 9 — TN-2: Đo độ trễ từ phần mềm ra không khí (7h)

**Câu hỏi:** giữa dòng code ghi sample đầu tiên và sóng âm chạm mic, có bao nhiêu mili-giây?

Thí nghiệm bắt buộc số 2 — lộ trình gọi nó là **quan trọng nhất trong năm cái**. Tiêu chí PASS số 3 của M4 đòi độ phân giải ≤1ms.

### Khái niệm

Vấn đề: bạn cần so **một sự kiện phần mềm** với **một sự kiện vật lý** trên cùng một trục thời gian. Đây chính xác là bài toán đồng bộ mà Khóa 5 sẽ làm ở quy mô lớn — làm nhỏ trước ở đây.

Giải pháp: dùng một chân GPIO **trên ESP32** làm cầu nối. Kéo GPIO lên HIGH tại **đúng dòng code** ghi sample đầu tiên vào I2S DMA. Chân đó và tín hiệu mic cùng được logic analyzer ghi lại → cùng một trục thời gian, cùng một đồng hồ.

Có **hai độ trễ** phải tách, vì kiến trúc có hai chặng:

| Độ trễ | Từ | Tới | Đo bằng |
|---|---|---|---|
| **Chặng host** | Host gửi gói đầu tiên | ESP32 nhận gói đó | Host gửi kèm timestamp monotonic; ESP32 echo lại ngay; đo round-trip, chia đôi, **ghi rõ đây là ước lượng** |
| **Chặng vật lý** | ESP32 ghi sample đầu vào DMA (GPIO lên) | Sóng âm tới mic | Logic analyzer — đây là phép đo chính |

### Làm

**Phương pháp chính — logic analyzer 4 kênh:**

| Kênh | Nối vào |
|---|---|
| GND | GND |
| D0 | GPIO đánh dấu (từ firmware phát) |
| D1 | BCK của **mic** INMP441 |
| D2 | LRCK của mic |
| D3 | SD (data) của mic |

**Bước 1 — sửa firmware.** Ngay trước lệnh `i2s_channel_write` đầu tiên, kéo GPIO lên HIGH bằng `gpio_set_level` (hoặc ghi thẳng thanh ghi GPIO để nhanh hơn). Đo thời gian của chính lệnh toggle — trên MCU nó cỡ sub-µs, nhỏ hơn nhiều so với GPIO từ userspace Linux. Ghi vào phần "sai số của phép đo". Đây là một lý do nữa việc tách MCU là đúng.

**Bước 2 — đặt mic.** Cách loa **chính xác 30cm**, đo bằng thước. Ghi khoảng cách vào setup.md.

**Bước 3 — capture.** PulseView. Buffer 1M mẫu ở 24MHz chỉ được ~42ms — có thể không đủ nếu độ trễ lớn. Giảm xuống 8MHz để kéo dài thời gian capture (BCK mic 1.536MHz → ~5 mẫu/chu kỳ, đủ cho decode). Ghi rõ đánh đổi này vào lab notebook.

**Bước 4 — phát và bắt.** Audio test bắt đầu bằng **xung dốc đứng** (click, hoặc burst tone) chứ không phải fade-in.

**Bước 5 — đo.** Decode I2S của mic, export giá trị sample. Tìm sample đầu tiên vượt ngưỡng năng lượng. Khoảng cách từ cạnh lên GPIO tới sample đó = độ trễ chặng vật lý.

**Bước 6 — trừ phần không khí.** `latency_dma_dac_amp = latency_đo − 0,87ms`

**Phương pháp dự phòng — không cần logic analyzer:** mic INMP441 cắm vào **bộ I2S thứ hai** của chính ESP32-S3 (chip có hai bộ I2S). Phát và ghi dùng **cùng một timer phần cứng**: ghi timestamp tại lúc ghi sample phát đầu tiên và tại lúc nhận từng frame mic; tìm onset. Độ phân giải = 1 chu kỳ LRCK = 41,7µs ở 24kHz. Đủ đạt tiêu chí ≤1ms, và dùng làm kiểm chéo cho phương pháp chính.

### Số phải ra

| Đại lượng | Giá trị kỳ vọng |
|---|---|
| Độ trễ chặng vật lý (DMA 200ms) | Xấp xỉ 200ms + vài ms |
| Độ trễ chặng vật lý (DMA 50ms) | Xấp xỉ 50ms + vài ms |
| Phần dư sau khi trừ DMA và không khí | 1–5ms — đây là DAC + amp + loa |
| Chặng host (ước lượng round-trip/2) | Vài ms, **có đuôi** — ghi phân bố, không ghi một con số |
| Độ phân giải phép đo chặng vật lý | ≤1ms ← tiêu chí PASS |

**Kiểm tra chéo bắt buộc:** độ trễ chặng vật lý phải **thay đổi gần như tuyến tính** khi bạn đổi kích thước DMA buffer. Nếu không đổi, bạn đang đo nhầm — GPIO toggle không nằm đúng chỗ, hoặc có vùng đệm ẩn bạn chưa biết.

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Độ trễ nhỏ hơn kích thước DMA / rate | GPIO toggle đặt sau khi DMA đã được nạp mồi | Đặt toggle trước lệnh write đầu tiên tuyệt đối |
| Độ trễ lớn hơn dự đoán rất nhiều | Driver đã ép `dma_frame_num` khác giá trị bạn xin | Đọc lại cấu hình thật (Bài 4) |
| Không tìm được onset trong tín hiệu mic | Audio test fade-in quá chậm | Đổi sang click hoặc burst |
| Kết quả nhảy loạn giữa các lần | Chưa cố định vị trí mic, hoặc nhiễu phòng | Cố định mic bằng giá, đo trong phòng yên, lặp 10 lần lấy trung vị và độ lệch chuẩn |

**Lặp ít nhất 10 lần và báo cáo trung vị + độ lệch chuẩn, không phải một con số.** Một phép đo đơn lẻ không phải dữ liệu.

---

## Bài 10 — Đường cong độ trễ vs underrun (6h)

**Câu hỏi:** đánh đổi giữa độ trễ và độ tin cậy, bằng số, trông như thế nào?

Tiêu chí PASS số 3 của M4 đòi: ≥5 điểm kích thước DMA buffer, mỗi điểm ≥10 phút chạy.

### Khái niệm

Bạn đã vẽ đường cong này ở tầng API cả sự nghiệp. Ở đây trục X là `dma_frame_num`, trục Y là độ trễ đo được và tỉ lệ underrun. Điểm khác duy nhất: failure mode là một tiếng "tách" nghe được bằng tai thay vì một dòng log.

Và có **hai nguồn tải** khác nhau, mỗi nguồn đánh vào một chặng:

| Tải | Đánh vào | Mô phỏng tình huống thật |
|---|---|---|
| CPU host (`stress-ng --cpu 4` trên mini PC) | Chặng host → USB | Mini PC vừa chạy TTS, ingest, logging |
| CPU ESP32 (task WiFi gửi log liên tục) | Task nạp DMA | MCU vừa phát audio vừa làm việc khác — đúng điều sẽ xảy ra ở Khóa 7 |

### Làm

1. Chọn 5 giá trị `dma_frame_num`, cách nhau theo cấp số nhân. Gợi ý ở 24kHz: 80, 160, 320, 640, 1280 frame. Giữ `dma_desc_num` cố định (ví dụ 3).
2. **Đọc lại giá trị thực tế** driver chấp nhận cho từng mức.
3. Với mỗi điểm: phát liên tục **≥10 phút**, đếm underrun, đo độ trễ bằng phương pháp Bài 9.
4. Chạy lại với **tải host**, rồi với **tải ESP32**. Ba kịch bản.
5. Vẽ: độ trễ vs `dma_frame_num`, và underrun/giờ vs `dma_frame_num`. Ba kịch bản chồng lên nhau.
6. **Chọn điểm vận hành cho V1 và viết lý do vào `decisions.md`.**

### Số phải ra

| `dma_frame_num` (24kHz, desc=3) | DMA buffer | Độ trễ lý thuyết | Underrun (nhàn) | Underrun (có tải) |
|---|---|---|---|---|
| 80 | 240 | 10 ms | Thỉnh thoảng | Nhiều |
| 160 | 480 | 20 ms | Hiếm | Thỉnh thoảng |
| 320 | 960 | 40 ms | ~0 | Hiếm |
| 640 | 1920 | 80 ms | 0 | ~0 |
| 1280 | 3840 | 160 ms | 0 | 0 |

Hình dạng quan trọng hơn giá trị tuyệt đối: **underrun phải tăng mạnh khi buffer giảm dưới một ngưỡng**, và ngưỡng đó **dịch sang phải khi có tải**. Quan sát thêm: tải host và tải ESP32 có dịch ngưỡng **như nhau** không? Nếu ring buffer ESP32 đủ lớn, tải host gần như không ảnh hưởng — đó là bằng chứng bằng số rằng vùng đệm trung gian làm đúng việc của nó.

### Nếu ra khác

| Triệu chứng | Ý nghĩa |
|---|---|
| Underrun = 0 ở mọi mức, kể cả 80 | Chưa đủ tải. Giảm xuống 40, tăng tải ESP32, hoặc chạy TTS đồng thời trên host |
| Underrun cao ở mọi mức | Ring buffer ESP32 quá nhỏ, flow control sai, hoặc task phát có priority quá thấp |
| Độ trễ không giảm khi buffer giảm | Nút thắt nằm ở nơi khác — có thể ở ring buffer hoặc ở chính TTS |

### Cái phải viết ra sau bài này

Một đoạn ngắn trong `decisions.md`, đúng dạng bạn sẽ viết lại nhiều lần trong sự nghiệp robotics:

> **Quyết định:** `dma_frame_num` = X, `dma_desc_num` = Y, độ trễ DMA = Z ms, ring buffer ESP32 = W ms.
> **Lý do:** ở tải dự kiến của V1, điểm này cho underrun < N lần/giờ trong khi giữ độ trễ dưới ngưỡng chấp nhận được. Điểm thấp hơn tiếp theo (X/2) cho underrun gấp M lần với tải tương đương.
> **Số đo:** [link tới lab/NN]

---

# MODULE 3 — TTS VÀ QUYẾT ĐỊNH KIẾN TRÚC (14h)

---

## Bài 11 — RTF: chỉ số quyết định kiến trúc (3h)

**Câu hỏi:** "máy yếu quá" có phải một lý do không?

### Khái niệm

Không. "Máy yếu quá" là cảm giác. **RTF là lý do.**

```
RTF = thời_gian_sinh_audio / độ_dài_audio_sinh_ra
```

RTF = 0,5 nghĩa là sinh 10 giây audio mất 5 giây — nhanh gấp đôi thời gian thực. RTF = 2,0 nghĩa là mất 20 giây để sinh 10 giây audio — không thể chạy real-time.

**Ngưỡng:** RTF < 1 là điều kiện cần để streaming. Nhưng RTF = 0,95 vẫn nguy hiểm vì không còn biên an toàn khi có tải. Thực tế nên nhắm RTF ≤ 0,5.

Đây là quyết định kiến trúc số 1 trong bốn quyết định bạn phải tự bảo vệ được: **TTS stream trực tiếp trên CPU N100, hay phải pre-render**. Có model chạy real-time thật trên CPU — VieNeu-TTS được thiết kế cho inference real-time trên CPU ở 24kHz. Đo RTF rồi mới quyết.

Nói cách khác: **bạn có thể phát hiện ra kế hoạch của mình sai, và đó là kết quả tốt.** Phát hiện bằng số đo ở tuần thứ 8 rẻ hơn nhiều so với phát hiện bằng trực giác ở tuần thứ 30.

### Làm

Viết một harness benchmark tái sử dụng được (đây là code bạn sẽ dùng lại ở Khóa 4):

- Đầu vào: danh sách câu tiếng Việt có độ dài khác nhau (ngắn 5 từ, trung bình 20 từ, dài 50 từ)
- Với mỗi câu: chạy N=20 lần, bỏ 3 lần đầu (warm-up)
- Ghi: thời gian sinh, độ dài audio, RTF, **và time-to-first-chunk nếu model hỗ trợ streaming**
- Báo cáo p50, p95, p99 — không phải trung bình
- Ghi: CPU model, số core, RAM, nhiệt độ trước và sau

---

## Bài 12 — Chạy TTS tiếng Việt và đo RTF (6h)

**Câu hỏi:** TTS nên chạy ở đâu — CPU mini PC, hay phải pre-render?

### Khái niệm

**Đừng train from scratch.** Đã có sẵn nhiều lựa chọn tiếng Việt:

| Model | Đặc điểm | Lưu ý |
|---|---|---|
| **VietTTS** (dangvansam) | Server API tương thích định dạng OpenAI, clone giọng từ file audio local, cài qua pip hoặc Docker | Dễ tích hợp nhất cho V1 |
| **VieNeu-TTS** | Hướng on-device, inference real-time trên CPU ở 24kHz | **Ứng viên số 1 cho CPU N100** |
| **Viterbox** | Fine-tune từ Chatterbox, zero-shot clone với 3–10 giây mẫu, huấn luyện trên >3.000h dữ liệu tiếng Việt | **License CC BY-NC → chỉ dùng nội bộ.** Ghi rõ điều này vào README. |
| **F5-TTS-Vietnamese** (hynt) | | |

Ở V1 chỉ cần **chọn một cái, chạy được, và đo RTF trên CPU N100.** Nếu có laptop khác hoặc GPU thuê, đo thêm để có điểm so sánh.

### Làm

1. Chọn một model. Ghi lý do chọn vào `decisions.md` (không được viết "vì nó phổ biến").
2. Chạy trên mini PC. Đo RTF bằng harness Bài 11.
3. Chạy **cùng model, cùng câu** trên laptop của bạn (CPU khác) — đây là điểm so sánh thứ hai, miễn phí.
4. Nếu model quá nặng cho N100, thử VieNeu-TTS và ghi rõ là so sánh hai model khác nhau — đừng giả vờ là cùng một phép đo.
5. Ghi nhiệt độ và tần số CPU thật trong lúc chạy (`sensors`, `turbostat`). N100 hạ xung khi nóng hoặc khi chạm giới hạn công suất.
6. **Viết quyết định kiến trúc, kèm số.**

### Số phải ra

| Máy | RTF kỳ vọng | Kết luận |
|---|---|---|
| N100, model on-device tối ưu (VieNeu-TTS) | Có thể <1 | Stream được |
| N100, model nặng | Có thể >1 | Pre-render, hoặc chạy trên GPU thuê theo lô |
| GPU thuê | <0,1 | Dư sức, nhưng phụ thuộc mạng — ghi rõ đánh đổi |

Đây là những dải kỳ vọng thô — chính phép đo của bạn mới là con số. Và: nếu tần số CPU tụt hoặc nhiệt độ chạm trần khi chạy TTS liên tục, bạn có một ràng buộc nhiệt cần ghi vào kiến trúc.

### Nếu ra khác

| Triệu chứng | Ý nghĩa |
|---|---|
| RTF trên N100 < 0,5 | Stream thoải mái. Ghi lại — đây là số đỡ lưng cho kiến trúc |
| RTF dao động mạnh giữa các lần | Hạ xung do nhiệt/công suất, hoặc swap. Kiểm tần số thật và RAM |
| Model không chạy nổi (OOM) | Ghi lại giới hạn RAM. Đây là số thật cho resource budget của robot ở Khóa 7 |

---

## Bài 13 — Streaming chunk đầu: độ trễ cảm nhận vs độ trễ tổng (5h)

**Câu hỏi:** vì sao stream chunk đầu tiên làm hệ thống *cảm giác* nhanh hơn nhiều mà tổng thời gian không đổi?

### Khái niệm

Đây là bài học số hai của latency budget, và nó là một trong những bài học chuyển ngành sạch nhất từ backend sang robotics: **time-to-first-byte và total-time là hai chỉ số khác nhau, tối ưu khác nhau, và người dùng chỉ cảm nhận cái đầu.**

Nếu đợi TTS sinh xong cả file rồi mới phát: độ trễ cảm nhận = toàn bộ thời gian sinh + buffer. Nếu stream chunk đầu ngay khi có: độ trễ cảm nhận = thời gian sinh chunk đầu + buffer, trong khi phần còn lại được sinh song song với việc phát.

Rủi ro: nếu RTF > 1 thì streaming sẽ **underrun giữa chừng** — người nghe nghe được nửa câu rồi đứt. Đây là lý do phải đo RTF trước khi quyết streaming.

### Làm

1. Triển khai hai chế độ trong client: `batch` (đợi xong) và `stream` (phát ngay khi có chunk đầu).
2. Đo cho mỗi chế độ, với 3 độ dài câu:
   - **time-to-first-audio**: từ lúc gửi request tới lúc sample đầu ra loa (dùng phương pháp Bài 9)
   - **total-time**: tới lúc sample cuối ra loa
3. Chạy streaming với một model có RTF > 1 (ép bằng cách thêm tải CPU). Đếm số lần đứt giữa chừng.
4. Vẽ: time-to-first-audio vs độ dài câu, hai chế độ chồng lên nhau.

### Số phải ra

| Chế độ | time-to-first-audio (câu 20 từ) | total-time |
|---|---|---|
| batch | ≈ RTF × độ_dài + buffer | ≈ RTF × độ_dài + độ_dài + buffer |
| stream | ≈ thời gian sinh chunk đầu + buffer | Xấp xỉ bằng batch |

Điểm phải chứng minh được bằng số: **time-to-first-audio giảm mạnh, total-time gần như không đổi.** Nếu total-time của streaming *tệ hơn* đáng kể, bạn đang trả giá cho overhead chunking — ghi lại con số đó.

Và: với RTF > 1, streaming phải **đứt**. Nếu không đứt, bạn đang buffer nhiều hơn mình nghĩ — tìm ra chỗ đó.

---

# MODULE 4 — HỆ THỐNG V1 (22h)

**Điều kiện vào module này:** B2 đã có câu trả lời bằng văn bản. Nếu quản lý từ chối, vẫn làm toàn bộ module này nhưng chạy ở nhà và **bỏ hoàn toàn phần nhận diện mặt** — portfolio không mất gì, vì giá trị nằm ở lab notebook và số đo, không nằm ở việc cái loa đặt ở đâu.

---

## Bài 14 — Ingest, dedupe, state machine (6h)

**Câu hỏi:** làm sao biến một Google Sheet thành một nguồn sự kiện đáng tin?

### Khái niệm

Phần này đúng nghề bạn, nên tôi sẽ nói ngắn và chỉ nhấn vào chỗ khác với backend thường ngày.

**Push hay pull** — quyết định kiến trúc số 3, phải tự bảo vệ được:

| | Apps Script webhook | Sheets API polling |
|---|---|---|
| Độ trễ | <1s | Nửa chu kỳ poll |
| Cần endpoint public | Có (ngrok / Cloudflare Tunnel) | Không |
| Điểm hỏng | Tunnel chết, Google đổi quota | Quota API, chu kỳ poll |
| Phù hợp khi | Cần độ trễ thấp | Không muốn expose gì ra ngoài |

Chọn có lý do và **ghi lý do vào `decisions.md`**. Cả hai đều là câu trả lời đúng; không ghi lý do mới là sai.

**Điểm khác với backend thường ngày:** ở đây "xử lý trùng" không chỉ là vấn đề dữ liệu, nó là vấn đề **âm thanh**. Một confession phát hai lần giữa văn phòng là một sự cố nhìn thấy được. Idempotency ở đây có hậu quả vật lý.

### Làm

1. Dựng ingest API (FastAPI). Endpoint nhận record mới.
2. **Dedupe** theo một khóa ổn định (row id + hash nội dung). Lưu vào SQLite với ràng buộc UNIQUE.
3. **State machine** rõ ràng cho mỗi confession:
   ```
   RECEIVED → PENDING_MODERATION → APPROVED → QUEUED → SPEAKING → DONE
                                 ↘ REJECTED
                                                      ↘ FAILED → (retry hoặc DEAD)
   ```
4. Mọi chuyển trạng thái ghi log có cấu trúc, kèm timestamp monotonic **và** wall clock (nhớ Bài 3.1 của tài liệu nền — hai đồng hồ khác nhau, dùng khác nhau).
5. Viết test: gửi cùng record 5 lần → chỉ phát 1 lần.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Gửi lặp 5 lần cùng record | Đúng 1 lần vào QUEUED |
| Kill process giữa lúc ghi DB, khởi động lại | Không mất record, không phát trùng |
| Mất mạng 5 phút rồi có lại | Ingest tự phục hồi, không mất record đã có trong Sheet |

---

## Bài 15 — Moderation queue và kill switch (5h)

**Câu hỏi:** vì sao đây là yêu cầu kỹ thuật chứ không phải nice-to-have?

### Khái niệm

Đọc kỹ đoạn này, vì nó là chỗ project chết nếu làm sai, và nó không phải vấn đề kỹ thuật.

Một hòm confession ẩn danh gắn với một cái loa đọc to giữa văn phòng là **một kênh quấy rối có khuếch đại**. Không phải "có thể bị lạm dụng" — mà là sẽ bị, trong tuần thứ hai. Lộ trình ghi rõ: bỏ moderation thì project chết vì lý do phi kỹ thuật.

Ba thành phần bắt buộc, có từ ngày đầu:
1. **Hàng đợi duyệt tay** — không có gì được phát mà không qua một con người
2. **Filter tên riêng** — chặn nội dung nhắm vào cá nhân cụ thể
3. **Nút kill** — dừng ngay lập tức, phần cứng nếu có thể

Và ràng buộc pháp lý cho các version sau: Nghị định 13/2023 xếp dữ liệu sinh trắc học vào dữ liệu cá nhân nhạy cảm. Nhận diện mặt ở V3 chỉ làm trên chính mình và người tình nguyện có consent viết. Không đàm phán.

### Làm

1. Web UI tối giản cho duyệt: danh sách PENDING, nút Approve / Reject, hiển thị nội dung đầy đủ.
2. Filter tên riêng: danh sách tên đồng nghiệp → nội dung khớp tự động chuyển sang cần-duyệt-kỹ, không tự động từ chối (tránh false positive gây bực).
3. **Nút kill**: một endpoint dừng mọi phát, xả queue, và một nút vật lý (GPIO trên ESP32 — ngắt ưu tiên cao, dừng I2S ngay tại MCU, rồi báo lên host) làm điều tương tự. Nút vật lý quan trọng vì lúc cần dừng gấp thì không ai mở laptop.
4. Log mọi quyết định duyệt: ai duyệt, lúc nào, nội dung gì.
5. **Test kill switch 10 lần**, trong đó ≥3 lần đúng lúc đang phát giữa câu.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Nội dung chưa duyệt | **Không bao giờ** đến được player. Chứng minh bằng test tự động. |
| Bấm kill giữa lúc đang phát | Âm thanh dừng trong <1s, queue xả sạch, hệ thống vẫn sống |
| Sau kill, khởi động lại | Không tự động phát lại thứ đã bị kill |

---

## Bài 16 — Streamer daemon, firmware, watchdog hai tầng (5h)

**Câu hỏi:** làm sao để nó tự sống khi không ai nhìn?

### Làm

1. Đóng gói streamer trên mini PC thành daemon (Rust hoặc Python), chạy dưới `systemd` với `Restart=always`.
2. **Ring buffer hai đầu** (Bài 4) — để jitter mạng và jitter host không thành underrun.
3. **Watchdog hai tầng**, đúng kiến trúc robot thật:
   - **Host:** systemd `WatchdogSec=` cho daemon, và `RuntimeWatchdogSec=` để systemd vỗ watchdog phần cứng của chipset Intel (driver `iTCO_wdt`, kiểm có trên máy bạn không). Treo cả hệ điều hành → máy tự reset.
   - **ESP32:** task watchdog của ESP-IDF. Mất kết nối host quá N giây → ESP32 tự dừng phát và chờ.
4. Structured logging (JSON lines). Yêu cầu: trả lời được câu hỏi *"3h sáng thứ Bảy nó làm gì"* chỉ bằng cách grep log.
5. **Log rotation** (`journald` giới hạn dung lượng + logrotate cho file riêng). Đĩa đầy là chuyện có thật, không phải lo xa.
6. Xử lý ba tình huống lỗi: mất mạng, Google API lỗi, TTS worker chết — cộng tình huống thứ tư mới: **rút cáp USB tới ESP32**. Mỗi cái có hành vi xác định và được log.
7. **BIOS mini PC: bật Auto Power On** (restore on AC power loss). Không bật thì bài soak rút điện ở Bài 17 sẽ trượt ngay lần đầu.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| `kill -9` daemon | systemd khởi động lại trong <5s, không mất record trong queue |
| Ngắt mạng 10 phút | Log ghi rõ, tự phục hồi khi có mạng, không crash loop |
| Rút rồi cắm lại cáp USB tới ESP32 | Daemon phát hiện, kết nối lại, không phát trùng |
| Treo daemon giả lập (sleep vô hạn) | systemd watchdog giết và khởi động lại |
| Làm đầy 90% đĩa (file rác) | Log rotation kích hoạt, hệ thống vẫn chạy |

---

## Bài 17 — TN-5: 72 giờ không ai trông (6h người, 72h treo máy)

**Câu hỏi:** nó có thật sự chạy được không, hay chỉ chạy được lúc bạn đang nhìn?

Thí nghiệm bắt buộc số 5, tiêu chí PASS số 7 của M4 — và là tiêu chí khắt khe nhất.

### Làm

Chạy liên tục 72 giờ, trong đó:

1. ≥20 confession thật được phát đúng
2. **0 lần can thiệp tay**
3. **Rút điện đột ngột 10 lần**, trong đó ≥3 lần đúng lúc đang ghi DB. Bật lại. Kiểm dữ liệu.
4. Chứng minh log rotation bằng cách **cố tình làm đầy đĩa**
5. Theo dõi nhiệt độ CPU suốt 72h, vẽ đồ thị
6. Đo công suất trung bình của mini PC (đồng hồ điện ổ cắm, hoặc đo dòng trên dây 12V) và của ESP32 + amp ← **số đầu tiên trong power budget của robot Khóa 7**

### Số phải ra

| Đại lượng | Giá trị chấp nhận |
|---|---|
| Confession phát đúng | ≥20 |
| Lần can thiệp tay | **0** |
| Mất dữ liệu sau 10 lần rút điện | **0** |
| Nhiệt độ CPU tối đa | Ghi lại, cùng tần số CPU thật — không được hạ xung kéo dài |
| Công suất trung bình mini PC | Ghi lại. N100 nhàn cỡ vài W, có tải TTS cao hơn nhiều — số thật của bạn là thứ đi vào power budget |
| Underrun trong 72h | Ghi lại con số, so với dự đoán từ Bài 10 |
| Brownout reset của ESP32 trong 72h | **0** |

**Về việc rút điện:** đây là bài test mà phần lớn hệ thống tự chế trượt. SQLite với WAL mode và `synchronous=FULL` sẽ sống sót; SQLite mặc định thì có thể không. Nếu bạn mất dữ liệu, **đó là kết quả tốt** — nó dạy bạn về durability ở tầng mà backend thường được framework che cho.

---

# GATE KHÓA 3 (6h)

Đối chiếu đúng 7 tiêu chí PASS của M4. Nhị phân, không chấm bằng cảm giác.

```
[ ] 1. Không còn lời gọi cloud TTS nào trong chuỗi
       → grep repo, chứng minh bằng CI check

[ ] 2. TN-1: BCK đo được sai <1% so với dự đoán, ở 2 sample rate khác nhau
       → file .sr commit sau prediction.md, kèm bảng dự đoán vs đo

[ ] 3. TN-2: đường cong latency vs underrun ≥5 điểm dma_frame_num, ≥2 kịch bản tải,
       mỗi điểm ≥10 phút chạy; latency GPIO→mic đo được với độ phân giải ≤1ms

[ ] 4. TN-3: bảng ≥3 cấu hình nguồn, mỗi dòng có V_rail lúc nghỉ và lúc phát,
       số brownout reset của ESP32, mô tả tiếng

[ ] 5. TN-4: F0 giọng mình bằng số; đồ thị SNR đo vs lý thuyết 6.02×bits+1.76
       ở 4 mức bit depth, sai lệch <3dB

[ ] 6. Bảng latency budget: MỌI DÒNG là số đo, không dòng nào là ước tính,
       nút thắt được chỉ tên

[ ] 7. TN-5 soak 72h: ≥20 confession phát đúng, 0 lần can thiệp tay,
       log rotation đã chứng minh bằng cách cố tình làm đầy đĩa,
       ≥3 lần rút điện đúng lúc đang ghi DB mà dữ liệu còn nguyên
```

**FAIL → action (cam kết trước, không bàn lại lúc nản):** chạm 140h chưa PASS → **cắt scope, không gia hạn**. Bỏ tiêu chí 5 và 7, chỉ giữ "phát được audio ổn định 24h", publish nguyên trạng kèm ghi chú rõ cái gì chưa làm được, sang Khóa 4. V1 không được phép ăn hết năm đầu.

---

# LỊCH 12 TUẦN

| Tuần | Giờ | Làm | Xong thì có |
|---|---|---|---|
| 1 | 7 | Bài 1–2 · mini PC, ESP-IDF, I2S, DAC | Nghe được tiếng đầu tiên |
| 2 | 7 | Bài 3 (TN-1) | **Nhìn thấy âm thanh trên dây** |
| 3 | 7 | Bài 4 (DMA + USB streaming) | Host stream PCM qua USB, có flow control |
| 4 | 7 | Bài 5–6 (loa, TN-3 nguồn) | Bảng cấu hình nguồn |
| 5 | 8 | Bài 7 (TN-4) | F0 giọng mình, đồ thị SNR |
| 6 | 7 | Bài 8–9 (TN-2) | Độ trễ thật, độ phân giải ≤1ms |
| 7 | 7 | Bài 10 | Đường cong latency vs underrun |
| 8 | 7 | Bài 11–12 (RTF) | **Quyết định kiến trúc có số đỡ lưng** |
| 9 | 6 | Bài 13 (streaming) | time-to-first-audio |
| 10 | 7 | Bài 14–15 (ingest, moderation) | Hệ thống có gate an toàn |
| 11 | 6 | Bài 16 (daemon) | Tự sống |
| 12 | 7 | Bài 17 (soak) + Gate | **Khóa 3 PASS** |

**Tuần crunch MDP:** chuyển sang Khóa 2 hoặc chế độ tối thiểu 2h chỉ đọc. Đừng ép một thí nghiệm phần cứng vào tuần go-live.

---

# BẢY BẪY ĐÃ BIẾT TRƯỚC

Tổng hợp từ lộ trình và từ các bài ở trên. Đọc một lần, dán lên tường.

1. **Mini PC không có GPIO.** Mọi chân tín hiệu nằm trên ESP32-S3. Đừng mua USB sound card cho "tiện" — nó giấu toàn bộ chuỗi.
2. **Chân strapping và chân USB của ESP32-S3** (0, 3, 45, 46, 19, 20). Dùng nhầm thì không boot hoặc mất cổng nạp.
3. **Chân SCK của module PCM5102A thường cần nối GND** để dùng PLL nội. Không nối, DAC im lặng và bạn sẽ nghĩ nó hỏng.
4. **Đừng nối loa trực tiếp vào line-out của DAC.** Sai trở kháng, không đủ dòng, có thể làm chết DAC.
5. **Logic analyzer clone 24MHz** đủ cho I2S ở 768kHz nhưng chật vật ở sample rate cao. Biết giới hạn của dụng cụ đo cũng là một phần của việc đo.
6. **Mua 2 cái cho mọi module rẻ và quan trọng.** Không có module thứ hai để so, bạn không phân biệt được "module chết" với "cấu hình sai".
7. **Driver có thể ép tham số khác thứ bạn xin** (`dma_frame_num`, sample rate thật). Luôn đọc lại cấu hình thật và đo bằng logic analyzer — đừng tin config.

---

# NGUỒN HỌC KÈM KHÓA 3

| Nguồn | Xem/đọc phần nào | Cho bài nào |
|---|---|---|
| **Datasheet PCM5102A** (TI) | Pin config, timing diagram, chế độ FMT | Bài 2, 3 |
| **Datasheet INMP441** | Định dạng khung I2S, dải động, độ nhạy | Bài 7 |
| **ESP-IDF Programming Guide — I2S** | Standard mode, DMA buffer (`dma_desc_num`, `dma_frame_num`), event callbacks | Bài 2, 4, 9, 10 |
| **ESP-IDF — USB-CDC / TinyUSB, Reset reason, Brownout, Task Watchdog** | | Bài 4, 6, 16 |
| **FreeRTOS — Ring buffer, task priority** | | Bài 4, 10 |
| **ALSA Project docs** — `alsa-project.org` | PCM interface, period/buffer, XRUN — **chỉ cho bước tùy chọn Bài 4** | Bài 4 |
| **systemd docs** — `WatchdogSec`, `RuntimeWatchdogSec` | | Bài 16 |
| **sigrok/PulseView docs** — decoder I2S | | Bài 3, 9 |
| **Ben Eater** (YouTube) — series về clock và tín hiệu số | | Bài 3 |
| **VietTTS / VieNeu-TTS / Viterbox** — README của từng repo | | Bài 12 |
| **Making Embedded Systems** — Elecia White | Chương về debugging và về thời gian | Toàn khóa |

Vẫn giữ quy tắc ba nguồn: một nguồn chính + một tra cứu + datasheet. Ở khóa này **datasheet là nguồn quan trọng nhất**, vì mọi con số "phải ra" đều bắt nguồn từ đó.

---

# SAU KHÓA 3

**Khóa 4 — Đo hiệu năng inference trên edge (70h).** Không cần mua gì mới, thuê GPU theo giờ. Harness benchmark bạn viết ở Bài 11 dùng lại được gần như nguyên vẹn, chỉ đổi payload từ TTS sang VLA model. Đây là artifact ★ thứ hai và nó tạo tín hiệu phỏng vấn nhanh hơn Khóa 3.

**Nhắc lần cuối:** nếu Khóa 2 vẫn chưa xong khi bạn đọc dòng này, dừng Khóa 3 lại và đóng Khóa 2 trước. Khóa 3 là thứ khiến bạn không bị loại. Khóa 2 là thứ khiến bạn được gọi.
