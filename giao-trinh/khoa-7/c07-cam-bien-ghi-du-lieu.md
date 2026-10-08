# Chặng 7 — Cảm biến và ghi dữ liệu (35h)

> **Vị trí:** C6 (odometry đã hiệu chuẩn) → **C7** → C8 (định vị và điều hướng) · **Cần trước:** K7 C6 trọn; K5 M1–M3 (K5 Bài 3–4 IMU qua I2C, K5 Bài 8–9 đo offset đồng hồ, K5 Bài 13–15 ingest MCAP, upload resumable, index); K2 M1–M2 (MCAP, `mcap recover`, tool audit `lerobot-audit`); → F3.1, F3.4, F4.6; đọc → F3.5, F3.7, F4.3, F5.5 khi tới bài tương ứng · **Chạy song song với:** K5
> **Làm ra được:** IMU và camera USB gá cứng trên robot, cây TF tĩnh `base_link → imu_link`, `base_link → camera_front_link → camera_front_optical_frame` đúng REP-103/105 · sidecar ghi MCAP trên mini PC, niêm phong + manifest, upload resumable lên object store, audit tự động, data contract của robot, layout Foxglove commit trong repo · **Sau chặng này bạn quyết định được:** gá IMU kiểu gì và đặt lọc bao nhiêu để rung motor không thành chuyển động ma; định dạng và độ phân giải camera nào vừa băng thông USB; timestamp mỗi luồng lấy từ đồng hồ nào và sai bao nhiêu ms; một file MCAP của robot được phép rời robot, được phép xóa local, được phép vào tập huấn luyện khi nào.

Sau C6 robot biết nó **nghĩ** mình ở đâu. C7 cho nó hai giác quan độc lập với bánh xe (quán tính và ảnh) và cho bạn hệ thống giữ lại mọi thứ robot thấy. Đây là chỗ K5 vào việc trên robot thật: không có khái niệm mới về MCAP hay upload, nhưng có ba thứ K5 trên bàn chưa gặp: **rung** của motor, **lịch** của một CPU đang bận chạy ROS 2, và một con robot chạy bằng pin rời khỏi tầm Wi-Fi.

**Phân bổ 35h** `[ước lượng]`:

| Phần | Giờ |
|---|---|
| Lắp bước 1–5: gá IMU (ba kiểu thử), gá camera, đi dây I2C + INT, URDF/TF, udev cho camera | 5 |
| Bài C7.1 Gá cảm biến: rung, frame, TF tĩnh, băng thông USB | 8 |
| Bài C7.2 Timestamp trên robot: source time ESP32 vs host | 7 |
| Bài C7.3 Sidecar MCAP, upload, audit (gồm Foxglove) | 9 |
| Bài C7.4 Data contract cho robot của chính mình | 4 |
| Gate chặng 7 | 2 |
| **Tổng** | **35** |

Bản gốc dành 14h cho Bài 5 (ghi dữ liệu), không có phần gá cảm biến, TF hay timestamp riêng. Phần thêm là phần người mới tự dựng robot phải làm mà K5 (trên bàn) không làm.

## 0. Bức tranh chặng

```
                    camera USB (UVC, MJPEG) ── cáp USB ngắn, có kẹp giảm lực kéo ──┐
                    gá cứng, nhìn thẳng trước, cao ~ __ cm                          │
   ┌──────────────── NÓC ROBOT ─────────────────────────────────┐                 │
   │   [camera_front_link]                                      │                 ▼
   │        ▲ x (trước)                                         │      ┌─────────────────────┐
   │        │                                                   │      │ MINI PC N100        │
   │   y ◄──● base_link (giữa trục bánh, trên sàn)              │      │ ROS 2 Jazzy/Docker  │
   │        │                                                   │      │ ├ ros2_control (C5) │
   │   [imu_link] gần base_link, trên đế giảm rung              │      │ ├ camera driver     │
   │      │ I2C (xanh dương SDA / vàng SCL) + INT + 3V3 + GND   │      │ ├ imu: stamp nguồn  │
   │      ▼                                                     │      │ ├ SIDECAR: rosbag2  │
   │   ESP32-S3 (C4) ── USB ───────────────────────────────────────►   │ │   → MCAP split    │
   │   ISR data-ready: t_src (esp_timer, µs) + seq                │      │ ├ sealer + manifest │
   └────────────────────────────────────────────────────────────┘      │ └ uploader (K5 B14) │
                                                                        └──────────┬──────────┘
                                                                                   │ Wi-Fi, resumable
                                                                        ┌──────────▼──────────┐
                                                                        │ SERVER / LAPTOP     │
                                                                        │ object store, index │
                                                                        │ audit (K2), Foxglove│
                                                                        └─────────────────────┘
```

Khối mới: IMU (qua ESP32), camera (thẳng vào mini PC), sidecar ghi dữ liệu, và đường dữ liệu ra khỏi robot. Dòng năng lượng: IMU ăn 3,3 V từ ESP32 (vài mA); camera ăn 5 V từ cổng USB của mini PC (vài trăm mA `[tự đo]`): cả hai thuộc nhánh compute/logic, **không** qua điểm cắt E-stop (E-stop cắt động lực, không cắt compute: `_KE-HOACH-K7.md` mục 5). Dòng dữ liệu: mọi luồng → topic ROS 2 chuẩn (`CONVENTIONS.md` mục 3) → MCAP → niêm phong → hàng đợi upload → object store → audit + index.

## 1. An toàn của chặng

**Rủi ro của C7:** khoan/vít gần pin và dây nguồn khi gá cảm biến; chập 3,3 V khi đi dây IMU lúc ESP32 đang có điện; camera và cáp USB vướng vào bánh; chạy robot nhiều giờ để thu dữ liệu (pin xả sâu, motor nóng); lần đầu robot chạy mà bạn **nhìn màn hình Foxglove** thay vì nhìn robot. Và một rủi ro không vật lý: camera ghi hình người trong văn phòng.

**Quy tắc cứng:**
- KHÔNG khoan, bắt vít trên khung khi pin còn cắm. Rút XT60 pin trước, che dây nguồn bằng bìa.
- KHÔNG đi dây IMU khi ESP32 có điện. Ngắt USB và nguồn 5 V logic; đo thông mạch trước khi cấp lại (mục 5, bước 3).
- KHÔNG để cáp camera/USB treo lỏng: kẹp cách bánh ≥ 3 cm, có điểm giảm lực kéo (C2.3) ở cả hai đầu.
- KHÔNG vừa lái robot vừa nhìn dashboard. Một người lái và cầm E-stop tạm; xem dữ liệu sau, hoặc người thứ hai xem.
- KHÔNG ghi hình người khác trong văn phòng khi họ chưa biết và chưa đồng ý. Ở C7, quay camera vào vùng thử không có người, hoặc báo trước và dán thông báo; KHÔNG upload ảnh có mặt người lên dịch vụ ngoài. Quy trình đồng ý đầy đủ là C9.1; ở đây chỉ cần quy tắc tối thiểu này, ghi vào `decisions.md`.
- KHÔNG chạy thu dữ liệu > 0,3 m/s ở chặng này `[đề xuất cho C7, dưới kẹp 0,5 m/s của C4.4]`.
- Các quy tắc pin và chạy tự động của C1, C6 vẫn có hiệu lực.

**Khi sự cố:** chập khi đi dây (khói, mùi nhựa, ESP32 nóng): rút USB và nguồn logic ngay, không chạm chip trong 1 phút, đo lại Ω giữa 3V3 và GND. Cáp vướng bánh: E-stop, tắt động lực, gỡ bằng tay khi bánh đã đứng yên.

## 2. BOM chặng

Giá `[ước lượng 10/2026]`, kiểm lại ở cửa hàng.

| Món | Thông số phải chọn | Vì sao (bằng số) | Giá | Kiểm khi nhận hàng | Thay thế được bằng |
|---|---|---|---|---|---|
| **IMU** ICM-42688-P (module breakout), hoặc dùng lại module đã mua ở K5 M0 | I2C/SPI, chân INT ra header, 3,3 V; có lọc chống aliasing (AAF) cấu hình được và FIFO | Nhiễu gyro ~2,8 mdps/√Hz, accel ~70 µg/√Hz `[spec — TDK DS ICM-42688-P, kiểm]`; AAF cho phép chặn rung motor trước khi hạ tần số (Bài C7.1) | 150–250k | `WHO_AM_I` = 0x47 (K5 Bài 3) | MPU-6050: rẻ, nhiều tài liệu, nhiễu cao hơn nhiều lần (gyro ~0,005 °/s/√Hz, accel ~400 µg/√Hz `[spec — PS-MPU-6000A-00, kiểm]`), DLPF thô hơn; nhiều nguồn ghi đã ngừng sản xuất `[kiểm trang TDK]`, hàng nhái nhiều (K5 Bài 3). Bosch BMI088 (quảng cáo chịu rung cho drone `[spec — Bosch, kiểm]`) nếu rung quá lớn |
| Đế giảm rung | Băng keo xốp hai mặt dày 1–3 mm; hoặc grommet cao su M3; tấm gel silicone | Thử ba kiểu ở C7.1, chọn bằng phổ rung đo được | 30–100k | — | Miếng cao su xe đạp |
| Dây I2C + INT | 5 sợi 24–26 AWG: SDA xanh dương, SCL vàng (C0.5), 3V3 trắng "3V3", GND đen, INT màu riêng có nhãn; dài ≤ 30 cm, đầu JST-XH | I2C 400 kHz không chịu dây dài, tụ ký sinh làm cạnh lên chậm `[chuẩn]` | 20–50k | Thông mạch từng sợi | Cáp Qwiic có sẵn (JST-SH) + adapter |
| **Camera USB** | UVC (không cần driver riêng), **MJPEG** 1280×720 @30 fps, **lấy nét cố định**, FOV ghi rõ, gá ren 1/4" hoặc lỗ vít | MJPEG vừa băng thông USB 2.0 (Bài C7.1); nét cố định để hiệu chuẩn ở C8.2 còn đúng (autofocus đổi tiêu cự) | 300–900k | `v4l2-ctl --list-formats-ext` liệt kê MJPEG 720p30 | Camera global shutter USB (đắt hơn, ít rolling shutter khi rung `[ước lượng]`) |
| Giá camera | Nhôm hoặc nhựa in dày, bắt **hai** vít vào khung | Một vít = trục xoay; rung làm camera lắc | 50–200k | Lắc tay không thấy dịch | — |
| Cáp USB ngắn + kẹp | 0,3–0,5 m, có kẹp dây | Cáp dài treo lỏng vướng bánh, lắc đầu nối | 50–100k | — | — |
| Ổ lưu trên mini PC | Còn trống ≥ 50 GB | Ngân sách dữ liệu (Bài C7.3) | có sẵn | `df -h` | SSD ngoài USB 3 (lưu ý nhiễu 2,4 GHz, Bài C7.1) |

**Tổng C7 `[ước lượng]`:** ~0,6–1,7tr (0 cho IMU nếu dùng lại K5). Object store: MinIO/Garage tự chạy trên laptop như K5 Bài 14 (0đ).

## 3. Dụng cụ và kỹ năng tay

| Kỹ năng | Bài | Luyện trước | Đạt trông thế nào |
|---|---|---|---|
| Gá cảm biến đúng hướng, ghi lại hướng | Lắp bước 1–2 | Vẽ trục x/y/z của chip (in trên module) lên băng keo cạnh module | Ảnh chụp có trục chip và trục `base_link` trên cùng khung hình |
| Đo offset gá bằng thước (x, y, z từ `base_link`) | Lắp bước 4 | Đo một điểm trên robot ba lần | Ba lần lệch ≤ 3 mm |
| Bấm JST-XH 5 chân, đi dây dọc khung | Lắp bước 3 | C0.3 | Dây không căng, có kẹp mỗi 10–15 cm |
| Đọc topo USB | Lắp bước 5 | `lsusb -t` trên laptop | Biết camera nằm trên controller/hub nào, tốc độ 480M hay 5000M |

`base_link` theo `CONVENTIONS.md`: gốc ở giữa trục hai bánh (đúng điểm tham chiếu của C6), `x` tiến, `y` trái, `z` lên. Mọi offset đo từ đó.

## 4. Sơ đồ đi dây

```
  ESP32-S3 (C4)                                         IMU ICM-42688-P (module)
  3V3  ──────────[trắng "3V3", 24 AWG]──────────────────► VDD / VDDIO
  GND  ──────────[đen, 24 AWG]──────────────────────────► GND
  GPIO_SDA ──────[xanh dương]───────────────────────────► SDA   (pull-up 4,7 kΩ lên 3V3: kiểm module đã có chưa)
  GPIO_SCL ──────[vàng]─────────────────────────────────► SCL
  GPIO_INT ◄─────[màu riêng, nhãn "IMU-INT"]────────────  INT1  (data-ready → ISR đóng dấu t_src)
                 dài ≤ 30 cm; xoắn SCL với một sợi GND nếu chạy gần dây motor
  Cùng bus I2C với INA226 (C1.5): địa chỉ INA226 0x40–0x4F, IMU 0x68/0x69 `[spec]` → không trùng; quét bus để xác nhận (K5 Bài 3)

  Mini PC  USB-A ──[cáp 0,3–0,5 m, kẹp hai đầu]──► camera UVC
           USB   ──[cáp C4]────────────────────────► ESP32-S3
```

**Bảng chân:** chân I2C và INT lấy từ bảng chân (pin budget) của C4.1, không chọn mới ở đây. Nếu bảng chưa có INT: chọn một GPIO **không** phải chân strapping (ESP32-S3: GPIO0, 3, 45, 46 `[spec — ESP32-S3 datasheet, mục Strapping Pins, kiểm]`) và không phải USB (GPIO19/20 `[spec]`), cập nhật bảng chân C4.1 và `wiring/wires.csv`. Màu INT không có trong quy ước C0.5: chọn một màu, thêm dòng vào `CONVENTIONS.md` mục "Dây", ghi `decisions.md`.

## 5. Trình tự chặng

1. **Học Bài C7.1** phần 1–5 (commit `prediction.md`).
2. **Lắp bước 1 — Gá IMU** gần `base_link` (càng gần trục bánh càng ít gia tốc hướng tâm khi quay), mặt chip song song sàn, trục x chip theo trục x robot nếu được. Làm **ba** đế để so: vít cứng qua standoff, băng xốp, grommet cao su.
   - ✅ Checkpoint: module không lắc khi gõ nhẹ bằng bút; không chạm khung kim loại ở mặt dưới (chập chân).
3. **Lắp bước 2 — Gá camera** bằng hai vít, nhìn thẳng trước, không thấy thân robot trong khung hình (hoặc thấy một phần cố định, ghi lại). Cáp kẹp hai đầu.
   - ✅ Checkpoint: lắc nhẹ robot, ảnh trên màn hình không giật lệch so với khung.
4. **Lắp bước 3 — Đi dây I2C + INT** theo mục 4, ESP32 **không** có điện.
   - ✅ Checkpoint trước khi cấp điện: Ω giữa 3V3 và GND của IMU **không** gần 0; thông mạch từng sợi đầu–cuối; không thông mạch giữa SDA và SCL. Cấp điện qua USB từ laptop (không phải pin) lần đầu.
   - Nếu sai: tháo, bấm lại đầu JST.
   - Sau cấp điện: quét bus thấy 0x68/0x69 và địa chỉ INA226; `WHO_AM_I` đúng (K5 Bài 3).
5. **Lắp bước 4 — URDF/TF tĩnh**: đo offset (x, y, z) của IMU và camera từ `base_link` bằng thước, góc gá bằng thước đo độ/ê-ke; thêm hai joint `fixed` vào URDF của C5 (Bài C7.1 mục 6).
   - ✅ Checkpoint: robot đứng yên, `/imu/data_raw` trong `imu_link` biến đổi sang `base_link` cho gia tốc ≈ +g theo `z` (rule `gravity_up`, Bài C7.4).
6. **Lắp bước 5 — Camera trên hệ thống**: udev rule cho tên thiết bị cố định (theo serial/đường cổng), đưa vào container (C5.2), chạy driver camera.
   - ✅ Checkpoint: `ros2 topic hz` của ảnh nén đạt fps đặt ±5 % trong 5 phút khi `ros2_control` cũng đang chạy.
7. **Làm Bài C7.1** mục 6 (đo rung, chọn đế và lọc; đo băng thông USB).
8. **Học và làm Bài C7.2** (timestamp).
9. **Học và làm Bài C7.3** (sidecar, upload, audit, Foxglove).
10. **Học và làm Bài C7.4** (data contract; chạy lại bước va chạm của C6.3 với gyro).
11. **Gate chặng 7.**

Robot vẫn chạy được ở phạm vi nhỏ hơn suốt chặng: teleop và odometry C5–C6 không phụ thuộc IMU, camera hay sidecar. Sidecar chết thì robot vẫn chạy (và Bài C7.3 kiểm đúng điều đó).

## 6. Lỗi người mới hay gặp

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| IMU đọc bình thường trên bàn, rác khi motor chạy | Nhiễu motor lên dây I2C; ground chung với đường dòng motor | Logic analyzer trên SDA/SCL khi motor chạy | Dây ngắn, xoắn với GND, tách xa dây motor; ground hình sao (C1) |
| `VIDIOC_STREAMON: No space left on device` | Hết băng thông isochronous USB (định dạng thô, hai camera chung controller) | `dmesg`, `lsusb -t` | MJPEG; độ phân giải thấp hơn; cổng/controller khác |
| Camera ra 15 fps dù đặt 30 | Phơi sáng tự động dài trong phòng tối; định dạng không hỗ trợ 30 fps | `v4l2-ctl --all` xem exposure | Tắt auto exposure, đặt exposure ≤ 1/fps; thêm đèn |
| Wi-Fi upload chậm/đứt khi camera cắm cổng USB 3 | Nhiễu băng 2,4 GHz từ USB 3 `[chuẩn — Intel white paper 2012]` | Đổi camera sang cổng USB 2, đo lại iperf3 | Cổng USB 2, cáp bọc chống nhiễu, Wi-Fi 5 GHz |
| TF đúng trên giấy, `gravity_up` FAIL | IMU úp ngược hoặc xoay 90° mà URDF chưa ghi | Đặt robot đứng yên, đọc accel thô | Sửa rpy trong URDF (Bài C7.1) |
| Ổ mini PC đầy sau một buổi | Ghi ảnh thô, không split, không xóa sau upload | `du -sh` thư mục bag | MJPEG nén; split; chính sách xóa sau xác nhận (Bài C7.3) |

## 7. Lăng kính data infra

**Dữ liệu chặng này sinh ra** (giữ tần số bản gốc Bài 5; message và frame theo `CONVENTIONS.md`):

| Luồng | Message | Topic | Frame | Tần số | Nguồn timestamp |
|---|---|---|---|---|---|
| Encoder | `sensor_msgs/msg/JointState` | `/joint_states` | — | 100 Hz | host (controller), `host_unsynced` |
| Lệnh PWM / lệnh vận tốc | lệnh của controller (ví dụ `TwistStamped`), PWM qua topic chẩn đoán của C4/C5 `[tự đo]` | `/cmd_vel`, PWM theo C5 | — | 100 Hz | host |
| IMU | `sensor_msgs/msg/Imu` | `/imu/data_raw` | `imu_link` | 200 Hz | nguồn ESP32 đã ánh xạ (`estimated`), hoặc host (Bài C7.2) |
| Đối chiếu đồng hồ | `sensor_msgs/msg/TimeReference` | `/esp32/time_reference` | — | 1–10 Hz | `header.stamp` = host nhận, `time_ref` = ESP32 |
| Odometry | `nav_msgs/msg/Odometry` | `/odom` | `odom` → `base_link` | 50 Hz | host |
| Pin | `sensor_msgs/msg/BatteryState` | `/battery` | — | 1 Hz | host |
| Camera | `sensor_msgs/msg/CompressedImage` + `CameraInfo` | `/camera_front/image/compressed` | `camera_front_optical_frame` | 10–30 fps | host lúc driver nhận (Bài C7.2) |
| TF tĩnh | `tf2_msgs/msg/TFMessage` | `/tf_static` | — | một lần (latched) | — |
| Chẩn đoán | `diagnostic_msgs/msg/DiagnosticArray` | `/diagnostics` | — | 1 Hz | host |

Metadata theo `CONVENTIONS.md` mục 4 (`metadata_version`, `calibration_id`, `clock_source`, `source_device_id`, `firmware_version`) đi vào **metadata của channel và Metadata record MCAP** lúc niêm phong (Bài C7.3), không chèn vào message. Mất gói host ↔ ESP32 đếm bằng số thứ tự ở tầng truyền, báo qua `/diagnostics`.

**Test tự động sinh ra (hạt giống HIL/CI cho C11):**
- Data contract (Bài C7.4) chạy trên mọi file sau niêm phong: là test của **pipeline ghi**, cũng là test hồi quy khi đổi firmware, đổi driver, đổi URDF.
- `kill -9` sidecar và rút Wi-Fi giữa phiên (Bài C7.3): file vẫn cứu được, upload tiếp tục, không trùng. Ở C11.2 thành kịch bản fault injection chạy định kỳ.
- Rule `gravity_up` chặn mọi file có TF/đơn vị IMU sai: một cấu hình URDF sai không bao giờ lọt vào dataset.

**SLI/SLO đề xuất (→ F7.4):** tỉ lệ file niêm phong qua contract; độ trễ ghi → có trên object store (p95); tỉ lệ mẫu IMU mất theo `seq`; số byte chờ upload trên robot; tuổi của file cũ nhất chưa upload.

**Vai trò nghề:** Data Platform (ingest, niêm phong, upload, index, contract) và Test & Validation (rule vật lý có tiền điều kiện, fault injection lên pipeline). Đây là phần giống nhất với công việc bạn nhắm tới.

## 8. Nhật ký build

Copy vào `build-log/c07.md`, một mục mỗi buổi:

```markdown

## 2026-MM-DD — buổi N (giờ bắt đầu–kết thúc, giờ thực: _._ h)
- Trạng thái người: tỉnh táo / mệt (mệt → chỉ phân tích dữ liệu, không khoan, không đi dây)
- E-stop tạm đã thử đầu buổi (nếu robot chạy): có / không
- Phần cứng đã đổi (gá, dây, cổng USB): ... · ảnh: build-log/img/c07/...
- firmware_version / URDF commit / calibration_id đang dùng: ...
- Phiên ghi: session_id, thời lượng, số file, tổng MB, đã upload? đã qua contract?
- Số đo (rung RMS, fps thật, offset/skew đồng hồ, jitter): vào measurements.jsonl? số dòng: __
- Lỗi gặp (triệu chứng → nguyên nhân → sửa):
- Có ghi hình người không? Ai đã đồng ý? (C9.1 sẽ thay dòng này bằng quy trình)
- Quyết định (ghi decisions.md):
- Câu hỏi còn mở:
```

---

## Bài C7.1 — Gá cảm biến: rung, frame, TF tĩnh, băng thông USB (8h)

> **Vị trí:** C6 → **C7.1** → C7.2 (timestamp) · **Cần trước:** K5 Bài 3–4 (IMU qua I2C, raw → SI), → F5.5 (Nyquist, aliasing), → F5.6 mục 2 (phổ, lọc), K2 Bài 3 (frame và TF), → F1.1 · **Sau bài này bạn quyết định được:** gá IMU bằng đế nào và đặt lọc bao nhiêu; IMU chạy ODR nào; camera chạy định dạng, độ phân giải, fps nào trên cổng nào; offset và góc gá nào đi vào URDF, ghi ở đâu.

### 1. Câu chuyện — ai đã khổ vì chuyện này

Cộng đồng autopilot mã nguồn mở cho drone (ArduPilot, PX4) học bài này bằng máy bay rơi: rung của cánh quạt đi qua khung vào accelerometer, bị lấy mẫu thành tín hiệu tần số thấp giả, bộ ước lượng tin đó là chuyển động thật, và máy bay mất độ cao hoặc tự trôi. Tài liệu ArduPilot có hẳn trang "Measuring Vibration": firmware ghi mức rung (log `VIBE`) và hướng dẫn coi mức rung vượt ngưỡng là lỗi phải sửa bằng đế giảm rung **trước** khi chỉnh bất kỳ tham số điều khiển nào `[chuẩn — ArduPilot docs, kiểm ngưỡng cụ thể]`.

Robot của bạn chậm hơn drone nhiều, nhưng có motor DC giảm tốc quay nhanh ngay cạnh IMU, gắn trên cùng tấm khung. Lỗi gá ở chặng này không làm robot rơi; nó làm **dữ liệu** sai theo cách trông rất hợp lý, và mọi thứ dùng dữ liệu đó (bộ hợp nhất C8.3, dataset C11.5) thừa hưởng lỗi.

### 2. Mô hình tư duy

Gá một cảm biến quyết định ba thứ, và mỗi thứ có một cách kiểm riêng:

| Gá quyết định | Sai thì | Kiểm bằng |
|---|---|---|
| **Tín hiệu vật lý nào tới cảm biến** (đường truyền rung) | Rung motor thành "chuyển động ma" sau khi lấy mẫu | Phổ rung đo trên robot (mô phỏng 1, mục 6) |
| **Dữ liệu được biểu diễn trong frame nào** (TF tĩnh) | Gia tốc, góc quay đúng độ lớn nhưng sai trục/sai dấu | Vật lý đã biết: đứng yên thì +g hướng lên (mô phỏng 2) |
| **Dữ liệu có ra khỏi được thiết bị không** (băng thông bus) | Rớt frame, camera không bật, nhiễu sang Wi-Fi | Tính ngân sách băng thông, đo fps thật |

**Mô phỏng 1 — rung 170 Hz lấy mẫu ở 200 Hz.** Tần số rung là giả định (`[ước lượng]`; bạn đo cái thật ở mục 6).

```python
# [đã chạy] Rung motor 170 Hz lấy mẫu ở ODR 200 Hz: không lọc chống aliasing -> "chuyển động ma" 30 Hz
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import signal
FS_IN, ODR, T = 8000, 200, 10.0                    # mô phỏng "liên tục" 8 kHz; IMU xuất 200 Hz; 10 s
t = np.arange(0, T, 1 / FS_IN)
motion = 0.3 * np.sin(2 * np.pi * 1.0 * t)         # chuyển động thật của thân: 1 Hz, 0,3 m/s²
vib = 2.0 * np.sin(2 * np.pi * 170 * t)            # rung từ motor/hộp số: 170 Hz, 2 m/s² [ước lượng]
a = motion + vib
step = FS_IN // ODR
raw = a[::step]                                    # (a) lấy mẫu tức thời, không lọc trước
sos = signal.butter(2, 50, fs=FS_IN, output="sos") # (b) lọc thông thấp 50 Hz TRƯỚC khi hạ tần số
filt = signal.sosfilt(sos, a)[::step]              #     (IMU làm việc này bên trong nếu bạn cấu hình đúng)
ts = t[::step]
def amp_at(x, f0):                                  # biên độ thành phần tần số f0 trong chuỗi 200 Hz
    X = np.fft.rfft(x * np.hanning(x.size)); f = np.fft.rfftfreq(x.size, 1 / ODR)
    return 2 * np.abs(X[np.argmin(abs(f - f0))]) / np.hanning(x.size).sum()
for name, x in [("không lọc", raw), ("lọc 50 Hz trước", filt)]:
    print(f"{name:16s} biên độ ở 1 Hz = {amp_at(x, 1):.2f}  ở 30 Hz (ma) = {amp_at(x, 30):.3f} m/s²"
          f"  | std(a − chuyển động thật) = {np.std(x - 0.3*np.sin(2*np.pi*ts)):.3f}")
plt.plot(ts[:100], raw[:100], label="không lọc"); plt.plot(ts[:100], filt[:100], label="lọc trước")
plt.plot(ts[:100], 0.3*np.sin(2*np.pi*ts[:100]), "k--", label="thật"); plt.legend(); plt.xlabel("t (s)")
plt.savefig("c71_alias.png")                       # trong bài: plt.show()
```

Ba ý bản chất: (1) sau khi đã lấy mẫu, **không** phần mềm nào phân biệt được 30 Hz ma với 30 Hz thật (→ F5.5); lọc phải xảy ra **trước** bước hạ tần số, tức là trong chip (DLPF/AAF của IMU, nó lấy mẫu nội bộ ở tần số cao hơn ODR) hoặc bằng cơ khí (đế giảm rung). (2) Lọc có giá: trễ pha, nên băng thông lọc là thỏa hiệp với vòng điều khiển/ước lượng dùng IMU. (3) Đế mềm là một bộ lọc cơ khí thông thấp; quá mềm thì nó **cộng hưởng** ở tần số riêng của nó và khuếch đại rung ở đó.

**Mô phỏng 2 — TF tĩnh: kiểm rpy bằng câu hỏi "trục nào đi đâu".** URDF và `static_transform_publisher` dùng roll–pitch–yaw quanh trục cố định; nhầm thứ tự hay dấu là lỗi phổ biến nhất.

```python
# [đã chạy] Kiểm TF tĩnh trước khi tin: rpy của URDF -> ma trận, rồi hỏi "trục nào đi đâu"
import numpy as np
def rpy_to_R(r, p, y):
    """URDF/ROS: quay quanh trục CỐ ĐỊNH x (roll), rồi y (pitch), rồi z (yaw): R = Rz·Ry·Rx."""
    cx, sx, cy, sy, cz, sz = np.cos(r), np.sin(r), np.cos(p), np.sin(p), np.cos(y), np.sin(y)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx
names = {"x": 0, "y": 1, "z": 2}
def where(R, parent="cha", child="con"):
    """Cột i của R = trục i của frame con, viết trong frame cha."""
    for ax, i in names.items():
        v = np.round(R[:, i], 3) + 0.0
        print(f"  trục {ax} của {child} = {v} trong {parent}")
# 1) camera_link (x trước, y trái, z lên, REP-103) -> camera_optical_frame (z trước, x phải, y xuống)
R = rpy_to_R(-np.pi / 2, 0, -np.pi / 2)
print("camera_link -> optical, rpy = (-pi/2, 0, -pi/2):"); where(R, "camera_link", "optical")
assert np.allclose(R[:, 2], [1, 0, 0]) and np.allclose(R[:, 0], [0, -1, 0]) and np.allclose(R[:, 1], [0, 0, -1])
# 2) IMU gắn úp ngược (chip quay mặt xuống), trục x của chip vẫn hướng trước: base_link -> imu_link
R_imu = rpy_to_R(np.pi, 0, 0)
print("base_link -> imu_link (úp ngược):"); where(R_imu, "base_link", "imu_link")
# Kiểm bằng vật lý: robot đứng yên, accel đo trong imu_link phải là +g theo trục lên của base_link
a_imu = R_imu.T @ np.array([0, 0, 9.81])           # lực riêng khi đứng yên: +g hướng LÊN (REP-103 z lên)
print("  accel đứng yên đọc ở imu_link:", np.round(a_imu, 2), "-> trục z của chip đọc âm là đúng")
```

Accelerometer đo **lực riêng** (specific force), không đo gia tốc: đứng yên trên bàn nó đọc +g hướng **lên** (K5 Bài 4). Đó là phép kiểm TF miễn phí mà bạn luôn có.

**Băng thông USB, bằng số** (→ F7.1 nếu muốn nhìn như một hàng đợi): USB 2.0 High-Speed 480 Mbit/s; truyền đẳng thời (isochronous, kiểu mà camera UVC dùng cho video) **đặt trước** băng thông mỗi vi khung 125 µs, tối đa 3 × 1024 byte mỗi endpoint mỗi vi khung, và tổng truyền định kỳ không quá 80 % vi khung `[spec — USB 2.0 Specification, mục 5.6 và 5.7]`. Ngân sách một luồng thô: `rộng × cao × byte/pixel × fps` (YUYV = 2 byte/pixel). MJPEG nén từng ảnh, kích thước đổi theo cảnh `[tự đo]`.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Prometheus scrape mỗi 15 s: một counter dao động nhanh trông như đứng yên hoặc dao động chậm | IMU ODR 200 Hz lấy mẫu rung 170 Hz | Exporter không có cách lọc trước khi scrape; IMU **có** (DLPF/AAF) và đế cơ khí cũng là bộ lọc. Ở đây bạn sửa được ở nguồn | "Tăng scrape rate là xong": tăng ODR mà không lọc vẫn alias rung ở tần số cao hơn nữa |
| Hợp đồng đơn vị/định dạng giữa service (ms hay s, UTC hay local) | TF tĩnh: dữ liệu IMU ở `imu_link`, người dùng cần `base_link` | Lỗi đơn vị backend thường làm số sai nhiều bậc, dễ thấy. Lỗi trục/dấu cho số **đúng độ lớn**, trông hợp lý | Robot "rẽ trái" trong dữ liệu khi thật ra rẽ phải; bộ hợp nhất C8.3 đánh nhau với odometry |
| QoS mạng: băng thông đặt trước vs best effort | Isochronous (video, đặt trước) vs bulk (ổ đĩa, serial) | Mạng backend cho bạn thử rồi chậm dần; USB isochronous **từ chối ngay** lúc mở luồng nếu không đủ chỗ đặt trước | Cắm thêm camera thứ hai, cái đầu đang chạy bình thường, cái sau báo lỗi khó hiểu |

**Chấm mô hình:**

1. *"IMU 200 Hz thì thấy đúng mọi chuyển động tới 100 Hz, phần trên 100 Hz chỉ bị mất."* **SAI.** Phần trên Nyquist không mất; nó **gập xuống** dưới 100 Hz và cộng vào tín hiệu thật. **Phản ví dụ:** mô phỏng 1: rung 170 Hz xuất hiện ở 30 Hz với nguyên biên độ.
2. *"Data đi qua dây data; cách đọc/ghi, schema phải dùng các dây khác như clock để phối hợp"* (mô hình của bạn ở K3 lượt 2), áp vào chuyện gá IMU: "dây I2C đúng, WHO_AM_I đúng thì dữ liệu đúng". **ĐÚNG MỘT PHẦN.** Đúng cho tầng truyền. Gãy ở chỗ ý nghĩa của ba con số accel (trục nào của **robot**) không nằm trên dây nào, cũng không nằm trong datasheet: nó nằm trong cách bạn vặn con chip vào khung, và chỉ được ghi lại trong URDF. **Phản ví dụ:** cùng chip, cùng dây, xoay 90° trên khung: mọi byte hợp lệ, `x` của chip thành `y` của robot.
3. *"Đế càng mềm càng tốt cho IMU."* **ĐÚNG MỘT PHẦN.** Mềm hơn cắt rung tần số cao tốt hơn, nhưng hạ tần số cộng hưởng của đế xuống; nếu nó rơi vào dải chuyển động thật hoặc dải rung khác (bánh lăn qua mạch gạch), đế khuếch đại. **Phản ví dụ:** IMU trên miếng xốp dày lắc lư khi robot tăng tốc, gyro thấy "nghiêng" không có thật.

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | ODR (output data rate) | Tần số IMU xuất mẫu ra ngoài | Tần số lấy mẫu bên trong chip (thường cao hơn) |
| 🟢 | Aliasing | Thành phần trên Nyquist gập xuống thành tần số thấp giả | Mất dữ liệu tần số cao |
| 🟢 | DLPF / AAF | Lọc thông thấp số / chống aliasing bên trong IMU, trước khi hạ xuống ODR | Lọc phần mềm trên host (quá muộn) |
| 🟢 | Lực riêng (specific force) | Thứ accelerometer đo: gia tốc trừ trọng trường; đứng yên đọc +g lên | "Gia tốc của robot" |
| 🟢 | TF tĩnh, joint `fixed` | Biến đổi không đổi theo thời gian giữa hai frame, publish một lần trên `/tf_static` | Biến đổi đo một lần là đúng mãi (gá có thể xê dịch) |
| 🟢 | Optical frame | Frame camera theo quy ước ảnh: z trước, x phải, y xuống | `camera_link` (x trước, z lên) |
| 🟡 | Isochronous / bulk (USB) | Băng thông đặt trước, không gửi lại / phần còn lại, có gửi lại | "USB 480 Mbit/s là của mỗi thiết bị" |
| 🟡 | Tần số cộng hưởng của đế | Tần số đế giảm rung khuếch đại thay vì giảm | — |
| 🔴 | Hiệu chuẩn ngoại (extrinsic) camera–IMU bằng tối ưu | Ước lượng chính xác TF camera–IMU từ dữ liệu chuyển động | — |

### 5. Dự đoán

**Đề:**
1. Ở vận tốc robot 0,1 / 0,2 / 0,3 m/s, trục motor quay bao nhiêu Hz? Tần số "gear mesh" của cấp bánh răng đầu tiên? Ở ODR 200 Hz không lọc, những tần số đó alias về đâu?
2. RMS rung (accel, m/s²) trên ba kiểu đế (vít cứng, băng xốp, grommet) khi bánh quay trên giá kê ở 0,3 m/s: xếp hạng, và tỉ số giữa tốt nhất và tệ nhất.
3. Băng thông USB của camera ở ba chế độ: YUYV 640×480@30, YUYV 1280×720@30, MJPEG 1280×720@30. Chế độ nào **không thể** chạy trên USB 2.0? Hai camera YUYV 640×480@30 cùng một controller có chạy không?
4. Accel đứng yên trong `imu_link` của robot bạn (theo cách bạn đã gá): ba trục đọc gì?

**Tham số cần tra:** bán kính bánh (C6), tỉ số truyền và PPR (C3, datasheet motor), số răng bánh răng cấp đầu (nếu nhà bán có; không có thì bỏ câu đó); thanh ghi DLPF/AAF và ODR của IMU (datasheet ICM-42688-P mục cấu hình bộ lọc; MPU-6050: `CONFIG` 0x1A); định dạng camera hỗ trợ (`v4l2-ctl --list-formats-ext`); topo USB (`lsusb -t`).

**Công thức:** `f_motor = v / (2π r) × N_truyền`; alias của `f` ở ODR `fs`: `|f − k·fs|` nhỏ nhất với k nguyên; băng thông thô = `W × H × 2 × fps` byte/s; so với ~24,6 MB/s mỗi endpoint isochronous (3 × 1024 B × 8000 vi khung/s) và 80 % của bus.

```markdown
# prediction.md — K7 C7.1
commit: <hash>
| Đại lượng | Dự đoán | Cách tính |
|---|---|---|
| f_motor ở 0,1/0,2/0,3 m/s (Hz) | | |
| Alias ở ODR 200 Hz (Hz) | | |
| RMS rung: vít / xốp / grommet (m/s²) | | |
| Băng thông YUYV VGA30 / YUYV 720p30 / MJPEG 720p30 (MB/s) | | |
| Chế độ không chạy được trên USB 2.0 | | |
| Accel đứng yên trong imu_link (x, y, z) | | |
## Tôi sẽ ngạc nhiên nếu...
```

### 6. Làm

**A. Rung và lọc (3h).**
1. Firmware (C4) đặt IMU ở ODR cao nhất mà đường serial chịu được để **nhìn** phổ (ví dụ 1 kHz, gói nhỏ `[tự đo]`), DLPF/AAF **rộng nhất**. Đây là chế độ đo, không phải chế độ chạy.
2. Với từng đế (vít, xốp, grommet): robot trên giá kê, bánh quay ở 0,1 / 0,2 / 0,3 m/s, ghi 30 s mỗi mức; rồi robot chạy thẳng trên sàn gạch 0,2 m/s. Ghi `V_bat`.
3. Tính phổ (Welch, `scipy.signal.welch`, → F5.6) và RMS accel/gyro trên dải > 20 Hz cho mỗi lần. Tìm đỉnh: có trùng `f_motor`, bội của nó, hay tần số khác (bánh xe, caster)?
4. Chọn đế có RMS nhỏ nhất **mà** không có đỉnh cộng hưởng mới dưới 20 Hz. Đặt ODR chạy (200 Hz theo `CONVENTIONS.md`) và DLPF/AAF dưới ODR/2 với lề; ghi lý do và số vào `decisions.md`. Ghi lại 30 s ở cấu hình chạy: đỉnh rung còn bao nhiêu sau khi gập.
5. Ghi `calibration_id` của IMU (`imu-01@<ngày>-a`) cùng cấu hình bộ lọc; đo bias gyro tĩnh 10 phút (K5 Bài 4) **trên robot**, không phải trên bàn.

**B. TF tĩnh (2h).**
6. Đo offset IMU và camera từ `base_link` (thước thép, ±3 mm `[ước lượng]`; z tính từ mặt sàn). Ghi góc gá: nếu chip/camera thẳng hàng với khung, góc = 0 với độ bất định ±2° `[ước lượng]`.
7. Thêm vào URDF của C5 (dùng `robot_state_publisher` publish `/tf_static`):

```xml
<!-- [chưa chạy] Thêm vào URDF của C5. Số là VÍ DỤ: thay bằng số đo của bạn (m, rad). -->
<link name="imu_link"/>
<joint name="imu_joint" type="fixed">
  <parent link="base_link"/><child link="imu_link"/>
  <origin xyz="0.020 0.000 0.085" rpy="0 0 0"/>          <!-- úp ngược: rpy="3.14159 0 0" -->
</joint>
<link name="camera_front_link"/>
<joint name="camera_front_joint" type="fixed">
  <parent link="base_link"/><child link="camera_front_link"/>
  <origin xyz="0.120 0.000 0.210" rpy="0 0.10 0"/>        <!-- pitch dương = chúc xuống (REP-103) -->
</joint>
<link name="camera_front_optical_frame"/>
<joint name="camera_front_optical_joint" type="fixed">
  <parent link="camera_front_link"/><child link="camera_front_optical_frame"/>
  <origin xyz="0 0 0" rpy="-1.5708 0 -1.5708"/>           <!-- kiểm bằng mô phỏng 2 -->
</joint>
```

8. Kiểm bằng vật lý: robot đứng yên trên sàn phẳng, `ros2 run tf2_ros tf2_echo base_link imu_link` `[tự đo cú pháp]`, rồi biến đổi accel trung bình 10 s sang `base_link`: z ≈ +g, x, y ≈ 0 (trong dung sai dựng của sàn và gá). Quay robot tại chỗ bằng teleop: `ω_z` gyro trong `base_link` **dương** khi quay trái. Camera: giơ một vật trước robot lệch sang **trái**; trong ảnh nó phải ở nửa trái, và tọa độ x trong optical frame âm.
9. Quyết định **một** chỗ xử lý hướng gá: hoặc URDF ghi xoay (khuyến nghị: dữ liệu thô giữ trục chip, TF nói sự thật), hoặc firmware hoán trục trước khi gửi. Không làm cả hai. Ghi `decisions.md`.

**C. Camera và băng thông USB (3h).**
10. `lsusb -t`: camera và ESP32 nằm trên controller/hub nào, tốc độ bao nhiêu. `v4l2-ctl -d /dev/<camera> --list-formats-ext` `[tự đo]`.
11. Thử ba chế độ ở đề 3. Với mỗi chế độ: luồng có mở không (`dmesg` khi lỗi), fps thật trong 5 phút (`ros2 topic hz`), băng thông topic (`ros2 topic bw`), CPU của driver (`top`).
12. Chọn chế độ chạy (gợi ý xuất phát: MJPEG 1280×720 hoặc 640×480 ở 15–30 fps theo nhu cầu C8.2) và **khóa** exposure, white balance, focus (nếu có) bằng `v4l2-ctl` hoặc tham số driver `[tự đo tên tham số]`: tự động thay đổi những thứ này làm đổi thời điểm giữa phơi sáng (C7.2) và đổi tiêu cự (C8.2).
13. Nếu dùng Wi-Fi 2,4 GHz: đo `iperf3` từ robot về server với camera ở cổng USB 3 và ở cổng USB 2.
14. Chạy robot thẳng 0,2 m/s, xem ảnh: nhòe chuyển động và "lắc thạch" (rolling shutter khi rung). Ghi vào `decisions.md` nếu cần giảm exposure.

### 7. Số phải ra

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

**Mô phỏng 1:** không lọc: thành phần ma 30 Hz biên độ **2,0 m/s²**, gần **7 lần** chuyển động thật 0,3 m/s²; std sai lệch ~1,4 m/s². Lọc thông thấp bậc 2 ở 50 Hz trước khi hạ tần số: ma còn ~0,17 m/s² (bậc 2 suy giảm ~ (170/50)² ≈ 12 lần), sai lệch ~0,12 m/s² (một phần là trễ pha của bộ lọc).

**Mô phỏng 2:** rpy `(−π/2, 0, −π/2)` đưa `z` optical về `x` của `camera_link`, `x` optical về `−y`, `y` optical về `−z`: đúng quy ước optical. IMU úp ngược: đứng yên đọc `a_z ≈ −g` ở chip, và URDF có `roll = π` biến nó thành +g trong `base_link`.

**Tần số motor** `[ước lượng]` với bánh r ≈ 32,5 mm, tỉ số truyền ~30–50: ở 0,2 m/s bánh ~1 vòng/s, trục motor ~30–50 Hz; ở 0,3 m/s ~45–75 Hz. Gear mesh của cấp đầu là bội số răng của tần số trục, thường hàng trăm Hz trở lên: đó là chỗ đỉnh phổ hay nằm, và ở 200 Hz không lọc chúng gập vào dải chuyển động.

**Đế** `[ước lượng]`: vít cứng thường cho RMS > 20 Hz cao nhất; xốp mỏng hoặc grommet giảm vài lần; xốp dày có thể xuất hiện cộng hưởng dưới 20 Hz. Số của bạn là số đúng.

**Băng thông USB:**

| Chế độ | Băng thông thô | Trên USB 2.0 HS |
|---|---|---|
| YUYV 640×480@30 | 18,4 MB/s | Một camera chạy được (< ~24,6 MB/s/endpoint) |
| YUYV 1280×720@30 | 55,3 MB/s | **Không thể**: vượt cả endpoint lẫn 80 % bus (48 MB/s). Camera thường chỉ cho YUYV 720p ở 5–10 fps |
| MJPEG 1280×720@30 | vài MB/s `[ước lượng 50–150 KB/ảnh]` | Chạy được; CPU giải nén nếu cần ảnh thô |

Hai camera YUYV VGA@30 trên một controller: tổng 36,8 MB/s < 48 MB/s nên **trên lý thuyết** vừa, nhưng nhiều camera UVC xin băng thông theo kích thước gói tối đa thay vì nhu cầu thật, nên camera thứ hai hay bị từ chối `[tự đo]`. Đó là lý do mặc định MJPEG.

**Accel đứng yên:** theo cách bạn gá; nếu chip phẳng, mặt lên: `(≈0, ≈0, ≈+9,8)` m/s² trong dung sai offset (K5 Bài 4).

</details>

### 8. Nếu ra khác

| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|
| Phổ có đỉnh ở mọi tốc độ cùng một tần số | Cộng hưởng khung/đế, không phải motor | Gõ nhẹ khung khi motor tắt, xem phổ | Đổi đế; thêm điểm bắt vít cho tấm gá |
| Đỉnh dịch theo tốc độ, tỉ lệ đúng với `f_motor` | Rung motor/hộp số | — | Đế + lọc; kiểm motor có lệch tâm, bánh có đảo |
| Gyro đứng yên trên robot khác trên bàn | Nhiệt (gần driver/mini PC), ứng suất cơ khi siết vít | Đo bias theo nhiệt độ chip | Gá xa nguồn nhiệt; không siết vít ép module |
| `ω_z` âm khi quay trái | Trục z chip ngược, TF chưa ghi | Bước 8 | Sửa rpy URDF (hoặc hoán trục firmware, chỉ một nơi) |
| Ảnh lộn ngược / vật bên trái hiện bên phải | Camera gá ngược; optical frame sai | Bước 8 | Xoay camera, hoặc rpy; KHÔNG lật ảnh trong driver mà không sửa TF |
| fps thật thấp hơn đặt, CPU driver cao | Giải nén MJPEG trên host rồi nén lại | `top` | Ghi thẳng ảnh nén (`CompressedImage`) không giải nén |

### 9. Câu hỏi ngược

1. **[Nếu…thì]** Nếu bạn tăng ODR IMU lên 1 kHz và lọc trên host bằng phần mềm, có thay được AAF trong chip không? Nếu có, giá là gì?
<details><summary>Hướng nghĩ</summary>

Có, nếu 1 kHz đủ cao để mọi rung đáng kể nằm dưới 500 Hz (đo phổ ở bước A mới biết). Giá: 5× băng thông serial và dung lượng, thêm tải CPU, và vẫn alias nếu có thành phần trên 500 Hz. Lọc trong chip miễn phí và ở đúng chỗ, nhưng bạn phải tin cấu hình chip (đọc lại thanh ghi).

</details>

2. **[Quy mô]** 100 robot cùng thiết kế, lắp bởi 3 người khác nhau. Gá IMU lệch vài độ, đế mềm cứng khác nhau. Cái gì trong dataset gãy trước, và bạn phát hiện bằng dữ liệu nào mà không phải đi xem từng con?
<details><summary>Hướng nghĩ</summary>

TF tĩnh trong URDF là của **thiết kế**, không của **từng con**: lệch gá thành bias trục chéo (gravity rò sang x/y). Phát hiện bằng rule đứng yên (`gravity_up` mở rộng cho x/y) và phổ rung theo `robot_id`. Cần `calibration_id` theo từng robot cho cả TF, không chỉ cho hệ số.

</details>

3. **[Failure mode]** Một vít gá camera lỏng dần sau hai tuần. Dữ liệu nào lộ ra trước khi ai đó nhìn thấy bằng mắt?
<details><summary>Hướng nghĩ</summary>

Ảnh rung khi robot đứng yên mà motor chạy (rung tần số motor trong luồng ảnh); pose marker (C8) có phần dư lớn dần và có hướng; extrinsic hiệu chuẩn ở C8.2 không còn đúng. Một phép kiểm định kỳ: chụp một mục tiêu cố định khi robot ở trạm sạc.

</details>

4. **[Vì sao không]** Vì sao không cắm IMU thẳng vào mini PC qua một adapter USB–I2C, khỏi đi qua ESP32?
<details><summary>Hướng nghĩ</summary>

Được, nhưng mất thứ C7.2 cần: một đồng hồ tất định đóng dấu ngay lúc data-ready. Adapter USB–I2C bị host thăm dò theo lịch USB; thời điểm đọc trên host là thời điểm của lịch, không của mẫu. Và kiến trúc K7 đã quyết mọi tín hiệu phần cứng đi qua ESP32 (mini PC không có GPIO).

</details>

### 10. Liên kết ra ngoài

- **Âm thanh số: lọc chống aliasing trước ADC.** Mọi ADC âm thanh có lọc tương tự (hoặc oversampling + lọc số) trước khi hạ xuống 44,1/48 kHz; K3 đã gặp phía phát. Giống hệt nguyên lý. Khác: âm thanh biết trước dải quan tâm (20 Hz–20 kHz), robot phải **đo** dải rung của chính nó.
- **Máy quay phim: gimbal và giảm rung cơ khí.** Gá camera điện ảnh trên đế treo giảm rung trước khi nói tới ổn định ảnh bằng phần mềm. Cùng thứ tự ưu tiên: chặn ở cơ khí, rồi lọc, cuối cùng mới bù bằng thuật toán.

### 11. Độ tin cậy và sửa lỗi

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| Aliasing của rung khi không lọc trước | [chuẩn] + [đã chạy] | Mô phỏng 1 |
| ICM-42688-P: nhiễu gyro ~2,8 mdps/√Hz, accel ~70 µg/√Hz, AAF cấu hình được | [spec — kiểm] | TDK datasheet DS-000347 |
| MPU-6050: nhiễu ~0,005 °/s/√Hz, ~400 µg/√Hz; trạng thái sản xuất | [spec — kiểm] | PS-MPU-6000A-00; trang sản phẩm TDK |
| USB 2.0 HS: 3 × 1024 B/vi khung/endpoint isochronous, ≤ 80 % cho truyền định kỳ | [spec] | USB 2.0 Specification mục 5.6–5.7 |
| USB 3 gây nhiễu băng 2,4 GHz | [chuẩn] | Intel, *USB 3.0 Radio Frequency Interference Impact on 2.4 GHz Wireless Devices* (2012) |
| rpy optical `(−π/2, 0, −π/2)` | [chuẩn] + [đã chạy] | Mô phỏng 2 |
| ArduPilot đo rung và coi rung cao là lỗi | [chuẩn — kiểm ngưỡng] | ArduPilot docs, "Measuring Vibration" |
| Tên lệnh `v4l2-ctl`, `tf2_echo`, tham số driver camera | [tự đo] | Theo bản cài |

**Đã thêm so với bản gốc:** bản gốc Bài 5 liệt kê luồng IMU 200 Hz và camera 10–30 fps mà không nói gá, rung, TF hay băng thông. Thêm toàn bộ bài này; chọn IMU có AAF và giải thích; kiểm TF bằng vật lý thay vì tin URDF.

### 12. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** REP-103 (đơn vị, quy ước trục, optical frame), REP-105; datasheet IMU bạn dùng (mục bộ lọc và ODR); USB 2.0 Specification chương 5 (kiểu truyền).
- **Giải thích:** ArduPilot docs, "Measuring Vibration" và "Vibration Damping".
- **Đào sâu (tùy chọn):** tài liệu `tf2` (docs.ros.org), mục static transforms và URDF.
- **Tự kiểm tra:** (1) giải thích trong 5 câu vì sao lọc trên host không cứu được aliasing ở ODR thấp; (2) vẽ lại bảng "gá quyết định ba thứ"; (3) câu dưới.

<details><summary>Camera chúc xuống 0,10 rad. Trong URDF, pitch của camera_front_link là +0,10 hay −0,10?</summary>

+0,10. Quay dương quanh trục y (hướng sang trái) theo quy tắc tay phải đưa trục x (trước) xuống dưới. Kiểm bằng `rpy_to_R(0, 0.1, 0)[:, 0]`: thành phần z âm.

</details>

---
