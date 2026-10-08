# Khóa 1 — Từ zero đến đo được · Tổng quan

**Cho:** backend engineer 8 năm, chưa từng cầm que đo nghiêm túc, đang học bật tắt mỏ hàn.
**Giờ:** 35h lõi (trần 55h) + 1–2h luyện hàn khuyến nghị. **Chi phí đợt 1:** ~2,3–2,9tr, hoặc ~3,0–4,4tr nếu mua luôn nguồn bàn `[ước lượng 10/2026]` (chi tiết ở Bài 4).
**Xong khóa này bạn làm được:** cắm que đo vào một mạch và biết số đó đúng hay sai **và sai tới ± bao nhiêu**; nhìn thấy dữ liệu chạy trên dây bằng logic analyzer và biết khi nào analyzer đang nói dối; đọc được một datasheet; và quan trọng nhất — biết khi nào mình đang tự lừa mình.

**Khóa này chạy song song với K2** (thuần phần mềm, làm ở tuần bận). Thứ tự lộ trình: K1 + K2 song song → K3 → K4 → K5 → K6, với K7 (khóa build robot) chạy thành đường ray song song từ sau K1 (xem `khoa-7/_KE-HOACH-K7.md`).

**Ngân sách toàn lộ trình — không giấu.** K1–K6 cộng lại **545h** (K1 35 · K2 80 · K3 90 · K4 70 · K5 150 · K6 120). Ngay với K7 gốc (340h), tổng đã là **885h**, vượt con số 650h mà lộ trình gốc ghi. K7 thiết kế lại thành khóa build cho người mới có lõi **561h** (C0–C12, chưa tính phần tùy chọn) → tổng **1.106h**, ở 6,5h/tuần là khoảng **170 tuần ≈ 3,3 năm**. Đường lõi tối thiểu của K7 mới (~340h: C0–C7 trọn, C10.1–C10.2, C11.1–C11.3) cho tổng **545 + 340 = 885h ≈ 2,6 năm** (`khoa-7/_KE-HOACH-K7.md` mục 3). Đây là quyết định của bạn, ghi vào `decisions.md`, không phải thứ để phát hiện ra ở năm thứ hai.

**K7 không chờ tới cuối.** Chặng **K7 C0** (xưởng, dụng cụ, an toàn: bàn làm việc, hàn dây, nguồn bàn giới hạn dòng, sổ build) mở được **ngay sau Phần B** của khóa này và chạy song song với phần còn lại của K1 và K2; C1 (hệ nguồn) cần K1 trọn (`_KE-HOACH-K7.md` mục 4).

---

## 1. Bản đồ khóa

```mermaid
flowchart TB
    subgraph A["Phần A — Nền (6h, không cần mua gì) · phan-a-nen.md"]
        B1["Bài 1<br/>V, I, R, P"] --> B2["Bài 2<br/>Mạch kín, GND,<br/>dây không lý tưởng"] --> B3["Bài 3<br/>Tín hiệu số, bus, clock"]
    end
    subgraph B["Phần B — Dụng cụ (5h) · phan-b-dung-cu.md"]
        B4["Bài 4<br/>Mua gì"] --> B5["Bài 5<br/>Multimeter"] --> B6["Bài 6<br/>Breadboard"] --> B7["Bài 7<br/>Logic analyzer"] --> B8["Bài 8<br/>Mỏ hàn"]
    end
    subgraph C["Phần C — Đo thật (14h) · phan-c-do-that.md"]
        B9["Bài 9<br/>Voltage divider"] --> B10["Bài 10<br/>LED + điện trở"] --> B11["Bài 11<br/>Datasheet BME280"]
    end
    subgraph D["Phần D — Dữ liệu trên dây (10h) · phan-d-du-lieu-tren-day.md"]
        B12["Bài 12<br/>I2C + ACK"] --> B13["Bài 13<br/>I2S"] --> B14["Bài 14<br/>Gate"]
    end
    A --> B --> C --> D
    F11(["F1.1 sai số dụng cụ"]) -.-> B5 & B7 & B9
    F17(["F1.7 báo cáo trung thực"]) -.-> B9 & B14
    F55(["F5.5 lấy mẫu, Nyquist"]) -.-> B3 & B7 & B12
    F41(["F4.1 đồng hồ vật lý, ppm"]) -.-> B3 & B13
    F57(["F5.7 nguồn, ground"]) -.-> B2
    B8 ==> K7C0["K7 C0.3<br/>hàn dây, bấm đầu nối"]
    B ==> K7(["K7 C0 mở được"])
    D ==> K3(["K3 mở khi K1 PASS"])
    K2(["K2 chạy song song<br/>tuần bận"]) -.- A
```

## 2. Bài → giờ → viên nang nền → quyết định

Giờ Phần C–D là phân bổ đề xuất từ tổng của bản gốc; con số chuẩn nằm ở đầu file phần đó.

| Bài | File | Giờ | Viên nang nền cần trước | Sau bài này bạn quyết định được |
|---|---|---|---|---|
| 1 Bốn đại lượng và một quy tắc | phan-a | 2 | — | Linh kiện có sống được trong mạch không (V·I·R·P), nguồn "3 A" có đẩy 3 A không |
| 2 Mạch kín, GND, dây là giả định | phan-a | 1.5 | F5.7 (đọc lướt) | Hai module có cần dây GND chung không; dây có còn "lý tưởng" ở dòng này không |
| 3 Tín hiệu số, bus, clock | phan-a | 2.5 | F5.5, F4.1, F7.1 (lướt) | Bus dựa vào cơ chế định thời nào và hỏng kiểu gì; "tần số tối đa" là giới hạn vật lý, không phải chính sách |
| 4 Mua gì *(rút gọn)* | phan-b | 0,5 | — | Danh sách đợt 1 đủ cho K1 và mở K7 C0 không; món nào mua 2 cái |
| 5 Multimeter | phan-b | 1,5 | F1.1 | Chức năng, thang, lỗ cắm nào cho một phép đo; số đọc đúng tới ± bao nhiêu |
| 6 Breadboard | phan-b | 0,5 | — | Mạch trên board có đúng sơ đồ không, trước khi cấp điện |
| 7 Logic analyzer và PulseView | phan-b | 1,5 | F5.5, F1.1 | Sample rate và số mẫu cho một capture; phép đo thời gian chính xác tới đâu |
| 8 Mỏ hàn | phan-b | 1 (+1–2 luyện) | — | Mối hàn ĐẠT hay làm lại, trước khi cấp điện |
| 9 Voltage divider | phan-c | 5 | F1.1, F1.7, F6.6 (lướt) | Chênh lệch dự đoán–đo có nằm trong sai số không; dụng cụ có đang kéo lệch mạch không |
| 10 LED và điện trở | phan-c | 5 | F1.1, F6.1 | Chọn điện trở cho LED; có tin V_f trên datasheet như hằng số không |
| 11 Đọc trọn một datasheet | phan-c | 4 | F2.1, F3.7 (lướt) | Đọc mục nào để quyết định cấp nguồn, nối chân, kiểm chip còn sống |
| 12 I2C và ACK | phan-d | 5 | F5.5, F2.1 | Pull-up nào cho tốc độ và độ dài dây; lỗi "không đọc được cảm biến" nằm ở tầng nào |
| 13 Nhìn thấy I2S | phan-d | 4 | F4.1, F5.5 | Analyzer 24 MHz kiểm được cấu hình I2S nào (`BCLK = fs × slot × kênh`); lệch LRCK là cấu hình (%) hay thạch anh (ppm) |
| 14 Gate Khóa 1 | phan-d / mục 4 dưới đây | 1 | F1.7 | PASS hay chưa — bằng repo, không bằng cảm giác |

**Tổng:** 6 + 5 + 14 + 10 = **35h**, cộng 1–2h luyện hàn (khuyến nghị, tính trước cho K7 C0.3).

## 3. Bốn câu hỏi để tự biết mình đo đúng

Bản gốc có ba câu. Thêm câu thứ tư, vì không có nó thì ba câu kia không trả lời được bằng số.

1. **Số này có nằm trong khoảng vật lý hợp lý không?** Rail 5 V không thể đo ra 12 V. Điện trở không âm. Dòng qua LED không thể là 3 A.
2. **Đo bằng cách khác có ra cùng số không?** Đo điện áp trên điện trở rồi tính `I = V/R`; so với đo dòng trực tiếp. Hai đường phải gặp nhau.
3. **Có khớp với tính toán từ nguyên lý đầu không?** Tính ra 9 mA, đo 9,3 mA: tốt. Đo 90 mA: có gì đó sai — tìm ra *cái gì* sai mới là bài học.
4. **Chênh lệch lớn hơn hay nhỏ hơn sai số của chính phép đo?** "Gặp nhau" ở câu 2 và "khớp" ở câu 3 nghĩa là chênh lệch **nhỏ hơn tổng sai số** của dụng cụ và linh kiện (→ F1.1). Không biết sai số thì không trả lời được câu 2–3.

Cả bốn "có" → số đúng. Một câu "không" → dừng, đừng đi tiếp.

**Quy tắc bất di bất dịch:** viết dự đoán bằng số vào `prediction.md`, **commit**, rồi mới cắm que đo hoặc mở khối 🔒. Thư mục `lab/00-*` là bài luyện của Phần A–B; `lab/01-*` … `lab/05-*` là năm lab của gate. Mọi thư mục lab đều qua CI check thứ tự commit (lộ trình tổng mục 0.5).

## 4. Gate Khóa 1

Kiểm được bởi người khác đọc repo của bạn. Giữ nguyên sáu tiêu chí gốc (cũng là PASS của M1 trong lộ trình tổng); chỗ sửa ghi ở cột cuối.

| # | Tiêu chí | Cách kiểm | Đã sửa gì so với gốc |
|---|---|---|---|
| 1 | Repo public có `hours.csv` ≥ 14 ngày ghi giờ và cấu trúc `/lab/` | Mở repo | — |
| 2 | **5** thư mục `lab/01-*`…`lab/05-*`, mỗi cái có `prediction.md` commit **trước** file số đo / `analysis.md` | `git log --diff-filter=A --format="%ci" -- lab/01-*/prediction.md` so với file đo; hoặc CI check | Đầu file gốc ghi "lab notebook **4** thí nghiệm" trong khi gate đòi 5 → thống nhất là **5**. Ghi chú trung thực: timestamp commit do bạn tự đặt được; lịch sử push công khai là bằng chứng bổ sung, không tuyệt đối |
| 3 | Voltage divider: 3 tỉ lệ, sai lệch **< 5%** sau khi hiệu chỉnh Vin | Bảng trong `analysis.md` | Ngưỡng giữ nguyên. Cách đọc: "hiệu chỉnh" gồm Vin đo **và** R đo — với điện trở ±5%, cặp 10k/1k lắp đúng vẫn có thể lệch >5% so với dự đoán danh định (dung sai bị khuếch đại), cặp 1k/10k thì 5% quá lỏng (Bài 9). Bảng phải có **cột sai số dụng cụ** và **R đo được**. Thí nghiệm phá 1 MΩ: hiệu ứng tải của đồng hồ ~10 MΩ **cùng bậc** với dung sai ±5% → so với R đo, kiểm tổng V_R1 + V_R2, hoặc thêm cặp 10 MΩ |
| 4 | LED: dòng tính vs đo sai lệch **< 10%**, kèm **giải thích bằng lời** vì sao V_f không phải hằng số | Đoạn văn trong `analysis.md` | Giữ 10% (như M1). Phép kiểm chéo nội bộ của Bài 10 (V_R/R vs dòng đo, < 5%) là kiểm tra chất lượng phép đo, không phải tiêu chí gate |
| 5 | File capture `.sr` của bus I2C thật, decode ra **ACK**, kèm ảnh chụp PulseView | File trong repo | Ghi chú: **NACK ở byte cuối của một lần đọc** là controller cố ý báo kết thúc, không phải lỗi (Bài 3, 12). Scanner chỉ dò địa chỉ; dải nhãn có `Data read: 60` chỉ xuất hiện với sketch đọc chip ID (Bài 12 bước 6) |
| 6 | Register map viết tay chụp ảnh, đúng ≥ 90%; đo được LRCK / BCK sai lệch **< 1%** | Ảnh + bảng số | LRCK đo một chu kỳ là đủ. **BCK phải đo qua ≥ 32 chu kỳ**: với độ phân giải 41,7 ns, đo một chu kỳ BCK không đạt < 1% (tự tính ở Bài 3 câu 3; bảng đủ ở Bài 13 phần 7). Sửa phương pháp đo, không đổi ngưỡng. Bảng ghi rõ đo qua bao nhiêu chu kỳ |
| + | *(bổ sung, không thay thế)* Mỗi `analysis.md` có mục "sai số của phép đo" | Đọc từng analysis | Lộ trình tổng mục 0.6 đã yêu cầu trong mẫu notebook; gate gốc không kiểm |

**Ngân sách:** 35h. **Trần:** 55h.
**FAIL → action (cam kết trước):** chạm 55h chưa PASS → không phải thiếu kiến thức mà sai cách học: theo một khóa có cấu trúc (EEVblog Fundamentals hoặc Ben Eater theo thứ tự), cấp thêm 15h, thử lại đúng một lần. Chạm 70h → dừng K1, dồn giờ sang K2, xem lại sau 3 tháng. **Hệ quả mới cần biết:** K7 C0 cần K1 Phần B, K7 C1 cần K1 trọn (`_KE-HOACH-K7.md` mục 4) — dừng K1 cũng là dừng đường ray K7.

## 5. Lịch

Bản gốc: "4 tuần ở nhịp 8–10h/tuần". Ngân sách thật của bạn là ~6–7h/tuần, chia với K2. Lịch dưới đây giả định ~6h/tuần cho K1 ở tuần thường.

| Tuần | Giờ | Làm | Xong thì có |
|---|---|---|---|
| 1 | 6 | Bài 1–3 (giấy, Python, Falstad, WaveDrom) · đặt mua đợt 1 · tạo repo, `hours.csv`, CI check thứ tự commit | Nền khái niệm, repo, mô phỏng chạy được |
| 2 | 6 | Bài 4 (nhận hàng, kiểm từng món) · Bài 5 · Bài 6 | Đo áp/điện trở/dòng an toàn có sai số; board và dây đã kiểm |
| 3 | 6 | Bài 7 (boot log UART) · Bài 8 + luyện hàn · hàn header BME280 nếu cần | Capture `.sr` đầu tiên; 20 mối hàn luyện có chấm điểm |
| 4 | 6 | Bài 9 (voltage divider) | Lab 01 |
| 5 | 6 | Bài 10 (LED) · Bài 11 (datasheet) | Lab 02, 03 |
| 6 | 6 | Bài 12 (I2C) · Bài 13 (I2S) | Lab 04, 05 |
| 7 | 1–2 | Bài 14 (gate) · dọn repo | **K1 PASS** |

≈ 37h trong 7 tuần. Có tuần crunch thì lịch giãn ra; điều đó bình thường, miễn là `hours.csv` phản ánh đúng.

## 6. Bẫy đã biết

| # | Bẫy | Ở bài | Cách tránh |
|---|---|---|---|
| 1 | Quên GND của logic analyzer — và capture **vẫn đúng** vì GND đi vòng qua laptop, tới lúc đổi nguồn thì thành rác | 2, 7 | GND kẹp đầu tiên, tháo cuối cùng; thí nghiệm phá ở Bài 7 |
| 2 | Que đỏ còn ở lỗ dòng từ lần đo trước, chạm vào nguồn | 5 | Đo dòng xong rút que về VΩmA **ngay** |
| 3 | 24 MHz × 1M mẫu cho tín hiệu chậm → thời lượng ghi quá ngắn, thấy đường thẳng | 7 | Sample rate theo chi tiết ngắn nhất, số mẫu theo thời lượng dài nhất |
| 4 | Dùng ngưỡng TTL (0,8 V / 2,0 V) cho ESP32-S3 (0,25 / 0,75·VDD) | 3 | Tra ngưỡng của chip cụ thể |
| 5 | Cáp USB chỉ sạc → "board chết" | 4 | Thử cáp truyền dữ liệu trước khi nghi board |
| 6 | Module "BME280" thật ra là BMP280 | 4, 11, 12 | Đọc chip ID: 0x60 vs 0x58 |
| 7 | Rail breadboard đứt giữa, nửa board không có nguồn | 6 | Kiểm thông mạch rail trước khi dùng |
| 8 | Tin chữ decoder in ra mà không kiểm cấu hình | 7, 12, 13 | Kiểm một tính chất vật lý độc lập (chu kỳ SCL, độ rộng bit) |
| 9 | Đo một chu kỳ BCK rồi kết luận "< 1%" | 3, 13 | Đo qua ≥ 32 chu kỳ |
| 10 | Hiệu ứng tải của đồng hồ ở 1 MΩ chìm trong sai số điện trở | 5, 9 | Đo từng điện trở trước, hoặc dùng 10 MΩ |
| 11 | Coi V_f, tần số danh định, ngưỡng là hằng số | 1, 3, 10, 13 | Hỏi "hằng số này phụ thuộc vào gì?" |
| 12 | BCK gấp đôi dự đoán vì driver dùng slot 32 bit | 3, 13 | Không sai — sửa dự đoán và giải thích, đừng sửa số đo |
| 13 | Gọi một độ lệch tần số **cố định** là "clock drift" | 13 | Offset/skew khác drift (→ F4.1); lệch cỡ phần trăm là cấu hình/bộ chia, không phải thạch anh |
| 14 | Hâm đi hâm lại một mối hàn không thêm flux | 8 | Tối đa 2–3 lần, mỗi lần thêm flux |
| 15 | Làm phần cứng khi mệt (đặc biệt đo dòng và hàn) | mọi bài | Tuần crunch không ngồi bàn hàn — xem mục 8 |

## 7. Danh sách sửa lỗi so với bản gốc

Bản gốc: `khoa-1-tu-zero-den-do-duoc.md`. Không có bản Gemini cho K1.

**Đã sửa trong Phần A–B (chi tiết ở mục 11 của từng bài):**
- Bài 1: mô hình "dòng = throughput" và "điện trở = rate limiter" được chấm và bổ sung KCL; thêm công suất điện trở khi đổi nguồn (12 V làm quá tải cả LED lẫn điện trở 1/4 W); LED xanh lá InGaN ~2.8–3.3 V chứ không phải 2.0–2.2 V (gốc chỉ đúng với GaP kiểu cũ).
- Bài 2: thêm ground shift có số; phân biệt đất bảo vệ với mốc tín hiệu; chấm mô hình K3 lượt 11; "LED cắm ngược không hỏng" chỉ đúng ở 5 V (ngay ngưỡng V_R max thường gặp); "không chung GND thì vô nghĩa" là điều kiện của tín hiệu single-ended, tín hiệu vi sai/cách ly (Ethernet, K5) là ngoại lệ.
- Bài 3: ngưỡng "0,8 V / 2,0 V" là TTL, ESP32-S3 dùng 0,25/0,75·VDD (lỗi tương tự trong `robotics-data-infra-roadmap.md` mục 1.4); UART không "hỏng toàn bộ stream" khi lệch — start bit tái đồng bộ từng khung; công thức BCK cần `slot_width`; "Bài 14 nhìn thấy I2S" → Bài 13; I2S không chỉ điểm–điểm; thêm chấm ba mô hình K3 lượt 7 (quy chuẩn mục 7); bổ sung cách định thời thứ ba (clock nhúng: USB, Ethernet); "31 mẫu mỗi chu kỳ thừa sức" đúng để **nhìn**, không đủ để **đo** một chu kỳ BCK <1%.
- Bài 4: khói flux rosin là tác nhân mẫn cảm hô hấp (gốc: "không độc cấp tính"); "nguồn USB sẽ tự ngắt" không chắc với hub/sạc rẻ; thêm món thứ hai, dây đo, phụ kiện an toàn → chi phí tăng.
- Bài 5: UT33D+ dùng **2 pin AAA**, không phải pin 9 V; là đồng hồ **chỉnh thang tay** (gốc nói "nếu là đồng hồ chỉnh tay"); pin NiMH đầy nằm trong khoảng gốc gọi là "đã dùng"; hiệu ứng cầm hai đầu điện trở chỉ đáng kể với điện trở lớn; vùng chấp nhận chia ba: PASS / FAIL / KHÔNG KẾT LUẬN theo sai số đồng hồ; thêm mã màu 5 vòng và hệ số nhân; thêm bảng lỗi phá đồng hồ.
- Bài 6: "mọi thứ đều kêu → đồng hồ ở chế độ Ω thang thấp" sai (chế độ Ω không kêu), nguyên nhân thật thường là que chạm nhau; bíp là bộ phân loại có ngưỡng, đo ngưỡng trước khi tin; thêm kiểm từng jumper, vấn đề độ rộng ESP32 DevKit.
- Bài 7: 24 MHz × 1M mẫu không thể thấy LED 1 Hz; capture đầu tiên "chưa cần mạch gì" nhưng cần một chân có tín hiệu → thay bằng boot log UART; thêm bảng giới hạn có số (41,7 ns, Nyquist 12 MHz), phần Nyquist cho tín hiệu số (tần số / xung hẹp / thời điểm cạnh là ba ngưỡng khác nhau), cài đặt Linux.
- Bài 8: "hình nón bóng" chỉ đúng với thiếc có chì; thêm kỹ thuật, kiểm ba lớp, liên kết K7 C0.3.

**Sửa ở cấp khóa (file này):** "4 thí nghiệm" vs gate 5 lab; lịch 8–10h/tuần vs ngân sách 6–7h/tuần; gate tiêu chí 6 về BCK; ngân sách toàn lộ trình 885h / 1.106h thay vì 650h; thêm câu hỏi thứ tư về sai số.

**Đã sửa trong Phần C–D:**
- Bài 9: mẫu `prediction.md` của gốc điền sẵn đáp án → mẫu trống, số vào 🔒. Ngưỡng "<5%" giữ, nhưng cặp 10k/1k lắp đúng vẫn có thể vượt 5% so với dự đoán danh định (dung sai khuếch đại theo hệ số 1−k), cặp 1k/10k thì 5% quá lỏng → thêm bước đo R và dự đoán lần hai. Thí nghiệm 1 MΩ: "thấp hơn rõ rệt" là nói quá — mức sụt ~4–5% cùng bậc dung sai; thêm kiểm tổng KVL và suy ngược trở kháng vào của đồng hồ. Divider không dùng làm nguồn, không dùng cho I2C.
- Bài 10: "tiêu chí PASS số 3" → câu giải thích V_f là **tiêu chí 4**; "dòng đo ra 0 vì vượt thang" sai — vượt thang hiện `OL`/`1`, đọc 0 là cầu chì đứt/sai lỗ; thêm burden voltage, chế độ diode, phân biệt hai ngưỡng 5% (kiểm chéo) và 10% (gate).
- Bài 11: gốc không có `prediction.md` trong khi gate đòi 5 lab đều có → thêm dự đoán (hiệu chuẩn trực giác + tính thời gian đo typ/max); tách Absolute Max / Recommended / typ–max; chip ID là kiểm danh tính (gần `/version`) chứ không phải `/health`; thêm BMP280 (0x58), ngữ nghĩa ctrl_hum/burst read, điều cấm về thứ tự cấp nguồn.
- Bài 12: gốc hứa thấy `Data write: D0 … Data read: 60` khi chạy **scanner** — scanner chỉ dò địa chỉ; thêm sketch đọc chip ID. Gốc dự đoán **sau** khi chạy scanner → đưa lên trước. 4 MHz × 1M mẫu + "bấm reset" gần như chắc bắt trượt (WireScan chờ 5 s) → trigger. Tên ví dụ là `WireScan`. "Cả hai thẳng LOW → thiếu pull-up" sai trên ESP32 (driver bật pull-up nội): thiếu pull-up ngoài cho cạnh lên chậm, LOW liên tục là chập/bus treo.
- Bài 13: "chu kỳ BCK ±1%" không kiểm được bằng một chu kỳ ở 24 MHz (±2.1% ở 16 kHz, ±4.3% ở 32 kHz) → đo qua ≥32 chu kỳ. "LRCK lệch vài % … đây chính là clock drift": thạch anh lệch cỡ ppm, lệch % là cấu hình/bộ chia, và lệch cố định là offset chứ không phải drift; số đo là **tỉ số** hai thạch anh (ESP32/analyzer). "16 BCK mỗi LRCK → mono" không chắc với ESP-IDF. "Gán ba chân bất kỳ" → tránh chân strapping, USB, flash/PSRAM.
- Bài 14: thay kiểm `git log` bằng mắt bằng script kiểm thứ tự commit từng file; ngưỡng gate giữ nguyên, chỉ sửa phương pháp đo (tiêu chí 6) và cách đọc (tiêu chí 3).

Nhật ký hợp nhất hai bản soạn (Claude và Kiro) cho từng bài: `giao-trinh/_hop-nhat/khoa-1.md`.

## 8. Cách học khóa này

**Tuần thường (~6h cho K1):**
- Buổi 1 (≈2h, không cần bàn): đọc phần 1–4 của bài; viết `prediction.md` bằng tay, **không dùng AI**; commit.
- Buổi 2–3 (≈2h mỗi buổi, tại bàn): phần 6 "Làm"; ghi số đo **kèm sai số** ngay lúc đo, ảnh mạch vào `setup.md`.
- 30 phút cuối tuần: mở khối 🔒, viết `analysis.md` — chênh lệch, giải thích, thí nghiệm tiếp theo. Chọn 2 câu hỏi ngược để trả lời bằng chữ của bạn.

**Tuần crunch (0–2h):**
- Đọc phần 1–4 của bài kế tiếp và viết `prediction.md` (làm được trên điện thoại, không cần bàn). Hoặc chuyển hẳn sang K2.
- **Không** đo dòng, không hàn, không cấp điện cho mạch mới khi mệt. Lỗi ở Bài 5 và Bài 8 đến từ mất tập trung, không từ thiếu kiến thức.
- Ghi giờ thật vào `hours.csv`, kể cả 0.

**Dùng AI ở đâu:**

| Bước | AI? | Vì sao |
|---|---|---|
| Dự đoán bằng số | **Không** | Đây là thứ bạn đang mua bằng 35h |
| Tra cứu (datasheet ở đâu, lệnh PulseView) | **Có**, rồi kiểm lại ở nguồn gốc | AI cũng là một "dụng cụ đo" có sai số (→ F2.8) |
| Script mô phỏng, script phân tích số đo | **Có**, đọc lại từng dòng | Có stack trace |
| Giải thích chênh lệch dự đoán–đo | **Có điều kiện:** chỉ **sau khi** đã tự viết giả thuyết, và dùng prompt "chấm mô hình" | Tránh tích lũy mô hình đúng một nửa |

Prompt "chấm mô hình" (copy):

```
Dưới đây là mô hình tôi tự xây về <chủ đề>, và số đo của tôi. Đừng khen, đừng mở đầu bằng xác nhận.
Chấm từng ý: ĐÚNG / ĐÚNG MỘT PHẦN / SAI.
Với mỗi ý không ĐÚNG: chỉ chỗ gãy, đưa MỘT phản ví dụ cụ thể có số, và nói tôi cần đo gì để tự kiểm.
Nếu không chắc, nói "không chắc" và vì sao. Ghi rõ khẳng định nào cần tra datasheet.
---
<mô hình của tôi>
<số đo + sai số>
```

Bối cảnh của prompt này: ở phiên K3 với Gemini, nhiều mô hình chỉ đúng một phần đã được xác nhận "chính xác 100%" (xem chấm mô hình ở Bài 3). Cách học "trừu tượng hóa rồi hỏi ngược" của bạn hiệu quả, nhưng chỉ khi có ai đó — số đo, datasheet, hoặc một prompt buộc phải chấm — nói "sai".

## 9. Nguồn học kèm

| Nguồn | Xem phần nào | Cho bài |
|---|---|---|
| Ben Eater (YouTube) | Series máy tính 8-bit: clock, bus | 1–3, 12 |
| EEVblog Fundamentals (Dave Jones) | Multimeter, đọc datasheet, hàn | 5, 8, 11 |
| SparkFun tutorials | "How to Use a Multimeter", "How to Use a Breadboard", "I2C", "Serial Communication" | 3, 5, 6, 12 |
| Adafruit, "Guide To Excellent Soldering" | Toàn bộ, có ảnh mối đạt/không đạt | 8 |
| sigrok / PulseView docs | Getting started, fx2lafw, decoder | 7, 12, 13 |
| *Making Embedded Systems* — Elecia White | Chương đầu | Tư duy embedded cho người từ phần mềm |
| Espressif ESP-IDF Programming Guide, ESP32-S3 Datasheet | I2C, I2S driver; DC Characteristics | 3, 12, 13 |

Không cần sách điện tử dày ở giai đoạn này. *The Art of Electronics* để làm từ điển tra cứu, đừng đọc tuần tự.

## 10. Sau Khóa 1

- **K2 — Dữ liệu robot mà không cần robot (80h).** Không cần phần cứng; bắt đầu song song với K1, đừng chờ. Artifact công khai đầu tiên.
- **K3 — Chuỗi audio (90h).** Mở khi K1 PASS và `hours.csv` cho thấy median ≥ 5h/tuần. Nếu chưa đo được thì mua linh kiện về cũng chỉ để chạy tutorial.
- **K7 C0 — Xưởng, dụng cụ, an toàn (20h).** Mở được ngay sau **Phần B** của K1 (dụng cụ), chạy song song với phần còn lại của K1 và K2. Bài 8 của khóa này là bước luyện đầu tiên cho K7 C0.3; nguồn bàn giới hạn dòng (Bài 4, tùy chọn ở K1) thành bắt buộc ở K7 C0.4 trước khi đụng pin.
- **K7 C1 — Hệ nguồn.** Cần K1 trọn (tức gate này), tốt nhất sau K3 Bài 5–6.
