# KHÓA 3 — CHUỖI AUDIO: TỪ SỐ NGUYÊN ĐẾN ÁP SUẤT KHÔNG KHÍ

**Cho:** người đã PASS Khóa 1, biết cầm que đo và đọc logic analyzer.
**Thời lượng:** ~90h · **Trần:** 140h. Khoảng 12–14 tuần ở nhịp 6–7h/tuần.
**Chi phí:** đợt 2, ~3.5–4.5tr.
**Tương ứng:** milestone **M4** trong lộ trình 24 tháng.

**Xong khóa này bạn làm được:** đi hết chuỗi từ một số nguyên trong RAM tới sóng áp suất trong không khí, và **có số đo ở mọi chặng**. Đó là câu chuyện bạn kể trong phỏng vấn khi người ta hỏi "anh đã thực sự chạm phần cứng chưa".

**Điều kiện mở khóa — cả ba:**
1. Khóa 1 PASS (5 tiêu chí của M1)
2. `hours.csv` cho thấy median ≥5h/tuần trong 4 tuần gần nhất
3. Đã mua đợt 2

**Điều kiện mở Module 4 (deploy ở công ty):** B2 đã có câu trả lời **bằng văn bản** từ quản lý. Đồng ý hay từ chối đều được — chỉ cần có câu trả lời. Nếu từ chối: chạy V1 ở nhà, bỏ hoàn toàn phần nhận diện mặt, portfolio không mất gì.

---

## VỊ TRÍ TRONG BẢN ĐỒ 6 KHÓA

| Khóa | Tên | Giờ | Trạng thái |
|---|---|---|---|
| 1 | Từ zero đến đo được | 35 | Gần xong |
| 2 | Dữ liệu robot mà không cần robot | 80 | **Chạy song song — đừng dừng** |
| **3** | **Chuỗi audio** | **90** | ← tài liệu này |
| 4 | Đo hiệu năng inference trên edge | 70 | Sau |
| 5 | Cảm biến, đồng bộ thời gian, data platform | 150 | Sau |
| 6 | Robot learning với SO-101 | 120 | Tùy chọn |

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

## Bài 2 — Dựng Pi 5 và DAC I2S (5h)

**Câu hỏi:** làm sao để một máy tính Linux đẩy bit ra ba sợi dây?

### Khái niệm

**Vì sao I2S chứ không phải jack 3.5mm.** Lý do bề mặt: Pi 5 đã bỏ jack 3.5mm. Lý do thật: bạn muốn **nhìn thấy tín hiệu số trước khi nó thành analog**. Với I2S bạn cắm logic analyzer và thấy từng bit sample chạy trên dây. Với USB sound card, toàn bộ chuỗi bị giấu trong firmware và bạn không học được gì.

**Ba dây của I2S:**

| Dây | Tên khác | Là gì |
|---|---|---|
| **BCK** | BCLK, SCK, PCM_CLK | Bit clock — mỗi cạnh đánh nhịp một bit |
| **LRCK** | WS, LRCLK, PCM_FS | Word select — mức thấp = kênh trái, cao = kênh phải. **Tần số của nó chính là sample rate.** |
| **DIN** | SD, DATA, PCM_DOUT | Dữ liệu |

Cộng GND. Luôn luôn cộng GND.

### Làm

**Bước 1 — cài hệ điều hành.** Raspberry Pi OS 64-bit lên thẻ A2. Cắm Ethernet, không dùng WiFi trong lúc dev (một biến số ít đi).

**Bước 2 — bật I2S.** Sửa `/boot/firmware/config.txt`:

```
dtparam=audio=off
dtoverlay=hifiberry-dac
```

Dòng đầu tắt audio onboard để không tranh chấp. Reboot.

**Bước 3 — đấu dây PCM5102A.** Đây là bảng phải kiểm tra ba lần trước khi cấp điện:

| PCM5102A | Pi 5 | Ghi chú |
|---|---|---|
| VCC | 5V (module có regulator riêng — **kiểm tra module của bạn**) | Một số module chỉ nhận 3.3V |
| GND | GND | |
| BCK | GPIO 18 (pin 12) | |
| LCK / LRCK | GPIO 19 (pin 35) | |
| DIN | GPIO 21 (pin 40) | |
| **SCK** | **GND** | ← **Chỗ giết người.** Không nối, DAC im lặng và bạn sẽ nghĩ nó hỏng. |

Các chân jumper trên module (thường đã set sẵn, kiểm tra lại):

| Chân | Nối vào | Nghĩa |
|---|---|---|
| FMT | GND | Định dạng I2S chuẩn |
| XSMT | 3.3V (HIGH) | Unmute. LOW = câm. |
| FLT | GND | Bộ lọc bình thường |
| DEMP | GND | Tắt de-emphasis |

**Bước 4 — xác minh card xuất hiện.**

```bash
aplay -l
speaker-test -D hw:0,0 -c 2 -r 24000 -F S16_LE -t sine -f 440
```

**Lưu ý về `aplay`:** dùng nó **chỉ ở bước này**, để xác minh phần cứng tồn tại. Từ Bài 4 trở đi bạn viết player riêng. `aplay` giấu toàn bộ cấu hình buffer — thứ chính là bài học của Module 2.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| `aplay -l` | Liệt kê một card tên chứa `hifiberry` hoặc `snd_rpi_hifiberry_dac` |
| `speaker-test` | Nghe thấy tone 440Hz ở line-out của DAC (cắm tai nghe thử) |
| Đo áp VCC của module lúc chạy | Đúng bằng áp bạn cấp, sai lệch <5% |
| Đo áp chân XSMT | ≥2.0V (mức HIGH) |

### Nếu ra khác

| Triệu chứng | Nguyên nhân nghi ngờ | Cách sửa |
|---|---|---|
| `aplay -l` không thấy card | Overlay chưa nạp | Kiểm tra chính tả trong `config.txt`, đã reboot chưa, `dmesg \| grep -i hifi` |
| Card có, nhưng hoàn toàn im lặng | **SCK chưa nối GND** | Nối SCK xuống GND. Đây là nguyên nhân số 1. |
| Im lặng, SCK đã nối | XSMT đang LOW | Kéo XSMT lên 3.3V |
| Có tiếng nhưng rè, méo | Sai FMT, hoặc dây quá dài, hoặc thiếu GND chắc | Kiểm FMT=GND, rút ngắn dây, thêm một dây GND thứ hai |
| Tiếng đúng nhưng cao/thấp bất thường | Sai sample rate giữa player và DAC | Ép rate cụ thể trong `speaker-test -r` |
| Có tiếng ở một kênh | DIN chập, hoặc LRCK lỗi | Sang Bài 3 đo bằng logic analyzer thay vì đoán |

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

**Bước 6 — lặp ở 48kHz.** Đổi cấu hình player, dự đoán lại, đo lại.

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
| LRCK không phải 24kHz mà là 48kHz | ALSA đang resample ngầm | Ép `hw:0,0` thay vì `default` (plughw resample tự động) |
| Decoder I2S không ra gì | Gán nhầm kênh, hoặc sai polarity | Thử đảo Word select polarity trong tùy chọn decoder |
| Waveform trông giống răng cưa | Sample rate capture quá thấp | Tăng lên 24MHz |

**Ghi chú về `plughw` vs `hw`:** ALSA có một lớp `plug` tự động resample, đổi format, đổi số kênh — rất tiện và **rất tai hại** cho việc học. Nó khiến bạn tưởng mình đang phát 24kHz trong khi phần cứng chạy 48kHz. Từ giờ dùng `hw:0,0` trực tiếp. Nếu nó báo lỗi không hỗ trợ format, đó là thông tin thật, đừng che nó bằng `plughw`.

### Tự kiểm tra

1. *Nếu đếm được 64 cạnh BCK trong một chu kỳ LRCK ở stereo, bit depth là bao nhiêu?* → 32-bit
2. *BCK 3.072 MHz tương ứng cấu hình nào?* → 48kHz × 32 bit × 2 kênh
3. *Vì sao logic analyzer 24MHz vẫn đọc được BCK 768kHz mà không vi phạm Nyquist?* → Nyquist đòi >2× cho tín hiệu tương tự. Với tín hiệu số ta cần đủ mẫu để xác định vị trí cạnh, thực tế cần 4–10×. 24/0,768 ≈ 31× nên rất an toàn.

---

## Bài 4 — ALSA từ dưới lên: period, buffer, underrun (6h)

**Câu hỏi:** độ trễ audio nằm ở đâu, và ai quyết định nó?

### Khái niệm

Đây là bài nối trực tiếp 8 năm backend của bạn vào thế giới vật lý, nên đọc chậm.

ALSA có một vòng đệm tròn (ring buffer) giữa chương trình của bạn và phần cứng. Hai tham số:

| Tham số | Là gì | Tương tự backend |
|---|---|---|
| **buffer_size** | Tổng số frame trong ring buffer | Kích thước queue |
| **period_size** | Số frame phần cứng tiêu thụ trước khi báo "tôi cần thêm" | Batch size / prefetch chunk |

`buffer_size` thường = `period_size × periods` (periods hay là 2, 3, hoặc 4).

**Độ trễ tối đa do buffer gây ra:**

```
latency_buffer (giây) = buffer_size / sample_rate
```

Ở 24kHz: buffer 4800 frame → 200ms. Buffer 1200 frame → 50ms. Buffer 240 frame → 10ms.

**Underrun (XRUN)** xảy ra khi phần cứng đòi dữ liệu mà buffer rỗng. Failure mode của nó là **một tiếng "tách" nghe được bằng tai** — không phải một dòng log. Đây chính là đường cong bạn đã tối ưu ở tầng API cả sự nghiệp, chỉ đổi đơn vị đo của sự cố.

Buffer nhỏ → độ trễ thấp, dễ underrun. Buffer lớn → độ trễ cao, ổn định. **Không có cấu hình tốt nhất, chỉ có điểm đánh đổi phù hợp với yêu cầu.** Module 2 sẽ đo đường cong này.

### Làm

**Bước 1 — bỏ `aplay`.** Viết player tối thiểu bằng Python với `pyalsaaudio` (hoặc C với `libasound` nếu muốn xuống sâu hơn). Yêu cầu tối thiểu:

- Mở thiết bị bằng `hw:0,0`, **không** `default`, **không** `plughw`
- Set rõ ràng: rate, format S16_LE, channels, period_size
- Đọc file PCM raw, ghi từng period vào thiết bị
- Bắt và **đếm** XRUN, không nuốt exception

**Bước 2 — xác minh tham số thực sự được chấp nhận.** ALSA có thể im lặng điều chỉnh tham số bạn xin. Sau khi set, **đọc lại** giá trị thực tế và in ra. Đây là một thói quen chung: đừng tin thứ mình set, hãy đọc lại thứ thiết bị chấp nhận.

**Bước 3 — đo độ trễ bằng đồng hồ trước.** Chưa cần logic analyzer. Đơn giản: đo thời gian từ lúc gọi ghi frame đầu tiên tới lúc chương trình kết thúc, so với độ dài file. Chênh lệch xấp xỉ bằng buffer đang được xả nốt.

**Bước 4 — cố tình gây underrun.** Chèn `time.sleep()` vào giữa vòng lặp ghi. Nghe. Đếm XRUN.

### Số phải ra

| Cấu hình (24kHz stereo) | Độ trễ buffer lý thuyết | Hiện tượng |
|---|---|---|
| buffer 4800 frame | 200 ms | Rất ổn định, không XRUN |
| buffer 2400 | 100 ms | Ổn định |
| buffer 1200 | 50 ms | Ổn định trên Pi 5 nhàn |
| buffer 480 | 20 ms | Bắt đầu nhạy với tải CPU |
| buffer 240 | 10 ms | XRUN khi có tải nền |

Và: **giá trị `period_size` bạn xin phải bằng giá trị đọc lại**. Nếu không bằng, driver đã điều chỉnh và mọi tính toán độ trễ của bạn sai.

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| XRUN liên tục ngay cả với buffer lớn | Đang chạy qua `default` với dmix/resample | Ép `hw:0,0` |
| Không nghe thấy gì nhưng không lỗi | Ghi sai format (S16_LE vs S32_LE) | Đọc lại format thực tế thiết bị chấp nhận |
| Độ trễ đo được gấp đôi tính toán | Nhầm **frame** với **sample** | Xem lại Bài 1: 1 frame stereo = 2 sample = 4 byte |
| period_size xin 256 nhưng đọc lại ra 1024 | Driver ép giá trị tối thiểu | Ghi nhận giá trị thật vào lab notebook, dùng nó cho mọi tính toán |

### Tự kiểm tra

1. *Buffer 1024 frame ở 48kHz gây trễ bao nhiêu?* → 21,3 ms
2. *Vì sao giảm period_size lại làm CPU bận hơn?* → Mỗi period là một lần đánh thức tiến trình. Period nhỏ = nhiều lần đánh thức/giây = nhiều context switch.
3. *Nếu quan tâm độ trễ hơn độ ổn định, tăng hay giảm buffer?* → Giảm, và chấp nhận tỉ lệ XRUN cao hơn. Module 2 sẽ định lượng "cao hơn" là bao nhiêu.

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

1. Đấu chuỗi đầy đủ: Pi → PCM5102A → line-out → PAM8403/TPA3110 → loa 4Ω. Amp dùng **nguồn riêng**, nhưng **chung GND** với Pi.
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

**Câu hỏi:** điều gì xảy ra khi amp và Pi tranh nhau một nguồn?

Đây là thí nghiệm bắt buộc số 3 và là tiêu chí PASS số 4 của M4. Nó cũng là bài học sẽ cứu bạn ba ngày debug ở Khóa 5, khi motor làm ESP32 reset.

### Khái niệm

Amplifier tiêu thụ dòng **theo nhịp nhạc**, không đều. Một đoạn bass mạnh có thể kéo dòng gấp nhiều lần lúc nghỉ. Nếu amp lấy dòng từ chính rail 5V của Pi, dòng vọt đó làm sụt áp toàn hệ — và Pi phản ứng bằng cách throttle hoặc reset.

Pi có cờ phần cứng ghi lại việc này:

```bash
vcgencmd get_throttled
```

Trả về một bitmask hex. `0x0` = mọi thứ ổn. Các bit đáng nhớ:

| Bit | Nghĩa |
|---|---|
| 0 | Đang under-voltage **ngay lúc này** |
| 1 | Đang giới hạn tần số ARM |
| 2 | Đang throttle |
| 16 | Under-voltage **đã từng xảy ra** kể từ khi boot |
| 18 | Đã từng throttle |

Bit 16 là bit quan trọng nhất — nó nhớ sự kiện đã qua, và nó là bằng chứng cho điều mà tai bạn chỉ nghe thấy mơ hồ.

### Làm

Ba cấu hình, mỗi cấu hình chạy cùng một đoạn audio có bass mạnh ở âm lượng tối đa:

**Cấu hình 1 — tệ nhất, cố tình.** Amp lấy 5V từ chân 5V của Pi.
**Cấu hình 2 — tháo GND chung** giữa DAC và amp (giữ nguyên nguồn chung). Nghe. Đo. *Rồi nối lại ngay.*
**Cấu hình 3 — nguồn riêng cho amp**, giữ common ground.
**Cấu hình 4 — như 3, thêm tụ 470µF–1000µF sát chân nguồn amp.**

Với mỗi cấu hình, ghi:
- V rail 5V lúc **nghỉ** (đo bằng multimeter tại chân nguồn của amp)
- V rail lúc **đang phát bass mạnh**
- `vcgencmd get_throttled` sau khi phát 2 phút
- Mô tả tiếng bằng lời

**Trước khi làm: viết dự đoán.** Bạn nghĩ V rail sẽ sụt bao nhiêu ở cấu hình 1? Commit trước.

### Số phải ra

| Cấu hình | V rail nghỉ | V rail lúc phát | get_throttled | Tiếng |
|---|---|---|---|---|
| 1 — chung nguồn Pi | ~5.0V | Sụt rõ rệt, thường 4.6–4.8V hoặc thấp hơn | Khả năng cao **≠ 0x0**, bit 16 bật | Méo theo nhịp bass, có thể có tiếng lạo xạo |
| 2 — mất GND chung | — | — | — | Ù, nhiễu, hoặc im hẳn |
| 3 — nguồn riêng | ~5.0V | Sụt rất ít, <0.1V | `0x0` | Sạch |
| 4 — thêm tụ | ~5.0V | Sụt ít hơn nữa | `0x0` | Sạch, bass chắc hơn |

Nếu cấu hình 1 **không** gây sụt áp đáng kể, tăng âm lượng, dùng loa trở kháng thấp hơn, hoặc dùng đoạn audio có bass mạnh hơn. Thí nghiệm này chỉ có giá trị khi bạn **thực sự tạo được lỗi**, rồi sửa nó.

### Nếu ra khác

| Triệu chứng | Ý nghĩa |
|---|---|
| `get_throttled` ra `0x50000` | Đã từng under-voltage (bit 16) và đã từng throttle (bit 18) — chính xác là thứ bạn đang cố tạo ra |
| Không tạo được sụt áp ở cấu hình 1 | Nguồn Pi quá khỏe hoặc amp quá nhỏ. Vẫn ghi lại kết quả — "không tái hiện được" cũng là một kết quả, nhưng phải ghi rõ điều kiện |
| Pi reset giữa chừng | Thí nghiệm thành công quá mức. Đây chính xác là brownout. Chụp màn hình log và ghi lại. |

**Bài học để mang đi:** bạn vừa tự tay tạo lỗi rồi tự tay sửa. Sau này ở Khóa 5, khi ESP32 reset lúc motor quay, bạn sẽ nhận ra triệu chứng trong 30 giây thay vì mất ba ngày nghi ngờ code.

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
1. Đấu INMP441: VDD 3.3V, GND, SD→DIN của Pi, SCK→BCK, WS→LRCK, L/R→GND (chọn kênh trái).
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
| Pi không cho vừa phát vừa ghi | Một bus I2S chỉ làm một chiều tại một thời điểm trên cấu hình mặc định | Ghi và phát ở hai lần chạy riêng. Bài 9 sẽ giải quyết bài toán đồng thời bằng cách khác. |

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
| Truyền LAN | | Có | Timestamp hai đầu |
| ALSA buffer | | **Có — bài học chính** | buffer_size / rate |
| DAC + amp + loa | | Không | Đo ở Bài 9 |
| Âm thanh truyền trong không khí | | Không | khoảng cách / 343 m/s |

Chặng cuối: tốc độ âm thanh ~343 m/s ở 20°C. 1m = 2,92ms. Mic đặt cách loa 30cm = 0,87ms. Con số này nhỏ nhưng **phải trừ ra** khi đo ở Bài 9, nếu không bạn đang tính thời gian truyền trong không khí vào độ trễ phần mềm.

### Số phải ra

Không có số đúng ở bài này — chỉ có **dự đoán được commit trước**. Giá trị của bài nằm ở chỗ so sánh dự đoán với thực tế ở Bài 9 và 10.

Nhưng có một dự đoán tôi muốn bạn viết ra và ký tên: **bạn nghĩ nút thắt nằm ở đâu?** Ghi vào `prediction.md`. Phần lớn người có nền backend sẽ đoán là TTS hoặc ALSA. Kết quả thật thường làm họ ngạc nhiên.

---

## Bài 9 — TN-2: Đo độ trễ từ phần mềm ra không khí (7h)

**Câu hỏi:** giữa dòng code ghi sample đầu tiên và sóng âm chạm mic, có bao nhiêu mili-giây?

Thí nghiệm bắt buộc số 2 — lộ trình gọi nó là **quan trọng nhất trong năm cái**. Tiêu chí PASS số 3 của M4 đòi độ phân giải ≤1ms.

### Khái niệm

Vấn đề: bạn cần so **một sự kiện phần mềm** với **một sự kiện vật lý** trên cùng một trục thời gian. Đây chính xác là bài toán đồng bộ mà Khóa 5 sẽ làm ở quy mô lớn — làm nhỏ trước ở đây.

Giải pháp: dùng một chân GPIO làm cầu nối. Kéo GPIO lên HIGH tại **đúng dòng code** ghi sample đầu tiên vào ALSA. Chân đó và tín hiệu mic cùng được logic analyzer ghi lại → cùng một trục thời gian, cùng một đồng hồ.

### Làm

**Phương pháp chính — logic analyzer 4 kênh:**

| Kênh | Nối vào |
|---|---|
| GND | GND |
| D0 | GPIO đánh dấu (từ player) |
| D1 | BCK của **mic** INMP441 |
| D2 | LRCK của mic |
| D3 | SD (data) của mic |

**Bước 1 — sửa player.** Ngay trước lệnh ghi buffer đầu tiên vào ALSA, kéo GPIO lên HIGH. Dùng thư viện GPIO có độ trễ thấp (`libgpiod`, hoặc ghi thẳng vào sysfs đã mở sẵn file descriptor). Đo thời gian của chính lệnh toggle GPIO và ghi vào phần "sai số của phép đo" — nó thường là vài chục µs và không thể bỏ qua nếu bạn muốn độ phân giải 1ms.

**Bước 2 — đặt mic.** Cách loa **chính xác 30cm**, đo bằng thước. Ghi khoảng cách vào setup.md.

**Bước 3 — capture.** PulseView, sample rate 24MHz. Buffer 1M mẫu chỉ được ~42ms — có thể không đủ nếu độ trễ lớn. Giảm sample rate xuống 4MHz (đủ cho BCK 1.536MHz của mic, ~2.6 mẫu/chu kỳ — hơi sát; dùng 8MHz cho an toàn) để kéo dài thời gian capture. Ghi rõ đánh đổi này vào lab notebook.

**Bước 4 — phát và bắt.** Audio test nên bắt đầu bằng một **xung dốc đứng** (click, hoặc burst tone) chứ không phải fade-in — cạnh càng dốc, thời điểm khởi phát càng xác định được chính xác.

**Bước 5 — đo.** Decode I2S của mic, export giá trị sample. Tìm sample đầu tiên vượt ngưỡng năng lượng. Khoảng cách từ cạnh lên GPIO tới sample đó = độ trễ tổng.

**Bước 6 — trừ phần vật lý.** `latency_phần_mềm_và_phần_cứng = latency_đo − 0,87ms`

**Phương pháp dự phòng** nếu logic analyzer không đủ buffer: chạy hai tiến trình trên cùng Pi, một phát một ghi, dùng chung đồng hồ monotonic; ghi timestamp monotonic tại lúc ghi sample đầu tiên và tại lúc nhận từng frame mic; tìm onset trong file ghi. Độ phân giải = 1 chu kỳ LRCK = 41,7µs ở 24kHz. Kém trực quan hơn nhưng đủ đạt tiêu chí ≤1ms.

### Số phải ra

| Đại lượng | Giá trị kỳ vọng |
|---|---|
| Độ trễ tổng đo được (buffer 200ms) | Xấp xỉ 200ms + vài ms |
| Độ trễ tổng (buffer 50ms) | Xấp xỉ 50ms + vài ms |
| Phần dư sau khi trừ buffer và không khí | 1–5ms — đây là DAC + amp + loa |
| Độ phân giải phép đo | ≤1ms ← tiêu chí PASS |

**Kiểm tra chéo bắt buộc:** độ trễ đo được phải **thay đổi gần như tuyến tính** khi bạn đổi `buffer_size`. Nếu nó không đổi, bạn đang đo nhầm cái gì đó — có thể GPIO toggle không nằm đúng chỗ, hoặc ALSA đang đệm thêm ở tầng bạn không biết.

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Độ trễ đo được nhỏ hơn buffer_size/rate | GPIO toggle đặt sau khi buffer đã được nạp mồi | Đặt toggle trước lệnh write đầu tiên tuyệt đối |
| Độ trễ lớn hơn dự đoán rất nhiều | Đang đi qua `plughw` hoặc dmix | Ép `hw:0,0` |
| Không tìm được onset trong tín hiệu mic | Audio test fade-in quá chậm | Đổi sang click hoặc burst |
| Kết quả nhảy loạn giữa các lần | Chưa cố định vị trí mic, hoặc nhiễu phòng | Cố định mic bằng giá, đo trong phòng yên, lặp 10 lần lấy trung vị và độ lệch chuẩn |

**Lặp ít nhất 10 lần và báo cáo trung vị + độ lệch chuẩn, không phải một con số.** Một phép đo đơn lẻ không phải dữ liệu. Đây cũng là thói quen mà Khóa 5 sẽ đòi hỏi ở quy mô lớn hơn.

---

## Bài 10 — Đường cong độ trễ vs underrun (6h)

**Câu hỏi:** đánh đổi giữa độ trễ và độ tin cậy, bằng số, trông như thế nào?

Tiêu chí PASS số 3 của M4 đòi: ≥5 điểm `period_size`, mỗi điểm ≥10 phút chạy.

### Khái niệm

Bạn đã vẽ đường cong này ở tầng API cả sự nghiệp. Ở đây trục X là `period_size`, trục Y là độ trễ đo được và tỉ lệ XRUN. Điểm khác duy nhất: failure mode là một tiếng "tách" nghe được bằng tai thay vì một dòng log.

### Làm

1. Chọn 5 giá trị `period_size`, cách nhau theo cấp số nhân. Gợi ý ở 24kHz: 128, 256, 512, 1024, 2048 frame. Giữ `periods` cố định (ví dụ 3) để `buffer_size` tỉ lệ thuận.
2. **Đọc lại giá trị thực tế** driver chấp nhận cho từng mức. Nếu driver ép giá trị khác, dùng giá trị thật.
3. Với mỗi điểm: chạy phát liên tục **≥10 phút**, đếm XRUN, đo độ trễ bằng phương pháp Bài 9.
4. Chạy lần hai với **tải CPU nền** (`stress-ng --cpu 4` hoặc tương đương). Đây là kịch bản thật — V1 sẽ chạy cùng TTS client, logging, và ingest.
5. Vẽ hai đường cong: độ trễ vs period_size, và tỉ lệ XRUN/giờ vs period_size. Chồng hai kịch bản tải lên nhau.
6. **Chọn điểm vận hành cho V1 và viết lý do vào `decisions.md`.**

### Số phải ra

| period_size (24kHz, periods=3) | buffer | Độ trễ lý thuyết | XRUN kỳ vọng (Pi nhàn) | XRUN kỳ vọng (có tải) |
|---|---|---|---|---|
| 128 | 384 | 16 ms | Thỉnh thoảng | Nhiều |
| 256 | 768 | 32 ms | Hiếm | Thỉnh thoảng |
| 512 | 1536 | 64 ms | ~0 | Hiếm |
| 1024 | 3072 | 128 ms | 0 | ~0 |
| 2048 | 6144 | 256 ms | 0 | 0 |

Hình dạng đường cong quan trọng hơn giá trị tuyệt đối: **XRUN phải tăng mạnh khi period_size giảm dưới một ngưỡng**, và ngưỡng đó **dịch sang phải khi có tải CPU**. Nếu đường cong của bạn phẳng, hoặc bạn chưa đủ tải, hoặc chưa chạy đủ lâu.

### Nếu ra khác

| Triệu chứng | Ý nghĩa |
|---|---|
| XRUN = 0 ở mọi mức, kể cả 128 | Pi 5 khỏe và chưa có tải thật. Tăng tải, giảm period_size xuống 64, hoặc chạy TTS client đồng thời |
| XRUN cao ở mọi mức | Có tiến trình nền chiếm CPU, hoặc thermal throttle. Kiểm `vcgencmd measure_temp` và `get_throttled` |
| Độ trễ không giảm khi period_size giảm | Nút thắt nằm ở nơi khác — có thể ở tầng truyền LAN hoặc ở chính TTS |

### Cái phải viết ra sau bài này

Một đoạn ngắn trong `decisions.md`, đúng dạng bạn sẽ viết lại nhiều lần trong sự nghiệp robotics:

> **Quyết định:** period_size = X, periods = Y, độ trễ buffer = Z ms.
> **Lý do:** ở tải dự kiến của V1, điểm này cho XRUN < N lần/giờ trong khi giữ độ trễ dưới ngưỡng chấp nhận được. Điểm thấp hơn tiếp theo (X/2) cho XRUN gấp M lần với tải tương đương.
> **Số đo:** [link tới lab/NN]

---

# MODULE 3 — TTS VÀ QUYẾT ĐỊNH KIẾN TRÚC (14h)

---

## Bài 11 — RTF: chỉ số quyết định kiến trúc (3h)

**Câu hỏi:** "Pi yếu quá" có phải một lý do không?

### Khái niệm

Không. "Pi yếu quá" là cảm giác. **RTF là lý do.**

```
RTF = thời_gian_sinh_audio / độ_dài_audio_sinh_ra
```

RTF = 0,5 nghĩa là sinh 10 giây audio mất 5 giây — nhanh gấp đôi thời gian thực. RTF = 2,0 nghĩa là mất 20 giây để sinh 10 giây audio — không thể chạy real-time.

**Ngưỡng:** RTF < 1 là điều kiện cần để streaming. Nhưng RTF = 0,95 vẫn nguy hiểm vì không còn biên an toàn khi có tải. Thực tế nên nhắm RTF ≤ 0,5.

Đây là quyết định kiến trúc số 1 trong bốn quyết định bạn phải tự bảo vệ được. Lộ trình nói rõ: **phải đo RTF trên cả hai máy rồi mới được quyết**. Có model chạy real-time thật trên CPU — VieNeu-TTS được thiết kế cho inference real-time trên CPU ở 24kHz. Nếu đo ra RTF < 1 trên Pi thì kiến trúc ba tầng của bạn sai và nên chạy on-device.

Nói cách khác: **bạn có thể phát hiện ra kế hoạch của mình sai, và đó là kết quả tốt.** Phát hiện bằng số đo ở tuần thứ 8 rẻ hơn nhiều so với phát hiện bằng trực giác ở tuần thứ 30.

### Làm

Viết một harness benchmark tái sử dụng được (đây là code bạn sẽ dùng lại ở Khóa 4):

- Đầu vào: danh sách câu tiếng Việt có độ dài khác nhau (ngắn 5 từ, trung bình 20 từ, dài 50 từ)
- Với mỗi câu: chạy N=20 lần, bỏ 3 lần đầu (warm-up)
- Ghi: thời gian sinh, độ dài audio, RTF, **và time-to-first-chunk nếu model hỗ trợ streaming**
- Báo cáo p50, p95, p99 — không phải trung bình
- Ghi: CPU model, số core, RAM, nhiệt độ trước và sau

---

## Bài 12 — Chạy TTS tiếng Việt và đo trên cả hai máy (6h)

**Câu hỏi:** TTS nên chạy ở đâu?

### Khái niệm

**Đừng train from scratch.** Đã có sẵn nhiều lựa chọn tiếng Việt:

| Model | Đặc điểm | Lưu ý |
|---|---|---|
| **VietTTS** (dangvansam) | Server API tương thích định dạng OpenAI, clone giọng từ file audio local, cài qua pip hoặc Docker | Dễ tích hợp nhất cho V1 |
| **VieNeu-TTS** | Hướng on-device, inference real-time trên CPU ở 24kHz | Ứng viên số 1 nếu muốn chạy thẳng trên Pi |
| **Viterbox** | Fine-tune từ Chatterbox, zero-shot clone với 3–10 giây mẫu, huấn luyện trên >3.000h dữ liệu tiếng Việt | **License CC BY-NC → chỉ dùng nội bộ.** Ghi rõ điều này vào README. |
| **F5-TTS-Vietnamese** (hynt) | | |

Ở V1 chỉ cần **chọn một cái, chạy được, và đo RTF trên cả Pi lẫn LAN box.**

### Làm

1. Chọn một model. Ghi lý do chọn vào `decisions.md` (không được viết "vì nó phổ biến").
2. Chạy trên LAN box. Đo RTF bằng harness Bài 11.
3. Chạy **cùng model, cùng câu** trên Pi 5. Đo lại.
4. Nếu model quá nặng cho Pi, thử một model on-device (VieNeu-TTS) trên Pi và ghi rõ là so sánh hai model khác nhau — đừng giả vờ là cùng một phép đo.
5. Đo nhiệt độ Pi trong lúc chạy. Kiểm `get_throttled` sau.
6. **Viết quyết định kiến trúc, kèm số.**

### Số phải ra

| Máy | RTF kỳ vọng | Kết luận |
|---|---|---|
| LAN box (CPU desktop) | 0,1–0,5 | Chạy được thoải mái |
| LAN box có GPU | <0,1 | Dư sức |
| Pi 5, model nặng | 1,5–5 | Không chạy real-time được |
| Pi 5, model on-device tối ưu | Có thể <1 | **Nếu ra kết quả này, kiến trúc của bạn cần xem lại** |

Và: nhiệt độ Pi khi chạy TTS liên tục. Nếu vượt 80°C hoặc `get_throttled` khác 0, bạn có một ràng buộc nhiệt cần ghi vào kiến trúc.

### Nếu ra khác

| Triệu chứng | Ý nghĩa |
|---|---|
| RTF trên Pi < 1 | Kiến trúc ba tầng không cần thiết cho V1. **Ghi lại, và vẫn giữ ba tầng nếu lý do là để học kiến trúc production** — nhưng phải nói rõ đó là lý do, không được nói "vì Pi yếu" |
| RTF dao động mạnh giữa các lần | Thermal throttle, hoặc swap. Kiểm nhiệt độ và RAM |
| Model không chạy nổi trên Pi (OOM) | Ghi lại giới hạn RAM. Đây là số thật cho power/resource budget về sau |

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
3. **Nút kill**: một endpoint dừng mọi phát, xả queue, và một nút vật lý (GPIO) làm điều tương tự. Nút vật lý quan trọng vì lúc cần dừng gấp thì không ai mở laptop.
4. Log mọi quyết định duyệt: ai duyệt, lúc nào, nội dung gì.
5. **Test kill switch 10 lần**, trong đó ≥3 lần đúng lúc đang phát giữa câu.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Nội dung chưa duyệt | **Không bao giờ** đến được player. Chứng minh bằng test tự động. |
| Bấm kill giữa lúc đang phát | Âm thanh dừng trong <1s, queue xả sạch, hệ thống vẫn sống |
| Sau kill, khởi động lại | Không tự động phát lại thứ đã bị kill |

---

## Bài 16 — Player daemon, ring buffer, systemd (5h)

**Câu hỏi:** làm sao để nó tự sống khi không ai nhìn?

### Làm

1. Đóng gói player thành daemon (Rust hoặc Python), chạy dưới `systemd` với `Restart=always`.
2. **Ring buffer** giữa network receive và ALSA write — để jitter mạng không thành XRUN.
3. Bật **hardware watchdog** của Pi. Daemon phải "vỗ" watchdog định kỳ; nếu treo, Pi tự reset.
4. Structured logging (JSON lines). Yêu cầu: phải trả lời được câu hỏi *"3h sáng thứ Bảy nó làm gì"* chỉ bằng cách grep log.
5. **Log rotation.** Thẻ SD hỏng vì ghi nhiều là chuyện có thật, không phải lo xa.
6. Xử lý ba tình huống lỗi: mất mạng, Google API lỗi, TTS worker chết. Mỗi cái có hành vi xác định và được log.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| `kill -9` daemon | systemd khởi động lại trong <5s, không mất record trong queue |
| Ngắt mạng 10 phút | Log ghi rõ, tự phục hồi khi có mạng, không crash loop |
| Treo daemon giả lập (sleep vô hạn) | Watchdog reset Pi |
| Làm đầy 90% thẻ nhớ | Log rotation kích hoạt, hệ thống vẫn chạy |

---

## Bài 17 — TN-5: 72 giờ không ai trông (6h người, 72h treo máy)

**Câu hỏi:** nó có thật sự chạy được không, hay chỉ chạy được lúc bạn đang nhìn?

Thí nghiệm bắt buộc số 5, tiêu chí PASS số 7 của M4 — và là tiêu chí khắt khe nhất.

### Làm

Chạy liên tục 72 giờ, trong đó:

1. ≥20 confession thật được phát đúng
2. **0 lần can thiệp tay**
3. **Rút điện đột ngột 10 lần**, trong đó ≥3 lần đúng lúc đang ghi DB. Bật lại. Kiểm dữ liệu.
4. Chứng minh log rotation bằng cách **cố tình làm đầy thẻ**
5. Theo dõi nhiệt độ CPU suốt 72h, vẽ đồ thị
6. Đo dòng tiêu thụ trung bình bằng USB power meter ← **số đầu tiên trong power budget về sau**

### Số phải ra

| Đại lượng | Giá trị chấp nhận |
|---|---|
| Confession phát đúng | ≥20 |
| Lần can thiệp tay | **0** |
| Mất dữ liệu sau 10 lần rút điện | **0** |
| Nhiệt độ CPU tối đa | <80°C, không throttle |
| Dòng tiêu thụ trung bình | Ghi lại — Pi 5 nhàn thường 3–4W, có tải 7–9W |
| XRUN trong 72h | Ghi lại con số, so với dự đoán từ Bài 10 |

**Về việc rút điện:** đây là bài test mà phần lớn hệ thống tự chế trượt. SQLite với WAL mode và `synchronous=FULL` sẽ sống sót; SQLite mặc định thì có thể không. Nếu bạn mất dữ liệu, **đó là kết quả tốt** — nó dạy bạn về durability ở tầng mà backend thường được framework che cho.

---

# GATE KHÓA 3 (6h)

Đối chiếu đúng 7 tiêu chí PASS của M4. Nhị phân, không chấm bằng cảm giác.

```
[ ] 1. Không còn lời gọi cloud TTS nào trong chuỗi
       → grep repo, chứng minh bằng CI check

[ ] 2. TN-1: BCK đo được sai <1% so với dự đoán, ở 2 sample rate khác nhau
       → file .sr commit sau prediction.md, kèm bảng dự đoán vs đo

[ ] 3. TN-2: đường cong latency vs underrun ≥5 điểm period_size,
       mỗi điểm ≥10 phút chạy; latency GPIO→mic đo được với độ phân giải ≤1ms

[ ] 4. TN-3: bảng ≥3 cấu hình nguồn, mỗi dòng có V_rail lúc nghỉ và lúc phát,
       cờ get_throttled, mô tả tiếng

[ ] 5. TN-4: F0 giọng mình bằng số; đồ thị SNR đo vs lý thuyết 6.02×bits+1.76
       ở 4 mức bit depth, sai lệch <3dB

[ ] 6. Bảng latency budget: MỌI DÒNG là số đo, không dòng nào là ước tính,
       nút thắt được chỉ tên

[ ] 7. TN-5 soak 72h: ≥20 confession phát đúng, 0 lần can thiệp tay,
       log rotation đã chứng minh bằng cách cố tình làm đầy thẻ,
       ≥3 lần rút điện đúng lúc đang ghi DB mà dữ liệu còn nguyên
```

**FAIL → action (cam kết trước, không bàn lại lúc nản):** chạm 140h chưa PASS → **cắt scope, không gia hạn**. Bỏ tiêu chí 5 và 7, chỉ giữ "phát được audio ổn định 24h", publish nguyên trạng kèm ghi chú rõ cái gì chưa làm được, sang Khóa 4. V1 không được phép ăn hết năm đầu.

---

# LỊCH 12 TUẦN

| Tuần | Giờ | Làm | Xong thì có |
|---|---|---|---|
| 1 | 7 | Bài 1–2 · dựng Pi, I2S, DAC | Nghe được tiếng đầu tiên |
| 2 | 7 | Bài 3 (TN-1) | **Nhìn thấy âm thanh trên dây** |
| 3 | 7 | Bài 4 (ALSA) | Player riêng, không dùng aplay |
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

1. **Pi 5 không có jack 3.5mm.** Bắt buộc I2S hoặc USB.
2. **I2S trên Pi cần overlay** trong `/boot/firmware/config.txt` và nó chiếm GPIO 18/19/21. Đừng dùng những chân đó cho việc khác.
3. **Chân SCK của module PCM5102A thường cần nối GND** để dùng PLL nội. Không nối, DAC im lặng và bạn sẽ nghĩ nó hỏng.
4. **Đừng nối loa trực tiếp vào line-out của DAC.** Sai trở kháng, không đủ dòng, có thể làm chết DAC.
5. **Logic analyzer clone 24MHz** đủ cho I2S ở 768kHz nhưng chật vật ở sample rate cao. Biết giới hạn của dụng cụ đo cũng là một phần của việc đo.
6. **Mua 2 cái cho mọi module rẻ và quan trọng.** Không có module thứ hai để so, bạn không phân biệt được "module chết" với "cấu hình sai".
7. **`plughw` và `default` của ALSA sẽ nói dối bạn** — chúng resample ngầm. Dùng `hw:0,0` và chấp nhận lỗi thật.

---

# NGUỒN HỌC KÈM KHÓA 3

| Nguồn | Xem/đọc phần nào | Cho bài nào |
|---|---|---|
| **Datasheet PCM5102A** (TI) | Pin config, timing diagram, chế độ FMT | Bài 2, 3 |
| **Datasheet INMP441** | Định dạng khung I2S, dải động, độ nhạy | Bài 7 |
| **ALSA Project docs** — `alsa-project.org` | PCM interface, period/buffer, XRUN handling | Bài 4, 10 |
| **"A close look at ALSA"** và các bài về `snd_pcm_hw_params` | Cấu hình hw params | Bài 4 |
| **sigrok/PulseView docs** — decoder I2S | | Bài 3, 9 |
| **Raspberry Pi docs** — device tree overlays, `vcgencmd` | | Bài 2, 6 |
| **Ben Eater** (YouTube) — series về clock và tín hiệu số | | Bài 3 |
| **VietTTS / VieNeu-TTS / Viterbox** — README của từng repo | | Bài 12 |
| **Making Embedded Systems** — Elecia White | Chương về debugging và về thời gian | Toàn khóa |

Vẫn giữ quy tắc ba nguồn: một nguồn chính + một tra cứu + datasheet. Ở khóa này **datasheet là nguồn quan trọng nhất**, vì mọi con số "phải ra" đều bắt nguồn từ đó.

---

# SAU KHÓA 3

**Khóa 4 — Đo hiệu năng inference trên edge (70h).** Không cần mua gì mới, thuê GPU theo giờ. Harness benchmark bạn viết ở Bài 11 dùng lại được gần như nguyên vẹn, chỉ đổi payload từ TTS sang VLA model. Đây là artifact ★ thứ hai và nó tạo tín hiệu phỏng vấn nhanh hơn Khóa 3.

**Nhắc lần cuối:** nếu Khóa 2 vẫn chưa xong khi bạn đọc dòng này, dừng Khóa 3 lại và đóng Khóa 2 trước. Khóa 3 là thứ khiến bạn không bị loại. Khóa 2 là thứ khiến bạn được gọi.
