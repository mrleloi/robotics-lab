# KHÓA 1 — PHẦN C: ĐO THẬT (14h)

Từ phần này, mọi bài đi theo cùng một vòng: **viết dự đoán bằng số → commit → mới cắm que đo → so → giải thích chỗ lệch**. Vòng này có tên chuẩn: *preregistration* (→ F1.7). Không phải nghi thức. Nếu bạn đo trước rồi mới "dự đoán", bạn sẽ luôn đúng, và sẽ không học được gì.

Bạn mang vào phần này từ Bài 1–8: định luật Ohm và công suất, "điện áp luôn là giữa hai điểm", GND là mốc, đo áp song song / đo dòng nối tiếp / đo trở khi rời mạch, mã màu điện trở, cấu trúc breadboard, PulseView chạy được với logic analyzer (đã qua Zadig), và hàn được chân module.

| Bài | Giờ | Viên nang nền nên đọc trước | Thư mục lab |
|---|---|---|---|
| Bài 9 — Voltage divider: thí nghiệm đầu tiên có dự đoán | 5 | F1.1 (phần sai số dụng cụ và lan truyền), F1.7 (đọc lướt) | `lab/01-voltage-divider/` |
| Bài 10 — LED và điện trở: tại sao, bằng số | 5 | F1.1; F1.6 nếu làm phần fit tùy chọn | `lab/02-led-current/` |
| Bài 11 — Đọc trọn một datasheet | 4 | F1.2 (đoạn "typical không phải phân bố") | `lab/03-datasheet/` |

Giờ ở bảng là giờ gốc `[ước lượng]`. Phần mô phỏng Python và các câu hỏi ngược thêm khoảng 1h mỗi bài; nếu tuần đó chật, làm phần 5–8 trước, phần 9–10 để tuần sau.

**Cấu trúc một thư mục lab** (dùng cho cả Khóa 1):

```
lab/01-voltage-divider/
  prediction.md     ← commit TRƯỚC khi cắm mạch (Bài 14 kiểm bằng git log)
  analysis.md       ← bảng dự đoán / đo / chênh lệch, và lời giải thích
  photos/           ← ảnh mạch, ảnh màn hình đồng hồ ở các phép đo quan trọng
```

---

## Bài 9 — Voltage divider: thí nghiệm đầu tiên có dự đoán (5h)

> **Vị trí:** Bài 8 (mỏ hàn) → **Bài 9** → Bài 10 (LED) · **Cần trước:** Bài 1, 5, 6; F1.1 · **Sau bài này bạn quyết định được:** một con số đo lệch so với tính toán là "bình thường, nằm trong sai số" hay "có gì đó sai, dừng lại tìm" — và dụng cụ của bạn có đủ tốt cho mạch này không.

### 1. Câu chuyện — ai đã khổ vì chuyện này

Hai câu chuyện, một bài học.

**Đồng hồ làm hỏng phép đo.** Đồng hồ kim thời trước (moving-coil) lấy dòng từ chính mạch để làm kim quay. Chất lượng của nó được ghi bằng "ohm trên volt" — một đồng hồ 20 kΩ/V ở thang 10 V chỉ là một điện trở 200 kΩ cắm song song vào mạch `[chuẩn]`. Đo trên mạch có điện trở lớn (mạch bias của đèn điện tử, mạch transistor) thì số đọc sai vài chục phần trăm, và người kỹ thuật phải nhớ "thang nào, đồng hồ nào" để hiệu chỉnh. Vôn kế đèn điện tử (VTVM) ra đời chính để giải quyết chuyện này: trở kháng vào cỡ 10 MΩ, không đổi theo thang `[chuẩn]`. Con số "~10 MΩ" trên đồng hồ số của bạn hôm nay là di sản trực tiếp của cuộc chiến đó. Nó tốt hơn nhiều, nhưng **không phải vô hạn**, và bài này sẽ cho bạn thấy nó bằng số.

**Dự đoán trước làm thay đổi kết quả.** Kaplan và Irvin (PLOS ONE, 2015) xem lại các thử nghiệm lâm sàng lớn về tim mạch do NHLBI (Mỹ) tài trợ. Trước năm 2000, khi chưa bắt buộc đăng ký trước kết cục chính trên ClinicalTrials.gov, khoảng 57% thử nghiệm báo lợi ích; sau khi bắt buộc, còn khoảng 8% `[chuẩn — số theo bài báo, kiểm lại nếu trích dẫn]`. Thuốc không tệ đi. Cái thay đổi là người ta không còn chọn kết cục *sau khi* thấy số. `prediction.md` của bạn là phiên bản một người của cơ chế đó.

### 2. Mô hình tư duy

```
        Vin (5V của ESP32, đo lại)
         │
        ┌┴┐
        │ │ R1           Dòng I như nhau qua R1 và R2 (nối tiếp, không có chỗ rẽ)
        └┬┘              I = Vin / (R1 + R2)
         ├──────────┬─── Vout = I·R2 = Vin · R2 / (R1 + R2)
        ┌┴┐        ┌┴┐
        │ │ R2     │ │ R_in của đồng hồ (~10 MΩ, tra manual)   ← khi bạn cắm que,
        └┬┘        └┬┘                                           nó thành một nhánh rẽ
         ├──────────┘
        GND
```

Ba ý cốt lõi:

1. **Divider là một tỉ số, không phải một điện áp.** Vout/Vin = R2/(R1+R2). Vin trôi bao nhiêu phần trăm, Vout trôi đúng bấy nhiêu phần trăm. Vì vậy luôn đo Vin trước và tính lại dự đoán theo Vin thật.
2. **Mỗi con số có một khoảng, không phải một điểm.** Điện trở ±5% là *dung sai sản xuất*: con điện trở bạn cầm có giá trị cố định nào đó trong khoảng ±5% quanh danh định. Đồng hồ có sai số ±(a% số đọc + b digit) theo thang. Dự đoán đúng là một **dải**, và dải đó **không giống nhau cho mọi tỉ lệ** (xem phần 5).
3. **Dụng cụ đo là một linh kiện trong mạch.** Khi que đo chạm vào, R_in nằm song song với R2. Ảnh hưởng của nó phụ thuộc vào tỉ số giữa R_in và điện trở "nhìn thấy" từ điểm đo — không phụ thuộc vào việc đồng hồ "tốt hay xấu" một cách tuyệt đối.

**Lan truyền sai số cho divider** (→ F1.1). Gọi tỉ số k = R2/(R1+R2). Độ nhạy tương đối của k theo từng điện trở:

```
∂ln k / ∂ln R2 = + R1/(R1+R2)
∂ln k / ∂ln R1 = − R1/(R1+R2)
```

- **Trường hợp xấu nhất** (worst case, hai điện trở lệch ngược chiều): `|Δk/k| ≤ R1/(R1+R2) · (t1 + t2)` với t là dung sai tương đối.
- **Thống kê** (GUM loại B, coi dung sai là phân bố đều trên ±t → độ lệch chuẩn t/√3, hai điện trở độc lập): `u(k)/k = R1/(R1+R2) · √(t1² + t2²) / √3`.

Hệ số R1/(R1+R2) là chìa khóa: cùng bộ điện trở ±5%, có tỉ lệ cho dải rộng, có tỉ lệ cho dải hẹp. Bạn sẽ tự tính ở phần 5.

**Mô phỏng đồ chơi** — chạy trước khi đụng phần cứng. Code dùng một cặp **khác** với cặp trong lab (2.2 kΩ / 4.7 kΩ, ±1%) để bạn thấy phương pháp mà không thấy đáp án; sửa `PAIRS` thành các cặp của bạn *sau khi* đã tính tay.

```python
# [đã chạy] Monte Carlo cầu phân áp: dung sai điện trở + tải của đồng hồ
import numpy as np

rng = np.random.default_rng(0)
N = 100_000
PAIRS = [(2.2e3, 4.7e3, 0.01), (2.2e6, 4.7e6, 0.01)]  # (R1, R2, dung sai) — KHÔNG phải cặp trong lab
VIN, R_IN = 5.00, 10e6                                 # R_IN: tra manual đồng hồ của bạn

def simulate(R1, R2, tol):
    # Dung sai: phân bố đều trên [−tol, +tol] (giả định GUM loại B hình chữ nhật)
    r1 = R1 * (1 + rng.uniform(-tol, tol, N))
    r2 = R2 * (1 + rng.uniform(-tol, tol, N))
    ideal = VIN * r2 / (r1 + r2)
    r2_loaded = r2 * R_IN / (r2 + R_IN)          # đồng hồ nằm song song với R2
    loaded = VIN * r2_loaded / (r1 + r2_loaded)
    return ideal, loaded

for R1, R2, tol in PAIRS:
    ideal, loaded = simulate(R1, R2, tol)
    nominal = VIN * R2 / (R1 + R2)
    lo, hi = np.percentile(ideal, [0.5, 99.5])
    print(f"R1={R1:.0f} Ω  R2={R2:.0f} Ω  dung sai ±{tol:.0%}")
    print(f"  danh định            : {nominal:.4f} V")
    print(f"  99% do dung sai      : {lo:.4f} … {hi:.4f} V (±{(hi - lo) / 2 / nominal:.2%})")
    print(f"  trung bình khi đo bằng đồng hồ R_in={R_IN/1e6:.0f} MΩ: "
          f"{loaded.mean():.4f} V (lệch {loaded.mean() / nominal - 1:+.2%})")
```

Với cặp mẫu, bạn sẽ thấy hai dòng "99% do dung sai" giống hệt nhau (tỉ lệ như nhau), nhưng dòng "khi đo bằng đồng hồ" của cặp megaohm lệch hẳn. Đó là toàn bộ bài này trong hai dòng in ra.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Chuỗi service nối tiếp trên một request path: cùng throughput qua mọi hop, tổng latency = tổng latency từng hop | Nối tiếp: cùng dòng I qua R1 và R2; điện áp rơi trên mỗi điện trở tỉ lệ với R của nó, cộng lại bằng Vin (KVL) | Trong backend, throughput do client quyết định; ở đây I do **chính tổng R** quyết định (Vin cố định). Đổi R2 thì dòng qua R1 cũng đổi — không có "hop độc lập" | Tưởng thay R2 chỉ ảnh hưởng điện áp trên R2, quên rằng điện áp trên R1 cũng đổi |
| Probe effect / Heisenbug: bật tracing làm thay đổi timing, bug biến mất | Đồng hồ R_in song song với R2 kéo Vout xuống | Trong phần mềm overhead thường cộng thêm và khó dự đoán; ở đây ảnh hưởng **tính được chính xác** từ R_in và điện trở của mạch, và có thể hiệu chỉnh | Hoặc bỏ qua hoàn toàn (đo mạch MΩ rồi kết luận mạch sai), hoặc nghi ngờ mọi phép đo (tê liệt) |
| Config `replicas: 3` vs số pod thật đang chạy | Giá trị danh định trên vòng màu vs giá trị thật của con điện trở | Pod có thể đổi theo thời gian; con điện trở **cố định** (bỏ qua nhiệt độ) — sai lệch của nó là hệ thống, đo lại 100 lần vẫn lệch y như thế | Lấy trung bình nhiều lần đo để "khử" dung sai — không khử được, chỉ khử được nhiễu ngẫu nhiên |
| Số chữ số của một metric trên dashboard | Số chữ số trên màn hình đồng hồ | Dashboard in `3.28471` vì float; đồng hồ in 3 chữ số nhưng chỉ bảo đảm ±(0.5% + 2 digit) | Ghi "đo được 2.503 V" rồi so lệch 0.1% với dự đoán — lệch đó nhỏ hơn sai số của chính đồng hồ, không có nghĩa |

**Chấm mô hình:**

- *"Điện trở ±5% nghĩa là mỗi lần đo giá trị dao động ±5%."* — **SAI.** Dung sai là độ phân tán **giữa các con** khi sản xuất (sai số hệ thống của một con cụ thể), không phải nhiễu giữa các lần đo. Phản ví dụ: đo một con "10 kΩ" mười lần, cả mười lần ra cùng một số (ví dụ 9.87 kΩ) trong phạm vi 1 digit. Muốn biết giá trị thật thì đo nó (loại A, có sai số của đồng hồ), không lấy trung bình dung sai.
- *"Đồng hồ có trở kháng vào 10 MΩ thì coi như không ảnh hưởng."* — **ĐÚNG MỘT PHẦN.** Đúng khi điện trở nhìn từ điểm đo nhỏ hơn R_in hàng nghìn lần (mạch kΩ). Gãy khi mạch có điện trở cỡ MΩ: lúc đó R_in là một linh kiện ngang hàng. Phản ví dụ: thí nghiệm 1 MΩ ở phần 6.
- *"Divider hạ 5 V xuống 3.3 V được thì dùng nó cấp nguồn cho cảm biến 3.3 V."* — **SAI.** Divider chỉ cho đúng tỉ số khi dòng lấy ra ở điểm giữa rất nhỏ so với dòng qua R2. Cảm biến kéo dòng thay đổi theo thời gian → nó là một "R_in" thay đổi → Vout sụp và nhảy. Divider dùng cho **tín hiệu** (đọc mức áp, đọc pin bằng ADC trở kháng cao), không dùng cho **nguồn**. Đây là lý do có LDO và buck (→ K7 C1.4).

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | Voltage divider (cầu phân áp) | Hai điện trở nối tiếp, điểm giữa cho Vin·R2/(R1+R2) khi không có tải | Một "bộ hạ áp" dùng được cho nguồn |
| 🟢 | Tolerance (dung sai) | Khoảng mà nhà sản xuất bảo đảm giá trị thật nằm trong đó | Nhiễu ngẫu nhiên giữa các lần đo |
| 🟢 | Accuracy spec ±(a% + b digit) | Sai số giới hạn của đồng hồ ở một thang: a% của số đọc cộng b lần chữ số cuối | Chỉ có phần trăm; quên phần digit (ở số đọc nhỏ, phần digit chiếm ưu thế) |
| 🟢 | Resolution vs accuracy | Chữ số nhỏ nhất hiển thị vs độ đúng được bảo đảm | Hiển thị 3 chữ số = đúng 3 chữ số |
| 🟢 | Loading / probe loading (hiệu ứng tải) | Dụng cụ đo lấy dòng hoặc thêm nhánh vào mạch, làm đổi đại lượng cần đo | Lỗi của đồng hồ "dỏm" |
| 🟢 | Input impedance (trở kháng vào) | Điện trở tương đương giữa hai que khi đồng hồ ở chế độ đo áp | Vô hạn |
| 🟡 | Lan truyền sai số (propagation of uncertainty) | Tính sai số của kết quả từ sai số của từng đầu vào, qua đạo hàm/độ nhạy | Cộng phần trăm của mọi thứ lại |
| 🟡 | GUM loại A / loại B | A: ước lượng từ thống kê các lần đo lặp; B: từ thông tin khác (spec, dung sai, manual) | Chỉ loại A mới "là sai số thật" |
| 🟡 | Thevenin equivalent | Mọi mạch tuyến tính nhìn từ hai điểm = một nguồn áp nối tiếp một điện trở | (🟡 ở bài này: chỉ cần biết divider nhìn từ điểm giữa = Vout nối tiếp R1‖R2) |
| 🔴 | Hệ số nhiệt điện trở (tempco, ppm/°C) | Giá trị trôi theo nhiệt độ | Không cần ở Khóa 1; quay lại khi đo chính xác ở K5 |

### 5. Dự đoán

**Đề bài.** Bốn cặp điện trở, nguồn là chân 5V của ESP32 đang cắm USB:

| Cặp | R1 | R2 | Ghi chú |
|---|---|---|---|
| A | 10 kΩ | 10 kΩ | |
| B | 10 kΩ | 1 kΩ | |
| C | 1 kΩ | 10 kΩ | |
| D | 1 MΩ | 1 MΩ | thí nghiệm tải — dự đoán **hai lần**: không tính và có tính R_in |

Với mỗi cặp, dự đoán: (1) Vout danh định; (2) dải do dung sai điện trở — cả worst case và ±2u (thống kê); (3) sai số đồng hồ ở thang bạn sẽ dùng; (4) dải chấp nhận cuối cùng. Với cặp D, dự đoán thêm: điện áp đo được trên R2, điện áp đo được trên R1 (que đỏ ở đầu trên R1, que đen ở điểm giữa), và **tổng hai số đó** so với Vin.

**Tham số cần tra, tra ở đâu:**

- Sai số DCV của UT33D+ theo từng thang, số count (bao nhiêu chữ số), và **trở kháng vào ở chế độ DCV**: bảng thông số trong manual UT33+ series (bản PDF của UNI-T hoặc tờ giấy trong hộp). Ghi lại một chữ số cuối ("1 digit") ở thang 2 V và 20 V bằng bao nhiêu volt.
- Thang Ω nào có trên đồng hồ của bạn (có thang 2 MΩ không, hay chỉ 200 kΩ rồi nhảy lên 20 MΩ?) và sai số của nó — cần cho bước đo lại điện trở.
- Dung sai từ vòng màu cuối của từng con điện trở bạn dùng (Bài 5). Kit điện trở 5 vòng thường là ±1% (nâu); 4 vòng thường ±5% (vàng kim).

**Công thức:** phần 2 (divider, lan truyền). Với cặp D có tải: thay R2 bằng R2‖R_in = R2·R_in/(R2+R_in). Với phép đo trên R1, thay R1 bằng R1‖R_in và giữ R2 nguyên.

**Mẫu `prediction.md`** — copy, điền, commit:

```markdown
# lab/01-voltage-divider/prediction.md
Ngày: YYYY-MM-DD · Commit trước khi cắm bất kỳ linh kiện nào.

## Dụng cụ (tra trước)
- Đồng hồ: UNI-T UT33D+ · thang DCV dùng cho Vout lớn: ___ (1 digit = ___ V) · cho Vout nhỏ: ___ (1 digit = ___ V)
- Sai số DCV (manual): ±(___ % + ___ digit)
- Trở kháng vào DCV (manual): ___ MΩ (trang/mục: ___)
- Dung sai điện trở: cặp A–C ±___ % · cặp D ±___ %

## Vin
- Danh định 5 V. Sẽ đo lại; mọi dự đoán dưới đây tính lại theo Vin đo được trong analysis.md.

## Dự đoán (theo Vin = 5.00 V)
| Cặp | Vout danh định | Hệ số R1/(R1+R2) | Dải worst case (V) | Dải ±2u (V) | Sai số đồng hồ (V) | Dải chấp nhận (V) |
|---|---|---|---|---|---|---|
| A 10k/10k | | | | | | |
| B 10k/1k  | | | | | | |
| C 1k/10k  | | | | | | |
| D 1M/1M (không tải) | | | | | | |
| D 1M/1M (có R_in)   | | | | | | |

## Thí nghiệm tải (cặp D)
- V trên R2 dự đoán: ___ V · V trên R1 dự đoán: ___ V · Tổng: ___ V so với Vin ___ V
- R_in sẽ tính ngược từ số đo bằng công thức: ___

## Điều gì sẽ làm tôi đổi ý
- Nếu cặp ___ lệch ngoài dải chấp nhận sau khi đã hiệu chỉnh Vin, tôi sẽ nghi ___ trước, rồi ___.
```

Không dùng AI hay máy tính bỏ túi có lưu lịch sử ở bước này. Tính tay, sai cũng được — sai ở đây chính là dữ liệu.

### 6. Làm

**Bước 1 — commit `prediction.md`.** `git add` + `git commit`. Bài 14 kiểm thứ tự commit bằng script.

**Bước 2 — đo từng điện trở khi chưa cắm vào mạch.** Chế độ Ω, linh kiện rời, chỉ cầm một đầu (Bài 5). Ghi giá trị đo của cả 8 con vào `analysis.md`, kèm thang và sai số ±(0.8% + 2 digit) `[spec, kiểm manual]` của thang đó. Bước này tách "dung sai sản xuất" khỏi "lỗi lắp mạch" ở bước sau.

> Sai số dụng cụ: ở thang 20 kΩ, một con 10 kΩ đọc ra với 1 digit = 10 Ω. Nếu đồng hồ không có thang 2 MΩ, con 1 MΩ đo ở thang 20 MΩ chỉ còn 3 chữ số (1 digit = 10 kΩ) — sai số tương đối lớn hơn nhiều. Ghi rõ.

**Bước 3 — dựng mạch cặp A.** Breadboard: chân 5V của ESP32 → R1 → điểm giữa → R2 → GND của ESP32. Hai điện trở cắm ở hai hàng khác nhau, chung một hàng ở điểm giữa. ESP32 không cần firmware gì đặc biệt, chỉ cần cấp USB.

**Bước 4 — đo Vin.** Que đen GND, que đỏ chân 5V. Ghi kèm thang. Con số này hiếm khi đúng 5.00 V: nhiều DevKit có diode hoặc công tắc nguồn giữa cổng USB và chân 5V, và cổng USB của máy tính tự nó cũng dao động `[tự đo]`. **Tính lại dự đoán theo Vin đo được** trước khi nhìn Vout.

**Bước 5 — đo Vout cặp A, rồi B, C.** Mỗi lần đổi cặp, đo lại Vin (nó có thể trôi). Với cặp B (Vout nhỏ), chọn thang cho nhiều chữ số nhất mà không tràn — đổi thang làm đổi phần "digit" của sai số. Nếu số đọc nhảy, ghi khoảng nhảy, không ghi một số đẹp.

Thói quen REP-103 bắt đầu từ đây: mọi con số kèm đơn vị SI (`V`, `A`, `Ω`, `s`, `Hz`). Không ghi "2.5" trần trụi. Từ Khóa 2 trở đi đây là quy ước dữ liệu của cả repo (`CONVENTIONS.md`).

**Bước 6 — dự đoán lần hai bằng giá trị đo được.** Thay R danh định bằng R đo ở bước 2, Vin bằng Vin đo ở bước 4. Lúc này dải chấp nhận chỉ còn sai số đồng hồ (của Vin, Vout và hai R). Cột này trong `analysis.md` là cột quan trọng nhất: nếu lệch ngoài dải *này*, có lỗi thật.

**Bước 7 — thí nghiệm tải, cặp D (1 MΩ / 1 MΩ).** Mã màu 1 MΩ: nâu–đen–lục (vòng ba là 5 số 0).

1. Đo V trên R2 (que đen GND, que đỏ điểm giữa).
2. Đo V trên R1 (que đen điểm giữa, que đỏ chân 5V). Đây là lần đầu bạn đo áp mà que đen *không* ở GND — đúng theo Bài 1: điện áp là giữa hai điểm.
3. Cộng hai số. So với Vin. Với cặp A, làm lại đúng thao tác này để có đối chứng.

Phép cộng này là **phép thử không phụ thuộc dung sai**: dù hai con 1 MΩ lệch nhau bao nhiêu, nếu đồng hồ không tải mạch thì tổng phải bằng Vin (KVL). Nếu tổng hụt, phần hụt là do đồng hồ.

4. **Tính ngược R_in** từ số đo trên R2 (dùng R1, R2 đã đo ở bước 2). Gọi R_eq là điện trở tương đương phía dưới khi có đồng hồ:

```
R_eq = R1 · Vout / (Vin − Vout)        (từ Vout = Vin · R_eq / (R1 + R_eq))
1/R_in = 1/R_eq − 1/R2
```

So R_in tính được với số trong manual. Lệch bao nhiêu thì bình thường? Thử thay Vout ±1 digit, rồi R1, R2 ±1 digit vào công thức để thấy R_in nhảy bao nhiêu, và ghi dải đó vào `analysis.md` thay vì một con số.

**Bước 8 — `analysis.md`.** Bảng: cặp · Vin đo · Vout dự đoán (danh định) · Vout dự đoán (R đo) · Vout đo · chênh lệch % · dải chấp nhận · trong/ngoài. Thêm một đoạn ≤5 câu bằng lời của bạn: phép đo làm thay đổi thứ được đo như thế nào, và khi nào được phép bỏ qua. Câu này sẽ quay lại ở dạng khó hơn nhiều khi đo đồng bộ thời gian (→ K5 Bài 7) và khi đọc điện áp pin bằng ADC (→ K7 C1.2).

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

Tính với Vin = 5.00 V, điện trở ±5%, đồng hồ ±(0.5% + 2 digit) `[spec UT33+ series]`, R_in = 10 MΩ `[spec — kiểm manual của bạn]`. Nếu Vin của bạn khác, nhân mọi số Vout với Vin_đo/5.00.

| Cặp | Vout danh định | R1/(R1+R2) | Dải worst case do dung sai | Sai số đồng hồ (thang) | Ghi chú |
|---|---|---|---|---|---|
| A 10k/10k | 2.500 V | 0.50 | 2.375 – 2.625 V (±5.0%) | ±0.033 V (20 V, 1 digit 0.01 V) | |
| B 10k/1k | 0.4545 V | 0.909 | 0.415 – 0.498 V (−8.7% / +9.5%) | ±0.004 V (2 V, 1 digit 0.001 V) | dải rộng nhất |
| C 1k/10k | 4.545 V | 0.091 | 4.502 – 4.585 V (±0.9%) | ±0.043 V (20 V) | dải hẹp nhất; ở đây sai số đồng hồ ngang dung sai |
| D 1M/1M không tải | 2.500 V | 0.50 | 2.375 – 2.625 V | ±0.033 V | |
| D 1M/1M có R_in 10 MΩ | **≈ 2.381 V** (−4.8%) | | | | rơi **vào trong** dải dung sai không tải |

Dải thống kê ±2u nhỏ hơn worst case: với cặp A là khoảng ±4.1% (2 × 0.5 × √2 × 5%/√3).

**Bốn điều phải thấy:**

1. **Cặp B lệch nhiều nhất là bình thường.** Hệ số 0.909 khuếch đại dung sai gần gấp đôi so với cặp A. Bản gốc của khóa đặt ±5% cho mọi cặp — sai: với cặp B, một mạch lắp đúng hoàn toàn có thể lệch tới ~9%; với cặp C, ±5% lại quá rộng, không bắt được lỗi cắm nhầm 1.2 kΩ thay cho 1 kΩ (cho 4.46 V, vẫn lọt dải ±5%).
2. **Sau khi dùng R đo được (bước 6), mọi cặp A–C phải lệch ≲1.5%** — chỉ còn sai số đồng hồ. Lệch hơn thế: nghi lắp mạch, tiếp xúc breadboard, hoặc đọc nhầm thang.
3. **Thí nghiệm tải:** với cặp D, mỗi số đo trên R1 và R2 ≈ 2.38 V, tổng ≈ 4.76 V, **hụt ~4.8% so với Vin**. Với cặp A, tổng bằng Vin trong sai số đồng hồ. Phép thử tổng hoạt động bất kể dung sai: tính lại với R1 = 1.05 MΩ, R2 = 0.95 MΩ vẫn cho tổng ≈ 4.76 V.
4. **Chỉ nhìn Vout cặp D thì không kết luận được gì:** 2.38 V vẫn nằm trong dải ±5% của dung sai. Bản gốc nói "bạn sẽ thấy số thấp hơn rõ rệt" — chỉ đúng nếu bạn đã đo R (bước 2) hoặc dùng phép thử tổng (bước 7). Đây là ví dụ đầu tiên của bài học "hiệu ứng nhỏ hơn độ bất định thì không nhìn thấy được, dù nó có thật" (→ F1.5, power).

**R_in tính ngược:** chỉ kỳ vọng **đúng bậc** (vài MΩ tới ~15 MΩ), không kỳ vọng 10.0 MΩ. Lý do: công thức trừ hai số gần nhau (1/R_eq − 1/R2), nên sai số đầu vào bị khuếch đại. Riêng 1 digit (0.01 V) trên Vout ≈ 2.38 V đã làm R_in nhảy cỡ ±1 MΩ; sai số ~3% của R1, R2 đo ở thang 20 MΩ (3 chữ số) làm R_in nhảy tới ~30%. Đây là bài học lan truyền sai số thứ hai của bài: có những đại lượng tính được nhưng không đo chính xác được bằng dụng cụ đang có. Nếu ra ~1 MΩ hoặc ~100 MΩ (sai bậc), xem phần 8.

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Vout = Vin | R2 hở: cắm nhầm hàng, chân không tiếp xúc | Thông mạch từ điểm giữa xuống GND qua R2 (tắt nguồn) | Cắm lại, đổi hàng breadboard |
| Vout = 0 | R1 hở, hoặc điểm giữa chập xuống GND | Đo áp trên R1: nếu = Vin thì R1 hở | Cắm lại R1, tìm dây chập |
| Vout lệch >20% | Đọc nhầm mã màu (nâu/đỏ/cam dưới đèn vàng) | Đo lại từng con ở chế độ Ω (bước 2) | Đổi con đúng giá trị |
| Lệch ngoài dải *sau* bước 6 | Đọc nhầm thang, tiếp xúc breadboard có điện trở, Vin trôi giữa hai lần đo | Đo lại Vin ngay trước Vout; ấn chắc que; đo áp hai đầu một chân cắm (phải ≈0) | Đo Vin và Vout liền nhau; đổi hàng breadboard |
| Số nhảy liên tục | Que chạm chập chờn; Vin USB dao động theo tải của ESP32 (WiFi) | Đo Vin vài lần; dùng kẹp cá sấu | Ghi khoảng nhảy; đổi cổng USB/sạc |
| Cặp D: tổng ≈ Vin, không hụt | Đồng hồ của bạn có R_in lớn hơn nhiều so với 10 MΩ ở thang này, hoặc điện trở không phải 1 MΩ | Đo lại R ở chế độ Ω; tra lại manual mục DCV input impedance cho đúng thang | Ghi lại: đây là một phát hiện, không phải lỗi |
| R_in tính ra ~1 MΩ | Nhầm 1 MΩ với 100 kΩ (vòng ba vàng thay vì lục), hoặc cầm que bằng tay vào hai đầu (cơ thể là một điện trở song song) | Đo lại R; buông tay khỏi que khi đọc | Dùng kẹp cá sấu cho cặp D |

### 9. Câu hỏi ngược

**[Nếu…thì]** Nếu bạn đo Vin và Vout cùng ở thang 20 V của cùng một đồng hồ, phần "0.5% số đọc" của sai số có còn làm sai **tỉ số** Vout/Vin không?
<details><summary>Hướng nghĩ</summary>

Phần phần trăm của spec chủ yếu là sai số hệ số khuếch đại (gain) của mạch đo ở thang đó. Nếu cùng thang, cùng đồng hồ, gain sai bao nhiêu thì cả hai số đều sai bấy nhiêu — tỉ số triệt tiêu phần đó. Phần digit thì không triệt tiêu. Câu hỏi sâu hơn: spec không nói phần % là gain thuần; có điều kiện nào làm giả định này gãy (đổi thang giữa hai phép đo)? Đây là ý "sai số tương quan" trong lan truyền (→ F1.1).

</details>

**[Vì sao không]** Vì sao không mua đồng hồ có trở kháng vào 10 GΩ để hết hiệu ứng tải?
<details><summary>Hướng nghĩ</summary>

Một số đồng hồ để bàn có chế độ >10 GΩ ở thang thấp. Nghĩ xem cái giá là gì: đầu vào trở kháng rất cao nhặt nhiễu từ môi trường (que hở mạch vẫn hiện số trôi), rò bề mặt của chính breadboard và tay bạn trở thành đáng kể. Và câu hỏi thật: bạn có cần không, khi đã biết cách *tính* và *hiệu chỉnh* hiệu ứng tải?

</details>

**[Quy mô]** Robot ở K7 đọc điện áp pin 4S (lên tới ~16.8 V) bằng ADC của ESP32 (tối đa ~3.3 V) qua một divider. Divider này nối thường trực vào pin 24/7. Chọn R1, R2 ở cỡ kΩ hay MΩ? Đánh đổi là gì?
<details><summary>Hướng nghĩ</summary>

Hai lực kéo ngược nhau: R nhỏ → dòng xả pin thường trực lớn (tính bằng µA hay mA? bao nhiêu mAh mỗi tháng?); R lớn → trở kháng nguồn nhìn từ ADC lớn, và ADC lấy mẫu bằng tụ nên chính nó là một "R_in" không lý tưởng. Tìm xem người ta thêm gì ở điểm giữa (một tụ nhỏ) để có cả hai. → K7 C1.2.

</details>

**[Failure mode]** Sau một tuần, cùng mạch cặp A cho Vout lệch 3% so với tuần trước. Liệt kê ít nhất bốn nguyên nhân, xếp theo xác suất, và phép thử rẻ nhất cho mỗi cái.
<details><summary>Hướng nghĩ</summary>

Nghĩ theo tầng: nguồn (Vin khác vì cổng USB khác), dụng cụ (pin đồng hồ yếu — nhiều đồng hồ đọc sai trước khi hiện cảnh báo pin), tiếp xúc (breadboard rão, oxi hóa), linh kiện (hiếm khi điện trở đổi 3% khi không bị quá nhiệt). Phép thử rẻ nhất cho tầng dụng cụ: đo một thứ bạn biết rõ giá trị (pin AA mới vừa đo tuần trước — nhưng pin cũng đổi; tốt hơn là một điện trở "chuẩn" dành riêng, không dùng vào mạch).

</details>

**[Phản biện]** Một người nói: "Lan truyền sai số kiểu thống kê (±2u) là để tự lừa mình cho dải hẹp lại. Cứ dùng worst case cho an toàn." Bạn đồng ý tới đâu?
<details><summary>Hướng nghĩ</summary>

Worst case đúng khi bạn cần *bảo đảm* (thiết kế an toàn, một con robot không được sai). Thống kê đúng khi bạn cần *nhận định* trên nhiều mẫu (100 mạch thì mấy cái ngoài dải?). Với nhiều đầu vào, worst case trở nên quá bi quan rất nhanh. Câu hỏi thật là "dùng dải này để quyết định gì", không phải "dải nào an toàn hơn". Và cả hai đều dựa trên giả định phân bố mà nhà sản xuất không nói (dung sai có thể bị "cắt" vì con tốt đã được lọc ra bán làm ±1%).

</details>

### 10. Liên kết ra ngoài

- **Sinh học và y khoa — observer effect trong đo lường sinh lý.** Đo huyết áp bằng vòng bít làm người bệnh căng thẳng và tăng huyết áp ("white coat effect"); người ta đo lặp ở nhà để tách hiệu ứng. Giống: dụng cụ đo thay đổi đại lượng. Khác: ở mạch điện, hiệu ứng tính được từ hai con số; ở người, nó phải được ước lượng thống kê.
- **Hệ phân tán — sampling profiler vs instrumentation.** Instrumentation từng hàm (giống đồng hồ R_in thấp) cho số đủ nhưng làm chậm chương trình; sampling profiler (giống R_in cao) ít tác động nhưng thưa. Chọn công cụ theo tỉ số "chi phí của probe / thứ được đo" — đúng cấu trúc R_in / R của mạch.
- **Mạng — tap thụ động vs SPAN port.** Optical tap chia một phần ánh sáng (làm suy giảm tín hiệu chính vài dB, tính được); SPAN port sao chép gói bằng phần mềm switch (có thể drop khi tải cao, không tính trước được). Cùng câu hỏi: dụng cụ quan sát lấy bao nhiêu từ hệ thống.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| UT33D+ DCV ±(0.5% + 2 digit), 2000 count, thang 200 mV/2 V/20 V/200 V/600 V | `[spec]` | Trang sản phẩm UT33+ series của UNI-T; kiểm lại trong manual của bạn |
| UT33D+ điện trở ±(0.8% + 2 digit); danh sách thang Ω khác nhau giữa các model trong series | `[spec]` | Tra đúng model D+; có thể không có thang 2 MΩ |
| Trở kháng vào DCV ~10 MΩ | `[spec, tự đo]` | Nhiều đồng hồ cùng họ ghi ~10 MΩ; kiểm manual, và bài này tự đo ngược |
| Đồng hồ kim ghi chất lượng bằng Ω/V; VTVM có trở kháng vào ~10 MΩ | `[chuẩn]` | Kiến thức giáo khoa đo lường điện tử |
| Kaplan & Irvin 2015: ~57% → ~8% thử nghiệm báo lợi ích sau khi bắt buộc đăng ký trước | `[chuẩn]` | "Likelihood of Null Effects of Large NHLBI Clinical Trials Has Increased over Time", PLOS ONE 10(8), 2015 |
| Chân 5V của DevKit không đúng 5.00 V | `[tự đo]` | Phụ thuộc board và cổng USB |
| Dải worst case/thống kê ở phần 7 | `[ước lượng]` | Tính từ công thức phần 2; Monte Carlo phần 2 cho cùng kết quả khi đặt cặp của lab |

**Đã sửa so với bản gốc:**

1. Bản gốc đặt dải chấp nhận ±5% cho mọi cặp và gate yêu cầu "sai lệch <5% sau khi hiệu chỉnh Vin". Sai: độ nhạy của tỉ số theo dung sai là R1/(R1+R2) × (t1+t2), nên có cặp lắp đúng vẫn vượt 5%, có cặp thì 5% quá lỏng để bắt lỗi (số cụ thể trong phần 7). Sửa: dải tính riêng cho từng cặp, và thêm bước đo R để dự đoán lần hai (tiêu chí gate sửa tương ứng ở Bài 14).
2. Bản gốc nói thí nghiệm 1 MΩ cho số "thấp hơn rõ rệt". Hiệu ứng tải với đồng hồ ~10 MΩ có cùng cỡ với dải dung sai ±5% (phần 7), nên chỉ nhìn Vout thì không phân biệt được. Sửa: thêm phép thử tổng V_R1 + V_R2 so với Vin (không phụ thuộc dung sai) và phép tính ngược R_in.
3. Bản gốc đặt "Số phải ra" công khai trước phần làm. Sửa: niêm phong.
4. Thêm tra sai số dụng cụ theo thang, mẫu `prediction.md` có dải thay vì một điểm.

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** manual UNI-T UT33+ series (bảng thông số DCV, Ω, input impedance); JCGM 100:2008 (GUM), mục về đánh giá loại B và phân bố hình chữ nhật.
- **Giải thích:** SparkFun Learn, "Voltage Dividers" (có phần ứng dụng và lý do không dùng cho nguồn).
- **Đào sâu (tùy chọn):** Horowitz & Hill, *The Art of Electronics* (3rd ed.), chương 1 — divider, Thevenin, và trở kháng của dụng cụ đo. Dùng như từ điển, không đọc tuần tự.
- **Tự kiểm tra:** (1) giải thích lại cho một backend engineer khác trong 5 câu vì sao "lấy trung bình 100 lần đo" không làm hẹp được dải dung sai; (2) vẽ lại sơ đồ phần 2 có R_in từ trí nhớ; (3) hai câu dưới.

1. Divider 100 kΩ / 100 kΩ, Vin = 3.30 V, đo bằng đồng hồ R_in = 10 MΩ. Vout đọc ra bao nhiêu, lệch bao nhiêu phần trăm?
2. Cùng bộ điện trở ±1%, tỉ lệ nào cho dải Vout/Vin hẹp nhất: R1 ≪ R2, R1 = R2, hay R1 ≫ R2? Vì sao?

<details><summary>Đáp án</summary>

1. R2‖R_in = 100k·10M/(10.1M) ≈ 99.01 kΩ. Vout = 3.30 × 99.01/199.01 ≈ 1.642 V, so với 1.650 V không tải: lệch ≈ −0.5%. Nhỏ hơn sai số đồng hồ ở thang 20 V (±0.028 V) — có thật nhưng không nhìn thấy trong một lần đo.
2. R1 ≪ R2: hệ số R1/(R1+R2) gần 0, tỉ số gần 1 và gần như không nhạy với dung sai. Đổi lại, nó gần như không chia gì cả. Khi cần chia mạnh (R1 ≫ R2), dung sai bị khuếch đại gần trọn — đó là lý do mạch đo pin dùng điện trở ±1% hoặc hiệu chuẩn từng con.

</details>

---

## Bài 10 — LED và điện trở: tại sao, bằng số (5h)

> **Vị trí:** Bài 9 (divider) → **Bài 10** → Bài 11 (datasheet) · **Cần trước:** Bài 1 (hiểu nhầm 2), Bài 5 (đo dòng nối tiếp), Bài 9; F1.1 · **Sau bài này bạn quyết định được:** chọn điện trở hạn dòng cho một tải phi tuyến từ datasheet, biết dòng sẽ trôi bao nhiêu khi nguồn trôi, và nhận ra lúc nào điện trở không còn đủ (cần nguồn dòng / driver).

### 1. Câu chuyện — ai đã khổ vì chuyện này

Georg Ohm công bố năm 1827 rằng dòng qua dây dẫn tỉ lệ với điện áp. Đó là một **quy luật thực nghiệm cho vật liệu dẫn điện kiểu kim loại** ở nhiệt độ ổn định, không phải định luật của mọi linh kiện `[chuẩn]`. Hơn một thế kỷ sau, William Shockley (1949, *Bell System Technical Journal*) viết phương trình cho tiếp giáp p-n: dòng tăng theo **hàm mũ** của điện áp `[chuẩn]`. LED là một tiếp giáp p-n phát sáng. Nó không "có điện trở" theo nghĩa của Ohm.

Hệ quả thực tế ai làm đèn LED cũng từng gặp: mắc nhiều LED **song song** với một điện trở chung. Con nào có V_f thấp hơn một chút sẽ ăn nhiều dòng hơn, nóng lên; mà V_f của LED **giảm** khi nóng (cỡ −1.5 đến −2.5 mV/°C `[chuẩn, ước lượng]`), nên nó càng ăn thêm dòng. Vòng phản hồi dương này gọi là *thermal runaway* / *current hogging*. Đó là lý do dải LED 12 V thường được làm theo cụm: vài LED nối tiếp + một điện trở riêng cho mỗi cụm, và đèn công suất dùng driver dòng không đổi thay vì điện trở `[chuẩn]`.

### 2. Mô hình tư duy

```
 I (mA)
  30 ┤                         │ LED: dòng tăng theo hàm mũ khi qua "đầu gối"
     │                        ╱
  20 ┤                       ╱
     │   đường tải           │
  10 ┤ ───────────·─────────●───────────  ← giao điểm = điểm làm việc
     │  (Vs − V)/R     ·      ╲  ·
   0 ┼─────────────────╯────────────·──── V trên LED (V)
     0       1        V_f            Vs
```

1. **Điểm làm việc là giao điểm của hai đường.** Đường cong của LED (vật lý của linh kiện) và đường tải `I = (Vs − V)/R` (điện trở + nguồn). Điện trở không "chặn" dòng ở một mức; nó biến phần **điện áp dư** (Vs − V_f) thành dòng theo tỉ lệ 1/R.
2. **Đầu gối dốc nên V_f gần như cố định**, và đó là lý do mô hình "LED = một nguồn áp V_f cố định" dùng được để tính nhanh. Nhưng "gần như" có số: với hệ số lý tưởng n ≈ 2, mỗi lần dòng tăng 10× thì phần Shockley của V_f tăng n·V_T·ln10 ≈ 0.12 V `[chuẩn]`, cộng sụt áp trên điện trở nội của chip.
3. **Không có điện trở thì đường tải dựng đứng** ở V = Vs. Giao điểm nằm ở dòng mà chỉ điện trở nội của LED và của nguồn cản — hàng trăm mA với LED 5 mm, và LED chết.
4. **V_f = f(I, nhiệt độ, từng con).** Trong code, `const V_F = 2.0` là đúng. Trong mạch, V_f là một đường cong và một phân bố.

**Mô phỏng đồ chơi** — đường cong Shockley + điện trở nội, giải điểm làm việc. Tham số `n`, `Rs` là của một LED **giả định**, không phải LED của bạn.

```python
# [đã chạy] Đường cong I–V của LED (Shockley + điện trở nội) và điểm làm việc với điện trở hạn dòng
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

VT = 0.02585          # điện áp nhiệt kT/q ở ~300 K
n, Rs = 2.0, 10.0     # hệ số lý tưởng và điện trở nội: THAM SỐ ĐỒ CHƠI
# Chọn Is sao cho LED đồ chơi có V_f = 2.0 V tại 20 mA (giống cách datasheet ghi V_f tại một dòng thử)
Is = 0.020 / np.exp((2.0 - 0.020 * Rs) / (n * VT))

def v_of_i(i):
    """Điện áp trên LED khi dòng là i: nghịch đảo Shockley + sụt áp trên Rs."""
    return n * VT * np.log(i / Is + 1) + i * Rs

def operating_point(Vs, R):
    """Giải Vs = I·R + V_led(I): giao điểm đường tải và đường cong LED."""
    return brentq(lambda i: Vs - i * R - v_of_i(i), 1e-12, Vs / max(R + Rs, 1e-3))

for target in [1e-3, 5e-3, 20e-3]:
    print(f"I = {target*1e3:5.1f} mA  ->  V_LED = {v_of_i(target):.3f} V")
print(f"Mỗi lần dòng x10, phần Shockley tăng {n*VT*np.log(10)*1e3:.0f} mV")

for Vs in [4.75, 5.00, 5.25]:                     # USB được phép trôi quanh 5 V
    I = operating_point(Vs, 470)                  # 470 Ω: KHÔNG phải giá trị của lab
    print(f"Vs={Vs:.2f} V, R=470 Ω -> I={I*1e3:.2f} mA")
print(f"Không có điện trở, Vs=5 V -> I ≈ {operating_point(5.0, 0)*1e3:.0f} mA")

i = np.logspace(-6, -0.5, 400)
v = np.linspace(0, 5, 100)
plt.plot(v_of_i(i), i * 1e3, label="LED đồ chơi (Shockley + Rs)")
plt.plot(v, (5.0 - v) / 470 * 1e3, "--", label="đường tải (5 V − V)/470 Ω")
plt.xlim(0, 5); plt.ylim(0, 30); plt.grid(True); plt.legend()
plt.xlabel("V trên LED (V)"); plt.ylabel("I (mA)")
plt.show()
```

Ba thứ phải để ý khi chạy: (a) từ 1 mA lên 20 mA dòng tăng 20×, còn V_f chỉ tăng vài trăm mV; (b) khi Vs trôi ±5%, dòng trôi **nhiều hơn** ±5% (vì sao? — xem phần 3); (c) dòng khi không có điện trở.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Rate limiter / token bucket: chặn throughput ở một trần | Điện trở nối tiếp hạn dòng qua LED | Rate limiter **cắt** ở trần, dưới trần thì không ảnh hưởng. Điện trở **không có trần**: I = (Vs − V_f)/R, tuyến tính theo phần dư. Vs tăng 10% thì dòng tăng Vs/(Vs − V_f) × 10% — với 5 V và LED đỏ là ~17% | Tính R cho "dòng tối đa" rồi tin rằng dòng không thể vượt — nó vượt ngay khi nguồn cao hơn danh định |
| Đầu gối latency của hàng đợi khi utilization → 1 (→ F7.1) | Đầu gối đường cong I–V | Đầu gối hàng đợi là thống kê (do ngẫu nhiên) và hậu quả là *chậm*; đầu gối diode là vật lý tất định và hậu quả là *cháy* | Coi "qua đầu gối một chút" là chấp nhận được như chạy server ở 85% CPU |
| Retry storm: lỗi → retry → thêm tải → thêm lỗi | Thermal runaway: nóng → V_f giảm → dòng tăng → nóng hơn | Retry storm tự dừng khi client backoff/bỏ cuộc; runaway chỉ dừng khi có **phản hồi âm** (điện trở: dòng tăng → sụt áp trên R tăng → phần dư cho LED giảm) hoặc khi linh kiện chết | Thiết kế song song không có điện trở riêng, tin rằng "các LED giống nhau thì chia đều" |
| Hằng số trong config | V_f | V_f phụ thuộc dòng, nhiệt độ và từng con; datasheet ghi nó *tại một dòng thử* | Lấy V_f ở 20 mA của datasheet rồi ngạc nhiên khi đo ở 9 mA ra khác |

**Chấm mô hình:**

- *"Điện trở là rate limiter cho dòng."* (cách nói của chính Bài 1) — **ĐÚNG MỘT PHẦN.** Đúng về vai trò: không có nó thì không có gì cản. Gãy ở cơ chế: nó không đặt trần, nó đặt một quan hệ tuyến tính với phần điện áp dư. Phản ví dụ: LED đỏ, R tính cho 10 mA ở 5.0 V; cắm vào nguồn 5.5 V, dòng lên ~11.7 mA — vượt "trần" mà không có gì chặn.
- *"LED như một viên pin 2 V cắm ngược: V_f cố định."* — **ĐÚNG MỘT PHẦN.** Đây là mô hình bậc một mà kỹ sư dùng thật để chọn R, và nó cho sai số vài phần trăm trong dải dòng hẹp. Gãy khi dòng đổi nhiều (1 mA vs 20 mA lệch vài trăm mV), khi nhiệt độ đổi, và khi mắc song song (mô hình nói chia đều, thực tế không). Phản ví dụ: phần 7 của bài này.
- *"Nguồn 5 V 3 A cắm thẳng vào LED thì LED chỉ lấy dòng nó cần."* — **SAI.** "Tải quyết định dòng" (Bài 1) đúng, nhưng tải này không có điểm dừng tự nhiên: theo Shockley, ở V = 5 V nó "cần" một dòng khổng lồ, chỉ bị chặn bởi điện trở nội và giới hạn của nguồn. Phản ví dụ: mô phỏng ở phần 2, dòng không có điện trở.

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | V_f (forward voltage) | Điện áp trên LED khi nó dẫn, **ghi tại một dòng thử** trong datasheet | Hằng số của LED |
| 🟢 | Anode / cathode | Chân + (dài) / chân − (ngắn, phía vành nhựa vát phẳng) | Đảo được như điện trở |
| 🟢 | Điện trở hạn dòng | Điện trở nối tiếp đặt dòng qua phần điện áp dư: R = (Vs − V_f)/I | Thứ "chặn" dòng ở một trần |
| 🟢 | Công suất định mức điện trở | P = I²R phải dưới định mức (thường 1/4 W cho loại cắm breadboard) với biên an toàn | Chỉ cần đúng Ω |
| 🟢 | I–V curve | Đồ thị dòng theo áp của một linh kiện; đường thẳng qua gốc chỉ khi linh kiện tuân theo Ohm | Mọi linh kiện đều có "R = V/I" có nghĩa |
| 🟡 | KVL | Tổng điện áp rơi quanh một vòng kín bằng điện áp nguồn | — |
| 🟡 | Load line (đường tải) | Đường I = (Vs − V)/R; giao với đường cong linh kiện cho điểm làm việc | — |
| 🟡 | Phương trình Shockley | I = Is·(e^(V/(n·V_T)) − 1): dòng diode tăng theo hàm mũ của áp | Áp dụng cho LED công suất ở dòng lớn mà không tính điện trở nội |
| 🟡 | Burden voltage | Sụt áp trên chính đồng hồ khi đo dòng (qua điện trở shunt bên trong) | Đồng hồ đo dòng "trong suốt" với mạch |
| 🟡 | Thermal runaway / current hogging | Phản hồi dương nhiệt–dòng làm một linh kiện ăn hết dòng | Chuyện chỉ có ở mạch công suất lớn |
| 🟡 | Constant-current driver | Mạch giữ dòng cố định bất kể V_f; dùng cho LED công suất | Một loại điện trở đặc biệt |
| 🔴 | Hệ số lý tưởng n, dòng bão hòa Is, vật lý bán dẫn | Tham số của mô hình Shockley | Chỉ cần biết chúng tồn tại; fit ở phần tùy chọn |

### 5. Dự đoán

**Đề bài.** Một LED đỏ 5 mm, nguồn 5V của ESP32 (đo lại), muốn dòng ~10 mA.

1. Tính R lý tưởng, chọn giá trị chuẩn gần nhất có trong kit (dãy E12: …, 220, 270, 330, 390, 470, … Ω — chọn **lớn hơn** để an toàn, ghi lý do).
2. Với R đã chọn và V_f từ datasheet: dự đoán I, V_R, V_LED, công suất trên R.
3. Dự đoán V_f thật ở dòng của bạn **khác** V_f datasheet bao nhiêu và theo chiều nào. Dùng đồ thị "Forward current vs forward voltage" trong datasheet, hoặc quy tắc ~n·V_T·ln(I₂/I₁) ở phần 2, hoặc mô phỏng.
4. Dự đoán khi cắm đồng hồ đo dòng vào mạch, V_R thay đổi theo chiều nào.
5. Dự đoán tổng V_R + V_LED so với Vin.

**Tham số cần tra:**

- Datasheet một LED đỏ 5 mm phổ biến (LED trong kit thường không có tên hãng; lấy datasheet của một mã đỏ 5 mm của Kingbright, Everlight hoặc tương đương và **ghi rõ bạn dùng tờ nào**): V_f typ và max **tại dòng thử bao nhiêu**, I_F max liên tục, đồ thị I–V.
- Sai số DCA của UT33D+ ở thang 20 mA, và lỗ cắm que đỏ cho mA (manual). Cầu chì của lỗ mA là bao nhiêu (manual) — để biết bạn đang bảo vệ cái gì.

**Mẫu `prediction.md`:**

```markdown
# lab/02-led-current/prediction.md
Ngày: YYYY-MM-DD · Commit trước khi cắm LED.

## Nguồn tham số
- Datasheet LED: <hãng, mã, link/tên file> · V_f = ___ V (typ) / ___ V (max) tại I_F = ___ mA · I_F max = ___ mA
- Đồng hồ: thang DCA ___ · sai số ±(___ % + ___ digit) · lỗ cắm que đỏ: ___

## Tính toán
- Vs = 5.00 V (sẽ đo lại) · I mục tiêu = ___ A
- R lý tưởng = (Vs − V_f)/I = ___ Ω → chọn ___ Ω vì ___
- Với R đã chọn: I = ___ mA · V_R = ___ V · V_LED = ___ V · P_R = ___ mW (định mức ___ W)

## Dự đoán lệch
- V_f thật ở dòng của tôi so với datasheet: cao hơn / thấp hơn khoảng ___ V, vì ___
- Khi cắm ampe kế, V_R sẽ: tăng / giảm / không đổi, vì ___
- V_R + V_LED so với Vin: ___

## Điều gì sẽ làm tôi đổi ý
- Nếu V_R/R và I đo trực tiếp lệch nhau quá ___ %, tôi nghi ___
```

### 6. Làm

**Bước 1 — commit `prediction.md`.**

**Bước 2 — đo trước khi lắp.** Đo R thật (chế độ Ω, rời mạch). Kiểm chiều LED bằng chế độ diode của đồng hồ (biểu tượng ▶|): que đỏ vào chân dài, que đen chân ngắn — đồng hồ hiện một con số (đơn vị V hoặc mV tùy đồng hồ) và nhiều LED đỏ sáng mờ; đảo que thì hiện `OL`. Đây cũng là lần đầu bạn thấy V_f ở **dòng rất nhỏ** (dòng thử của chế độ diode, tra manual) — ghi lại, bạn sẽ cần nó ở câu hỏi ngược.

**Bước 3 — dựng.** 5V → điện trở → chân dài LED (anode) → chân ngắn (cathode) → GND. Nếu chân đã bị cắt bằng nhau, cathode ở phía vành nhựa vát phẳng.

**Bước 4 — đo ba điện áp liền nhau** (đồng hồ ở DCV): Vin, V_R (hai đầu điện trở), V_LED (hai chân LED). Đo liền nhau vì Vin trôi; nếu đo cách nhau vài phút, đo lại Vin.

**Bước 5 — đo dòng trực tiếp.** Rút USB. Chuyển núm sang thang 20 mA, que đỏ sang lỗ mA (theo manual; **không** dùng lỗ 10 A cho dòng mA — mất độ phân giải). Rút một đầu của điện trở khỏi hàng nối với LED, nối đồng hồ vào chỗ hở để dòng đi xuyên qua đồng hồ. Cắm USB lại, đọc.

> Sai số dụng cụ: ±(1% + 2 digit) ở thang 20 mA `[spec, kiểm manual]`; 1 digit = 0.01 mA. Khi đồng hồ đang nối tiếp, dùng đồng hồ thứ hai (nếu có) hoặc đo lại V_R sau khi tháo ampe kế để thấy burden voltage. Không có đồng hồ thứ hai: đo dòng, ghi; tháo ampe kế, đo V_R; so V_R/R với dòng.

**Bước 6 — tháo ampe kế, trả que về lỗ VΩ, núm về DCV.** Làm ngay. Để que ở lỗ mA rồi đi đo áp nguồn là cách phổ biến nhất để đứt cầu chì đồng hồ (Bài 1, hiểu nhầm 3).

**Bước 7 — kiểm chéo.** (a) V_R / R_đo so với I đo trực tiếp. (b) V_R + V_LED so với Vin (KVL). Tính sai số giới hạn của mỗi phép so từ spec đồng hồ trước khi kết luận "khớp" hay "không khớp".

**Bước 8 (tùy chọn, +1h, → F1.6) — vẽ đường cong I–V của LED của bạn.** Lặp bước 4 với 5 điện trở (2.2 kΩ, 1 kΩ, 470 Ω, 330 Ω, 220 Ω — dòng lớn nhất ~14 mA, an toàn cho LED 5 mm). Mỗi điểm: I = V_R/R_đo, V = V_LED. Fit mô hình `V = a + b·ln(I) + Rs·I` — tuyến tính theo (a, b, Rs) nên giải bằng bình phương tối thiểu:

```python
# [đã chạy] Fit mô hình LED từ vài điểm (I, V): V = a + b·ln(I) + Rs·I, tuyến tính theo a, b, Rs
import numpy as np

# Dữ liệu MẪU sinh từ mô hình đồ chơi ở phần 2 (n=2, Rs=10 Ω), làm tròn theo độ phân giải đồng hồ.
# THAY bằng số đo của bạn: dòng (A) và V_LED (V)
I = np.array([1.51e-3, 3.26e-3, 6.78e-3, 9.52e-3, 13.99e-3])
V = np.array([1.681, 1.739, 1.812, 1.857, 1.921])

A = np.column_stack([np.ones_like(I), np.log(I), I])   # ma trận thiết kế
(a, b, Rs), *_ = np.linalg.lstsq(A, V, rcond=None)
VT = 0.02585
print(f"n·VT = {b*1e3:.1f} mV  ->  n ≈ {b/VT:.2f}")
print(f"Rs ≈ {Rs:.1f} Ω")
print(f"Is ≈ {np.exp(-a/b):.2e} A")
print("residual (mV):", np.round((V - A @ np.array([a, b, Rs])) * 1e3, 2))
# 5 điểm, 3 tham số: chỉ 2 bậc tự do. Residual nhỏ KHÔNG chứng minh mô hình đúng (→ F1.6)
```

Với dữ liệu mẫu, fit trả lại n ≈ 2.05 và Rs ≈ 9.8 Ω — gần tham số đã sinh ra nó. Với LED thật, n thường ra lớn hơn 2 `[ước lượng]`, và n với Rs "đánh đổi" nhau khi dữ liệu nhiễu: thử bỏ một điểm rồi fit lại để thấy tham số nhảy bao nhiêu.

**Bước 9 — `analysis.md`.** Bảng dự đoán / đo / chênh lệch cho I, V_R, V_LED; hai phép kiểm chéo kèm sai số giới hạn; và **một đoạn văn bằng lời của bạn giải thích vì sao V_f đo được khác V_f datasheet**. Đoạn này là tiêu chí PASS số 4 của gate (Bài 14). Viết như giải thích cho đồng nghiệp backend, không chép câu của bài.

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

**Tính toán mẫu** (V_f datasheet 2.0 V tại 20 mA, Vs = 5.00 V, mục tiêu 10 mA):

- R lý tưởng = 3.00 V / 0.010 A = 300 Ω → E12 không có 300 Ω (đó là E24); chọn 330 Ω.
- I = 3.00/330 = 9.09 mA · V_R = 3.00 V · V_LED = 2.00 V · P_R = 3.00 × 0.00909 ≈ 27 mW (điện trở 1/4 W: biên an toàn ~9×).

**Đo thật:**

| Đại lượng | Dự đoán (mô hình V_f cố định) | Thường đo được | Ghi chú |
|---|---|---|---|
| V_LED (V_f thật) | 2.00 V | **1.75 – 2.00 V** với LED đỏ thông dụng `[ước lượng]` | Thấp hơn datasheet vì dòng thấp hơn dòng thử. LED đỏ công nghệ cũ có thể còn thấp hơn; LED "đỏ siêu sáng" có thể ~2.0 V |
| V_R | 3.00 V | 3.00 – 3.25 V | = Vin − V_LED |
| I | 9.09 mA | **9.1 – 9.9 mA** với Vin = 5.00 V, R = 330 Ω đúng | Nhân theo Vin và R đo thật của bạn |
| V_R/R_đo vs I trực tiếp | khớp | lệch ≲ 3–4% | Gồm sai số đồng hồ (~1–2% mỗi phép) và burden |
| V_R + V_LED vs Vin | bằng | lệch ≲ 2% | Mỗi số đọc có ±(0.5% + 2 digit); ba số đọc |
| Gate: dòng tính (dự đoán) vs đo | — | lệch < 10% | Lệch chủ yếu đến từ V_f giả định |

**Vì sao V_f thấp hơn datasheet:** datasheet ghi V_f tại 20 mA; bạn chạy ~9–10 mA. Theo Shockley, giảm dòng ~2× làm phần tiếp giáp giảm n·V_T·ln2 ≈ 35 mV (n = 2); cộng phần điện trở nội giảm Rs·ΔI (vài chục mV đến ~0.1 V tùy LED). Thêm: V_f datasheet là *typical* — con của bạn là một mẫu trong phân bố (→ Bài 11).

**Burden voltage:** khi ampe kế ở trong mạch, V_R **giảm** một chút: shunt của đồng hồ cộng thêm vào R. Nếu dòng giảm Δ%, shunt ≈ Δ% × (R + điện trở động của LED). Thang 20 mA của đồng hồ cầm tay thường có shunt cỡ vài Ω đến ~10 Ω `[ước lượng]` → dòng giảm ≲3%. Tự tính shunt của đồng hồ bạn từ ΔV_R và ghi lại.

**Độ nhạy theo nguồn:** Vin trôi ±5% (4.75–5.25 V) thì dòng trôi khoảng ±8% với LED đỏ (hệ số Vs/(Vs − V_f) ≈ 1.6), không phải ±5%.

**Chế độ diode của đồng hồ (bước 2):** V_f đọc ra thấp hơn rõ rệt so với trong mạch, vì dòng thử của chế độ diode cỡ vài trăm µA đến ~1 mA `[ước lượng — tra manual]`. Đây là một điểm thứ ba trên đường cong I–V của bạn, miễn phí.

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| LED không sáng, không nóng, V_LED ≈ Vin | Cắm ngược chiều (LED chặn, toàn bộ áp nằm trên nó) | Chế độ diode của đồng hồ | Đảo LED |
| LED sáng rất mờ, I ≪ 9 mA | Điện trở quá lớn (33 kΩ thay vì 330 Ω — vòng ba cam thay vì nâu) | Đo R rời mạch | Đổi đúng điện trở |
| LED sáng chói rồi tắt hẳn, có mùi | Quên điện trở hoặc điện trở bị chập qua hàng breadboard | Đo R giữa hai hàng (tắt nguồn) | LED đã chết; thay LED, sửa mạch. Đây là lý do mua nhiều LED |
| V_LED ≈ 2.8–3.3 V | Không phải LED đỏ (LED trắng/xanh dương, hoặc LED có vỏ đỏ nhưng chip khác) | So màu ánh sáng; tra lại | Dùng V_f đúng loại, tính lại |
| Dòng đọc ra 0 (đồng hồ ở thang mA) | Cầu chì lỗ mA đã đứt từ lần trước, hoặc que đỏ ở sai lỗ (10 A với thang mA, hoặc VΩ) | Đo thông mạch giữa lỗ mA và COM qua một điện trở biết trước (tắt nguồn mạch) — xem manual cách kiểm cầu chì | Thay cầu chì đúng loại theo manual |
| Đồng hồ hiện `OL`/`1` ở thang mA | Vượt thang (dòng > 20 mA) — không phải 0 | Chuyển thang 200 mA | Kiểm lại vì sao dòng lớn thế: thiếu điện trở? |
| Mạch tắt khi cắm ampe kế | Mạch vẫn hở: ampe kế nối sai chỗ, hoặc cầu chì đứt | Thông mạch qua ampe kế | Nối lại nối tiếp đúng chỗ hở |
| V_R/R lệch I trực tiếp >5% | Dùng R danh định thay vì R đo; burden lớn; đo ở hai thời điểm Vin khác nhau | Dùng R đo; đo V_R ngay khi ampe kế đang trong mạch (đồng hồ thứ hai) | Ghi đúng điều kiện từng phép đo |
| V_R + V_LED lệch Vin >2% | Que đo không chạm đúng điểm (đo qua một chân breadboard có điện trở tiếp xúc); đổi thang giữa các phép đo | Đo áp rơi trên chính tiếp xúc breadboard (phải ≈0) | Cắm lại; đo cả ba ở cùng thang |

### 9. Câu hỏi ngược

**[Nếu…thì]** Nếu thay LED đỏ bằng LED trắng (V_f ~3 V) với nguồn 5 V, rồi với nguồn 3.3 V, độ nhạy của dòng theo nguồn thay đổi thế nào? Ở 3.3 V, chọn R bao nhiêu và có nên không?
<details><summary>Hướng nghĩ</summary>

Hệ số khuếch đại là Vs/(Vs − V_f). Khi phần dư Vs − V_f nhỏ, một chút trôi của nguồn hoặc của V_f (theo nhiệt, theo con) thành phần trăm lớn của dòng. Ở 3.3 V với LED trắng, phần dư cỡ vài trăm mV: R nhỏ, dòng phụ thuộc gần hết vào V_f của từng con. Đây là lúc điện trở không còn là lựa chọn tốt.

</details>

**[Vì sao không]** Vì sao không nối LED thẳng vào chân GPIO 3.3 V của ESP32 không điện trở, với lý do "GPIO có giới hạn dòng sẵn"?
<details><summary>Hướng nghĩ</summary>

Tìm trong datasheet ESP32-S3 xem "drive strength" được mô tả là gì: là khả năng lái ở một mức áp đầu ra nào đó, hay một giới hạn dòng được bảo đảm? Nếu không có chữ "current limit" kèm số max được bảo đảm, thì thứ cản dòng là điện trở của transistor đầu ra — một thứ không được thiết kế để làm điện trở hạn dòng, và nóng lên bên trong chip. Bài 11 sẽ cho bạn từ vựng để đọc câu này.

</details>

**[Quy mô]** 60 LED đỏ trên một tấm hiển thị, cấp từ 12 V. Bạn mắc thế nào: 60 song song với một điện trở chung, 60 song song mỗi con một điện trở, hay cụm nối tiếp? Tính công suất tổn hao trên điện trở cho mỗi phương án.
<details><summary>Hướng nghĩ</summary>

Song song chung một điện trở: current hogging (phần 1). Mỗi con một điện trở 12 V: phần dư ~10 V nằm trên điện trở — tính P = I·(Vs − V_f) × 60 so với công suất LED. Cụm nối tiếp: phần dư nhỏ hơn nhiều, ít điện trở hơn, nhưng một LED hở là cả cụm tắt (failure mode cụm). Đây là bài toán thiết kế dải LED thật.

</details>

**[Failure mode]** LED chạy liên tục 2 giờ trong hộp kín. Dòng đo được tăng dần, giảm dần, hay đứng yên? Thiết kế một phép đo để biết, với dụng cụ bạn đang có.
<details><summary>Hướng nghĩ</summary>

LED nóng lên → V_f giảm → với điện trở, dòng tăng nhẹ (phản hồi dương nhưng bị R hãm). Điện trở cũng nóng nhưng 27 mW là nhỏ. Đo: ghi V_R mỗi 10 phút (không cần ampe kế), tính I. Câu hỏi khó hơn: thay đổi bạn thấy có lớn hơn sai số đồng hồ và trôi của Vin không? Nếu không, kết luận là "không phát hiện được", không phải "không đổi".

</details>

**[Liên ngành]** Motor DC khi bị giữ chặt (stall) kéo dòng rất lớn; khi quay tự do kéo dòng nhỏ. Cấu trúc này giống và khác LED không điện trở ở đâu?
<details><summary>Hướng nghĩ</summary>

Motor đứng yên: chỉ còn điện trở cuộn dây (nhỏ) cản dòng, giống LED không điện trở. Khi quay, motor sinh back-EMF chống lại nguồn — một "V_f" tăng theo tốc độ. Khác: back-EMF tuyến tính theo tốc độ, không phải hàm mũ theo dòng. Hệ quả cho robot: dòng hãm (stall) là con số phải chọn driver và cầu chì theo, → K7 C3.2.

</details>

**[Phản biện]** "Đo dòng bằng V_R/R luôn tốt hơn đo trực tiếp bằng ampe kế." Đúng tới đâu?
<details><summary>Hướng nghĩ</summary>

Ưu: không phải cắt mạch, không burden, không rủi ro đứt cầu chì — đây là nguyên lý của điện trở shunt và các chip như INA226 (→ K7 C1.5). Nhược: sai số của R (phải đo hoặc dùng R ±1%) cộng sai số của phép đo áp nhỏ; với dòng rất nhỏ, V_R nhỏ tới mức phần digit chiếm ưu thế. "Tốt hơn" phụ thuộc vào dòng, R và dụng cụ — tính cả hai sai số rồi mới chọn.

</details>

### 10. Liên kết ra ngoài

- **Đèn phóng điện (huỳnh quang, đèn hồ quang) — ballast.** Plasma trong đèn có điện trở *âm*: dòng càng lớn, áp càng giảm. Không có ballast (cuộn cảm hoặc điện trở nối tiếp), dòng tăng tới khi đèn hoặc nguồn hỏng. Giống: một linh kiện không tự giới hạn cần phần tử nối tiếp tạo phản hồi âm. Khác: đèn chạy AC, ballast là cuộn cảm để không tốn công suất như điện trở.
- **Mạng — điều khiển tắc nghẽn TCP.** AIMD là phản hồi âm: mất gói → giảm cửa sổ. Thiếu nó (như một số luồng UDP không kiểm soát) thì mạng có thể rơi vào congestion collapse — vòng phản hồi dương giữa retransmit và nghẽn, như thermal runaway. Khác: TCP có thể "phục hồi" khi tải giảm; LED đã cháy thì không.
- **Tài chính — đòn bẩy và margin call.** Giá giảm → bị gọi ký quỹ → bán tháo → giá giảm thêm. Cùng cấu trúc phản hồi dương; "điện trở" ở đây là hạn mức đòn bẩy và circuit breaker của sàn — và cái tên "circuit breaker" không phải ngẫu nhiên.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| Dòng diode tăng theo hàm mũ của áp (Shockley 1949) | `[chuẩn]` | Bất kỳ giáo trình điện tử bán dẫn |
| Mỗi 10× dòng, phần tiếp giáp tăng n·V_T·ln10 ≈ 0.12 V với n = 2 | `[chuẩn]` | Tính từ phương trình; LED thật có thêm điện trở nội |
| V_f LED giảm ~1.5–2.5 mV/°C | `[chuẩn, ước lượng]` | Tùy công nghệ; kiểm đồ thị "V_f vs temperature" trong datasheet LED |
| Dải V_f thường gặp của LED đỏ ở ~10 mA (phần 7) | `[ước lượng]` | Phụ thuộc công nghệ chip (GaAsP vs AlGaInP); tự đo |
| UT33D+ DCA thang 2000 µA/20 mA/200 mA/10 A, ±(1% + 2 digit) | `[spec]` | Trang UT33+ series; kiểm manual |
| Shunt thang 20 mA vài Ω đến ~10 Ω | `[ước lượng]` | Tự tính từ ΔV_R ở bước 5; manual có thể ghi burden voltage |
| Tham số n = 2, Rs = 10 Ω trong mô phỏng | `[ước lượng]` | Tham số đồ chơi để thấy hình dạng, không phải của LED nào |

**Đã sửa so với bản gốc:**

1. Mẫu `prediction.md` của bản gốc điền sẵn mọi con số (300 Ω, 9.09 mA…). Sửa: mẫu để trống, số tính sẵn chuyển vào khối 🔒.
2. Bản gốc ghi "Dòng đo ra 0 khi chuyển sang mA — … dòng vượt thang". Vượt thang hiện `OL`/`1`, không hiện 0. Đọc 0 gần như luôn là cầu chì đứt hoặc sai lỗ cắm. Tách thành hai dòng.
3. Bản gốc giải thích V_f thấp hơn chỉ bằng "phụ thuộc dòng". Bổ sung: phần tiếp giáp (hàm mũ) và điện trở nội, cộng phân bố giữa các con (typical không phải giá trị của con bạn) và nhiệt độ.
4. Dải chấp nhận V_LED của bản gốc mở rộng về phía thấp và gắn nhãn `[ước lượng]`, vì phụ thuộc công nghệ chip.
5. Thêm đo burden voltage, kiểm chéo có sai số giới hạn, mô phỏng Shockley + đường tải, và phần fit tùy chọn.

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** datasheet LED bạn chọn (mục Electro-Optical Characteristics và đồ thị I_F–V_F); W. Shockley, "The Theory of p-n Junctions in Semiconductors and p-n Junction Transistors", *Bell System Technical Journal*, 1949.
- **Giải thích:** SparkFun Learn, "Light-Emitting Diodes (LEDs)" — phần chọn điện trở và đọc V_f.
- **Đào sâu (tùy chọn):** Horowitz & Hill, *The Art of Electronics* (3rd ed.), chương 1 phần diode và chương 12 phần LED driver.
- **Tự kiểm tra:** (1) giải thích lại cho một backend engineer khác trong 5 câu vì sao điện trở không phải rate limiter; (2) vẽ lại đồ thị đường cong + đường tải từ trí nhớ, đánh dấu chuyện gì xảy ra với giao điểm khi R giảm và khi Vs tăng; (3) hai câu dưới.

1. LED xanh dương V_f = 3.1 V tại 10 mA, nguồn 5.0 V, muốn ≤10 mA. Chọn điện trở E12 nào, dòng thực tế bao nhiêu?
2. Với LED đỏ và R = 330 Ω, vì sao dòng chỉ đổi ~0.3 mA khi Vs đổi 0.1 V, dù đường cong LED dốc theo hàm mũ?

<details><summary>Đáp án</summary>

1. R = (5.0 − 3.1)/0.010 = 190 Ω → E12 gần nhất phía trên là 220 Ω. I ≈ (5.0 − 3.1)/220 ≈ 8.6 mA (V_f thật sẽ thấp hơn một chút ở dòng này, nên dòng nhỉnh hơn một chút).
2. Độ dốc của điểm làm việc theo Vs là 1/(R + r_d), với r_d = điện trở động của LED tại điểm đó ≈ n·V_T/I + Rs ≈ 0.052/0.0095 + 10 ≈ 15 Ω (mô hình đồ chơi). R = 330 Ω chiếm ưu thế, nên ΔI ≈ 0.1/345 ≈ 0.29 mA. Chính sự dốc của LED làm V_f gần như cố định, và điện trở quyết định dòng.

</details>

---

## Bài 11 — Đọc trọn một datasheet (4h)

> **Vị trí:** Bài 10 (LED) → **Bài 11** → Bài 12 (I2C) · **Cần trước:** Bài 3 (bus), Bài 10 (V_f "tại dòng thử" — ý niệm *điều kiện đo*); F1.2 · **Sau bài này bạn quyết định được:** một linh kiện có dùng được trong điều kiện của bạn không (áp, nhiệt, timing), và firmware phải dựa vào con số nào — typical hay max — cho từng quyết định.

### 1. Câu chuyện — ai đã khổ vì chuyện này

Tàu con thoi Challenger (28/1/1986) phóng trong buổi sáng lạnh hơn rõ rệt mọi lần phóng trước. Ủy ban Rogers kết luận vòng đệm O-ring ở mối nối tên lửa đẩy mất khả năng bịt kín, và các kỹ sư nhà thầu đã cảnh báo trước về hành vi của O-ring ở nhiệt độ thấp — vùng mà dữ liệu và kinh nghiệm bay không bao phủ `[chuẩn — Rogers Commission Report, 1986]`. Mười năm sau, Ariane 5 chuyến 501 (4/6/1996) tự hủy ~40 giây sau khi cất cánh: phần mềm định vị quán tính dùng lại từ Ariane 4, một phép chuyển số thực 64-bit sang số nguyên 16-bit bị tràn vì Ariane 5 có vận tốc ngang lớn hơn những gì Ariane 4 từng đạt `[chuẩn — báo cáo Inquiry Board, J.-L. Lions, 1996]`.

Hai sự cố khác nhau, một cấu trúc: **một thành phần được dùng ngoài vùng điều kiện mà nó được đặc tả và kiểm chứng**. Datasheet là tài liệu ghi chính xác vùng đó cho một con chip. Nó không chỉ nói chip làm gì — nó nói chip làm gì **trong điều kiện nào**, và con số nào được bảo đảm, con số nào chỉ là "thường thấy".

### 2. Mô hình tư duy

**Bốn vùng điện áp** của mọi IC (số cụ thể của BME280 bạn tự tra ở phần 5):

```
 V_supply ─┼────────────┼──────────────────┼────────────┼──────────────▶
           0       V_op,min           V_op,max     V_abs,max
  ┌────────┬────────────┬──────────────────┬────────────┬──────────────┐
  │ âm quá │ chip có thể│ RECOMMENDED      │ không hỏng │ ABSOLUTE MAX │
  │ abs min│ chạy, KHÔNG│ OPERATING:       │ ngay, nhưng│ vượt = có thể│
  │ = hỏng │ bảo đảm    │ mọi số trong     │ KHÔNG bảo  │ hỏng vĩnh    │
  │        │            │ Electrical Char. │ đảm hoạt   │ viễn, kể cả  │
  │        │            │ chỉ đúng ở đây   │ động/tuổi  │ hỏng ngầm    │
  └────────┴────────────┴──────────────────┴────────────┴──────────────┘
```

**Ba cột của một bảng thông số:**

```
 số con chip
   │            ▁▃▆█▆▃▁                 typ  = giá trị "thường thấy", thường ở 25 °C,
   │          ▁▃███████▃▁                      KHÔNG kèm n, σ, hay cam kết nào
   │        ▁▅███████████▅▁
   │   ···▁▃███████████████▃▁···        min / max = biên được BẢO ĐẢM trong điều kiện ghi
   └───┼──────────┼──────────┼───▶             (hoặc test 100% khi xuất xưởng, hoặc
      min        typ        max                  "guaranteed by design/characterization")
```

Bốn câu về bản chất:

1. **Datasheet là một hợp đồng có điều kiện.** Mọi con số trong *Electrical Characteristics* đi kèm một cột *Conditions* (nhiệt độ, áp, dòng, chế độ). Ngoài điều kiện đó, con số không còn hiệu lực — giống V_f "tại 20 mA" ở Bài 10.
2. **Typical không phải bảo đảm.** Nó là mô tả, không phải cam kết. Quyết định an toàn (chờ bao lâu, cấp bao nhiêu dòng, sai số tối đa) dựa vào min/max. Typical dùng để ước lượng trung bình của nhiều con.
3. **Register map là API, có quy tắc gọi.** Địa chỉ, quyền đọc/ghi, giá trị sau reset, và — thứ hay bị bỏ qua — *thứ tự ghi* và *tác dụng phụ*. Ví dụ BME280: thay đổi trong thanh ghi điều khiển độ ẩm chỉ có hiệu lực sau khi ghi thanh ghi đo chính `[spec, kiểm mục mô tả ctrl_hum]`.
4. **Timing diagram là sequence diagram có đơn vị nanô giây.** Mỗi mũi tên giữa hai cạnh tín hiệu có một tên (t_SU, t_HD, t_LOW…) và một dòng trong bảng timing với min/max. Vi phạm không sinh lỗi; nó sinh **bit sai**.

**Thứ tự đọc** (không đọc tuần tự từ trang 1 ở lượt đầu):

| Mục | Tìm gì | Vì sao |
|---|---|---|
| Absolute Maximum Ratings | Áp tối đa mọi chân, nhiệt độ, ESD | Vượt là hỏng. Đọc đầu tiên, luôn luôn |
| Recommended Operating / Electrical Characteristics | Dải VDD, dòng tiêu thụ, độ chính xác — kèm điều kiện | Mọi số "đúng" chỉ đúng ở đây |
| Pin description | Từng chân làm gì, chân nào không được để hở | Biết nối vào đâu; chân để hở = trạng thái không xác định |
| Memory map / Register map | Địa chỉ, tên, R/W, reset value, bit field | Đây là API |
| Interface & timing | Chế độ I2C/SPI hỗ trợ, bảng timing, địa chỉ I2C | Cần ở Bài 12, K3, K5 |
| Measurement time / modes | Chờ bao lâu sau khi ra lệnh đo | Quyết định của firmware |
| Package / soldering | Kích thước, reflow | Bỏ qua: bạn dùng module |

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| OpenAPI spec | Datasheet | Không có schema máy đọc được, không có validator, không có contract test tự động. **Bạn** là validator | Tin rằng "code chạy được trên bàn" = "đúng spec" |
| `GET /version`, `GET /health` | Thanh ghi chip ID | Chip ID chứng minh *giao tiếp bus* sống và đúng loại chip, không chứng minh *phép đo* đúng | Dùng chip ID làm health check duy nhất cho cảm biến (→ F2.1: một oracle yếu) |
| SLA: p99 < 200 ms, vi phạm thì bồi hoàn | min/max trong Electrical Characteristics | SLA có điều khoản loại trừ, datasheet cũng vậy (*Conditions*). Nhưng vượt **absolute max** không có bồi hoàn, không có 4xx, không có retry: chip hỏng vĩnh viễn hoặc hỏng ngầm, có thể vẫn trả lời bình thường | Thử "cho biết giới hạn" bằng cách vượt nó, như load test tới khi 503 |
| Benchmark p50 trong blog của vendor | typical | Typical thường không kèm cỡ mẫu, phân bố, nhiệt độ; nhiều dòng ghi "not tested in production" | Tính timeout/budget theo typical rồi gặp lỗi hiếm trên một số con, ở một số nhiệt độ |
| Endpoint có side effect, thứ tự gọi bắt buộc (phải `POST /session` trước `PUT /config`) | Ghi thanh ghi theo thứ tự quy định; bit reserved phải giữ nguyên (read-modify-write) | Không có lỗi trả về khi gọi sai thứ tự: thanh ghi nhận giá trị nhưng không có hiệu lực | Cấu hình "đã ghi" nhưng chip chạy cấu hình cũ, không có log nào |
| Sequence diagram + timeout | Timing diagram (t_SU, t_HD, t_LOW…) | Thời gian do vật lý áp đặt ở thang ns; vi phạm cho dữ liệu sai **im lặng**, không phải timeout | Cho rằng "chậm hơn thì an toàn hơn" — có những thông số có cả min và max |
| Changelog, API version, "beta" | Revision history, "Preliminary/Advance information", errata | Errata của chip không vá được bằng deploy: chip đã hàn lên board là phiên bản đó mãi mãi | Đọc datasheet bản cũ trên một trang mirror, bỏ lỡ sửa đổi |

**Chấm mô hình:**

- *"Datasheet giống OpenAPI spec + SLA."* — **ĐÚNG MỘT PHẦN.** Đúng ở cấu trúc: endpoint (register), schema (bit field), bảo đảm có điều kiện (min/max). Gãy ở hậu quả của vi phạm: API có lỗi trả về và retry; chip vượt absolute max thì không có gì để retry. Gãy ở kiểm chứng: không có validator. Phản ví dụ: cấp 5 V vào chân VDD của một chip 3.3 V trong vài giây; nó có thể vẫn trả chip ID đúng, nhưng thông số đo không còn được bảo đảm — không có cách nào biết từ phía phần mềm.
- *"Typical là giá trị trung bình được bảo đảm."* — **SAI.** Typical không được bảo đảm, và thường cũng không được định nghĩa thống kê (không nói là mean hay median, của bao nhiêu con, ở nhiệt độ nào). Phản ví dụ: thời gian đo của BME280 có cả typ và max (phần 5); firmware chờ đúng typ rồi đọc sẽ đôi khi đọc dữ liệu của lần đo trước.
- *"Không vượt absolute max là an toàn."* — **ĐÚNG MỘT PHẦN.** Không hỏng *ngay* là đúng. Nhưng vùng giữa recommended max và absolute max không bảo đảm chip hoạt động đúng, và hầu hết datasheet ghi rằng ở lâu gần absolute max có thể ảnh hưởng độ tin cậy. Phản ví dụ: chạy VDD hơi trên recommended max, trên bàn ở 25 °C đọc đúng; trong hộp robot nóng thì không có gì bảo đảm.
- *"Datasheet của chip mô tả module tôi mua."* — **SAI.** Module thêm LDO (hoặc không), điện trở pull-up, mạch chuyển mức, jumper chọn địa chỉ. Phản ví dụ: hai module BME280 trông giống nhau, một có LDO cấp được 5 V vào chân VIN, một không có LDO và chết với 5 V.

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | Absolute Maximum Ratings | Giới hạn mà vượt qua có thể hỏng vĩnh viễn; **không** phải điều kiện hoạt động | Dải hoạt động bình thường |
| 🟢 | Recommended Operating Conditions | Dải mà mọi thông số trong bảng điện được bảo đảm | Chỉ là "khuyến nghị", vượt chút không sao |
| 🟢 | Electrical Characteristics + Conditions | Bảng thông số, mỗi dòng đúng trong một điều kiện cụ thể | Thông số tuyệt đối |
| 🟢 | min / typ / max | Biên bảo đảm / giá trị thường thấy / biên bảo đảm | typ = trung bình bảo đảm |
| 🟢 | Register map / memory map | Bảng địa chỉ thanh ghi, R/W, reset value, bit field | Chỉ là danh sách địa chỉ |
| 🟢 | Chip ID | Thanh ghi chỉ đọc chứa mã loại chip | Health check đầy đủ |
| 🟢 | Timing diagram | Hình thứ tự cạnh tín hiệu theo thời gian, mỗi khoảng có tên và min/max | Hình minh họa |
| 🟡 | Setup / hold time | Dữ liệu phải ổn định bao lâu trước / sau cạnh clock | — |
| 🟡 | Reserved bits, read-modify-write | Bit không được đổi; muốn đổi một field phải đọc, sửa, ghi lại | Ghi 0 vào reserved cũng được |
| 🟡 | Errata | Danh sách lỗi đã biết của một revision chip | — |
| 🟡 | Guaranteed by design / characterization | Không test từng con, bảo đảm bằng thiết kế hoặc đo mẫu | Đã test 100% |
| 🟡 | Compensation / trimming coefficients | Hệ số hiệu chuẩn riêng từng con, đọc từ chip để đổi raw → đơn vị vật lý | Hằng số chung (→ K5 Bài 4) |
| 🔴 | Reflow profile, MSL, package drawing | Hàn SMD công nghiệp | Bạn dùng module |

### 5. Dự đoán

**Đề bài.** Trước khi đọc kỹ datasheet BME280, viết dự đoán cho các câu sau. Câu 1–3 là **hiệu chuẩn trực giác**: đoán trước, đọc sau, chấm mình đoán lệch bao nhiêu. Câu 4 là **tính toán** sau khi tìm được công thức trong datasheet — viết kết quả vào `prediction.md` trước khi đo nó ở bước 8 (sau Bài 12).

1. Dải VDD hoạt động và absolute max của chip BME280. Cấp 5 V thẳng vào chip có sao không? Vào chân VIN của **module bạn có** thì sao?
2. Địa chỉ I2C của chip, chân nào chọn địa chỉ, module của bạn đang đặt chân đó thế nào.
3. Giá trị chip ID. Nếu đọc ra giá trị khác thì có thể là chip gì?
4. Thời gian đo ở **forced mode**, oversampling ×1 cho cả nhiệt độ, áp suất, độ ẩm: **typical và maximum**. Tìm công thức ở mục/phụ lục về "measurement time" của datasheet. Tính thêm cho oversampling ×16 cả ba. Max lớn hơn typ bao nhiêu phần trăm?
5. Dự đoán điện trở pull-up có sẵn trên module (đo ở bước 6).

**Tham số cần tra, tra ở đâu:** datasheet BME280 chính hãng của Bosch Sensortec (mã tài liệu BST-BME280-DS002, lấy revision mới nhất từ trang Bosch Sensortec; ghi revision và ngày). Trang bán hàng của module **không phải** datasheet.

**Mẫu `prediction.md`:**

```markdown
# lab/03-datasheet/prediction.md
Ngày: YYYY-MM-DD · Câu 1–3, 5 viết TRƯỚC khi mở datasheet. Câu 4 viết sau khi tìm công thức, TRƯỚC khi đo.

## Hiệu chuẩn trực giác (đoán)
1. VDD hoạt động: ___ … ___ V · absolute max: ___ V · 5 V thẳng vào chip: ___ · vào VIN module của tôi: ___
2. Địa chỉ I2C: ___ / ___ · chọn bằng chân ___ · module của tôi: ___
3. Chip ID = ___ · nếu khác, có thể là ___
5. Pull-up trên module: ___ kΩ (đoán)
Độ tự tin của tôi cho từng câu (0–100%): 1: __ · 2: __ · 3: __ · 5: __

## Tính toán (sau khi tìm công thức — ghi trang/mục)
4. Forced mode, osrs ×1/×1/×1: t_typ = ___ ms · t_max = ___ ms · (max − typ)/typ = ___ %
   osrs ×16/×16/×16: t_typ = ___ ms · t_max = ___ ms
   Firmware của tôi sẽ chờ: ___ ms hoặc poll bit ___ của thanh ghi ___, vì ___
```

### 6. Làm

**Bước 1 — commit câu 1–3, 5 của `prediction.md`** trước khi mở datasheet.

**Bước 2 — tải datasheet.** Ghi revision, ngày, số trang vào `analysis.md`. Nếu bạn tải từ trang mirror, đối chiếu revision với trang Bosch.

**Bước 3 — lượt một (~30 phút): đọc theo bảng thứ tự ở phần 2.** Chỉ các mục đó. Tìm công thức measurement time, điền câu 4 của `prediction.md`, **commit**.

**Bước 4 — lượt hai: đọc trọn, không skim.** Chỗ nào không hiểu thì ghi lại nguyên văn câu đó và số trang vào `analysis.md` mục "chưa hiểu", đừng bỏ qua. Phần compensation formula được phép đọc lướt — bạn sẽ tự cài nó ở K5 Bài 4.

**Bước 5 — viết tay register map** ra giấy, ít nhất 8 thanh ghi: địa chỉ, tên, R/W, giá trị sau reset (nếu có), bit field chính. Bắt buộc có: chip ID, reset, các thanh ghi điều khiển (độ ẩm, đo, cấu hình), status, và ít nhất một thanh ghi dữ liệu. Ghi cạnh thanh ghi điều khiển độ ẩm **quy tắc thứ tự ghi** nếu bạn tìm thấy. Chụp ảnh, commit vào `lab/03-datasheet/photos/`.

Viết tay, không copy-paste: chép tay ép mắt đi qua từng dòng, và bạn sẽ thấy những chữ nhỏ như "reserved" và "only becomes effective after".

**Bước 6 — module ≠ chip.** Rút module khỏi mọi nguồn. Chụp ảnh hai mặt module. Tìm:
- Có IC ổn áp (LDO, thường là IC 3 chân gần chân VIN) không? Tra mã khắc trên IC nếu đọc được.
- Đo điện trở giữa SDA và VCC, giữa SCL và VCC (chế độ Ω, module không cấp điện) → giá trị pull-up thật trên module. Bài 12 cần con số này.
- Chân SDO/ADDR nối đi đâu (đo thông mạch tới GND hoặc VCC) → địa chỉ I2C dự kiến.

> Sai số dụng cụ: đo pull-up ở thang 20 kΩ, ±(0.8% + 2 digit) `[spec]`. Nếu module có cả mạch chuyển mức, số đo có thể là nhiều điện trở song song — ghi lại số đọc, đừng ép nó thành 4.7 kΩ hay 10 kΩ.

**Bước 7 — "bảng hợp đồng" trong `analysis.md`.** 6–8 dòng, mỗi dòng một thông số bạn sẽ dựa vào trong khóa này:

| Thông số | min | typ | max | Đơn vị | Điều kiện | Trang | Tôi dựa vào cột nào, cho quyết định gì |
|---|---|---|---|---|---|---|---|

Gợi ý dòng: VDD, VDDIO, dòng ở sleep, dòng trung bình ở 1 Hz, sai số tuyệt đối nhiệt độ, sai số tuyệt đối áp suất, thời gian đo, tần số I2C tối đa.

**Bước 8 — (làm sau Bài 12, bước capture) đo thời gian đo thật.** Khi đã đọc được chip ID trên PulseView, viết một sketch nhỏ: ghi thanh ghi đo chính ở forced mode, rồi đọc status liên tục cho tới khi bit "measuring" về 0. Trên PulseView, đo từ cạnh STOP của lệnh ghi tới lần đọc đầu tiên thấy bit đó = 0. Lặp ≥20 lần, ghi phân bố (min, median, max) — không ghi một số.

> Sai số dụng cụ: độ phân giải thời gian bằng khoảng cách giữa hai lần poll (mỗi lần đọc status mất vài trăm µs ở 100 kHz — Bài 12 sẽ cho bạn số này), lớn hơn nhiều so với độ phân giải của logic analyzer. Ghi rõ đó là giới hạn của phương pháp.

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

**Đối chiếu register map:** ≥90% số dòng bạn viết đúng với datasheet (địa chỉ, tên, R/W). Danh sách tham chiếu `[spec — kiểm memory map của datasheet; khớp với định nghĩa trong driver Zephyr và BME280_SensorAPI của Bosch]`:

| Địa chỉ | Tên | R/W | Ghi chú |
|---|---|---|---|
| 0x88–0xA1 | calib00…calib25 | R | Hệ số hiệu chuẩn nhiệt độ, áp suất (+ một byte độ ẩm) |
| 0xD0 | id | R | **0x60** cho BME280 |
| 0xE0 | reset | W | Ghi 0xB6 để soft reset |
| 0xE1–0xF0 | calib26…calib41 | R | Hệ số hiệu chuẩn độ ẩm |
| 0xF2 | ctrl_hum | R/W | Oversampling độ ẩm; **chỉ có hiệu lực sau khi ghi ctrl_meas** |
| 0xF3 | status | R | bit 3 `measuring`, bit 0 `im_update` |
| 0xF4 | ctrl_meas | R/W | osrs_t [7:5], osrs_p [4:2], mode [1:0] (00 sleep, 01/10 forced, 11 normal) |
| 0xF5 | config | R/W | t_sb [7:5], filter [4:2], spi3w_en [0] |
| 0xF7–0xF9 | press_msb/lsb/xlsb | R | Áp suất raw 20 bit |
| 0xFA–0xFC | temp_msb/lsb/xlsb | R | Nhiệt độ raw 20 bit |
| 0xFD–0xFE | hum_msb/lsb | R | Độ ẩm raw 16 bit |

**Câu 1:** VDD 1.71–3.6 V, VDDIO 1.2–3.6 V; absolute max VDD và VDDIO khoảng −0.3…4.25 V `[spec — kiểm bảng Absolute Maximum Ratings trong revision của bạn]`. 5 V thẳng vào chip vượt absolute max → có thể hỏng. 5 V vào VIN của module: **tùy module** — có LDO thì được, không có thì không. Câu trả lời đúng là "tùy, và tôi đã kiểm module của tôi ở bước 6".

**Câu 2:** 0x76 khi SDO nối GND, 0x77 khi SDO nối VDDIO; SDO không được để hở `[spec]`. Nhiều module đặt sẵn một trong hai bằng điện trở hoặc jumper hàn.

**Câu 3:** 0x60. Nếu ra **0x58**, đó là **BMP280** (không có cảm biến độ ẩm) — tình huống được báo cáo rộng rãi khi mua module rẻ ghi "BME280" `[chuẩn — kiểm bằng chính chip ID của bạn]`. 0x56/0x57 là mẫu BMP280 đời đầu. Ghi lại: đây là lần đầu bạn dùng chip ID như một **kiểm tra danh tính**, đúng như `GET /version`.

**Câu 4** `[spec — công thức ở phụ lục measurement time; hằng số max khớp với BME280_SensorAPI: 1250 µs + 2300 µs·osrs + 575 µs cho mỗi kênh P/H]`:

| Oversampling T/P/H | t_typ | t_max | (max − typ)/typ |
|---|---|---|---|
| ×1 / ×1 / ×1 | 1 + 2 + 2.5 + 2.5 = **8 ms** | 1.25 + 2.3 + 2.875 + 2.875 = **9.3 ms** | ≈ +16% |
| ×16 / ×16 / ×16 | 1 + 32 + 32.5 + 32.5 = **98 ms** | 1.25 + 36.8 + 37.375 + 37.375 = **112.8 ms** | ≈ +15% |

Quyết định đúng cho firmware: chờ theo **max** (cộng biên), hoặc poll bit `measuring` của status. Chờ theo typ là đặt cược vào phân bố mà nhà sản xuất không công bố.

**Câu 5 / bước 6:** pull-up trên module thường đọc ra cỡ 4.7–10 kΩ `[tự đo]`; module có mạch chuyển mức có thể cho số lạ hơn.

**Bước 8 (đo thời gian đo thật):** nếu phương pháp đúng, các lần đo nằm giữa typ và max, gần typ hơn, cộng sai số do khoảng poll. Nếu một lần vượt max đáng kể: kiểm phương pháp trước (mốc thời gian bắt đầu đặt sai chỗ?), rồi mới nghĩ tới chip.

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Không tìm thấy register map | Đang đọc trang bán hàng của module hoặc datasheet của BMP280 | Tên tài liệu trên trang 1, mã BST-BME280-DS002 | Tải đúng PDF từ Bosch Sensortec |
| Quá tải, không hiểu gì | Bình thường ở lần đầu | — | Lượt hai chỉ nhắm 6 mục trong bảng thứ tự đọc; bỏ compensation formula |
| Register map viết tay đúng <90% | Chép sai địa chỉ dải (calib), nhầm R/W | Đối chiếu từng dòng với memory map | Sửa trên giấy bằng bút màu khác, giữ cả bản sai — đó là dữ liệu |
| Không tìm thấy công thức measurement time | Nằm ở phụ lục cuối, không ở phần mô tả mode | Tìm chữ "measurement time" trong PDF | — |
| Module ghi "3.3V–5V" nhưng không thấy LDO | Có thể IC ổn áp rất nhỏ, hoặc module không có thật | Đo áp ở chân VDD của chip khi cấp 5 V vào VIN qua nguồn có giới hạn dòng (nếu có); không có nguồn bàn thì **không thử** | Cấp 3.3 V vào chân 3V3 của module cho chắc |
| Pull-up đo ra hàng trăm kΩ hoặc `OL` | Module không có pull-up | Đo lại cả SDA và SCL | Bài 12 phải thêm pull-up ngoài |
| Chip ID 0x58 ở Bài 12 | Module là BMP280 | — | Ghi lại; vẫn làm được Bài 12; không có độ ẩm |

### 9. Câu hỏi ngược

**[Nếu…thì]** Nếu firmware chờ đúng thời gian typical rồi đọc dữ liệu, chuyện gì xảy ra trên một số con chip hoặc ở nhiệt độ thấp? Dữ liệu ghi xuống trông thế nào, và audit tool ở K2 phát hiện được không?
<details><summary>Hướng nghĩ</summary>

Đọc trước khi đo xong thì nhận giá trị của lần đo trước (BME280 có cơ chế giữ bản sao dữ liệu nhất quán — tìm chữ "shadowing" trong datasheet). Dữ liệu không sai hẳn, nó **trễ một chu kỳ** và đôi khi lặp lại. Nghĩ xem lỗi "giá trị lặp lại" và "timestamp lệch một chu kỳ" khác gì "frozen channel" trong bảy lớp lỗi của K2 Bài 11.

</details>

**[Vì sao không]** Vì sao nhà sản xuất không ghi min/max cho mọi thông số mà để nhiều dòng chỉ có typical?
<details><summary>Hướng nghĩ</summary>

Mỗi con số min/max là một cam kết phải kiểm (test 100% trên máy test tốn thời gian máy = tiền), hoặc phải có đủ dữ liệu characterization để dám bảo đảm. Typical rẻ. Nghĩ như người viết SLA: bạn chỉ cam kết những gì bạn đo và trả được bồi hoàn. Hệ quả cho bạn: dòng chỉ có typical thì phải tự đo trên con của mình, với điều kiện của mình.

</details>

**[Quy mô]** Đội robot 500 con, mỗi con một BME280. Bạn dùng typical hay max cho: (a) ngân sách dòng sleep của cả đội, (b) timeout đọc cảm biến, (c) sai số nhiệt độ ghi vào metadata?
<details><summary>Hướng nghĩ</summary>

Ba câu có ba đáp án khác nhau. Tổng dòng của 500 con: trung bình của nhiều mẫu tiến về mean — typical là ước lượng hợp lý cho tổng (nếu typical gần mean), max cho một con xấu nhất. Timeout: một con chậm nhất là đủ gây lỗi → max. Sai số ghi metadata: phải là con số bảo đảm (max), không phải "thường thấy" (→ F1.1, F1.2: tail của 500 mẫu).

</details>

**[Failure mode]** Bạn lỡ cấp 5 V vào chân VDD của chip BME280 (module không có LDO) khoảng 3 giây rồi rút. Cắm lại 3.3 V, chip vẫn trả chip ID đúng. Kết luận "không sao" được không? Bạn sẽ kiểm gì thêm?
<details><summary>Hướng nghĩ</summary>

Chip ID chỉ kiểm khối giao tiếp và một thanh ghi ROM. Phần analog (cảm biến áp, màng ẩm) có thể đã trôi. Oracle mạnh hơn: so với một con chip thứ hai (nguyên tắc "mua 2 cái" của Bài 4) cùng chỗ, cùng lúc, trong nhiều giờ. Đây là bài toán oracle (→ F2.1): test pass không có nghĩa hệ đúng, nó chỉ có nghĩa test không đủ mạnh để thấy cái sai.

</details>

**[Liên ngành]** Trong hàng không, một máy bay có "flight envelope" với tốc độ không bao giờ được vượt (V_NE) và dải tốc độ hoạt động bình thường. Ánh xạ nó sang bốn vùng điện áp ở phần 2. Chỗ nào không ánh xạ được?
<details><summary>Hướng nghĩ</summary>

Vùng hoạt động ↔ recommended; vùng thận trọng (vàng trên đồng hồ tốc độ) ↔ giữa recommended max và absolute max; V_NE ↔ absolute max. Khác: phi công có thể "cảm thấy" máy bay rung khi gần biên, chip thì không báo gì. Và phi công có quy trình bắt buộc kiểm tra sau khi vượt (overspeed inspection) — bạn đã có quy trình nào tương tự cho linh kiện chưa?

</details>

**[Phản biện]** "Đọc trọn 60 trang là phí thời gian. Driver chính thức của Bosch đã cài đúng mọi thứ; chỉ cần đọc code driver."
<details><summary>Hướng nghĩ</summary>

Driver mã hóa *một* tập lựa chọn (chế độ, thời gian chờ, thứ tự ghi) — cho những trường hợp tác giả nghĩ tới. Datasheet cho bạn lý do của các lựa chọn đó và giới hạn của chúng. Khi dữ liệu lạ ở K5, bạn cần biết driver đang dựa vào typ hay max, và đó là quyết định của bạn chứ không phải của driver. Nhưng đọc driver cùng datasheet là một cách học rất tốt: nó cho bạn "test case" cho từng đoạn datasheet.

</details>

### 10. Liên kết ra ngoài

- **Dược phẩm — tờ hướng dẫn sử dụng thuốc.** Liều thông thường (≈ recommended operating), liều tối đa (≈ absolute max), chống chỉ định (≈ điều kiện ngoài vùng đặc tả), tác dụng phụ "thường gặp" kèm tần suất. Giống: hợp đồng có điều kiện. Khác: tờ thuốc ghi tần suất tác dụng phụ bằng con số thống kê; datasheet thường ghi typical mà không nói nó là thống kê gì.
- **Xây dựng — tải trọng thiết kế và hệ số an toàn.** Dầm được tính cho tải thiết kế nhân hệ số an toàn; vượt tải thiết kế chưa chắc gãy, nhưng không còn được bảo đảm, và có thể nứt ngầm. Giống hệt vùng giữa recommended max và absolute max, kể cả chuyện hỏng ngầm.
- **Phần mềm — semantic versioning và API deprecation.** "Preliminary" trong datasheet ≈ API `v0.x`: có thể đổi không báo. Khác: phần mềm đổi phiên bản bằng deploy; chip đã hàn thì là revision đó mãi mãi, và errata là cách duy nhất để biết nó sai ở đâu.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| Register map BME280 ở phần 7 (địa chỉ, tên, chip ID, reset, bit measuring) | `[spec]` | Memory map trong datasheet; khớp định nghĩa trong driver Zephyr (`drivers/sensor/bosch/bme280/bme280.h`) và BME280_SensorAPI của Bosch |
| Dải VDD/VDDIO hoạt động ở phần 7 | `[spec]` | Trang 1 và bảng điện của datasheet |
| Absolute max VDD/VDDIO ở phần 7 | `[spec — kiểm]` | Bảng Absolute Maximum Ratings; kiểm trong revision bạn tải |
| Công thức measurement time typ và max | `[spec]` | Phụ lục measurement time; hằng số của công thức max khớp `BME280_MEAS_OFFSET`, `BME280_MEAS_DUR`, `BME280_PRES_HUM_MEAS_OFFSET` trong `bme280_defs.h` của Bosch |
| ctrl_hum chỉ có hiệu lực sau khi ghi ctrl_meas | `[spec]` | Mô tả thanh ghi điều khiển độ ẩm |
| Chip ID khác giá trị của BME280 → BMP280; module rẻ ghi nhầm | `[chuẩn]` | Mã chip ID khớp driver Zephyr; chuyện ghi nhầm được báo nhiều trên diễn đàn — kiểm bằng chip của bạn |
| Challenger, Ariane 501 | `[chuẩn]` | Rogers Commission Report (1986); Ariane 501 Inquiry Board Report (1996) |

**Đã sửa so với bản gốc:**

1. Bản gốc không có `prediction.md` cho bài này, trong khi gate (Bài 14, tiêu chí 2) yêu cầu 5 thư mục lab đều có `prediction.md` commit trước `analysis.md`. Sửa: thêm phần dự đoán (hiệu chuẩn trực giác + tính measurement time) và một phép đo thật (bước 8).
2. Bản gốc ví chip ID với `/health`. Sửa: chip ID là kiểm tra **danh tính và giao tiếp** (gần `/version` hơn), không phải health check của phép đo; đã chấm ở phần 3.
3. Thêm phân biệt recommended operating vs absolute max (bản gốc chỉ có absolute max), typical vs min/max, quy tắc thứ tự ghi thanh ghi, kiểm module ≠ chip bằng đo pull-up và tìm LDO.
4. "Số phải ra" niêm phong.

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** Bosch Sensortec, *BME280 — Combined humidity and pressure sensor, Datasheet* (BST-BME280-DS002, revision mới nhất).
- **Giải thích:** SparkFun Learn, "How to Read a Datasheet"; EEVblog (Dave Jones) có tập về đọc datasheet — nên xem hai lần như roadmap gợi ý.
- **Đào sâu (tùy chọn):** mã nguồn `BME280_SensorAPI` của Bosch trên GitHub — đọc song song với datasheet, tìm từng hằng số trong code về lại trang datasheet của nó.
- **Tự kiểm tra:** (1) giải thích lại cho một backend engineer khác trong 5 câu vì sao vượt absolute max khác với vượt rate limit; (2) vẽ lại hình bốn vùng điện áp từ trí nhớ; (3) hai câu dưới.

1. Một dòng trong datasheet: "Supply current, typ 3.6 µA, condition: 1 Hz forced mode, humidity + pressure + temperature, osrs ×1". Bạn chạy 10 Hz, oversampling ×16. Dùng được con số này không?
2. Datasheet một chip ghi "VDD absolute max 4.0 V, recommended 2.7–3.6 V". Pin Li-ion một cell sạc đầy ~4.2 V. Cấp thẳng được không?

<details><summary>Đáp án</summary>

1. Không trực tiếp. Điều kiện khác cả tần số và oversampling. Dòng trung bình xấp xỉ tỉ lệ với (thời gian đo × dòng khi đo × tần số) + dòng sleep; tìm bảng/công thức dòng theo chế độ trong datasheet và tính lại. Con số 3.6 µA chỉ đúng trong đúng điều kiện ghi cạnh nó.
2. Không. 4.2 V vượt cả recommended max lẫn absolute max. Cần ổn áp (LDO/buck) giữa pin và chip. Đây chính là lý do ở K7 mini PC và logic đều ăn qua DC-DC, không ăn thẳng từ pin (→ K7 C1.4).

</details>

---
