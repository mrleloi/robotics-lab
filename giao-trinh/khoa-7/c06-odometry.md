# Chặng 6 — Odometry (25h)

> **Vị trí:** C5 (robot chạy bằng pin, teleop, `/odom` từ `diff_drive_controller`) → **C6** → C7 (cảm biến và ghi dữ liệu) · **Cần trước:** K7 C5 trọn (đặc biệt C5.2 `ros2_control` + `diff_drive_controller`, C5.3 teleop có deadman và E-stop tạm); `hw/robot_params.yaml` của C2.4; → F1.1, F1.6, F6.4; đọc mục 2 của → F6.1; đọc mục 2 của → F6.7 trước Bài C6.3 · **Chạy song song với:** K4–K5
> **Làm ra được:** robot đi hình vuông 2 m theo odometry của chính nó với sai số hệ thống đã hiệu chuẩn; một sàn thử có trục tọa độ dán băng và đồ gá xuất phát · `data/c06/` (40 điểm dừng UMBmark trước/sau, 20 lần chạy thẳng 10 m, 3 mặt sàn, va chạm), `calib/umbmark.yaml` có `calibration_id`, bài viết "Calibrating differential drive odometry: UMBmark with numbers" · **Sau chặng này bạn quyết định được:** hệ số nào nạp vào `diff_drive_controller` (tỉ lệ chung, tỉ số đường kính, khoảng cách bánh); odometry một mình đủ cho quãng đường bao xa trước khi phải có định vị ngoài (C8); một hồ sơ hiệu chuẩn còn hợp lệ trên sàn nào, ở tốc độ và gia tốc nào; tín hiệu nào phải có để robot biết mình vừa trượt.

C5 cho bạn một con robot chạy bằng pin, điều khiển tay, có topic `/odom`. Con số trong `/odom` trông rất tự tin: sáu chữ số thập phân, cập nhật đều 50 lần mỗi giây. C6 hỏi con số đó **sai bao nhiêu**, sai theo kiểu nào, và phần nào sửa được. Bạn không lắp thêm khối điện nào ở chặng này. Thứ bạn dựng là một **phép đo**: sàn có trục tọa độ, đồ gá xuất phát, điểm tham chiếu trên robot, thước có sai số đã biết. Đây là chặng đầu tiên trong K7 mà sản phẩm chính là một bộ dữ liệu có ground truth.

**Phân bổ 25h** `[ước lượng]`:

| Phần | Giờ |
|---|---|
| Lắp bước 1–3: sàn thử, trục tọa độ 3-4-5, đồ gá xuất phát chữ L, điểm tham chiếu trên robot, script chạy hình | 4 |
| Bài C6.1 Động học vi sai và odometry (gồm Phần A: đo tay, lăn bánh) | 5 |
| Bài C6.2 UMBmark: tách sai số đường kính và khoảng cách bánh (Phần B: thẳng 10 m; Phần C: UMBmark trước/sau) | 9 |
| Bài C6.3 Odometry không biết mình sai: trượt, va chạm (Phần D) | 4 |
| Bài viết UMBmark (tiêu chí 6 của Gate 7A gốc) + Gate chặng 6 | 3 |
| **Tổng** | **25** |

Bản gốc dành 16h cho Bài 4 (odometry + UMBmark). Ở đây thêm 9h cho phần người mới thật sự cần: dựng sàn thử có sai số biết trước, viết script cho robot tự đi hình, và bài viết (bản gốc đặt nó ở Gate 7A mà không cấp giờ).

## 0. Bức tranh chặng

Robot sau chặng này trông giống hệt sau C5. Thứ mới nằm trên **sàn** và trong **file cấu hình**:

```
  SÀN THỬ (gạch, phẳng, ≥ 3 m × 3 m cho UMBmark; hành lang ≥ 11 m cho đường thẳng)

        y ▲  (trục y: băng giấy, vuông góc trục x bằng tam giác 3-4-5)
          │
          │          ┌ ─ ─ ─ ─ ─ ─ ─ ─ ┐   hình vuông 2 m (robot tự đi theo /odom,
          │                               KHÔNG có băng dọc cạnh để tránh "bám vạch")
          │          │                 │
          │
          │          │                 │
     ┌────┤
     │ L  │          └ ─ ─ ─ ─ ─ ─ ─ ─ ┘
     │khung◄── đồ gá xuất phát chữ L: hai bánh tựa vào, hướng +x
     └────●──────────────────────────────────────────►  x (trục x: băng giấy)
         gốc O = vị trí điểm tham chiếu khi robot nằm trong đồ gá

  TRÊN ROBOT: điểm tham chiếu chạm/chiếu xuống sàn đúng giữa trục hai bánh
              (bút dạ trong ống trượt, hoặc laser chấm thẳng xuống)

  DÒNG DỮ LIỆU:
  encoder ─► ESP32 (C4) ─► ros2_control hardware interface ─► diff_drive_controller ─► /odom
                                                                    ▲
                                       calib/umbmark.yaml ─────────┘ (hệ số mới, calibration_id)
  thước dây + ê-ke ─► data/c06/*.csv (điểm dừng THẬT) ─► umbmark_solve.py ─► calib/umbmark.yaml
  ros2 bag record /odom /joint_states ─► data/c06/bags/  (đối chiếu odometry với điểm dừng thật)
```

Dòng năng lượng không đổi so với C5. Dòng dữ liệu mới: hai nguồn "vị trí" độc lập (odometry của robot và thước của bạn) được đặt cạnh nhau. Toàn bộ chặng là việc đo khoảng cách giữa hai nguồn đó.

## 1. An toàn của chặng

**Rủi ro của C6:** robot lần đầu **tự đi** theo script, không có tay bạn trên cần teleop từng giây; đi 10 m một mạch; cố ý cho đâm tường (Bài C6.3); chạy nhiều giờ liền nên pin xả sâu hơn mọi chặng trước; người cúi sát sàn đo đạc ngay trên đường robot đi; người khác (đồng nghiệp, trẻ em, thú nuôi) đi ngang hành lang thử.

**Quy tắc cứng:**
- KHÔNG chạy script tự đi khi chưa thử E-stop tạm (C5.3) trong buổi đó: bấm E-stop khi bánh đang quay trên giá kê, bánh phải dừng. Ghi kết quả vào sổ.
- KHÔNG chạy script khi bạn không cầm nút E-stop tạm (hoặc deadman) trong tay. Script không thay cho người.
- KHÔNG đặt tốc độ thử trên 0,2 m/s trong chặng này, kể cả khi kẹp firmware (C4.4) cho phép cao hơn. Va chạm ở Bài C6.3 chỉ ở **≤ 0,1 m/s**.
- KHÔNG chạy gần cầu thang, cửa mở ra cầu thang, mép bậc, hoặc nơi có dây điện vắt ngang sàn. Hành lang 10 m phải có vật chắn ở cuối (thùng carton, gối) cách điểm dừng dự kiến ≥ 1 m.
- KHÔNG cúi đo điểm dừng khi robot chưa ở trạng thái an toàn (motor tắt, E-stop đang ấn hoặc controller đã dừng). Đầu và tay bạn ở ngang bánh xe.
- KHÔNG nhấc robot lên khi bánh đang quay. Ngón tay vào giữa bánh và khung là kẹp thật.
- KHÔNG chạy khi `V_bat` đã chạm ngưỡng cảnh báo bạn đặt ở C1 (pin xả sâu làm robot đổi hành vi, và làm hỏng pin). Ghi `V_bat` đầu và cuối mỗi loạt.
- KHÔNG để robot chạy một mình để đi lấy thước. Dừng, tắt motor, rồi mới đi.
- KHÔNG đâm tường bằng mặt có camera, mini PC lộ, hoặc pin lộ. Va chạm vào cản trước (nếu có) hoặc vào tấm xốp dán tường.

**Khi sự cố xảy ra:**

| Sự cố | Làm ngay | KHÔNG |
|---|---|---|
| Robot chạy thẳng không dừng ở cuối đường (script treo, odometry sai) | Bấm E-stop tạm; nếu không dừng: ngắt công tắc chính (C1) | Chạy theo chặn bằng chân hoặc tay |
| Robot quay tròn không dừng | E-stop tạm; đứng ngoài bán kính quay | Thò tay vào nhấc lên |
| Sau va chạm robot đẩy tường mãi, motor kêu ù, mùi nóng | E-stop; sờ vỏ motor sau 1 phút (mu bàn tay, chạm nhẹ) | Tiếp tục thử lại ngay khi motor đang nóng |
| Pin hoặc dây nóng bất thường sau nhiều giờ chạy | Theo bảng "Khi sự cố" của C0 và C1.6 | Sạc ngay khi pin đang nóng |

## 2. BOM chặng

Giá `[ước lượng 10/2026]`, kiểm lại ở cửa hàng. Chặng này rẻ: hầu hết là dụng cụ đo sàn.

| Món | Thông số phải chọn | Vì sao (bằng số) | Giá | Kiểm khi nhận hàng | Thay thế được bằng |
|---|---|---|---|---|---|
| Thước dây thép | 10 m, lưỡi rộng ≥ 19 mm, có ghi cấp chính xác (ví dụ "Class II") | Cấp II theo chuẩn đo lường châu Âu cho phép sai số ±(0,3 + 0,2·L) mm, L tính bằng m → ±2,3 mm ở 10 m `[spec — EU MID Annex MI-008, kiểm lại]`; nhỏ hơn rất nhiều so với độ lệch đang tìm | 150–400k | So vạch 1 m với thước thép 1 m; móc đầu trượt được đúng bằng bề dày móc | Thước dây 5 m (đo 10 m bằng hai lần, cộng sai số) |
| Thước thép 1 m + ê-ke thợ mộc | Vạch mm khắc, ê-ke 30 cm | Đo khoảng cách vuông góc từ điểm dừng tới trục | 100–250k | Ê-ke áp vào cạnh thước, lật mặt: khe hở hai lần phải như nhau | Ê-ke học sinh lớn |
| Băng keo giấy (masking tape) | 2 màu, rộng 24 mm, loại không để lại keo | Trục tọa độ trên sàn, đánh dấu điểm dừng | 30–60k | Dán thử 1 ngày lên sàn, bóc không để vết | Băng keo điện (kém: co dãn) |
| Bút dạ đầu mảnh + ống trượt, hoặc module laser chấm 5 mW chiếu xuống | Đầu bút ≤ 0,5 mm; ống cho bút trượt tự do và chạm sàn bằng trọng lượng của bút | Điểm tham chiếu giữa trục bánh; vết bút cho phép đo **sau** khi robot dừng | 20–80k | Vết chấm tròn, không nhòe | Mũi kim gắn lò xo |
| Gỗ hoặc nhôm định hình làm khung chữ L | Hai thanh ≥ 40 cm, vuông góc | Đồ gá xuất phát: đặt lại robot đúng vị trí và hướng mỗi lần | 50–100k | Kiểm vuông bằng tam giác 3-4-5 | Hai hộp sách nặng đặt vuông góc |
| Tấm xốp 2–3 cm | ~ 50 × 50 cm | Mặt tường cho va chạm ở C6.3 | 30–50k | — | Gối |
| Thảm thử | ≥ 1 × 3 m, loại văn phòng | Mặt sàn thứ hai ở C6.3 | 0–200k | — | Thảm sẵn có |

**Tổng C6 `[ước lượng]`:** ~0,4–1,1tr. Thước cặp đã có từ C2. Không có linh kiện điện mới.

## 3. Dụng cụ và kỹ năng tay

Kỹ năng mới của chặng là **đo sàn có sai số biết trước**. Không khó, nhưng người mới gần như luôn sai ở ba chỗ: móc đầu thước, góc vuông "bằng mắt", và đọc vạch nghiêng.

| Kỹ năng | Bài | Luyện trước | Đạt trông thế nào |
|---|---|---|---|
| Đọc thước dây đúng | Lắp bước 1 | Đo cùng một đoạn 2 m năm lần, hai cách (móc đầu và "bắt đầu từ vạch 10 cm") | Năm lần trong ±1 mm; hai cách khớp nhau trong ±1 mm |
| Dựng góc vuông bằng tam giác 3-4-5 | Lắp bước 1 | Dựng trên sàn với 0,6 / 0,8 / 1,0 m | Cạnh huyền đo được 1,000 m ± 2 mm |
| Đo tọa độ một chấm | Lắp bước 2 | Chấm 5 điểm bất kỳ, đo (x, y) hai lần cách nhau 10 phút | Hai lần lệch ≤ 2 mm mỗi trục |
| Đặt robot vào đồ gá | Lắp bước 3 | Đặt 10 lần, mỗi lần chấm điểm tham chiếu | 10 chấm nằm trong vòng tròn đường kính ≤ 3 mm |

**Móc đầu thước dây trượt là có chủ đích.** Móc kim loại ở đầu thước di chuyển đúng bằng bề dày của chính nó, để phép đo "móc vào mép" (kéo) và "tì vào vách" (đẩy) cùng đúng `[chuẩn]`. Móc bị cong (thước rơi nhiều lần) làm mọi phép đo lệch một hằng số. Cách tránh: đo từ vạch 10 cm (hoặc 100 mm) và trừ đi; thợ mộc gọi là "burn an inch". Ghi cách bạn dùng vào `instruments.jsonl`.

**Tam giác 3-4-5:** đánh dấu điểm O, kéo 0,6 m theo trục x đánh dấu A. Từ O kéo một đoạn 0,8 m, từ A kéo một đoạn 1,0 m; chỗ hai đoạn gặp nhau là B, và OB vuông góc OA `[chuẩn — Pythagoras: 0,6² + 0,8² = 1,0²]`. Hai người làm dễ hơn một.

**Đọc vạch:** mắt nhìn vuông góc với thước, không nhìn xiên (thị sai). Với bút trên robot, đo **tâm** vết chấm.

## 4. Sơ đồ đi dây

**Chặng này không có dây mới.** Mọi dây giữ nguyên như C5 và `wiring/wires.csv`. Nếu bạn gắn module laser chấm sàn thay cho bút, nó là một tải 5 V nhỏ, đi theo quy ước C0.5:

```
  buck 5 V logic (C1) ──[tím, 22 AWG]──► module laser (+)       qua JST-XH 2 chân, có nhãn wire_id
  GND (sao, phía logic) ─[đen, 22 AWG]──► module laser (−)
  Dòng: vài chục mA [tự đo bằng UT33D+ trên nguồn bàn trước khi gắn lên robot]
```

KHÔNG cấp laser từ chân GPIO của ESP32 trực tiếp (dòng chân giới hạn, và một chân GPIO không có lý do gì phải liên quan tới phép đo sàn). Làm theo "một khối mới một lần": thử laser trên nguồn bàn có giới hạn dòng (C0.4) trước, rồi mới nối vào nhánh 5 V.

Thay cho sơ đồ dây, chặng này có **sơ đồ sàn** ở mục 0 và bảng dữ liệu ở mục 7.

## 5. Trình tự chặng

1. **Lắp bước 1 — Dựng trục tọa độ trên sàn**
   - Làm: chọn sàn gạch phẳng ≥ 3 × 3 m. Dán trục x dài ≥ 2,5 m. Dựng trục y bằng tam giác 3-4-5. Đánh dấu gốc O bằng dấu cộng nhỏ trên băng. Chọn hành lang ≥ 11 m cho đường thẳng; dán một đường x dài 10 m, đánh dấu vạch 10,000 m.
   - ✅ Checkpoint: cạnh huyền của tam giác 3-4-5 đo được 1,000 m ± 2 mm; vạch 10 m đo lại hai lần lệch ≤ 2 mm. Ghi vào `measurements.jsonl` (`quantity: floor_axis_check`).
   - Nếu sai: dựng lại; KHÔNG "nắn" bằng cách kéo căng băng.
2. **Lắp bước 2 — Điểm tham chiếu trên robot**
   - Làm: gắn ống trượt cho bút (hoặc laser) sao cho đầu bút chạm sàn **đúng giữa đoạn nối tâm hai vết bánh**. Tìm điểm đó: đặt robot lên tờ giấy, lăn nhẹ 5 cm, hai vết bánh cho hai đường; điểm giữa của đoạn vuông góc nối hai đường.
   - ✅ Checkpoint: đặt robot, chấm, xoay robot 180° tại chỗ bằng tay quanh điểm chấm (nhấc nhẹ, đặt lại sao cho hai bánh đổi chỗ trên hai đường vết cũ), chấm lại: hai chấm cách nhau ≤ 3 mm. Lệch nhiều nghĩa là điểm tham chiếu không nằm trên trục bánh.
   - Nếu sai: dời ống trượt theo nửa khoảng lệch, làm lại.
3. **Lắp bước 3 — Đồ gá xuất phát và script chạy hình**
   - Làm: đặt khung chữ L sao cho khi hai bánh (hoặc mép khung robot) tựa vào, điểm tham chiếu trùng O và robot hướng +x. Cố định khung bằng băng keo. Cài `drive_shape.py` (Bài C6.2, mục 6).
   - ✅ Checkpoint trước khi chạy script lần đầu: robot trên giá kê (bánh không chạm sàn), chạy `drive_shape.py --shape straight --length 0.5`: bánh quay rồi tự dừng; bấm E-stop tạm giữa chừng một lần: bánh dừng. Đặt 10 lần vào đồ gá: 10 chấm trong vòng ≤ 3 mm.
   - Nếu sai: xem mục 6 (lỗi người mới).
4. **Học Bài C6.1.** Làm Phần A (đo tay, lăn bánh) và commit `prediction.md` **trước** khi robot tự đi lần đầu.
5. **Học Bài C6.2.** Phần B (thẳng 10 m × 10), hiệu chỉnh tỉ lệ chung, rồi Phần C (UMBmark trước), nạp hệ số, UMBmark sau, thẳng 10 m × 10 lần nữa.
   - ✅ Checkpoint trước khi nạp hệ số: chạy `umbmark_solve.py` trên điểm dừng **giả** sinh từ mô phỏng có sai số biết trước; script phải tìm lại đúng dấu (Bài C6.2, mục 6 bước 9).
6. **Học Bài C6.3.** Phần D: ba mặt sàn, va chạm.
7. **Viết bài** "Calibrating differential drive odometry: UMBmark with numbers".
8. **Gate chặng 6.**

Robot vẫn "chạy được ở phạm vi nhỏ hơn" suốt chặng: teleop của C5 không đổi; chỉ cấu hình `diff_drive_controller` đổi, và mỗi lần đổi có `calibration_id` mới để quay lại bản cũ.

## 6. Lỗi người mới hay gặp

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Đo cùng một điểm dừng hai lần lệch 5–10 mm | Móc thước cong; đọc xiên; trục y không vuông | Đo lại từ vạch 10 cm; kiểm lại 3-4-5 | Dùng ê-ke áp trục; một người đọc, một người ghi |
| Robot đi ngắn hơn lệnh rõ rệt ngay từ đầu | `wheel_radius` trong cấu hình là bán kính danh định của nhà bán, không phải số đo; hoặc nhầm đường kính với bán kính | So cấu hình với `robot_params.yaml` (C2.4) | Dùng bán kính hiệu dụng đo được; đơn vị m |
| Robot quay 90° thành ~80° hay ~100° | `wheel_separation` là khoảng cách mép ngoài bánh | Đo lại B theo C6.1 | Dùng tâm vết bánh; để UMBmark tinh chỉnh |
| Lần chạy đầu lệch khác hẳn các lần sau | Motor nguội, mỡ hộp số đặc; robot chưa "ngồi" vào đồ gá | Bỏ lần đầu có ghi chú; chạy 2 vòng khởi động | Ghi quy trình khởi động vào `procedure.md` |
| Kết quả buổi sáng khác buổi chiều | `V_bat` khác, nhiệt độ motor khác | So `V_bat` hai buổi | Chạy ở dải `V_bat` cố định, ghi vào điều kiện |
| Script dừng giữa hình, robot đứng yên | Timeout của controller hoặc của firmware (C4.4) vì script gửi lệnh thưa | Đếm tần số lệnh bằng `ros2 topic hz` | Script gửi lệnh đều ≥ 10 Hz `[tự đo theo timeout của bạn]` |
| Bút để vệt dài thay vì chấm | Bút chạm sàn lúc robot đang chạy | — | Bút chạm sàn suốt cũng được (vệt cho biết quỹ đạo thật); chấm cuối là điểm dừng |

Lỗi riêng của từng phép đo nằm ở phần 8 của mỗi bài.

## 7. Lăng kính data infra

**Dữ liệu chặng này sinh ra:**

| Luồng | File | Schema (rút gọn) | Tần số / số lượng | Đơn vị (theo `CONVENTIONS.md`) |
|---|---|---|---|---|
| Đo tay hình học | `build-log/measurements.jsonl` | schema C0.5; `quantity`: `wheel_diameter_left`, `wheel_diameter_right`, `track_width_min`, `track_width_max`, `rollout_distance`… | ~30 dòng | `m` (không `mm` trong dữ liệu) |
| Điểm dừng | `data/c06/runs.csv` | `run_id, ts, test` (`straight10`/`umbmark_cw`/`umbmark_ccw`/`floor`/`bump`)`, calibration_id, floor, speed_mps, v_bat_start_V, v_bat_end_V, x_true_m, y_true_m, odom_x_m, odom_y_m, odom_yaw_rad, bag, note` | 10 + 10 + 20 + 20 + 6–12 dòng | `m`, `rad`, `V`, `m/s` |
| Odometry thô của mỗi lần chạy | `data/c06/bags/<run_id>/` (rosbag2 → MCAP) | `/odom` (`nav_msgs/msg/Odometry`), `/joint_states` (`sensor_msgs/msg/JointState`) | 50 Hz, 100 Hz `[theo cấu hình C5]` | SI, `rad` |
| Hồ sơ hiệu chuẩn | `calib/umbmark.yaml` | `calibration_id, parent_id, created_at, floor, speed_mps, v_bat_range_V, scale, E_d, E_b, c_L, c_R, B_new_m, alpha_rad, beta_rad, n_runs, runs_ref` | mỗi lần hiệu chuẩn | SI |

`calibration_id` theo mẫu trong `CONVENTIONS.md` mục 4 (`odom-01@2026-11-20-a`). Mỗi dòng trong `runs.csv` ghi `calibration_id` **đang chạy** lúc đó: thiếu cột này thì không ai tách được "trước" và "sau" sau ba tháng.

**Test tự động sinh ra từ chặng này (hạt giống HIL/CI cho C11):**
- **Golden replay:** một bag thật (`/joint_states` → `/odom`) và hàm odometry offline của bạn (Bài C6.1) phải cho cùng quỹ đạo trong dung sai; khi đổi phiên bản `diff_drive_controller` hay đổi tham số, CI chạy lại và so. Đây là regression test của **phép tính**, không của robot.
- **Metamorphic:** hoán đổi chuỗi encoder trái–phải thì quỹ đạo là ảnh gương qua trục x (→ F2.4, câu hỏi tự kiểm ở đó dùng đúng ví dụ này).
- **UMBmark là một bench test có ngưỡng:** ở C11.2 nó có thể chạy lại định kỳ trong sim với tham số nhiễu, và trên robot thật mỗi khi đổi bánh/lốp; `E_max,syst` là metric có lịch sử theo `calibration_id`.

**SLI:** `E_max,syst` hiện tại; tuổi của hồ sơ hiệu chuẩn (ngày, km đã chạy kể từ lần hiệu chuẩn); tỉ lệ lần chạy có đủ cặp (điểm dừng thật, bag).

**Covariance của `/odom`:** `diff_drive_controller` điền covariance từ tham số cấu hình **hằng số** (`pose_covariance_diagonal`, `twist_covariance_diagonal`) `[tự đo theo phiên bản ros2_controllers bạn cài]`, trong khi độ bất định thật của pose lớn dần theo quãng đường (Bài C6.2, C6.3). Ở chặng này bạn **đo** con số để điền (phương sai theo mét đi được, phương sai vận tốc); cách bộ hợp nhất dùng nó là việc của C8.3. Đừng điền theo mẫu trên mạng: đó là con số của robot người khác.

**Vai trò nghề:** Test & Validation (ground truth có sai số, thiết kế thí nghiệm hai chiều, ngưỡng gate); Data Platform (`calibration_id` như khóa phiên bản, bag gắn với điểm dừng thật, provenance từ thước tới hệ số).

## 8. Nhật ký build

Copy vào `build-log/c06.md`, một mục mỗi buổi:

```markdown

## 2026-MM-DD — buổi N (giờ bắt đầu–kết thúc, giờ thực: _._ h)
- Trạng thái người: tỉnh táo / mệt (mệt → chỉ phân tích dữ liệu, không chạy robot)
- E-stop tạm đã thử đầu buổi: có / không (không → không chạy script)
- Sàn: gạch / thảm / gỗ · nhiệt độ phòng: __ °C
- calibration_id đang nạp: odom-01@...
- V_bat đầu / cuối buổi: __ V / __ V
- Đã chạy: (ví dụ: umbmark_cw ×5, run_id c06-021…025)
- Số đo (đã vào runs.csv? có/không; số dòng: __) · bag: data/c06/bags/...
- Ảnh: sàn, vết chấm, đồ thị điểm dừng
- Lỗi gặp (triệu chứng → nguyên nhân → sửa):
- Quyết định (ghi decisions.md nếu đổi hệ số, đổi sàn chuẩn):
- Suýt sự cố: không / có → mô tả
- Câu hỏi còn mở:
```

---
