# Khóa 1 — Phần C: Đo thật (14h)

Từ phần này trở đi mọi bài đi theo một quy trình duy nhất: **viết dự đoán bằng số → `git commit` → rồi mới cắm que đo**. `prediction.md` là preregistration của bạn (→ F1.7): một bản ghi có timestamp chứng minh bạn đã đoán trước khi nhìn số. Gate Khóa 1 (→ `d-du-lieu-tren-day.md`, Bài 14) kiểm đúng thứ tự commit này.

| Bài | Giờ | Viên nang nền nên đọc cùng lúc |
|---|---|---|
| 9 — Voltage divider | 5h | F1.1 (bắt buộc), F6.6 (lướt phần Monte Carlo) |
| 10 — LED và điện trở | 4h | F1.1, F6.1 |
| 11 — Đọc trọn một datasheet | 5h | F2.1 (lướt), F3.7 (lướt) |

Bản gốc chỉ ghi Phần C = 14h, không chia theo bài; cách chia trên là đề xuất.

---

## Bài 9 — Voltage divider: thí nghiệm đầu tiên có dự đoán (5h)

> **Vị trí:** Bài 8 (mỏ hàn) → **Bài 9** → Bài 10 (LED) · **Cần trước:** Bài 1–2 (Ohm, nối tiếp, GND), Bài 5 (multimeter), Bài 6 (breadboard), F1.1 (độ bất định, sai số hệ thống vs ngẫu nhiên, lan truyền sai số) · **Sau bài này bạn quyết định được:** chọn cặp điện trở cho một divider (đo mức pin, hạ mức một tín hiệu chậm) khi biết trở kháng của thứ sẽ đọc nó, và phân xử một sai lệch đo là "đúng theo dung sai" hay "có lỗi".

### 1. Câu chuyện — ai đã khổ vì chuyện này

Thế kỷ 19, đo một suất điện động là chuyện khó vì mọi vôn kế thời đó đều *hút dòng* từ chính thứ nó đo, và điện áp đọc được luôn thấp hơn điện áp thật. Poggendorff (1841) đưa ra phương pháp bù (compensation/potentiometer method): đặt một nguồn điều chỉnh được ngược chiều với nguồn cần đo, vặn tới khi điện kế chỉ số 0. Lúc cân bằng không có dòng chạy qua nguồn cần đo, nên phép đo không làm thay đổi nó `[chuẩn]`. Cả một nhánh dụng cụ ra đời chỉ để né một vấn đề: **dụng cụ đo là một phần của mạch**.

Vấn đề đó không biến mất. Đồng hồ kim (VOM) của thợ điện tử thế kỷ 20 ghi độ nhạy bằng "Ω/V" (kiểu 20 kΩ/V): trên thang 10 V, đồng hồ chỉ là một điện trở 200 kΩ cắm song song vào mạch. Vôn kế đèn điện tử (VTVM) rồi đồng hồ số với trở kháng vào cỡ 10 MΩ ra đời phần lớn vì lý do này `[chuẩn]`. Đồng hồ UT33D+ của bạn là hậu duệ của lịch sử đó, nhưng **10 MΩ vẫn không phải vô cùng**. Bài này cho bạn tự tay nhìn thấy chỗ nó không còn là vô cùng.

Divider là mạch phổ biến nhất trong điện tử: đọc biến trở, đo mức pin bằng ADC, hạ mức một tín hiệu 5 V chậm xuống 3.3 V. Nó cũng là nơi người mới hay mắc một lỗi kinh điển: dùng divider làm **nguồn** hạ áp. Lỗi đó là chủ đề thí nghiệm phá ở cuối bài.

### 2. Mô hình tư duy

```
  Mạch thật                         Cái mà "điểm giữa" nhìn ra ngoài
  ─────────                         ─────────────────────────────────
  Vin ──[R1]──┬── Vout                 Vth ──[Rth]──┬── Vout
              │                                     │
             [R2]   ║ que đo = [Rm]                [RL]  ← bất cứ thứ gì đọc Vout:
              │     ║ (~10 MΩ)                      │      đồng hồ, ADC, chân GPIO
  GND ────────┴─────╨──                GND ─────────┴──

  Vth = Vin · R2/(R1+R2)      Rth = R1·R2/(R1+R2)  (R1 // R2)
  Vout khi có tải RL = Vth · RL/(Rth + RL)  ≈ Vth · (1 − Rth/RL)   khi RL ≫ Rth
```

1. **Công thức `Vout = Vin·R2/(R1+R2)` chỉ đúng khi không ai lấy dòng ra từ điểm giữa.** Mọi thứ đọc Vout đều là một tải `RL` song song với R2.
2. Nhìn từ điểm giữa ra, cả divider tương đương **một nguồn Vth nối tiếp một điện trở Rth = R1 // R2** (tên chuẩn: tương đương Thevenin, chỉ cần biết tên). Rth là "độ yếu" của nguồn: Rth càng lớn, tải càng làm Vout sụt nhiều.
3. **Sai số tương đối do tải ≈ Rth/RL.** Đây là con số duy nhất bạn cần để chọn điện trở: muốn sai số tải < 1%, cần RL ≥ 100·Rth.
4. **Dung sai lan truyền không đều giữa các cặp.** Với `k = R2/(R1+R2)`, sai số tương đối của Vout là `δVout/Vout ≈ (1 − k)·(δR2 − δR1)`. Khi k gần 1 (R2 ≫ R1), dung sai gần như bị triệt tiêu; khi k nhỏ, gần như toàn bộ dung sai của cả hai điện trở đổ vào Vout. Cùng hai con điện trở ±5%, ba cặp trong bài sẽ có ba dải chấp nhận khác nhau.
5. Có một đánh đổi không né được: Rth nhỏ (điện trở nhỏ) thì "cứng" trước tải nhưng đốt dòng liên tục `Vin/(R1+R2)` ngay cả khi không ai đọc; Rth lớn thì tiết kiệm nhưng mềm. Divider đo pin trên thiết bị chạy pin luôn nằm ở giữa đánh đổi này.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Observer effect của tracing/profiler: bật profiler làm service chậm đi, Heisenbug biến mất khi gắn debugger | Đồng hồ 10 MΩ song song với R2 kéo Vout xuống | Ở phần mềm, overhead thường nhiễu và khó tính; ở đây hiệu ứng là **tất định và tính được chính xác** từ Rth/Rm, nên **hiệu chỉnh ngược được** | Coi nó là nhiễu ngẫu nhiên rồi đo nhiều lần lấy trung bình → sai lệch vẫn y nguyên, vì đó là sai số hệ thống (→ F1.1) |
| Service chậm dần khi tải tăng | Divider "sụp" khi có tải | Service có đầu gối utilization: ổn tới ~70–80% rồi mới vỡ (→ F7.1). Divider **không có đầu gối**: Vout sụt tuyến tính theo dòng tải ngay từ microampe đầu tiên | Thiết kế kiểu "tải nhỏ thì chưa sao" → mọi tải đều làm sai số, câu hỏi chỉ là bao nhiêu |
| Error budget latency: cộng p99 các chặng | Cộng dung sai: R1, R2, đồng hồ | Latency chỉ cộng dồn; sai số **có thể triệt tiêu** (hệ số (1−k)·(δR2 − δR1) ở trên) và sai số tương quan triệt tiêu khi chia tỉ số (cùng một đồng hồ đo Vin và Vout) | Cộng worst-case mọi nguồn → dải chấp nhận rộng vô nghĩa; hoặc coi mọi nguồn độc lập → bỏ sót sai số tương quan |
| Hằng số cấu hình `VIN = 5` | Vin thật của chân 5V | Trong code, hằng số là sự thật; ở đây "5 V" là **giá trị danh định**, giống con số trong SLA: lời hứa, không phải số đo | Không đo Vin → mọi so sánh lệch thêm vài phần trăm và bạn đổ lỗi cho điện trở |

**Chấm mô hình:**

- *"Divider là bộ hạ áp: muốn có 3.3 V từ 5 V thì dùng 1k/2k rồi cấp cho module."* — **SAI.** Divider chỉ cho đúng Vout khi tải ≫ Rth. Phản ví dụ: 1k/2k có Rth ≈ 667 Ω; một ESP32 khi bật WiFi kéo hàng trăm mA, tương đương tải chỉ vài chục ohm, nên Vout sụp xuống một phần nhỏ của 3.3 V và chip reset. Hạ áp để **cấp nguồn** là việc của regulator (LDO/buck) — chúng có trở kháng ra cỡ mΩ nhờ vòng hồi tiếp. Divider chỉ dùng cho **tín hiệu** đi vào một đầu vào trở kháng cao.
- *Mô hình của bạn ở K3 lượt 11:* "mọi thiết bị khi chung nguồn … luôn có trường hợp sụt nguồn … vì chiếm dụng nguồn chung là xảy ra." — **ĐÚNG MỘT PHẦN.** Đúng là sụt áp xảy ra ở mọi hệ chung nguồn. Gãy ở cơ chế: không phải "chiếm dụng" một bể tài nguyên có hạn (kiểu connection pool cạn), mà là **dòng tổng chạy qua trở kháng chung** (trở kháng ra của nguồn + dây + mối nối) sinh ra sụt áp `I·Z`. Phản ví dụ: một adapter 3 A nuôi ESP32 qua một sợi jumper dài mảnh vẫn có thể làm ESP32 reset ở vài trăm mA — nguồn còn dư rất nhiều "dung lượng", nhưng trở kháng của dây đủ để sụt áp. Divider là trường hợp cực đoan và dễ tính nhất của cùng hiện tượng (Rth chính là Z chung). Ở K3 Bài 6 bạn sẽ gặp phiên bản động: dòng tăng đột ngột qua điện cảm của dây.
- *"Que đo chỉ đọc, giống `SELECT` — không đổi dữ liệu."* — **ĐÚNG MỘT PHẦN.** Gần đúng khi Rm ≫ Rth (cặp 10k/10k). Sai rõ khi Rth tiến tới cỡ Rm/20. Phản ví dụ: chính thí nghiệm phá ở bước 5. Đồng hồ ở chế độ đo dòng thì còn tệ hơn: nó chèn một điện trở shunt vào mạch (Bài 10).

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | Voltage divider (cầu phân áp) | Hai điện trở nối tiếp, điểm giữa cho một phần của Vin theo tỉ lệ R2/(R1+R2) | Bộ hạ áp cấp nguồn |
| 🟢 | Nominal (danh định) / tolerance (dung sai) | Giá trị in trên linh kiện / khoảng giá trị thật được phép lệch (vàng kim ±5%, nâu ±1%) | Giá trị thật; hoặc "±5% nghĩa là thường lệch 5%" |
| 🟢 | Loading effect (hiệu ứng tải) | Thứ đọc tín hiệu lấy dòng ra và làm tín hiệu thay đổi | Lỗi của đồng hồ |
| 🟢 | Input impedance (trở kháng vào) | Điện trở tương đương mà một đầu vào (đồng hồ, ADC, chân GPIO) đặt lên mạch | Vô cùng |
| 🟡 | Output/source impedance (trở kháng ra, Rth) | Điện trở tương đương nhìn từ đầu ra vào nguồn; càng nhỏ nguồn càng "cứng" | Chỉ có ở nguồn điện |
| 🔴 | Thevenin equivalent | Tên chuẩn của phép quy một mạch tuyến tính về Vth nối tiếp Rth; biết tên, không cần học phương pháp | — |
| 🟢 | Accuracy spec `±(a% rdg + n digit)` | Cách đồng hồ số ghi sai số: một phần theo số đọc, một phần theo chữ số cuối của thang đang dùng | "±0.5%" là hết |
| 🟢 | Count / resolution | Số đếm tối đa của màn hình (2000 count → thang 2 V hiện tới 1.999) và bước nhỏ nhất | Độ chính xác |
| 🟢 | Sai số hệ thống vs ngẫu nhiên | Lệch cùng chiều mỗi lần đo vs dao động quanh giá trị thật (→ F1.1) | Lấy trung bình là khử được mọi sai số |
| 🟡 | Worst-case vs RSS | Cộng trị tuyệt đối mọi sai số (an toàn, bi quan) vs căn tổng bình phương (giả định độc lập) | Chỉ có một cách "đúng" |

### 5. Dự đoán

**Tham số cần tra / đo trước, ghi vào `prediction.md`:**

| Tham số | Lấy ở đâu |
|---|---|
| Vin danh định | Chân 5V của ESP32-S3 DevKit cắm USB (sẽ đo lại) |
| Dung sai điện trở | Vạch thứ 4 (vàng kim ±5%, nâu ±1%); kit thân xanh 5 vạch thường là ±1% — kiểm vạch, đừng đoán |
| Sai số DCV của đồng hồ, số count, các thang | Manual UT33D+, bảng "DC Voltage" (dạng `±(a% + n)`) |
| Trở kháng vào DCV | Manual UT33D+ (nếu có ghi); nếu không có, giả định 10 MΩ và gắn `[tự đo]` — bước 7 sẽ đo nó |

**Công thức/phương pháp (không có đáp án ở đây):**

- Vout danh định: `Vin·R2/(R1+R2)`.
- Dải do dung sai, worst-case: `±(1 − k)·(tol_R1 + tol_R2)` với `k = R2/(R1+R2)`. RSS (phân bố đều): `(1 − k)·√2·tol/√3`.
- Sai số đồng hồ ở mỗi số đọc: `a%·|V| + n·(bước của thang)`; thang 2 V của đồng hồ 2000 count có bước 1 mV, thang 20 V có bước 10 mV.
- Cặp 1 MΩ/1 MΩ có đồng hồ cắm vào: thay R2 bằng `R2 // Rm` rồi tính lại.
- Kiểm KVL (bước 6): đo riêng điện áp trên R1 và trên R2 rồi cộng lại. Nếu đồng hồ không tải mạch thì tổng phải bằng Vin; nếu có tải thì tổng thiếu bao nhiêu?

**Mô phỏng trước khi cắm** — chạy trên laptop, đổi `VIN_TRUE`, `TOL`, `R_METER` theo số bạn tra được. Ghi kết quả vào `prediction.md` **trước** khi đo. Kết quả mẫu nằm trong phần 7.

```python
# [đã chạy] Monte Carlo cho voltage divider: dung sai điện trở + sai số đồng hồ + tải của đồng hồ
import numpy as np
rng = np.random.default_rng(0)
N = 100_000
VIN_TRUE = 4.90          # giả định: chân 5V của DevKit thường thấp hơn 5.00 V [tự đo]
TOL = 0.05               # điện trở vạch vàng kim ±5%, coi là phân bố đều (GUM loại B)
R_METER = 10e6           # trở kháng vào DCV ~10 MΩ [ước lượng — tra manual / tự đo]

def meter(v):
    """Đồng hồ 2000 count, đổi thang tay: ±(0.5% + 2 digit), lỗi coi là phân bố đều."""
    rng_full = np.where(np.abs(v) < 2.0, 2.0, 20.0)      # thang 2 V hoặc 20 V
    digit = rng_full / 2000
    err = 0.005 * np.abs(v) + 2 * digit
    return np.round((v + rng.uniform(-1, 1, v.shape) * err) / digit) * digit

def par(a, b):
    return a * b / (a + b)

pairs = [(10e3, 10e3), (10e3, 1e3), (1e3, 10e3), (1e6, 1e6)]
print(f"{'R1/R2':>12} {'p2.5%':>7} {'p50':>7} {'p97.5%':>7} {'P(|e|>5%)':>10} {'KVL sum/Vin':>11}")
for r1n, r2n in pairs:
    r1 = r1n * (1 + rng.uniform(-TOL, TOL, N))
    r2 = r2n * (1 + rng.uniform(-TOL, TOL, N))
    # que đo đặt lên R2: đồng hồ song song với R2
    vout_true = VIN_TRUE * par(r2, R_METER) / (r1 + par(r2, R_METER))
    vr1_true = VIN_TRUE * par(r1, R_METER) / (r2 + par(r1, R_METER))
    vin_m = meter(np.full(N, VIN_TRUE))
    vout_m = meter(vout_true)
    vr1_m = meter(vr1_true)
    pred = vin_m * r2n / (r1n + r2n)          # dự đoán danh định, đã hiệu chỉnh Vin đo
    e = (vout_m - pred) / pred * 100
    kvl = (vout_m + vr1_m) / vin_m
    p = np.percentile(e, [2.5, 50, 97.5])
    label = f"{r1n/1e3:g}k/{r2n/1e3:g}k"
    print(f"{label:>12} {p[0]:7.2f} {p[1]:7.2f} {p[2]:7.2f} {np.mean(np.abs(e) > 5):10.3f} {np.median(kvl):11.3f}")

# Suy ngược trở kháng vào của đồng hồ từ cặp 1M/1M khi đã đo R1, R2 bằng chế độ Ω (±1%)
r1, r2 = 1e6 * 1.012, 1e6 * 0.991                  # "giá trị đo được" giả định
vout = VIN_TRUE * par(r2, R_METER) / (r1 + par(r2, R_METER))
r1m = r1 * (1 + rng.uniform(-.01, .01, N)); r2m = r2 * (1 + rng.uniform(-.01, .01, N))
vin_m = meter(np.full(N, VIN_TRUE)); vo_m = meter(np.full(N, vout))
rp = r1m * vo_m / (vin_m - vo_m)                   # = R2 // Rm
rm = 1 / (1 / rp - 1 / r2m)
rm = rm[(rm > 0) & (rm < 1e9)]
print("Rm suy ngược (MΩ) p5/p50/p95:", np.round(np.percentile(rm, [5, 50, 95]) / 1e6, 1))
```

**Mẫu `lab/01-voltage-divider/prediction.md`** (copy, điền, commit):

```markdown
# Dự đoán — voltage divider
Ngày: YYYY-MM-DD · Đồng hồ: UT33D+ · Sai số DCV (tra manual): ±(__% + __ digit), thang dùng: __ V
Trở kháng vào DCV: __ MΩ (nguồn: manual / giả định [tự đo])
Vin danh định: 5.00 V (sẽ đo lại; mọi dự đoán dưới đây sẽ tính lại theo Vin đo)

| R1 | R2 | k = R2/(R1+R2) | Vout dự đoán (V) | Dải do dung sai (worst / RSS) | Sai số đồng hồ ở mức này (V) | Dải chấp nhận cuối (V) |
|---|---|---|---|---|---|---|
| 10 kΩ | 10 kΩ | | | | | |
| 10 kΩ | 1 kΩ | | | | | |
| 1 kΩ | 10 kΩ | | | | | |
| 1 MΩ | 1 MΩ | | (không tải) __ / (có Rm) __ | | | |

Cặp nào nhạy với dung sai nhất? Vì sao (một câu, dùng hệ số 1−k):
Kiểm KVL cặp 10k/10k: V_R1 + V_R2 = __ V. Cặp 1M/1M: __ V.
Kết quả Monte Carlo (dán bảng in ra):
```

`git commit -m "lab01: prediction"`. **Bắt buộc trước bước 2.**

### 6. Làm

**Thói quen từ bài này trở đi (REP-103):** mọi con số ghi kèm đơn vị SI — `V`, `A`, `Ω`, `s`, `Hz`. Không ghi "2.5" trần trụi. Từ Khóa 2 đây là chuẩn dữ liệu của cả ngành (`CONVENTIONS.md`). Thêm một thói quen nữa: **ghi số đúng với độ phân giải của thang**, không thêm chữ số đồng hồ không hiển thị.

**Bước 0 — đo từng điện trở (mới, so với bản gốc).** Rút điện trở ra khỏi mạch, đo bằng thang Ω, ghi vào bảng. Không cầm hai đầu điện trở bằng hai tay (cơ thể bạn song song với nó — Bài 5). Sai số thang Ω tra trong manual; ghi lại. Bước này tách được hai nguồn sai số: dung sai linh kiện và sai số đo điện áp.

**Bước 1 — dự đoán, commit** (phần 5).

**Bước 2 — dựng mạch.** Trên breadboard: 5V → R1 → (điểm giữa) → R2 → GND. Nguồn 5V lấy từ chân 5V của ESP32 đang cắm USB. GND của mạch là GND của ESP32.

**Bước 3 — đo.**
1. Đo Vin thật giữa chân 5V và GND. Ghi lại — nó hiếm khi đúng 5.00 V `[tự đo]`. Ghi luôn thang đang dùng.
2. Đo Vout giữa điểm giữa và GND.
3. Lặp cho cả ba cặp 10k/10k, 10k/1k, 1k/10k. Mỗi cặp đo Vin lại một lần (Vin có thể đổi khi bạn cắm/rút).
4. Ghi sai số đồng hồ cho **từng** số đọc theo công thức ở phần 5. Một số đọc không có sai số đi kèm chưa phải là kết quả.

**Bước 4 — ghi vào `analysis.md`:** bảng `dự đoán (theo Vin đo) / đo / chênh lệch %`, thêm cột `dự đoán theo R đo ở bước 0`. Thêm một cột tỉ số `Vout/Vin` đo được so với `R2/(R1+R2)` — tỉ số này loại được phần lớn sai số tỉ lệ (gain) của đồng hồ khi Vin và Vout đo cùng thang (→ F1.1, sai số tương quan).

**Bước 5 — thí nghiệm phá: làm cái này, nó dạy nhiều nhất.** Đổi cả hai điện trở sang **1 MΩ** (nâu–đen–xanh lục). Tỉ lệ vẫn 1:1. Đo ở bước 0 cả hai con trước khi cắm. Đo Vout. So với dự đoán *không tải* và dự đoán *có Rm*. Trong lúc đo, không chạm tay vào điểm giữa: một nút 1 MΩ đủ "mềm" để bắt nhiễu từ cơ thể, số sẽ nhảy.

**Bước 6 — kiểm KVL để phát hiện tải mà không cần biết dung sai.** Với cả cặp 10k/10k và cặp 1M/1M, đo riêng `V_R1` (hai đầu R1) và `V_R2` (hai đầu R2), cộng lại, so với Vin. Định luật Kirchhoff về điện áp (KVL) nói tổng phải bằng Vin *trong mạch không bị đo*. Chỗ thiếu hụt là dấu vân tay của đồng hồ: dung sai điện trở gần như không ảnh hưởng đến tổng này, nên phép kiểm này phân biệt được "tải" và "dung sai".

**Bước 7 — suy ngược trở kháng vào của đồng hồ.** Từ Vin, Vout (cặp 1M/1M) và R1, R2 đo ở bước 0:
`R2 // Rm = R1·Vout/(Vin − Vout)`, rồi `Rm = 1 / (1/(R2//Rm) − 1/R2)`. Ghi Rm kèm khoảng bất định (dùng phần cuối của script Monte Carlo, thay số của bạn). Bạn vừa làm *nhận dạng hệ thống* (→ F6.4) trên chính dụng cụ đo của mình: dùng một mạch biết trước để đo một tham số của đồng hồ.

**Bước 8 (tùy chọn, 15 phút).** Lặp bước 5 ở thang 2 V nếu Vout đủ nhỏ (dùng cặp 1M trên 10M nếu kit có), xem Rm có đổi theo thang không `[tự đo]`.

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

**Bảng của bản gốc** (Vin = 5.00 V; tính lại theo Vin đo trước khi so):

| Cặp | Vout dự đoán | Chấp nhận được (bản gốc, ±5%) |
|---|---|---|
| 10k / 10k | 2.500 V | 2.38 – 2.63 V |
| 10k / 1k | 0.455 V | 0.43 – 0.48 V |
| 1k / 10k | 4.545 V | 4.32 – 4.77 V |

**Tiêu chí PASS giữ như gốc: sai lệch < 5% sau khi hiệu chỉnh Vin.** Nhưng đọc kết quả Monte Carlo (Vin = 4.90 V, điện trở ±5% phân bố đều, đồng hồ ±(0.5% + 2 digit), Rm = 10 MΩ):

| Cặp | p2.5% | p50 | p97.5% | Xác suất \|sai lệch\| > 5% | Tổng KVL / Vin |
|---|---|---|---|---|---|
| 10k/10k | −4.3% | 0.0% | +4.3% | ~2% | 1.000 |
| 10k/1k | −7.0% | 0.0% | +7.5% | **~21%** | 1.000 |
| 1k/10k | −1.6% | 0.0% | +1.6% | 0% | 1.000 |
| 1M/1M | −8.9% | **−4.7%** | −0.6% | ~46% | **0.953** |

Rm suy ngược từ cặp 1M/1M (R đo ±1%): p5/p50/p95 ≈ 7.3 / 10.0 / 15.5 MΩ.

Đọc bảng:

- **Ba cặp không có cùng dải chấp nhận.** Cặp 1k/10k (k ≈ 0.91) gần như miễn nhiễm dung sai: worst-case chỉ ~±0.9% cộng sai số đồng hồ. Cặp 10k/1k (k ≈ 0.09) gánh gần trọn dung sai của cả hai điện trở: worst-case ~±9%. Với điện trở ±5%, cặp 10k/1k **có thể trượt tiêu chí 5% mà không có lỗi gì** (~1/5 khả năng nếu dung sai phân bố đều; thực tế phân bố thường hẹp hơn dải in trên vạch, nên tỉ lệ thật thấp hơn `[ước lượng]`). Nếu trượt: tính lại dự đoán với R đo ở bước 0. Sai lệch còn lại phải nằm trong sai số đồng hồ (~1%) — khi đó ghi PASS kèm giải thích. Đây là cách đọc đúng tiêu chí gốc, không phải nới tiêu chí.
- Ngược lại, cặp 1k/10k lệch 3% là **đáng ngờ** dù vẫn "dưới 5%": dung sai không giải thích được mức đó. Hãy nghi Vin đổi giữa hai lần đo, hoặc đọc nhầm mã màu.
- **1M/1M: Vout thấp hơn khoảng 4–5%** (với Rm ≈ 10 MΩ: 1 MΩ // 10 MΩ ≈ 0.909 MΩ → Vout ≈ 0.476·Vin). Bản gốc gọi đây là "thấp hơn rõ rệt" — thực ra mức này **ngang dung sai ±5%**, nên chỉ nhìn Vout thì không chứng minh được gì. Hai cách làm hiệu ứng tải hiện rõ: dự đoán theo R đo ở bước 0 (dự đoán chặt còn ~1–2%, chênh 4–5% nổi bật), hoặc **kiểm KVL**: tổng V_R1 + V_R2 thiếu ~5% so với Vin ở cặp 1M, trong khi cặp 10k cho tổng khớp Vin trong sai số đồng hồ. Vì mỗi lần đo, đồng hồ song song với *điện trở đang đo* và kéo áp của nó xuống.
- **Rm suy ngược có khoảng bất định rộng** (thấy trong Monte Carlo), vì Rm chỉ ảnh hưởng ~5% tới Vout, nên 1% sai số của R hay đồng hồ phóng to lên nhiều lần trong Rm. Một phép đo gián tiếp càng ít nhạy với đại lượng cần tìm, sai số càng bị phóng đại. Muốn đo Rm chặt hơn: dùng R2 lớn hơn (10 MΩ), để Rm chiếm phần lớn hơn trong `R2 // Rm`.
- Mô phỏng coi sai số đồng hồ ở mỗi lần đo là độc lập. Thật ra phần `a%` là sai số tỉ lệ, tương quan giữa các lần đo trên cùng thang, nên tỉ số Vout/Vin thật chặt hơn mô phỏng. Đó là lý do bước 4 có cột tỉ số.

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Vout = Vin | R2 hở — cắm nhầm hàng breadboard, chân không tiếp xúc | Thông mạch từ điểm giữa xuống GND qua R2 (tắt nguồn) | Cắm lại, đổi hàng |
| Vout = 0 | R1 hở, hoặc điểm giữa bị nối thẳng xuống GND | Thông mạch hai đầu R1 | Cắm lại |
| Vout lệch > 20% | Đọc nhầm mã màu (10k vs 1k vs 100k) | Bước 0: đo từng con bằng Ω | Thay đúng con |
| Cặp 10k/1k lệch quá 5%, hai cặp kia ổn | Dung sai đổ dồn vào cặp k nhỏ (phần 2, ý 4) | Dự đoán lại theo R đo | Không cần sửa mạch; ghi giải thích |
| Số nhảy liên tục | Que đo chạm chập chờn; ở cặp 1M: nút trở kháng cao bắt nhiễu từ tay | Kẹp que bằng kẹp cá sấu, bỏ tay ra | Kẹp cố định |
| Vin đổi khi đổi cổng USB / cáp | Cổng USB và cáp có sụt áp riêng | Đo Vin ngay trước mỗi Vout | Luôn dự đoán theo Vin đo cùng lúc |
| Cặp 1M/1M gần như không sụt | Đồng hồ có trở kháng vào lớn hơn nhiều ở thang đang dùng, hoặc R2 thật nhỏ hơn danh định | Bước 7 + bước 8, đổi thang | Ghi Rm thật của bạn vào notebook — số đó dùng lại suốt lộ trình |
| Tổng KVL ở cặp 10k thiếu > 2% | Vin trôi giữa các lần đo, hoặc tiếp xúc breadboard có điện trở | Đo Vin trước và sau | Kẹp chắc, đo nhanh liên tiếp |

### 9. Câu hỏi ngược

1. **[Nếu…thì]** Nếu thay đồng hồ bằng ADC của ESP32 để đọc điểm giữa của cặp 1M/1M, sai số có giống đồng hồ không? ADC không phải điện trở 10 MΩ cố định mà là một tụ lấy mẫu được nối vào rồi ngắt ra theo nhịp.
   <details><summary>Hướng nghĩ</summary>Tụ lấy mẫu phải được nạp qua Rth trong một khoảng thời gian ngắn; Rth lớn thì nó nạp không kịp, sai số phụ thuộc tốc độ lấy mẫu chứ không chỉ tỉ số điện trở. Lời giải kinh điển là một tụ đệm ở điểm giữa hoặc một op-amp buffer. Datasheet ESP32-S3 (mục ADC) có gợi ý về trở kháng nguồn — tra ở K5 Bài 4.</details>
2. **[Quy mô]** 100 robot, mỗi con đo pin bằng divider 100k/100k ±1% vào ADC. Ở 1000 giờ vận hành, con số "% pin" trên dashboard của đội vận hành sai ở đâu trước: dung sai điện trở, sai số ADC từng chip, hay nhiệt độ? Bạn lưu hiệu chuẩn theo từng con hay theo lô?
   <details><summary>Hướng nghĩ</summary>Phân biệt sai số cố định theo từng thiết bị (hiệu chuẩn một lần là khử được) với sai số trôi theo thời gian/nhiệt. Sai số cố định theo thiết bị là lý do `CONVENTIONS.md` bắt buộc có `calibration_id`. Hỏi thêm: khi thay một board, ai đảm bảo hiệu chuẩn cũ không bị áp nhầm cho board mới?</details>
3. **[Failure mode]** Ai đó dùng divider 10k/20k để hạ tín hiệu UART 5 V → 3.3 V ở 1 Mbaud, và dùng cùng cách cho đường SDA của I2C. Cái nào hỏng, hỏng kiểu gì, và có thể chạy "được" trong lúc thử nghiệm không?
   <details><summary>Hướng nghĩ</summary>Chân vào có điện dung vài pF; Rth của divider cùng điện dung đó tạo hằng số thời gian RC làm bo tròn cạnh — tính RC rồi so với độ rộng một bit. I2C là hai chiều và open-drain (Bài 12): divider chặn chiều ngược lại. "Chạy được ở bàn, hỏng ở dây dài" là dấu hiệu của bài toán biên độ thời gian.</details>
4. **[Vì sao không]** Vì sao không dùng luôn 10 Ω/10 Ω cho "cứng" trước mọi tải?
   <details><summary>Hướng nghĩ</summary>Tính dòng và công suất trên mỗi điện trở với Vin 5 V, so với định mức 1/4 W. Rồi nghĩ tới nguồn: divider đó là tải gì đối với chân 5V của USB? Mọi thiết kế divider là chọn một điểm trên đường đánh đổi giữa dòng tĩnh và Rth.</details>
5. **[Phản biện]** Tiêu chí "sai lệch < 5% cho cả ba cặp" có phải là một test tốt không? Nó có dương tính giả/âm tính giả kiểu gì (→ F2.1)?
   <details><summary>Hướng nghĩ</summary>Một ngưỡng cố định cho ba phép đo có độ nhạy khác nhau thì quá lỏng ở chỗ này và quá chặt ở chỗ kia. Một test tốt hơn: ngưỡng tính từ ngân sách sai số của từng cặp. Đây chính là bài toán "test là một phép đo có tỉ lệ sai" bạn đã gặp khi viết script chấm pass/fail.</details>
6. **[Liên ngành]** Ngành điện lực có khái niệm "lưới yếu" khi nối một nhà máy điện gió vào điểm có trở kháng lưới lớn. Nó giống divider bị tải ở chỗ nào?
   <details><summary>Hướng nghĩ</summary>Tra "short circuit ratio" (SCR). Đó là cùng tỉ số Rth/RL, nhìn từ phía nguồn. Khác biệt: lưới là AC, có thành phần cảm kháng, và tải không thụ động.</details>

### 10. Liên kết ra ngoài

- **Đo lường điện thế kỷ 19–20 (phương pháp bù, VTVM).** Giống: cả ngành dụng cụ đo tiến hóa để giảm dòng hút từ mạch bị đo. Khác: phương pháp bù triệt tiêu hiệu ứng tải bằng cân bằng (dòng = 0 lúc đọc), còn đồng hồ số chỉ làm nó nhỏ đi (Rm lớn), không triệt tiêu. Hệ quả: với đồng hồ số bạn luôn phải hỏi "Rth của điểm đo là bao nhiêu".
- **Tracing/profiling trong hệ phân tán.** Giống: công cụ quan sát thay đổi hành vi hệ bị quan sát (sampling profiler làm lệch phân bố latency; log đồng bộ làm mất race condition). Khác: ở mạch tuyến tính, hiệu ứng là một hàm biết trước của Rth/Rm và hiệu chỉnh được; ở phần mềm hiếm khi có mô hình đóng như vậy, nên người ta giảm overhead bằng sampling thay vì hiệu chỉnh.
- **Lưới điện (short circuit ratio).** Giống: một nguồn có trở kháng trong, tải càng lớn so với độ "cứng" của nguồn thì điện áp tại điểm nối càng sụt và càng nhạy. Khác: lưới có điều khiển chủ động (bù công suất phản kháng), divider thì không có gì bù.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| `Vout = Vin·R2/(R1+R2)` khi không tải; Rth = R1 // R2 | [chuẩn] | Giáo khoa mạch tuyến tính |
| `δVout/Vout ≈ (1−k)(δR2 − δR1)` | [chuẩn] | Đạo hàm riêng của công thức divider; kiểm lại bằng Monte Carlo |
| UT33D+: 2000 count, DCV ±(0.5% + 2) | [spec] | Bảng thông số dòng UT33+ của UNI-T; **kiểm lại trong manual đi kèm máy**, một số đại lý ghi khác cho thang 200 mV |
| Trở kháng vào DCV của UT33D+ ≈ 10 MΩ | [ước lượng] | Không tìm thấy trong tài liệu chính hãng; review độc lập báo ~10–11 MΩ. Bước 7 đo nó → `[tự đo]` |
| Chân 5V của DevKit thấp hơn 5.00 V | [tự đo] | Phụ thuộc cổng USB, cáp, và việc board có diode bảo vệ trên đường 5V hay không |
| Tỉ lệ trượt ~21% của cặp 10k/1k | [ước lượng] | Dưới giả định dung sai phân bố đều trong ±5%; phân bố thật của nhà sản xuất thường hẹp hơn |
| Poggendorff 1841, phương pháp bù | [chuẩn] | Lịch sử đo lường điện; chi tiết năm có thể kiểm trong tài liệu lịch sử dụng cụ đo |

**Đã sửa so với bản gốc:**
- Mẫu `prediction.md` của bản gốc ghi sẵn các Vout đã tính → chuyển thành mẫu trống + công thức; số kỳ vọng vào khối 🔒 (quy chuẩn mục 3.1).
- "Sai lệch phải < 5%" áp cho cả ba cặp như nhau → giữ ngưỡng gốc, nhưng thêm bước 0 (đo R) và giải thích vì sao cặp 10k/1k có thể trượt hợp lệ, còn cặp 1k/10k lệch 3% đã là đáng ngờ. Lý do: độ nhạy với dung sai khác nhau gấp ~10 lần giữa các cặp.
- Thí nghiệm 1 MΩ: bản gốc nói "thấp hơn rõ rệt"; với Rm ≈ 10 MΩ mức sụt ~4–5%, ngang dung sai ±5%, nên không chứng minh được nếu chỉ nhìn Vout. Đã thêm bước 6 (kiểm KVL) và bước 7 (suy ngược Rm).
- "Divider là cách hạ 5V xuống 3.3V cho một chân tín hiệu" → giới hạn rõ: chỉ cho tín hiệu **chậm, một chiều, đi vào đầu vào trở kháng cao**; không dùng cho nguồn, không dùng cho I2C.

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** manual UT33D+ (UNI-T), bảng thông số DCV và Ω; JCGM 100:2008 *Evaluation of measurement data — Guide to the expression of uncertainty in measurement* (GUM), mục 4.3 (đánh giá loại B, phân bố chữ nhật).
- **Giải thích:** Horowitz & Hill, *The Art of Electronics* (3rd ed.), chương 1, phần voltage divider và Thevenin — dùng làm từ điển tra cứu, không đọc tuần tự.
- **Đào sâu (tùy chọn):** F1.1 và F6.6 trong `nen-tang/`; thử viết lại Monte Carlo với phân bố chuẩn σ = tol/3 rồi so với phân bố đều.
- **Tự kiểm tra:** (1) giải thích lại cho một backend engineer khác trong 5 câu vì sao "que đo chỉ đọc" là sai; (2) vẽ lại hình ở phần 2 từ trí nhớ, kèm công thức Rth; (3) hai câu dưới.
  1. Divider 10k/10k, Vin = 5 V, đọc bằng một đầu vào 100 kΩ. Vout sụt bao nhiêu phần trăm so với không tải?
  2. Vì sao tỉ số Vout/Vin đo bằng cùng một đồng hồ, cùng thang, lại chính xác hơn từng số đọc riêng lẻ?

<details><summary>Đáp án</summary>

1. Rth = 5 kΩ. Vout = Vth·100/(5 + 100) ≈ 0.952·Vth → sụt ~4.8% (xấp xỉ Rth/RL = 5%).
2. Phần sai số tỉ lệ (`a%` của số đọc, ví dụ hệ số gain của mạch đo hơi lệch) nhân cùng một hệ số vào cả Vin lẫn Vout, nên bị triệt tiêu khi chia. Phần còn lại không triệt tiêu: sai số ±digit và sai số nếu hai số đọc ở hai thang khác nhau.

</details>

---

## Bài 10 — LED và điện trở: tại sao, bằng số (4h)

> **Vị trí:** Bài 9 (divider) → **Bài 10** → Bài 11 (datasheet) · **Cần trước:** Bài 1 (hiểu nhầm 2: LED cháy vì dòng), Bài 5 (đo dòng: cắt mạch, nối tiếp), Bài 9 (dụng cụ đo là một phần của mạch), F1.1, F6.1 (mô hình có miền hiệu lực) · **Sau bài này bạn quyết định được:** chọn điện trở hạn dòng cho một linh kiện phi tuyến ở một điện áp nguồn cho trước, và nhận ra khi nào "khoảng dư điện áp" quá nhỏ để điện trở còn giữ được dòng ổn định (ví dụ LED xanh dương chạy thẳng từ 3.3 V).

### 1. Câu chuyện — ai đã khổ vì chuyện này

Đèn hồ quang thế kỷ 19 có một tính chất khó chịu: dòng càng lớn thì hồ quang càng nóng, càng dẫn điện tốt, dòng càng lớn nữa. Nối thẳng vào nguồn là tự phá. Người ta phải mắc nối tiếp một **ballast** (điện trở hoặc cuộn cảm) để giữ dòng. Đèn huỳnh quang trong nhà bạn có chấn lưu cũng vì đúng lý do đó `[chuẩn]`. Bài học chung: **có những tải không tự giới hạn dòng, và nguồn điện áp không giới hạn dòng cho chúng.**

Diode bán dẫn, trong đó có LED, thuộc loại đó theo một cách khác. Shockley (1949) mô tả dòng qua tiếp giáp p-n tăng **theo hàm mũ** của điện áp `[chuẩn]`. LED đỏ nhìn thấy được đầu tiên (Holonyak, GE, 1962) kế thừa đặc tính đó `[chuẩn]`. Hệ quả thực tế: tăng điện áp trên LED thêm một chút xíu thì dòng tăng gấp nhiều lần. Không ai "đặt" dòng cho LED bằng cách đặt điện áp; người ta đặt dòng bằng một thứ tuyến tính đứng trước nó. Thứ đó là điện trở 330 Ω trong bài này.

### 2. Mô hình tư duy

```
  5V ──[R = 330 Ω]──┬──|>|── GND        KVL:  Vs = I·R + V_LED(I)
                    │  LED
                 V_LED(I) ≈ n·VT·ln(I/Is) + I·Rs     (hàm mũ ngược + điện trở nối tiếp nhỏ)

  I (mA)
   25 ┤                         ╱ đường cong LED (dốc đứng)
   20 ┤                        ╱
   15 ┤ ╲  đường tải: I = (Vs − V)/R
   10 ┤    ╲  ─ ─ ─ ─ ─ ─ ─ ─ ● ← điểm làm việc: giao của hai đường
    5 ┤        ╲            ╱│   ╲
    0 ┼─────────────────────┴──────────╲──── V
      0          1.0       V_f        Vs
```

1. LED không có "điện trở". Nó có một **đường cong I–V** gần như dựng đứng sau một ngưỡng; V_f trên datasheet chỉ là **một điểm** trên đường cong đó, kèm điều kiện (thường I_F = 20 mA, 25 °C).
2. Điểm làm việc là nghiệm của KVL: giao giữa đường cong LED và **đường tải** thẳng của điện trở. Không có R, đường tải dựng đứng tại Vs và giao điểm nằm ở dòng phá hủy.
3. Vì đường cong LED dốc, V_LED gần như không đổi khi dòng thay đổi trong một dải rộng. Nhờ vậy, dòng do **R và khoảng dư điện áp `Vs − V_f`** quyết định: `I ≈ (Vs − V_f)/R`.
4. Độ nhạy: nếu V_f lệch một lượng ΔV_f (khác lô, nhiệt độ), dòng lệch tương đối `ΔI/I ≈ −ΔV_f/(Vs − V_f)`. Khoảng dư càng nhỏ, R càng mất khả năng giữ dòng. Đây là con số quyết định thiết kế, không phải V_f.
5. Mô phỏng đồ chơi dưới đây vẽ cả hai đường và tính điểm làm việc. Tham số của nó là **đồ chơi** (chọn để V_f = 2.00 V tại 20 mA), không phải của LED bạn cầm.

```python
# [đã chạy] LED = diode: điểm làm việc là giao của đường cong I-V và "đường tải" của điện trở
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

VT = 0.02585          # điện áp nhiệt kT/q ở ~27 °C
N_IDEAL = 2.0         # hệ số lý tưởng — tham số đồ chơi, KHÔNG phải của LED bạn
RS = 10.0             # điện trở nối tiếp nội của LED (Ω) — đồ chơi
# Chọn Is sao cho V_f = 2.00 V tại 20 mA (kiểu "typ" trên datasheet LED đỏ 5 mm)
IS = 0.020 / np.exp((2.00 - 0.020 * RS) / (N_IDEAL * VT))

def v_led(i):
    """Điện áp trên LED khi dòng i chạy qua (mô hình Shockley + Rs)."""
    return N_IDEAL * VT * np.log(i / IS + 1) + i * RS

def operating_point(vs, r):
    """Giải (vs - V_led(I)) / r = I, tức KVL cho vòng nguồn-điện trở-LED."""
    return brentq(lambda i: vs - r * i - v_led(i), 1e-9, vs / r)

for vs in (5.0, 3.3):
    for r in (330.0, 150.0):
        i = operating_point(vs, r)
        # độ nhạy: V_f lệch +0.1 V (con LED khác lô) thì dòng đổi bao nhiêu %
        i2 = brentq(lambda x: vs - r * x - (v_led(x) + 0.1), 1e-9, vs / r)
        print(f"Vs={vs:.1f} V R={r:.0f} Ω -> I={i*1e3:5.2f} mA, Vf={v_led(i):.3f} V, "
              f"Vf+0.1V => I đổi {100*(i2-i)/i:+.1f}%")

i = np.linspace(1e-5, 0.03, 400)
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(v_led(i), i * 1e3, label="LED (đồ chơi)")
for vs, r in ((5.0, 330.0), (3.3, 330.0)):
    v = np.linspace(0, vs, 50)
    ax.plot(v, (vs - v) / r * 1e3, "--", label=f"đường tải {vs} V / {r:.0f} Ω")
ax.set_xlabel("V trên LED (V)"); ax.set_ylabel("I (mA)"); ax.set_ylim(0, 25); ax.legend()
fig.tight_layout(); plt.show()
```

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Rate limiter đặt trước một service không có backpressure | Điện trở trước LED | Rate limiter là **trần cứng**: vượt thì từ chối. Điện trở là **giới hạn mềm**: dòng tỉ lệ với `Vs − V_f`, nguồn tăng thì dòng tăng theo. Trần cứng thật là driver dòng không đổi (constant-current) | Tưởng "có điện trở là an toàn ở mọi nguồn" → đổi sang nguồn 12 V với cùng 330 Ω là quá dòng |
| `const V_F = 2.0` trong config | V_f thật | Hằng số trong code là sự thật; V_f là **một hàm** `f(I, T, từng con)`. Gần với "latency của service" — số đó chỉ có nghĩa kèm tải và percentile | Dùng V_f datasheet như hằng số → dự đoán lệch vài phần trăm và tưởng đồng hồ sai |
| Proxy inline đo throughput | Đồng hồ ở chế độ mA chèn nối tiếp | Proxy thêm độ trễ nhưng ít đổi throughput khi chưa bão hòa. Ampe kế chèn một **điện trở shunt** vào vòng: nó làm dòng giảm trực tiếp (burden voltage), tất định | Coi số của ampe kế là ground truth |
| Đối soát hai nguồn số liệu (billing vs metrics) | So `V_R/R` với dòng đo trực tiếp | Hai đường ở đây **dùng chung một đồng hồ** và cùng phụ thuộc R thật, nên không độc lập hoàn toàn: khớp nhau là điều kiện cần, chưa phải bằng chứng đúng | Thấy khớp → kết luận "đúng" trong khi cả hai cùng lệch theo một sai số chung |

**Chấm mô hình:**

- *"LED là một điện trở, R_LED = V/I."* — **SAI.** Phản ví dụ: tăng gấp đôi điện áp trên một điện trở thì dòng gấp đôi; trên LED, đi từ ~1.5 V lên ~2.2 V làm dòng đi từ gần như 0 lên hàng chục mA. Tỉ số V/I tại mỗi điểm khác nhau hoàn toàn, nên "điện trở của LED" không phải một tham số.
- *"V_f là một thông số cố định của LED, datasheet ghi 2.0 V thì nó là 2.0 V."* — **SAI.** V_f là một điểm trên đường cong, kèm điều kiện đo. Phản ví dụ: cùng một con LED đo ở 1 mA và ở 20 mA cho hai V_f khác nhau thấy được trên đồng hồ của bạn (bước 6). Hơn nữa datasheet thường ghi cả *typ* và *max* cho V_f — hai con cùng mã có thể lệch nhau cả trăm mV (Bài 11 nói về "typ không phải cam kết").
- *"Đo dòng trực tiếp là đúng nhất; tính V_R/R chỉ là ước lượng."* — **ĐÚNG MỘT PHẦN.** Cả hai đều là ước lượng với sai số hệ thống khác nhau: đường V_R/R mang dung sai của R (đo R ở thang Ω để thu hẹp); đường ampe kế mang sai số thang DCA **và** làm thay đổi chính dòng nó đo (burden). Phản ví dụ: đổi thang 20 mA sang 200 mA (shunt khác), số đọc dòng đổi — dòng thật không đổi vì bạn đổi thang, mạch thì có.

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | LED, anode/cathode | Diode phát sáng; dòng chỉ chạy từ anode (+, chân dài) sang cathode (−, cạnh vát) | Linh kiện không cực |
| 🟢 | V_f (forward voltage) | Điện áp trên LED khi dẫn, **tại một dòng và nhiệt độ cho trước** | Hằng số |
| 🟢 | Đường cong I–V | Quan hệ dòng–áp của linh kiện; với diode là gần hàm mũ | Đường thẳng (Ohm) |
| 🟡 | Điểm làm việc / đường tải | Nghiệm chung của linh kiện phi tuyến và phần tuyến tính của mạch | Thứ chỉ dân analog cần |
| 🟢 | Điện trở hạn dòng | Điện trở nối tiếp biến khoảng dư `Vs − V_f` thành dòng xác định | Thứ "làm LED tối đi" |
| 🟢 | Burden voltage | Sụt áp trên shunt bên trong đồng hồ khi đo dòng | Không tồn tại |
| 🟡 | KVL (Kirchhoff điện áp) | Tổng điện áp quanh một vòng kín bằng 0 | Chỉ dùng trong sách |
| 🟢 | Power rating | Công suất tối đa linh kiện tỏa được (điện trở cắm board: 1/4 W) | Đúng Ω là đủ |
| 🟡 | Hệ số nhiệt của V_f | V_f giảm khi LED nóng lên, cỡ vài mV/°C | Không đổi theo nhiệt |
| 🟡 | Constant-current driver | Mạch giữ dòng cố định bất kể nguồn; cách chiếu sáng thật sự dùng | Điện trở xịn |
| 🔴 | Phương trình Shockley | Mô hình hàm mũ của tiếp giáp p-n; chỉ cần biết dạng `exp(V/(n·VT))` | — |

### 5. Dự đoán

**Tham số cần tra / đo:**

| Tham số | Lấy ở đâu |
|---|---|
| V_f của LED đỏ | LED kit thường không có datasheet. Dùng datasheet một LED đỏ 5 mm của hãng thật (Kingbright, Vishay…), bảng *Electrical / Optical Characteristics*, dòng V_F: ghi **cả typ và max, và điều kiện I_F** |
| Dòng liên tục tối đa của LED | Cùng datasheet, bảng *Absolute Maximum Ratings*, dòng I_F (continuous) |
| Vs | Đo chân 5V như Bài 9 |
| R thật | Đo bằng thang Ω trước khi cắm |
| Sai số và các thang DCA của đồng hồ, cầu chì thang mA | Manual UT33D+, bảng DC Current |
| Burden voltage / điện trở shunt | Manual nếu có ghi; nếu không, gắn `[tự đo]` (bước 5) |

**Công thức/phương pháp:**
- `R_cần = (Vs − V_f)/I_muốn`, chọn giá trị chuẩn E12 gần nhất **phía lớn hơn** (lệch về phía dòng nhỏ an toàn hơn).
- Với R chuẩn đã chọn: `I = (Vs − V_f)/R`, `V_R = I·R`, `P_R = V_R·I`; so P_R với 1/4 W.
- Dự đoán **chiều và độ lớn** V_f thật ở dòng của bạn so với V_f datasheet (đo ở dòng khác): lớn hơn hay nhỏ hơn, cỡ bao nhiêu mV? Dùng mô hình `V ≈ n·VT·ln(I) + I·Rs`: đổi dòng từ I₁ sang I₂ thì V_f đổi `n·VT·ln(I₂/I₁) + Rs·(I₂ − I₁)`. Tham số n, Rs bạn không biết — hãy đoán một khoảng và ghi lý do.
- Dải chấp nhận cho phép kiểm chéo `V_R/R` vs `I_đo`: cộng sai số của R đo, của thang DCV và thang DCA.

**Mẫu `lab/02-led-current/prediction.md`:**

```markdown
# Dự đoán — LED + điện trở
LED: đỏ 5 mm (kit). Datasheet tham chiếu: <hãng, mã>, V_F typ __ V / max __ V tại I_F = __ mA
Vs (đo): __ V · I muốn: 10 mA
R cần = (__ − __) / 0.010 = __ Ω → chọn chuẩn: __ Ω (đo thật: __ Ω)

Với R chuẩn:
  I dự đoán     = __ mA
  V trên R      = __ V
  V trên LED    = __ V   (V_f thật ở dòng này lớn hơn / nhỏ hơn datasheet khoảng __ mV vì: __)
  P trên R      = __ mW  (so với 250 mW: __)

Sai số đồng hồ: DCV ±(__% + __), DCA thang __ mA ±(__% + __)
Kiểm chéo V_R/R vs I đo: chấp nhận nếu lệch < __ % (cách tính: __)
KVL: V_R + V_LED vs Vs: chấp nhận nếu lệch < __ %
```

`git commit -m "lab02: prediction"`.

### 6. Làm

**Bước 1 — dự đoán, commit** (phần 5).

**Bước 2 — dựng.** 5V → điện trở 330 Ω → chân dài của LED (anode, +) → chân ngắn (cathode, −) → GND. Nếu chân đã bị cắt bằng nhau, tìm cạnh vát phẳng trên vành nhựa: cạnh đó là cathode (−).

**Bước 3 — đo ba thứ:**
1. Điện áp trên điện trở (hai đầu điện trở). Ghi thang và sai số.
2. Điện áp trên LED (hai chân LED). Đo luôn Vs ngay lúc đó.
3. Dòng: **cắt mạch** (rút đầu GND của LED ra), chuyển que đỏ sang lỗ mA và núm sang thang `20 mA` DC, nối đồng hồ **nối tiếp** vào chỗ cắt. Xong thì **trả que đỏ về lỗ VΩ ngay** — để que ở lỗ mA rồi đi đo áp là chập nguồn qua shunt (Bài 5).

**Bước 4 — kiểm tra chéo.** Lấy V trên điện trở chia cho R **đo được** (không phải 330 danh định). So với dòng đo trực tiếp. Đây là câu hỏi số 2 trong "Ba câu hỏi để tự biết mình đo đúng" ở phần đầu Khóa 1. Kèm **tổng kiểm KVL:** `V_R + V_LED` so với `Vs` — tổng điện áp rơi trên một vòng kín bằng điện áp cấp. Không khớp thì một trong ba số đo sai, hoặc Vs đã đổi giữa các lần đo.

**Bước 5 — nhìn thấy burden (mới).** Đo dòng ở thang `20 mA`, rồi ở thang `200 mA`. Hai thang dùng shunt khác nhau. Ghi cả hai số kèm sai số từng thang. Câu hỏi để trả lời trong `analysis.md`: chênh lệch giữa hai thang lớn hơn hay nhỏ hơn sai số đồng hồ? Nếu lớn hơn, đó là dấu vết của burden: đồng hồ đã làm thay đổi dòng nó đo `[tự đo]`.

**Bước 6 — vẽ đường cong của chính con LED của bạn (mới, 30 phút).** Thay R lần lượt bằng 1 kΩ, 330 Ω, 150 Ω (với 150 Ω, kiểm lại phần 5: dòng và công suất có còn trong định mức không trước khi cắm). Mỗi lần ghi V_LED và I (tính từ V_R/R đo). Ba điểm (I, V_f) là ba điểm trên đường cong thật. Vẽ chúng lên cùng hình với mô phỏng ở phần 2, xem mô hình đồ chơi lệch ở đâu.

**Bước 7 — câu giải thích bằng lời.** Viết vào `analysis.md`, bằng lời của bạn, vì sao V_f đo được không bằng V_f trên datasheet. Đây là **tiêu chí số 4 của Gate Khóa 1** (Bài 14).

**Tùy chọn:** kẹp LED giữa hai ngón tay 30 giây cho ấm lên, đo lại V_LED. Chiều thay đổi nói gì về hệ số nhiệt?

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

**Bảng của bản gốc** (Vs = 5.00 V, V_f giả định 2.0 V, R = 330 Ω):

| Đại lượng | Dự đoán | Chấp nhận được |
|---|---|---|
| R cần | 300 Ω → chọn 330 Ω | — |
| V trên điện trở | 3.00 V | 2.7 – 3.3 V |
| V trên LED (V_f thật) | 2.00 V | **1.8 – 2.1 V** cho LED đỏ |
| Dòng | 9.09 mA | **8 – 10 mA** |
| P trên điện trở | ~27 mW | ≪ 250 mW, an toàn |
| V_R/R vs dòng đo | khớp | lệch < 5% |
| V_R + V_LED vs Vs | bằng nhau | lệch < 2% |

**V_f thật gần như chắc chắn không đúng 2.00 V; thường 1.85–1.95 V ở ~9 mA** `[ước lượng]`. Lý do: datasheet ghi V_f ở 20 mA, bạn chạy ~9 mA, và V_f giảm khi dòng giảm (cả phần `n·VT·ln` lẫn phần `I·Rs`). V_f thấp hơn làm dòng thật **cao hơn** 9.09 mA một chút.

**Mô phỏng đồ chơi** (V_f = 2.00 V tại 20 mA, n = 2, Rs = 10 Ω):

| Vs | R | I | V_f | V_f lệch +0.1 V thì I đổi |
|---|---|---|---|---|
| 5.0 V | 330 Ω | 9.52 mA | 1.857 V | −3.0% |
| 5.0 V | 150 Ω | 20.00 mA | 2.000 V | −3.1% |
| 3.3 V | 330 Ω | 4.63 mA | 1.771 V | −6.1% |
| 3.3 V | 150 Ω | 9.61 mA | 1.858 V | −6.3% |

Đọc bảng: cùng một sai lệch V_f, ở 3.3 V dòng nhạy gấp đôi ở 5 V, vì khoảng dư `Vs − V_f` chỉ còn một nửa. Với LED xanh dương/trắng (V_f ~3 V) chạy thẳng từ 3.3 V, khoảng dư chỉ vài trăm mV: dòng gần như do lô LED quyết định, không do R.

**Bước 5 (burden):** nếu shunt thang 20 mA cỡ 10 Ω `[ước lượng — tra manual hoặc tự đo]`, nó thêm ~0.09 V vào vòng 3 V khoảng dư → dòng giảm ~3%. Thang 200 mA có shunt nhỏ hơn nên ít tải hơn, nhưng độ phân giải kém hơn (0.1 mA). Đánh đổi độ phân giải ↔ mức xâm lấn là đánh đổi của mọi dụng cụ đo.

**Gate (tiêu chí 4):** dòng **tính từ nguyên lý đầu** (dự đoán) vs dòng **đo** lệch < 10%, kèm câu giải thích V_f. Phép kiểm chéo V_R/R vs I đo (< 5%) là phép kiểm khác, chặt hơn, vì hai đường đo cùng một mạch.

**Bước 6:** ba điểm của bạn sẽ nằm trên một đường cong lõm (V_f tăng chậm dần theo dòng). Nếu mô hình đồ chơi lệch, thường lệch ở Rs và n — không sao, chính bạn vừa đo ra hai tham số đó cho con LED của mình (→ F6.4).

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| LED không sáng, không nóng | Cắm ngược chiều | Thang diode của đồng hồ: chiều thuận LED sáng mờ | Đảo LED |
| LED sáng rất mờ | Điện trở quá lớn (33 kΩ thay vì 330 Ω) | Đo R bằng thang Ω | Thay đúng con |
| LED sáng chói rồi tắt hẳn, có mùi khét | Quên điện trở → dòng phá hủy | — | LED đã chết. Đây là lý do mua nhiều LED |
| Dòng đo ra 0 khi chuyển sang mA | Que đỏ đúng lỗ nhưng dòng vượt thang, hoặc cầu chì thang mA đã đứt từ lần trước | Thông mạch qua cầu chì (manual chỉ cách), hoặc thử thang 10 A với lỗ 10 A | Thay cầu chì đúng loại ghi trong manual |
| Đồng hồ đo dòng làm mạch tắt hẳn | Chưa nối tiếp đúng — mạch vẫn hở; hoặc cầu chì đứt | Lần lại đường dòng bằng tay | Nối lại |
| V_R/R lệch dòng đo 3–8% | Dùng R danh định thay vì R đo; burden của shunt | Bước 4 với R đo; bước 5 | Ghi cả hai nguồn sai số vào `analysis.md` |
| `V_R + V_LED` lệch Vs > 2% | Vs đổi giữa các lần đo; que tiếp xúc kém | Đo ba số liền nhau, kẹp cá sấu | Đo lại liên tiếp |
| Điện trở ấm tay | Dòng lớn hơn dự kiến — R sai hoặc nguồn không phải 5 V | Đo Vs và R | Kiểm lại trước khi để mạch chạy lâu |

### 9. Câu hỏi ngược

1. **[Nếu…thì]** Nếu nuôi LED bằng chân GPIO 3.3 V của ESP32 thay vì chân 5V, giữ nguyên 330 Ω, ba thứ gì thay đổi: dòng, độ nhạy với V_f, và giới hạn nào của chính chân GPIO phải tra?
   <details><summary>Hướng nghĩ</summary>Khoảng dư giảm → dòng giảm và nhạy hơn (bảng trong phần 7). Chân GPIO không phải nguồn lý tưởng: nó có trở kháng ra và có giới hạn dòng (drive strength) ghi trong datasheet ESP32-S3. Đây là Bài 9 lần nữa: nguồn có Rth.</details>
2. **[Failure mode]** Hai LED đỏ mắc song song, dùng chung **một** điện trở 150 Ω. Chuyện gì xảy ra theo thời gian?
   <details><summary>Hướng nghĩ</summary>Hai con có V_f hơi khác nhau; đường cong dốc nên con có V_f thấp hơn ăn phần lớn dòng. Nó nóng lên, V_f của nó giảm thêm (hệ số nhiệt âm), nó ăn thêm dòng. Đây là phản hồi dương — tên chuẩn là current hogging/thermal runaway. Lời giải: mỗi LED một điện trở.</details>
3. **[Vì sao không]** Vì sao không bỏ điện trở và cấp cho LED một nguồn điện áp đặt đúng bằng V_f datasheet?
   <details><summary>Hướng nghĩ</summary>Tính độ nhạy của dòng theo điện áp ở đoạn dốc của đường cong hàm mũ: một sai số 50 mV của nguồn tương đương bao nhiêu lần dòng? Rồi cộng thêm hệ số nhiệt. Chính câu chuyện ballast ở phần 1.</details>
4. **[Quy mô]** Ở K5 bạn sẽ lưu dữ liệu từ hàng trăm cảm biến có quan hệ phi tuyến (như V_f(I, T)). Ở 100 robot, lưu "một hằng số hiệu chuẩn" hay "một đường cong hiệu chuẩn có version" cho mỗi cảm biến? Cái gì gãy trước nếu chọn hằng số?
   <details><summary>Hướng nghĩ</summary>Hằng số đúng ở một điểm làm việc, sai ở điểm khác. Hỏng sớm nhất ở các robot chạy xa điểm hiệu chuẩn (nóng hơn, dòng khác). Đường cong cần schema, version và `calibration_id` (→ F3.2, F3.8).</details>
5. **[Phản biện]** Bản gốc có hai ngưỡng: kiểm chéo < 5% trong bài, "tính vs đo" < 10% trong gate. Một người nói "chỉ cần một ngưỡng". Bạn bảo vệ hay bác bỏ?
   <details><summary>Hướng nghĩ</summary>Hai phép so sánh trả lời hai câu hỏi khác nhau: "mô hình nguyên lý đầu của tôi đúng đến đâu" (gồm sai số do giả định V_f) vs "hai phép đo của cùng một mạch có nhất quán không" (chỉ gồm sai số dụng cụ). Ngưỡng nên tỉ lệ với ngân sách sai số của từng câu hỏi.</details>
6. **[Liên ngành]** Trong dược lý, liều thuốc và đáp ứng có quan hệ phi tuyến (đường cong liều–đáp ứng) và khác nhau giữa từng bệnh nhân. Chỗ nào giống LED, chỗ nào khác?
   <details><summary>Hướng nghĩ</summary>Giống: tham số là một đường cong theo từng cá thể, "liều chuẩn" chỉ là một điểm. Khác: phương sai giữa người lớn hơn nhiều, và không đo được đường cong của từng người trước khi dùng — nên y học dùng ngưỡng an toàn rộng và theo dõi, tương tự "chọn R phía lớn hơn".</details>

### 10. Liên kết ra ngoài

- **Chấn lưu (ballast) trong chiếu sáng.** Giống: tải không tự giới hạn dòng cần một phần tử nối tiếp để giữ dòng. Khác: đèn huỳnh quang dùng cuộn cảm (ít tỏa nhiệt hơn điện trở trên lưới AC); LED công suất dùng driver dòng không đổi có hồi tiếp, không dùng điện trở, vì điện trở phí năng lượng tỉ lệ với khoảng dư.
- **Cost model của query planner.** PostgreSQL có các hằng số như `random_page_cost` — một con số danh định cho một quan hệ thật ra phụ thuộc phần cứng và tải. Giống: "hằng số" là một điểm trên đường cong, phải hiệu chỉnh theo máy. Khác: planner chỉ cần thứ tự tương đối đúng để chọn kế hoạch; mạch cần giá trị tuyệt đối đúng để không cháy.
- **Dược lý (liều–đáp ứng).** Xem câu hỏi 6.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| Dòng qua diode tăng gần hàm mũ theo điện áp | [chuẩn] | Shockley 1949 |
| V_f LED đỏ 5 mm ~1.8–2.2 V tại 20 mA | [spec] | Theo datasheet hãng; LED kit không rõ nguồn → [tự đo] |
| V_f ~1.85–1.95 V ở ~9 mA | [ước lượng] | Bản gốc; phụ thuộc lô LED. Bước 6 kiểm |
| Hệ số nhiệt V_f cỡ −1.5 đến −2 mV/°C | [ước lượng] | Giá trị điển hình của diode; tra datasheet LED cụ thể |
| UT33D+ DCA ±(1% + 2), thang 2000 µA/20 mA/200 mA/10 A, cầu chì mA 0.2 A | [spec] | Bảng thông số UT33+ và mô tả của đại lý; **kiểm trong manual của máy** |
| Shunt thang 20 mA cỡ 10 Ω | [ước lượng] | Không có số chính hãng; bước 5 cho bằng chứng gián tiếp |
| Mô hình đồ chơi n = 2, Rs = 10 Ω | [ước lượng] | Tham số chọn cho hợp lý, không phải số đo |

**Đã sửa so với bản gốc:**
- "Đó là tiêu chí PASS số 3 của Khóa 1" → câu giải thích V_f là **tiêu chí số 4** trong bảng Gate (Bài 14); số 3 là voltage divider.
- Số kỳ vọng V_f 1.85–1.95 V nằm ngoài khối niêm phong ở bản gốc → chuyển vào 🔒.
- Bản gốc không nhắc ampe kế làm thay đổi dòng nó đo → thêm burden voltage (bước 5), nối tiếp bài học của Bài 9.
- Làm rõ hai ngưỡng: < 5% (kiểm chéo hai phép đo) và < 10% (tính vs đo, tiêu chí gate) là hai phép so sánh khác nhau, giữ cả hai.
- Kiểm chéo dùng **R đo được** thay vì 330 Ω danh định, để không lẫn dung sai R vào sai số đo dòng.

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** datasheet một LED đỏ 5 mm của hãng thật (Kingbright hoặc Vishay), các bảng Absolute Maximum Ratings và Electrical/Optical Characteristics; W. Shockley, "The Theory of p-n Junctions in Semiconductors and p-n Junction Transistors", *Bell System Technical Journal*, 1949 (chỉ để biết nguồn của dạng hàm mũ).
- **Giải thích:** Horowitz & Hill, *The Art of Electronics*, chương 1 (diode) — tra phần đặc tuyến diode và điện trở hạn dòng.
- **Đào sâu (tùy chọn):** EEVblog Fundamentals, tập về multimeter burden voltage (Dave Jones).
- **Tự kiểm tra:** (1) giải thích lại cho một backend engineer khác trong 5 câu vì sao LED cần điện trở mà không nói "để hạn dòng" như một khẩu hiệu; (2) vẽ lại đường tải và đường cong LED từ trí nhớ; (3) hai câu dưới.
  1. Nguồn 3.3 V, LED đỏ V_f ≈ 1.9 V, muốn ~5 mA. R bao nhiêu, chọn giá trị chuẩn nào?
  2. V_f lệch 0.1 V. Ở nguồn 5 V và nguồn 3.3 V, dòng lệch xấp xỉ bao nhiêu phần trăm? (dùng `ΔI/I ≈ ΔV_f/(Vs − V_f)`)

<details><summary>Đáp án</summary>

1. (3.3 − 1.9)/0.005 = 280 Ω → chọn 330 Ω (phía lớn hơn), dòng ≈ 4.2 mA; hoặc 270 Ω nếu chấp nhận ≈ 5.2 mA.
2. 5 V: 0.1/3.1 ≈ 3%. 3.3 V: 0.1/1.4 ≈ 7%. Khoảng dư nhỏ hơn thì R giữ dòng kém hơn.

</details>

---

## Bài 11 — Đọc trọn một datasheet (5h)

> **Vị trí:** Bài 10 (LED) → **Bài 11** → Bài 12 (I2C + ACK, dùng địa chỉ và register map bạn rút ra ở đây) · **Cần trước:** Bài 3 (bus, clock), Bài 9–10 (dung sai, "danh định ≠ thật"), F2.1 (lướt: test và spec đều là phép đo có sai), F3.7 (lướt: validate theo vật lý) · **Sau bài này bạn quyết định được:** một linh kiện có được phép nối vào hệ của bạn không (điện áp, giao tiếp, địa chỉ, ngân sách dòng), thiết kế theo con số nào (max, không phải typ), và con chip trả lời trên bus có đúng là con bạn nghĩ không.

### 1. Câu chuyện — ai đã khổ vì chuyện này

Ariane 5, chuyến bay 501 (1996): hệ dẫn đường quán tính (SRI) được dùng lại từ Ariane 4, nơi nó đã chạy tốt. Phần mềm chuyển một giá trị liên quan đến vận tốc ngang từ số thực 64 bit sang số nguyên 16 bit; với quỹ đạo của Ariane 4, giá trị đó không bao giờ vượt phạm vi, nên phép chuyển không được bảo vệ. Ariane 5 bay nhanh hơn, giá trị tràn, cả hai SRI dừng, tên lửa tự hủy khoảng 40 giây sau khi cất cánh `[chuẩn — báo cáo của ủy ban điều tra ESA/CNES, 1996]`. Thành phần không hỏng. Nó bị dùng **ngoài điều kiện hoạt động mà nó đã được kiểm chứng**, và không ai đọc lại các điều kiện đó khi đổi hệ.

Datasheet là bản ghi những điều kiện đó cho một con chip. Tutorial nói bạn *gõ gì*; datasheet nói con chip *làm gì, trong điều kiện nào, với bảo đảm nào*. Nguyên tắc số 3 của cả lộ trình: datasheet > tutorial (`00-lo-trinh-tong.md`). Bài này đọc trọn datasheet BME280 của Bosch — cảm biến bạn cắm ở Bài 12 — và tập một kỹ năng mà nghề backend gần như không dạy: đọc một tài liệu mà **mỗi con số đều đi kèm điều kiện**.

### 2. Mô hình tư duy

**Ba tầng con số trên cùng một trục** (ký hiệu, không phải số của BME280 — bạn tự điền ở phần 5):

```
 điện áp nguồn →
 0 V ──────[V_rec_min ═══════ vùng thiết kế ═══════ V_rec_max]─────── ░░░░░░░ V_absmax ✕✕✕✕✕
          │◄─ Recommended Operating Conditions: chip HOẠT ĐỘNG ĐÚNG SPEC ─►│
                                                                 │◄ không hỏng, nhưng ►│◄ có thể hỏng
                                                                 │  KHÔNG bảo đảm chạy │  vĩnh viễn,
                                                                 │  đúng (≈ UB của C)  │  ngay hoặc về sau
 Trong vùng thiết kế, mỗi thông số điện có ba cột:
   min ──────── typ ──────── max
   │            │             └─ bảo đảm trên toàn dải nhiệt độ / lô sản xuất: THIẾT KẾ THEO CỘT NÀY
   │            └─ giá trị điển hình ở phòng lab (thường 25 °C, VDD danh định): KHÔNG phải cam kết
   └─ bảo đảm phía dưới
```

**Thứ tự đọc** (không đọc từ trang 1):

```mermaid
flowchart LR
  A[Absolute Maximum Ratings<br/>cái gì làm chết chip] --> B[Recommended Operating /<br/>Electrical Characteristics<br/>min-typ-max + điều kiện]
  B --> C[Pin description<br/>chân nào làm gì, chân nào không được để hở]
  C --> D[Interface: I2C/SPI<br/>địa chỉ, cách chọn giao tiếp, timing]
  D --> E[Register map<br/>API của chip]
  E --> F[Phần còn lại, từ đầu tới cuối<br/>kể cả chú thích nhỏ]
  F --> G[Errata / revision history<br/>nếu có]
```

| Datasheet | Thứ tương ứng trong nghề của bạn | Khác ở đâu |
|---|---|---|
| Absolute Maximum Ratings | Giới hạn phá hủy (không có trong API docs) | Vượt không trả lỗi; có thể hỏng âm thầm |
| Recommended Operating Conditions | Môi trường được hỗ trợ (OS, runtime version) | Bảo đảm chỉ có nghĩa **trong** vùng này |
| Electrical Characteristics min/typ/max | SLO có điều kiện + dashboard p50 | Typ ≈ p50 ở phòng lab; max ≈ cam kết |
| Pin description | Danh sách endpoint + bắt buộc/tùy chọn | Một chân "để hở" có thể là hành vi không xác định |
| Register map | API reference | Có thứ tự, có tác dụng phụ, có đọc rách (phần 3) |
| Timing diagram | Sequence diagram + timeout | Đơn vị ns, và vi phạm không báo lỗi |
| Revision history / errata | Changelog / known issues | Thường nằm ở file riêng, ít người đọc |

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Đọc API docs: tìm endpoint, gọi thử | Đọc register map trước | API docs hiếm khi kèm điều kiện cho từng con số; datasheet thì **mọi con số có điều kiện** (nhiệt độ, VDD, tải bus) | Chỉ đọc register map → mạch chạy ở bàn, hỏng ở nhiệt độ hoặc nguồn khác |
| SLA vs p50 trên dashboard | max/min vs typ | SLA là lời hứa thương mại có phạt; "max" là giới hạn đặc tính hóa trên các lô và dải nhiệt, nhiều khi bảo đảm bằng thiết kế/đặc tính hóa chứ không đo từng con. "Typ" thậm chí không phải p50 của lô **bạn** mua | Tính ngân sách pin theo typ → robot hết pin sớm hơn tính toán ở ngày lạnh |
| Quota bị vượt → HTTP 429, thử lại sau | Vượt Absolute Max | Không có 429. Có thể chết ngay, có thể suy giảm ngầm rồi chết sau nhiều tuần. Vùng giữa rec max và abs max giống **undefined behavior của C**: có vẻ chạy, không ai bảo đảm | "Thử 5 V xem sao, vẫn chạy" → một hư hỏng tiềm ẩn mà bạn không có log nào ghi lại |
| Endpoint `/health` | Thanh ghi chip ID | Chip ID chỉ nói "một con chip *loại này* đang trả lời", không nói nó đo đúng. Gần với `/version` hơn `/health` | Health xanh trong khi cảm biến trả số rác (→ K5 Bài 16, validate theo vật lý) |
| `PUT /config` rồi đọc lại thấy đã đổi | Ghi thanh ghi cấu hình | Có thanh ghi chỉ có hiệu lực sau khi ghi **một thanh ghi khác**; có dữ liệu nhiều byte phải đọc trong **một lần** để không bị lẫn hai lần đo; có bit "reserved" phải giữ nguyên khi ghi (read-modify-write) | Cấu hình "đã ghi" mà không có tác dụng; số đo ghép từ hai thời điểm khác nhau |

**Chấm mô hình:**

- *"Register map là API của chip."* (bản gốc) — **ĐÚNG MỘT PHẦN.** Đúng ở cấu trúc: địa chỉ ↔ endpoint, đọc/ghi ↔ GET/PUT, chip ID ↔ endpoint định danh. Gãy ở ngữ nghĩa: thanh ghi trạng thái **tự đổi** mà không ai ghi (một GET đổi kết quả không cần PUT nào là chuyện bình thường); có thanh ghi chỉ nhận một giá trị "mật khẩu" và đọc lại luôn ra 0; không có version, không có xác thực, không có mã lỗi. Phản ví dụ cụ thể nằm trong datasheet BME280 — việc của bạn ở bước 5 là tìm ra hai chỗ register map BME280 có ngữ nghĩa "transaction/commit" và "snapshot".
- *"Typ là con số nhà sản xuất cam kết."* — **SAI.** Phản ví dụ ngay trong datasheet BME280: phần quy ước đầu tài liệu ghi rằng giá trị typ của dòng tiêu thụ được xác định ở 25 °C, còn min/max xác định bằng các lô góc (corner lots) trên toàn dải nhiệt độ `[spec — BME280 datasheet, phần đầu mục 1]`. Typ là một mẫu ở phòng lab.
- *"Absolute maximum là mức tối đa chip chạy được."* — **SAI.** Abs max là ngưỡng **không được vượt kể cả trong chốc lát**; chip không được bảo đảm *chạy đúng* ở bất kỳ đâu ngoài Recommended Operating Conditions. Phản ví dụ: một chip có thể chịu được điện áp gần abs max mà không hỏng nhưng ADC của nó đã ra số sai.
- *"Module ghi '5V tolerant' thì chip chịu 5V."* — **SAI.** Module có thể có LDO hạ áp và mạch dịch mức; chip trên đó vẫn là chip điện áp thấp. Đọc **hai** tài liệu: datasheet chip và sơ đồ/ mô tả module (bước 6).

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | Datasheet | Tài liệu đặc tả của nhà sản xuất chip: giới hạn, đặc tính có điều kiện, giao tiếp, thanh ghi | Trang bán hàng của module |
| 🟢 | Absolute Maximum Ratings | Ngưỡng mà vượt qua thì không còn bảo đảm gì, có thể hỏng vĩnh viễn | Dải hoạt động |
| 🟢 | Recommended Operating Conditions | Dải điện áp/nhiệt độ mà mọi thông số khác trong datasheet có hiệu lực | Gợi ý cho có |
| 🟢 | min / typ / max | Bảo đảm dưới / giá trị điển hình ở lab / bảo đảm trên, luôn kèm điều kiện | typ = cam kết |
| 🟢 | Pin description | Chức năng từng chân, chân nào phải nối cố định | Chỉ để đấu dây |
| 🟢 | Register map | Bảng địa chỉ thanh ghi, ý nghĩa từng bit, giá trị sau reset | REST API |
| 🟢 | Chip ID / WHO_AM_I | Thanh ghi chỉ đọc trả về một hằng số định danh loại chip | Health check đầy đủ |
| 🟢 | Bitfield | Một nhóm bit trong một thanh ghi mang một tham số riêng | Cả byte là một giá trị |
| 🟡 | Reset value / reserved bit | Giá trị thanh ghi sau khi bật nguồn / bit không được thay đổi | Bỏ qua được |
| 🟡 | Burst read | Đọc nhiều thanh ghi liên tiếp trong một giao dịch | Chỉ để tiết kiệm thời gian |
| 🟢 | Timing diagram | Hình các tín hiệu theo thời gian với t_setup, t_hold… | Hình minh họa |
| 🟡 | VDD vs VDDIO | Nguồn lõi vs nguồn cho chân giao tiếp, có thể khác nhau | Một nguồn duy nhất |
| 🟡 | Errata / revision history | Lỗi đã biết của chip / thay đổi giữa các bản tài liệu | Không tồn tại |
| 🟡 | Compensation / trimming parameters | Hệ số hiệu chuẩn riêng từng con, lưu trong chip, để đổi số thô ra đơn vị vật lý | Thư viện tự lo, không cần biết (→ K5 Bài 4) |
| 🔴 | Package, footprint, reflow profile | Kích thước vỏ, mẫu hàn trên PCB, nhiệt độ hàn | — (bạn dùng module) |
| 🔴 | ESD rating (HBM/CDM) | Mức phóng tĩnh điện chịu được | — |

### 5. Dự đoán

Bài này không có đồng hồ đo, nhưng vẫn có dự đoán: bạn đo **trực giác của chính mình về một con chip** trước khi đọc, rồi so sau khi đọc. Đó là cách hiệu chuẩn trực giác (→ F1.7).

**Tài liệu cần lấy:** PDF datasheet BME280 **của Bosch Sensortec** (trang sản phẩm BME280 trên site Bosch Sensortec), không phải trang bán module. Ghi **số tài liệu và revision** ở trang bìa vào notes — các revision khác nhau đánh số mục/trang khác nhau. Lấy thêm ảnh hoặc mô tả của **đúng module bạn mua** (số chân, có LDO không).

**Mẫu `lab/03-datasheet/prediction.md`** (viết TRƯỚC khi mở PDF, chỉ dùng trực giác + những gì đã học ở Bài 1–10):

```markdown
# Dự đoán — trước khi đọc datasheet BME280
Datasheet: (chưa mở)

1. VDD hoạt động: từ __ V đến __ V. Cấp 5 V trực tiếp: hỏng / không sao / không chắc. Vì: __
2. Có bao nhiêu địa chỉ I2C có thể có: __. Đổi bằng cách: __
3. Dòng tiêu thụ khi ngủ: cỡ (chọn) 1 nA / 1 µA / 1 mA. Khi đang đo: cỡ __
4. Có cần tôi tự tính hệ số hiệu chuẩn không, hay chip trả thẳng °C/Pa/%RH? __
5. Số thanh ghi tôi phải biết để đọc được nhiệt độ: __
6. Thời gian tôi cần để đọc trọn: __ h. Số chỗ tôi đoán sẽ không hiểu: __
7. Module tôi mua có: LDO (có/không), điện trở pull-up I2C (có/không, giá trị __), chân SDO nối __
```

`git commit -m "lab03: prediction"`.

### 6. Làm

**Bước 1 — tải datasheet** (phần 5). Ghi số tài liệu + revision.

**Bước 2 — lượt 1 (khoảng 45 phút): đọc theo thứ tự ưu tiên** ở phần 2 (Abs Max → Electrical/Operating → Pins → Interface → Register map). Với mỗi con số bạn chép ra, chép kèm **điều kiện** của nó (nhiệt độ, VDD, ghi chú chân trang). Một con số không có điều kiện đi kèm thì chưa được tính là đã đọc.

**Bước 3 — lượt 2: đọc từ đầu tới cuối, không skim.** Chỗ nào không hiểu thì ghi lại vào `lab/03-datasheet/confusions.md` (số trang + câu hỏi), đừng bỏ qua. Cuối khóa nhìn lại danh sách này rất có ích. Phần công thức bù (compensation) được phép đọc lướt — K5 Bài 4 sẽ làm nó bằng tay.

**Bước 4 — viết tay ra giấy register map:** địa chỉ, tên, ý nghĩa từng bitfield, đọc hay ghi, giá trị reset. **Ít nhất 8 thanh ghi**, trong đó có thanh ghi chip ID, ít nhất một thanh ghi cấu hình, ít nhất một thanh ghi dữ liệu. Viết tay, không copy-paste: việc chép tay ép mắt bạn đi qua từng dòng. Chụp ảnh, commit vào `lab/03-datasheet/`.

**Bước 5 — săn ngữ nghĩa "không giống REST"** (mới). Trong datasheet có ít nhất hai chỗ mà một backend engineer gọi thẳng tên được: một chỗ giống *staging rồi commit* (ghi thanh ghi A chưa có tác dụng cho tới khi ghi thanh ghi B), một chỗ giống *snapshot read* (phải đọc nhiều byte trong một giao dịch để không lẫn hai lần đo). Tìm chúng, ghi số trang, viết một câu cho mỗi chỗ: nếu thư viện của bạn làm sai thì triệu chứng trên dữ liệu là gì? Thêm: tìm một **điều cấm liên quan đến thứ tự cấp nguồn** (gợi ý: đọc kỹ phần power-on).

**Bước 6 — đối chiếu module** (mới, 20 phút, cần đồng hồ). Module **không cấp nguồn**:
1. Đo điện trở giữa SDA và VCC của module, giữa SCL và VCC → module có pull-up không, giá trị bao nhiêu (Bài 12 cần số này).
2. Thông mạch chân SDO của chip (hoặc chân SDO trên module nếu có) với GND và với VCC → **dự đoán địa chỉ I2C** cho Bài 12.
3. Nhìn trên module có con chip 3 hoặc 5 chân nhỏ cạnh đầu VCC không (thường là LDO) → module là loại 3.3 V hay có hạ áp.
Ghi cả ba vào `analysis.md`; đây là dự đoán đầu vào cho Bài 12.

**Bước 7 — trả lời ba câu**, mỗi câu kèm số trang/bảng:
1. BME280 chạy ở điện áp nào? Cấp 5 V trực tiếp vào chip có sao không?
2. Địa chỉ I2C của nó là gì, và làm sao đổi được?
3. Đọc thanh ghi nào để biết chip còn sống, và giá trị đúng là gì? Nếu đọc ra một giá trị khác nhưng "gần giống", nghĩa là gì?

**Bước 8 — so với `prediction.md`.** Câu nào trực giác của bạn lệch nhiều nhất? Lệch theo hướng nào (đánh giá cao hay thấp)? Một dòng trong `analysis.md`.

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

**Tiêu chí của bản gốc (giữ nguyên):** register map viết tay đối chiếu đúng **≥ 90%** với datasheet; có ít nhất `0xD0` (chip ID, giá trị `0x60`), một thanh ghi cấu hình, một thanh ghi dữ liệu.

Số dưới đây kiểm theo **BST-BME280-DS001-12, revision 1.3 (05/2016)** `[spec]`; bản mới hơn có thể đánh số bảng khác.

| Câu | Đáp án | Ở đâu |
|---|---|---|
| 1. Điện áp | VDD 1.71–3.6 V, VDDIO 1.2–3.6 V (typ 1.8 V). Abs max mọi chân nguồn: −0.3 đến **4.25 V**; chân giao tiếp: −0.3 đến **VDDIO + 0.3 V**. 5 V trực tiếp **vượt abs max** → có thể hỏng. Tín hiệu I2C kéo lên 5 V khi VDDIO = 3.3 V cũng vượt (5 > 3.6) | Table 1, Table 5 |
| 2. Địa chỉ | 7 bit `111011x`: SDO nối GND → **0x76**, SDO nối VDDIO → **0x77** (trùng địa chỉ BMP280). SDO **không được để hở** (địa chỉ không xác định). CSB phải nối VDDIO để chọn I2C | Mục giao tiếp I2C (mục 6.2 ở rev 1.3) |
| 3. Còn sống | Đọc `0xD0` → **0x60**. Đọc ra **0x58** (hoặc 0x56/0x57) là **BMP280** — chip khác, không có cảm biến độ ẩm, rất hay bị bán nhầm dưới tên BME280 | Thanh ghi "id", Table 17 (BMP280 vs BME280) |

**Bước 5:**
- *Staging → commit:* thay đổi ở `ctrl_hum` (0xF2) chỉ có hiệu lực **sau khi ghi `ctrl_meas` (0xF4)**. Thư viện ghi độ ẩm rồi quên ghi lại ctrl_meas → cấu hình độ ẩm không đổi, không có lỗi nào.
- *Snapshot:* dữ liệu 0xF7–0xFE nên đọc bằng **một burst read**; chip có cơ chế **shadowing** giữ dữ liệu nhất quán tới khi giao dịch kết thúc (STOP trên I2C). Đọc từng byte bằng nhiều giao dịch → có thể ghép byte cao của lần đo này với byte thấp của lần đo sau (đọc rách — torn read). Triệu chứng: thỉnh thoảng có giá trị nhảy vọt rồi trở lại.
- *Reset:* ghi `0xB6` vào `0xE0` để soft reset; đọc lại luôn ra 0x00.
- *Thứ tự cấp nguồn:* **cấm giữ chân giao tiếp ở mức cao khi VDDIO tắt** — dòng qua diode bảo vệ ESD có thể làm hỏng chip vĩnh viễn. Nghĩa là: tắt nguồn cảm biến trong khi ESP32 vẫn cấp pull-up 3.3 V lên SDA/SCL là một cách giết chip từ từ.

**Dòng tiêu thụ** (để so với dự đoán câu 3): ngủ 0.1 µA typ / 0.3 µA max; trong lúc đo áp suất cỡ 714 µA (ghi chú: max ở −40 °C); trung bình ~3.6 µA ở 1 Hz đo cả ba đại lượng `[spec]`. Bốn bậc độ lớn giữa ngủ và đang đo — đó là lý do ngân sách năng lượng tính theo **chu kỳ hoạt động**, không theo một con số.

**Câu 4 dự đoán:** chip trả số thô; phải dùng **hệ số hiệu chuẩn riêng từng con** đọc từ vùng 0x88–0xA1 và 0xE1–0xF0 để đổi sang °C/Pa/%RH (→ K5 Bài 4).

**Lệch trực giác hay gặp ở người làm phần mềm:** đánh giá dòng ngủ quá cao (nghĩ cỡ mA), và không đoán được rằng có điều cấm về thứ tự cấp nguồn.

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Không tìm thấy register map | Bạn đang đọc trang bán hàng của module, không phải datasheet chip | Trang bìa có logo Bosch và số tài liệu BST-…? | Tải PDF từ Bosch Sensortec |
| Quá tải, không hiểu gì | Bình thường ở lần đầu | — | Lượt 2 chỉ nhắm 4 mục trong bảng phần 2, bỏ qua compensation formula |
| Module ghi 3.3 V nhưng bán kèm "5V tolerant" | Module có LDO/mạch dịch mức; chip vẫn là chip điện áp thấp | Bước 6.3 | Đọc kỹ mô tả module, tách bạch với chip |
| Số trang/số bảng của bạn khác hướng dẫn | Revision khác | Trang bìa, revision history | Ghi revision vào notes; đối chiếu theo tên mục |
| Module chỉ có 4 chân, không thấy SDO/CSB | Module đã nối cứng SDO và CSB | Bước 6.2 bằng thông mạch | Ghi địa chỉ suy ra; Bài 12 sẽ kiểm |
| Đo pull-up ra vô cùng | Module không có pull-up | Bước 6.1 | Bài 12 cần thêm 4.7 kΩ lên 3.3 V |
| Register map viết tay đúng < 90% | Chép thiếu bitfield, nhầm đọc/ghi | Đối chiếu từng dòng với bảng memory map | Chép lại những dòng sai, ghi lý do sai vào `confusions.md` |

### 9. Câu hỏi ngược

1. **[Nếu…thì]** Nếu trên cùng bus I2C có một module khác kéo pull-up lên 5 V, còn BME280 chạy VDDIO 3.3 V, thì vi phạm điều gì trong datasheet, và triệu chứng có xuất hiện ngay không?
   <details><summary>Hướng nghĩ</summary>Tìm abs max của **chân giao tiếp** (không phải chân nguồn), nó tính theo VDDIO. Dòng chạy qua diode bảo vệ vào nguồn 3.3 V. Có thể chạy được nhiều ngày — "chạy được" không phải bằng chứng an toàn. Lời giải: mạch dịch mức cho I2C (loại dùng MOSFET hai chiều).</details>
2. **[Quy mô]** 100 robot, module BME280 mua từ ba nhà bán khác nhau. Ở bước nào trong pipeline (nhận hàng, firmware boot, ingest dữ liệu) bạn phát hiện một con BMP280 trà trộn, và ghi nhận nó vào đâu?
   <details><summary>Hướng nghĩ</summary>Chip ID đọc lúc boot là kiểm rẻ nhất; ghi vào metadata `source_device_id`/loại chip của MCAP (`CONVENTIONS.md`). Kiểm theo vật lý ở tầng ingest (kênh độ ẩm luôn trống hoặc hằng) là lưới thứ hai. Hỏi thêm: firmware nên từ chối chạy hay chạy ở chế độ suy giảm và báo cáo?</details>
3. **[Failure mode]** Robot tắt nguồn cảm biến để tiết kiệm pin, nhưng ESP32 vẫn bật và chân I2C của nó vẫn kéo lên 3.3 V. Datasheet nói gì, và lỗi này trông thế nào sau ba tháng ngoài hiện trường?
   <details><summary>Hướng nghĩ</summary>Tìm điều cấm về thứ tự cấp nguồn ở bước 5. Hư hỏng tích lũy, không tái hiện được ở bàn, phân bố theo số chu kỳ bật/tắt chứ không theo thời gian chạy — loại lỗi mà soak test ngắn không bắt được (→ F7.6).</details>
4. **[Vì sao không]** Vì sao không dùng thư viện Adafruit/SparkFun và bỏ qua datasheet? Thư viện đã chạy được.
   <details><summary>Hướng nghĩ</summary>Thư viện chọn sẵn chế độ đo, oversampling, filter — tức là chọn sẵn đánh đổi nhiễu/độ trễ/năng lượng cho bạn. Khi dữ liệu có vấn đề, không biết các lựa chọn đó thì không phân biệt được lỗi cảm biến, lỗi cấu hình hay lỗi thư viện. Datasheet là thứ cho phép bạn **đánh giá** thư viện, không chỉ dùng nó.</details>
5. **[Liên ngành]** Đồng hồ tốc độ của máy bay có cung xanh, cung vàng, và vạch đỏ V_NE (never exceed). Ánh xạ chúng vào ba tầng con số của datasheet. Chỗ nào ánh xạ không khớp?
   <details><summary>Hướng nghĩ</summary>Cung xanh ≈ recommended; cung vàng (chỉ khi không khí êm) ≈ vùng giữa rec max và abs max; vạch đỏ ≈ abs max. Khác: phi công có đồng hồ hiển thị liên tục; con chip không có cảnh báo nào khi bạn đi vào cung vàng — bạn phải tự đo.</details>
6. **[Phản biện]** "Chép tay register map là phí thời gian khi có thể copy bảng từ PDF." Bảo vệ hoặc bác bỏ.
   <details><summary>Hướng nghĩ</summary>Mục tiêu không phải bản sao mà là buộc sự chú ý đi qua từng bitfield và từng ghi chú. Thử đo: sau khi chép tay, bạn trả lời được bao nhiêu câu ở bước 5 mà không mở lại PDF? Nếu bạn tìm được cách khác đạt cùng kết quả (ví dụ tự viết test decode từng bitfield), đó là phản biện hợp lệ.</details>

### 10. Liên kết ra ngoài

- **Hàng không: đường bao bay (flight envelope).** Giống: mọi thông số có điều kiện (độ cao, trọng tải, nhiệt độ), và có ba tầng bình thường/cẩn trọng/cấm. Khác: máy bay hiện đại có bảo vệ đường bao chủ động (fly-by-wire chặn lệnh vượt giới hạn); con chip không có cơ chế nào chặn bạn.
- **Hợp đồng và SLA.** Một SLA tốt có phần loại trừ (exclusions) và điều kiện đo; datasheet là SLA mà phần điều kiện dày hơn phần cam kết. Khác: SLA vi phạm thì có bồi thường, datasheet vi phạm thì chỉ có linh kiện hỏng và không ai chịu trách nhiệm ngoài bạn.
- **Semantic versioning và changelog.** Datasheet có revision history, chip có errata — giống changelog/known issues. Khác: không có semver; một revision datasheet có thể đổi một giới hạn mà không đổi tên chip, và con chip bạn cầm có thể là lô trước hoặc sau thay đổi đó.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| Các số BME280 trong 🔒 (điện áp, abs max, địa chỉ, chip ID, dòng, ctrl_hum, shadowing, power-on) | [spec] | Kiểm trực tiếp trên BST-BME280-DS001-12 rev 1.3 khi soạn bài; đối chiếu lại với bản bạn tải |
| Typ đo ở 25 °C, min/max từ corner lots trên toàn dải nhiệt | [spec] | Phần quy ước đầu mục 1 của datasheet BME280; các hãng khác có quy ước tương tự nhưng phải đọc từng tài liệu |
| Module BMP280 bị bán dưới tên BME280 | [ước lượng] | Hiện tượng phổ biến trên chợ module giá rẻ; Bài 12 kiểm bằng chip ID |
| Ariane 501 | [chuẩn] | Báo cáo ủy ban điều tra ESA/CNES (J. L. Lions, 1996) |
| Vùng giữa rec max và abs max "không hỏng nhưng không bảo đảm" | [chuẩn] | Quy ước chung của datasheet; một số hãng ghi rõ câu này ngay dưới bảng Abs Max |

**Đã sửa so với bản gốc:**
- Bản gốc vừa nói "không đọc tuần tự từ trang 1" vừa nói "đọc từ đầu tới cuối, không skim" → tách thành hai lượt: lượt 1 theo thứ tự ưu tiên, lượt 2 trọn tài liệu.
- Bảng gốc đặt "cấp 5 V vào chip 3.3 V là hỏng" dưới mục Electrical Characteristics → giới hạn phá hủy thuộc **Absolute Maximum Ratings**; Electrical Characteristics/Recommended Operating là vùng thiết kế. Tách ba tầng.
- "Vượt [abs max] là chết chip" → chính xác hơn: vượt thì không còn bảo đảm gì, có thể hỏng ngay hoặc suy giảm ngầm; và **giữa rec max và abs max** chip cũng không được bảo đảm hoạt động đúng.
- Đáp án ba câu hỏi và giá trị chip ID đưa vào 🔒.
- Thêm: phân biệt BMP280/BME280 qua chip ID, ngữ nghĩa ctrl_hum/burst read, điều cấm về thứ tự cấp nguồn, đối chiếu module bằng đồng hồ (dự đoán địa chỉ và pull-up cho Bài 12).

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** Bosch Sensortec, *BME280 — Combined humidity and pressure sensor, Datasheet* (BST-BME280-DS001/DS002, bản mới nhất trên trang Bosch Sensortec).
- **Giải thích:** EEVblog Fundamentals (Dave Jones), tập về cách đọc datasheet.
- **Đào sâu (tùy chọn):** mã nguồn *BME280_SensorAPI* của Bosch Sensortec trên GitHub — xem nhà sản xuất tự cài đặt burst read và compensation thế nào, đối chiếu với register map bạn chép tay.
- **Tự kiểm tra:** (1) giải thích lại cho một backend engineer khác trong 5 câu sự khác nhau giữa abs max, recommended, typ, max; (2) vẽ lại trục ba tầng ở phần 2 từ trí nhớ; (3) hai câu dưới.
  1. Bạn đọc thanh ghi chip ID của một module "BME280" và nhận 0x58. Kết luận gì, và dữ liệu nào trong dataset của bạn bị ảnh hưởng?
  2. Một bảng ghi dòng ngủ "typ 0.1 µA, max 0.3 µA". Ngân sách pin cho 3 năm của bạn dùng số nào, và vì sao?

<details><summary>Đáp án</summary>

1. Đó là BMP280, không phải BME280: không có cảm biến độ ẩm, một vài thanh ghi cấu hình có ý nghĩa khác (ví dụ thời gian standby). Mọi kênh độ ẩm từ thiết bị đó là rác hoặc trống; metadata loại chip phải ghi đúng để lọc.
2. Dùng max (0.3 µA), và kiểm điều kiện nhiệt độ của nó. Typ là số ở 25 °C; robot không sống ở 25 °C suốt 3 năm, và ngân sách phải đúng cho cả những con xấu nhất trong lô.

</details>

---
