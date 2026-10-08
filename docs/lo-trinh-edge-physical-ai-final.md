# LỘ TRÌNH EDGE / PHYSICAL AI — 24 THÁNG

**Cho:** full-stack engineer 8 năm, mạnh backend / hạ tầng / low-latency, đang làm sole delivery dev, Hà Nội, 30 tuổi.
**Vị trí nhắm:** Robotics Data Infrastructure Engineer → Platform / System Design.
**Không nhắm:** Robotics Engineer thuần (kinematics, control theory, motion planning). Không cạnh tranh nổi trong 24 tháng với người học cơ điện tử 5 năm. Đừng phí giờ vào đó.
**Ngân sách tiền:** 14–23tr, trải 24 tháng, chia 4 đợt có điều kiện kích hoạt.
**Ngân sách giờ:** ~650h. Đây là ràng buộc chính, không phải tiền. Toàn bộ tài liệu được scope theo con số này.

---

## CÁCH ĐỌC TÀI LIỆU NÀY

- **Phần 0** là ràng buộc. Đọc trước, và làm M0 trước khi tiêu quá 2.5tr.
- **Phần 3** là phần chính: 9 milestone, mỗi cái có ngân sách giờ, điều kiện vào, việc cụ thể, tiêu chí PASS nhị phân, và hành động khi FAIL đã cam kết sẵn.
- Các phần còn lại là tài nguyên tra cứu: đích ngắm thị trường, chi tiết kỹ thuật V1, mua sắm, kênh học, cộng đồng.
- Không milestone nào được chấm bằng cảm giác. Mỗi tiêu chí PASS phải kiểm được bởi người khác đọc repo, hoặc bởi một con số.

---

# PHẦN 0 — NGUYÊN TẮC VÀ RÀNG BUỘC

## 0.1 Sáu nguyên tắc giữ suốt 24 tháng

1. **Đo trước, quyết sau.** Mọi quyết định kiến trúc phải có số đo kèm theo. "Pi yếu quá" không phải lý do; "RTF đo được là 1.8" mới là lý do.
2. **Dự đoán trước, đo sau.** Tính ra con số kỳ vọng, ghi lại, rồi mới cắm que đo. Nếu đo trước rồi mới giải thích, thí nghiệm đó không tính.
3. **Datasheet > tutorial.** Tutorial dạy copy. Datasheet dạy thiết kế.
4. **Công khai từ ngày đầu.** Ngành này tuyển qua repo và commit history, không qua CV. Repo là kênh phân phối duy nhất.
5. **Uncertainty, provenance, calibration state là trường dữ liệu hạng nhất.** Đây là câu phân biệt bạn với một backend engineer chuyển ngành thông thường.
6. **Đi tới đáy đúng một chain, dùng module cho phần còn lại.** Chain đó là audio. Nhiệt độ, ánh sáng, khoảng cách thì mua module, đọc datasheet, đọc raw register là đủ.

## 0.2 Ngân sách giờ

Đây là chỗ đa số lộ trình tự học chết. Không phải vì khó, mà vì lập kế hoạch trên số giờ không tồn tại.

| Loại tuần | Tỉ lệ | Giờ/tuần |
|---|---|---|
| Tuần tốt | ~35% | 10–12h |
| Tuần thường | ~45% | 5–8h |
| Tuần crunch (UAT, go-live, release, region mới) | ~20% | 0–2h |
| **Trung bình thật** | | **6–7h/tuần** |
| **Tổng 24 tháng** | | **~650h** |

**Ba kịch bản, chuẩn bị trước cho cả ba:**

| Trung bình thật | Tổng 24 tháng | Làm được gì |
|---|---|---|
| 6–7h/tuần | ~650h | Toàn bộ M0–M8. Không còn slack. |
| 5h/tuần | ~520h | M0–M7. **Bỏ M8 (SO-101).** Vẫn là hồ sơ đủ mạnh cho robot data infra. |
| 4h/tuần | ~420h | M0–M6 + M7 bản MVP. Track C dừng sau V1. |
| <3h/tuần | <320h | Chỉ Track B. Ràng buộc nằm ở công việc, không ở lộ trình — giải quyết cái đó trước. |

**Quy tắc thay cho deadline theo tháng:** mỗi milestone có **ngân sách giờ** và **trần giờ**. Chạm trần mà chưa PASS không có nghĩa là cần cố thêm — nó là tín hiệu sai phương pháp, và kích hoạt FAIL action đã viết sẵn.

**Chế độ tối thiểu cho tuần crunch:** 2h/tuần, chỉ đọc, không build. Đọc datasheet, đọc docs.ros.org, đọc source lerobot. Không cố ép một thí nghiệm vào tuần 14h/ngày — sẽ hỏng cả hai.

**Bắt buộc:** ghi giờ thật vào `hours.csv` trong repo (ngày, số giờ, milestone). Không có file này thì mọi gate phía dưới vô nghĩa vì không biết đã tiêu bao nhiêu.

## 0.3 Ngân sách tiền và điều kiện mua

Không mua theo lịch. Mua theo gate.

| Đợt | Kích hoạt bởi | Số tiền |
|---|---|---|
| Đợt 1 — dụng cụ đo + hàn | Ngay. Giữ giá trị kể cả nếu bỏ cuộc. | 1.5–2.5tr |
| Đợt 2 — Pi 5 + chuỗi audio | **M0 PASS + M1 PASS** | 3.5–4.5tr |
| Đợt 3 — sensor + ESP32-S3 | **M4 PASS** | 2–3tr |
| Đợt 4 — SO-101 cặp | **M5 PASS** ở mức ≥2 phản hồi | 7–13tr |
| **Tổng** | | **14–23tr** |

**Lead time là blocker, không phải chi tiết.** SO-101 ship từ US/CN + hải quan = 3–8 tuần. Đặt hàng phải nằm trong lịch trước điểm cần dùng ít nhất 8 tuần.

**Không mua GPU.** Thuê vast.ai / runpod theo giờ. Một lần train ACT (52M params) khoảng 4h trên RTX 3080 — thuê rẻ hơn mua rất nhiều lần.

## 0.4 Blocker phi kỹ thuật — xử lý TRƯỚC khi mua món đầu tiên

| # | Blocker | Trạng thái phải đạt | Nếu không đạt |
|---|---|---|---|
| B1 | Không đủ giờ | `hours.csv` 2 tuần liên tục, median ≥5h/tuần | Chỉ chạy Track B. Không mua đợt 2. |
| B2 | Triển khai hòm confession ở công ty | Có xác nhận **bằng văn bản** (chat/email) của quản lý | Chạy V1 ở nhà. Bỏ hoàn toàn nhận diện mặt. Portfolio không mất gì. |
| B3 | Máy chạy TTS ("LAN box") | Nêu tên máy + spec trong repo. Không có GPU → đo RTF trên CPU trước khi chốt kiến trúc | Kiến trúc V1 đổi: TTS on-device trên Pi, hoặc pre-render |
| B4 | Dữ liệu sinh trắc học | Chỉ làm trên chính mình + người tình nguyện có consent viết. Nghị định 13/2023 xếp sinh trắc học vào dữ liệu cá nhân nhạy cảm. | Cắt. Không đàm phán. Làm face recognition trên dataset công khai nếu vẫn muốn học. |
| B5 | Moderation | Hàng đợi duyệt tay + filter tên riêng + nút kill, có từ ngày đầu | Không deploy |

**B2 đáng nói thêm.** Hòm confession ẩn danh + loa đọc to giữa văn phòng là **sự kiện HR**, không phải project kỹ thuật. Rủi ro không nằm ở code. Hỏi trước, hỏi bằng văn bản, và chấp nhận câu trả lời "không" — vì giá trị portfolio nằm ở lab notebook và số đo, không nằm ở việc cái loa đặt ở đâu.

**B5 tương tự.** Hòm ẩn danh + loa = kênh quấy rối có khuếch đại. Bỏ moderation thì project chết vì lý do phi kỹ thuật trong tuần thứ hai.

## 0.5 Quy tắc dùng AI — phiên bản thi hành được

Bạn build nhanh nhờ AI. Đó là tài sản, không phải tật xấu. Nhưng có đúng một chỗ nó phá hỏng toàn bộ mục đích của 650h này. Ranh giới cụ thể:

| Việc | AI được dùng? | Lý do |
|---|---|---|
| Tooling, script đo, parser, dashboard, CI, harness benchmark | ✅ Thoải mái, dùng hết công suất | Có stack trace. Đây là thế mạnh. |
| Firmware, driver, code chạm timing/thanh ghi | ✅ Nhưng phải tự đọc lại từng dòng chạm vào register và timing | Sai ở đây không crash, chỉ ra số sai |
| Debug lỗi phần cứng | ⚠️ Chỉ sau khi đã có số đo | Lỗi phần cứng không có stack trace. Thông tin cần thiết chỉ tồn tại trên đầu que đo. |
| **Dự đoán bằng số trước khi đo** | ❌ Tuyệt đối không | Đây chính xác là thứ đang mua bằng 650h |
| Giải thích chênh lệch dự đoán vs đo | ❌ Chỉ được hỏi sau khi đã tự viết giả thuyết của mình | — |

**Cơ chế thi hành, kiểm được bằng máy:** `prediction.md` phải được **commit trước** file capture/số đo. Git history là bằng chứng, không phải lời hứa. Viết CI check:

```
mỗi thư mục /lab/NN-*/ phải có:
  - prediction.md  (commit timestamp T1)
  - measurement.*  (commit timestamp T2)
  và T1 < T2, nếu không → CI đỏ
```

Đây là cách duy nhất biến một nguyên tắc thành gate.

## 0.6 Hạ tầng theo dõi — dựng trong tuần đầu

```
github.com/<bạn>/robotics-lab/     ← public từ commit đầu tiên
├── hours.csv                       ngày, giờ, milestone
├── decisions.md                    mỗi quyết định kiến trúc + lý do + số đo
├── /lab/                           mỗi thí nghiệm một thư mục
│   └── NN-ten-thi-nghiem/
│       ├── prediction.md           commit TRƯỚC
│       ├── setup.md                sơ đồ đấu nối, dụng cụ, cấu hình
│       ├── measurement.*           raw capture / csv
│       └── analysis.md             số đo, chênh lệch, giải thích
└── .github/workflows/lab-check.yml CI check của mục 0.5
```

**Mẫu một entry lab notebook** — giữ nguyên thứ tự này, không đảo:

> câu hỏi → dự đoán bằng số (kèm cách tính) → sơ đồ đấu nối → phương pháp đo + sai số của phép đo → số đo → chênh lệch với dự đoán → giải thích chênh lệch → thí nghiệm tiếp theo

Phần "sai số của phép đo" là thứ hầu hết người tự học bỏ qua và là thứ người phỏng vấn ở vị trí này nhìn vào đầu tiên.

---

# PHẦN 1 — ĐÍCH NGẮM: THỊ TRƯỜNG THẬT

Toàn bộ lộ trình được thiết kế ngược từ các JD dưới đây. Đọc kỹ chúng trước khi đọc phần milestone.

## 1.1 Verne Robotics — Robotics Data Infrastructure Engineer (SF)

Yêu cầu:
- Hệ thống thu dữ liệu on-device chịu lỗi trên edge PC, dùng **MCAP/Protobuf**, schema contract rõ ràng, buffering, upload resumable lên cloud
- Tổ chức và version hàng triệu ảnh, video, time-series (robot state, force/torque), annotation
- Pipeline MLOps/DataOps: tự động validate, label, augment, train/eval bằng container và orchestrator (Batch, Step Functions, Airflow, Prefect)
- Ingestion check, schema validation, dedupe, drift detection, alert về data freshness
- Tool nội bộ: UI/CLI để browse dữ liệu, launch job, debug robot ngoài hiện trường, tích hợp **Foxglove**

**Đây là JD quan trọng nhất trong tài liệu này.** Đếm xem bao nhiêu dòng bạn đã làm được ngay hôm nay. Câu trả lời là phần lớn. Cái thiếu là ba công cụ có tên riêng (MCAP, Foxglove, Protobuf-cho-sensor) và hiểu bản chất dữ liệu cảm biến. Khoảng cách nhỏ hơn bạn nghĩ — và M2 đóng ba công cụ đó trong 20h.

## 1.2 FieldAI — DevOps/Data (robotics)

- Đường ingest từ robot tới dataset dùng được: rosbag/MCAP capture, **episode segmentation**, chuyển định dạng, đưa vào training
- Data lifecycle guardrail: filter, review-for-deletion, retention, để dữ liệu robot chạy không tải không tích tụ vô hạn
- Dataset và mission registry: mọi dataset truy được về subject, session, robot, mục đích
- AWS as code: ECR, S3, IAM, VPC, EKS

→ **Provenance registry.** Đúng nguyên tắc số 5.

## 1.3 VinMotion — Robotics Engineer (Hà Nội, Gia Lâm)

ROS, State Estimation, Motion Planning, SLAM, Manipulation, inverse kinematics, trajectory planning, force control, Gazebo/Mujoco/IsaacGym.

→ JD này bạn **không** apply trong 24 tháng đầu. Nhưng nó cho bạn từ vựng phải học, và cho biết công ty này tồn tại, ở Hà Nội, đang tuyển. Theo dõi trang tuyển dụng mỗi tháng để chờ vị trí data/infra/platform xuất hiện — đó mới là cửa của bạn.

Bối cảnh: Vingroup có ba pháp nhân robot — VinRobotics, VinMotion, VinDynamics. Đây là cụm R&D physical AI thật duy nhất ở VN có quy mô.

## 1.4 Foxglove — Solutions Engineer (remote, 180–230K USD/năm)

Đánh giá kiến trúc hệ thống của khách, thiết kế workflow ingestion/storage/visualization, troubleshoot hiệu năng ở quy mô lớn. Tuyển trong khoảng ±4h so với múi giờ Mỹ.

→ Múi giờ là rào cản với VN, nhưng JD này cho thấy **mức giá thị trường của đúng kỹ năng bạn đang xây**. Các công ty tương tự ở châu Âu thì múi giờ dễ hơn nhiều — đó là target thực tế hơn.

## 1.5 Ba thị trường, đừng gộp

| Thị trường | Nhiệt độ | Ý nghĩa với bạn |
|---|---|---|
| **Toàn cầu — physical AI** | Rất nóng, thiếu người nghiêm trọng. Nhóm khan hiếm nhất là calibration, sensor fusion, simulation realism, real-time control, **robot data pipeline** — ba trong năm là kỹ năng hệ thống, không phải cơ điện tử. | Đích lương và đích remote |
| **VN — robot công nghiệp** | Nhỏ. Tăng trưởng % đẹp nhưng tổng quy mô vài trăm triệu USD. | Có việc ổn định, không có bùng nổ. Đừng đặt cược quy mô vào đây. |
| **VN — physical AI R&D** | Cụm Vingroup, đang tuyển, ở Hà Nội | Đây là cửa nội địa thật. Nhưng vào bằng cửa data/infra, không bằng cửa robotics engineer. |

## 1.6 Bốn vị trí bạn thắng ngay từ ngày đầu

| Vị trí | Tại sao |
|---|---|
| **Robot data infrastructure** | Fleet telemetry, rosbag/MCAP ingest hàng TB/ngày, time-series. Đúng bài toán 30k msg/s của bạn |
| **Teleop / low-latency streaming** | Điều khiển từ xa cần p99 chặt. Đúng 10–30ms của bạn, đổi domain |
| **Simulation infrastructure** | Chạy hàng nghìn episode song song, orchestration, artifact management. Là bài toán scaling |
| **Deployment / OTA / observability cho fleet** | Không roboticist nào muốn làm. Không ai giỏi hơn người đã vận hành hệ high-load |

Bốn vị trí này ở công ty robotics **hiếm hơn cả robotics engineer**, vì người giỏi kinematics thường không giỏi và không thích làm hạ tầng. Đây là arbitrage thật.

Định vị quan trọng: bạn **sở hữu một tầng**, không **đứng giữa hai team**. Đứng giữa thì thành glue — dịch yêu cầu, nối API, không tích lũy tài sản kỹ thuật, và là vai đầu tiên bị cắt. Sở hữu một tầng thì tầng đó có tên, có bài toán riêng, có văn liệu riêng.

## 1.7 Ma trận kỹ năng

| Kỹ năng | Có? | Học ở |
|---|---|---|
| Pipeline, batching, parallel, scaling | ✅ Mạnh | — |
| Low-latency, p99, backpressure | ✅ Mạnh | — |
| K8s, IaC, observability | ✅ | — |
| Time-series ở quy mô | ✅ | — |
| MCAP / Protobuf / rosbag | ❌ | **M2** |
| Foxglove / Rerun | ❌ | **M2** |
| LeRobot dataset format | ❌ | **M3** |
| Đo: multimeter, logic analyzer | ❌ | **M1** |
| Sensor: I2C/SPI/I2S/UART, datasheet | ❌ | M1, M4, M7 |
| ROS 2 (node, topic, TF, QoS, DDS) | ❌ | Track song song |
| Time sync: PTP, hardware trigger | ❌ | **M7** |
| Inference benchmark trên edge | ⚠️ Có nền, đổi payload | **M6** |
| Calibration (intrinsic/extrinsic) | ❌ | M8 |
| Sensor fusion, Kalman/EKF | ❌ | Vừa đủ, ở M7/M8 |
| Kinematics, control, MPC | ❌ | **Không học sâu. Chỉ đủ từ vựng để nói chuyện.** |

**Điểm bạn chưa khai thác:** robot là một **hệ phân tán real-time**. Time sync, backpressure, message bus, latency budget — bạn đã biết. Cái chưa biết là **determinism**: trong hệ của bạn p99 30ms là tốt; trong control loop 1kHz, một lần jitter 5ms làm robot mất ổn định. Throughput và determinism là hai bài toán ngược nhau. Đó là thứ đầu tiên nên học lại, không phải điện trở.

---

# PHẦN 2 — BỐN TRACK

Đừng all-in vào một đường.

| Track | Nội dung | Giờ | Ghi chú |
|---|---|---|---|
| **A — Đổi domain có lương** | Chuyển sang công ty có phần cứng thật, ở đúng vai trò backend/data/infra hiện tại | 40h | **Đòn bẩy lớn nhất.** Được trả tiền để tích lũy domain, thay vì học buổi tối. |
| **B — Portfolio phần mềm** | M2, M3, M6. Không cần phần cứng, không bị chặn bởi ship hàng hay tuần crunch. | 150h | Ra artifact nhanh nhất. Đúng thế mạnh. |
| **C — Chiều sâu phần cứng** | M1, M4, M7, M8. Chứng minh "đã chạm phần cứng thật". | 395h | Chậm, nhưng là thứ khiến bạn khác backend engineer nói "tôi quan tâm robotics" |
| **D — Vòng phản hồi thị trường** | M5 và lặp lại. Apply là một **phép đo**, không phải bước cuối. | 60h | Bắt đầu tháng 5–6, không phải tháng 24 |

**Đảo thứ tự quan trọng nhất:** hai trong ba artifact khác biệt (dataset audit, VLA benchmark) **không cần phần cứng gì cả**. Chúng phải ra trước, vì chúng tạo tín hiệu phỏng vấn, không bị chặn bởi ship hàng, và đúng nghề hiện tại chỉ đổi payload. Track C chứng minh chiều sâu **trong phỏng vấn** — nhưng nó không nên là đường tới artifact đầu tiên.

---

# PHẦN 3 — MILESTONE

Định dạng: **Intent → Giờ/Trần → Entry → Việc cụ thể → PASS (nhị phân) → FAIL action (cam kết trước)**.

---

## M0 — Kiểm tra ràng buộc

**Intent:** biết kế hoạch có chạy được không, trước khi tiêu quá 2.5tr.
**Giờ:** 8h · **Trần:** 3 tuần lịch · **Entry:** không · **Tiền:** đợt 1 (mua ngay, không chờ M0)

**Việc cụ thể:**
1. Tạo repo public theo cấu trúc 0.6. Commit đầu tiên hôm nay.
2. Bắt đầu ghi `hours.csv` mỗi ngày. Ghi cả ngày 0h.
3. Nhắn quản lý về B2, bằng văn bản. Nội dung: mô tả project, nêu rõ có moderation queue và nút kill, hỏi có được đặt ở văn phòng không.
4. Xác định máy chạy TTS (B3). Ghi tên + CPU + RAM + GPU vào `decisions.md`.
5. Mua đợt 1 (Phần 5).
6. Viết CI check của 0.5, test bằng một thư mục lab giả.

**PASS — cả 4:**
1. `hours.csv` ≥14 ngày liên tục, median ≥5h/tuần, có ≥1 tuần ≥8h
2. Có câu trả lời bằng văn bản cho B2 — **đồng ý hoặc từ chối đều là PASS**, chỉ cần có câu trả lời
3. B3 có tên máy + spec trong `decisions.md`
4. CI check chạy xanh

**FAIL → action:**
- Median 3–5h/tuần → **không mua đợt 2**. Chỉ chạy M2 + M3 + M6. Xem lại sau 3 tháng.
- Median <3h/tuần → Track C hoãn vô thời hạn. Dồn vào Track A. Ràng buộc nằm ở công việc, phải giải quyết ở đó.

---

## M1 — Đo được

**Intent:** cắm que đo vào một tín hiệu và xác định được vấn đề nằm trên hay dưới mình.
**Giờ:** 35h · **Trần:** 55h · **Entry:** M0 PASS

**Việc cụ thể:**
1. **Ohm's law thật.** Cấp 5V qua điện trở vào LED. Trước khi cắm: tính `I = (5 − V_f)/R` với V_f tra từ datasheet LED. Ghi vào `prediction.md`, commit. Rồi đo V nguồn / V trở / V LED / dòng. So sánh.
2. **Voltage divider.** Ba tỉ lệ khác nhau. Dự đoán Vout trước, commit, rồi đo.
3. **Logic analyzer + I2C.** Cắm vào một bus I2C bất kỳ (module BME280 hoặc bất cứ thứ gì có sẵn), mở PulseView, bật decoder I2C. Nhìn thấy start condition, address, ACK/NACK, stop.
4. **Đọc trọn một datasheet.** Từ đầu tới cuối, không skim. Viết tay register map ra giấy. Chụp ảnh commit.
5. **Đo một tín hiệu I2S bất kỳ** và tính ngược ra sample rate từ tần số LRCK.

**Kiến thức cần trong giai đoạn này:**
- Ben Eater (YouTube) — điện tử cơ bản và bus, chất lượng cao nhất trên internet cho tầng này
- EEVblog Fundamentals (Dave Jones) — cách dùng multimeter, cách đọc datasheet
- SparkFun / Adafruit tutorials — ngắn, chính xác, có sơ đồ
- sigrok/PulseView documentation

**PASS — cả 5:**
1. File capture PulseView (`.sr`) của bus I2C thật, decode ra ACK/NACK, commit **sau** `prediction.md`
2. Bảng 3 tỉ lệ voltage divider: dự đoán vs đo, sai lệch **<5%** mọi dòng
3. Dòng qua LED: tính trước, đo sau, sai lệch **<10%**, kèm giải thích chênh lệch (V_f không phải hằng số, nó phụ thuộc dòng)
4. Register map viết tay, chụp ảnh, đối chiếu đúng ≥90% với datasheet
5. Tính ngược được sample rate từ LRCK đo được, sai lệch **<1%**

**FAIL → action:** chạm 55h chưa PASS → không phải thiếu kiến thức mà sai cách học. Mua một khoá có cấu trúc, cấp thêm 15h, thử lại đúng một lần. Chạm 70h → cắt Track C, chuyển toàn bộ giờ sang Track B.

---

## M2 — MCAP + Foxglove + Protobuf cho sensor

**Intent:** đóng ba gap có tên riêng trong JD Verne, với chi phí gần bằng 0.
**Giờ:** 20h · **Trần:** 30h · **Entry:** không có. **Chạy song song M1, không chờ.**
**Tiền:** 0đ. Không cần phần cứng.

Đây là milestone rẻ nhất và có tỉ lệ đổi-giờ-lấy-tín-hiệu cao nhất trong toàn bộ lộ trình. Làm sớm.

**Việc cụ thể:**
1. `pip install mcap mcap-protobuf-support`. Đọc spec ở `mcap.dev` — đặc biệt phần chunk, index, và message indexing.
2. Tải ≥2 dataset công khai: dataset dưới org `lerobot` trên HF Hub, hoặc rosbag/MCAP mẫu từ Foxglove.
3. Định nghĩa Protobuf schema cho một message cảm biến (ví dụ `ImuSample`: timestamp, frame_id, accel xyz, gyro xyz, **và** trường uncertainty + calibration_id — nguyên tắc số 5).
4. Viết converter: dataset công khai → MCAP với schema đó.
5. Đổi schema v1 → v2 (thêm một trường). Viết test chứng minh reader v1 vẫn đọc được file v2.
6. Cài Foxglove desktop, mở file, chụp màn hình.
7. Thử luôn Rerun (`rerun.io`) cho một dataset, để biết khi nào dùng cái nào.

**PASS — cả 4:**
1. Repo public: đọc ≥2 dataset công khai → ghi ra MCAP hợp lệ với Protobuf schema có version
2. Test tự động chứng minh schema v1 → v2 backward compatible
3. File mở được trong Foxglove không lỗi, có ảnh chụp trong README
4. README trả lời bằng chữ ba câu hỏi: chunk index của MCAP làm gì · tại sao nó quan trọng cho random access trên file 50GB · điều gì xảy ra với file nếu process bị kill giữa lúc ghi

**FAIL → action:** không có kịch bản fail hợp lý. Nếu 30h vẫn không xong, toàn bộ giả thuyết nghề nghiệp cần xem lại — vì đây là phiên bản dễ nhất của công việc đang nhắm.

---

## M3 — ★ Dataset audit tool

**Intent:** artifact công khai đầu tiên chứng minh năng lực tầng dữ liệu robot — **trước khi sở hữu bất kỳ robot nào**.
**Giờ:** 60h · **Trần:** 85h · **Entry:** M2 PASS · **Tiền:** 0đ

Chưa ai làm tốt việc này. Đó là chỗ nổi bật. Và nó không cần phần cứng.

**Việc cụ thể:**
1. Đọc LeRobot Dataset Format trong `huggingface.co/docs/lerobot`. Hiểu episode, observation, state, action được tổ chức thế nào.
2. Viết detector cho từng lớp lỗi, mỗi cái kèm một test case tổng hợp (tự tạo dữ liệu hỏng) để chứng minh detector đúng:
   - timestamp không đơn điệu
   - frame drop (khoảng cách timestamp lệch khỏi kỳ vọng)
   - lệch giữa hai stream (camera vs robot state)
   - outlier độ dài episode
   - desync action/state (action tại t không khớp state chuyển tiếp t→t+1)
3. Chạy trên ≥5 dataset công khai trên HF Hub.
4. Viết report generator: HTML hoặc markdown, có biểu đồ phân bố.
5. Tìm được lỗi thật → viết script reproduce tối giản → báo cáo ra ngoài (issue trên repo/dataset, hoặc LeRobot Discord).
6. Viết bài tiếng Anh: *"Auditing LeRobot datasets: what breaks and how to detect it"*. Cross-post r/robotics, Hacker News, LinkedIn.

**PASS — cả 5:**
1. Chạy được trên ≥5 dataset công khai bằng **một lệnh**
2. ≥4 lớp lỗi, mỗi lớp có test case tổng hợp chứng minh detector đúng
3. Tìm ≥1 lỗi **thật** trong ≥1 dataset công khai, có script reproduce
4. Đã báo cáo lỗi đó ra ngoài
5. **Tín hiệu ngoài trong 60 ngày kể từ khi publish:** ≥1 phản hồi có nội dung từ maintainer hoặc người dùng khác, HOẶC ≥10 star

Điều kiện 5 do **người ngoài** chấm. Đó là định nghĩa của không-cảm-tính.

**FAIL → action:**
- Đạt 1–4 nhưng trượt 5 → vấn đề ở kênh phân phối, không phải ở công việc. Cấp thêm 8h cho bài viết và cross-post. Vào LeRobot Discord, hỏi trực tiếp.
- Vẫn trượt sau 90 ngày → đây là tín hiệu thị trường đầu tiên, và là tín hiệu xấu. Chạy M5 ngay, sớm hơn kế hoạch.

---

## M4 — V1 chạy được

**Intent:** đi hết chuỗi số nguyên → áp suất không khí đúng một lần, có số ở mọi chặng.
**Giờ:** 90h · **Trần:** 140h · **Entry:** M0 + M1 PASS, đợt 2 đã mua, B2 đã có câu trả lời

Chi tiết kỹ thuật đầy đủ ở **Phần 4**. Đây là phần gate.

**PASS — cả 7:**
1. Không còn lời gọi cloud TTS nào trong chuỗi — grep repo, chứng minh bằng CI
2. **TN-1:** BCK đo được sai **<1%** so với dự đoán, ở **2** sample rate khác nhau
3. **TN-2:** đường cong latency vs underrun ≥5 điểm `period_size`, mỗi điểm ≥10 phút chạy; latency GPIO→mic đo được với độ phân giải ≤1ms
4. **TN-3:** bảng ≥3 cấu hình nguồn, mỗi dòng có V_rail đo lúc nghỉ và lúc phát, cờ `get_throttled`, mô tả tiếng
5. **TN-4:** F0 giọng mình bằng số; đồ thị SNR đo vs lý thuyết `6.02×bits + 1.76` ở 4 mức bit depth, sai lệch **<3dB**
6. Bảng latency budget: **mọi dòng là số đo, không dòng nào là ước tính**, nút thắt được chỉ tên
7. **TN-5 soak 72h:** ≥20 confession phát đúng, **0** lần can thiệp tay, log rotation đã được chứng minh bằng cách cố tình làm đầy thẻ, ≥3 lần rút điện đúng lúc đang ghi DB mà dữ liệu còn nguyên

**FAIL → action:** chạm 140h chưa PASS → **cắt scope, không gia hạn**. Bỏ điều kiện 5 và 7, chỉ giữ "phát được audio ổn định 24h", publish nguyên trạng kèm ghi chú rõ cái gì chưa làm được, sang M6. V1 không được phép ăn hết năm đầu.

---

## M5 — Đo thị trường

**Intent:** lấy dữ liệu thật về phản hồi thị trường **sớm**, khi đổi hướng còn rẻ.
**Giờ:** 15h · **Entry:** M2 + M3 PASS (phải có cái để chỉ vào) · **Thời điểm:** ~tháng 5–6

Phỏng vấn không tự xuất hiện. Nếu đặt "tháng 12 phải có 1 phỏng vấn" mà không apply gì trong 12 tháng, đó không phải mốc kiểm tra, đó là mong đợi.

**Việc cụ thể:**
1. Viết lại CV theo hướng robot data infra. Bốn dòng đầu phải là: MCAP/Protobuf, time-series ở quy mô, latency p99, và link repo M3.
2. Apply 10 vị trí: 3 VN (Vingroup cluster, IoT công nghiệp, manufacturing data), 4 remote EU (robotics tooling, fleet data), 3 US-remote.
3. Gửi 5 tin nhắn outreach tới người đang làm đúng vai trò đó (LinkedIn, ROS Discourse, Foxglove community). Không xin việc — hỏi một câu kỹ thuật cụ thể về bài toán của họ, kèm link M3.

**PASS/FAIL — diễn giải cam kết TRƯỚC, không bàn lại lúc có kết quả:**

| Kết quả / 15 lần chạm | Kết luận | Hành động |
|---|---|---|
| ≥2 phản hồi có nội dung | Giả thuyết đúng | Giữ nguyên phân bổ. **Mở gate đợt 4 (SO-101).** |
| 1 phản hồi | CV/định vị sai, không phải năng lực | Sửa CV, chạy lại đúng 1 lần sau 6 tuần |
| 0 phản hồi | Artifact chưa đủ trọng lượng | **Hoãn SO-101.** Dồn giờ vào M6 + M7. Chạy lại M5 sau M6. |
| 0 phản hồi lần thứ hai | Sai định vị hoặc sai thị trường | Kích hoạt Track A gấp (xem M9) |

Sau M5, lặp Track D mỗi quý: 5 application + 2 outreach, ghi tỉ lệ phản hồi vào repo. Đường xu hướng của tỉ lệ này là chỉ số sức khỏe thật của toàn bộ kế hoạch.

---

## M6 — ★ VLA edge benchmark

**Intent:** làm đúng công việc 8 năm qua, đổi payload. ROI trên mỗi giờ cao nhất trong lộ trình.
**Giờ:** 70h · **Trần:** 95h · **Entry:** M2 PASS · **Tiền:** thuê GPU ~500k–1.5tr

Có hẳn một nhánh nghiên cứu về tối ưu runtime VLA (vla.cpp, VLA-Perf, BitVLA 1-bit). Đó là quantization và benchmark inference — chính xác nghề bạn đang làm.

**Việc cụ thể:**
1. Chọn ≥3 model: SmolVLA (nhẹ nhất, bắt đầu ở đây), OpenVLA, và một trong π0 (`Physical-Intelligence/openpi`) hoặc GR00T N1.
2. Chọn ≥2 target: Pi 5, GPU thuê. (Jetson chỉ nếu M6 chứng minh được là cần — đừng mua trước.)
3. Viết harness: chạy bằng một lệnh, cấu hình bằng file, output JSON chuẩn.
4. **Methodology là phần quan trọng nhất, không phải con số.** Phải xử lý: warm-up bao nhiêu iteration, cách cô lập thermal throttling (`vcgencmd measure_temp` + `get_throttled` trên Pi, `nvidia-smi` trên GPU), cách pin CPU frequency, cách loại nhiễu từ tiến trình khác.
5. Báo cáo p50/p95/p99 latency, RTF, VRAM peak, throughput. **Không báo cáo mean.**
6. Viết bài tiếng Anh: *"Benchmarking VLA inference on edge hardware"*. Đăng kèm harness.
7. Nhờ ≥1 người trong LeRobot Discord chạy lại harness và xác nhận số.

**PASS — cả 5:**
1. ≥3 model × ≥2 target
2. Báo cáo p50/p95/p99, RTF, VRAM peak, throughput
3. Methodology mô tả rõ warm-up và cách cô lập thermal throttling, **kèm số chứng minh đã cô lập được** (ví dụ: nhiệt độ ổn định ±2°C trong suốt phép đo)
4. ≥1 người ngoài reproduce được và xác nhận công khai
5. Bài viết tiếng Anh publish + repo public

**FAIL → action:** không đủ target phần cứng → chạy toàn bộ trên GPU thuê ở ≥2 cấu hình khác nhau (ví dụ 3090 vs 4090, hoặc cùng card khác batch size). Vẫn hợp lệ, vẫn publish được.

---

## M7 — ★ Sensor data platform

**Intent:** artifact duy nhất mà kỹ năng dữ liệu gặp phần cứng thật, với **số đo sync thật**. Đây là chỗ hệ phân tán gặp vật lý.
**Giờ:** 150h · **Trần:** 200h · **Entry:** M4 PASS, đợt 3 đã mua

**Nguyên tắc scope:** số đo là deliverable, platform là vỏ. Rủi ro lớn nhất ở milestone này là phần mềm (thế mạnh) xong nhanh và đẹp, còn phần khác biệt thật — số đo sync — thì mỏng. Đảo lại thứ tự làm: đo trước, dựng platform sau.

**Việc cụ thể:**

*7.1 — Sensor + ESP32-S3 (~30h)*
1. IMU (ICM-42688 tốt hơn, MPU6050 rẻ và nhiều tài liệu), ToF VL53L1X, nhiệt/ẩm BME280.
2. **Đọc raw register, không dùng thư viện wrapper.** Tự convert raw int16 → đơn vị vật lý bằng scale factor trong datasheet.
3. ESP32-S3 làm node cảm biến, gửi về Pi qua UART **và** WiFi. So sánh hai đường: latency, jitter, packet loss.

*7.2 — Time sync (~50h, phần quan trọng nhất)*
1. **Thí nghiệm 1:** ESP32 và Pi cùng đọc một sự kiện (một chân GPIO chung được kéo lên). So timestamp hai bên. Đo lệch, vẽ phân bố.
2. **Thí nghiệm 2:** bật `linuxptp` giữa Pi và LAN box qua Ethernet. Đo lại. Ghi phân bố trước/sau.
3. **Thí nghiệm 3:** đo drift clock ESP32 theo nhiệt độ — chạy 6 tiếng, hơ nóng bằng máy sấy, ghi ppm.
4. **Thí nghiệm 4:** hardware trigger — một xung chung kích cả camera và IMU. So với software timestamp.
5. Với mỗi thí nghiệm, phải nêu **sai số của chính phép đo**. Bạn đang đo lệch cỡ µs bằng dụng cụ có độ phân giải bao nhiêu?

Tài liệu: IEEE 1588 PTP qua `linuxptp` docs · `chrony` docs phần hardware timestamping · Foxglove blog series về time trong robotics.

*7.3 — Data stack (~70h)*
1. Ghi log cảm biến vào **MCAP** với Protobuf schema versioned (dùng lại M2).
2. Upload resumable lên **MinIO/S3**.
3. Index vào **ClickHouse** hoặc TimescaleDB.
4. Ingestion check: schema validation, dedupe, drift detection, alert freshness.
5. **Validation theo vật lý, không chỉ theo schema.** Ví dụ: |a| lúc đứng yên phải bằng g địa phương ±ngưỡng; nhiệt độ không thể đổi 20°C trong 100ms; ToF không thể đọc âm.
6. Mở được bằng Foxglove.

**PASS (MVP — đây là gate) — cả 5:**
1. 2 thiết bị, 3 sensor, ghi MCAP với Protobuf schema có version
2. **Sync đo được:** phân bố offset clock trước/sau khi bật PTP, ≥1 giờ dữ liệu, có nêu phương pháp đo **và sai số của phép đo đó**
3. ≥1 rule validation theo vật lý bắt được dữ liệu xấu thật, chứng minh bằng một lần cố tình gây lỗi
4. Chạy 7 ngày không can thiệp, completeness ≥99%, alert freshness **đã thực sự bắn** ≥1 lần khi cố tình ngắt một nguồn
5. Bisect được lỗi qua 4 tầng (pipeline → firmware → bus → sensor), có ghi lại ≥1 lần bisect thật trong notebook

**Stretch, KHÔNG phải gate:** calibration registry có version, dashboard drift, mission registry, retention/review-for-deletion.

**Bài viết:** *"Time synchronization for multi-sensor robots: PTP vs hardware trigger, measured"*.

**FAIL → action:** PTP không chạy được sau 60h → chuyển sang hardware-trigger-only sync, đo lệch bằng GPIO chung. Kết quả vẫn publish được, vẫn trả lời được câu hỏi phỏng vấn. Không đâm đầu vào `linuxptp`.

---

## M8 — SO-101 + LeRobot (có điều kiện)

**Intent:** vào ecosystem robot learning bằng đúng nghề dữ liệu.
**Giờ:** 120h · **Trần:** 160h · **Tiền:** 7–13tr

**Entry — cả 3, không bỏ qua cái nào:**
- M5 PASS ở mức "≥2 phản hồi"
- M3 và M6 đã publish
- Đã đặt hàng trước điểm cần dùng ≥8 tuần

SO-101 là ngoại lệ với quy tắc "không mua kit". Lý do: nó không phải kit đồ chơi, nó là hạ tầng nghiên cứu đang được dùng ở lab học thuật toàn cầu, và nó đưa bạn thẳng vào ecosystem robot learning hiện đại. Cánh tay 6-DOF open source, lắp 3–4 tiếng, do Hugging Face làm cùng The Robot Studio.

**Việc cụ thể:**
1. Đặt **cặp** leader + follower (leader để cầm tay điều khiển, follower để bắt chước hoặc chạy policy). Vendor: Seeed Studio, WowRobo, PartaBot, Hiwonder, ThinkRobotics. Rẻ nhất: tự in 3D + mua servo STS3215.
2. Lắp, calibrate, teleoperation.
3. **Định nghĩa task và metric thành công bằng văn bản TRƯỚC khi thu dữ liệu.** Ví dụ: "nhặt khối gỗ 3cm từ vùng A đặt vào hộp B, thành công = khối nằm trong hộp sau 30s".
4. Thu 50 episode `lerobot-record`, đẩy lên HF Hub.
5. Train một policy (ACT hoặc Diffusion Policy) trên GPU thuê. ACT 52M params ≈ 4h trên RTX 3080.
6. Chạy inference thật, đo success rate trên 20 lần thử.
7. **Rồi làm phần của bạn:** chạy tool M3 lên chính dataset của mình. Episode nào drop frame? Timestamp có đều? Camera và encoder có đồng bộ? Sửa lỗi tìm được, thu lại phần hỏng, train lại, **đo success rate trước/sau**.

**PASS — cả 4:**
1. 50 episode trên HF Hub, task và metric đã định nghĩa bằng văn bản trước khi thu
2. Policy train xong, chạy inference thật, success rate **≥30%** trên 20 lần thử
3. Tool M3 chạy trên dataset của mình, tìm ≥1 lỗi thật, đã sửa
4. Có một con số so sánh success rate **trước/sau** khi sửa dữ liệu — đó mới là nội dung bài viết, không phải "tôi train được policy"

**FAIL → action:** success rate <20% sau 40h lặp → **publish dataset + phân tích thất bại**. Negative result có tài liệu tốt vẫn là artifact hợp lệ, và trong ngành này còn được đánh giá cao. Đừng train lại lần thứ tư.

**Hai bẫy vận hành đã biết:**
- Đừng dùng **hai camera cùng model** — USB path bị gán lại giữa chừng và làm crash recorder. Dùng hai model khác nhau.
- Một kit chỉ đủ cho scripted motion và debug servo. Workflow leader-follower cần đủ **hai** cánh tay.

---

## M9 — Điểm quyết định

Không phải milestone công việc. Là hai lần dừng lại đọc số, với luật viết trước.

### Tháng 12

| Điều kiện | Hành động |
|---|---|
| M2+M3+M4 PASS, M5 ≥2 phản hồi | Tiếp như viết. Mở M8. |
| M2+M3 PASS, M4 trượt hoặc chậm | Track C quá đắt so với giờ có. **Cắt M8 và mọi thứ về robot di động.** Dồn vào M6+M7. Vẫn là hồ sơ tốt cho robot data infra. |
| M5 = 0 phản hồi hai lần liên tiếp | Không phải thiếu artifact. Đổi hướng: ưu tiên **Track A** — chuyển việc sang công ty có phần cứng ở đúng vai trò hiện tại. |
| Tổng giờ tích lũy <250h | Ràng buộc là công việc, không phải lộ trình. Giải quyết ràng buộc trước. Giữ Track B ở chế độ tối thiểu 2h/tuần. |

### Tháng 18

| Điều kiện | Hành động |
|---|---|
| ≥1 phỏng vấn thật đã diễn ra | Chuyển 6 tháng cuối sang chuẩn bị phỏng vấn + apply có hệ thống. Giảm giờ build. |
| 0 phỏng vấn, cả 3 artifact ★ đã publish | Vấn đề ở kênh, không ở nội dung. 6 tháng cuối dồn cho outreach có mục tiêu, hội nghị, và đóng góp upstream vào `lerobot`/`mcap`. |
| 0 phỏng vấn, <2 artifact ★ | Chấp nhận: 24 tháng không đủ với ngân sách giờ này. Chuyển sang mục tiêu 36 tháng, hoặc chuyển sang hướng sản phẩm. **Đây là kết quả hợp lệ, không phải thất bại.** |

---

## Track A — chạy nền suốt 24 tháng, 40h

Không có milestone riêng vì phụ thuộc thị trường việc làm, nhưng đây là **đòn bẩy lớn nhất trong toàn bộ kế hoạch**.

Nội dung: theo dõi các công ty ở VN có phần cứng thật — cụm Vingroup (VinRobotics/VinMotion/VinDynamics), IoT công nghiệp, manufacturing data, bán dẫn — ở đúng vai trò backend/data/infra hiện tại, **không** phải vai trò robotics engineer. Mục tiêu là được **trả tiền để tích lũy domain**, thay vì học buổi tối.

Cùng kỹ năng, cùng mức lương hoặc cao hơn, nhưng đồng hồ tích lũy domain chạy trong giờ hành chính thay vì 6h/tuần buổi tối. Đó là chênh lệch 40h/tuần so với 6h/tuần.

**Kiểm tra hàng quý, nhị phân:** đã xem ≥5 JD mới trong quý và ghi lại vào repo? Có / Không.

---

# PHẦN 4 — CHI TIẾT KỸ THUẬT V1 (cho M4)

## 4.1 Kiến trúc

Phiên bản dễ — **đừng làm**: `Google Form → Pi polling → cloud TTS → aplay → jack 3.5mm → loa`. Xong trong một buổi tối, học được số không.

Phiên bản làm:

```
Google Form ──► Google Sheet
                    │
         Apps Script webhook (hoặc Sheets API polling)
                    ▼
┌────────────────────────────────────────────┐
│  LAN BOX (PC có GPU, hoặc tạm dùng laptop) │
│    ingest API (FastAPI)                    │
│      → dedupe + state machine              │
│      → moderation queue         ← BẮT BUỘC │
│      → job queue                           │
│    TTS worker (VietTTS / Viterbox)         │
│      → PCM 16-bit / 24 kHz                 │
│      → stream chunk đầu tiên ngay          │
└──────────────────┬─────────────────────────┘
                   │ HTTP chunked / WebSocket (Ethernet)
                   ▼
┌────────────────────────────────────────────┐
│  Raspberry Pi 5                            │
│    player daemon (systemd, Rust hoặc Python)│
│      → ring buffer                         │
│      → ALSA trực tiếp (KHÔNG gọi aplay)    │
│      → GPIO pin đánh dấu sample đầu tiên   │
└──────────────────┬─────────────────────────┘
                   │ I2S: BCK / LRCK / DIN / GND
                   ▼
        PCM5102A (DAC) ──line out──► Class-D amp ──► Loa 4Ω
```

Kiến trúc 3 tầng này là kiến trúc production thật, và về sau mở rộng thẳng thành:
`LAN GPU box (train, heavy inference, log store)` → `Pi/Jetson (perception, ROS 2, planner)` → `ESP32-S3 (hard real-time: motor, encoder, IMU, E-stop)` → thế giới vật lý.

## 4.2 Bốn quyết định phải tự bảo vệ được

**1. Tại sao TTS chạy ở LAN box chứ không trên Pi.** Câu trả lời không phải "Pi yếu". Câu trả lời là một con số: **RTF (real-time factor)**. Phải đo RTF của model trên cả hai máy rồi mới được quyết. Có model chạy real-time thật trên CPU — VieNeu-TTS được thiết kế cho inference real-time trên CPU ở 24kHz. Nếu đo ra RTF < 1 trên Pi thì kiến trúc của bạn sai và nên chạy on-device.

**2. Tại sao I2S chứ không phải jack 3.5mm.** Lý do đơn giản: Pi 5 đã bỏ jack 3.5mm. Lý do thật: bạn muốn nhìn thấy tín hiệu số trước khi nó thành analog. Với I2S bạn cắm logic analyzer và *nhìn thấy* từng bit sample chạy trên dây. Với USB sound card, toàn bộ chuỗi bị giấu trong firmware.

**3. Push hay pull.** Apps Script webhook cần endpoint public (ngrok/Cloudflare Tunnel), trễ <1s. Sheets API polling đơn giản, không cần expose gì, nhưng trễ bằng nửa chu kỳ poll. Chọn có lý do và ghi lý do vào `decisions.md`.

**4. Moderation là yêu cầu kỹ thuật, không phải nice-to-have.** Xem B5.

## 4.3 Latency budget — điền số đo thật

| Chặng | Ước tính | Kiểm soát được? |
|---|---|---|
| Submit form → Sheet có dữ liệu | 1–3s | Không |
| Phát hiện record mới | webhook <1s / poll = T/2 | Có |
| TTS sinh audio | RTF × độ dài | Có |
| Truyền qua LAN | ~5–15ms | Có |
| ALSA buffer | 20–200ms | **Có, và đây là bài học chính** |
| DAC + amp + loa | <1ms | Không |

Bạn sẽ phát hiện nút thắt nằm ở Google, không ở code của mình. Bài học một: **tối ưu đúng chỗ.** Bài học hai: stream chunk đầu của TTS thay vì đợi sinh xong cả file làm latency *cảm nhận* giảm mạnh trong khi latency *tổng* không đổi.

## 4.4 Năm thí nghiệm bắt buộc

Quy tắc chung: **dự đoán bằng số trước, đo sau, commit dự đoán trước.**

### TN-1: Nhìn thấy âm thanh trên dây
**Câu hỏi:** với audio 24kHz, 16-bit, stereo, BCK và LRCK phải là bao nhiêu?
**Dự đoán:** BCK = 24000 × 16 × 2 = 768 kHz. LRCK = 24 kHz. Data rate = 768 kbit/s.
**Đo:** logic analyzer vào BCK/LRCK/DIN, bật decoder I2S trong PulseView.
**Rồi phá nó:** đổi sample rate sang 48kHz — dự đoán lại, đo lại. Đổi sang mono. Cấu hình sai chân FMT, xem điều gì xảy ra.
**Học được:** sample rate không còn là tham số trừu tượng, nó là một xung clock có thật trên sợi dây bạn cầm được.

### TN-2: Đo latency thật từ phần mềm ra không khí
**Quan trọng nhất trong năm cái** — nó nối trực tiếp 8 năm kinh nghiệm của bạn vào thế giới vật lý.
**Setup:** kéo một chân GPIO lên HIGH tại đúng dòng code ghi sample đầu tiên vào ALSA. Đặt mic INMP441 trước loa. Ghi đồng thời chân GPIO (logic analyzer) và tín hiệu mic.
**Đo:** khoảng cách giữa cạnh lên GPIO và lúc mic bắt được sóng âm. Đó là latency thật: ALSA buffer + DAC + amp + thời gian truyền trong không khí.
**Rồi quét tham số:** đổi `period_size` và `buffer_size` qua 5 giá trị. Mỗi giá trị ghi latency **và** số lần underrun trong 10 phút.
**Vẽ:** latency vs underrun rate.
**Học được:** đây chính xác là đường cong latency-vs-reliability bạn đã tối ưu ở tầng API, nhưng failure mode là tiếng "tách" nghe được bằng tai thay vì một dòng log.

### TN-3: Cố tình làm hỏng nó bằng nguồn
1. Lấy 5V cho amp từ chính chân 5V của Pi. Mở âm lượng tối đa, phát bass mạnh. Đo V rail bằng multimeter trong lúc phát. Chạy `vcgencmd get_throttled`.
2. Tháo dây GND chung giữa DAC và amp. Nghe. Đo.
3. Tách nguồn riêng cho amp, giữ common ground. Đo lại. Thêm tụ 470µF–1000µF sát chân nguồn amp. Đo lại.

| Cấu hình | V rail (nghỉ / phát) | throttled flag | Mô tả tiếng |
|---|---|---|---|

**Học được:** current surge, voltage sag, common ground, decoupling. Quan trọng hơn: bạn tự tay tạo lỗi rồi tự tay sửa — nên sau này khi motor làm ESP32 reset, bạn nhận ra ngay chứ không mất ba ngày.

### TN-4: Từ không khí thành số nguyên, và ngược lại
- **4a.** Ghi giọng mình nói "aaaaa" bằng INMP441, lưu raw PCM. Vẽ waveform. FFT. Tìm F0 của giọng bạn. Ghi lại — đó là một thông số vật lý của chính bạn.
- **4b.** Cho TTS đọc cùng câu đó, ghi lại bằng chính mic đó, FFT, so hai phổ. Bạn đang đo *khoảng cách* giữa giọng thật và giọng máy, bằng số, trước khi V2 bắt đầu.
- **4c.** Ghi âm quá to đến mức clip. Nhìn waveform bị cắt phẳng đầu. Nhìn phổ: hài bậc cao xuất hiện.
- **4d.** Giảm bit depth 16 → 12 → 8 → 4. Nghe từng mức. Đo noise floor trên phổ. Tính SNR lý thuyết `≈ 6.02 × bits + 1.76 dB` và so với đo được.
- **4e.** Trong lúc loa phát tone 100Hz, đo điện áp AC trên hai đầu loa. Tính `P = V²/R` với R là trở kháng ghi trên loa. So với công suất amp công bố. Chạm nhẹ tay vào màng loa. Bạn vừa đi hết chuỗi: số nguyên → điện áp → dòng qua cuộn dây → lực từ → chuyển động màng → áp suất không khí.

### TN-5: 72 giờ không ai trông
- `systemd` với `Restart=always`, hardware watchdog bật
- structured log, trả lời được "3h sáng thứ Bảy nó làm gì"
- xử lý mất mạng, Google API lỗi, TTS worker chết
- log rotation — thẻ SD hỏng vì ghi nhiều là chuyện có thật
- **rút điện đột ngột 10 lần**, ≥3 lần đúng lúc đang ghi DB. Bật lại. Dữ liệu còn nguyên không?
- theo dõi nhiệt độ CPU suốt 72h
- đo dòng tiêu thụ trung bình bằng USB power meter → số đầu tiên trong power budget về sau

## 4.5 Bẫy cụ thể sẽ gặp

- **Pi 5 không có jack 3.5mm.** Bắt buộc I2S hoặc USB.
- **I2S trên Pi cần bật overlay** trong `/boot/firmware/config.txt` (`dtoverlay=hifiberry-dac` cho PCM5102A) và nó chiếm GPIO 18/19/21. Đừng dùng những chân đó cho việc khác.
- **Chân SCK của module PCM5102A** thường cần nối GND để dùng PLL nội. Không nối, DAC im lặng và bạn sẽ nghĩ nó hỏng.
- **Đừng nối loa trực tiếp vào line-out của DAC.** Sai trở kháng, không đủ dòng, có thể làm chết DAC.
- **Logic analyzer clone 24MHz** đủ cho I2S ở 768kHz nhưng sẽ chật vật ở sample rate cao. Biết giới hạn của dụng cụ đo cũng là một phần của việc đo.
- **Mua 2 cái cho mọi module rẻ và quan trọng.** Không có module thứ hai để so, bạn không phân biệt được "module chết" với "cấu hình sai" — và sẽ mất nhiều ngày.

## 4.6 TTS tiếng Việt (dùng ở V1, fine-tune ở V2)

Đã có sẵn nhiều lựa chọn, **đừng train from scratch**:
- **VietTTS** (dangvansam) — server API tương thích định dạng OpenAI, clone giọng từ file audio local, cài qua pip hoặc Docker
- **VieNeu-TTS** — hướng on-device, inference real-time trên CPU ở 24kHz
- **Viterbox** — fine-tune từ Chatterbox, zero-shot clone với 3–10 giây mẫu, huấn luyện trên >3.000h dữ liệu tiếng Việt. License CC BY-NC → chỉ dùng nội bộ.
- **F5-TTS-Vietnamese** (hynt)

Ở V1 chỉ cần chọn một cái, chạy được, và **đo RTF trên cả Pi lẫn LAN box**. Đó là dữ liệu để quyết kiến trúc.

Về sau (nếu làm V2 clone giọng mình): bài học thật không nằm ở "train được", mà ở tự thu dataset giọng mình, đo WER/MOS trước-sau, quantize, đo RTF trên từng thiết bị, và quyết định chạy ở đâu. Đó chính là kỹ năng edge AI thật. Thuê GPU, đừng mua card.

---

# PHẦN 5 — MUA SẮM

Giá ước tính, kiểm tra lại khi mua.

## Đợt 1 — mua ngay (~1.5–2.5tr)

| Món | Spec | Giá ~ |
|---|---|---|
| Logic analyzer USB 8 kênh 24MHz | Clone Saleae, dùng PulseView | 150–250k |
| Multimeter UNI-T UT33D+ | Đủ để bắt đầu | 285k |
| USB power meter | Đo dòng | 150–250k |
| Breadboard 830 + jumper | M-M / M-F / F-F | 100k |
| Kit điện trở + tụ + LED + nút | | 150–250k |
| Mỏ hàn chỉnh nhiệt T12/936 + thiếc + flux | | 400–700k |
| Nguồn bench có giới hạn dòng | Tuỳ chọn, rất nên có — sẽ cứu bạn vài lần cháy linh kiện | 600k–1.5tr |

## Đợt 2 — sau M0 + M1 PASS (~3.5–4.5tr)

| Món | Spec | Giá ~ |
|---|---|---|
| Raspberry Pi 5 **8GB** | Không mua Pi 4 | 2.4–2.5tr |
| Nguồn USB-C PD 5V/5A 27W chính hãng | Bắt buộc chính hãng | 250–400k |
| microSD 64GB A2 | Samsung Evo Plus / SanDisk Extreme | 200–280k |
| Case + Active Cooler | | 150–300k |
| GY-PCM5102 (DAC I2S) | **Mua 2 cái** | 50–90k/cái |
| MAX98357A (I2S amp) | Để so sánh kiến trúc | 60–100k |
| Amp class-D PAM8403/TPA3110 | | 30–120k |
| Loa full-range 4Ω 3–5W ×2 | Phải có in thông số | 50–150k |
| INMP441 (mic I2S) | **Mua 2 cái** | 60–100k |
| Cáp Ethernet Cat6 | Dùng LAN, không WiFi khi dev | 30–50k |

## Đợt 3 — sau M4 PASS (~2–3tr)

ESP32-S3 DevKit ×2 (~200k/cái) · IMU ICM-42688 hoặc MPU6050 (~85–250k) · ToF VL53L1X (~150k) · BME280 (~80k) · Pi Camera Module 3 (~700k–1tr) · microSD dự phòng · cáp và linh kiện lặt vặt.

ESP32-**S3** chứ không phải ESP32 thường: có I2S, PSRAM, vector instruction cho audio.

## Đợt 4 — sau M5 PASS (~7–13tr)

**SO-101 cặp leader + follower.** Giá thật cần biết: con số "~100 USD" hay lưu truyền là giá sàn cho *một* cánh tay. Một **cặp** assembled kèm camera từ vendor quốc tế khoảng **200–400 USD**; cộng ship + thuế nhập về VN, đặt kế hoạch **7–13tr**. Vendor: Seeed Studio, WowRobo, PartaBot, Hiwonder, ThinkRobotics. Rẻ nhất: tự in 3D + mua servo STS3215 (follower dùng bản 12V/30kg·cm, leader dùng bản 7.4V để giữ back-drivable).

Cộng 2 webcam USB **khác model** (xem bẫy ở M8).

## Ngoài phạm vi 24 tháng

Jetson Orin Nano Super (7–10tr) · máy in 3D (3–6tr) · lidar 2D RPLidar A1 (1.5–2.5tr) · motor + chassis + LiPo. Xem Phần 8.

## Nơi mua tại Hà Nội

**Cửa hàng có địa chỉ:**
- **Linh Kiện Điện Tử 3M / chotroihn.vn** — Số 9, Ngõ 40/2 Tạ Quang Bửu, Bách Khoa, Hai Bà Trưng. Có Pi 5, logic analyzer.
- **Lập Trình Nhúng A-Z** — Số 6, Ngách 38/12, Ngõ 38 Khúc Thừa Dụ, Dịch Vọng, Cầu Giấy. Có PCM5102A và module nhúng.
- **Chợ Trời** — khu Thịnh Yên / Hòa Bình, Hai Bà Trưng. Linh kiện thụ động, rẻ, có ngay.

**Online toàn quốc:** mlab.com.vn · pivietnam.com.vn · cytrontech.vn · linhkienaiot.com · dientudat.com · hshop.vn · nshopvn.com · dientutuyetnga.com

**Quốc tế:** Seeed Studio · Adafruit · SparkFun · Mouser · DigiKey · AliExpress (chấp nhận rủi ro hàng nhái)

---

# PHẦN 6 — KÊNH KIẾN THỨC

## 6.1 Tài liệu gốc — đọc thay vì xem tutorial

| Nguồn | Dùng cho |
|---|---|
| Datasheet từng con chip | **Quan trọng nhất trong bảng này** |
| `mcap.dev` | Format log robot |
| `foxglove.dev/docs` | Data platform |
| `rerun.io/docs` | Visualization |
| `huggingface.co/docs/lerobot` | Robot learning, dataset format |
| `docs.ros.org` | ROS 2 — nguồn chính, không dùng blog copy |
| `docs.nav2.org` | Navigation stack |
| Raspberry Pi documentation | Pinout, GPIO, I2C/SPI/UART, cảnh báo điện áp và motor |
| Espressif ESP-IDF Programming Guide | ESP32 — dùng tài liệu hãng |
| `linuxptp` + `chrony` docs | Time sync, hardware timestamping |

## 6.2 ROS 2 — track song song, ~3h/tuần từ sau M1

Bạn không cần robot để học ROS 2. Cài Ubuntu 24.04 + ROS 2 Jazzy trong Docker, học bằng turtlesim.

Điều quan trọng với bạn: **ROS 2 là pub/sub trên DDS, có QoS policy** — reliability, durability, history depth, deadline. Bạn sẽ thấy rất quen. Điểm khác biệt phải nắm: **TF tree** (cây biến đổi tọa độ giữa các khung), và tại sao mọi thứ trong robot đều gắn với một frame.

- `docs.ros.org` — đọc thay vì xem video
- **Articulated Robotics** (YouTube, Josh Newans) — build robot ROS 2 từ đầu trên phần cứng thật. Nguồn tốt nhất cho người thực dụng.
- **The Construct** (`theconstruct.ai`) — môi trường ROS chạy sẵn trên browser, đỡ mất thời gian setup
- Udemy "ROS 2 for Beginners (Jazzy)" — nếu cần cấu trúc tuyến tính

## 6.3 Toán — học trên chính raw data của mình, ~2h/tuần

Đây là chỗ tách "người ghép module" khỏi "engineer", và là chỗ AI hỗ trợ code không giúp được. Bốn mảng, theo thứ tự:

1. **Linear algebra + rigid body transform SE(3)** — quaternion, rotation matrix, frame transform. Không có cái này thì IMU và camera là hộp đen vĩnh viễn. Bắt đầu bằng 3Blue1Brown "Essence of Linear Algebra", rồi Modern Robotics chương 2–3.
2. **Probability & estimation** — complementary filter → Kalman → EKF. Đây là câu trả lời cho "tại sao gyro drift".
3. **Signals** — sampling, aliasing, FFT, filter design. Đi cùng chain audio ở M4.
4. **Control** — PID → state space → cơ bản về stability. Chỉ đủ từ vựng.

**Cách học hiệu quả với bạn:** thu 10 phút dữ liệu IMU của chính mình ở M7, tự viết complementary filter, so với EKF, vẽ drift. Không học chay từ sách.

## 6.4 Sách

**Bắt buộc:**
- **Kalman and Bayesian Filters in Python** — Roger Labbe. GitHub, free, dạng Jupyter notebook chạy được. Cách học filter tốt nhất hiện có.
- **Modern Robotics: Mechanics, Planning, and Control** — Lynch & Park. PDF free trên trang khoá học Northwestern. Đọc chương 2–3.
- **State Estimation for Robotics** — Timothy Barfoot. PDF free.

**Tham khảo khi cần:**
- **Making Embedded Systems** — Elecia White. Tư duy embedded cho người từ software. Đọc sớm.
- **Practical Electronics for Inventors** — Scherz & Monk. Dễ vào.
- **The Art of Electronics** — Horowitz & Hill. Dùng như từ điển, không đọc tuần tự.
- **Probabilistic Robotics** — Thrun, Burgard, Fox. Kinh điển về SLAM/localization. Nặng, chỉ khi cần.

## 6.5 Khoá học

- **Modern Robotics Specialization** (Coursera, Northwestern) — audit free
- **Robotics: Perception / Estimation** (Coursera, UPenn)
- **Underactuated Robotics** (MIT, Russ Tedrake) — free, YouTube + notes. Nặng nhưng hay.
- **The Construct** — ROS chạy trên browser
- Class Central có tổng hợp 60+ khoá ROS 2, lọc theo nhu cầu

## 6.6 YouTube — chọn lọc, không lướt

| Kênh | Mảng |
|---|---|
| **Articulated Robotics** (Josh Newans) | ROS 2 + phần cứng thật. Tốt nhất cho người thực dụng |
| **Ben Eater** | Điện tử và bus ở mức bản chất |
| **Phil's Lab** | PCB design, embedded, DSP. Rất hợp hướng của bạn |
| **EEVblog** | Dụng cụ đo, đọc datasheet |
| **Nikodem Bartnik** | Có series đầy đủ về SO-ARM101 từ lắp ráp tới train policy |
| **Robotics Back-End** | ROS 2 thực hành |
| **James Bruton** | Cơ khí robot DIY, ý tưởng |

## 6.7 Repo để clone và ĐỌC (không chỉ chạy — đọc kiến trúc)

```
foxglove/mcap                        ← format log, đọc kỹ phần indexing
huggingface/lerobot                  ← robot learning end-to-end + dataset format
rerun-io/rerun                       ← visualization, viết bằng Rust
rlabbe/Kalman-and-Bayesian-Filters-in-Python
TheRobotStudio/SO-ARM100             ← thiết kế cánh tay, in 3D
Physical-Intelligence/openpi         ← π0 / π0.5
NVIDIA/Isaac-GR00T                   ← VLA foundation model
openvla/openvla
keon/awesome-physical-ai             ← danh mục paper VLA, world model, embodied AI
ros2/rclpy, ros-navigation/navigation2
sigrokproject/libsigrok
espressif/esp-idf
```

## 6.8 Theo dõi tin tức

- **The Robot Report** — tin ngành, gọi vốn, triển khai
- **IEEE Spectrum Robotics** — chất lượng cao, có chiều sâu
- **Hugging Face blog** (mục robotics) — LeRobot cập nhật liên tục
- **NVIDIA robotics blog** — Isaac, GR00T, Jetson
- **Foxglove blog** — đặc biệt series về time trong robotics
- **arXiv cs.RO** — theo qua list trên X hoặc arxiv-sanity
- **Hội nghị:** ICRA, IROS, CoRL, RSS. Đọc paper list mỗi năm kể cả không dự.
- `humanoid.guide`, `theaiinsider.tech` — mảng humanoid

**Xu hướng cần nắm từ vựng (không cần làm được ngay):** VLA models (π0, π0.5, GR00T N1, OpenVLA, SmolVLA) · diffusion policy · action chunking · world models · sim-to-real · imitation learning từ teleoperation · cross-embodiment. Có cả nhánh **runtime hiệu năng** (vla.cpp, VLA-Perf, BitVLA 1-bit) — nhánh này rất hợp với bạn, vì nó là tối ưu inference, đúng nghề. Đó là nội dung của M6.

## 6.9 Cộng đồng

**Toàn cầu — đây mới là cộng đồng thật của bạn:**
- **ROS Discourse** (`discourse.ros.org`) — nơi ra quyết định của ROS. Đọc, đừng chỉ hỏi.
- **LeRobot Discord** (link trong docs HF) — active, nhiều người đang build SO-101. Đây là nơi báo cáo kết quả M3 và tìm người reproduce M6.
- **Foxglove Slack/community**
- Reddit: `r/robotics`, `r/ROS`, `r/embedded`, `r/AskElectronics`
- Hackaday.io, Hackster.io

**Việt Nam:**
- Group Facebook về Arduino / ESP32 / điện tử — chất lượng không đều nhưng hỏi mua linh kiện thì nhanh
- Forum của hshop / nshop
- Meetup quanh Bách Khoa / UET — theo dõi qua Facebook

Thật lòng: **cộng đồng robotics VN còn mỏng.** Đừng kỳ vọng tìm được mentor trong nước ở mảng này. Đây cũng là lý do viết bài bằng tiếng Anh quan trọng — nó không phải để khoe, nó là cách duy nhất để có người phản biện.

---

# PHẦN 7 — PORTFOLIO

Đây là thứ quyết định, không phải CV. Trong ngành này người ta tuyển qua repo và commit history.

```
github.com/<bạn>/
├── robotics-lab/              lab notebook, hours.csv, decisions.md, mọi thí nghiệm
├── mcap-sensor-toolkit/       M2 — schema versioned, converter, Foxglove
├── lerobot-dataset-audit/     ★ M3 — công cụ chưa ai làm tốt
├── vla-edge-benchmark/        ★ M6 — đo RTF/latency/VRAM các VLA trên edge
├── sensor-data-platform/      ★ M7 — MCAP + PTP + validation theo vật lý
└── confession-robot/          M4 — V1, chứng minh đã chạm phần cứng thật
```

**Ba repo có ★ là ba thứ khiến bạn khác biệt.** Chúng nằm đúng giao điểm giữa cái bạn đã giỏi và cái ngành đang thiếu. Chúng quan trọng hơn con robot.

**Ba bài viết tiếng Anh:**
1. *Auditing LeRobot datasets: what breaks and how to detect it* (sau M3)
2. *Benchmarking VLA inference on edge hardware* (sau M6)
3. *Time synchronization for multi-sensor robots: PTP vs hardware trigger, measured* (sau M7)

Bài về audio latency gộp vào README của M4.

Đăng trên blog cá nhân + cross-post Hacker News / r/robotics / LinkedIn / LeRobot Discord.

---

# PHẦN 8 — PHẠM VI, RỦI RO, VÀ MỘT ĐIỀU GIỮ SUỐT

## 8.1 Nằm ngoài phạm vi 24 tháng — và tại sao

Ghi ra rõ ràng để 12 tháng nữa không tự trách vì "chưa làm được".

| Ngoài phạm vi | Lý do |
|---|---|
| **Robot di động, Nav2, SLAM, lidar** | ~250h+. Không vừa 650h. Và với mục tiêu robot data infra, nó đóng góp ít hơn M7 trên mỗi giờ bỏ ra. Từ robot đứng yên sang robot tự đi là bước nhảy 10x — SLAM, localization, path planning, người đi lại, thảm, dây điện, bậc cửa, và an toàn thật (một khối 8–10kg tự hành đâm vào chân người là tai nạn lao động, không phải bug). |
| **Humanoid / mobile manipulator tự thiết kế** | Không phải project cá nhân ở ngân sách này. Nếu vẫn muốn hướng đó, mục tiêu đúng là **mobile manipulator** (base bánh xe + cánh tay 5–6 DOF), không phải biped — và nó là kế hoạch 36 tháng. |
| **Jetson Orin Nano** | 7–10tr cho thứ chỉ cần khi Pi 5 nghẽn — mà M6 chưa chắc chứng minh được là nghẽn. Mua sau, **nếu** M6 chỉ ra cần. |
| **Máy in 3D** | Dùng dịch vụ in ở HN. Cần <10 lần in trong 24 tháng. |
| **Nhận diện mặt đồng nghiệp** | Rủi ro pháp lý + HR không tương xứng giá trị portfolio. Xem B4. |
| **Fleet scale-out** | Là phần mở rộng của M7, không phải milestone riêng. Xong M7 sớm thì làm. |
| **Tự chế cảm biến (thermistor, photodiode + op-amp)** | ROI thấp. Nguyên tắc số 6: đi tới đáy đúng một chain (audio), dùng module cho phần còn lại. |

**Nếu ngân sách giờ thực tế cao hơn dự kiến** (median >9h/tuần trong 3 tháng liên tục), mở lại theo thứ tự: (1) phần stretch của M7 — calibration registry, drift dashboard · (2) M8 nếu chưa mở · (3) robot di động ở mức tối thiểu "đi 10m có encoder feedback + PID" · (4) Jetson.

## 8.2 Bốn rủi ro lớn nhất

**1. Không đủ giờ.** Lớn hơn mọi rủi ro kỹ thuật. Đã xử lý bằng: ngân sách giờ thật, `hours.csv`, chế độ tối thiểu cho tuần crunch, ba kịch bản ở 0.2, và điểm quyết định tháng 12. Nếu công việc còn những đợt 12–14h/ngày kéo dài nhiều tuần, **giải quyết ràng buộc đó trước**, không phải sau.

**2. Dùng AI để vượt phần cứng.** Lỗi phần cứng không có stack trace. Nếu không tự đo, bạn sẽ có robot chạy được và không hiểu gì thêm — tức là mất đúng thứ đang đi tìm. Đã xử lý bằng ranh giới ở 0.5 và CI check.

**3. Xây phần mềm đẹp, số đo mỏng.** Rủi ro đặc thù của người mạnh backend: M7 dễ biến thành một platform đẹp với sync giả lập. Đã xử lý bằng cách đặt số đo sync làm gate và platform làm stretch.

**4. Làm 24 tháng rồi mới biết thị trường không phản hồi.** Đã xử lý bằng M5 ở tháng 5–6 và vòng lặp Track D hàng quý.

## 8.3 Một điều giữ suốt 24 tháng

Với mỗi module mua về, đừng hỏi "code nào để nó chạy". Hỏi:

> *"Bên trong cái này đang xảy ra hiện tượng vật lý gì, và bằng cơ chế nào nó biến thành con số tôi đang đọc?"*

Cái làm bạn khác biệt trong mười năm tới không phải là biết ROS, mà là vẫn còn muốn hỏi câu đó khi không ai trả tiền cho câu hỏi.

---

# PHẦN 9 — BẢNG DÁN LÊN TƯỜNG

| ID | Milestone | Giờ | Trần | Entry | Chấm bởi |
|---|---|---|---|---|---|
| M0 | Kiểm tra ràng buộc | 8 | 3 tuần | — | Dữ liệu (`hours.csv`) |
| M1 | Đo được | 35 | 55 | M0 | Số đo vs dự đoán |
| M2 | MCAP + Foxglove | 20 | 30 | — | Test tự động |
| M3 | ★ Dataset audit | 60 | 85 | M2 | **Người ngoài** |
| M4 | V1 chạy được | 90 | 140 | M0, M1, đợt 2 | Soak test 72h |
| M5 | Đo thị trường | 15 | — | M2, M3 | **Thị trường** |
| M6 | ★ VLA benchmark | 70 | 95 | M2 | **Reproduce bởi người khác** |
| M7 | ★ Sensor platform | 150 | 200 | M4, đợt 3 | Chạy 7 ngày |
| M8 | SO-101 (có điều kiện) | 120 | 160 | M5 PASS | Success rate ≥30% |
| A | Đổi domain | 40 | — | — | Nhị phân hàng quý |
| D | Vòng thị trường | 45 | — | M5 | Tỉ lệ phản hồi |

**Lõi (M0–M7 + A + D) = 533h.** Vừa với 5h/tuần.
**Cộng M8 = 653h.** Cần 6–7h/tuần. Không còn slack.
Mọi thứ thêm vào phải lấy ra một thứ khác.

**Tuần này làm gì:** tạo repo · bắt đầu `hours.csv` · nhắn quản lý về B2 · mua đợt 1 · bắt đầu M2 (không cần chờ hàng về).
