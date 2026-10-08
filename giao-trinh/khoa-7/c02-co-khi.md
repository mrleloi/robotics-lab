# Chặng 2 — Cơ khí (30h)

> **Vị trí:** C0 (xưởng, an toàn) → **C2** → C3 (bring-up trên bàn), C5 (lắp hoàn chỉnh) · **Cần trước:** C0; đọc → F1.1 · **Chạy song song với:** K2–K3 (và với C1 nếu bạn làm hai chặng xen kẽ)
> **Làm ra được:** khung có motor, bánh, caster, gá mini PC và gá pin (bằng vật giả cùng khối lượng), cáp đã đi và có giảm lực kéo · `mass_budget.csv`, `robot_params.yaml` (khối lượng, trọng tâm, đường kính bánh hiệu dụng, khoảng cách bánh, vị trí caster, kèm độ bất định) · **Sau chặng này bạn quyết định được:** mua motor tỉ số truyền nào cho khối lượng và tốc độ của bạn; đặt pin và mini PC ở đâu để robot không lật khi phanh gấp; một mối ghép ren cần ốc khóa, keo khóa ren hay chỉ cần siết đúng; con số hình học nào đủ tin để đưa vào sim.

Bạn chưa từng lắp cơ khí. Ở phần mềm, "gắn hai module với nhau" là một dòng import; ở đây nó là một con vít, và con vít đó sẽ tự lỏng ra sau vài giờ rung nếu không ai nghĩ về nó. Chặng này không cấp điện cho motor (đó là C3). Nó chọn motor bằng số, dựng khung, cân đo khung, và để lại một file tham số mà sim ở C11.1 sẽ đọc.

**Phân bổ 30h** `[ước lượng]`:

| Phần | Giờ |
|---|---|
| Bài C2.1 Lực, mô-men, chọn motor và tỉ số truyền bằng số | 6 |
| Bài C2.2 Khung, bố trí khối lượng, trọng tâm, chống lật | 5 |
| Bài C2.3 Gá lắp: vít, ốc khóa, rung, standoff, strain relief | 4 |
| Bài C2.4 Đo và cân robot: tham số hình học đầu tiên cho sim | 5 |
| Lắp bước 1–9 (kiểm hàng, mô hình bìa, khoan, gắn motor/bánh/caster, gá, đi cáp, thử nghiêng) | 9 |
| Gate chặng 2 | 1 |
| **Tổng** | **30** |

## 0. Bức tranh chặng

Sau chặng này robot là một **xe đẩy tay có hình học đã biết**: đẩy được, lăn được, chưa tự chạy. Mọi khối điện tử nặng đã có chỗ; pin được thay bằng vật giả cùng khối lượng.

```
  NHÌN TỪ TRÊN (tầng dưới)                         NHÌN NGANG
                 +x (trước, REP-103)
                   ▲                                 ┌───────────────┐  tầng trên: mini PC, ESP32
        ┌──────────┴──────────┐                      │  [mini PC]    │  (C5 thêm camera, loa)
        │       caster ◎      │  ← điểm tựa trước   ├──┬─────────┬──┤  standoff M3/M4
        │                     │                      │  │[PIN GIẢ]│  │  tầng dưới: pin thấp,
        │  ┌───────────────┐  │                      │ ═╪═════════╪═ │  sát trục bánh
   ┌──┐ │  │  PIN (giả)    │  │ ┌──┐            ─────┴──●─────────●──┴────  sàn
   │B │═╪══│  trọng tâm ✚  │══╪═│B │  ← trục bánh       bánh       caster
   │T │ │  └───────────────┘  │ │P │    (base_link)
   └──┘ │ [driver] [driver]   │ └──┘               h_G: chiều cao trọng tâm (C2.2, C2.4)
        │   cáp động lực ───► │                    d:   khoảng ngang trọng tâm → điểm tựa
        │   cáp tín hiệu ···► │
        └─────────────────────┘
          ◄─── track width b ──►  (khoảng giữa tâm vết bánh, C2.4 đo)
```

Mới trong chặng: khung, 2 motor có encoder (chưa nối điện), 2 bánh, caster, gá. Dòng điện: **không có**. Dòng dữ liệu: cân và thước → `build-log/measurements.jsonl` (schema của C0.5) → `mass_budget.csv`, `robot_params.yaml` → (C6.1 động học, C11.1 model sim).

## 1. An toàn của chặng

**Rủi ro cụ thể của C2:** mũi khoan kẹt làm tấm nhôm/gỗ quay theo, cứa tay; ba via (mép sắc) sau khi khoan/cắt nhôm cắt da và cắt **vỏ dây** (dây chạm khung nhôm là ngắn mạch xuống khung ở C5); vụn kim loại bắn vào mắt và rơi vào bo mạch; kẹp tay giữa bánh và khung; robot lăn khỏi bàn; vít quá dài đâm vào pin hoặc bo mạch ở tầng dưới; loctite dính da/mắt.

**Quy tắc cứng:**
- KHÔNG gắn pin thật lên khung trong C2. Dùng pin giả (hộp gỗ/bao cát cùng khối lượng và kích thước). Pin thật lên khung ở C5, sau khi gá đã qua thử lắc.
- KHÔNG khoan khi cầm tấm bằng tay. Kẹp tấm vào bàn bằng kẹp chữ C/ê tô, kê gỗ lót bên dưới.
- KHÔNG khoan, cắt, giũa gần bo mạch, mini PC, ESP32. Làm xong mọi lỗ, thổi/lau sạch vụn, rồi mới đưa điện tử lại gần.
- KHÔNG đeo găng vải khi dùng máy khoan (găng cuốn vào mũi). Kính bảo hộ luôn đeo khi khoan, cắt, giũa.
- KHÔNG để mép kim loại nào chưa vát ba via ở chỗ dây đi qua. Lỗ xuyên tấm cho dây phải có grommet (khoen cao su) hoặc ống bọc.
- KHÔNG dùng vít dài hơn mức cần (Bài C2.3 có công thức). Vít thừa chĩa vào vùng pin là cấm tuyệt đối.
- KHÔNG đặt robot gần mép bàn khi bánh tự do; khi làm việc trên bàn, kê khung lên khối gỗ cho bánh hở đất.
- KHÔNG dùng loctite trên nhựa acrylic/polycarbonate (Bài C2.3: làm nứt nhựa). Dùng ốc khóa nylon.
- KHÔNG làm cơ khí khi mệt. Tuần crunch: chỉ đọc Bài C2.1–C2.4 và chạy code.

**Khi sự cố xảy ra:**

| Sự cố | Làm ngay | KHÔNG làm |
|---|---|---|
| Mũi khoan kẹt, tấm quay | Nhả cò, buông máy theo hướng an toàn; máy có chế độ đảo chiều thì rút mũi ra bằng đảo chiều tốc độ thấp | Không cố giữ tấm đang quay bằng tay |
| Đứt tay do ba via | Rửa nước sạch, ép băng; vết sâu → cơ sở y tế | Không làm tiếp với tay chảy máu (máu + điện tử) |
| Vụn vào mắt | Rửa nước sạch chảy liên tục; không dụi; vụn kim loại → khám mắt | Không dùng nhíp tự gắp |
| Loctite dính da | Lau, rửa xà phòng; đã khô thì ngâm nước ấm rồi bóc nhẹ | Không dùng dung môi mạnh lên da |

## 2. BOM chặng

Giá `[ước lượng 10/2026]`, kiểm lại ở cửa hàng (danh sách nơi mua ở C0). Motor và bánh chỉ mua **sau** khi chạy xong Bài C2.1 với số của bạn.

| Món | Thông số phải chọn | Vì sao (bằng số) | Giá | Kiểm khi nhận hàng | Thay thế được bằng |
|---|---|---|---|---|---|
| 2× motor JGB37-520 12 V có encoder Hall | Tỉ số truyền theo Bài C2.1; trục ra 6 mm chữ D `[tự đo: có listing ghi 5,5 mm]`; encoder 2 kênh A/B, cấp 3,3–5 V `[tự đo]` | Mô-men đỉnh mỗi bánh và tốc độ khi chạy đều tính ở C2.1 | 150–300k/cái | Hai motor cùng mã, cùng tỉ số (đọc nhãn); quay trục ra bằng tay: êm, không lạo xạo, độ rơ đều; đo R cuộn dây bằng ohm kế, hai motor gần nhau | Motor DC giảm tốc có encoder cùng cỡ (JGA25 nhỏ hơn: tính lại C2.1) |
| 2× gá motor chữ L cho JGB37 | Nhôm/thép, lỗ khớp mặt hộp số | Gá nhựa in 3D mỏng xoắn dưới mô-men phanh | 20–50k/cái | Đặt motor thử: lỗ trùng, vít M3 vào được ren mặt hộp số `[tự đo: cỡ ren mặt hộp số]` | Gá in 3D PETG dày ≥4 mm (đo độ cứng ở bước 5) |
| 2× bánh cao su + khớp nối lục giác | Đường kính theo C2.1 (mặc định 85 mm `[ước lượng]`), lỗ khớp đúng trục, vít trí (set screw) | Bán kính vào thẳng công thức mô-men và tốc độ; bánh to qua ngưỡng cửa tốt hơn | 80–200k/cặp | Lắp lên trục, quay: bánh không đảo (lắc ngang) quá ~1 mm `[ước lượng]`; vít trí tì vào **mặt phẳng** chữ D | Bánh xe đẩy cỡ tương đương + khớp nối tự làm (khó) |
| Caster | Bánh xoay 1,5–2" có vòng bi, **hoặc** caster bi (ball caster) cỡ lớn | Caster nhỏ là thứ kẹt đầu tiên ở ngưỡng cửa và dây điện trên sàn (C2.2) | 30–100k | Xoay tự do, không rơ trục đứng | Hai caster (bố trí A, C2.2) |
| Tấm khung ×2 tầng | Ván ép 6 mm, **hoặc** nhôm tấm 2–3 mm, **hoặc** khung nhôm dựng sẵn cho JGB37 (kiểm kích thước chở mini PC) | Ván ép dễ khoan, không dẫn điện, đủ cứng cho 5–6 kg `[ước lượng]`; nhôm cứng hơn nhưng dẫn điện và có ba via | 50–400k | Phẳng (đặt lên bàn, ấn góc không bập bênh); đủ kích thước cho bố trí ở C2.2 | Mica/acrylic: KHÔNG khuyên (giòn, nứt ở lỗ vít, kỵ loctite) |
| Bộ vít, đai ốc, long đen M3 và M4 | Inox, đầu lục giác chìm (socket head), dài 6–30 mm; đai ốc thường + đai ốc khóa nylon (nyloc); long đen phẳng | Bài C2.3: M3 cho điện tử, M4 cho gá motor/tầng | 100–250k/bộ | Vặn thử đai ốc vào vít: trơn tay hết chiều dài | — |
| Bộ trụ đồng (standoff) M3 | Đồng thau lục giác + nylon, cao 10–40 mm, đực–cái và cái–cái | Tầng trên, gá bo mạch; nylon khi cần cách điện | 100–200k/bộ | Ren trơn; đo chiều cao 3 cái cùng cỡ bằng thước kẹp | — |
| Keo khóa ren cường độ trung bình | Loại "tháo được bằng dụng cụ tay" (ví dụ Loctite 243, màu xanh) `[spec — Henkel TDS]` | Vít kim loại vào kim loại chịu rung (gá motor) | 150–300k | Hạn dùng; nắp kín | Ốc khóa nylon (với mối có đai ốc) |
| Quản lý cáp | Dây rút nhiều cỡ, đế dán + đế bắt vít cho dây rút, grommet, ống lưới bọc dây | Giảm lực kéo lên đầu nối (C2.3) | 80–150k | — | — |
| Đai giữ pin | Dây đai có khóa (strap) + miếng chống trượt; hoặc hộp gá | Băng dính gai dán không giữ được 1 kg khi phanh gấp (C2.2) | 30–80k | — | Gá in 3D ôm pin + đai |
| Vật giả pin, mini PC | Hộp gỗ/túi cát cùng kích thước và khối lượng **đo được** (C1 cho số pin) | Bố trí khối lượng thật mà không có rủi ro pin | ~0 | Cân | Pin thật **không** được dùng thay |
| 3× cân điện tử | Giống nhau, ≥5 kg, phân giải 1 g | Cân ba điểm chạm cùng lúc (C2.4) | 3× 100–200k | Cân cùng một vật trên cả ba: lệch nhau ≤ vài g `[tự đo]` | 1 cân + 2 khối kê cùng độ cao, cân từng điểm một (chậm hơn, kém hơn) |
| Thước kẹp điện tử 150 mm | Phân giải 0,01 mm | Đo trục, bánh, lỗ | 150–300k | Đóng ngàm, về 0; đo một mũi khoan đã biết cỡ | Thước lá (kém 10 lần) |
| Máy khoan/vặn vít cầm tay có ly hợp (clutch) + mũi khoan 3,2/3,5/4,5 mm + mũi vát | Có nấc ly hợp mô-men, có đảo chiều | Lỗ cho M3 là ~3,2–3,4 mm, M4 là ~4,3–4,5 mm `[chuẩn — lỗ lọt ISO 273]` | 500k–1,5tr | Khoan thử lỗ trên gỗ thừa; vít lọt | Khoan tay + tua vít (chậm) |
| Bộ lục giác đầu bi hệ mét, tua vít PH1/PH2, cờ lê/tuýp 5,5 và 7 mm | 1,5–5 mm | 5,5 mm là đai ốc M3, 7 mm là M4 `[chuẩn — ISO 4032]` | 150–300k | — | — |
| Đột tâm, giũa nhỏ, kẹp chữ C ×2, bút sơn đánh dấu | — | Mũi khoan không trượt; vát ba via; kẹp phôi; vạch đánh dấu siết (C2.3) | 150–300k | — | — |

**Tổng C2 `[ước lượng]`:** ~2,5–5tr, phần lớn là motor, bánh, máy khoan và cân. Nếu mua khung nhôm dựng sẵn thì bớt việc khoan nhưng phải kiểm nó có chở được mini PC và pin không (bản gốc K7 đã cảnh báo: đừng mua khung mini thiết kế cho Pi).

## 3. Dụng cụ và kỹ năng tay

| Kỹ năng | Bài | Luyện trên phế liệu trước | Đạt trông thế nào | Hỏng trông thế nào |
|---|---|---|---|---|
| Lấy dấu, đột tâm, khoan đúng vị trí | C2.3 | 10 lỗ trên gỗ thừa theo một dưỡng giấy | Tâm lỗ lệch vạch ≤0,5 mm (đo thước kẹp); lỗ tròn, vuông góc | Lỗ hình bầu dục; mũi trượt khỏi vạch; lỗ nghiêng |
| Vát ba via | C2.3 | Mọi lỗ ở trên | Vuốt ngón tay qua mép không thấy vướng; nhìn có vát nhẹ | Gờ kim loại dựng lên quanh lỗ |
| Vặn vít bằng máy có ly hợp, siết tay lần cuối | C2.3 | 10 vít vào gỗ thừa và vào đai ốc | Đầu vít không toét; mặt tì phẳng, long đen không cong | Đầu lục giác toét (cam-out); gỗ nứt; long đen cong |
| Dùng keo khóa ren | C2.3 | 2 vít vào đai ốc trên phế liệu | 1–2 giọt trên ren phần ăn khớp, không tràn | Keo tràn vào khớp quay, vào ổ bi |
| Bó cáp, giảm lực kéo | C2.3 | Một bó dây thừa trên tấm thừa | Kéo dây gần đầu nối, lực truyền vào điểm buộc, không vào đầu nối | Dây căng như dây đàn tới đầu nối; dây rút cắt vào vỏ dây |
| Cân ba điểm, đo nghiêng | C2.4 | Cân một hộp đã biết khối lượng | Tổng ba cân khớp cân đơn trong vài g | Cân bị kê lệch, bánh chạm mép cân |

**Cầm máy khoan:** hai tay, khuỷu thẳng hàng với mũi; bắt đầu tốc độ chậm cho mũi ăn vào vết đột tâm, rồi tăng; ấn vừa đủ, để mũi tự cắt; sắp xuyên thủng thì giảm lực (lúc này mũi hay giật). Nhôm: nhỏ một giọt dầu. Lỗ ≥5 mm trên nhôm: khoan mồi 2,5–3 mm trước.

**Cầm tua vít điện:** đặt ly hợp ở nấc thấp nhất, thử; vít chưa xuống thì tăng một nấc. Máy chỉ dùng để **đưa vít xuống**; siết lần cuối bằng tay (lục giác chữ L, cầm đầu ngắn) để cảm được lúc vít "chạm" rồi thêm khoảng 1/8–1/4 vòng `[ước lượng — quy tắc tay cho M3 inox vào đai ốc thép; vào gỗ/nhựa ít hơn]`.

## 4. Sơ đồ đi dây

C2 chưa cấp điện, nhưng **đường đi** của cáp được quyết định lúc khoan lỗ và đặt đế dây rút. Quyết định sai ở đây sẽ thành nhiễu motor lên tín hiệu encoder ở C3/C5 (→ K7 C5.1).

```
   TẦNG DƯỚI (nhìn từ trên)                                ký hiệu
   ┌──────────────────────────────────────┐                ═══ cáp động lực (motor, nguồn) — đỏ/đen,
   │  ◎ caster                            │                    xoắn đôi, cỡ theo C1.3
   │                                      │                ··· cáp tín hiệu (encoder: 6 sợi) — đi
   │   ┌────────── PIN GIẢ ──────────┐    │                    phía đối diện, cắt cáp động lực vuông góc
   │   │ đai + miếng chống trượt     │    │                ▣   điểm giảm lực (dây rút qua đế bắt vít)
   │   └─────────────────────────────┘    │                ⊙   grommet (lỗ xuyên tầng)
   │ ▣═══════[DRV-T]      [DRV-P]═══════▣ │
   │ ║          ⊙ (lên tầng trên)       ║ │                Khoảng cách tối thiểu song song giữa
   │ M_T▣···············⊙··············▣M_P│                cáp động lực và cáp encoder:
   │  ↑ cáp motor ngắn, xoắn, buộc vào gá  │                vài cm `[ước lượng]`; chỗ phải cắt
   └──────────────────────────────────────┘                nhau thì cắt vuông góc.
```

| Cáp | Từ → tới | Loại | Màu (C0.5) | Giảm lực ở đâu |
|---|---|---|---|---|
| Motor T/P (+,−) | Cọc motor → driver (C3) | Cỡ theo dòng hãm đo ở C3 + C1.3 | Đỏ/đen, hoặc theo dây sẵn của motor | Dây rút qua gá motor, cách cọc motor 2–3 cm |
| Encoder T/P (VCC, GND, A, B) | Đầu cắm encoder → ESP32 (C3/C4) | Cáp sẵn của motor (thường 6 sợi chung đầu PH2.0 `[tự đo]`) | Theo cáp sẵn; ghi bảng màu vào `wiring/wires.csv` | Dây rút cách đầu cắm 3–5 cm, có vòng dư (service loop) |
| Nguồn lên tầng trên | Bo nguồn (C1) → mini PC, ESP32 | Theo C1 | Đỏ/đen | Grommet + dây rút hai phía lỗ |

Chưa nối gì vào gì ở C2: dây được **đặt và buộc**, đầu dây để chờ, quấn băng dính đánh nhãn.

## 5. Trình tự chặng

1. **Học Bài C2.1** (lực, mô-men, chọn motor). Commit `prediction.md` và kết quả script trước khi mua motor.
2. **Lắp bước 1 — Kiểm motor, bánh, caster khi nhận**
   - Làm: theo cột "Kiểm khi nhận hàng" ở mục 2. Đo đường kính trục ra và đường kính bánh bằng thước kẹp; quay tay trục ra, đếm cảm giác "rơ" khi đảo chiều (backlash hộp số).
   - ✅ Checkpoint (không cấp điện): ohm kế giữa hai cọc motor: phải là vài Ω, không phải 0 Ω (chập cuộn dây) cũng không phải hở (∞). Giữa cọc motor và vỏ motor: phải hở. Ghi R của cả hai motor vào `measurements.jsonl`.
   - Nếu sai: đổi hàng. Hai motor lệch R hơn ~30% `[ước lượng]` là dấu hiệu khác lô, hỏi người bán.
3. **Học Bài C2.2** (khung, khối lượng, trọng tâm, chống lật).
4. **Lắp bước 2 — Bảng khối lượng (mass budget)**
   - Làm: cân **từng** món sẽ lên robot (motor kèm gá, bánh, caster, tấm, mini PC, pin giả, ESP32, driver, bo nguồn ước lượng, vít); ghi vào `mass_budget.csv` cùng tọa độ dự kiến (x, y, z) của tâm mỗi món.
   - ✅ Checkpoint: tổng ≤ khối lượng thiết kế đã dùng ở C2.1. Vượt thì quay lại C2.1 chạy lại script **trước** khi khoan.
   - Nếu sai: bớt khối lượng, hoặc tính lại motor.
5. **Lắp bước 3 — Mô hình bìa 1:1**
   - Làm: cắt bìa carton theo kích thước tấm; đặt các món thật (trừ pin: dùng pin giả) lên; vẽ vị trí lỗ; chụp ảnh. Kiểm khoảng hở cho tay vặn vít và cho đầu cắm cáp.
   - ✅ Checkpoint: trọng tâm dự kiến (tính từ `mass_budget.csv`) nằm trong vùng an toàn của Bài C2.2 cho cả phanh tới và phanh lùi.
   - Nếu sai: dời pin, không dời quy tắc.
6. **Học Bài C2.3** (gá lắp).
7. **Lắp bước 4 — Lấy dấu và khoan**
   - Làm: dán dưỡng giấy in 1:1 lên tấm; đột tâm; khoan lỗ mồi rồi lỗ chính; vát ba via cả hai mặt; khoan **tất cả** lỗ trước khi gắn bất cứ thứ gì.
   - ✅ Checkpoint: đặt tấm trên, tấm dưới chồng nhau, xỏ vít qua lỗ standoff: lọt không cần ép. Vuốt tay qua mọi mép lỗ: không vướng.
   - Nếu sai: lỗ lệch ≤1 mm thì doa rộng bằng mũi lớn hơn một cỡ; lệch hơn thì khoan lỗ mới cách xa ≥2 lần đường kính.
8. **Lắp bước 5 — Gắn motor, bánh, caster**
   - Làm: gá motor bằng vít M3 + keo khóa ren (vào mặt hộp số kim loại) hoặc vít + nyloc (qua tấm); bánh lên trục, vít trí tì vào mặt phẳng chữ D, keo khóa ren; caster bằng M4 + nyloc.
   - ✅ Checkpoint (không cấp điện): (a) kê khung hở bánh, quay tay mỗi bánh 10 vòng: không chạm khung, không đảo ngang quá ~1 mm (đo bằng thước kẹp tì cạnh bánh vào một khối cố định); (b) đặt robot lên sàn phẳng, đo khoảng cách hai bánh ở **phía trước** và **phía sau** trục (thước kẹp/thước lá): hai số lệch nhau ≤1 mm `[ước lượng]`; (c) cả bánh và caster đều chạm sàn (luồn một tờ giấy dưới mỗi điểm chạm, rút ra phải có lực cản).
   - Nếu sai: bánh "chụm/doãng" → gá motor xoắn; chèn long đen hoặc làm lại gá. Một điểm không chạm sàn → bố trí 4 điểm (Bài C2.2), sửa chiều cao caster.
9. **Lắp bước 6 — Tầng trên, gá mini PC, gá pin giả**
   - Làm: standoff; mini PC trên giá có lỗ thông gió không bị che; pin giả bằng đai có khóa + miếng chống trượt.
   - ✅ Checkpoint: nghiêng khung 30° về mỗi phía bằng tay (giữ chắc): không món nào trượt. Lắc mạnh theo phương tới–lùi 10 lần: không tiếng lục cục.
   - Nếu sai: thêm đai thứ hai; chặn cơ khí (gờ, cữ) thay vì chỉ dựa vào ma sát.
10. **Lắp bước 7 — Đặt và buộc cáp** theo mục 4 (chưa nối điện).
    - ✅ Checkpoint: kéo nhẹ từng cáp ở chỗ cách đầu cắm 10 cm (khoảng 10 N, đo bằng cân hành lý của C0): đầu cắm không nhúc nhích; lực dồn vào điểm buộc. Không dây nào chạm mép kim loại chưa bọc.
    - Nếu sai: thêm điểm giảm lực; grommet.
11. **Học Bài C2.4** (đo và cân). Commit `prediction.md` trước khi cân.
12. **Lắp bước 8 — Cân ba điểm, đo nghiêng, đo bánh lăn** theo C2.4; xuất `robot_params.yaml`.
13. **Lắp bước 9 — Thử góc lật tĩnh và thử đẩy**
    - Làm: đặt robot lên tấm ván, nâng một đầu ván từ từ (robot quay ngang chặn bằng cữ để không trượt) tới khi bánh phía trên vừa nhấc; đo góc bằng điện thoại (ứng dụng đo nghiêng). Làm cho hướng chúi trước và ngửa sau. Có người hoặc gối đỡ phía dưới. Sau đó đẩy tay robot thẳng 5 m, đổi chiều đẩy, quan sát caster lật hướng.
    - ✅ Checkpoint: góc lật đo được so với dự đoán từ trọng tâm ở C2.4 (đáp án gập trong C2.4).
    - Nếu sai: xem C2.4 mục 8.
14. **Gate chặng 2.**

## 6. Lỗi người mới hay gặp

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Bánh lỏng trên trục sau vài lần quay tay | Vít trí tì vào phần tròn của trục, không vào mặt phẳng chữ D; không keo | Tháo, nhìn vết vít trên trục | Xoay cho vít tì mặt phẳng; keo khóa ren cường độ trung bình |
| Robot đẩy tay đi cong rõ | Hai bánh chụm/doãng (gá xoắn); hai bánh khác đường kính; caster lệch tâm | Đo khoảng cách trước/sau trục (bước 5b); đo đường kính hai bánh | Sửa gá; ghi đường kính thật vào `robot_params.yaml` (C6 sẽ hiệu chuẩn tiếp) |
| Một bánh kéo quay trơn khi đặt trên sàn | Bố trí 4 điểm tựa, sàn không phẳng → bánh nhấc lên | Tờ giấy dưới bánh (bước 5c) | Ba điểm tựa, hoặc caster có lò xo/treo (C2.2) |
| Lỗ khoan lệch, vít không lọt | Không đột tâm; dưỡng giấy co giãn; khoan nghiêng | Đo khoảng tâm lỗ bằng thước kẹp | Khoan theo thứ tự: một lỗ, bắt vít tạm, rồi khoan lỗ thứ hai qua lỗ của chi tiết thật |
| Đầu vít lục giác toét | Lục giác hệ inch/mòn; không ấn đủ; máy vặn quá nấc | Thử lục giác vào đầu vít mới: có rơ không | Lục giác hệ mét đúng cỡ, đầu thẳng (không dùng đầu bi) để siết lần cuối |
| Tấm ván ép nứt quanh vít | Siết quá; vít sát mép | Nhìn mép | Long đen to; lỗ cách mép ≥2–3 lần đường kính vít `[ước lượng]` |
| Mini PC nóng hơn khi lên khung | Che khe gió | Sờ vỏ sau 15 phút chạy (ở C5) | Kê standoff để hở đáy; không đặt pin sát cửa gió |
| Caster rung lắc (shimmy) khi đẩy nhanh | Caster rơ trục đứng, độ lệch trục (offset) nhỏ | Đẩy ở các tốc độ | Caster tốt hơn; caster bi |

## 7. Lăng kính data infra

**Dữ liệu chặng này sinh ra:**

| Luồng | File | Schema (rút gọn) | Tần số | Đơn vị |
|---|---|---|---|---|
| Phép đo thủ công | `build-log/measurements.jsonl` | schema C0.5 (`ts, stage, step, sample_id, quantity, value, unit, instrument_id, result, note`) | theo sự kiện, ~60–100 dòng ở C2 `[ước lượng]` | SI: `kg`, `m`, `rad`, `ohm` — không `g`, `mm`, `độ` trong dữ liệu |
| Bảng khối lượng | `hw/mass_budget.csv` | `part_id, mass_kg, x_m, y_m, z_m, source(measured/estimated), note` | khi đổi phần cứng | kg, m, trong `base_link` |
| Tham số hình học | `hw/robot_params.yaml` | mỗi tham số: `value`, `unit`, `std` (1σ), `method`, `measured_at`, `calibration_id` | khi đo lại | SI |
| Kết quả chọn motor | `hw/motor_sizing.md` + output script | đầu vào, đầu ra, quyết định | một lần (và khi khối lượng đổi) | — |

**Test tự động sinh ra từ chặng này:**
- **Kiểm nhất quán khối lượng:** tổng `mass_budget.csv` so với cân tổng ở C2.4; lệch quá ngưỡng (Gate) → CI báo. Đây là "reconciliation" kiểu kế toán: hai nguồn số độc lập phải khớp.
- **Kiểm hợp lệ tham số:** mọi tham số trong `robot_params.yaml` có `std` và `method`; đơn vị SI; trọng tâm nằm trong đa giác tựa. Đây là data contract theo **vật lý**, không chỉ theo schema (→ F3.7).
- **Hạt giống HIL/sim cho C11:** `robot_params.yaml` là đầu vào của model sim ở C11.1. Phép thử góc lật tĩnh (bước 9) là một **bài kiểm validation** đầu tiên cho model đó: sim với tham số này phải lật ở cùng góc. Ghi góc đo được làm "golden value".

**SLI:** tỉ lệ tham số có độ bất định (mục tiêu 100%); tỉ lệ khối lượng trong `mass_budget.csv` là `measured` thay vì `estimated`.

**Vai trò nghề:** Sim & Eval (tham số model có nguồn và độ bất định — thứ hiếm thấy trong repo sim thật); Test & Validation (golden value từ phép đo vật lý). Câu phỏng vấn tốt từ chặng này (theo tinh thần bản đồ vai trò của K7 gốc): "Tôi không thiết kế cơ khí. Tôi đo được hệ quả của nó, ghi nó thành tham số có sai số, và biết sim nhạy với tham số nào."

## 8. Nhật ký build

Copy vào `build-log/c02.md`, một mục mỗi buổi:

```markdown
## 2026-MM-DD — buổi N (giờ bắt đầu–kết thúc, giờ thực: _._ h)
- Trạng thái người: tỉnh táo / mệt (mệt → chỉ đọc, không khoan)
- Mục tiêu buổi: (ví dụ: khoan tấm dưới, gắn 2 motor)
- Đã làm:
- Số đo (đã ghi measurements.jsonl? số dòng: __)
- Ảnh trước/sau: build-log/img/c02/...
- Lỗ/vít làm lại (bao nhiêu, vì sao):
- Lỗi gặp (triệu chứng → nguyên nhân → sửa):
- Quyết định (→ decisions.md nếu ảnh hưởng chặng sau, ví dụ: tỉ số truyền, vị trí pin):
- Suýt sự cố (near miss): không / có → mô tả
- Câu hỏi còn mở:
```

---
