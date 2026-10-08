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
| Quản lý cáp, đai giữ pin | Dây rút, đế bắt vít, grommet; đai có khóa + miếng chống trượt | Giảm lực kéo lên đầu nối (C2.3); băng gai dán không giữ 1 kg khi phanh gấp (C2.2) | 100–250k | — | — |
| Vật giả pin, mini PC | Hộp gỗ/túi cát cùng kích thước và khối lượng **đo được** (C1 cho số pin) | Bố trí khối lượng thật mà không có rủi ro pin | ~0 | Cân | Pin thật **không** được dùng thay |
| 3× cân điện tử | Giống nhau, ≥5 kg, phân giải 1 g | Cân ba điểm chạm cùng lúc (C2.4) | 3× 100–200k | Cân cùng một vật trên cả ba: lệch nhau ≤ vài g `[tự đo]` | 1 cân + 2 khối kê cùng độ cao, cân từng điểm một (chậm hơn, kém hơn) |
| Thước kẹp điện tử 150 mm | Phân giải 0,01 mm | Đo trục, bánh, lỗ | 150–300k | Đóng ngàm về 0 | Thước lá |
| Máy khoan/vặn vít cầm tay có ly hợp (clutch) + mũi khoan 3,2/3,5/4,5 mm + mũi vát | Có nấc ly hợp mô-men, có đảo chiều | Lỗ cho M3 là ~3,2–3,4 mm, M4 là ~4,3–4,5 mm `[chuẩn — lỗ lọt ISO 273]` | 500k–1,5tr | Khoan thử lỗ trên gỗ thừa; vít lọt | Khoan tay + tua vít (chậm) |
| Dụng cụ tay nhỏ | Lục giác hệ mét 1,5–5 mm, tuýp 5,5/7 mm, đột tâm, giũa, kẹp chữ C ×2, bút sơn | 5,5 mm là đai ốc M3, 7 mm là M4 `[chuẩn — ISO 4032]` | 300–600k | — | — |

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

**Cầm máy khoan:** hai tay, khuỷu thẳng hàng với mũi; chậm cho mũi ăn vào vết đột tâm rồi tăng; sắp xuyên thủng thì giảm lực (mũi hay giật). Nhôm: một giọt dầu, lỗ ≥5 mm thì khoan mồi trước.

**Cầm tua vít điện:** đặt ly hợp ở nấc thấp nhất, thử; vít chưa xuống thì tăng một nấc. Máy chỉ dùng để **đưa vít xuống**; siết lần cuối bằng tay (lục giác chữ L, cầm đầu ngắn) để cảm được lúc vít "chạm" rồi thêm khoảng 1/8–1/4 vòng `[ước lượng — quy tắc tay cho M3 inox vào đai ốc thép; vào gỗ/nhựa ít hơn]`.

## 4. Sơ đồ đi dây

C2 chưa cấp điện, nhưng **đường đi** của cáp được quyết định lúc khoan lỗ và đặt đế dây rút. Quyết định sai ở đây sẽ thành nhiễu motor lên tín hiệu encoder ở C3/C5 (→ K7 C5.1).

```
   TẦNG DƯỚI (nhìn từ trên)                                ký hiệu
   ┌──────────────────────────────────────┐                ═══ cáp động lực (motor, nguồn) — màu C0.5,
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
| Motor T/P (M+, M−) | Cọc motor → driver (C3) | Cỡ theo dòng hãm đo ở C3 + C1.3 | Giữ màu dây sẵn của motor; dây nối dài **không** dùng đỏ (chỉ dành cho VBAT, C0.5) và không dùng đen (chỉ cho GND); nhãn `wire_id` hai đầu | Dây rút qua gá motor, cách cọc motor 2–3 cm |
| Encoder T/P (VCC, GND, A, B) | Đầu cắm encoder → ESP32 (C3/C4) | Cáp sẵn của motor (thường 6 sợi chung một đầu cắm `[tự đo]`) | Cáp sẵn giữ màu nhà sản xuất; dây nối dài theo C0.5: A xanh lá, B xám, 3,3 V trắng nhãn "3V3", GND đen; ghi vào `wiring/wires.csv` | Dây rút cách đầu cắm 3–5 cm, có vòng dư (service loop) |
| Nguồn lên tầng trên | Bo nguồn (C1) → mini PC, ESP32 | Theo C1 | Theo C0.5: cam 12 V (mini PC), tím 5 V (logic), đen GND | Grommet + dây rút hai phía lỗ |

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

## Bài C2.1 — Lực, mô-men, chọn motor và tỉ số truyền bằng số (6h)

> **Vị trí:** (mở đầu C2) → **C2.1** → C2.2 · **Cần trước:** K1 Bài 1 (bốn đại lượng), → F1.1 (con số nào là ước lượng); không cần C1 · **Sau bài này bạn quyết định được:** mua JGB37-520 tỉ số truyền nào với bánh đường kính nào, cho khối lượng và tốc độ của bạn; và chuyển con số dòng đỉnh, dòng chạy đều cho C1.2 (power budget) và C3 (chọn driver).

### 1. Câu chuyện — ai đã khổ vì chuyện này

Năm 1902–1903, anh em Wright cần một động cơ cho chiếc Flyer. Họ đã có số liệu lực nâng và lực cản đo bằng ống gió tự làm, nên tính được trước **cần bao nhiêu lực đẩy** và từ đó bao nhiêu công suất. Không nhà sản xuất động cơ ô tô nào họ hỏi chịu làm một động cơ đủ nhẹ cho công suất đó, nên thợ máy Charlie Taylor của họ đúc một động cơ khối nhôm khoảng 12 mã lực; còn cánh quạt thì họ tự thiết kế bằng lý thuyết, vì không có tài liệu nào về cánh quạt máy bay `[chuẩn — lịch sử được ghi chép rộng rãi, ví dụ Smithsonian National Air and Space Museum]`. Thứ đáng học không phải động cơ nhôm. Đó là **thứ tự**: yêu cầu (lực, tốc độ) → con số → rồi mới chọn hoặc làm phần cứng.

Người mới thường làm ngược: mua motor "trông khỏe", lắp, thấy robot ì, mua motor khác. Tỉ số truyền quá thấp thì kéo dòng lớn và nóng; quá cao thì không đạt tốc độ, và **chính rotor của motor thành một khối lượng ảo** phải tăng tốc mỗi lần khởi hành.

### 2. Mô hình tư duy

```
  LỰC Ở MẶT ĐẤT                  MÔ-MEN Ở BÁNH            Ở TRỤC MOTOR (qua hộp số N, hiệu suất η)
                                                          
       ▲ N (pháp tuyến)          τ_bánh = F_bánh · r      τ_motor = τ_bánh / (N·η)
  ┌────┴────┐  → F kéo           ω_bánh = v / r           ω_motor = ω_bánh · N
  │  m·a    │                                              Công suất: τ·ω gần như KHÔNG đổi qua
  └────┬────┘                                              hộp số (trừ tổn hao η) — hộp số chỉ
   ●───┼───● ← dốc θ                                       đổi tỉ lệ giữa mô-men và tốc độ.
       ▼ m·g
  F_tổng = m·a  +  m·g·sinθ  +  C_rr·m·g·cosθ  (+ quán tính rotor quy đổi, xem dưới)
            tăng tốc   leo dốc       cản lăn

  ĐƯỜNG ĐẶC TÍNH MOTOR DC (ở một điện áp)        dòng I = I0 + (I_hãm − I0)·τ/τ_hãm
  tốc độ                                           
  ω0 ●╲                                            hai điểm làm việc phải nằm DƯỚI đường:
     │  ╲   ✚ chạy đều (mô-men nhỏ, cần tốc độ)    ✚ chạy đều: cần ω đủ (kể cả dư cho PID)
     │    ╲                                        ✖ đỉnh (tăng tốc + dốc): cần τ, không cần ω tối đa
     │      ╲  ✖ đỉnh                              áp pin thấp → cả đường dịch xuống (ω0 ∝ V)
     │        ╲                                    
     └─────────●── mô-men                          
              τ_hãm (stall)                       
```

Năm câu bản chất:

1. **Mọi thứ bắt đầu từ lực ở mặt đất.** Ba thành phần: tăng tốc (`m·a`), leo dốc (`m·g·sinθ`), cản lăn (`C_rr·m·g·cosθ`). Cản lăn nhỏ nhưng **luôn có**; tăng tốc và dốc lớn nhưng **thỉnh thoảng**. Chia đều cho hai bánh kéo (caster không kéo).
2. **Hộp số là bộ đổi tỉ lệ, không phải bộ khuếch đại.** Nhân mô-men lên N lần thì chia tốc độ đi N lần; công suất cơ không tăng `[chuẩn]`. Chọn N là chọn **điểm làm việc** trên đường đặc tính của cùng một motor.
3. **Đường đặc tính motor DC gần như thẳng** từ tốc độ không tải `ω0` (mô-men 0) tới mô-men hãm `τ_hãm` (tốc độ 0), và dòng tăng tuyến tính theo mô-men `[chuẩn — từ mô hình R + back-EMF, C3.1]`. Hai con số đầu mút đọc được trên trang người bán; đường giữa là suy ra.
4. **Không chồng mọi trường hợp xấu nhất lên một điểm.** Lúc tăng tốc lên dốc, robot chưa cần tốc độ tối đa; lúc chạy tốc độ tối đa trên sàn phẳng, nó không cần mô-men đỉnh. Kiểm **hai điều kiện riêng**: mô-men đỉnh đủ (và không quá gần mô-men hãm), tốc độ khi chạy đều đủ (ở áp pin thấp nhất, có dư cho PID).
5. **Hộp số nhân quán tính rotor lên N².** Rotor quay nhanh hơn bánh N lần; động năng `½·J·ω²` của nó quy về bánh thành một khối lượng tịnh tiến tương đương `J_rotor·N²/r²` mỗi motor `[chuẩn — quy đổi quán tính qua hộp số]`. Với N lớn, con số này cùng cỡ khối lượng cả robot.

**Mô phỏng: ba tỉ số truyền JGB37-520, hai điều kiện, có quán tính rotor.** Số trong `cands` là số **ví dụ** kiểu trang người bán (có listing ghi 12 V 1:56: 178 rpm không tải, mô-men hãm 7,2 kg·cm, dòng hãm 2,4 A; listing khác ghi khác `[spec người bán, mâu thuẫn giữa các listing — tự đo ở C3.1]`). Thay bằng số của lô bạn định mua.

```python
# [đã chạy] Chọn tỉ số truyền bằng số: mô-men cần (tăng tốc + dốc + lăn) vs đường đặc tính motor
import numpy as np
G = 9.81
# --- Yêu cầu (thay bằng số của bạn) ---
m      = 6.0             # kg: mục tiêu 5 kg + 20% dự phòng
v_max  = 0.5             # m/s: tốc độ cứng tối đa
a_req  = 0.5             # m/s^2: tới 0,5 m/s trong 1 s
slope  = np.radians(5)   # dốc nhẹ (ram dốc văn phòng)
c_rr   = 0.03            # hệ số cản lăn: bánh cao su + caster trên sàn cứng/thảm mỏng
r      = 0.085 / 2       # m: bán kính bánh 85 mm
J_rot  = 1.5e-6          # kg·m²: quán tính rotor motor cỡ 520 [ước lượng: ~30 g, bán kính ~1 cm]
V_min, V_rated = 12.0, 12.0   # V: áp pack thấp còn dùng (4S LiFePO4, C1.1) / áp danh định motor
headroom = 1.25          # dư 25% tốc độ cho vòng PID (C4.2)
# --- Ứng viên: (tên, N, rpm không tải @V_rated ở trục ra, mô-men hãm kg·cm, I0 A, I_stall A) ---
# Số VÍ DỤ kiểu trang người bán JGB37-520; thay bằng số của lô bạn mua, rồi đo lại ở C3
cands = [("1:30", 30, 333, 3.9, 0.15, 2.4), ("1:56", 56, 178, 7.2, 0.15, 2.4),
         ("1:90", 90, 110, 12.0, 0.15, 2.4)]
rpm_need = v_max / (2*np.pi*r) * 60 * headroom
F_flat = m * c_rr * G                                      # chạy đều trên sàn phẳng, N
print(f"rpm bánh cần (kể cả dư {headroom}) = {rpm_need:.0f}")
for name, N, rpm0, ts_kgcm, I0, Is in cands:
    m_rot = 2 * J_rot * N**2 / r**2                        # rotor quy về khối lượng tịnh tiến
    F = (m + m_rot) * a_req + m * G * (np.sin(slope) + c_rr * np.cos(slope))
    tau_w = F * r / 2                                      # mô-men đỉnh mỗi bánh, N·m
    ts = ts_kgcm * 0.0981                                  # kg·cm -> N·m
    frac = tau_w / ts                                      # phần mô-men hãm dùng lúc đỉnh
    frac_c = (F_flat * r / 2) / ts                         # lúc chạy đều
    rpm_cruise = rpm0 * V_min / V_rated * (1 - frac_c)     # đặc tính thẳng, pin yếu
    I_peak, I_cruise = I0 + (Is - I0) * frac, I0 + (Is - I0) * frac_c
    ok_t, ok_v = frac <= 0.5, rpm_cruise >= rpm_need       # hai điều kiện TÁCH RIÊNG
    print(f"{name}: rotor ≈ {m_rot:4.1f} kg tương đương | đỉnh {tau_w/0.0981:4.2f} kg·cm = "
          f"{frac*100:3.0f}% hãm ({'đạt' if ok_t else 'trượt'}) | rpm chạy đều "
          f"{rpm_cruise:4.0f} ({'đạt' if ok_v else 'trượt'}) | I đỉnh {I_peak:.2f} A, "
          f"I đều {I_cruise:.2f} A")
```

Vì sao "≤50% mô-men hãm" cho đỉnh: ở đó motor cho công suất cơ lớn nhất nhưng hiệu suất ≤ ~50% và nhiệt cuộn dây ∝ `I²R` `[chuẩn]`; listing JGB37 ghi mô-men định mức (liên tục) chỉ cỡ 1/4–1/3 mô-men hãm `[spec người bán]`. Đỉnh ngắn được lên gần 50%, chạy đều phải dưới định mức. Quy tắc thô, đổi được nếu ghi lý do vào `decisions.md`.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Capacity planning: tính QPS đỉnh và trung bình, chọn instance có dư | Tính mô-men đỉnh và chạy đều, chọn tỉ số truyền có dư | Instance to hơn chỉ tốn tiền. Tỉ số truyền "to hơn" (N lớn) **làm hỏng** điều kiện kia: mất tốc độ và tăng quán tính rotor theo N². Không có lựa chọn "cứ lớn cho chắc" | Mua 1:90 "cho khỏe" → robot không bao giờ đạt 0,5 m/s khi pin yếu; PID bão hòa ở tốc độ cao |
| Không cộng p99 của từng service để ra p99 hệ thống (các đỉnh không đồng thời) | Không chồng đỉnh tăng tốc + dốc + tốc độ tối đa vào một điểm | Ở backend, cộng p99 cho ra con số **quá bi quan** nhưng vẫn an toàn. Ở đây, chồng điều kiện có thể loại **mọi** motor (thử: bỏ tách hai điều kiện trong code), đẩy bạn sang motor to gấp đôi, nặng hơn, ăn dòng hơn | Over-provision → motor nặng → khối lượng tăng → vòng lặp tính lại |
| Headroom 20–30% để autoscaler kịp phản ứng | Dư 25% tốc độ cho PID | PID cần dư để **sửa sai số** (tải đổi, pin sụt), không phải để "kịp scale". Không dư thì ở tốc độ đặt tối đa, bộ điều khiển bão hòa và mất điều khiển | Đặt `headroom = 1.0` → robot chạy 0,5 m/s trên sàn phẳng lúc pin đầy, chậm dần khi pin yếu mà không ai biết |

**Chấm mô hình:**

- *"Motor có tỉ số truyền lớn hơn thì mạnh hơn, nên an toàn hơn."* **ĐÚNG MỘT PHẦN.** Đúng là mô-men hãm ở trục ra tăng gần tỉ lệ N. Sai ở "an toàn hơn": tốc độ giảm cùng tỉ lệ, quán tính rotor quy đổi tăng theo N², và hộp số tỉ số cao có thể **gãy răng** trước khi motor đạt mô-men hãm (người bán thường ghi "mô-men cho phép" của hộp số thấp hơn mô-men hãm × N `[tự đo — đọc kỹ listing]`). Phản ví dụ: trong mô phỏng, 1:90 qua điều kiện mô-men dễ nhất nhưng trượt điều kiện tốc độ.
- *"Chọn motor theo công suất (W) là đủ."* **ĐÚNG MỘT PHẦN.** Công suất cho biết motor **có thể** làm được việc đó ở **một** điểm làm việc nào đó; nó không nói điểm đó có trùng với tốc độ bánh bạn cần không. Phản ví dụ: cùng một motor 520, ba tỉ số truyền cho ba kết quả đạt/trượt khác nhau.
- *"Khối lượng robot là thứ duy nhất phải tăng tốc."* **SAI** với gearmotor tỉ số cao. Phản ví dụ: dòng `rotor ≈ … kg tương đương` của mô phỏng (gập ở phần 7).

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | Mô-men xoắn (torque), N·m | Lực × cánh tay đòn; thứ làm bánh quay | "Lực" — cùng lực, bánh to cần mô-men lớn hơn |
| 🟢 | kg·cm (kgf·cm) | Đơn vị người bán hay dùng; 1 kgf·cm ≈ 0,0981 N·m `[chuẩn]` | Khối lượng × khoảng cách |
| 🟢 | Tỉ số truyền N | Số vòng motor cho một vòng trục ra | "Càng lớn càng khỏe" (xem chấm mô hình) |
| 🟢 | Tốc độ không tải, mô-men hãm (stall torque) | Hai đầu mút đường đặc tính ở một điện áp | Hai giới hạn vận hành bình thường — motor không nên làm việc gần cả hai |
| 🟢 | Hệ số cản lăn C_rr | Lực cản lăn chia cho trọng lượng | Ma sát trượt (μ) — hai thứ khác hẳn, cùng cỡ thì sai |
| 🟡 | Quán tính quy đổi (reflected inertia) | Quán tính phía motor nhìn từ phía bánh, nhân N² | Không đáng kể (đúng với N nhỏ, sai với N lớn) |
| 🟡 | Hiệu suất hộp số η | Phần công suất qua được hộp số | Hằng số — thay đổi theo tải, nhiệt, mỡ |
| 🔴 | Thiết kế bánh răng, mô-đun răng | Kỹ sư cơ khí | — |

### 5. Dự đoán

**Đề:** với robot mục tiêu ≤5 kg (dùng 6 kg để tính), tốc độ tối đa 0,5 m/s, tăng tốc 0,5 m/s², dốc 5°, bánh 85 mm:

1. Tính **bằng tay** (máy tính bỏ túi, không chạy code): lực kéo tổng (chưa tính quán tính rotor), mô-men mỗi bánh (N·m và kg·cm), số vòng/phút bánh cần ở 0,5 m/s.
2. Đoán: trong ba tỉ số 1:30, 1:56, 1:90, cái nào qua cả hai điều kiện? Cái nào trượt, trượt điều kiện nào?
3. Đoán độ lớn của "khối lượng tương đương" của hai rotor ở 1:56: nhỏ hơn 0,5 kg, cỡ 1–2 kg, hay cỡ khối lượng robot?
4. Dòng đỉnh mỗi motor ở tỉ số bạn chọn.
5. Nếu bạn đổi sang bánh 65 mm, kết luận ở câu 2 đổi thế nào? (đoán hướng trước, rồi sửa `r` trong code)

**Tham số cần tra:** trang người bán (hoặc datasheet nếu có) của đúng mã JGB37-520 bạn định mua: điện áp danh định, rpm không tải ở trục ra, dòng không tải, mô-men hãm, dòng hãm, mô-men định mức, mô-men cho phép của hộp số; ghi rõ **listing nào** (link, ngày). Áp pack: C1 chốt mặc định **4S LiFePO4** (~12,8 V danh định, 14,6 V đầy, cắt ~10–11 V) và động lực motor đi thẳng từ pack qua E-stop (→ K7 C1.1). LiFePO4 giữ áp gần phẳng quanh 13 V phần lớn dung lượng rồi tụt nhanh ở cuối `[chuẩn]`; bài này lấy `V_min = 12,0 V` (đầu gối cuối đường xả `[ước lượng]`) để tính tốc độ, và 14,6 V để tính trường hợp nhanh nhất/dòng lớn nhất. Pin khác thì thay số. C_rr: chưa đo thì 0,03 `[ước lượng]`, sẽ đo ở bước 6 phần Làm.

**Công thức:** `F = m·a + m·g·sinθ + C_rr·m·g·cosθ`; `τ_bánh = F·r/2`; `rpm = v/(2πr)·60`; `m_rotor_tđ = 2·J·N²/r²`; `I = I0 + (I_hãm − I0)·τ/τ_hãm`.

```markdown
# prediction.md — K7 C2.1
commit: <hash>  ngày: <yyyy-mm-dd>
## Đầu vào (nguồn từng dòng)
- m = 6.0 kg (mục tiêu 5 kg + 20%)   v_max = 0.5 m/s   a = 0.5 m/s²   θ = 5°   C_rr = 0.03 (ước lượng)
- Bánh D = ... mm (đo thước kẹp)   V_min pack = ... V (nguồn: C1.1, mặc định 4S LiFePO4 → 12,0 V)
- Listing motor: <link, ngày> — rpm0 = ..., τ_hãm = ... kg·cm, I0 = ... A, I_hãm = ... A
## Tính tay
| Đại lượng | Giá trị | Cách tính |
|---|---|---|
| F tổng (N), chưa có rotor | | |
| τ mỗi bánh (N·m / kg·cm) | | |
| rpm bánh cần (có dư 25%) | | |
## Đoán
- Tỉ số qua cả hai điều kiện: ...   trượt: ... (điều kiện ...)
- Khối lượng rotor tương đương ở 1:56: ...
- I đỉnh mỗi motor: ... A
- Bánh 65 mm: ...
## Tôi sẽ ngạc nhiên nếu...
```

### 6. Làm

1. Commit `prediction.md`.
2. Chạy script với số mặc định; so với tính tay của bạn (lệch >5% → tìm lỗi đơn vị, thường là kg·cm ↔ N·m hoặc đường kính ↔ bán kính).
3. Thay `cands` bằng số của **listing thật** bạn định mua (ít nhất 3 tỉ số). Kiểm `V_min` với C1.1. Chạy thêm một lần với `V_min = V_rated = 14.6` (pin đầy): tốc độ không tải cao hơn ~22%, dòng đỉnh khi kẹt cũng cao hơn ~22% — ghi cả hai vào `motor_sizing.md`.
4. **Độ nhạy (→ F6.6, dạng tối thiểu):** chạy lại với `c_rr` = 0,015 và 0,06; `J_rot` gấp đôi và một nửa; `m` = 5 và 7 kg. Ghi bảng: tham số nào làm đổi **quyết định** (tỉ số nào thắng), tham số nào chỉ đổi con số. Quyết định không đổi qua cả dải → yên tâm mua.
5. Ghi `hw/motor_sizing.md`: đầu vào, bảng kết quả, bảng độ nhạy, quyết định (tỉ số, bánh), dòng đỉnh và dòng chạy đều **mỗi motor** để chuyển cho C1.2 và C3. Ghi một dòng vào `decisions.md`. Rồi mới mua.
6. **Sau Lắp bước 6 (khung đã có khối lượng thật):** đo C_rr. Buộc cân hành lý vào khung ở độ cao trục bánh, kéo robot **thật chậm và đều** trên sàn văn phòng (và một lần trên thảm nếu có), đọc lực khi đã lăn đều (không đọc lúc giật ra). Lặp 5 lần mỗi mặt sàn, lấy trung vị. `C_rr ≈ F/(m·g)`. Sai số: cân hành lý phân giải 10 g ≈ 0,1 N `[spec — loại bạn mua]`, so với lực cỡ 1–3 N là 3–10%; tay kéo không đều là sai số lớn hơn — đó là lý do lấy trung vị. Lưu ý: motor chưa nối điện vẫn quay theo qua hộp số, nên số đo **gồm** ma sát hộp số và motor bị kéo ngược — đúng cái bạn cần cho chạy thật? Ghi câu trả lời của bạn vào `motor_sizing.md` (gợi ý ở câu hỏi ngược 4).
7. Chạy lại script với C_rr đo được và khối lượng từ `mass_budget.csv`. Quyết định còn đứng không?

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

**Tính tay (đầu vào mặc định):** `a + g·sin5° + 0,03·g·cos5° = 0,5 + 0,855 + 0,293 = 1,648 m/s²` → F ≈ 9,9 N → τ mỗi bánh ≈ 9,9 × 0,0425 / 2 ≈ 0,21 N·m ≈ **2,14 kg·cm**. rpm bánh ở 0,5 m/s: 0,5/(π·0,085)·60 ≈ 112 rpm; có dư 25% → **140 rpm**. Thành phần lớn nhất là **dốc**, không phải tăng tốc; cản lăn nhỏ nhất nhưng là thứ duy nhất có mặt **mọi lúc**.

**Output script (số listing ví dụ):**

| Tỉ số | Rotor tương đương (2 motor) | Mô-men đỉnh mỗi bánh | % mô-men hãm | rpm chạy đều (12 V) | I đỉnh / I đều mỗi motor | Kết luận |
|---|---|---|---|---|---|---|
| 1:30 | ~1,5 kg | 2,30 kg·cm | 59% (trượt) | 300 (đạt) | 1,48 / 0,37 A | Nhanh nhưng làm việc quá gần mô-men hãm |
| **1:56** | **~5,2 kg** | 2,71 kg·cm | 38% (đạt) | 169 (đạt) | 1,00 / 0,27 A | **Qua cả hai** |
| 1:90 | ~13,5 kg | 3,60 kg·cm | 30% (đạt) | 106 (trượt) | 0,82 / 0,22 A | Khỏe nhưng không đạt tốc độ |

- Rotor tương đương ở 1:56 **gần bằng khối lượng robot**. Với 1:90 nó gấp đôi robot. Con số này dựa trên `J_rot` ước lượng; nếu J thật chỉ bằng một nửa, kết luận "1:56 thắng" vẫn đứng (thử ở bước 4). Đây cũng là lý do robot tỉ số cao "ì" khi khởi hành dù mô-men hãm lớn.
- Nếu không tách hai điều kiện (chồng đỉnh và tốc độ tối đa vào một điểm), **cả ba** tỉ số đều trượt. Đó là bản chạy đầu tiên khi viết bài này.
- Bánh 65 mm (`r = 0.0325`): rpm cần tăng (~183 rpm có dư), mô-men cần giảm → điểm làm việc dịch về phía tỉ số thấp; 1:56 không còn đạt tốc độ khi pin 12 V. Kết luận: **bánh và tỉ số truyền chọn cùng nhau**.
- I đỉnh ~1 A mỗi motor là dòng **tăng tốc theo kế hoạch**. Lúc khởi động từ đứng yên với lệnh bậc thang, motor chạm gần **dòng hãm** trong vài ms (C3.1) — đó mới là con số chọn driver và cầu chì.

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Tính tay lệch script ~10 lần | kg·cm vs N·m; hoặc mm vs m | In từng số hạng | Đơn vị SI trong code, đổi ở biên |
| Tính tay lệch script đúng 2 lần | Quên chia hai bánh, hoặc dùng đường kính thay bán kính | — | — |
| Không tỉ số nào đạt | Khối lượng/dốc quá tham vọng; hoặc pin quá thấp áp | Chạy độ nhạy | Bỏ yêu cầu dốc (văn phòng không dốc?), bánh to hơn, hoặc họ motor lớn hơn; ghi quyết định |
| Hai listing cùng mã cho số khác xa nhau | Người bán sao chép bảng của motor khác | So rpm × N: phải ra cùng tốc độ motor gốc | Tin số đo ở C3 hơn listing; mua 1 motor thử trước |

### 9. Câu hỏi ngược

1. **[Nếu…thì]** Nếu robot sau này chở thêm loa và amp (C12) nặng 1 kg đặt cao, phép tính ở bài này đổi ở những chỗ nào? Chỗ nào **không** đổi?
<details><summary>Hướng nghĩ</summary>

Lực tăng tuyến tính theo m ở ba số hạng; quán tính rotor không đổi (không phụ thuộc m). Tốc độ chạy đều gần như không đổi vì cản lăn nhỏ. Thứ đổi nhiều hơn nằm ở bài sau: trọng tâm cao lên. Đó là lý do khối lượng thiết kế có dự phòng 20%.

</details>

2. **[Vì sao không]** Vì sao không dùng motor bước (stepper) hay BLDC với driver FOC, vốn chính xác hơn và không cần encoder (stepper) hoặc hiệu suất cao hơn (BLDC)?
<details><summary>Hướng nghĩ</summary>

Stepper mất bước âm thầm khi quá tải (đúng loại lỗi "không có dấu hiệu" như mất count encoder), mô-men giảm mạnh ở tốc độ cao, ăn dòng cả khi đứng yên. BLDC + FOC tốt hơn nhiều về hiệu suất nhưng thêm một tầng firmware phức tạp. Câu hỏi đúng: thứ bạn muốn học ở K7 là data infra quanh robot hay điều khiển motor? Ghi lựa chọn vào `decisions.md`.

</details>

3. **[Quy mô]** Đội 100 robot giao hàng trong tòa nhà; mỗi robot chở tải khác nhau mỗi chuyến (0–3 kg). Bạn có `motor_sizing.md` cho robot rỗng. Cái gì gãy trước: động cơ quá nhiệt, pin hết sớm, hay vòng điều khiển được tinh chỉnh cho khối lượng rỗng?
<details><summary>Hướng nghĩ</summary>

Nghĩ về thứ bị ảnh hưởng **liên tục** (cản lăn, nhiệt ∝ I²) và thứ bị ảnh hưởng **ở đỉnh** (tăng tốc, phanh, chống lật C2.2). Khối lượng thay đổi là một tham số ẩn mà PID không biết. Đội xe thật thường ước lượng tải từ dòng motor lúc tăng tốc: đó là system ID trực tuyến (→ F6.4).

</details>

4. **[Failure mode]** Bạn đo C_rr bằng cách kéo robot chưa cấp điện. Kể một cách con số này sai **có hệ thống** so với lúc robot tự chạy, và hướng sai.
<details><summary>Hướng nghĩ</summary>

Khi bị kéo, hộp số chạy ngược chiều truyền lực (bánh kéo motor); hiệu suất ngược của hộp số khác chiều thuận, và motor bị kéo ngược có ma sát chổi than. Khi tự chạy, motor gánh ma sát hộp số **bên trong** đường đặc tính (dòng không tải). Có bị tính hai lần không?

</details>

5. **[Phản biện]** "Cứ mua motor to hơn hai cỡ cho chắc, pin thừa sức." Bạn phản bác bằng ba con số nào trong `motor_sizing.md`?
<details><summary>Hướng nghĩ</summary>

Khối lượng motor (vào lại phương trình), dòng hãm (vào driver, cầu chì, C1), và mô-men phanh khi phanh gấp (vào chống lật, C2.2). "To hơn" không miễn phí ở cả ba.

</details>

### 10. Liên kết ra ngoài

- **Thang máy và đối trọng.** Motor thang máy không nâng cả cabin: đối trọng cân bằng cabin cộng khoảng nửa tải định mức, nên motor chỉ gánh phần chênh. Giống: tách thành phần "luôn có" khỏi phần "thỉnh thoảng". Khác: robot không có đối trọng cho dốc; thứ gần nhất là chọn N sao cho trường hợp thường xuyên nằm ở vùng hiệu suất tốt.
- **Hàng không, chân vịt bước thay đổi (variable-pitch propeller).** Máy bay cánh quạt đổi bước cánh để động cơ làm việc gần vòng tua tối ưu ở cả cất cánh (cần lực đẩy) và bay bằng (cần tốc độ). Đây chính là "hai điểm làm việc" của bài, được giải bằng một hộp số biến thiên. Robot rẻ không có thứ đó, nên phải thỏa hiệp bằng tính toán.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| `F = m·a + m·g·sinθ + C_rr·m·g·cosθ` | [chuẩn] | Cơ học Newton |
| Hộp số giữ công suất trừ tổn hao | [chuẩn] | — |
| Đường đặc tính motor DC gần thẳng, dòng tuyến tính theo mô-men | [chuẩn] | Từ mô hình R + back-EMF; C3.1 kiểm |
| Quán tính quy đổi `J·N²` | [chuẩn] | Động năng bảo toàn qua hộp số |
| `J_rot ≈ 1,5·10⁻⁶ kg·m²` cho motor cỡ 520 | [ước lượng] | Từ khối lượng/bán kính rotor đoán; chạy độ nhạy |
| JGB37-520 12 V 1:56: 178 rpm, 7,2 kg·cm, 2,4 A hãm | [spec người bán] | Listing khác ghi khác (có bảng ghi dòng hãm 1,2 A cho dải tỉ số thấp); đo ở C3.1 |
| C_rr = 0,03 | [ước lượng] | Đo ở bước 6 |
| 1 kgf·cm = 0,0981 N·m | [chuẩn] | — |
| Lịch sử động cơ Wright Flyer | [chuẩn] | Smithsonian NASM |

**Đã sửa so với bản gốc:** K7 gốc chỉ ghi "2 motor DC có hộp số và encoder đủ mô-men cho tổng khối lượng" mà không có phương pháp; bài này thêm phương pháp hai điều kiện, quán tính rotor, và độ nhạy. K7 gốc lấy ví dụ 1:34 với bánh 65 mm; với robot chở mini PC + pin ~5 kg ở 0,5 m/s, ví dụ mặc định ở đây đổi sang bánh 85 mm và chọn tỉ số bằng tính toán (kết quả có thể khác với số listing của bạn).

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** trang người bán/datasheet motor của bạn (lưu bản PDF hoặc ảnh chụp vào repo, vì listing đổi).
- **Giải thích:** Hughes & Drury, *Electric Motors and Drives* — chương motor DC (đặc tính mô-men–tốc độ) và chương về hộp số/quán tính quy đổi.
- **Đào sâu (tùy chọn):** Siegwart, Nourbakhsh & Scaramuzza, *Introduction to Autonomous Mobile Robots* — chương về cơ cấu di chuyển có bánh.
- **Tự kiểm tra:** (1) giải thích cho một backend engineer khác trong 5 câu vì sao "tỉ số lớn hơn cho chắc" là sai; (2) vẽ lại đường đặc tính với hai điểm làm việc từ trí nhớ; (3) câu dưới.

  Robot 4 kg, bánh 100 mm, chỉ chạy sàn phẳng, tăng tốc 0,3 m/s², C_rr 0,02. Mô-men đỉnh mỗi bánh (bỏ quán tính rotor)?
  <details><summary>Đáp án</summary>

  F = 4 × (0,3 + 0,02 × 9,81) ≈ 4 × 0,496 ≈ 1,98 N; τ = 1,98 × 0,05 / 2 ≈ 0,050 N·m ≈ 0,50 kg·cm. Rất nhỏ: dốc mới là thứ quyết định motor.

  </details>

---

## Bài C2.2 — Khung, bố trí khối lượng, trọng tâm, chống lật (5h)

> **Vị trí:** C2.1 → **C2.2** → C2.3 · **Cần trước:** C2.1 · **Sau bài này bạn quyết định được:** bố trí bánh kéo/caster kiểu nào, đặt pin và mini PC ở đâu (cao bao nhiêu, cách trục bao xa) để robot không lật khi phanh gấp hay tăng tốc, và robot của bạn có cần giới hạn gia tốc phanh trong firmware không (→ K7 C4.4).

### 1. Câu chuyện — ai đã khổ vì chuyện này

Xe nâng hàng (forklift) đứng trên ba "điểm tựa hiệu dụng" (hai bánh trước và chốt xoay cầu sau), tạo thành **tam giác ổn định**. Chừng nào hình chiếu của trọng tâm tổng (xe + hàng) còn nằm trong tam giác, xe đứng; nâng hàng cao, phanh gấp, rẽ nhanh là ba cách đẩy hình chiếu đó ra ngoài. OSHA (cơ quan an toàn lao động Mỹ) ghi lật xe là nguyên nhân hàng đầu của tử vong liên quan xe nâng, và đào tạo người lái xoay quanh đúng khái niệm tam giác này `[chuẩn — tài liệu đào tạo forklift của OSHA]`.

Robot của bạn là một xe nâng nhỏ chở mini PC, pin, và (ở C12) loa. Nó lật không giết ai, nhưng một lần lật là mini PC rơi, đầu nối gãy, pin va đập (C1.6: pin đã va đập thì cách ly). Và khác xe nâng, người "lái" robot là firmware: nó sẽ phanh gấp đúng lúc bạn không ngờ, ví dụ khi mất heartbeat (C4.4) hay khi nhấn E-stop.

### 2. Mô hình tư duy

```
  NHÌN NGANG, robot đang PHANH khi đi tới (gia tốc a hướng ra sau)
                          m·a (lực quán tính, đặt tại trọng tâm, hướng tới trước)
                     ✚ ───►
                     │ G       h = chiều cao trọng tâm
                     │ m·g
     ────────●───────┼────────◎──────  sàn
          bánh kéo   │◄── d ──►caster trước = điểm lật
  Lật quanh điểm tựa trước khi mô-men lật > mô-men giữ:   m·a·h > m·g·d
                              ⇒  a_lật = g · d / h        (không phụ thuộc khối lượng)
  Robot chỉ phanh được tới  a_thật = min( μ·g·(phần tải trên bánh kéo) ,  mô-men phanh motor / (r·m) )
  An toàn khi a_thật < a_lật  ở CẢ hai hướng (phanh khi tới, phanh khi lùi = tăng tốc khi tới).
```

Bốn câu bản chất:

1. **Lật là chuyện tỉ số d/h, không phải chuyện nặng nhẹ.** Robot nặng gấp đôi nhưng cùng hình học lật ở cùng gia tốc. Muốn chắc: hạ h (pin xuống thấp nhất), tăng d (điểm tựa xa trọng tâm).
2. **Gia tốc phanh có trần do bám đường và do motor.** Bánh trượt trước khi lật là "an toàn" về lật (nhưng odometry hỏng, C6.3). Phanh ngắn mạch motor (C3.2) cho mô-men phanh cỡ mô-men hãm ở tốc độ cao `[chuẩn — C3.2 dẫn]`, có thể đủ để lật một robot cao.
3. **Ba điểm tựa xác định; bốn điểm thì không.** Hai bánh kéo + một caster luôn chạm sàn. Hai bánh kéo + hai caster (trước, sau) trên sàn không phẳng sẽ có lúc một bánh **kéo** nhấc lên hoặc mất tải → trượt `[chuẩn — tĩnh học siêu tĩnh]`. Bố trí 4 điểm cần một caster có lò xo hoặc trục bánh kéo có treo.
4. **Tải trên bánh kéo quyết định bám đường.** Trọng tâm càng gần trục bánh kéo, bánh kéo càng gánh nhiều tải, bám càng tốt; nhưng d về phía đó càng nhỏ → dễ lật về phía đó. Đây là đánh đổi thật, không có điểm "tối ưu mọi mặt".

**Mô phỏng: ba bố trí, ba chiều cao trọng tâm.** Số ví dụ: 6 kg, bánh 85 mm, μ = 0,6, mô-men phanh lấy bằng mô-men hãm của 1:56 ở C2.1 (trường hợp xấu nhất).

```python
# [đã chạy] Phanh gấp có lật không? So gia tốc gây lật với gia tốc phanh motor/ma sát cho phép
import numpy as np
G, mu = 9.81, 0.6                # ma sát cao su–sàn gạch [ước lượng]
m, r = 6.0, 0.0425               # kg, bán kính bánh m
tau_brake = 2 * 7.2 * 0.0981     # N·m, 2 bánh, phanh ngắn mạch ~ mô-men hãm (C3.2), ví dụ 1:56
# Bố trí: x đo dọc thân (+ = phía trước), gốc ở trục bánh kéo.
# điểm tựa trước/sau = điểm chạm đất ngoài cùng; cog_x = vị trí trọng tâm
layouts = {
  "A: bánh kéo giữa, caster trước+sau": dict(front=+0.12, rear=-0.12, cog_x=0.00),
  "B: bánh kéo sau, caster trước":      dict(front=+0.20, rear= 0.00, cog_x=0.05),
  "C: bánh kéo trước, caster sau":      dict(front= 0.00, rear=-0.20, cog_x=-0.05),
}
def drive_load_frac(L):
    """Phần trọng lượng trên bánh kéo (tĩnh, coi 3 điểm tựa trên một đường)."""
    if L["front"] > 0 and L["rear"] < 0:        # A: 4 điểm, bất định -> giả sử caster gánh ít
        return 0.8
    span = L["front"] - L["rear"]
    other = L["front"] if L["front"] != 0 else L["rear"]   # vị trí caster
    return abs(other - L["cog_x"]) / span
for h in (0.10, 0.20, 0.35):     # chiều cao trọng tâm: thấp / vừa / có cột loa+camera
    print(f"--- trọng tâm cao {h*100:.0f} cm ---")
    for name, L in layouts.items():
        a_tip_fwd  = G * (L["front"] - L["cog_x"]) / h   # phanh khi đi tới: chúi về trước
        a_tip_back = G * (L["cog_x"] - L["rear"]) / h    # tăng tốc tới / phanh khi lùi
        frac = drive_load_frac(L)
        a_grip = mu * G * frac                            # ma sát cho phép trên bánh kéo
        a_motor = tau_brake / r / m                       # motor phanh được bao nhiêu
        a_real = min(a_grip, a_motor)                     # cái nhỏ hơn quyết định
        flag = "LẬT" if a_real >= min(a_tip_fwd, a_tip_back) else "ổn"
        print(f"{name:38s} lật-chúi-trước {a_tip_fwd:5.1f} | lật-ngửa-sau {a_tip_back:5.1f} | "
              f"phanh thật {a_real:4.1f} m/s² (bám {a_grip:4.1f}, motor {a_motor:4.1f}) -> {flag}")
```

Rẽ gấp cũng lật được, theo cùng công thức với nửa khoảng cách bánh `b/2` thay cho d: `a_ngang_lật = g·(b/2)/h`, với gia tốc ngang `v²/R` (R bán kính rẽ). Tự thêm vào code nếu robot bạn cao và hẹp.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Quorum 3 node: số lẻ để quyết định không bị "hòa" | Ba điểm tựa: luôn xác định được tải trên mỗi điểm | Quorum là về logic đồng thuận; ba điểm tựa là về **hình học**: bốn điểm không sai về logic mà là siêu tĩnh, tải phân bố tùy độ phẳng sàn từng milimét | Thêm caster thứ hai "cho vững" → bánh kéo mất tải trên sàn gồ ghề, robot đứng quay bánh tại chỗ |
| Rate limiting để bảo vệ hệ thống khỏi burst | Giới hạn gia tốc (jerk/accel limit) trong firmware/Nav2 | Rate limit backend chỉ làm chậm; giới hạn gia tốc ở đây **mâu thuẫn trực tiếp với an toàn dừng**: dừng gấp để tránh va chạm cần gia tốc lớn, nhưng gia tốc lớn có thể làm lật | Kẹp gia tốc thật thấp cho "an toàn" → quãng dừng dài, đâm vào người; không kẹp → robot cao lật khi E-stop |
| Phân bổ tải (load balancing) đều giữa các node | Phân bố khối lượng giữa bánh kéo và caster | Đều không phải mục tiêu: bánh kéo cần **nhiều** tải để bám, caster cần ít; nhưng dồn hết lên bánh kéo thì d về phía đó tiến về 0 | Đặt pin ngay trên trục bánh kéo (bám tốt nhất) → robot ngửa ra sau khi tăng tốc mạnh |

**Chấm mô hình:**

- *"Robot nặng thì khó lật."* **SAI.** `a_lật = g·d/h` không chứa khối lượng. Phản ví dụ: thêm 2 kg pin dự phòng **ở tầng trên** làm robot nặng hơn và **dễ** lật hơn (h tăng).
- *"Trọng tâm càng thấp càng tốt, hết chuyện."* **ĐÚNG MỘT PHẦN.** Đúng về lật. Nhưng trọng tâm thấp cũng phải nằm đúng chỗ theo phương ngang (tải trên bánh kéo), và có giới hạn: pin sát sàn thì khoảng sáng gầm nhỏ, kẹt ngưỡng cửa. Phản ví dụ: robot lùn nhưng pin dồn về phía caster → bánh kéo gánh ít tải, trượt khi tăng tốc dù không bao giờ lật.
- *"Caster chỉ là bánh phụ, chọn cái nào cũng được."* **SAI.** Caster là một điểm tựa của tam giác ổn định (đặt d), và là thứ kẹt đầu tiên ở ngưỡng cửa hay dây điện trên sàn. Caster xoay còn "lật hướng" khi robot đổi chiều, đẩy robot lệch một chút (→ K7 C6.3).

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | Trọng tâm (CoG/CoM) | Điểm mà mọi trọng lượng coi như đặt vào | Tâm hình học của khung |
| 🟢 | Đa giác tựa (support polygon) | Hình nối các điểm chạm sàn; hình chiếu trọng tâm phải nằm trong | Hình chữ nhật của khung |
| 🟢 | Gia tốc lật `g·d/h` | Gia tốc ngang mà vượt qua thì robot lật quanh một cạnh tựa | Một ngưỡng "khi va chạm" — phanh bình thường cũng chạm tới |
| 🟢 | Hệ số ma sát μ | Lực bám tối đa chia cho lực pháp tuyến | C_rr ở C2.1 |
| 🟡 | Siêu tĩnh (statically indeterminate) | Nhiều điểm tựa hơn số cần, tải phụ thuộc biến dạng | "Vững hơn" |
| 🟡 | Caster offset (trail) | Khoảng lệch giữa trục xoay đứng và trục bánh caster | Lỗi chế tạo — nó là thứ làm caster tự quay theo hướng chạy |
| 🔴 | Ổn định động (ZMP), chống lật chủ động | Robot chân/xe cân bằng | — |

### 5. Dự đoán

**Đề:** với `mass_budget.csv` của bạn (Lắp bước 2) và bố trí bạn định chọn:

1. Tính trọng tâm dự kiến (x, z) từ bảng khối lượng: `x_G = Σ mᵢxᵢ / Σ mᵢ`, tương tự z.
2. Trong mô phỏng, đoán trước khi chạy: ở h = 20 cm, bố trí nào trong A, B, C "LẬT", và lật theo hướng nào?
3. Với bố trí và h của bạn: a_lật hai hướng là bao nhiêu? Gia tốc phanh thật bị giới hạn bởi bám hay bởi motor?
4. Góc lật tĩnh (nghiêng robot từ từ tới khi lật) theo mỗi hướng: `θ_lật = atan(d/h)`. Đây là số sẽ được kiểm ở Lắp bước 9.

**Tham số cần tra/đo:** `mass_budget.csv`; khoảng cách trục bánh kéo – điểm chạm caster (đo trên mô hình bìa); μ chưa đo thì 0,6 `[ước lượng]` (đo được bằng cách kéo robot với bánh **khóa** bằng cân hành lý, giống C2.1 bước 6); mô-men hãm từ listing (C2.1) hoặc từ C3.1 sau này.

```markdown
# prediction.md — K7 C2.2
commit: <hash>   bố trí: A / B / C / khác: ...
- x_G = ... m (từ trục bánh kéo, + về trước)   z_G = h = ... m   (từ mass_budget.csv)
- d_trước = ... m   d_sau = ... m
- a_lật chúi trước = ... m/s²   a_lật ngửa sau = ... m/s²
- a phanh thật = ... m/s² (bị giới hạn bởi: bám / motor)
- θ_lật tĩnh chúi trước = ...°   ngửa sau = ...°
- Mô phỏng ở h = 20 cm: lật ở bố trí ... theo hướng ...
## Tôi sẽ ngạc nhiên nếu...
```

### 6. Làm

1. Commit `prediction.md`. Chạy mô phỏng; rồi thay `layouts` bằng bố trí và trọng tâm của bạn.
2. Trên mô hình bìa (Lắp bước 3), thử ít nhất hai vị trí pin giả: thấp sát trục bánh kéo, và lệch về phía caster. Với mỗi vị trí, tính lại x_G, h và a_lật.
3. Chọn bố trí. Quy tắc gợi ý (đề xuất, không phải tiêu chí cứng): `a_lật` cả hai hướng ≥ 1,5 × gia tốc phanh thật lớn nhất `[ước lượng — hệ số an toàn]`; nếu không đạt, ghi giới hạn gia tốc phanh cần đặt ở firmware vào `decisions.md` để C4.4 dùng.
4. Kiểm ba điểm tựa: nếu chọn 4 điểm, ghi cách bảo đảm bánh kéo luôn chạm (caster lò xo, khe chỉnh) và kiểm bằng tờ giấy ở Lắp bước 5c trên **ba** vị trí sàn khác nhau.
5. Ghi bố trí cuối, x_G, h dự kiến vào `hw/robot_params.yaml` với `method: estimated_from_mass_budget` (C2.4 sẽ thay bằng số cân).

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

| h | A (kéo giữa, 2 caster) | B (kéo sau, caster trước) | C (kéo trước, caster sau) |
|---|---|---|---|
| 10 cm | ổn (a_lật 11,8 hai hướng) | ổn (a_lật ngửa sau 4,9 > phanh 4,4) | ổn (a_lật chúi trước 4,9 > 4,4) |
| 20 cm | ổn (5,9 > 4,7) | **LẬT ngửa sau** (2,5) khi phanh lúc lùi hoặc tăng tốc mạnh lúc tới | **LẬT chúi trước** (2,5) khi phanh lúc tới |
| 35 cm | LẬT (3,4) | LẬT | LẬT |

- Ở mọi dòng, gia tốc phanh thật bị giới hạn bởi **bám** (4,4–4,7 m/s²), không phải motor (5,5). Nghĩa là robot sẽ trượt bánh trước khi motor phanh hết sức; với robot thấp đó là chế độ hỏng "an toàn", với robot cao thì không cứu được.
- Hướng nguy hiểm là hướng có **d nhỏ**: phía bánh kéo khi trọng tâm đặt gần trục bánh kéo. B và C là đối xứng gương của nhau.
- A trông tốt nhất trên giấy nhưng chính là bố trí 4 điểm (siêu tĩnh). Con số 0,8 tải trên bánh kéo trong code là **giả định**, không phải kết quả.
- Mô-men phanh lấy bằng mô-men hãm là trường hợp xấu nhất: phanh ngắn mạch ở tốc độ v cho mô-men xấp xỉ tỉ lệ `v / v_không_tải` (C3.2). Ở 0,5 m/s với motor không tải ~0,8 m/s, khoảng 60% con số trên.
- Robot confession có loa và camera trên cột: trọng tâm 30–35 cm là thực tế `[ước lượng]`. Khi đó giới hạn gia tốc phanh trong firmware (C4.4) không còn là tùy chọn.
- Góc lật tĩnh `atan(d/h)` thường ra 30–60° cho robot thấp; nếu bạn dự đoán dưới 20° thì kiểm lại h.

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Trọng tâm tính từ bảng lệch xa trọng tâm cân ở C2.4 | Món chưa cân (dây, vít, đai); z của món đoán sai | Cộng `mass_budget.csv` so với cân tổng | Cân bổ sung; ghi `source=measured` |
| Robot khó lật trên giấy nhưng bánh kéo trượt khi khởi hành | Tải trên bánh kéo thấp (trọng tâm gần caster) | Cân ba điểm (C2.4) | Dời pin về phía trục bánh kéo |
| Robot rung lắc "bập bênh" khi chạy qua mối nối gạch | Bố trí 4 điểm | Tờ giấy ở nhiều vị trí | Bỏ một caster hoặc thêm lò xo |
| Caster kẹt ở ngưỡng cửa | Caster nhỏ; khoảng sáng gầm thấp | Đo chiều cao ngưỡng | Caster to hơn; chạy qua ngưỡng theo hướng bánh kéo đi trước |

### 9. Câu hỏi ngược

1. **[Nếu…thì]** Nếu E-stop (C10.1) cắt nguồn động lực và motor chuyển sang trôi tự do (coast), còn firmware phanh chủ động bằng ngắn mạch, thì chế độ nào nguy hiểm về lật hơn, chế độ nào nguy hiểm về va chạm hơn?
<details><summary>Hướng nghĩ</summary>

Coast: gia tốc nhỏ (chỉ ma sát), không lật, nhưng quãng dừng dài. Phanh ngắn mạch: dừng nhanh, gia tốc lớn. An toàn không phải một trục; ghi đánh đổi này vào `decisions.md` để C10 dùng.

</details>

2. **[Quy mô]** Một đội 50 robot cùng thiết kế nhưng mỗi robot gắn phụ kiện khác nhau (khay, cột màn hình). Bạn quản lý rủi ro lật thế nào mà không phải tính tay 50 lần?
<details><summary>Hướng nghĩ</summary>

`mass_budget.csv` theo cấu hình + script tính a_lật chạy trong CI mỗi khi cấu hình đổi; giới hạn gia tốc trong firmware đọc từ tham số theo cấu hình. Đó là "config validation" có vật lý bên trong.

</details>

3. **[Failure mode]** Liệt kê hai cách trọng tâm robot **di chuyển** trong lúc chạy mà bảng khối lượng tĩnh không thấy.
<details><summary>Hướng nghĩ</summary>

Pin trượt trong gá khi phanh; cột camera rung/uốn; người đặt đồ lên robot. Gá pin bằng đai + chặn cơ khí chính là để trọng tâm không di chuyển.

</details>

4. **[Vì sao không]** Vì sao không đặt luôn pin sát sàn, thấp nhất có thể?
<details><summary>Hướng nghĩ</summary>

Khoảng sáng gầm (ngưỡng cửa, dây trên sàn), vị trí ngang (tải trên bánh kéo), tiếp cận để tháo pin khi sự cố (C1.6). Thấp là một trong nhiều ràng buộc, không phải mục tiêu duy nhất.

</details>

### 10. Liên kết ra ngoài

- **Xe nâng và tam giác ổn định** (câu chuyện): giống hệt hình học. Khác: xe nâng có tải **thay đổi độ cao** liên tục, người lái được đào tạo; robot có firmware, nên quy tắc phải được viết thành giới hạn số.
- **Xe SUV và bài thử "moose test" (né tránh đột ngột):** xe trọng tâm cao lật khi đổi hướng gấp, cùng công thức `g·(b/2)/h`. Ngành ô tô giải bằng điều khiển ổn định điện tử (giảm mô-men, phanh từng bánh): đúng hướng của C4.4 là kẹp gia tốc ở tầng thấp nhất.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| `a_lật = g·d/h` | [chuẩn] | Cân bằng mô-men tĩnh; bỏ qua chuyển tải động và đàn hồi bánh |
| μ cao su–gạch ≈ 0,6 | [ước lượng] | Đo bằng kéo với bánh khóa |
| Tải bánh kéo 0,8 ở bố trí 4 điểm | [ước lượng] | Giả định cho mô phỏng; thực tế phụ thuộc độ phẳng sàn |
| Phanh ngắn mạch cho mô-men cỡ mô-men hãm ở tốc độ không tải | [chuẩn] | C3.2 mô phỏng; tỉ lệ với tốc độ |
| Lật là nguyên nhân hàng đầu của tử vong liên quan xe nâng | [chuẩn] | Tài liệu OSHA về xe nâng |

**Đã sửa so với bản gốc:** K7 gốc không có bài về bố trí khối lượng; bài mới.

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** OSHA, tài liệu "Powered Industrial Trucks" (eTool forklift), phần ổn định.
- **Giải thích:** Siegwart, Nourbakhsh & Scaramuzza, *Introduction to Autonomous Mobile Robots* — phần ổn định của robot có bánh.
- **Tự kiểm tra:** (1) giải thích trong 5 câu vì sao khối lượng không nằm trong công thức lật; (2) vẽ lại hình phần 2; (3) câu dưới.

  Robot h = 25 cm, caster trước cách trọng tâm 15 cm theo phương ngang. Phanh 3 m/s² khi đi tới có lật không?
  <details><summary>Đáp án</summary>

  a_lật = 9,81 × 0,15 / 0,25 ≈ 5,9 m/s² > 3 → không lật quanh caster trước. Còn phải kiểm hướng kia (tăng tốc, phanh lúc lùi) với d phía bánh kéo.

  </details>

---

## Bài C2.3 — Gá lắp: vít, ốc khóa, rung, standoff, strain relief (4h)

> **Vị trí:** C2.2 → **C2.3** → C2.4 · **Cần trước:** C0.3 (dụng cụ tay), C2.2 · **Sau bài này bạn quyết định được:** với mỗi mối ghép trên robot, dùng vít dài bao nhiêu, cần đai ốc khóa nylon, keo khóa ren, hay chỉ siết đúng; standoff kim loại hay nylon; và dây buộc ở đâu để lực kéo không đi vào đầu cắm.

### 1. Câu chuyện — ai đã khổ vì chuyện này

Năm 1969, kỹ sư Đức Gerhard Junker công bố thí nghiệm cho thấy mối ghép bu lông tự lỏng chủ yếu vì **rung theo phương ngang** (vuông góc trục vít): mỗi lần hai tấm trượt nhẹ lên nhau, ren cũng trượt và vít xoay ngược một chút. Máy thử Junker trở thành phép thử chuẩn cho các giải pháp chống lỏng, và kết quả nổi tiếng nhất của nó là **long đen vênh (lò xo) hầu như không giúp gì** dưới rung ngang `[chuẩn — Junker 1969; NASA Fastener Design Manual (RP-1228) cũng ghi long đen vênh không hiệu quả chống lỏng]`. Năm 1981, sảnh khách sạn Hyatt Regency ở Kansas City sập lối đi treo, 114 người chết; nguyên nhân là một thay đổi **chi tiết ghép nối** (thanh treo liền bị đổi thành hai thanh, làm đai ốc và dầm hộp phía trên gánh gấp đôi tải) `[chuẩn — điều tra NBS 1982]`. Hai câu chuyện cùng một bài: mối ghép là đường đi của lực, không phải chi tiết phụ.

Robot của bạn rung liên tục (motor, hộp số, mối nối gạch). Một vít gá motor lỏng làm bánh chụm lại vài phần mười độ, odometry lệch (C6), và không có log nào báo.

### 2. Mô hình tư duy

```
  MỐI GHÉP VÍT = MỘT LÒ XO ĐƯỢC KÉO CĂNG
     ┌──┐ đầu vít            Siết vít = kéo dãn thân vít (vài µm) → lực kẹp (preload) ép hai tấm.
  ═══╪══╪═══ long đen         Ma sát giữa hai tấm (do lực kẹp) chịu lực ngang.
  ▓▓▓▓│  │▓▓▓ tấm 1           Lực ngang > ma sát  → hai tấm trượt → ren trượt → vít xoay lỏng dần
  ▓▓▓▓│  │▓▓▓ tấm 2           (Junker). Mất lực kẹp → trượt nhiều hơn → vòng lặp dương.
  ═══╪══╪═══ long đen
     ╞══╡ đai ốc (M3: cao 2,4 mm, ISO 4032)
      ╧╧  ≥ 2 bước ren lòi ra (M3: bước 0,5 mm)
  Chiều dài vít tối thiểu = tổng chiều dày tấm + long đen + chiều cao đai ốc + 2 bước ren
  Vít vào lỗ ren (không đai ốc): ăn ren ≥ 1–1,5 × đường kính vào kim loại; nhiều hơn vào nhựa/gỗ
```

| Cách chống lỏng | Cơ chế | Chống **mất lực kẹp**? | Chống **rơi hẳn**? | Dùng ở robot của bạn |
|---|---|---|---|---|
| Siết đúng (đủ preload) | Ma sát giữ hai tấm không trượt | Có, nếu đủ | Gián tiếp | Mọi mối, luôn |
| Keo khóa ren trung bình (Loctite 243) | Keo kỵ khí đóng rắn trong khe ren, khóa ren | Có | Có | Kim loại vào kim loại: gá motor vào mặt hộp số, vít trí bánh |
| Đai ốc khóa nylon (nyloc) | Vòng nylon kẹp ren, tạo mô-men cản | Không nhiều | Có | Mối có đai ốc qua tấm gỗ/nhựa; caster |
| Long đen vênh | Lò xo nhỏ | Hầu như không (Junker) | Hầu như không | Không dựa vào nó |
| Long đen phẳng | Rải lực, bảo vệ bề mặt | Gián tiếp (giảm lún) | Không | Dưới đầu vít và đai ốc trên gỗ/nhôm mềm |
| Vạch sơn đánh dấu (torque stripe) | Không chống gì; **cho thấy** vít đã xoay | — | — | Mọi mối quan trọng |

Ba câu bản chất:

1. **Vít giữ được vì nó là lò xo đang căng.** Lực kẹp chứ không phải "độ chặt của ren" giữ hai tấm. Siết quá thì đứt vít/toét ren/nứt tấm; siết thiếu thì tấm trượt và vít tự lỏng.
2. **Rung ngang là kẻ thù; mọi biện pháp khác là phụ.** Chặn trượt ngang (chốt, cữ, lỗ khít) giúp nhiều hơn mọi loại long đen.
3. **Đầu cắm điện không phải điểm neo cơ khí.** Lực kéo trên dây phải đi vào một điểm buộc chắc **trước** đầu cắm (strain relief); đầu cắm chỉ mang điện. Thiếu điều này, chân đầu cắm hoặc mối bấm (C0.3) gãy dần sau hàng nghìn lần rung.

**Standoff kim loại hay nylon:** đo bằng thông mạch giữa lỗ bắt vít của bo mạch và chân GND. Lỗ nối GND + standoff đồng + khung nhôm = khung thành GND của bo đó; hai bo như vậy trên cùng khung nhôm là một đường GND song song ngoài ý muốn (→ K7 C5.1 quyết định nối khung thế nào). Chưa quyết thì dùng **nylon** cho bo mạch, kim loại cho tầng khung.

**Strain relief, bốn quy tắc:** (1) buộc dây vào khung bằng dây rút qua đế **bắt vít** (đế dán bong khi nóng) cách đầu cắm 3–5 cm; (2) chừa vòng dư (service loop) để tháo đầu cắm không phải cắt dây rút; (3) dây không được căng qua chỗ có chuyển động (bánh, caster): khoảng hở ≥ vài cm ở mọi góc xoay caster; (4) mọi lỗ xuyên tấm có grommet; dây rút siết vừa, không cắt vào vỏ dây.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Config drift: server lệch dần khỏi trạng thái khai báo | Vít tự lỏng dưới rung | Drift ở server phát hiện được bằng diff tự động. Vít lỏng không có "diff" nào ngoài mắt người, trừ khi bạn **cố ý tạo dấu**: vạch sơn là checksum vật lý | Không đánh dấu → phát hiện vít lỏng khi bánh đã chụm, odometry đã trôi hàng tuần |
| Không cho client gọi thẳng DB; đi qua một tầng chịu tải | Không để lực kéo dây đi thẳng vào đầu cắm; đi qua điểm buộc | Tầng trung gian backend có thể scale; điểm buộc có giới hạn cơ học cố định và chính nó cũng cần kiểm (dây rút giòn theo thời gian, nhiệt) | Đầu JST gánh lực → mối bấm gãy âm thầm, encoder mất kênh lúc có lúc không |

**Chấm mô hình:** *"Bản chất ngành hardware là luôn có buffer ở giữa để kiểm soát ổn định và tradeoff"* (mô hình của bạn ở K3 lượt 6, nói về buffer dữ liệu). Áp sang cơ khí: vòng dư dây, đệm cao su, khe hở là "buffer" cho chuyển vị. **ĐÚNG MỘT PHẦN.** Đúng là cơ khí cũng dùng phần tử hấp thụ (đệm, lò xo, vòng dư) để tách hai bên có chuyển động khác nhau. Gãy ở chỗ: buffer cơ khí **có hại khi đặt sai chỗ**. Phản ví dụ: đệm cao su dưới gá motor làm motor lắc theo mô-men → bánh đổi góc mỗi lần tăng tốc → odometry sai; ở chỗ truyền lực bạn cần **cứng**, không cần buffer. Quy tắc: cứng trên đường truyền lực và đường đo (motor, encoder, camera ở C7.1), mềm trên đường dây và chỗ cần cách ly rung (mini PC nếu cần).

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | Lực kẹp (preload) | Lực căng trong thân vít sau khi siết, ép hai chi tiết | "Độ chặt" của ren |
| 🟢 | Nyloc | Đai ốc có vòng nylon tạo mô-men cản | Thứ giữ lực kẹp — nó chỉ chống rơi hẳn |
| 🟢 | Keo khóa ren (kỵ khí) | Đóng rắn khi không có không khí và có kim loại | Keo dán đa năng |
| 🟢 | Strain relief, service loop | Điểm neo cơ khí cho dây; đoạn dây dư để tháo lắp | Dây rút ở bất kỳ đâu |
| 🟡 | Standoff | Trụ ren nâng bo mạch/tầng | Chi tiết cơ khí thuần — kim loại thì dẫn điện |
| 🔴 | Tính mô-men siết theo cấp bền, hệ số ma sát ren | Kỹ sư cơ khí | — |

### 5. Dự đoán

**Đề:** thí nghiệm lỏng vít ở bước 3 phần Làm (4 mẫu: a thiếu lực kẹp, b siết đúng, c siết đúng + nyloc, d siết đúng + long đen vênh, mỗi mẫu 200 lần lắc ngang). Xếp hạng bốn mẫu theo góc xoay vạch sơn, từ nhiều nhất tới ít nhất; đoán mẫu nào xoay **hơn 90°**. Đoán thêm: tổng số vít/đai ốc trên robot của bạn, và bao nhiêu mối cần keo.

```markdown
# prediction.md — K7 C2.3
commit: <hash>
- Xếp hạng xoay nhiều → ít: ... > ... > ... > ...
- Mẫu xoay > 90°: ...
- Số mối ghép: ...   cần keo: ...   cần nyloc: ...
## Tôi sẽ ngạc nhiên nếu...
```

### 6. Làm

1. **Bảng mối ghép:** liệt kê mọi mối ghép trên bản vẽ mô hình bìa: `joint_id, vật liệu hai bên, vít (M?, dài), đai ốc/lỗ ren, chống lỏng, chịu lực gì`. Tính chiều dài vít theo công thức ở phần 2, chọn cỡ có sẵn gần nhất **lớn hơn**, kiểm đầu vít không chĩa vào vùng pin.
2. **Luyện trên phế liệu (theo mục 3 của chặng):** 10 vít vào gỗ thừa bằng máy có ly hợp, siết tay lần cuối; 2 vít + keo khóa ren vào đai ốc; 2 nyloc. Cắt đôi một mối gỗ đã siết quá để thấy thớ gỗ bị nghiền.
3. **Thí nghiệm lỏng vít (30 phút):** hai thanh nhôm/gỗ bắt bằng một vít M3 + đai ốc thường, siết tay vừa chạm (thiếu preload). Đánh vạch sơn. Kẹp một thanh vào bàn, gõ/lắc thanh kia **ngang** 200 lần. Lặp với (b) siết đúng, (c) siết đúng + nyloc, (d) siết đúng + long đen vênh. Chụp vạch sơn. Ghi góc xoay ước lượng của mỗi mẫu.
4. Lắp thật (Lắp bước 5–7 của chặng) theo bảng mối ghép. Đánh vạch sơn mọi vít gá motor, bánh, caster, standoff tầng.
5. Sau Lắp bước 9 (thử nghiêng, thử đẩy): kiểm lại mọi vạch sơn; ghi số vạch bị lệch vào `measurements.jsonl` (`quantity: fastener_moved`).

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

- Mẫu (a) thiếu lực kẹp xoay nhiều nhất, thường thấy rõ sau vài chục lần lắc. Mẫu (d) long đen vênh **không** khá hơn (b) rõ rệt; nếu bạn xếp (d) tốt nhì là bạn đã tin vào long đen vênh như nhiều người. (b) và (c) xoay ít; (c) nếu có xoay thì đai ốc vẫn không rơi.
- Thí nghiệm tay này thô (lực lắc không đều), nên chỉ tin **thứ hạng lớn**, không tin chênh lệch vài độ. Phép thử Junker thật dùng máy tạo dịch chuyển ngang có biên độ xác định.
- Robot cỡ này thường có 60–100 vít/đai ốc `[ước lượng]`; mối cần keo là kim loại vào kim loại chịu rung (gá motor, vít trí bánh), thường dưới 15.

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Vạch sơn lệch sau vài giờ | Thiếu preload; trượt ngang | Lắc tay thấy rơ | Siết lại đúng; thêm keo (kim loại) hoặc nyloc; chặn trượt ngang |
| Ren đai ốc nyloc "trơn" sau 2–3 lần tháo | Vòng nylon mòn | Mô-men vặn đai ốc lên rất nhẹ | Thay đai ốc mới; nyloc nên coi là dùng một lần `[chuẩn]` |
| Keo khóa ren không đóng rắn | Ren dính dầu; vật liệu không kim loại (keo kỵ khí cần ion kim loại) `[spec — Henkel TDS]` | Sau 24 h vít vẫn xoay dễ | Lau ren bằng cồn; dùng primer hoặc đổi sang nyloc |
| Mica/nhựa trong nứt quanh vít có keo | Keo khóa ren làm nứt ứng suất (stress crazing) nhựa acrylic/polycarbonate `[spec — Henkel cảnh báo trên TDS]` | Nhìn vết nứt hình tia | Thay tấm; với nhựa dùng nyloc |
| Encoder lúc có lúc không khi chạm dây | Mối bấm/đầu cắm gánh lực | Lắc dây gần đầu cắm, nhìn PulseView (C3.3) | Strain relief đúng quy tắc 1 |

### 9. Câu hỏi ngược

1. **[Vì sao không]** Vì sao không dùng keo khóa ren cho **mọi** vít, cho chắc?
<details><summary>Hướng nghĩ</summary>

Nghĩ về: tháo bảo trì (C10 soak sẽ cần), vật liệu không tương thích (nhựa), keo chảy vào nơi không muốn (ổ bi, khớp quay), và việc keo che giấu một mối ghép thiếu preload.

</details>

2. **[Quy mô]** 100 robot, mỗi robot 60 vít, rung 8 giờ/ngày. Bạn thiết kế quy trình kiểm tra định kỳ thế nào để không tốn 6000 lần kiểm?
<details><summary>Hướng nghĩ</summary>

Phân hạng mối ghép theo hậu quả (gá motor, caster: hạng A; nắp che: hạng C); vạch sơn + ảnh chụp tự động so sánh; dữ liệu odometry (UMBmark trôi theo thời gian) làm cảm biến gián tiếp cho gá motor lỏng. Đó là giám sát dựa trên rủi ro, giống phân hạng SLO.

</details>

3. **[Failure mode]** Kể một cách strain relief **gây** hỏng thay vì ngăn.
<details><summary>Hướng nghĩ</summary>

Dây rút siết quá cắt vào vỏ dây theo thời gian → chạm khung nhôm; điểm buộc quá gần đầu cắm, dây bị bẻ gập ngay tại mối bấm; vòng dư quá dài cuốn vào bánh.

</details>

4. **[Liên ngành]** Ngành hàng không dùng vít có dây khóa (safety wire) và chốt chẻ cho mối quan trọng. Nó khác keo khóa ren ở điểm nào về khả năng **kiểm tra bằng mắt**?
<details><summary>Hướng nghĩ</summary>

Dây khóa nhìn thấy được trạng thái từ xa; keo thì không. Kiểm tra được là một thuộc tính thiết kế, giống observability.

</details>

### 10. Liên kết ra ngoài

- **Xe tải: chỉ thị đai ốc bánh xe (wheel nut indicator).** Một mũi nhựa gắn trên mỗi đai ốc, cùng chỉ một hướng khi siết đúng; tài xế nhìn lướt là thấy đai ốc nào đã xoay. Giống vạch sơn của bạn. Khác: có ngưỡng nhìn rõ và quy trình kiểm trước mỗi chuyến.
- **Hàng không: dây khóa an toàn (safety wire)** ở câu hỏi 4: chống lỏng **và** kiểm được bằng mắt.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| Lỏng vít chủ yếu do rung ngang; long đen vênh hầu như vô dụng | [chuẩn] | Junker 1969; NASA RP-1228 |
| Keo kỵ khí cần kim loại, làm nứt acrylic/polycarbonate | [spec] | Henkel TDS và hướng dẫn tương thích nhựa |
| Nyloc nên coi là dùng một lần | [chuẩn] | Thực hành phổ biến; NASA RP-1228 nói về giảm mô-men cản sau mỗi lần dùng |
| M3: đai ốc cao 2,4 mm, bước 0,5 mm; lỗ lọt 3,2–3,4 mm | [chuẩn] | ISO 4032, ISO 261, ISO 273 |
| Hyatt Regency 1981: đổi chi tiết thanh treo làm gấp đôi tải lên mối ghép | [chuẩn] | Báo cáo NBS 1982 |
| "Siết chạm + 1/8–1/4 vòng" cho M3 | [ước lượng] | Quy tắc tay, không thay cờ lê lực |

**Đã sửa so với bản gốc:** K7 gốc không có nội dung gá lắp; bài mới.

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** NASA, *Fastener Design Manual* (Barrett, NASA RP-1228, 1990); Henkel/Loctite, Technical Data Sheet của loại keo bạn mua.
- **Giải thích:** NASA RP-1228 phần chống lỏng; tài liệu về phép thử Junker (DIN 65151 là tiêu chuẩn phép thử rung ngang `[spec — kiểm tên tiêu chuẩn]`).
- **Tự kiểm tra:** (1) giải thích trong 5 câu vì sao long đen vênh không chống lỏng dưới rung ngang; (2) vẽ lại mối ghép lò xo từ trí nhớ; (3) câu dưới.

  Gá motor: tấm ván 6 mm + gá thép 2 mm + long đen 0,5 mm mỗi bên, đai ốc M3. Vít M3 dài tối thiểu?
  <details><summary>Đáp án</summary>

  6 + 2 + 2 × 0,5 + 2,4 + 2 × 0,5 = 12,4 mm → chọn M3×14 hoặc M3×16 (kiểm đầu thừa không chạm gì).

  </details>

---

## Bài C2.4 — Đo và cân robot: tham số hình học đầu tiên cho sim (5h)

> **Vị trí:** C2.3 → **C2.4** → C3; dùng ở → K7 C6.1 (động học), C6.2 (UMBmark hiệu chuẩn tiếp), C11.1 (model sim) · **Cần trước:** → F1.1 (độ bất định, lan truyền sai số); đọc kèm → F6.4 · **Sau bài này bạn quyết định được:** con số hình học nào đủ tin để đưa vào sim và động học, con số nào phải hiệu chuẩn bằng chuyển động (C6.2), và phép đo nào cần làm lại khi đổi phần cứng.

### 1. Câu chuyện — ai đã khổ vì chuyện này

Năm 1999, tàu Mars Climate Orbiter mất khi vào quỹ đạo sao Hỏa. Ban điều tra của NASA kết luận phần mềm mặt đất của một nhà thầu xuất xung lực đẩy theo đơn vị lbf·s, trong khi phần mềm điều hướng dùng nó như N·s; sai số tích lũy qua nhiều lần hiệu chỉnh quỹ đạo đưa tàu xuống quá thấp `[chuẩn — Mars Climate Orbiter Mishap Investigation Board, Phase I Report, 1999]`. Một file tham số chuyển từ hệ này sang hệ khác mà **không mang theo đơn vị và nguồn gốc**.

`robot_params.yaml` của bạn sẽ đi đúng con đường đó: từ thước kẹp và cân bếp, vào động học ở C6, vào sim ở C11. Bài này làm cho mỗi con số mang theo ba thứ: đơn vị, cách đo, và độ bất định.

### 2. Mô hình tư duy

| Tham số | Ký hiệu | Đo bằng | Độ bất định điển hình `[ước lượng]` | Ai dùng | Hiệu chuẩn tiếp ở |
|---|---|---|---|---|---|
| Khối lượng | m | 3 cân cộng lại | vài g | sim (C11.1), C2.1 | — |
| Trọng tâm ngang | x_G, y_G | cân bằng mô-men 3 cân | vài mm | sim, C2.2 | — |
| Chiều cao trọng tâm | h | phép nghiêng (code dưới) | vài mm nếu nghiêng đủ | sim, chống lật | góc lật tĩnh (Lắp bước 9) |
| Đường kính bánh hiệu dụng | D_T, D_P | lăn có tải 5 m, đếm vòng | ~0,1% | C6.1 | C6.2 (UMBmark) |
| Khoảng cách bánh | b | thước giữa tâm vết bánh | 1–2 mm (vết bánh rộng) | C6.1 | C6.2 (UMBmark) |
| Vị trí caster | x_c | thước | vài mm | sim | — |
| Quán tính quay quanh trục đứng | I_z | con lắc hai dây (tùy chọn) | ~5–10% | sim | C11.1 |

Bốn câu bản chất:

1. **Tham số là một phép đo, không phải một hằng số.** Nó có phương pháp, thời điểm, và sai số. Đường kính in trên bánh "85 mm" là danh nghĩa; bánh cao su **có tải** lăn với đường kính hiệu dụng nhỏ hơn.
2. **Đo cái ảnh hưởng tới hành vi, theo cách hành vi dùng nó.** Đường kính hiệu dụng đo bằng **lăn** dưới tải, không đo bằng thước kẹp ở bánh treo.
3. **Có tham số đo tĩnh đủ tốt, có tham số chỉ hiệu chuẩn được bằng chuyển động.** Khoảng cách bánh "hiệu dụng" phụ thuộc vết tiếp xúc bánh trên sàn; số đo thước là điểm khởi đầu, UMBmark ở C6.2 cho số cuối.
4. **Phép đo gián tiếp khuếch đại sai số.** h suy từ chênh lệch nhỏ giữa hai số cân chia cho `tanθ` nhỏ; nghiêng ít quá thì sai số cân lấn tín hiệu (→ F1.1, lan truyền sai số).

**Mô phỏng: trọng tâm từ ba cân, chiều cao từ phép nghiêng, và nghiêng bao nhiêu là đủ.** Phép nghiêng: robot đặt hai bánh kéo trên hai cân, caster trên cân thứ ba; kê caster (cùng cân của nó) cao thêm dz; tổng hai cân bánh kéo tăng lên vì trọng tâm dịch về phía thấp.

```python
# [đã chạy] Trọng tâm từ cân: vị trí ngang từ 3 cân, chiều cao từ phép nghiêng + độ bất định
import numpy as np
from scipy.optimize import brentq
rng = np.random.default_rng(1)
# Điểm chạm (m) trong base_link (gốc dưới trục bánh kéo): bánh trái, bánh phải, caster
P = np.array([[0.0, +0.10], [0.0, -0.10], [0.20, 0.0]])
W = np.array([2.10, 2.02, 1.30])            # kg đọc trên 3 cân (số ví dụ)
m = W.sum()
x_g, y_g = (W[:, None] * P).sum(0) / m      # cân bằng mô-men quanh hai trục
print(f"m = {m:.2f} kg, trọng tâm x = {x_g*1000:.0f} mm, y = {y_g*1000:+.0f} mm")
# Phép nghiêng: kê caster cao thêm dz, đọc lại tổng hai cân bánh kéo.
r, rc, Lc = 0.0425, 0.025, 0.20             # bán kính bánh kéo, bánh caster, khoảng trục–caster
zc = rc - r                                 # độ cao trục caster so với trục bánh kéo
def theta_of(dz):                           # góc thân khi caster được kê cao dz
    return brentq(lambda t: Lc*np.sin(t) + zc*(np.cos(t) - 1) - dz, 0, 1.2)
def caster_load(th, zg):                    # zg: độ cao trọng tâm trên TRỤC bánh kéo
    return m * (x_g*np.cos(th) - zg*np.sin(th)) / (Lc*np.cos(th) - zc*np.sin(th))
def zg_from(Wc, th):                        # giải ngược từ số cân caster
    return (x_g*np.cos(th) - Wc*(Lc*np.cos(th) - zc*np.sin(th))/m) / np.sin(th)
h_true = 0.12                               # chiều cao thật trên SÀN (chỉ để mô phỏng)
res_w, res_dz = 0.01, 0.001                 # cân 10 g, thước 1 mm
for dz in (0.02, 0.05, 0.10):
    th = theta_of(dz)
    Wd = m - caster_load(th, h_true - r)    # tổng hai cân bánh kéo khi nghiêng
    n = 20000                               # Monte Carlo: sai số cân + sai số đo dz
    Wd_n = Wd + rng.uniform(-res_w, res_w, (2, n)).sum(0)
    th_n = np.array([theta_of(d) for d in dz + rng.uniform(-res_dz, res_dz, n)])
    h = zg_from(m - Wd_n, th_n) + r         # đổi về độ cao trên sàn
    lo, hi = np.percentile(h, [2.5, 97.5])
    print(f"kê {dz*100:3.0f} cm (θ={np.degrees(th):4.1f}°): bánh kéo tăng "
          f"{(Wd-(m-W[2]))*1000:5.0f} g -> h = {np.median(h)*1000:5.1f} mm, "
          f"95%: [{lo*1000:5.1f}, {hi*1000:5.1f}]")
```

Code giả định bánh kéo và bánh caster tròn, điểm chạm luôn nằm ngay dưới trục, và caster không xoay khi nghiêng (khóa hướng caster bằng băng dính). Sai số cân lấy 10 g cho cân hành lý/cân rẻ; cân bếp 1 g cho kết quả tốt hơn — đổi `res_w` để thấy.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| File config có schema, validate ở CI | `robot_params.yaml` có `value, unit, std, method, measured_at` | Config backend đúng hay sai là nhị phân. Tham số vật lý luôn "sai một ít"; câu hỏi là sai bao nhiêu và hành vi nhạy bao nhiêu với nó | Ghi `wheel_diameter: 0.085` không sai số → C6 hiệu chuẩn ra 0,0838, không ai biết đó là sửa lỗi hay là trôi |
| Reconciliation: hai nguồn số độc lập phải khớp | Tổng `mass_budget.csv` vs cân tổng; h từ bảng vs h từ nghiêng vs góc lật tĩnh | Reconciliation tài chính khớp tới đồng. Ở đây khớp "trong sai số": phải biết sai số mới nói được là khớp | Thấy lệch 30 g, sửa bảng cho khớp → giấu một món chưa cân |
| Golden file cho test | Góc lật tĩnh đo được là golden value cho model sim | Golden file backend sinh lại được từ code. Golden value vật lý chỉ có được bằng đo lại; robot đổi phần cứng thì nó hết hạn | Giữ golden value cũ sau khi thêm loa → test sim "pass" trên một robot không còn tồn tại |

**Chấm mô hình:** *"Đo một lần thật cẩn thận là xong, sim cứ thế dùng."* **ĐÚNG MỘT PHẦN.** Đúng với khối lượng và vị trí caster (ổn định). Sai với đường kính bánh hiệu dụng (đổi theo tải, mòn, áp lực bánh) và khoảng cách bánh hiệu dụng (đổi theo sàn). Phản ví dụ: đo D lúc pin giả 1 kg, sau đó lắp pin thật 1,4 kg và loa: bánh cao su lún thêm, D hiệu dụng giảm, odometry ngắn đi một tỉ lệ không đổi — đúng loại sai số hệ thống C6.2 tìm thấy.

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | Đường kính hiệu dụng (effective rolling diameter) | Quãng đường mỗi vòng chia π, đo khi lăn có tải | Đường kính in trên bánh |
| 🟢 | Khoảng cách bánh (track width) b | Khoảng giữa hai điểm tiếp xúc bánh kéo | Chiều rộng khung |
| 🟢 | Độ bất định 1σ (`std`) | Độ lệch chuẩn ước lượng của sai số (→ F1.1) | Phân giải của dụng cụ |
| 🟡 | Mô-men quán tính I_z | "Khối lượng" đối với chuyển động quay | Tính được từ khối lượng là xong |
| 🟡 | URDF | Định dạng mô tả robot của ROS (link, joint, khối lượng, quán tính) | Chỉ để vẽ robot trong RViz |
| 🔴 | Tensor quán tính đầy đủ (Ixy, Ixz…) | Cần cho robot 3D phức tạp | — |

### 5. Dự đoán

**Đề:**
1. Tổng ba cân so với tổng `mass_budget.csv`: lệch bao nhiêu, theo hướng nào? (món nào bạn đã quên cân?)
2. x_G, y_G từ ba cân so với dự kiến ở C2.2.
3. Chạy mô phỏng **trước khi** nghiêng robot thật: kê caster bao nhiêu cm thì khoảng 95% của h hẹp dưới ±5 mm với cân của bạn?
4. D hiệu dụng so với đường kính danh nghĩa: lớn hơn, nhỏ hơn, bao nhiêu phần trăm?
5. Góc lật tĩnh hai hướng từ h đo được: `θ = atan(d/h)`.

**Phương pháp:** lan truyền sai số kiểu B (→ F1.1): cân phân giải q có sai số đều ±q/2… ±q tùy cách đọc; thước 1 mm; đếm vòng ±3° vạch.

```markdown
# prediction.md — K7 C2.4
commit: <hash>   cân: <model, phân giải>   thước: <loại>
- m (3 cân) = ... kg   tổng mass_budget = ... kg   lệch dự đoán = ... (vì ...)
- x_G = ... mm   y_G = ... mm
- kê caster dz = ... cm để h có 95% ±5 mm
- h dự đoán = ... mm (từ mass_budget)
- D hiệu dụng / D danh nghĩa = ... %
- θ lật tĩnh: chúi trước ...°, ngửa sau ...°
## Tôi sẽ ngạc nhiên nếu...
```

### 6. Làm

1. **Kiểm cân:** cân cùng một vật (chai nước) trên cả ba cân; ghi lệch giữa các cân vào `instruments.jsonl` (C0.5). Đặt ba cân trên sàn phẳng; kê đệm để mặt ba cân cùng độ cao (kiểm bằng thước thủy hoặc ứng dụng điện thoại).
2. **Cân ba điểm:** đặt mỗi bánh kéo giữa một cân, caster trên cân thứ ba (khóa hướng caster). Đọc 3 lần, mỗi lần nhấc robot lên đặt lại; ghi cả 9 số. Đo tọa độ các điểm chạm bằng thước (trục bánh kéo là gốc `base_link`, `x` tới trước, `y` sang trái — REP-103).
3. **Nghiêng:** kê cân caster lên khối gỗ cao dz bạn đã chọn ở dự đoán 3; đọc lại hai cân bánh kéo (3 lần). Có người giữ hờ phía trên. Tính h bằng các hàm trong code (thay số của bạn).
4. **Đường kính hiệu dụng:** robot đủ tải (pin giả đúng khối lượng), dán vạch băng dính trên mỗi bánh và trên sàn; đẩy robot thẳng **chậm** đúng 10 vòng bánh trái, đo quãng đường bằng thước dây (±2 mm); lặp cho bánh phải, 3 lần mỗi bánh. `D = L/(10π)`. Sai số: ±2 mm trên ~2,7 m và ±3° vạch là cỡ 0,1% `[ước lượng]`. (Ở C3, encoder sẽ đếm thay mắt.)
5. **Khoảng cách bánh:** đo mép ngoài–mép ngoài và mép trong–mép trong của hai bánh **chỗ chạm sàn** (ấn tờ giấy than hoặc bột phấn để thấy vết), lấy trung bình; sai số ít nhất ± một nửa độ rộng vết bánh chia √3 `[ước lượng]`.
6. **(Tùy chọn, 1h) Quán tính I_z bằng con lắc hai dây (bifilar):** treo robot nằm ngang bằng hai dây song song dài L, cách nhau d, đối xứng qua trọng tâm; xoay nhẹ quanh trục đứng, đo chu kỳ T qua 10 dao động. `I_z = m·g·d²·T² / (16·π²·L)` `[chuẩn — công thức con lắc hai dây]`. Không treo khi có pin thật hoặc mini PC thật.
7. **Xuất `hw/robot_params.yaml`:**

```yaml
# robot_params.yaml — mọi số SI, base_link theo REP-103
calibration_id: geom-01@2026-MM-DD-a
mass:            {value: 5.42,   unit: kg, std: 0.01,  method: three_scales, measured_at: 2026-MM-DD}
cog_x:           {value: 0.048,  unit: m,  std: 0.002, method: three_scales}
cog_y:           {value: 0.001,  unit: m,  std: 0.002, method: three_scales}
cog_z:           {value: 0.120,  unit: m,  std: 0.003, method: tilt_dz_0.05}
wheel_diameter_left:  {value: 0.0841, unit: m, std: 0.0001, method: roll_10rev_loaded}
wheel_diameter_right: {value: 0.0843, unit: m, std: 0.0001, method: roll_10rev_loaded}
track_width:     {value: 0.205,  unit: m,  std: 0.004, method: tape_contact_patch, note: "C6.2 sẽ hiệu chuẩn"}
caster_x:        {value: 0.200,  unit: m,  std: 0.002, method: tape}
inertia_zz:      {value: null,   unit: kg*m^2, std: null, method: not_measured}
```
(Số trong mẫu là ví dụ định dạng, không phải đáp án.) Viết một script nhỏ kiểm: mọi trường có `unit`, `std`, `method`; trọng tâm nằm trong đa giác tựa; tổng `mass_budget.csv` khớp `mass` trong ngưỡng Gate. Chạy nó trong CI.

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

**Mô phỏng (cân 10 g, thước 1 mm, h thật 120 mm):**

| Kê caster | Góc | Hai cân bánh kéo tăng | Khoảng 95% của h |
|---|---|---|---|
| 2 cm | 5,7° | ~220 g | ±7–8 mm |
| 5 cm | 14,3° | ~550 g | ±3 mm |
| 10 cm | 29,3° | ~1180 g | ±1,5 mm |

Kê 5 cm là thỏa hiệp tốt: đủ chính xác, chưa tới góc mà đồ trên robot trượt hay robot lật. Kê 2 cm cho số "trông hợp lý" nhưng sai số gấp đôi.

- Tổng ba cân **nặng hơn** `mass_budget.csv` vài chục tới vài trăm gram là bình thường ở lần đầu: dây, vít, dây rút, đai, keo — những thứ không ai cân. Lệch theo hướng ngược lại (cân nhẹ hơn bảng) nghĩa là một cân đọc sai hoặc robot không nằm trọn trên cân.
- D hiệu dụng của bánh cao su có tải thường **nhỏ hơn** danh nghĩa khoảng 0,5–2% `[ước lượng — tự đo]`, và hai bánh "giống nhau" lệch nhau vài phần nghìn. Vài phần nghìn đó là thứ làm robot đi cong ở C6.
- Góc lật tĩnh đo ở Lắp bước 9 khớp `atan(d/h)` trong 2–3° là tốt; lệch hơn thì nghi h (nghiêng quá ít), nghi điểm lật (caster xoay, bánh lún), hoặc đồ trên robot dịch khi nghiêng.

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Ba lần đặt lại cho x_G lệch nhau nhiều mm | Caster xoay hướng khác nhau mỗi lần; bánh không ở giữa mặt cân | Nhìn caster | Khóa hướng caster; đánh dấu vị trí trên cân |
| h âm hoặc lớn vô lý | Dấu dz sai; quên đổi g → kg; caster xoay khi nghiêng | In từng bước tính | Sửa đơn vị; khóa caster |
| D hai bánh lệch >1% | Bánh khác lô; một bánh bơm/lún khác; vạch đếm sai một vòng | Lăn lại, đổi bánh trái–phải | Ghi số thật; nếu bánh lỗi thì thay |
| Góc lật tĩnh nhỏ hơn dự đoán nhiều | Món trên robot trượt khi nghiêng (trọng tâm dịch) | Quay video khi nghiêng | Gá chặt hơn (C2.3); đo lại |

### 9. Câu hỏi ngược

1. **[Nếu…thì]** Nếu sim ở C11 lật robot ở góc khác với góc lật tĩnh bạn đo, bạn nghi tham số nào trước, và vì sao không nghi "engine vật lý sai" trước?
<details><summary>Hướng nghĩ</summary>

Góc lật tĩnh chỉ phụ thuộc hình học (d, h) — hai thứ bạn đã đo có sai số. Nếu sai lệch lớn hơn sai số đo, nghi cách bạn chuyển tham số vào model (đơn vị, gốc tọa độ, collision shape của bánh) trước khi nghi engine. Đó là verification trước validation (→ F6.2).

</details>

2. **[Quy mô]** 100 robot, mỗi robot một `robot_params.yaml`. Một năm sau bạn cần biết robot nào đang chạy với tham số đo trước khi thay bánh. Bạn cần lưu gì?
<details><summary>Hướng nghĩ</summary>

`calibration_id` có version, gắn vào metadata mọi bản ghi MCAP (CONVENTIONS mục 4); lịch sử thay phần cứng theo robot; tham số là dữ liệu có lineage (→ F3.8), không phải file ghi đè.

</details>

3. **[Failure mode]** Kể một cách `robot_params.yaml` "đúng" về mọi số nhưng vẫn làm sim sai.
<details><summary>Hướng nghĩ</summary>

Gốc tọa độ khác: bạn đo trọng tâm từ trục bánh kéo, URDF đặt `base_link` ở tâm khung; hoặc quy ước dấu `y`. Số đúng trong hệ quy chiếu sai — chính bài học Mars Climate Orbiter.

</details>

4. **[Phản biện]** "Đường kính bánh và khoảng cách bánh sẽ được UMBmark hiệu chuẩn ở C6 nên đo ở C2 làm gì cho mất công." Bạn trả lời thế nào?
<details><summary>Hướng nghĩ</summary>

Hiệu chuẩn cần điểm khởi đầu và cần một giá trị độc lập để kiểm: nếu UMBmark ra b lệch số thước 10%, đó là dấu hiệu lỗi ở đâu đó (encoder, trượt), không phải "kết quả hiệu chuẩn".

</details>

### 10. Liên kết ra ngoài

- **Hàng không, cân và cân bằng (weight and balance):** mọi chuyến bay tính khối lượng và trọng tâm theo bảng từng hạng mục và kiểm trọng tâm nằm trong giới hạn cho phép; máy bay được cân lại định kỳ. Giống `mass_budget.csv` + cân ba điểm. Khác: hàng không có quy định pháp lý và dung sai được chứng nhận.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| Công thức trọng tâm từ ba cân và từ phép nghiêng | [chuẩn] | Cân bằng mô-men; code kiểm bằng giá trị đã biết |
| Bánh cao su có tải: D hiệu dụng nhỏ hơn danh nghĩa 0,5–2% | [ước lượng] | Tự đo |
| `I_z = m·g·d²·T²/(16π²L)` | [chuẩn] | Con lắc hai dây, góc nhỏ |
| Mars Climate Orbiter: lbf·s vs N·s | [chuẩn] | Báo cáo Mishap Investigation Board 1999 |

**Đã sửa so với bản gốc:** K7 gốc dùng đường kính danh nghĩa 65 mm trong ví dụ mm/count và để UMBmark (Bài 4 gốc) gánh toàn bộ sai số; bài mới thêm đo tĩnh có sai số trước, để kết quả UMBmark ở C6.2 có giá trị đối chiếu.

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** ROS REP-103 (đơn vị, hệ trục); tài liệu URDF của ROS (thẻ `<inertial>`).
- **Giải thích:** JCGM 100 (GUM) — phần độ bất định loại B, hoặc viên nang → F1.1.
- **Tự kiểm tra:** (1) giải thích trong 5 câu vì sao đường kính hiệu dụng phải đo bằng lăn; (2) vẽ lại bảng tham số ở phần 2; (3) câu dưới.

  Robot 5 kg, ba cân đọc: bánh trái 1,8 kg, bánh phải 1,9 kg, caster 1,3 kg; caster ở x = 0,22 m, bánh ở y = ±0,1 m. x_G, y_G?
  <details><summary>Đáp án</summary>

  x_G = 1,3 × 0,22 / 5 = 0,057 m; y_G = (1,8 × 0,1 − 1,9 × 0,1)/5 = −0,002 m (lệch 2 mm về bên phải).

  </details>

---

## Gate chặng 2

Tiêu chí mới (K7 gốc không có gate cơ khí; theo `_KE-HOACH-K7.md` mục 7, C2 có gate "thông số hình học"). Mọi tiêu chí nhị phân, có bằng chứng trong repo.

```
[ ] 1. hw/motor_sizing.md: script C2.1 chạy với số listing thật (≥3 tỉ số), bảng độ nhạy,
       quyết định tỉ số + bánh, dòng đỉnh/chạy đều mỗi motor; commit TRƯỚC ngày mua motor
       (hoặc ghi rõ đã mua trước và kiểm lại sau)
[ ] 2. hw/mass_budget.csv: ≥90% khối lượng là "measured"; tổng lệch cân tổng ≤3%
[ ] 3. hw/robot_params.yaml: m, cog_x, cog_y, cog_z, D trái, D phải, track_width, caster_x —
       mỗi số có unit, std, method, measured_at; script kiểm chạy xanh trong CI
[ ] 4. Góc lật tĩnh đo được hai hướng; so với atan(d/h) từ robot_params.yaml, ghi lệch;
       a_lật hai hướng tính ra và quyết định giới hạn gia tốc (hoặc "không cần") ghi trong decisions.md
[ ] 5. Ba điểm tựa (hoặc 4 điểm có cơ cấu bảo đảm bánh kéo chạm): kiểm tờ giấy ở 3 vị trí sàn
[ ] 6. Bảng mối ghép; mọi mối gá motor/bánh/caster có vạch sơn; sau Lắp bước 9 không vạch nào lệch
[ ] 7. Cáp đã đặt theo mục 4: kéo thử 10 N mọi cáp, lực không vào đầu cắm; mọi lỗ xuyên tấm có grommet
[ ] 8. Không có pin thật trên khung; vít không chĩa vào vùng pin (ảnh chụp)
```

**FAIL action:** chặng chạm 40h (30h + 10h dư) mà chưa PASS → tiêu chí 1, 3 (tối thiểu m, D trái/phải, track_width), 5, 8 là bắt buộc; tiêu chí 2, 4, 6, 7 ghi "nợ" vào `decisions.md` kèm hạn trả ở C5 (trước lần cấp pin đầu tiên lên khung). Không được nợ tiêu chí 8.
