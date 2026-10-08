# KHÓA 2 — DỮ LIỆU ROBOT MÀ KHÔNG CẦN ROBOT

**Cho:** người đã làm data/backend 8 năm, nhưng chưa từng chạm dữ liệu cảm biến.
**Thời lượng:** ~80h. Chia hai module: 20h + 60h.
**Chi phí:** 0đ. Không cần phần cứng gì cả.
**Chạy song song với Khóa 1.** Khóa 1 cần ngồi bàn có mỏ hàn; khóa này chỉ cần laptop. Tuần bận thì làm khóa này.

**Xong khóa này bạn có:** hai repo public, một trong đó là artifact ★ đầu tiên, một bài viết tiếng Anh, và tín hiệu phản hồi đầu tiên từ người ngoài ngành.

---

## VÌ SAO KHÓA NÀY QUAN TRỌNG HƠN NÓ TRÔNG

Đọc lại JD của Verne Robotics: MCAP/Protobuf, schema contract, buffering, resumable upload, schema validation, dedupe, drift detection, alert freshness, tích hợp Foxglove.

Bạn đã làm gần hết những dòng đó, chỉ khác payload. Cái thiếu là **ba công cụ có tên riêng** và **hiểu bản chất dữ liệu cảm biến**. Khóa này đóng cả hai, trong 80h, với 0đ.

Và có một sự thật ít người nhận ra: **hai trong ba artifact khiến bạn khác biệt đều không cần robot.** Dataset audit tool và VLA benchmark là bài toán dữ liệu thuần. Bạn có thể ra artifact công khai ở tháng thứ 3 thay vì tháng thứ 18.

Đây là lý do khóa này không phải phần phụ trợ cho khóa phần cứng. Nó là đường ngắn nhất tới cuộc phỏng vấn đầu tiên.

---

## KHÁC BIỆT VỚI KHÓA 1

Ở Khóa 1 bạn là newbie hoàn toàn. Ở đây thì không: parquet, schema versioning, index, columnar storage, backward compatibility — bạn đã biết. Tài liệu này **không dạy lại những thứ đó**.

Cái bạn newbie là **miền**: một robot sinh ra dữ liệu gì, timestamp trong robotics khác timestamp trong web ở chỗ nào, thế nào là một episode, và — quan trọng nhất — **dữ liệu robot hỏng trông như thế nào**. Câu cuối là toàn bộ giá trị của Module 2.

**Quy tắc dự đoán-trước-đo-sau vẫn áp dụng.** Trước khi chạy `mcap info`, viết ra bạn kỳ vọng thấy bao nhiêu message, bao nhiêu channel, file bao nhiêu byte. Trước khi vẽ phân bố `dt`, viết ra bạn kỳ vọng hình dạng gì. Ở khóa này nó dễ bỏ qua hơn vì có sẵn stack trace — chính vì thế phải cố ý giữ.

---

# MODULE 1 — MCAP VÀ CÔNG CỤ (20h)

Tương ứng milestone **M2**.

---

## Bài 1 — Một con robot sinh ra dữ liệu gì (2h)

**Câu hỏi:** "dữ liệu robot" cụ thể là những luồng nào, tốc độ bao nhiêu, nặng bao nhiêu?

### Khái niệm

Một robot tay máy hoặc robot di động cỡ nhỏ chạy đồng thời khoảng 5–15 luồng dữ liệu, tần số chênh nhau tới hai bậc độ lớn:

| Luồng | Tần số điển hình | Kích thước một mẫu | Băng thông |
|---|---|---|---|
| Camera RGB 640×480 | 30 Hz | ~900 KB raw / ~30 KB nén | 27 MB/s raw |
| Depth camera | 30 Hz | ~600 KB | 18 MB/s |
| IMU (accel + gyro) | 100–1000 Hz | ~50 B | ~50 KB/s |
| Joint state (vị trí, vận tốc, dòng) | 100–1000 Hz | ~200 B | ~200 KB/s |
| Force/torque sensor | 500–1000 Hz | ~50 B | ~50 KB/s |
| Lidar 2D | 10 Hz | ~4 KB | 40 KB/s |
| Lệnh điều khiển (action) | 10–100 Hz | ~100 B | ~10 KB/s |
| Log, diagnostics | biến thiên | | |

Ba nhận xét quan trọng:

**1. Chênh lệch tần số là bản chất, không phải lỗi thiết kế.** Camera không thể chạy 1kHz, IMU không cần chạy 30Hz. Mọi hệ robot đều là hệ đa tần số. Điều này nghĩa là: **không tồn tại "một dòng dữ liệu" để join theo khóa.** Bạn luôn phải nội suy hoặc chọn mẫu gần nhất theo thời gian — và cách bạn chọn quyết định chất lượng dữ liệu.

**2. Ảnh chiếm 95% dung lượng nhưng chỉ 5% số message.** Đây là lý do format lưu robot log phải xử lý được cả hai chế độ: nhiều message nhỏ và ít message rất lớn. Và là lý do LeRobot dataset lưu ảnh dưới dạng video mp4 chứ không phải từng frame rời.

**3. Một robot chạy 8 tiếng sinh ra 100–800 GB.** Một fleet 20 con sinh ra vài chục TB/ngày. Đây chính là bài toán quy mô bạn đã quen — chỉ đổi payload từ message giao dịch sang mẫu cảm biến.

### So sánh với thứ bạn đã biết

| Web/fintech | Robotics |
|---|---|
| Event stream có schema | Message stream có schema — giống hệt |
| Kafka topic | ROS topic / MCAP channel |
| Partition theo key | Channel theo topic |
| Event time vs processing time | **stamp vs log_time** — xem Bài 2 |
| Idempotency key | `sequence` number trên mỗi channel |
| Schema registry | Schema **nhúng trong chính file** — khác biệt quan trọng |

Dòng cuối cùng đáng dừng lại. Trong hệ của bạn, schema nằm ở registry bên ngoài. Trong MCAP, **schema được nhúng vào trong file**. Lý do: một file log robot phải đọc được sau 5 năm, trên một máy không có mạng, không có registry. Nó phải tự mô tả. Đó là quyết định thiết kế xuất phát từ ràng buộc hiện trường.

### Tự kiểm tra

1. Robot có camera 30Hz và IMU 200Hz. Muốn biết gia tốc *tại thời điểm* một frame ảnh được chụp, bạn làm gì?
2. Vì sao MCAP nhúng schema vào file thay vì tham chiếu tới registry?

<details><summary>Đáp án</summary>

1. Không có mẫu IMU nào trùng chính xác thời điểm đó. Phải chọn: lấy mẫu gần nhất, hoặc nội suy tuyến tính giữa hai mẫu kề. Và phải ghi lại bạn đã chọn cách nào — đó là metadata quan trọng, không phải chi tiết cài đặt.
2. Vì file phải tự mô tả và đọc được offline, sau nhiều năm, không phụ thuộc dịch vụ ngoài. Ràng buộc hiện trường quyết định thiết kế format.
</details>

---

## Bài 2 — Timestamp trong robotics (3h)

**Câu hỏi:** vì sao "thời gian" ở đây khó hơn nhiều so với hệ web?

### Khái niệm

Đây là bài quan trọng nhất trong Module 1. Nếu chỉ nhớ một bài, nhớ bài này.

**Mỗi message có ít nhất hai timestamp, và chúng khác nhau:**

| Tên | Trong MCAP | Nghĩa |
|---|---|---|
| **publish_time** | `publish_time` | Khi phép đo *xảy ra* hoặc message được sinh ra |
| **log_time** | `log_time` | Khi bộ ghi *nhận được* và ghi xuống đĩa |

Trong ROS, cặp tương ứng là `header.stamp` (khi đo) và receive time của bag (khi ghi).

**Hiệu giữa hai số này là latency + buffering của pipeline.** Phân bố của hiệu này là một chỉ số sức khỏe hệ thống, và gần như không ai nhìn nó. Đây là chỗ bạn có lợi thế ngay lập tức, vì bạn đã dành 8 năm nhìn p99.

**Hai loại đồng hồ:**

| Loại | Đặc tính | Vấn đề |
|---|---|---|
| **Wall clock** (`CLOCK_REALTIME`) | Khớp với giờ thật, so sánh được giữa các máy | **Có thể nhảy** — NTP hiệu chỉnh, đổi múi giờ, leap second. Có thể chạy lùi. |
| **Monotonic** (`CLOCK_MONOTONIC`) | Không bao giờ lùi | **Vô nghĩa giữa hai máy.** Mốc 0 là lúc máy khởi động. |

Bạn cần cả hai: monotonic để đo khoảng thời gian trong một máy, wall clock để ghép dữ liệu giữa các máy. Và bạn cần biết offset giữa chúng.

**Bài toán thật:** camera cắm vào Pi, IMU cắm vào ESP32, cả hai gửi dữ liệu về. Timestamp của camera từ đồng hồ Pi, của IMU từ đồng hồ ESP32. Hai đồng hồ này **không đồng bộ** và **trôi khác nhau theo nhiệt độ**. Ghép hai luồng theo timestamp của chúng = ghép sai.

Ở Khóa 5 bạn sẽ đo hiện tượng này bằng tay. Ở khóa này bạn sẽ **tìm ra dấu vết của nó trong dataset của người khác** — vì hầu hết dataset công khai đều có vấn đề này ở mức độ nào đó, và không ai kiểm tra.

**Ba con số cần thuộc:**

```
dt          = khoảng cách giữa hai mẫu liên tiếp cùng channel
jitter      = độ lệch chuẩn của dt
skew        = lệch hệ thống giữa hai channel khác nguồn đồng hồ
drift       = skew thay đổi theo thời gian (thường tính bằng ppm)
```

Với fps = 30, `dt` kỳ vọng = 33.33ms. Jitter vài trăm µs là bình thường. Jitter vài ms nghĩa là có buffering hoặc thiếu real-time. Một `dt` bằng 66.67ms nghĩa là **rớt đúng một frame**.

### Làm

Không cần code. Viết vào `notes/02-time.md` câu trả lời cho ba tình huống:

1. Dataset có `dt` phân bố quanh 33.3ms nhưng có 40 mẫu ở 66.7ms và 3 mẫu ở 100ms. Chuyện gì đã xảy ra? Có nên vứt dataset không?
2. Dataset có `timestamp` giảm ở đúng một chỗ, lùi 1.2 giây, rồi tiếp tục tăng. Nguyên nhân khả dĩ nhất?
3. Hai channel: `observation.images.top` (30Hz) và `observation.state` (30Hz). Nếu ghép theo chỉ số frame thì khớp hoàn hảo, nhưng ghép theo timestamp thì lệch trung bình 15ms và độ lệch tăng dần theo episode. Nói lên điều gì?

<details><summary>Đáp án gợi ý</summary>

1. 40 lần rớt 1 frame, 3 lần rớt 2 frame. Nguyên nhân: CPU quá tải, ghi đĩa chậm, hoặc USB bandwidth. Không nên vứt — nên **ghi nhận và báo cáo**, rồi quyết định theo tỉ lệ. 43 trên vài nghìn frame thường chấp nhận được cho imitation learning; 43 trên 200 thì không.
2. Wall clock nhảy lùi vì NTP hiệu chỉnh giữa lúc ghi. Đây là lý do phải dùng monotonic để đo khoảng cách. Rất phổ biến và gần như không ai kiểm.
3. Hai luồng được đánh timestamp bởi hai nguồn đồng hồ khác nhau, và chúng **trôi** (drift). Ghép theo frame index đang che giấu lỗi. Bất kỳ mô hình nào học từ dữ liệu này đều đang học một quan hệ nhân quả lệch pha.
</details>

---

## Bài 3 — Frame và TF (1h)

**Câu hỏi:** vì sao mọi con số trong robot đều gắn với một cái tên?

### Khái niệm

Trong robotics, một vector `[0.3, 0.0, 0.5]` **không có nghĩa** nếu không nói nó được biểu diễn trong khung tọa độ nào.

- `base_link` — gốc của thân robot
- `camera_link` — gốc của camera
- `imu_link` — gốc của IMU
- `world` / `map` / `odom` — khung cố định ngoài robot

**TF tree** là cây các phép biến đổi giữa các khung: vị trí + xoay của khung con so với khung cha. Biết cây này, bạn chuyển được một điểm từ khung camera sang khung base.

**Với bạn, điều cần nhớ chỉ có một:** mọi message hình học phải có trường `frame_id`. Dataset thiếu `frame_id` là dataset không dùng được cho bất cứ việc gì liên quan tới hình học — và đó là một defect class đáng kiểm.

So sánh: `frame_id` là timezone của dữ liệu không gian. Một timestamp không có timezone là một con số vô nghĩa. Một vector không có `frame_id` cũng vậy.

Không cần học sâu TF ở khóa này. Chỉ cần từ vựng đủ để nói chuyện và để biết trường nào phải tồn tại.

---

## Bài 4 — MCAP: cấu trúc file (2h)

**Câu hỏi:** bên trong một file `.mcap` có gì?

### Khái niệm

MCAP là container cho nhiều luồng message có timestamp, khác schema, khác tần số, trong một file. Nó là format lưu mặc định của ROS 2 từ bản Iron trở đi.

**Cấu trúc file, từ đầu tới cuối:**

```
[Magic bytes]  \x89MCAP0\r\n
[Header]       profile, thư viện ghi
[Schema]       id, tên, encoding ("protobuf" | "jsonschema" | "ros2msg"), nội dung schema
[Channel]      id, schema_id, topic, message_encoding, metadata
[Chunk]        ── nhóm message, nén được (zstd / lz4 / none)
   [Message]      channel_id, sequence, log_time, publish_time, data
   [Message]
   ...
[MessageIndex] offset của từng message trong chunk, theo channel
[Chunk]
[MessageIndex]
...
[DataEnd]
── SUMMARY SECTION ──
[ChunkIndex]   phạm vi thời gian + offset của từng chunk
[Statistics]   tổng số message, số channel, thời gian đầu/cuối
[SummaryOffset]
[Footer]       trỏ tới đầu summary section
[Magic bytes]
```

**Bốn ý cần hiểu, phần còn lại là chi tiết:**

**1. Schema nhúng trong file.** Không cần registry. File tự mô tả. Với Protobuf, nội dung schema là một `FileDescriptorSet` được serialize.

**2. Chunk là đơn vị nén và đơn vị seek.** Message được gom thành chunk, chunk được nén. Muốn đọc một message, phải giải nén cả chunk chứa nó. Chunk lớn = nén tốt hơn nhưng seek đắt hơn. Đây là đúng cái trade-off bạn đã gặp ở columnar storage.

**3. Summary section nằm ở CUỐI file.** Vì khi bắt đầu ghi, bộ ghi chưa biết file sẽ có bao nhiêu chunk. Footer ở cuối trỏ ngược lên đầu summary. Reader muốn seek nhanh thì đọc cuối file trước.

**4. Hệ quả trực tiếp: nếu process bị kill giữa lúc ghi, summary section không tồn tại.** File vẫn đọc được — nhưng chỉ bằng cách quét tuần tự từ đầu, mất khả năng random access. Có công cụ `mcap recover` để dựng lại phần đọc được.

Ý số 4 là câu hỏi trong tiêu chí PASS của M2. Bạn sẽ tự tạo ra tình huống đó ở Bài 7 và nhìn thấy nó.

### So sánh với thứ bạn đã biết

| MCAP | Tương đương |
|---|---|
| Schema record | Avro schema nhúng trong file |
| Channel | Kafka topic + partition metadata |
| Chunk + ChunkIndex | Parquet row group + footer metadata |
| MessageIndex | Offset index trong row group |
| Summary ở cuối | Parquet footer |
| `mcap recover` | Sửa file parquet bị cắt |

Nếu đã làm việc với Parquet, bạn đã hiểu MCAP 70% rồi. Khác biệt lớn nhất: MCAP là **row-oriented và append-only theo thời gian**, vì nó phục vụ ghi streaming trên thiết bị chứ không phải phân tích cột.

### Làm

1. Đọc spec ở `mcap.dev`, mục "Specification". Đọc kỹ phần Records và phần Chunk/Index. ~45 phút.
2. Cài MCAP CLI: tải binary từ GitHub releases của `foxglove/mcap`, hoặc `brew install mcap`.
3. Tải một file MCAP mẫu từ `foxglove.dev` (họ có sample data), chạy:

```bash
mcap info sample.mcap
mcap list channels sample.mcap
mcap list schemas sample.mcap
mcap list chunks sample.mcap
mcap doctor sample.mcap
```

### Số phải ra

`mcap info` in ra: library ghi, khoảng thời gian, thời lượng, tổng số message, danh sách channel với số message mỗi channel, số chunk, tỉ lệ nén.

`mcap doctor` trên file lành lặn: **không báo lỗi nào**.

Trước khi chạy, viết dự đoán vào `notes/04-mcap.md`: bạn nghĩ file có bao nhiêu channel? Tỉ lệ nén khoảng bao nhiêu với zstd trên dữ liệu cảm biến?

### Nếu ra khác

| Triệu chứng | Nguyên nhân |
|---|---|
| `mcap info` báo "no summary section" | File bị cắt hoặc bộ ghi không ghi summary. Thử `mcap recover`. |
| `mcap doctor` báo lỗi | File hỏng thật, hoặc bộ ghi không tuân thủ spec |
| Số message = 0 nhưng file lớn | Chunk chưa được đóng đúng cách |

---

## Bài 5 — Viết file MCAP đầu tiên (4h)

**Câu hỏi:** làm sao biến một luồng số thành file MCAP hợp lệ?

### Làm

**Bước 1 — cài đặt.**

```bash
pip install mcap mcap-protobuf-support protobuf
```

**Bước 2 — định nghĩa schema.** File `proto/sensors/v1/imu.proto`:

```protobuf
syntax = "proto3";
package sensors.v1;

import "google/protobuf/timestamp.proto";

message Vec3 {
  double x = 1;
  double y = 2;
  double z = 3;
}

message ImuSample {
  google.protobuf.Timestamp stamp = 1;   // khi phép đo xảy ra
  string frame_id = 2;                   // khung tọa độ — Bài 3
  uint32 sequence = 3;                   // phát hiện mất mẫu

  Vec3 linear_acceleration = 4;          // m/s²
  Vec3 angular_velocity = 5;             // rad/s

  // Ba trường dưới đây là chỗ bạn khác một backend engineer thông thường
  repeated double acceleration_covariance = 6;  // uncertainty
  string calibration_id = 7;                    // calibration state
  string source_device_id = 8;                  // provenance
}
```

Ba trường cuối là **nguyên tắc số 5 của cả lộ trình**: uncertainty, provenance, calibration state là trường dữ liệu hạng nhất. Hầu hết người mới sẽ bỏ chúng. Đừng bỏ. Trong buổi phỏng vấn, chính ba trường này là thứ khiến người đối diện nhận ra bạn hiểu miền chứ không chỉ biết dùng thư viện.

```bash
protoc --python_out=. proto/sensors/v1/imu.proto
```

**Bước 3 — sinh dữ liệu giả có tính vật lý.** Đừng dùng `random()`. Sinh dữ liệu *trông giống thật*:

```python
import numpy as np

fps = 200
duration = 60
n = fps * duration
t = np.arange(n) / fps

g = 9.81
# IMU đứng yên: trục z đọc ~g, cộng nhiễu Gaussian ~0.02 m/s²
az = g + np.random.normal(0, 0.02, n)
ax = np.random.normal(0, 0.02, n)
ay = np.random.normal(0, 0.02, n)
# Gyro đứng yên: quanh 0, có bias nhỏ và drift chậm
gz = np.random.normal(0, 0.001, n) + 0.002 + 1e-5 * t
```

Vì sao quan trọng: ở Module 2 bạn sẽ viết detector tìm dữ liệu hỏng. Muốn biết detector đúng, bạn cần dữ liệu **lành** làm đối chứng. Dữ liệu random không có tính chất vật lý nào để so.

**Bước 4 — ghi MCAP.**

```python
from mcap_protobuf.writer import Writer
from sensors.v1 import imu_pb2

with open("imu.mcap", "wb") as f:
    writer = Writer(f)
    for i in range(n):
        t_ns = int(t[i] * 1e9)
        msg = imu_pb2.ImuSample(
            frame_id="imu_link",
            sequence=i,
            calibration_id="calib-2026-09-10-a",
            source_device_id="esp32-01",
        )
        msg.stamp.FromNanoseconds(t_ns)
        msg.linear_acceleration.x = ax[i]
        msg.linear_acceleration.y = ay[i]
        msg.linear_acceleration.z = az[i]
        msg.angular_velocity.z = gz[i]

        writer.write_message(
            topic="/imu",
            message=msg,
            log_time=t_ns + 1_500_000,   # ghi trễ 1.5ms so với lúc đo
            publish_time=t_ns,
        )
    writer.finish()
```

Chú ý dòng `log_time = publish_time + 1.5ms`. Đó là mô phỏng latency pipeline ở Bài 2. Ở Bài 13 bạn sẽ đo lại chính con số này từ file và xác nhận detector của mình đúng.

**Bước 5 — dự đoán rồi kiểm.** Trước khi chạy `mcap info`, viết:

```markdown
Dự đoán:
- số message = 200 × 60 = 12.000
- số channel = 1
- số schema = 1
- khoảng thời gian = 60.000s (log_time: 60.0015s)
- kích thước chưa nén ≈ 12.000 × ~90 B ≈ 1.1 MB
- sau nén zstd, dữ liệu float nhiễu nén kém, kỳ vọng tỉ lệ 1.5–2.5×
```

Rồi chạy `mcap info imu.mcap`.

**Bước 6 — round-trip test.** Đọc lại, so từng message với dữ liệu gốc.

```python
from mcap.reader import make_reader
from mcap_protobuf.decoder import DecoderFactory

with open("imu.mcap", "rb") as f:
    reader = make_reader(f, decoder_factories=[DecoderFactory()])
    out = list(reader.iter_decoded_messages(topics=["/imu"]))

assert len(out) == n
for i, (schema, channel, message, proto) in enumerate(out):
    assert proto.sequence == i
    assert abs(proto.linear_acceleration.z - az[i]) < 1e-12
```

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| `mcap info` số message | **chính xác 12.000** |
| `mcap info` số channel / schema | 1 / 1 |
| `mcap doctor` | **không lỗi** |
| Round-trip assert | **pass toàn bộ**, sai lệch float < 1e-12 |
| Tỉ lệ nén zstd | 1.5–2.5× (dữ liệu nhiễu nén kém — nếu ra 10× thì dữ liệu của bạn không đủ ngẫu nhiên) |

Dòng cuối là một bài học nhỏ nhưng thật: **tỉ lệ nén là một chỉ báo về nội dung.** Dữ liệu cảm biến thật có nhiễu nên nén kém. Nén quá tốt = có gì đó lặp lại = có thể là kênh bị đơ. Bạn sẽ dùng lại ý này ở Bài 11.

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Sửa |
|---|---|---|
| Số message ít hơn dự đoán | Quên gọi `writer.finish()` — chunk cuối chưa được đóng | Dùng context manager hoặc gọi finish |
| `mcap doctor` báo schema lỗi | Protobuf descriptor không được nhúng đủ | Kiểm tra import `google/protobuf/timestamp.proto` có được đóng gói không |
| Round-trip lệch float | Đang so sánh sau khi qua float32 ở đâu đó | Proto `double` là float64, kiểm lại kiểu numpy |
| Sai lệch float chính xác bằng 0 với mọi mẫu | Bạn đang so dữ liệu với chính nó, test vô nghĩa | Kiểm lại nguồn của mảng đối chứng |

---

## Bài 6 — Schema versioning và contract (3h)

**Câu hỏi:** thêm một trường vào schema, file cũ và reader cũ có còn dùng được không?

### Khái niệm

Phần này bạn đã biết về mặt nguyên lý. Điều mới là **ràng buộc của miền**: dữ liệu robot có vòng đời tính bằng năm. Một dataset thu năm 2026 phải đọc được năm 2031, bằng code đã đổi mười lần.

Luật Protobuf, tóm tắt:
- **Thêm trường mới, số hiệu mới** → an toàn cả hai chiều. Reader cũ bỏ qua trường lạ.
- **Xóa trường** → phải `reserved` số hiệu đó, vĩnh viễn. Không bao giờ tái sử dụng.
- **Đổi kiểu** → phá vỡ. Không làm.
- **Đổi tên trường** → an toàn về mặt binary (số hiệu mới là thứ quan trọng), nhưng phá vỡ JSON và mọi thứ dựa trên tên.
- **Đổi số hiệu trường** → phá vỡ.

Cái riêng của MCAP: schema nằm **trong file**. Nên một file MCAP luôn tự đọc được, kể cả khi code của bạn đã đổi. Điều bạn cần đảm bảo là: **code mới đọc được file cũ**, và **code cũ đọc được file mới** ở mức không crash.

### Làm

**Bước 1 — tạo v2.** Thêm trường vào `ImuSample`:

```protobuf
  // v2, thêm 2026-09
  double temperature_c = 9;        // nhiệt độ chip — cần cho bù drift
  uint32 calibration_version = 10;
```

**Bước 2 — sinh file v2.** Cùng code, thêm hai trường.

**Bước 3 — viết bốn test, đây là phần được chấm:**

```python
def test_new_reader_reads_old_file():
    # reader v2 đọc file v1 → 2 trường mới về giá trị mặc định
    ...

def test_old_reader_reads_new_file():
    # reader v1 đọc file v2 → không crash, bỏ qua trường lạ
    ...

def test_field_numbers_never_reused():
    # parse .proto, đảm bảo không có số hiệu nào bị xóa rồi dùng lại
    ...

def test_schema_embedded_matches_source():
    # schema nhúng trong file khớp với .proto trong repo
    ...
```

Test thứ ba và thứ tư ít người viết, và chúng là thứ đáng nói tới trong phỏng vấn. Test 3 bắt lỗi con người. Test 4 bắt trường hợp ai đó đổi `.proto` mà quên sinh lại và file cũ trở nên khó truy vết.

**Bước 4 — ghi vào `decisions.md`** chính sách version bằng lời: khi nào tăng major, ai được phép xóa trường, dataset cũ xử lý thế nào.

### Số phải ra

Cả bốn test pass. Cụ thể:
- Reader v2 đọc file v1: `temperature_c == 0.0`, `calibration_version == 0` (giá trị mặc định proto3), **không exception**
- Reader v1 đọc file v2: đọc đủ 12.000 message, các trường v1 giá trị đúng, **không exception**

### Nếu ra khác

| Triệu chứng | Nguyên nhân |
|---|---|
| Reader v1 crash khi đọc file v2 | Bạn đã đổi kiểu hoặc số hiệu trường, không phải chỉ thêm |
| Trường mới ra giá trị rác | Số hiệu trường trùng với trường đã bị xóa trước đó |
| Test 4 fail | `.proto` trong repo và schema trong file lệch nhau — có người sửa proto mà không sinh lại file |

---

## Bài 7 — Index, random access, và file bị cắt (3h)

**Câu hỏi:** trên file 50GB, làm sao lấy 10 giây ở giữa mà không đọc 50GB?

### Khái niệm

Đây là câu hỏi trong tiêu chí PASS của M2, và cách học nó là tự tay tạo ra tình huống.

**Random access hoạt động thế nào:**
1. Reader đọc **Footer** ở cuối file → biết offset của summary section
2. Đọc **ChunkIndex** → biết mỗi chunk chứa khoảng thời gian nào và nằm ở byte offset nào
3. Chọn chunk chứa khoảng thời gian cần → seek thẳng tới đó → giải nén một chunk
4. Dùng **MessageIndex** để nhảy tới đúng message trong chunk

Không có summary section, bước 1–2 bất khả thi → phải quét tuần tự từ đầu.

### Làm

**Bước 1 — sinh file lớn.** 30 phút dữ liệu ở 200Hz = 360.000 message, vài chục MB.

**Bước 2 — đo random access.**

```python
import time

# đọc toàn bộ
t0 = time.perf_counter()
n_all = sum(1 for _ in reader.iter_messages())
t_full = time.perf_counter() - t0

# đọc 10 giây ở giữa bằng start_time/end_time
t0 = time.perf_counter()
n_win = sum(1 for _ in reader.iter_messages(start_time=T0, end_time=T0 + 10_000_000_000))
t_window = time.perf_counter() - t0
```

**Bước 3 — cắt file, mô phỏng process bị kill.**

```bash
cp big.mcap truncated.mcap
# cắt bỏ 20% cuối
python -c "
import os
p='truncated.mcap'; s=os.path.getsize(p)
os.truncate(p, int(s*0.8))
"
mcap info truncated.mcap
mcap doctor truncated.mcap
mcap recover truncated.mcap -o recovered.mcap
mcap info recovered.mcap
```

**Bước 4 — dự đoán trước bước 3.** Viết ra: sau khi cắt 20%, `mcap info` sẽ nói gì? `mcap recover` sẽ cứu được bao nhiêu phần trăm message?

**Bước 5 — thiết kế lại theo số đo.** Thử ghi cùng dữ liệu với kích thước chunk khác nhau. Đo: thời gian random access, tỉ lệ nén, và số message mất khi cắt file. Vẽ ba đường.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Thời gian đọc cửa sổ 10s so với đọc toàn bộ | **Nhanh hơn ít nhất một bậc** trên file 30 phút. Nếu bằng nhau, index không được dùng. |
| `mcap info` trên file cắt | Báo thiếu summary / footer, hoặc lỗi |
| `mcap recover` | Cứu được **khoảng 80%** message — tức các chunk đã đóng hoàn chỉnh trước điểm cắt. Chunk đang dở thì mất. |
| Chunk nhỏ hơn | Random access nhanh hơn, nén kém hơn, mất ít message hơn khi cắt |

Đường cong ở bước 5 chính là một đường cong đánh đổi ba chiều, và nó có cùng hình dạng với đường latency-vs-underrun bạn sẽ vẽ ở Khóa 3. **Đây là cùng một loại bài toán, ở hai tầng khác nhau.** Nhận ra điều đó là mục tiêu thật của Module 1.

### Nếu ra khác

| Triệu chứng | Nguyên nhân |
|---|---|
| Đọc cửa sổ không nhanh hơn | Thư viện đang quét tuần tự — kiểm xem file có summary không, hoặc API có nhận start/end time không |
| `recover` cứu được 0% | Cắt quá sâu, mất cả chunk đầu tiên |
| `recover` cứu được 100% | Bạn cắt trúng ranh giới chunk. Thử tỉ lệ cắt khác. |

---

## Bài 8 — Foxglove và Rerun (2h)

**Câu hỏi:** nhìn dữ liệu này bằng mắt thì thấy gì?

### Khái niệm

| Công cụ | Bản chất | Dùng khi |
|---|---|---|
| **Foxglove** | App desktop + nền tảng cloud. Mở MCAP/ROS bag trực tiếp. Có panel 3D, image, plot, raw message, và phần fleet dashboard. | Dữ liệu MCAP/ROS-native, debug robot ngoài hiện trường, chia sẻ với team |
| **Rerun** | Thư viện + viewer, code-first. `rr.log(...)` từ Python. Nhẹ hơn nhiều. | Thí nghiệm nhanh, dữ liệu đa phương thức ad-hoc, vòng lặp phát triển |

JD Verne nhắc đích danh Foxglove. Học nó là bắt buộc. Rerun học để biết khi nào nên dùng cái nào — và câu trả lời đó là một câu hỏi phỏng vấn tốt.

### Làm

**Foxglove:**
1. Cài Foxglove desktop.
2. Mở `imu.mcap` từ Bài 5.
3. Thêm panel **Plot**, vẽ `linear_acceleration.z`. Phải thấy đường dao động quanh 9.81.
4. Thêm panel **Raw Messages**, xem một message đầy đủ — kiểm tra `calibration_id` và `frame_id` hiển thị đúng.
5. Thêm panel Plot thứ hai vẽ `angular_velocity.z`. Phải thấy đường trôi chậm lên — đó là drift bạn cố ý sinh ra ở Bài 5.
6. Lưu layout, export ra file JSON, commit vào repo. Layout là artifact — nó cho người khác mở dataset của bạn và thấy đúng thứ bạn muốn họ thấy.

**Rerun:**
```bash
pip install rerun-sdk
```
Log cùng dữ liệu bằng `rr.init()` + `rr.log()`, mở viewer, so sánh trải nghiệm.

**Ghi vào `notes/08-viz.md`:** ba câu, mỗi câu 2–3 dòng — Foxglove mạnh hơn ở đâu, Rerun mạnh hơn ở đâu, bạn chọn cái nào cho việc gì.

### Số phải ra

- Đường `linear_acceleration.z` dao động quanh **9.81**, biên độ nhiễu khoảng ±0.06 (3σ với σ=0.02)
- Đường `angular_velocity.z` bắt đầu ~0.002 và tăng tới ~0.0026 sau 60s — đúng drift `1e-5 × t` bạn đã sinh
- Raw message hiện đủ `frame_id="imu_link"`, `calibration_id`, `source_device_id`

Nếu Foxglove hiển thị đúng ba thứ này, schema và writer của bạn đúng, và bạn vừa nhìn thấy chính dữ liệu mình sinh ra qua con mắt của công cụ mà ngành đang dùng.

### Nếu ra khác

| Triệu chứng | Nguyên nhân |
|---|---|
| Foxglove không hiện gì | Schema không được nhúng đúng, hoặc `message_encoding` sai. Chạy `mcap list schemas`. |
| Plot phẳng ở 0 | Chọn nhầm đường dẫn trường trong panel |
| Timeline dài bất thường | `log_time` và `publish_time` chênh lớn — kiểm lại đơn vị, MCAP dùng **nanosecond** |

---

## GATE MODULE 1 (= M2 PASS)

| # | Tiêu chí | Cách kiểm |
|---|---|---|
| 1 | Repo public: đọc ≥2 nguồn dữ liệu → ghi MCAP hợp lệ với Protobuf schema có version | `mcap doctor` không lỗi |
| 2 | Test tự động chứng minh v1↔v2 backward + forward compatible | CI xanh, 4 test ở Bài 6 |
| 3 | File mở được trong Foxglove, có ảnh chụp trong README + layout JSON | Mở repo |
| 4 | README trả lời 3 câu: chunk index làm gì · vì sao quan trọng cho random access · điều gì xảy ra khi process bị kill giữa lúc ghi | Đọc README, kèm **số đo từ Bài 7** chứ không chỉ lời |

**Ngân sách:** 20h. **Trần:** 30h.

Tiêu chí 4 phải kèm số đo. Trả lời bằng lời thì ai cũng chép được từ docs. Trả lời kèm "tôi cắt file 20% và recover được 79.4% message" thì không.

---

# MODULE 2 — DATASET AUDIT TOOL (60h) ★

Tương ứng milestone **M3**. Đây là artifact công khai đầu tiên của bạn.

---

## Bài 9 — LeRobot dataset format từ zero (6h)

**Câu hỏi:** một dataset robot learning được tổ chức thế nào?

### Khái niệm

LeRobot là thư viện robot learning end-to-end của Hugging Face. Dataset của nó nằm trên HF Hub theo một format chuẩn, và **format đó là một bài toán data engineering** — đó là cửa vào ngành bằng đúng nghề của bạn.

**Đơn vị cơ bản là episode:** một lần thực hiện nhiệm vụ từ đầu tới cuối. "Nhặt khối gỗ, đặt vào hộp" — một episode. Thu 50 lần là 50 episode.

**Cấu trúc thư mục (LeRobotDataset v2.x):**

```
<dataset>/
├── meta/
│   ├── info.json          fps, robot_type, total_episodes, total_frames, features
│   ├── episodes.jsonl     mỗi dòng: episode_index, tasks, length
│   ├── tasks.jsonl        mô tả nhiệm vụ bằng ngôn ngữ tự nhiên
│   └── stats.json         min/max/mean/std từng feature
├── data/
│   └── chunk-000/
│       ├── episode_000000.parquet
│       └── episode_000001.parquet
└── videos/
    └── chunk-000/
        └── observation.images.top/
            ├── episode_000000.mp4
            └── episode_000001.mp4
```

**Một dòng trong parquet là một frame:**

| Cột | Nghĩa |
|---|---|
| `timestamp` | giây kể từ đầu episode |
| `frame_index` | chỉ số trong episode, bắt đầu từ 0 |
| `episode_index` | episode nào |
| `index` | chỉ số toàn cục trên cả dataset |
| `task_index` | trỏ vào `tasks.jsonl` |
| `observation.state` | vector trạng thái robot — thường là vị trí các khớp |
| `action` | vector lệnh gửi tới robot ở frame đó |

**Ảnh không nằm trong parquet.** Chúng được mã hóa thành mp4, một file mỗi camera mỗi episode. Lý do: 50 episode × 400 frame × 900KB = 18GB nếu lưu raw; nén video xuống còn vài trăm MB. Đánh đổi: mất khả năng random access rẻ, và **có thêm một cách để dữ liệu lệch nhau** — số frame trong mp4 có thể không khớp số dòng parquet.

Đó là defect class đầu tiên bạn sẽ tìm.

### Quyết định thiết kế quan trọng cho tool của bạn

**Đọc parquet + meta trực tiếp, không dùng lớp `LeRobotDataset`.**

Lý do giống hệt nguyên tắc "đọc raw register, không dùng thư viện wrapper" ở Khóa 1: wrapper che giấu đúng thứ bạn đang đi tìm. Nếu `LeRobotDataset` tự sửa lỗi timestamp khi load, bạn sẽ không bao giờ thấy lỗi đó. Và API của thư viện đổi theo phiên bản, còn format file thì ổn định hơn nhiều.

```bash
pip install huggingface_hub pyarrow pandas numpy av
```

```python
from huggingface_hub import snapshot_download
local = snapshot_download(repo_id="lerobot/<tên>", repo_type="dataset")
```

### Làm

1. Duyệt HF Hub, lọc dataset của org `lerobot`. Chọn 5 cái khác nhau — khác robot, khác fps, khác số camera, khác kích thước.
2. Tải về, mở `meta/info.json`, đọc kỹ. Ghi vào bảng: fps, robot_type, total_episodes, total_frames, danh sách features với dtype và shape.
3. Mở một file parquet bằng pandas. In ra 20 dòng đầu. Nhìn bằng mắt.
4. Đếm số frame trong mp4 tương ứng bằng `ffprobe`.

### Số phải ra

Với một dataset lành lặn:

| Kiểm tra | Kết quả đúng |
|---|---|
| Tổng số dòng parquet mọi episode | **bằng chính xác** `info.json → total_frames` |
| Số file parquet | bằng `total_episodes` |
| Số frame mp4 của episode k | **bằng chính xác** số dòng parquet của episode k |
| `timestamp` trong mỗi episode | tăng nghiêm ngặt, bắt đầu từ 0 |
| Trung vị của `diff(timestamp)` | bằng `1/fps` với sai lệch <1% |
| `frame_index` | 0, 1, 2, ... liên tục, không nhảy |

Viết dự đoán trước: bạn nghĩ bao nhiêu trong 5 dataset sẽ pass hết 6 dòng này?

Câu trả lời thực tế thường làm người ta ngạc nhiên, và đó chính là lý do tool này có giá trị.

### Nếu ra khác

| Triệu chứng | Ý nghĩa |
|---|---|
| Tổng dòng ≠ `total_frames` | Metadata không khớp dữ liệu. Lỗi thật, đáng báo cáo. |
| Số frame mp4 ≠ số dòng parquet | Video và state lệch nhau. **Lỗi nghiêm trọng** — mọi mô hình học từ đây đều học sai cặp ảnh-hành động. |
| `ffprobe` đếm chậm kinh khủng | Đang dùng `-count_frames` (giải mã toàn bộ). Thử `-count_packets` trước, chỉ dùng `-count_frames` khi cần chính xác tuyệt đối. |

---

## Bài 10 — Kiểm tra bằng tay trước khi tự động hóa (6h)

**Câu hỏi:** vì sao không viết code luôn?

### Khái niệm

Đây là bài dễ bị bỏ qua nhất và là bài quyết định chất lượng của tool.

Một detector chỉ tốt bằng hiểu biết của người viết về thứ nó phải bắt. Nếu bạn viết detector trước khi từng nhìn dữ liệu hỏng bằng mắt, bạn sẽ viết ra một tool bắt được đúng những lỗi bạn tưởng tượng — chứ không phải những lỗi thật sự tồn tại.

Tương đương ở Khóa 1: dự đoán trước khi đo. Ở đây: **nhìn trước khi tự động hóa.**

### Làm

Với **cả 5 dataset**, làm bằng tay, ghi vào `notes/10-manual-survey.md`:

1. **Vẽ `diff(timestamp)` cho 3 episode mỗi dataset.** Histogram + đường theo thời gian. Ghi lại hình dạng bằng lời.
2. **Vẽ `observation.state` từng chiều theo thời gian** cho 1 episode. Có chiều nào phẳng lì không? Có chiều nào nhảy bậc không?
3. **Vẽ `action` và `observation.state` cùng một khớp, chồng lên nhau.** Chúng lệch pha bao nhiêu frame? Nhìn bằng mắt trước, đo sau.
4. **Mở video, xem 3 episode.** Có episode nào tay robot không chạm vật? Có episode nào camera bị che? Có episode nào bị cắt giữa chừng?
5. **Vẽ phân bố độ dài episode** cho mỗi dataset.

Bước 4 quan trọng: có những lỗi chỉ con người thấy được. Một episode "thất bại" vẫn có timestamp hoàn hảo, schema hợp lệ, và hoàn toàn vô dụng cho training. Tool của bạn sẽ không bắt được nó — và biết giới hạn của tool cũng là một phần của việc làm tool.

### Số phải ra

Sau bài này bạn phải trả lời được, bằng số, cho từng dataset:
- Bao nhiêu phần trăm `dt` lệch khỏi `1/fps` quá 10%?
- Có chiều state nào đứng yên hoàn toàn trong ≥1 giây không?
- Độ lệch pha nhìn thấy giữa action và state là bao nhiêu frame?
- Độ dài episode: trung vị bao nhiêu, min/max bao nhiêu?

Và bạn phải có **ít nhất một điều bất ngờ** ghi lại. Nếu 5 dataset đều hoàn hảo, hoặc bạn chọn nhầm dataset quá sạch, hoặc bạn chưa nhìn đủ kỹ.

---

## Bài 11 — Bảy lớp lỗi: định nghĩa và toán (8h)

**Câu hỏi:** "dữ liệu hỏng" nghĩa là gì, chính xác?

Đây là phần lõi. Mỗi lớp lỗi có: định nghĩa, cách phát hiện, ngưỡng, và **vì sao nó làm hỏng việc training**.

---

### L1 — Timestamp không đơn điệu

**Định nghĩa:** trong một episode, tồn tại `i` sao cho `timestamp[i+1] <= timestamp[i]`.

**Phát hiện:** `np.diff(ts) <= 0`

**Ngưỡng:** không có ngưỡng. **Một lần cũng là lỗi.**

**Vì sao hại:** thời gian chạy lùi làm mọi phép nội suy và mọi cửa sổ trượt trở nên vô nghĩa. Nguyên nhân thường gặp: wall clock bị NTP kéo lùi giữa lúc thu.

---

### L2 — Rớt frame và jitter

**Định nghĩa:** `dt` lệch khỏi `1/fps`.

**Phát hiện:**
```python
dt = np.diff(ts)
expected = 1.0 / fps
ratio = dt / expected
drops = np.round(ratio) - 1        # 0 = bình thường, 1 = rớt 1 frame
jitter = np.std(dt[np.round(ratio) == 1])
```

**Ngưỡng:**
- Rớt frame: báo cáo tỉ lệ. **>1% là cảnh báo, >5% là nghiêm trọng.**
- Jitter: **>10% của `1/fps` là cảnh báo.**

**Vì sao hại:** policy học quan hệ thời gian. Rớt frame làm khoảng cách thời gian thật giữa hai frame liên tiếp khác với giả định của mô hình. Với action chunking, rớt frame làm lệch cả chunk.

---

### L3 — Số frame video ≠ số dòng parquet

**Định nghĩa:** với mỗi episode và mỗi camera, số frame trong mp4 phải bằng số dòng trong parquet.

**Phát hiện:**
```bash
ffprobe -v error -select_streams v:0 -count_packets \
  -show_entries stream=nb_read_packets -of csv=p=0 ep.mp4
```

**Ngưỡng:** lệch **≥1 frame là lỗi.**

**Vì sao hại:** lệch một frame nghĩa là mọi cặp (ảnh, hành động) đều sai một nhịp, trên toàn bộ episode. Mô hình học được một quan hệ nhân quả dịch pha. Đây là loại lỗi **im lặng nhất và tai hại nhất** — nó không làm gì crash, chỉ làm policy kém đi mà không ai biết vì sao.

---

### L4 — Kênh đơ (frozen channel)

**Định nghĩa:** một chiều của `observation.state` giữ nguyên giá trị chính xác trong một cửa sổ dài.

**Phát hiện:**
```python
win = int(fps)   # 1 giây
for j in range(state.shape[1]):
    d = np.abs(np.diff(state[:, j]))
    frozen = rolling_max(d, win) == 0.0
```

**Ngưỡng:** đứng yên **chính xác tuyệt đối** trong ≥1 giây trong lúc các khớp khác đang chuyển động.

**Vì sao hại:** cảm biến thật luôn có nhiễu ở bit thấp nhất. Giá trị bằng nhau *chính xác* qua 30 mẫu liên tiếp gần như chắc chắn là encoder chết, dây lỏng, hoặc giá trị bị giữ lại từ lần đọc cuối cùng thành công. Dữ liệu này hoàn toàn hợp lệ về schema, và hoàn toàn sai.

**Cảnh báo false positive:** robot đứng yên thật thì mọi khớp đều đứng yên. Nên điều kiện phải là: chiều này đơ **trong khi** chiều khác đang động.

---

### L5 — Lệch pha action/state

**Định nghĩa:** `action` tại frame `t` phải là nguyên nhân dẫn tới `state` ở `t+k` với `k` nhỏ và **nhất quán**.

**Phát hiện — bằng tương quan chéo:**
```python
def best_lag(action_j, state_j, max_lag=5):
    a = (action_j - action_j.mean()) / (action_j.std() + 1e-9)
    s = (state_j  - state_j.mean())  / (state_j.std()  + 1e-9)
    best, best_c = 0, -np.inf
    for lag in range(0, max_lag + 1):
        if lag == 0:
            c = np.corrcoef(a, s)[0, 1]
        else:
            c = np.corrcoef(a[:-lag], s[lag:])[0, 1]
        if c > best_c:
            best, best_c = lag, c
    return best, best_c
```

**Ngưỡng:**
- Lag tối ưu **>3 frame** → cảnh báo
- Lag **khác nhau giữa các episode trong cùng dataset** → cảnh báo mạnh, nghĩa là pipeline không xác định
- Tương quan đỉnh **<0.5** → action và state không liên quan như kỳ vọng, có thể ghép sai kênh

**Vì sao hại:** imitation learning học ánh xạ từ quan sát sang hành động. Lệch pha nghĩa là mô hình học "khi thấy X thì làm hành động vốn thuộc về thời điểm khác". Policy sẽ chạy nhưng kém, và không ai biết tại sao.

Đây là detector khó nhất và cũng là detector khiến tool của bạn khác với một script kiểm tra schema.

---

### L6 — Giá trị bất thường về vật lý

**Định nghĩa:** giá trị hợp lệ về kiểu dữ liệu nhưng không thể xảy ra về vật lý.

**Phát hiện:**
- `NaN` / `Inf` ở bất kỳ đâu
- Giá trị nằm ngoài `stats.json` min/max của chính dataset
- Vận tốc khớp ngầm định: `diff(position)/dt` vượt giới hạn cơ khí hợp lý
- Nhảy bậc: `|diff(state)| > k × median(|diff(state)|)` với k lớn (ví dụ 20)

**Ngưỡng:** NaN/Inf — không dung thứ. Nhảy bậc — báo cáo, để người đọc quyết.

**Vì sao hại:** một NaN đủ làm hỏng cả batch training. Một bước nhảy 180° trong góc khớp thường là lỗi wrap-around chứ không phải robot thật sự quay.

**Đây là "validation theo vật lý, không chỉ theo schema"** — nguyên tắc trung tâm của cả lộ trình, và nó xuất hiện lần đầu ở đây. Ở Khóa 5 bạn sẽ áp dụng nó lên dữ liệu thời gian thực.

---

### L7 — Metadata không khớp dữ liệu

**Định nghĩa:** những gì `meta/` tuyên bố khác với những gì `data/` chứa.

**Phát hiện:** `total_frames` vs tổng dòng thật · `total_episodes` vs số file · `fps` vs trung vị `1/dt` · `stats.json` min/max vs min/max thật · `episodes.jsonl` length vs số dòng thật.

**Ngưỡng:** lệch bất kỳ là lỗi.

**Vì sao hại:** metadata là contract. Code downstream tin nó. Sai metadata làm sai mọi thứ dựa trên nó, một cách âm thầm.

---

### Bảng tóm tắt

| ID | Lỗi | Cách phát hiện | Ngưỡng | Mức |
|---|---|---|---|---|
| L1 | Timestamp không đơn điệu | `diff(ts) <= 0` | 1 lần | Nghiêm trọng |
| L2 | Rớt frame / jitter | `dt` vs `1/fps` | >1% cảnh báo, >5% nặng | Trung bình |
| L3 | Video ≠ parquet | ffprobe vs row count | ≥1 frame | **Nghiêm trọng** |
| L4 | Kênh đơ | diff = 0 chính xác qua 1s | 1 cửa sổ | Nghiêm trọng |
| L5 | Lệch pha action/state | tương quan chéo | lag>3 hoặc không nhất quán | **Nghiêm trọng** |
| L6 | Bất thường vật lý | NaN, ngoài biên, nhảy bậc | NaN: 0 dung thứ | Tùy |
| L7 | Metadata lệch | so meta vs data | bất kỳ | Trung bình |

Bốn lớp là đủ để PASS M3. Làm được bảy thì tool của bạn tốt hơn mọi thứ hiện có công khai.

---

## Bài 12 — Viết detector và test tổng hợp (20h)

**Câu hỏi:** làm sao biết detector của mình đúng?

### Khái niệm

Đây là câu hỏi cốt lõi và nó có một câu trả lời sạch sẽ: **tự tạo dữ liệu hỏng có chủ đích, kiểm tra detector bắt được đúng cái đó và không báo nhầm thứ khác.**

Bạn đã có sẵn dữ liệu lành từ Bài 5. Bây giờ tiêm lỗi vào.

### Làm

**Bước 1 — bộ sinh dữ liệu hỏng.** Module `tests/synth.py`:

```python
def make_clean(n_episodes=3, length=300, fps=30, n_joints=6): ...

def inject_nonmonotonic(ds, episode, at_frame, jump_back_s): ...
def inject_frame_drops(ds, episode, n_drops, seed): ...
def inject_video_mismatch(ds, episode, delta_frames): ...
def inject_frozen_channel(ds, episode, joint, start, duration_s): ...
def inject_action_lag(ds, episode, lag_frames): ...
def inject_nan(ds, episode, frame, joint): ...
def corrupt_metadata(ds, field, delta): ...
```

**Bước 2 — mỗi detector có 3 test:**

```python
def test_L4_detects_frozen():
    ds = make_clean()
    inject_frozen_channel(ds, episode=1, joint=2, start=100, duration_s=1.5)
    r = audit(ds)
    assert r.has(L4, episode=1, joint=2)

def test_L4_no_false_positive_on_clean():
    assert not audit(make_clean()).has(L4)

def test_L4_no_false_positive_when_robot_still():
    # cả 6 khớp đứng yên cùng lúc — robot nghỉ thật, không phải cảm biến chết
    ds = make_clean()
    freeze_all_joints(ds, episode=0, start=50, duration_s=2.0)
    assert not audit(ds).has(L4)
```

Test thứ ba là loại test phân biệt tool nghiêm túc với script. Nó mã hóa hiểu biết về miền: *đơ thật* khác *đơ do hỏng*.

**Bước 3 — quét ngưỡng.** Với mỗi ngưỡng (ví dụ 1 giây cho L4, 3 frame cho L5), chạy detector ở nhiều giá trị ngưỡng trên bộ dữ liệu tổng hợp và vẽ đường false positive / false negative. Chọn ngưỡng theo đường cong, không theo cảm giác. **Ghi đường cong vào repo.**

Đây là điểm khác biệt lớn nhất giữa tool của bạn và những script tương tự trên GitHub: ngưỡng của bạn có căn cứ và căn cứ đó công khai.

**Bước 4 — CLI một lệnh.**

```bash
lerobot-audit lerobot/<dataset> --out report.html
lerobot-audit ./local/path --json --fail-on severe
```

`--fail-on severe` để dùng được trong CI của người khác. Đó là thứ khiến tool được dùng thật thay vì chỉ được star.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Mỗi detector có ≥3 test (bắt đúng, không báo nhầm trên sạch, không báo nhầm ở ca biên) | **Toàn bộ pass** |
| Trên dataset tổng hợp sạch | **0 phát hiện.** Một false positive ở đây là lỗi nghiêm trọng của tool. |
| Trên dataset tổng hợp có tiêm 1 lỗi | Bắt đúng lỗi đó, **và chỉ lỗi đó** |
| Chạy toàn bộ | Bằng **một lệnh**, không cần sửa code |
| Đường cong ngưỡng | Có mặt trong repo, cho ít nhất 2 detector |

### Nếu ra khác

| Triệu chứng | Nguyên nhân |
|---|---|
| False positive trên dữ liệu sạch | Ngưỡng quá chặt, hoặc dữ liệu tổng hợp chưa đủ nhiễu như thật |
| L5 báo lag khác nhau mỗi lần chạy | Tương quan trên chuỗi quá ngắn không ổn định. Cần độ dài tối thiểu, hoặc gộp nhiều khớp. |
| Detector đúng trên tổng hợp, sai trên thật | Dữ liệu tổng hợp quá lý tưởng. Quay lại Bài 10, thêm đặc tính đã thấy trong dữ liệu thật vào bộ sinh. |

---

## Bài 13 — Chạy trên dataset thật (8h)

### Làm

1. Chạy tool trên **cả 5 dataset** đã chọn ở Bài 9.
2. **Trước khi xem kết quả**, viết dự đoán vào `predictions/13-real-datasets.md`: dataset nào bạn nghĩ sẽ có lỗi gì, dựa trên khảo sát bằng tay ở Bài 10.
3. Chạy. So dự đoán với kết quả.
4. Với mỗi phát hiện, **xác minh bằng tay**. Mở đúng episode đó, vẽ đúng đoạn đó, xem đúng video đó. Detector nói có lỗi không đủ — bạn phải nhìn thấy nó.
5. Viết script reproduce tối giản cho ít nhất một lỗi: một file Python <40 dòng, tải dataset, in ra bằng chứng.

### Số phải ra

- Chạy hết 5 dataset không crash
- **≥1 lỗi thật được xác nhận bằng tay**
- Script reproduce chạy được trên máy sạch, chỉ cần `pip install` và tên dataset
- Tỉ lệ dự đoán đúng ghi lại — đây là chỉ số về mức độ bạn đã hiểu miền

### Nếu ra khác

| Triệu chứng | Xử lý |
|---|---|
| Không tìm thấy lỗi nào trong 5 dataset | Mở rộng lên 10 dataset, ưu tiên dataset do cộng đồng đóng góp thay vì dataset chính thức đã được làm sạch |
| Tìm thấy quá nhiều lỗi ở mọi nơi | Nghi ngờ detector trước, nghi ngờ dữ liệu sau. Xác minh bằng tay 3 trường hợp trước khi tin. |
| Tool crash trên dataset thật | Format có biến thể bạn chưa gặp. Xử lý gracefully và ghi lại biến thể đó — bản thân nó là phát hiện đáng báo cáo. |

---

## Bài 14 — Report, publish, và báo cáo ra ngoài (8h)

**Câu hỏi:** làm sao thứ này tới được mắt người cần thấy?

### Khái niệm

Tiêu chí PASS cuối cùng của M3 không do bạn chấm: **≥1 phản hồi có nội dung từ người ngoài, hoặc ≥10 star, trong 60 ngày.**

Lý do đặt tiêu chí như vậy: bạn đang xây một hồ sơ để người khác đánh giá. Một tool tốt mà không ai biết thì không phân biệt được với một tool không tồn tại. Và cách duy nhất để biết công việc của bạn có giá trị với người trong ngành là **hỏi người trong ngành**.

### Làm

**Bước 1 — report HTML.** Không phải bãi log. Cấu trúc:
- Tóm tắt: bao nhiêu episode, bao nhiêu phát hiện, chia theo mức
- Mỗi phát hiện: episode nào, frame nào, bằng chứng, biểu đồ, mức nghiêm trọng
- Phần "đã kiểm và sạch" — cũng quan trọng như phần lỗi, vì nó cho biết phạm vi kiểm

**Bước 2 — README.** Ba câu đầu phải trả lời: tool này làm gì, chạy thế nào, tại sao nên quan tâm. Kèm ảnh chụp report. Kèm đường cong ngưỡng.

**Bước 3 — báo cáo lỗi ra ngoài.** Chọn kênh phù hợp:
- Tab **Discussions** của chính dataset trên HF Hub — đúng chỗ nhất
- **Issue** trên `huggingface/lerobot` nếu là vấn đề format hoặc công cụ
- **LeRobot Discord** — kênh phù hợp, kèm link repo

Viết ngắn, khách quan, có script reproduce. Không "dataset của bạn hỏng" mà "tôi thấy hiện tượng X ở episode Y, đây là script reproduce, có thể tôi hiểu sai format — nhờ xác nhận giúp".

Câu cuối quan trọng: bạn đang mở một cuộc trò chuyện, không đang tuyên bố. Và bạn thật sự có thể hiểu sai — bạn mới vào miền này ba tháng.

**Bước 4 — phân phối.** Bài viết ở Bài 15, rồi cross-post: r/robotics, Hacker News, LinkedIn, LeRobot Discord.

### Số phải ra

| Kiểm tra | Đúng |
|---|---|
| Report mở được trong trình duyệt, tự chứa | Có |
| README có ảnh + lệnh chạy + đường cong ngưỡng | Có |
| Đã đăng báo cáo lỗi ở ≥1 kênh | Có link |
| Trong 60 ngày: ≥1 phản hồi có nội dung HOẶC ≥10 star | **Đây là gate** |

### Nếu ra khác

| Triệu chứng | Xử lý |
|---|---|
| Đăng rồi im lặng 3 tuần | Vấn đề ở kênh phân phối, không ở công việc. Viết bài (Bài 15) và cross-post. Cấp thêm 8h. |
| Vẫn im lặng sau 90 ngày | Đây là tín hiệu thị trường đầu tiên và nó xấu. Chạy **M5** (đo thị trường) ngay, sớm hơn kế hoạch, để lấy thêm dữ liệu trước khi đầu tư 90h nữa vào Khóa 3. |
| Có phản hồi nhưng chỉ ra tool sai | **Đây là kết quả tốt nhất có thể.** Sửa, cảm ơn công khai, ghi lại vào README phần "đã sửa nhờ phản hồi từ ai". Nó chứng minh bạn tham gia được vào một cuộc trao đổi kỹ thuật thật. |

---

## Bài 15 — Bài viết tiếng Anh (4h)

**Tiêu đề:** *Auditing LeRobot datasets: what breaks and how to detect it*

**Bố cục — 1200–1800 từ, không hơn:**

1. **Mở đầu, 3 câu.** Robot dataset là dữ liệu đa luồng đa tần số; hầu hết công cụ kiểm tra schema chứ không kiểm tra vật lý; đây là những gì tôi tìm thấy.
2. **Bảy lớp lỗi**, mỗi cái 100 từ + một biểu đồ. Nêu rõ *vì sao* nó làm hỏng training, không chỉ *nó là gì*.
3. **Chọn ngưỡng thế nào.** Đường cong FP/FN. Đây là phần khiến bài viết khác các bài "tôi viết một tool".
4. **Kết quả trên N dataset công khai.** Số liệu, khách quan, không quy kết. Dataset công khai là đóng góp miễn phí của người khác cho cộng đồng.
5. **Giới hạn.** Tool không bắt được gì (episode thất bại về mặt ngữ nghĩa, camera bị che, nhiệm vụ mơ hồ). Nêu thẳng.
6. **Chạy thử.** Một lệnh.

Phần 5 quan trọng hơn nó trông. Nêu giới hạn của công cụ mình làm là dấu hiệu của người đã đo đủ nhiều để biết mình chưa đo được gì.

---

## GATE MODULE 2 (= M3 PASS)

| # | Tiêu chí | Cách kiểm |
|---|---|---|
| 1 | Chạy trên ≥5 dataset công khai bằng **một lệnh** | Chạy thử từ repo sạch |
| 2 | ≥4 lớp lỗi, mỗi lớp có test tổng hợp chứng minh detector đúng **và** không báo nhầm | CI xanh |
| 3 | Tìm ≥1 lỗi **thật** trong ≥1 dataset công khai, có script reproduce | Chạy script |
| 4 | Đã báo cáo ra ngoài | Link công khai |
| 5 | **Tín hiệu ngoài trong 60 ngày:** ≥1 phản hồi có nội dung, HOẶC ≥10 star | Không do bạn chấm |

**Ngân sách:** 60h. **Trần:** 85h.

---

# LỊCH 8 TUẦN

Ở nhịp 10h/tuần. Chạy song song Khóa 1 — khóa này làm được ở bất cứ đâu có laptop.

| Tuần | Giờ | Làm |
|---|---|---|
| 1 | 6h | Bài 1–3 (từ vựng miền, đọc) |
| 2 | 9h | Bài 4–5 (MCAP, viết file đầu tiên) |
| 3 | 8h | Bài 6–8 (versioning, index, Foxglove) → **Gate M2** |
| 4 | 12h | Bài 9–10 (LeRobot format, khảo sát bằng tay) |
| 5 | 8h | Bài 11 (định nghĩa 7 lớp lỗi + toán) |
| 6–7 | 20h | Bài 12 (detector + test tổng hợp + đường cong ngưỡng) |
| 8 | 12h | Bài 13–15 (chạy thật, publish, bài viết) → **Gate M3** |

**+60 ngày chờ tín hiệu ngoài.** Trong lúc chờ, bắt đầu Khóa 3 hoặc Khóa 4 — đừng ngồi đợi.

---

# NGUỒN HỌC KÈM THEO

| Nguồn | Phần nào | Bài |
|---|---|---|
| `mcap.dev` | Specification, Guides | 4–7 |
| `foxglove/mcap` GitHub | `python/` examples, CLI source | 5, 7 |
| `foxglove.dev/docs` | Panels, layouts, MCAP support | 8 |
| **Foxglove blog** | Loạt bài về time và về best practices ghi dữ liệu robot | 2, 4 |
| `rerun.io/docs` | Getting started | 8 |
| `huggingface.co/docs/lerobot` | Dataset format | 9 |
| `huggingface/lerobot` GitHub | thư mục dataset, đọc kiến trúc | 9, 11 |
| Protobuf language guide | Updating a message type | 6 |

---

# SAU KHÓA 2

Bạn có: hai repo public, một artifact ★, một bài viết tiếng Anh, một liên hệ thật trong cộng đồng LeRobot, và — nếu Gate M3 pass — bằng chứng đầu tiên rằng người trong ngành thấy việc bạn làm có giá trị.

**Tiếp theo, hai hướng:**

**Khóa 3 — Chuỗi audio (90h, cần đợt 2 ~4tr).** Đi hết chuỗi từ số nguyên tới áp suất không khí. Đây là thứ chứng minh bạn đã chạm phần cứng thật, và nó là câu trả lời cho câu hỏi phỏng vấn "anh có từng làm việc với dữ liệu cảm biến thật chưa". Mở khi Khóa 1 PASS.

**Khóa 4 — VLA edge benchmark (70h, thuê GPU).** Artifact ★ thứ hai, cũng không cần phần cứng riêng. Nếu quỹ giờ đang eo hẹp hoặc Khóa 1 đang bị chặn, **làm Khóa 4 trước Khóa 3.** Nó rẻ hơn, nhanh hơn, và đúng nghề bạn hơn.

**Và ngay sau Gate M3: chạy M5 — đo thị trường.** Bạn đã có cái để chỉ vào. 15h, 10 application + 5 outreach, và bảng diễn giải kết quả đã cam kết sẵn trong lộ trình. Đừng chờ tới tháng 12.
