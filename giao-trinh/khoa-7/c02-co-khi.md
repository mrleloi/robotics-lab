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

## Bài C2.1 — Lực, mô-men, chọn motor và tỉ số truyền bằng số (6h)

> **Vị trí:** (mở đầu C2) → **C2.1** → C2.2 · **Cần trước:** K1 Bài 1 (bốn đại lượng), → F1.1 (con số nào là ước lượng); không cần C1 · **Sau bài này bạn quyết định được:** mua JGB37-520 tỉ số truyền nào với bánh đường kính nào, cho khối lượng và tốc độ của bạn; và chuyển con số dòng đỉnh, dòng chạy đều cho C1.2 (power budget) và C3 (chọn driver).

### 1. Câu chuyện — ai đã khổ vì chuyện này

Năm 1902–1903, anh em Wright cần một động cơ cho chiếc Flyer. Họ đã có số liệu lực nâng và lực cản đo bằng ống gió tự làm, nên tính được trước **cần bao nhiêu lực đẩy** và từ đó bao nhiêu công suất. Không nhà sản xuất động cơ ô tô nào họ hỏi chịu làm một động cơ đủ nhẹ cho công suất đó, nên thợ máy Charlie Taylor của họ đúc một động cơ khối nhôm khoảng 12 mã lực; còn cánh quạt thì họ tự thiết kế bằng lý thuyết, vì không có tài liệu nào về cánh quạt máy bay `[chuẩn — lịch sử được ghi chép rộng rãi, ví dụ Smithsonian National Air and Space Museum]`. Thứ đáng học không phải động cơ nhôm. Đó là **thứ tự**: yêu cầu (lực, tốc độ) → con số → rồi mới chọn hoặc làm phần cứng.

Người mới dựng robot thường làm ngược: mua motor "trông khỏe", lắp, thấy robot ì hoặc bò lên dốc không nổi, rồi mua motor khác. Với robot chở mini PC và pin, sai lầm còn đắt hơn: motor tỉ số truyền quá thấp thì kéo dòng lớn, nóng và làm sụt nguồn; quá cao thì robot không bao giờ đạt tốc độ, và (phần ít ai biết) **chính rotor của motor trở thành một khối lượng ảo** mà bạn phải tăng tốc mỗi lần khởi hành.

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
V_min, V_rated = 12.0, 12.0   # V: áp pack thấp nhất (C1.1) / áp danh định motor
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

Vì sao ngưỡng "≤50% mô-men hãm" cho đỉnh: ở 50% mô-men hãm motor cho công suất cơ lớn nhất nhưng hiệu suất không quá ~50% và dòng bằng nửa dòng hãm; nhiệt cuộn dây tỉ lệ `I²R` `[chuẩn]`. Các listing JGB37 ghi "mô-men định mức" (chạy liên tục) chỉ cỡ 1/4–1/3 mô-men hãm `[spec người bán]`. Đỉnh ngắn (≈1 s) được phép lên gần 50%; chạy đều phải nằm dưới định mức. Đây là quy tắc kỹ thuật thô, không phải định luật; bạn được đổi nếu có lý do và ghi vào `decisions.md`.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Capacity planning: tính QPS đỉnh và trung bình, chọn instance có dư | Tính mô-men đỉnh và chạy đều, chọn tỉ số truyền có dư | Instance to hơn chỉ tốn tiền. Tỉ số truyền "to hơn" (N lớn) **làm hỏng** điều kiện kia: mất tốc độ và tăng quán tính rotor theo N². Không có lựa chọn "cứ lớn cho chắc" | Mua 1:90 "cho khỏe" → robot không bao giờ đạt 0,5 m/s khi pin yếu; PID bão hòa ở tốc độ cao |
| Chọn họ instance (CPU-optimized vs memory-optimized) cùng giá, đổi tỉ lệ tài nguyên | Cùng một motor, đổi N là đổi tỉ lệ mô-men/tốc độ ở cùng công suất | Instance type đổi được trong 5 phút. Hộp số đổi là tháo robot, mua motor mới, và mọi hệ số encoder (count/vòng) đổi theo | Coi tỉ số truyền là "cấu hình chỉnh sau" → phải làm lại C3, C6 |
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

**Tham số cần tra:** trang người bán (hoặc datasheet nếu có) của đúng mã JGB37-520 bạn định mua: điện áp danh định, rpm không tải ở trục ra, dòng không tải, mô-men hãm, dòng hãm, mô-men định mức, mô-men cho phép của hộp số; ghi rõ **listing nào** (link, ngày). Áp pack thấp nhất: lấy từ C1.1 khi đã chọn hóa học pin; chưa có thì dùng 12 V. C_rr: chưa đo thì 0,03 `[ước lượng]`, sẽ đo ở bước 6 phần Làm.

**Công thức:** `F = m·a + m·g·sinθ + C_rr·m·g·cosθ`; `τ_bánh = F·r/2`; `rpm = v/(2πr)·60`; `m_rotor_tđ = 2·J·N²/r²`; `I = I0 + (I_hãm − I0)·τ/τ_hãm`.

```markdown
# prediction.md — K7 C2.1
commit: <hash>  ngày: <yyyy-mm-dd>
## Đầu vào (nguồn từng dòng)
- m = 6.0 kg (mục tiêu 5 kg + 20%)   v_max = 0.5 m/s   a = 0.5 m/s²   θ = 5°   C_rr = 0.03 (ước lượng)
- Bánh D = ... mm (đo thước kẹp)   V_min pack = ... V (nguồn: C1.1 / tạm 12 V)
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
3. Thay `cands` bằng số của **listing thật** bạn định mua (ít nhất 3 tỉ số). Thay `V_min` bằng số của C1.1 nếu đã có.
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
- C_rr đo bằng kéo (bước 6) trên sàn gạch thường ra **cao hơn** con số giáo khoa của bánh cao su đơn thuần, vì gồm caster và hộp số bị kéo ngược `[ước lượng — tự đo]`.

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Tính tay lệch script ~10 lần | kg·cm vs N·m; hoặc mm vs m | In từng số hạng | Đơn vị SI trong code, đổi ở biên |
| Tính tay lệch script đúng 2 lần | Quên chia hai bánh, hoặc dùng đường kính thay bán kính | — | — |
| Không tỉ số nào đạt | Khối lượng/dốc quá tham vọng; hoặc pin quá thấp áp | Chạy độ nhạy | Bỏ yêu cầu dốc (văn phòng không dốc?), bánh to hơn, hoặc họ motor lớn hơn; ghi quyết định |
| Listing ghi mô-men hãm nhưng không ghi dòng hãm | Phổ biến | — | Ước bằng `V/R` với R đo ở Lắp bước 1 (C3.1 đo kỹ) |
| C_rr đo được rất lệch giữa các lần kéo | Kéo không đều; đọc lúc giật | Quay video màn hình cân | Kéo bằng sợi dây dài, đi bộ đều; bỏ 1 m đầu |
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

5. **[Liên ngành]** Xe đạp có líp nhiều tầng. Người đạp xe chuyển số để giữ cadence (vòng đạp/phút) gần một khoảng. Điều đó tương ứng với cái gì trong bài, và chỗ nào khác?
<details><summary>Hướng nghĩ</summary>

Giống: hộp số đặt điểm làm việc trên đường đặc tính của "động cơ". Khác: robot của bạn có **một** tỉ số cố định, nên chọn sai là sai suốt đời; và đường đặc tính của người không thẳng như motor DC.

</details>

6. **[Phản biện]** "Cứ mua motor to hơn hai cỡ cho chắc, pin thừa sức." Bạn phản bác bằng ba con số nào trong `motor_sizing.md`?
<details><summary>Hướng nghĩ</summary>

Khối lượng motor (vào lại phương trình), dòng hãm (vào driver, cầu chì, C1), và mô-men phanh khi phanh gấp (vào chống lật, C2.2). "To hơn" không miễn phí ở cả ba.

</details>

### 10. Liên kết ra ngoài

- **Thang máy và đối trọng.** Motor thang máy không nâng cả cabin: đối trọng cân bằng cabin cộng khoảng nửa tải định mức, nên motor chỉ gánh phần chênh. Giống: tách thành phần "luôn có" khỏi phần "thỉnh thoảng". Khác: robot không có đối trọng cho dốc; thứ gần nhất là chọn N sao cho trường hợp thường xuyên nằm ở vùng hiệu suất tốt.
- **Hàng không, chân vịt bước thay đổi (variable-pitch propeller).** Máy bay cánh quạt đổi bước cánh để động cơ làm việc gần vòng tua tối ưu ở cả cất cánh (cần lực đẩy) và bay bằng (cần tốc độ). Đây chính là "hai điểm làm việc" của bài, được giải bằng một hộp số biến thiên. Robot rẻ không có thứ đó, nên phải thỏa hiệp bằng tính toán.
- **Điện toán đám mây, chọn instance theo profile.** Cùng giá, đổi tỉ lệ tài nguyên. Khác: ở đây bạn chỉ có **một** lần chọn, và sai thì phải tháo máy.

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
