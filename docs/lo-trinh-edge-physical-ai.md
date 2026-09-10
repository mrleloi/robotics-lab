# LỘ TRÌNH EDGE / PHYSICAL AI — 24 THÁNG

**Cho:** full-stack engineer 8 năm, mạnh backend/hạ tầng/low-latency, Hà Nội
**Vị trí nhắm:** Robotics Data Infrastructure Engineer → System Design
**Không nhắm:** Robotics Engineer (kinematics, control theory) — không cạnh tranh nổi trong 24 tháng
**Ngân sách:** ~15–25tr trải đều 24 tháng
**Thời gian:** 10–12h/tuần, đều đặn. Đây là ràng buộc chính, không phải tiền.

---

# PHẦN 0 — NGUYÊN TẮC

1. **Đo trước, quyết sau.** Mọi quyết định kiến trúc phải có số đo kèm theo.
2. **Dự đoán trước, đo sau.** Nếu đo trước rồi mới giải thích, thí nghiệm không tính.
3. **Datasheet > tutorial.** Tutorial dạy bạn copy. Datasheet dạy bạn thiết kế.
4. **Công khai từ ngày đầu.** Ngành này tuyển qua repo, không qua CV.
5. **Uncertainty, provenance, calibration state là trường dữ liệu hạng nhất.** Đây là câu phân biệt bạn với backend engineer chuyển ngành thông thường.
6. **Không mua kit hoàn chỉnh.** Trừ SO-101 ở Phase 3, có lý do riêng.

---

# PHẦN 1 — BẰNG CHỨNG THỊ TRƯỜNG

Đây là các JD thật, dùng làm đích ngắm. Đọc kỹ, vì toàn bộ lộ trình dưới đây được thiết kế ngược từ chúng.

## 1.1 Verne Robotics — Robotics Data Infrastructure Engineer (SF)

Yêu cầu công việc:
- Xây hệ thống thu dữ liệu on-device chịu lỗi trên edge PC, dùng **MCAP/Protobuf**, schema contract rõ ràng, buffering, upload resumable lên cloud
- Tổ chức và version hàng triệu ảnh, video, time-series (robot state, force/torque), annotation
- Pipeline MLOps/DataOps: tự động validate, label, augment, train/eval bằng container và orchestrator (Batch, Step Functions, Airflow, Prefect)
- Ingestion check, schema validation, dedupe, drift detection, alert về data freshness
- Tool nội bộ: UI/CLI để browse dữ liệu, launch job, debug robot ngoài hiện trường, tích hợp **Foxglove**

**Đây là JD quan trọng nhất trong tài liệu này.** Đọc lại và đếm xem bao nhiêu dòng bạn đã làm được ngay hôm nay. Câu trả lời là phần lớn. Cái thiếu là MCAP, Foxglove, và hiểu bản chất dữ liệu cảm biến.

## 1.2 FieldAI — DevOps/Data (robotics)

- Đường ingest từ robot tới dataset dùng được: **rosbag/MCAP capture, episode segmentation**, chuyển định dạng, đưa vào training
- Data lifecycle guardrail: filter, review-for-deletion, retention, để dữ liệu robot chạy không tải không tích tụ vô hạn
- Dataset và mission registry: mọi dataset truy được về subject, session, robot, mục đích
- AWS as code: ECR, S3, IAM, VPC, EKS

→ **Provenance registry.** Đúng nguyên tắc số 5.

## 1.3 VinMotion — Robotics Engineer (Hà Nội, Gia Lâm)

ROS, State Estimation, Motion Planning, SLAM, Manipulation, inverse kinematics, trajectory planning, force control, Gazebo/Mujoco/IsaacGym.

→ Đây là JD bạn **không** apply năm đầu. Nhưng nó cho bạn từ vựng phải học và cho biết công ty này tồn tại, ở Hà Nội, và đang tuyển. Theo dõi trang tuyển dụng của họ mỗi tháng để chờ vị trí data/infra xuất hiện.

## 1.4 Foxglove — Solutions Engineer (remote, 180–230K USD/năm)

Làm việc với engineering team của khách để đánh giá kiến trúc hệ thống, thiết kế workflow ingestion/storage/visualization, troubleshoot vấn đề hiệu năng ở quy mô lớn. Công ty remote-friendly nhưng tuyển trong khoảng ±4 giờ so với múi giờ Mỹ.

→ Múi giờ là rào cản với VN, nhưng JD này cho thấy **mức giá thị trường của đúng kỹ năng bạn đang xây**. Và các công ty tương tự ở châu Âu thì múi giờ dễ hơn nhiều.

## 1.5 Ma trận kỹ năng

| Kỹ năng | Bạn có? | Học ở phase |
|---|---|---|
| Pipeline, batching, parallel, scaling | ✅ Mạnh | — |
| Low-latency, p99, backpressure | ✅ Mạnh | — |
| K8s, IaC, observability | ✅ | — |
| Time-series ở quy mô | ✅ | — |
| MCAP / Protobuf / rosbag | ❌ | Phase 2 |
| Foxglove / Rerun | ❌ | Phase 2 |
| ROS 2 (node, topic, TF, QoS, DDS) | ❌ | Phase 1–2 |
| Sensor: I2C/SPI/I2S/UART, datasheet | ❌ | Phase 0–2 |
| Time sync: PTP, hardware trigger | ❌ | Phase 2 |
| Calibration (intrinsic/extrinsic) | ❌ | Phase 3 |
| Sensor fusion, Kalman/EKF | ❌ | Phase 3 |
| Đo: multimeter, logic analyzer, scope | ❌ | Phase 0 |
| Imitation learning, VLA, LeRobot | ❌ | Phase 3–4 |
| Kinematics, control, MPC | ❌ | **Không học sâu. Chỉ đủ để nói chuyện.** |

---

# PHẦN 2 — BỐN PHASE

## PHASE 0 — Tuần 1–4: Học cách ĐO

**Mục tiêu duy nhất:** cắm được que đo vào một tín hiệu và xác định vấn đề nằm trên hay dưới bạn.

**Mua:** đợt 1 (xem Phần 3)

**Làm:**
- Ohm's law thật: cấp 5V qua điện trở vào LED, đo V nguồn / V trở / V LED / dòng. Tính `I = V/R`, `P = V×I`. So tính với đo.
- Voltage divider: dự đoán Vout trước khi đo, ba tỉ lệ khác nhau.
- Cắm logic analyzer vào một bus I2C bất kỳ, mở PulseView, decode. Nhìn thấy ACK/NACK.
- Đọc trọn vẹn một datasheet cảm biến từ đầu tới cuối. Không skim. Ghi ra register map bằng tay.

**Kiến thức:**
- Ben Eater (YouTube) — series về điện tử cơ bản và bus. Chất lượng cao nhất trên internet cho tầng này.
- EEVblog Fundamentals (YouTube, Dave Jones) — cách dùng multimeter, đọc datasheet
- SparkFun / Adafruit tutorials — ngắn, chính xác, có sơ đồ
- sigrok/PulseView documentation

**Gate:** giải thích được tại sao LED cần điện trở, bằng số, không bằng "vì tutorial bảo thế".

---

## PHASE 1 — Tháng 1–4: V1 Loa Confession + từ vựng ROS 2

**Mục tiêu:** đi hết chuỗi số → analog → âm thanh, và học từ vựng ROS 2 song song.

**Mua:** đợt 2

**Track A — V1 (chi tiết đầy đủ ở tài liệu V1 riêng):**
- Kiến trúc: Google Form → LAN box (FastAPI + queue + moderation + TTS) → Pi 5 → I2S → PCM5102A → amp → loa
- 5 thí nghiệm bắt buộc: I2S timing, latency budget, power sag, audio analysis (FFT/quantization/clipping), soak test 72h
- Không dùng cloud TTS. Local từ đầu.

**Track B — ROS 2 (song song, 3h/tuần):**
Bạn không cần robot để học ROS 2. Cài Ubuntu 24.04 + ROS 2 Jazzy trong Docker, học bằng turtlesim.

Điều quan trọng cho bạn: **ROS 2 là pub/sub trên DDS, có QoS policy.** Reliability, durability, history depth, deadline. Bạn sẽ thấy nó rất quen. Điểm khác biệt phải nắm: TF tree (cây biến đổi tọa độ giữa các khung), và tại sao mọi thứ trong robot đều gắn với một frame.

- `docs.ros.org` — tài liệu chính thức, đọc thay vì xem video
- **Articulated Robotics** (YouTube, Josh Newans) — series build robot ROS 2 từ đầu trên phần cứng thật. Nguồn tốt nhất cho người thực dụng.
- The Construct (`theconstruct.ai`) — có môi trường ROS chạy sẵn trên browser, đỡ mất thời gian setup
- Udemy "ROS 2 for Beginners (Jazzy)" — nếu cần cấu trúc tuyến tính

**Track C — Toán (2h/tuần, bắt đầu nhẹ):**
- Linear algebra: 3Blue1Brown "Essence of Linear Algebra" trước, rồi mới sách
- Rigid body transform: SE(3), quaternion. Đọc chương 3 sách Modern Robotics.

**Deliverable Phase 1:**
Repo public với V1 chạy được + 5 experiment có số đo + notebook. Video 60 giây robot phát confession.

**Gate:** vẽ được I2S timing từ trí nhớ; đọc được latency budget với số thật; giải thích QoS của DDS.

---

## PHASE 2 — Tháng 5–10: Sensor, time sync, và data stack THẬT

Đây là phase quan trọng nhất cho mục tiêu nghề nghiệp của bạn. Nếu chỉ làm được một phase, làm phase này.

**Mua:** đợt 3

### 2.1 Sensor + ESP32-S3

- IMU (MPU6050 hoặc ICM-42688 tốt hơn), ToF (VL53L1X), nhiệt/ẩm (BME280), encoder
- Đọc raw register, không dùng thư viện wrapper. Tự convert raw int → đơn vị vật lý.
- ESP32-S3 làm node cảm biến, gửi về Pi qua UART và WiFi. So sánh hai đường.

### 2.2 Time sync — bài toán ngọt nhất cho bạn

Đây là chỗ hệ phân tán gặp vật lý. Làm nghiêm túc.

**Thí nghiệm bắt buộc:**
1. Cho ESP32 và Pi cùng đọc một sự kiện (một chân GPIO chung được kéo lên). So timestamp hai bên. Đo lệch.
2. Bật `linuxptp` giữa Pi và LAN box qua Ethernet. Đo lại. Ghi độ lệch trước/sau.
3. Đo drift clock ESP32 theo nhiệt độ: chạy 6 tiếng, hơ nóng bằng máy sấy, ghi ppm.
4. Dùng hardware trigger: một xung chung kích cả camera và IMU. So với software timestamp.

**Tài liệu:**
- IEEE 1588 PTP — đọc `linuxptp` docs
- `chrony` documentation (phần về hardware timestamping)
- Foxglove blog series về time trong robotics

### 2.3 Data stack — dựng đúng như JD

Bây giờ dựng lại pipeline của bạn, nhưng bằng công cụ của ngành:

- **MCAP** (`mcap.dev`) — container format chuẩn cho log robot đa phương thức. Là định dạng lưu mặc định của ROS 2, hỗ trợ Protobuf, FlatBuffers. Ghi log cảm biến vào MCAP thay vì JSON/CSV.
- **Foxglove** (`foxglove.dev`) — mở file MCAP, visualize. Có free tier. Học cả phần fleet dashboard.
- **Rerun** (`rerun.io`) — visualization cho dữ liệu đa phương thức, nhẹ hơn Foxglove, dùng cho experiment nhanh
- **Protobuf schema** cho mọi message cảm biến. Có version. Có contract.
- **ClickHouse** hoặc TimescaleDB cho metric/telemetry (JD thật có nhắc ClickHouse)
- **MinIO/S3** cho blob, **Airflow/Prefect** cho orchestration
- Ingestion check: schema validation, dedupe, **drift detection**, alert freshness

**Deliverable Phase 2 — đây là artifact quan trọng nhất trong portfolio của bạn:**

> Một **sensor data platform** mini: 3+ cảm biến trên 2 thiết bị, clock đồng bộ bằng PTP, ghi MCAP có schema Protobuf versioned, upload resumable lên MinIO, index vào ClickHouse, mở được bằng Foxglove, có validation layer **theo vật lý** (không chỉ theo schema), có calibration registry, có dashboard freshness/drift.

Cộng một bài viết kỹ thuật (tiếng Anh) giải thích thiết kế và số đo. Bài viết này chính là cái mở cửa phỏng vấn.

### 2.4 V2 + V3 chạy nền

- V2: fine-tune TTS giọng bạn. VietTTS / VieNeu-TTS / Viterbox / F5-TTS-Vietnamese. Thuê GPU (vast.ai / runpod), đừng mua card.
- V3: face recognition (InsightFace/ArcFace embedding). **Bắt buộc: opt-in, chỉ lưu embedding, có nút xoá.** Dữ liệu sinh trắc học là dữ liệu cá nhân nhạy cảm theo Nghị định 13/2023.

**Gate Phase 2:** platform chạy 7 ngày liên tục; bisect được lỗi qua 4 tầng (pipeline → firmware → bus → cảm biến); bài viết kỹ thuật đã publish.

---

## PHASE 3 — Tháng 11–18: Chuyển động, calibration, robot learning

**Mua:** đợt 4

### 3.1 SO-101 + LeRobot — đường tắt lớn nhất trong lộ trình này

Đây là ngoại lệ với quy tắc "không mua kit". Lý do: nó không phải kit đồ chơi, nó là **hạ tầng nghiên cứu thật đang được dùng ở lab học thuật toàn cầu**, và nó đưa bạn thẳng vào ecosystem robot learning hiện đại.

- **SO-101**: cánh tay 6-DOF open source, giá khởi điểm ~100 USD (thực tế 100–500 USD tuỳ nhà cung cấp và phí), lắp trong 3–4 tiếng. Do Hugging Face LeRobot làm cùng The Robot Studio. Bán qua Seeed Studio, WowRobo, PartaBot, Hiwonder, ThinkRobotics.
- Thường mua theo **cặp**: leader arm (bạn cầm tay điều khiển) + follower arm (bắt chước, hoặc chạy policy).
- **LeRobot** (`github.com/huggingface/lerobot`): thư viện end-to-end cho robot learning — thu dữ liệu, train, điều khiển, đánh giá policy. Dataset cộng đồng nằm trên HF Hub theo LeRobot Dataset Format.

**Tại sao cực hợp với bạn:** LeRobot Dataset Format là một bài toán **data engineering**. Episode có observation (ảnh camera), robot state, action, theo schema nhất quán. Bạn thu dữ liệu bằng `lerobot-record`, push lên Hub. Đây là chỗ kỹ năng data của bạn gặp robot thật, và là ngôn ngữ chung của toàn bộ ngành robot learning hiện nay.

**Việc phải làm:**
1. Lắp SO-101, calibrate, teleoperation
2. Thu 50 episode pick-and-place, đẩy lên HF Hub
3. Train một policy (ACT hoặc Diffusion Policy), chạy inference thật
4. **Rồi làm phần của bạn:** đo chất lượng dataset. Episode nào bị drop frame? Timestamp có đều không? Camera và encoder có đồng bộ không? Viết công cụ audit dataset. **Chưa ai làm tốt việc này và đó là chỗ bạn nổi bật.**

### 3.2 Calibration

- Camera intrinsic: chessboard, OpenCV. Hiểu distortion model.
- Extrinsic camera–IMU, camera–lidar. Đây là bài toán optimization.
- Hand-eye calibration cho cánh tay.
- Ghi calibration vào registry có version. Nối vào platform Phase 2.

### 3.3 Sensor fusion + state estimation

Học **vừa đủ**, không đi sâu:
- Complementary filter → Kalman → EKF, làm trên chính dữ liệu IMU bạn thu
- `rlabbe/Kalman-and-Bayesian-Filters-in-Python` (GitHub, free) — cách học tốt nhất, là notebook chạy được
- Barfoot, *State Estimation for Robotics* — PDF free trên trang tác giả

### 3.4 V4 — robot di động

- ESP32-S3 làm real-time layer (motor, encoder, IMU, E-stop)
- Pi 5 hoặc Jetson làm perception + ROS 2 + Nav2
- Bắt đầu **trong simulation** (Gazebo) trước khi chạy thật
- **LeKiwi** — nền tảng mobile manipulation trong hệ LeRobot, nếu muốn đi thẳng vào V4+V5 gộp

**Gate Phase 3:** SO-101 chạy policy tự train; dataset audit tool public; robot di động đi được 10m có feedback control.

---

## PHASE 4 — Tháng 19–24: Quy mô, portfolio, apply

- Mở rộng platform Phase 2 thành **fleet**: nhiều robot, mission registry, retention policy, review-for-deletion (đúng như JD FieldAI)
- Đóng vòng: dữ liệu → dataset → train → deploy → thu dữ liệu mới. Đây là data flywheel, và là thứ mọi công ty physical AI đang cố xây.
- Thử một VLA nhỏ trên edge: SmolVLA hoặc GR00T N1 (2.2B params, 1.34B trong VLM backbone) — và đo. RTF, latency, VRAM. **Đây là chỗ bạn về nhà**: benchmark inference là bài toán của bạn.
- Viết 3–4 bài kỹ thuật tiếng Anh
- Apply: VinMotion / VinRobotics (Hà Nội), công ty robotics remote châu Âu, Foxglove và các công ty tooling tương tự

---

# PHẦN 3 — MUA SẮM THEO ĐỢT

Giá ước tính, cần kiểm tra lại. Tổng ~15–25tr trải 24 tháng.

## Đợt 1 — Phase 0 (~1.5–2.5tr)

| Món | Spec | Giá ~ |
|---|---|---|
| Logic analyzer USB 8 kênh 24MHz | Clone Saleae, dùng PulseView | 150–250k |
| Multimeter UNI-T UT33D+ | Đủ để bắt đầu | 285k |
| USB power meter | Đo dòng | 150–250k |
| Breadboard 830 + jumper | M-M/M-F/F-F | 100k |
| Kit điện trở + tụ + LED + nút | | 150–250k |
| Mỏ hàn chỉnh nhiệt T12/936 + thiếc + flux | | 400–700k |
| Nguồn bench có giới hạn dòng | Tuỳ chọn, rất nên có | 600k–1.5tr |

## Đợt 2 — Phase 1 (~3.5–4.5tr)

| Món | Spec | Giá ~ |
|---|---|---|
| Raspberry Pi 5 **8GB** | | 2.4–2.5tr |
| Nguồn USB-C PD 5V/5A 27W chính hãng | Bắt buộc chính hãng | 250–400k |
| microSD 64GB A2 | Samsung Evo Plus / SanDisk Extreme | 200–280k |
| Case + Active Cooler | | 150–300k |
| GY-PCM5102 (DAC I2S) | **Mua 2 cái** | 50–90k/cái |
| MAX98357A (I2S amp) | Để so sánh kiến trúc | 60–100k |
| Amp class-D PAM8403/TPA3110 | | 30–120k |
| Loa full-range 4Ω 3–5W ×2 | Phải có in thông số | 50–150k |
| INMP441 (mic I2S) | | 60–100k |
| Cáp Ethernet Cat6 | Dùng LAN, không WiFi khi dev | 30–50k |

## Đợt 3 — Phase 2 (~2–3tr)

ESP32-S3 DevKit ×2 (~200k/cái), IMU ICM-42688 hoặc MPU6050 (~85–250k), ToF VL53L1X (~150k), BME280 (~80k), Pi Camera Module 3 (~700k–1tr), micro SD dự phòng, cáp và linh kiện lặt vặt.

**Không mua GPU.** Thuê vast.ai/runpod cho V2.

## Đợt 4 — Phase 3 (~6–10tr)

| Món | Ghi chú |
|---|---|
| **SO-101 cặp leader + follower** | 100–500 USD tuỳ nguồn. Seeed Studio / Hiwonder / WowRobo. Rẻ nhất: tự in 3D + mua servo STS3215 |
| Motor DC có encoder ×2 | ~245k/cái |
| Motor driver TB6612FNG | ~40k |
| Chassis, bánh, pin LiPo/Li-ion + BMS | ~500k–1tr |
| Lidar 2D (RPLidar A1) | ~1.5–2.5tr, cho SLAM |
| Jetson Orin Nano Super | ~7–10tr. **Chỉ mua khi Pi 5 thực sự nghẽn.** Có thể bỏ qua |
| Máy in 3D entry (Bambu A1 mini / Ender) | ~3–6tr. Cân nhắc dùng dịch vụ in ở HN trước |

## Nơi mua tại Hà Nội

**Cửa hàng có địa chỉ:**
- **Linh Kiện Điện Tử 3M / chotroihn.vn** — Số 9, Ngõ 40/2 Tạ Quang Bửu, Bách Khoa, Hai Bà Trưng. Có Pi 5, logic analyzer.
- **Lập Trình Nhúng A-Z** — Số 6, Ngách 38/12, Ngõ 38 Khúc Thừa Dụ, Dịch Vọng, Cầu Giấy. Có PCM5102A và module nhúng.
- **Chợ Trời** — khu Thịnh Yên / Hòa Bình, Hai Bà Trưng. Linh kiện thụ động, rẻ, có ngay.

**Online toàn quốc:** mlab.com.vn, pivietnam.com.vn, cytrontech.vn, linhkienaiot.com, dientudat.com, hshop.vn, nshopvn.com, dientutuyetnga.com

**Quốc tế (cho SO-101, cảm biến hiếm):** Seeed Studio, Adafruit, SparkFun, Mouser, DigiKey, AliExpress (chấp nhận rủi ro hàng nhái)

---

# PHẦN 4 — KÊNH KIẾN THỨC

## 4.1 Tài liệu gốc — đọc thay vì xem tutorial

| Nguồn | Dùng cho |
|---|---|
| `docs.ros.org` | ROS 2 — nguồn chính, không dùng blog copy |
| `docs.nav2.org` | Navigation stack |
| Raspberry Pi documentation | Pinout, GPIO, I2C/SPI/UART, cảnh báo điện áp và motor |
| Espressif ESP-IDF Programming Guide | ESP32 — dùng tài liệu hãng, không dùng blog |
| `mcap.dev` | Format log robot |
| `foxglove.dev/docs` | Data platform |
| `rerun.io/docs` | Visualization |
| `huggingface.co/docs/lerobot` | Robot learning |
| Datasheet từng con chip | **Quan trọng nhất trong bảng này** |

## 4.2 Sách

**Bắt buộc:**
- **Modern Robotics: Mechanics, Planning, and Control** — Lynch & Park. PDF free trên trang khoá học Northwestern. Đọc chương 2–3 (configuration space, rigid-body motion). Có khoá Coursera đi kèm.
- **Kalman and Bayesian Filters in Python** — Roger Labbe, GitHub, free, dạng Jupyter notebook chạy được. Cách học filter tốt nhất hiện có.
- **State Estimation for Robotics** — Timothy Barfoot. PDF free.

**Tham khảo khi cần:**
- **The Art of Electronics** — Horowitz & Hill. Không đọc tuần tự, dùng như từ điển.
- **Practical Electronics for Inventors** — Scherz & Monk. Dễ vào hơn.
- **Making Embedded Systems** — Elecia White. Tư duy embedded cho người từ software.
- **Probabilistic Robotics** — Thrun, Burgard, Fox. Kinh điển về SLAM/localization. Nặng, để dành Phase 3.

## 4.3 Khoá học

- **Modern Robotics Specialization** (Coursera, Northwestern) — audit free
- **Underactuated Robotics** (MIT, Russ Tedrake) — free, YouTube + notes. Nặng nhưng hay.
- **Robotics: Perception / Estimation** (Coursera, UPenn)
- **The Construct** (`theconstruct.ai`) — ROS chạy trên browser, tiết kiệm thời gian setup
- Class Central có tổng hợp 60+ khoá ROS 2 và 80+ khoá ROS, lọc theo nhu cầu

## 4.4 YouTube — chọn lọc, không lướt

| Kênh | Mảng |
|---|---|
| **Articulated Robotics** (Josh Newans) | ROS 2 + phần cứng thật. Tốt nhất cho người thực dụng |
| **Ben Eater** | Điện tử và bus ở mức bản chất |
| **Phil's Lab** | PCB design, embedded, DSP. Rất hợp hướng của bạn |
| **EEVblog** | Dụng cụ đo, đọc datasheet |
| **James Bruton** | Cơ khí robot DIY, ý tưởng |
| **Nikodem Bartnik** | Có series đầy đủ về SO-ARM101 từ lắp ráp tới train policy |
| **Robotics Back-End** | ROS 2 thực hành |

## 4.5 Repo để clone và ĐỌC

Không chỉ chạy. Đọc kiến trúc.

```
huggingface/lerobot                  ← robot learning end-to-end
TheRobotStudio/SO-ARM100             ← thiết kế cánh tay, in 3D
foxglove/mcap                        ← format log, đọc phần indexing
rerun-io/rerun                       ← visualization, viết bằng Rust
ros2/rclpy, ros-navigation/navigation2
NVIDIA/Isaac-GR00T                   ← VLA foundation model
Physical-Intelligence/openpi         ← π0 / π0.5
openvla/openvla
rlabbe/Kalman-and-Bayesian-Filters-in-Python
keon/awesome-physical-ai             ← danh mục paper VLA, world model, embodied AI
sigrokproject/libsigrok
espressif/esp-idf
```

## 4.6 Theo dõi tin tức và xu hướng

- **The Robot Report** (`therobotreport.com`) — tin ngành, gọi vốn, triển khai
- **IEEE Spectrum Robotics** — chất lượng cao, có chiều sâu
- **Robohub** — phân tích
- **Hugging Face blog** (mục robotics) — LeRobot cập nhật liên tục
- **NVIDIA robotics blog** — Isaac, GR00T, Jetson
- **arXiv cs.RO** — theo qua Twitter/X list hoặc arxiv-sanity
- **Hội nghị:** ICRA, IROS, CoRL, RSS. Đọc paper list mỗi năm kể cả không dự.
- `humanoid.guide`, `theaiinsider.tech` — theo dõi mảng humanoid

**Xu hướng đang nóng cần nắm từ vựng (không cần làm được ngay):**
VLA models (π0, π0.5, GR00T N1, OpenVLA, SmolVLA), diffusion policy, action chunking, world models, sim-to-real, imitation learning từ teleoperation, cross-embodiment. Có cả nhánh runtime hiệu năng (vla.cpp, VLA-Perf, BitVLA 1-bit) — nhánh này **rất hợp với bạn**, vì nó là tối ưu inference, đúng nghề.

## 4.7 Cộng đồng

**Toàn cầu:**
- **ROS Discourse** (`discourse.ros.org`) — nơi ra quyết định của ROS. Đọc, đừng chỉ hỏi.
- **LeRobot Discord** (link trong docs HF) — active, nhiều người đang build SO-101
- **Foxglove Slack/community**
- Reddit: `r/robotics`, `r/ROS`, `r/embedded`, `r/AskElectronics`
- **Hackaday.io** và **Hackster.io** — project, hackathon
- ROS 2 Discord

**Việt Nam:**
- Các group Facebook về Arduino / ESP32 / điện tử — chất lượng không đều nhưng hỏi mua linh kiện thì nhanh
- Cộng đồng AI Việt Nam (AI VIETNAM, VietAI) — mảng ML, không phải robotics, nhưng có người làm edge
- Forum của hshop / nshop
- Meetup ở Hà Nội quanh các trường Bách Khoa / UET — theo dõi qua Facebook

Thật lòng: **cộng đồng robotics VN còn mỏng.** Đừng kỳ vọng tìm được mentor trong nước ở mảng này. Cộng đồng thật của bạn sẽ là Discord/Discourse tiếng Anh. Đây cũng là lý do viết bài bằng tiếng Anh quan trọng.

---

# PHẦN 5 — PORTFOLIO PHẢI CÓ GÌ

Đây là thứ quyết định, không phải CV.

```
github.com/<bạn>/
├── confession-robot/          V1–V4, có lab notebook đầy đủ
├── sensor-data-platform/      ★ ARTIFACT QUAN TRỌNG NHẤT
│   ├── MCAP + Protobuf schema có version
│   ├── PTP time sync + số đo thật
│   ├── validation theo vật lý, không chỉ theo schema
│   ├── calibration registry
│   └── drift/freshness dashboard
├── lerobot-dataset-audit/     ★ công cụ chưa ai làm tốt
├── vla-edge-benchmark/        ★ đo RTF/latency/VRAM các VLA trên edge
└── lab-notebook/              mọi thí nghiệm: dự đoán → đo → giải thích
```

**Ba repo có ★ là ba thứ khiến bạn khác biệt.** Chúng nằm đúng giao điểm giữa cái bạn đã giỏi và cái ngành đang thiếu.

**Bài viết (tiếng Anh, 4 bài trong 24 tháng):**
1. "Measuring end-to-end audio latency on a Raspberry Pi: from ALSA buffer to air pressure"
2. "Time synchronization for multi-sensor robots: PTP vs hardware trigger, measured"
3. "Auditing LeRobot datasets: what breaks and how to detect it"
4. "Benchmarking VLA inference on edge hardware"

Đăng trên blog cá nhân + cross-post Hacker News / r/robotics / LinkedIn.

---

# PHẦN 6 — GATE VÀ RỦI RO

## Mốc kiểm tra

| Thời điểm | Phải đạt |
|---|---|
| Tháng 1 | Cắm logic analyzer, decode được một bus |
| Tháng 4 | V1 chạy 72h không can thiệp; hiểu QoS DDS |
| Tháng 10 | ★ Sensor data platform chạy 7 ngày; bài viết #1, #2 đã publish |
| Tháng 12 | **Ít nhất 1 cuộc phỏng vấn ở công ty robotics/edge.** Nếu chưa có → giả thuyết sai ở đâu đó, dừng lại và chỉnh |
| Tháng 18 | SO-101 chạy policy tự train; dataset audit tool public |
| Tháng 24 | Offer, hoặc quyết định chuyển sang hướng sản phẩm |

## Ba rủi ro lớn nhất

**1. Không đủ 10h/tuần.** Đây là rủi ro số một, lớn hơn mọi rủi ro kỹ thuật. Nếu công việc hiện tại còn những đợt 12–14h/ngày kéo dài, lộ trình này chết ở tuần thứ tám. Giải quyết ràng buộc thời gian **trước**, không phải sau.

**2. Dùng AI viết code hộ để vượt phần phần cứng.** Lỗi phần cứng không có stack trace. Nếu bạn không tự đo, bạn sẽ có robot chạy được và không hiểu gì thêm — tức là mất đúng thứ bạn đang đi tìm.

**3. Nhảy vọt độ khó ở V4.** Từ robot đứng yên sang robot tự di chuyển là bước nhảy 10x. Đã tính vào lịch (8 tháng cho Phase 3). Đừng nghĩ nó sẽ nhanh hơn.

## Một điều giữ suốt 24 tháng

Với mỗi module mua về, đừng hỏi "code nào để nó chạy". Hỏi:

> *"Bên trong cái này đang xảy ra hiện tượng vật lý gì, và bằng cơ chế nào nó biến thành con số tôi đang đọc?"*

Cái làm bạn khác biệt trong mười năm tới không phải là biết ROS, mà là vẫn còn muốn hỏi câu đó khi không ai trả tiền cho câu hỏi.
