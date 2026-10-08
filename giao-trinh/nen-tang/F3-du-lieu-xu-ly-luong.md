# F3 — Hệ thống dữ liệu và xử lý luồng (39h)

> Khóa nền, học **đúng lúc**: không đọc một mạch, mở viên nang ngay trước bài chính cần nó (bảng dưới). Tổng 39h = F3.1 4h · F3.2 4h · F3.3 5h · F3.4 5h · F3.5 4h · F3.6 4h · F3.7 5h · F3.8 4h · F3.9 4h. Giờ này chỉ một phần nằm trong ngân sách các bài chính; phần còn lại cộng thêm vào tổng lộ trình (đã vượt 650h, xem `00-lo-trinh-tong.md` và `khoa-7/_KE-HOACH-K7.md` mục 3).
>
> **Cách đọc khóa này cho người đã quen Kafka:** mỗi viên nang có mục 3 *Cầu nối* nói gọn phần bạn đã biết (đọc lướt) và dồn sức vào cột **Gãy ở chỗ**. Phần đáng làm nhất là mục 5 (bài tập Python, ≤2h) và mục 6 (Lăng kính đánh giá).

## Vì sao khóa nền này tồn tại

Bạn đã vận hành log, hàng đợi, schema registry, retry idempotent. Với dữ liệu robot, những thứ đó vẫn đúng **hình dạng** nhưng sai ở bốn giả định mà backend ngầm dựa vào:

1. **Thời gian của sự kiện do một đồng hồ vật lý trôi đóng dấu**, không phải do broker cấp. Không có `LogAppendTime` nào làm trọng tài.
2. **Dữ liệu là tín hiệu liên tục được lấy mẫu**, không phải sự kiện rời rạc. Ghép hai luồng là bài toán xử lý tín hiệu (as-of, nội suy, aliasing), không phải join theo khóa.
3. **Dữ liệu sai vẫn đúng schema.** Đơn vị, hướng trục, cảm biến đơ, đồng hồ lùi: không parser nào kêu.
4. **Mất một message là mất vĩnh viễn một phép đo.** Không có retry từ upstream; thứ duy nhất cứu dataset là việc đã mất được **đếm**.

Thiếu F3, bạn sẽ hụt ở đúng những chỗ này:

- **K2 Bài 4, 7** — đọc MCAP như "Kafka segment trong một file" rồi ngạc nhiên khi file bị `kill -9` không có index nào.
- **K2 Bài 6, 8b** — thêm trường proto3 "an toàn hai chiều" và nhận `0.0 °C` cho toàn bộ dữ liệu cũ.
- **K5 Bài 13** — ghép camera 30 Hz với IMU 200 Hz theo `log_time` và nhúng jitter USB vào dữ liệu fusion; hoặc resample về 30 Hz và biến rung motor 40 Hz thành dao động 10 Hz không có thật.
- **K5 Bài 14** — xóa file local sau `200 OK` của một file đang ghi dở.
- **K5 Bài 16** — tin rằng "schema bắt được sai đơn vị" (bản gốc viết đúng câu này).
- **K5 Bài 17, K3 Bài 16** — chọn "block producer" vì nghe an toàn, thực ra dời chỗ mất dữ liệu sang driver USB, nơi không ai đếm.
- **K6 Bài 7, 9** — cache kết quả theo `mtime` và đem báo cáo một con số không ai tái tạo được.
- **K7 C7.3, C7.4** — sidecar MCAP, upload, audit và data contract cho robot của chính bạn: đây là nơi cả chín viên nang gặp nhau.

## Mindset cốt lõi

1. **Log bất biến là nguồn sự thật; mọi bảng, index, dataset là view dẫn xuất tái tạo được.** Người làm hạ tầng dữ liệu tin điều này vì họ đã sống qua cảnh N hệ thống nối với nhau bằng N² pipeline mỗi cái tự chép dữ liệu theo cách riêng (Jay Kreps mô tả đúng cảnh này ở LinkedIn, *The Log*, 2013 `[chuẩn]`). Ở robot, log là file MCAP; dataset LeRobot, bảng index DuckDB, bộ split train/test là view.
2. **Thời điểm đo là một ước lượng có sai số, ghi kèm nguồn gốc của nó.** Người làm xử lý luồng tin "event time ≠ processing time" vì Google từng phải viết lại pipeline batch thành streaming và phát hiện kết quả đổi theo lúc dữ liệu tới (Akidau và cộng sự, *The Dataflow Model*, VLDB 2015 `[chuẩn]`). Người làm robot tin thêm một bước: event time do một thạch anh trôi vài chục ppm đóng dấu, nên nó cần `clock_source` và mô hình quy đổi đi kèm.
3. **Schema bảo vệ bytes, không bảo vệ nghĩa.** Mars Climate Orbiter (1999) mất vì một bên xuất lbf·s, bên kia đọc như N·s: dữ liệu đúng định dạng file giao tiếp, sai đơn vị `[chuẩn]`.
4. **Drop được phép; drop im lặng thì không.** Mạng Internet sống sót qua congestion collapse năm 1986 vì Van Jacobson biến *gói bị drop* thành tín hiệu đo được (1988) `[chuẩn]`. Một dataset biết mình thủng ở đâu thì dùng được; một dataset thủng mà không biết thì độc hại.
5. **Mọi kết quả phải truy ngược được tới bytes đầu vào, code và tham số.** Bảng tính của Reinhart–Rogoff (2010) bỏ sót dòng trong một công thức trung bình; chỉ phát hiện khi một nghiên cứu sinh xin được file gốc (Herndon, Ash, Pollin, 2013) `[chuẩn]`.

## Bản đồ viên nang

```mermaid
flowchart LR
  F31["F3.1 Log là trung tâm<br/>append-only, chunk, index"] --> F32["F3.2 Encoding & schema<br/>Protobuf/CDR, tương thích"]
  F31 --> F35["F3.5 Idempotency<br/>upload, object store"]
  F32 --> F37["F3.7 Data contract<br/>schema vs vật lý"]
  F33["F3.3 Event time<br/>window, watermark"] --> F34["F3.4 Ghép luồng<br/>as-of, nội suy, sai số"]
  F31 --> F33
  F31 --> F39["F3.9 Backpressure<br/>drop có đếm"]
  F33 --> F39
  F35 --> F36["F3.6 Lưu trữ phân tích<br/>Parquet, DuckDB"]
  F36 --> F38["F3.8 Lineage<br/>hash nội dung, DAG"]
  F37 --> F38
  F34 --> F37
```

### Học đúng lúc

| Viên nang | Học trước bài chính | Giờ |
|---|---|---|
| F3.1 Log là trung tâm | K2 Bài 1 (lướt), **K2 Bài 4**, K2 Bài 7 · K5 Bài 13 · K6 Bài 9 · K7 C7.3 | 4 |
| F3.2 Encoding và schema evolution | K1 Bài 10 (lướt) · K2 Bài 6, **Bài 8b**, Bài 9 · K4 Bài 10 · K5 Bài 4, Bài 13 · K6 Bài 5, Bài 9 · K7 C7.4 | 4 |
| F3.3 Event time vs processing time | **K2 Bài 2** · K5 Bài 7, **Bài 13** · K7 C7.2 | 5 |
| F3.4 Ghép luồng khác tần số | K2 Bài 1 (lướt), Bài 11 · **K5 Bài 13** · K7 C7 (trọn chặng), C8.3 | 5 |
| F3.5 Idempotency, upload, object store | K3 Bài 14 · **K5 Bài 14** · K6 Bài 9 · K7 C7.3 | 4 |
| F3.6 Lưu trữ phân tích | K2 Bài 9 · **K5 Bài 15** · K6 Bài 9 | 4 |
| F3.7 Chất lượng dữ liệu, data contract | K1 Bài 11 (lướt), Bài 12 · K2 Bài 6, Bài 10, **Bài 11** · K4 Bài 15 · **K5 Bài 16** · K6 Bài 5, Bài 17 · K7 C7.4 | 5 |
| F3.8 Lineage và provenance | K2 Bài 9 · K3 Bài 6 · K4 Bài 8, **Bài 14** · K5 Bài 15 · K6 Bài 6, **Bài 7**, Bài 9, Bài 10 · K7 C11.5 | 4 |
| F3.9 Backpressure và drop policy | K1 Bài 3, Bài 7 (lướt) · K3 Bài 4, Bài 10, Bài 16 · K4 Bài 3 · **K5 Bài 17** · K6 Bài 8 · K7 C7.3 | 4 |

Tuần crunch: đọc mục 3 + 6 của F3.1 trước K2 Bài 4; F3.3 + F3.4 mục 2, 5, 6 trước K5 Bài 13; F3.7 mục 6 trước K5 Bài 16; F3.9 mục 5 trước K5 Bài 17. Nếu chỉ còn sức cho một viên nang, chọn **F3.4**: nó là chỗ vốn backend của bạn ít giúp nhất.

## Bạn đã làm cái này rồi

| Bạn đã làm trong backend/AI-harness | Tên chuẩn | Còn thiếu khi sang dữ liệu robot | Viên nang |
|---|---|---|---|
| Kafka topic, consumer offset, replay từ đầu | Log-centric architecture; event sourcing | Không có broker cấp offset; địa chỉ là (chunk, `log_time`); index chỉ có khi file đóng đúng cách | F3.1 |
| Schema registry, Avro/Protobuf, rule BACKWARD/FORWARD | Schema evolution | Không có registry ở thời điểm ghi; kiểm dời sang CI và ingest; tương thích ngữ nghĩa (đơn vị, giá trị 0 của enum) | F3.2 |
| Flink/Kafka Streams window, `CreateTime` | Event time, watermark | Đồng hồ nguồn trôi; lateness tăng theo thời gian phiên; event time là *giữa phơi sáng*, không phải lúc gửi | F3.3 |
| Stream–stream join, lookup join | As-of join, interval join | Nội suy, aliasing khi resample, ngân sách sai số căn chỉnh; không có khóa nghiệp vụ | F3.4 |
| Idempotency key, retry với backoff, outbox | Effectively-once, content addressing | Đơn vị dữ liệu là file nhiều GB đang được ghi; điều kiện xóa local; checksum do server tính | F3.5 |
| Data warehouse, partition theo ngày, ClickHouse | Columnar storage, zone map, lakehouse | Raw không vào DB; index là tóm tắt có chủ đích (max, count, không phải mean) | F3.6 |
| Validate request bằng JSON Schema, Great Expectations | Data contract, data quality | Rule theo vật lý cần *giả định trạng thái* (đứng yên) và có tỉ lệ báo động giả phải đo (→ F2.1) | F3.7 |
| Docker image digest, lockfile, cache build | Provenance, content-addressed cache | Dataset và calibration cũng là đầu vào cần hash; mtime không phải danh tính | F3.8 |
| Rate limit, 429, DLQ | Backpressure, load shedding | Upstream là cảm biến không biết chờ; block = drop ở chỗ không đếm | F3.9 |

---

## F3.1 — Log là trung tâm: append-only, offset, segment, index (Kafka ↔ MCAP) (4h)

> **Dùng cho:** K2 Bài 1, 4, 7 · K5 Bài 13 · K6 Bài 9 · K7 C7.3 · **Cần trước:** không (vốn Kafka) · **Sau viên nang này bạn đánh giá được:** một khẳng định kiểu "file log này chịu được crash / đọc ngẫu nhiên được / đọc một topic nhỏ thì nhanh" là ĐÚNG, SAI hay còn tùy cấu hình nào; và chọn kích thước chunk bằng số thay vì mặc định.

### 1. Câu chuyện

Năm 2013, Jay Kreps (đồng tác giả Kafka) viết *The Log: What every software engineer should know about real-time data's unifying abstraction*. Luận điểm: write-ahead log của database, commit log của hệ phân tán, và hàng đợi tích hợp dữ liệu giữa các team là **cùng một thứ** — một chuỗi bản ghi chỉ nối thêm, có thứ tự, đánh địa chỉ bằng vị trí. Có nó, mỗi hệ thống tiêu thụ chỉ cần nhớ "tôi đã đọc tới đâu"; thiếu nó, mỗi cặp hệ thống phải tự viết pipeline chép dữ liệu `[chuẩn]`.

Ngành robot đi con đường riêng tới cùng kết luận. rosbag (ROS 1) là một log nối thêm có index ở cuối file. rosbag2 thời đầu dùng **SQLite** làm định dạng lưu: tiện truy vấn, nhưng ghi tốc độ cao và chịu crash kém hơn một log thuần, và file không tự mang định nghĩa message. Foxglove thiết kế **MCAP** (2022) quay lại dạng log: chunk nén, index thưa, schema nhúng; từ ROS 2 Iron (2023), MCAP là storage mặc định của rosbag2 `[spec: ROS 2 Iron release notes — kiểm theo bản bạn dùng]`. Bài học của vòng đi vòng lại này: thứ tối ưu cho *ghi trên robot* (append, chịu crash, không cần server) khác thứ tối ưu cho *truy vấn trên desktop* (index, random access). Một định dạng tốt tách hai việc đó ra, và trả giá ở chỗ nối giữa chúng.

### 2. Mô hình tư duy

```
 Kafka partition (nhiều file, có broker)          MCAP (một file, không có broker)
 ┌──────────────┐ ┌──────────────┐               ┌────┬────────┬────────┬─────┬─────────┬──────┬────┐
 │ 000.log      │ │ 512.log      │  ...          │Hdr │Chunk 1 │Chunk 2 │ ... │ Summary │Footer│Mgc │
 │ 000.index ◄──┼─┤ 512.index    │               │    │(zstd)  │(zstd)  │     │ChunkIdx │      │    │
 │ 000.timeindex│ │ 512.timeindex│               │    │+MsgIdx │+MsgIdx │     │Stats    │      │    │
 └──────────────┘ └──────────────┘               └────┴────────┴────────┴─────┴─────────┴──────┴────┘
  index cập nhật liên tục trong lúc ghi;           index chi tiết của chunk ghi ngay sau chunk;
  crash → broker quét segment cuối, dựng lại       index tổng (Summary) chỉ ghi khi finish();
  địa chỉ = offset toàn cục do broker cấp          địa chỉ = (byte offset chunk, log_time)
```

Bốn khái niệm, mỗi cái là một nút vặn:

| Khái niệm | Nó mua gì | Nó trả bằng gì |
|---|---|---|
| **Append-only** | Ghi tuần tự (nhanh nhất trên mọi loại đĩa), không có cập nhật tại chỗ nên crash chỉ hỏng *đuôi* | Không sửa được bản ghi cũ; sửa = ghi bản mới + view dẫn xuất |
| **Segment / chunk** | Đơn vị nén, đơn vị xóa (retention), đơn vị kiểm CRC | Dữ liệu trong chunk đang mở nằm trong RAM: **bán kính vụ nổ** khi process chết |
| **Offset / địa chỉ** | Consumer nhớ được vị trí, replay được | MCAP không có offset toàn cục; `sequence` do nguồn cấp, có thể bằng 0 `[spec: MCAP, Message record: "Optional message counter"]` |
| **Index thưa** | Tìm theo thời gian không cần quét | Index ở *cuối* file chỉ tồn tại nếu file đóng đúng cách |

Câu then chốt: **trong một log, crash-safety và random access kéo về hai phía.** Kafka giải bằng file index riêng cập nhật liên tục và một broker luôn sống để dựng lại. MCAP không có broker, nên chọn: data section tự đủ để *quét* lại (mỗi chunk có độ dài, CRC), còn index nhanh là phần thưởng cho file đóng đúng. Công cụ `mcap recover` tồn tại vì đúng lựa chọn này.

### 3. Cầu nối từ backend

Đã có ở K2 Bài 4 bảng đối chiếu Kafka segment ↔ MCAP và lời chấm mô hình *"MCAP chỉ là Kafka trong một file"* (**ĐÚNG MỘT PHẦN**, bốn chỗ gãy: không offset toàn cục, index chỉ có khi `finish()`, channel xen kẽ trong chunk, không broker/retention). Không lặp lại; đọc ở đó. Dưới đây là các phép so sánh *khác*.

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Database WAL: ghi log trước, áp vào bảng sau, checkpoint | MCAP là log; dataset/index là "bảng" | WAL bị cắt bỏ sau checkpoint; log robot **không bao giờ** cắt bỏ — nó là nguồn sự thật duy nhất của một phép đo không lặp lại được | Coi MCAP là file tạm, xóa sau khi "đã import vào DB", rồi không tái tạo được khi sửa bug extractor (→ F3.8) |
| Kafka `acks=all` + replication: một broker chết không mất gì | Writer MCAP trên một máy, không replica | Độ bền của Kafka đến từ *bản sao trên máy khác*, không từ fsync. Robot không có máy khác cho tới khi upload (→ F3.5) | Suy "kill -9 không mất gì nhiều" thành "mất điện không mất gì": page cache chưa xuống đĩa là phần mất thêm |
| Consumer group đọc song song nhiều partition | Đọc song song nhiều file MCAP, hoặc nhiều chunk trong một file | Song song theo chunk chỉ được khi có ChunkIndex (file đóng đúng); thứ tự toàn cục giữa các chunk theo `log_time` phải tự merge | Ghép kết quả các worker theo thứ tự xong việc, không theo thời gian |

**Chấm mô hình:**

- *"Append-only nghĩa là crash không bao giờ làm hỏng file."* — **ĐÚNG MỘT PHẦN.** Append-only giới hạn chỗ hỏng ở **đuôi**: không bản ghi cũ nào bị ghi đè dở. Gãy: (a) đuôi đó có thể là cả chunk đang mở, tức vài giây dữ liệu; (b) reader dùng index sẽ coi cả file là hỏng vì footer/summary không có; (c) một bản ghi bị cắt giữa chừng mà không có độ dài + CRC thì reader không biết dừng ở đâu. Phản ví dụ: bài tập mục 5 — file bị kill có 100% chunk đã flush còn nguyên, nhưng reader theo index đọc được 0 message.
- *Mô hình của bạn ở K3 lượt 6: "luôn phải có buffer để ổn định… đánh đổi bằng RAM".* — Đã chấm **ĐÚNG MỘT PHẦN** ở K5 Bài 13. Thêm một góc ở đây: chunk của log chính là buffer đó, và nó có *ba* giá, không phải một: RAM, độ trễ trước khi dữ liệu xuống đĩa, và lượng dữ liệu mất khi chết. Kích thước chunk chọn bằng cả ba.

**Tên chuẩn của thứ bạn đã làm:** khi bạn replay một topic Kafka từ offset 0 để dựng lại một service sau khi sửa bug, đó là **event sourcing / kappa architecture**: trạng thái là hàm của log. Với robot, "sửa bug extractor rồi chạy lại trên toàn bộ MCAP" là cùng mẫu. Còn thiếu: log của bạn ở backend được giữ bởi retention có chủ đích; log robot phải được giữ *vĩnh viễn* và có hash (→ F3.8), vì không có upstream nào phát lại.

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | Append-only log | Chuỗi bản ghi chỉ nối thêm, có thứ tự | "Không bao giờ hỏng" |
| 🟢 | Chunk / segment | Khối bản ghi nén và kiểm cùng nhau | Đơn vị chỉ để nén |
| 🟢 | Summary / footer / index | Phần cuối file trỏ vào chunk theo thời gian, channel | Luôn có |
| 🟢 | `log_time` vs `publish_time` vs `header.stamp` | Lúc ghi / lúc publish / lúc đo | Ba tên của một thứ (→ F3.3) |
| 🟢 | Recover / reindex | Quét data section, dựng lại summary | Phép màu cứu mọi file |
| 🟡 | Message index vs chunk index | Index trong chunk vs index các chunk | — |
| 🟡 | Kappa / lambda architecture | Một log cho cả batch và stream / hai đường riêng | — |
| 🔴 | Định dạng nhị phân chi tiết từng opcode MCAP | Tra spec khi cần | — |

### 5. Bài tập dự đoán

Một log đồ chơi giống tinh thần MCAP: message IMU thô (header 14 byte + 6 × int16), gom thành chunk nén zlib có độ dài + CRC32, index chỉ ghi ở footer khi đóng file. Mô phỏng `kill -9` ở một message ngẫu nhiên (chunk đang mở trong RAM mất, không có footer). Chạy với chunk = 20, 200, 2000 message.

**Dự đoán trước khi chạy** (ghi vào `prediction.md`):

1. Reader theo index đọc được bao nhiêu message từ file bị kill?
2. Reader quét tuần tự (dừng ở chunk hỏng) mất trung bình bao nhiêu message với chunk = 200? Mất tối đa bao nhiêu? Đổi ra giây ở 200 Hz.
3. Tỉ lệ nén tăng hay giảm theo kích thước chunk? Từ 20 lên 200 và từ 200 lên 2000, bước nào được nhiều hơn? Vì sao (gợi ý: zlib cần "xem" bao nhiêu byte để học được dữ liệu lặp)?
4. Với IMU 200 Hz + camera, chunk tính theo **byte** (MCAP mặc định tính theo byte, kiểm `chunk_size` của writer bạn dùng `[tự đo]`) thì một chunk 1 MiB chứa bao nhiêu giây IMU khi chỉ có IMU, và khi xen với ảnh 60 kB/frame ở 30 fps? Hệ quả cho bán kính vụ nổ của IMU?

Phương pháp: mất do kill = số message trong chunk đang mở = phân bố đều trên [0, chunk). Câu 4 tính tay từ byte/message (K5 Bài 13 đo được ~370 byte/message IMU trong MCAP).

```python
# [đã chạy] Log append-only đồ chơi: chunk nén + CRC, index chỉ ghi ở footer khi đóng file
import struct, zlib, io, numpy as np
rng = np.random.default_rng(7)
HDR = struct.Struct("<QHI")                       # log_time_ns, channel_id, độ dài payload
def imu_payload(i):                               # 6 × int16 giống gói IMU thô, nhiễu nhỏ
    v = np.array([0, 0, 16384, 0, 0, 0]) + rng.integers(-40, 40, 6)
    return v.astype("<i2").tobytes()

def write_log(n_msgs, chunk_msgs, kill_at=None):
    f, index, buf = io.BytesIO(), [], []
    f.write(b"TOYLOG01")
    def flush():
        raw = b"".join(buf); comp = zlib.compress(raw, 6)
        index.append((f.tell(), len(buf)))
        f.write(struct.pack("<4sII", b"CHNK", len(comp), zlib.crc32(raw)) + comp)
        buf.clear()
    for i in range(n_msgs):
        if i == kill_at: return f.getvalue()      # kill -9: chunk đang trong RAM mất, không có footer
        p = imu_payload(i); buf.append(HDR.pack(i * 5_000_000, 1, len(p)) + p)
        if len(buf) == chunk_msgs: flush()
    if buf: flush()
    f.write(b"INDX" + b"".join(struct.pack("<QI", o, c) for o, c in index)
            + struct.pack("<I", len(index)) + b"TOYLOG01")
    return f.getvalue()

def read_by_index(data):                          # reader nhanh: nhảy thẳng tới footer
    if not data.endswith(b"TOYLOG01") or len(data) < 20: return None
    return struct.unpack("<I", data[-12:-8])[0]   # số chunk theo index

def recover_by_scan(data):                        # reader chậm: quét tuần tự, dừng ở chunk hỏng
    pos, n = 8, 0
    while data[pos:pos+4] == b"CHNK":
        L, crc = struct.unpack("<II", data[pos+4:pos+12]); body = data[pos+12:pos+12+L]
        if len(body) < L or zlib.crc32(raw := zlib.decompress(body)) != crc: break
        n += len(raw) // (HDR.size + 12); pos += 12 + L
    return n

N, raw_size = 10_000, 10_000 * (HDR.size + 12)
print("chunk | nén x | index sau kill | mất TB sau kill (msg) | mất max")
for chunk in (20, 200, 2000):
    full = write_log(N, chunk)
    lost = []
    for _ in range(40):
        k = int(rng.integers(1, N))
        d = write_log(N, chunk, kill_at=k)
        assert read_by_index(d) is None
        lost.append(k - recover_by_scan(d))
    print(f"{chunk:5d} | {raw_size/len(full):5.2f} | không có      | {np.mean(lost):10.0f} | {max(lost):6d}")
```

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

Kết quả một lần chạy (seed 7, Python 3 + numpy; số "mất" dao động vài chục message giữa các seed):

| chunk | nén × | index sau kill | mất TB | mất max |
|---|---|---|---|---|
| 20 | 1,51 | không có | 9 | 19 |
| 200 | 1,92 | không có | 100 | 192 |
| 2000 | 2,01 | không có | 860 | 1807 |

1. **Không đọc được gì** qua index: footer không tồn tại. Đây là chỗ khác Kafka (broker tự dựng lại index khi khởi động).
2. Mất trung bình ≈ chunk/2 ≈ 100 message = **0,5 s ở 200 Hz**, tối đa gần một chunk (~1 s). Mọi chunk đã flush còn nguyên và quét lại được nhờ độ dài + CRC.
3. Tỉ lệ nén tăng theo chunk nhưng **lợi ích giảm dần**: 20→200 được nhiều (1,51→1,92), 200→2000 gần như không (→2,01). Chunk quá nhỏ thì header nén và từ điển chưa kịp học; vượt vài chục kB thì zlib (cửa sổ 32 kB) không thấy thêm gì. Vì vậy chunk lớn mua thêm rất ít nén nhưng mua thêm nhiều rủi ro mất dữ liệu.
4. Chỉ IMU: 1 MiB / 370 B ≈ 2830 message ≈ **14 s** IMU nằm trong RAM trước khi xuống đĩa. Xen với ảnh: luồng vào ≈ 30 × 60 kB + 200 × 370 B ≈ 1,87 MB/s, chunk 1 MiB đầy sau ≈ 0,56 s → bán kính vụ nổ của IMU chỉ ~0,56 s. **Cùng một `chunk_size`, bán kính vụ nổ theo thời gian khác nhau 25 lần tùy luồng nào đi chung file.** Đây là lý do K2 Bài 7 bắt chọn chunk bằng số đo, và là một lý do để tách luồng nhỏ quan trọng sang file/writer riêng.

</details>

### 6. Lăng kính đánh giá

Checklist khi đọc một khẳng định hay một kết quả về log/MCAP:

1. **Crash nào?** `kill -9` (process chết, OS sống: mất phần còn trong buffer của process) khác mất điện (mất thêm page cache chưa fsync) khác đĩa đầy (ghi dừng giữa record). Khẳng định không nói rõ là CHƯA RÕ.
2. **Reader nào?** Reader theo index, reader quét, hay `mcap recover`? "File đọc được" luôn phải đi kèm tên reader.
3. **Địa chỉ là gì?** Nếu tài liệu nói "offset" cho MCAP, hỏi: byte offset hay số thứ tự? Ai cấp? Có thể trùng không?
4. **Đọc một channel tốn bao nhiêu?** Có chunk nào chỉ chứa channel đó không, hay mọi chunk đều xen ảnh?
5. **Chunk tính theo byte hay theo thời gian, và luồng nào đi chung?** Bán kính vụ nổ đổi theo trộn luồng (mục 5 câu 4).
6. **Ai giữ bản sao thứ hai, từ lúc nào?** Trước khi upload VERIFIED (→ F3.5), độ bền = độ bền của một ổ đĩa trên robot.

**Khẳng định mẫu để tự chấm** (ĐÚNG / ĐÚNG MỘT PHẦN / SAI + vì sao):

- (a) Gemini, K5 Bài 13, bảng "Số phải ra": *"Sau 10 lần `kill -9`: file vẫn đọc được tới chunk hoàn chỉnh cuối cùng; mất mát tối đa chỉ là chunk đang dở. Cấu trúc append-only của MCAP bảo toàn dữ liệu khi mất điện."*
- (b) Bản gốc K5 Bài 13: *"MCAP append-only cho phép phục hồi file ghi dở."*
- (c) *"Đọc topic IMU 200 Hz từ một file MCAP 50 GB có camera thì nhanh, vì MCAP có index theo channel."*

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

- (a) **ĐÚNG MỘT PHẦN.** Vế đầu đúng *với reader quét hoặc sau `mcap recover`*; với `mcap info`/reader theo index thì file không có summary là lỗi (K2 Bài 4 bước 4 cho thấy CLI báo lỗi). "Mất tối đa là chunk đang dở" đúng cho `kill -9`; vế cuối **sai**: `kill -9` không phải mất điện — mất điện còn mất phần đã `write()` nhưng nằm trong page cache, và có thể để lại một chunk ghi dở giữa chừng. Hai thí nghiệm khác nhau (K5 Bài 13 vs Bài 14).
- (b) **ĐÚNG MỘT PHẦN.** Cho phép, nhưng không tự động: cần một bước `recover` có chủ đích trong pipeline ingest, và phần trong chunk đang mở thì không phục hồi được. Câu đúng: "data section tự mô tả đủ để quét lại; phần đã flush phục hồi được bằng `mcap recover`; phần trong RAM của writer thì mất."
- (c) **ĐÚNG MỘT PHẦN.** Index cho biết chunk nào *có* message IMU và ở đâu trong chunk. Nhưng nếu writer xen IMU và ảnh trong cùng chunk (mặc định thường là vậy), *mọi* chunk đều có IMU → phải tải và giải nén gần như toàn bộ 50 GB. Nhanh chỉ khi luồng nhỏ nằm ở chunk riêng hoặc file riêng (K2 Bài 7 đo đúng điều này).

</details>

### 7. Câu hỏi ngược

1. **[Vì sao không]** Vì sao MCAP không fsync sau mỗi chunk để mất điện chỉ mất đúng chunk đang mở?
   <details><summary>Hướng nghĩ</summary>

   Tính chi phí: fsync trên SSD/eMMC tốn từ dưới 1 ms tới hàng chục ms `[tự đo: fio --fsync=1]`, và chặn writer. Ở chunk 0,5 s thì chấp nhận được; ở chunk nhỏ thì không. Đây là chính sách của *ứng dụng ghi*, không phải của định dạng. Hỏi tiếp: fsync có giúp gì nếu ổ nói dối (cache ghi không có tụ dự phòng)?

   </details>
2. **[Quy mô]** 100 robot × 8 h/ngày, mỗi robot 24 GB/ngày. Một job sửa bug cần chạy lại extractor trên một năm dữ liệu. Cái gì gãy trước: băng thông đọc object store, CPU giải nén, hay việc tìm đúng file?
   <details><summary>Hướng nghĩ</summary>

   ≈ 876 TB/năm `[ước lượng: 100 × 24 GB × 365]`. Tính thời gian đọc ở vài GB/s tổng. Hỏi: có cần đọc ảnh không? Nếu IMU nằm xen trong chunk ảnh thì có. Quyết định bố trí chunk ở robot hôm nay quyết định chi phí reprocess năm sau.

   </details>
3. **[Failure mode]** Writer ghi đúng, file đóng đúng, nhưng thẻ nhớ đổi một bit trong một chunk giữa file. Reader theo index và reader quét mỗi bên thấy gì? Pipeline của bạn phát hiện ở đâu?
   <details><summary>Hướng nghĩ</summary>

   CRC của chunk (nếu writer ghi CRC — MCAP cho phép để 0 `[spec]`, kiểm writer của bạn) bắt được. Reader quét kiểu "dừng ở chunk hỏng" sẽ bỏ cả phần còn lại; reader theo index nhảy qua được. Hash cả file lúc niêm phong (→ F3.5, F3.8) bắt được trước khi xóa local.

   </details>
4. **[Liên ngành]** Hộp đen máy bay (FDR) ghi liên tục vào một vòng nhớ 25 giờ. Nó giống và khác log robot ở chỗ nào về "cái gì là nguồn sự thật" và "cái gì bị ghi đè"?
   <details><summary>Hướng nghĩ</summary>

   FDR là ring buffer: cũ bị đè, chỉ đoạn cuối trước sự cố quan trọng. Log robot cho học máy cần *toàn bộ* lịch sử. Nhưng trên robot thiếu đĩa (mất mạng nhiều ngày), bạn sẽ cần chính sách kiểu FDR cho luồng ưu tiên thấp (→ F3.9).

   </details>
5. **[Phản biện]** "Dùng Parquet thẳng trên robot, bỏ MCAP, vì cuối cùng dataset cũng là Parquet." Lập luận mạnh nhất cho và chống?
   <details><summary>Hướng nghĩ</summary>

   Chống: Parquet ghi footer một lần, file đang ghi bị cắt thường không cứu được bằng công cụ chuẩn; ghi từng dòng 200 Hz vào columnar cần buffer lớn; ảnh không hợp cột. Cho: bỏ một bước chuyển đổi, LeRobot v3 dùng Parquet + MP4. Xem phần "Tranh luận đang mở" cuối file.

   </details>

### 8. Liên kết ra ngoài

- **Database WAL và LSM-tree** (LevelDB, RocksDB): memtable trong RAM = chunk đang mở; SSTable bất biến = chunk đã flush; compaction = view dẫn xuất. Khác: WAL được cắt bỏ sau flush, log robot thì không.
- **Git**: object store bất biến định địa chỉ theo nội dung + ref trỏ vào. Giống "log là sự thật, branch là view". Khác: git không có thứ tự thời gian toàn cục; log cảm biến thì chỉ có thứ tự thời gian.

### 9. Áp vào khóa chính

- **K2 Bài 4, 7:** dùng checklist mục 6 khi đọc `mcap info`, khi cắt file thử recover, khi chọn chunk size bằng ba con số (nén, I/O đọc một channel, bán kính vụ nổ).
- **K5 Bài 13:** tách thí nghiệm `kill -9` khỏi thí nghiệm mất điện; ghi rõ reader nào đọc được bao nhiêu. Cân nhắc writer riêng cho IMU.
- **K6 Bài 9:** output episode là log bất biến; mọi bảng tổng hợp là view dẫn xuất có thể xóa và dựng lại.
- **K7 C7.3:** sidecar MCAP trên robot cần quy trình "đóng file → niêm phong → hash → upload" (→ F3.5); file không đóng đúng đi qua bước recover trước khi vào hàng đợi upload.

### 10. Độ tin cậy

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| Summary và Summary Offset là phần tùy chọn của MCAP; `sequence` là bộ đếm tùy chọn | `[spec]` | MCAP Specification, mục File structure và Message record |
| MCAP là storage mặc định của rosbag2 từ Iron | `[spec]` | Release notes ROS 2 Iron; kiểm `ros2 bag record --help` trên Jazzy |
| Kafka dựng lại index khi broker khởi động sau crash | `[chuẩn]` | Tài liệu Kafka, log recovery |
| Mất trung bình ≈ chunk/2 khi kill ngẫu nhiên | `[đã chạy]` | Mô phỏng mục 5 |
| Chi phí fsync trên ổ của robot | `[tự đo]` | `fio --fsync=1` trên đúng ổ |

### 11. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** MCAP Specification (mcap.dev, mục Specification).
- **Giải thích:** Jay Kreps, *The Log: What every software engineer should know about real-time data's unifying abstraction* (LinkedIn Engineering blog, 2013).
- **Đào sâu:** Martin Kleppmann, *Designing Data-Intensive Applications*, chương 3 (log-structured storage) và chương 11 (log-based message brokers).
- **Tự kiểm tra:** (1) giải thích cho một backend engineer trong 5 câu vì sao một file MCAP bị kill vẫn còn dữ liệu nhưng `mcap info` báo lỗi; (2) vẽ lại hình mục 2 từ trí nhớ; (3) câu hỏi:

  Robot ghi IMU + ảnh chung một writer, chunk 4 MiB, zstd. Bạn muốn giảm bán kính vụ nổ của IMU xuống dưới 0,5 s mà không đổi chunk của ảnh. Hai cách?
  <details><summary>Đáp án</summary>

  (1) Writer/file riêng cho luồng nhỏ (IMU, odom, diagnostics) với chunk nhỏ; (2) cùng file nhưng flush theo **thời gian** (đóng chunk mỗi ≤0,5 s bất kể kích thước) nếu writer hỗ trợ `[tự đo]`. Cách (1) còn giúp đọc IMU không phải giải nén ảnh.

  </details>

---
