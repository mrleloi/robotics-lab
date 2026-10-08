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

## F3.2 — Encoding và schema evolution: Protobuf/CDR/Avro, quy tắc tương thích, file tự mô tả (4h)

> **Dùng cho:** K2 Bài 6, 8b, 9 · K4 Bài 10 · K5 Bài 4, 13 · K6 Bài 5, 9 · K7 C7.4 · **Cần trước:** F3.1 · **Sau viên nang này bạn đánh giá được:** một thay đổi schema có an toàn ở tầng nào (bytes / code / nghĩa); một con số "byte/message" dùng để tính dung lượng có đáng tin không; một thông tin mới nên vào payload, metadata channel hay topic riêng.

### 1. Câu chuyện

Sáng 1/8/2012, Knight Capital triển khai code giao dịch mới lên tám server. Code mới **dùng lại một cờ** trong message lệnh, cờ này nhiều năm trước điều khiển một tính năng đã bỏ tên Power Peg. Một server không được cập nhật. Trên server đó, code cũ vẫn còn, đọc cờ theo nghĩa cũ và bắn lệnh liên tục. Trong khoảng 45 phút, công ty lỗ khoảng 460 triệu USD (theo lệnh của SEC năm 2013) `[chuẩn]`. Không có byte nào sai định dạng. Cùng một bit, hai reader, hai nghĩa.

Đây chính là lý do quy tắc đầu tiên của Protobuf là *không bao giờ dùng lại số hiệu trường; đánh dấu `reserved`* `[spec: protobuf.dev, "Updating A Message Type"]`. Với dữ liệu robot, rủi ro còn kéo dài hơn: một file ghi năm 2026 sẽ được đọc năm 2031 bằng code mà người ghi chưa từng thấy. K2 Bài 6 đã cho bạn bảng quy tắc theo tầng wire/code/nghĩa; viên nang này lo phần K2 chưa nói: **mỗi họ encoding chọn đặt thông tin schema ở đâu, và hệ quả của lựa chọn đó**.

### 2. Mô hình tư duy

Mọi encoding trả lời một câu: *reader biết cấu trúc của bytes nhờ đâu?*

| Họ | Thông tin cấu trúc nằm ở | Kích thước một message | Tiến hóa schema | Gặp ở đâu trong lộ trình |
|---|---|---|---|---|
| **JSON** | Trong từng message (tên trường lặp lại) | Lớn, phụ thuộc giá trị | Tự do, không ai kiểm | metadata nhỏ, config |
| **Protobuf** | Số hiệu trường + wire type trong từng trường; tên ở schema ngoài | **Phụ thuộc giá trị** (varint, trường bằng 0 bị bỏ) | Theo số hiệu: thêm/bỏ trường an toàn ở tầng wire | `imu.proto` K2, Foxglove schema |
| **CDR** (ROS 2) | Hoàn toàn ở schema ngoài; bytes chỉ là các trường xếp liền nhau có căn lề | Gần như cố định theo kiểu (`sensor_msgs/Imu` = 324 B với `frame_id` 8 ký tự, K5 Bài 13) | **Gần như không có**: thêm một trường làm lệch mọi trường sau; đổi định nghĩa = kiểu mới | mọi message ROS 2 |
| **Avro** | Schema của writer, bắt buộc phải có lúc đọc; bytes không có tag | Nhỏ nhất | Phân giải writer schema ↔ reader schema, có default | Kafka + registry |
| **Parquet/Arrow** | Footer/schema của file, theo cột | Tính theo cột, không theo message | Thêm cột dễ, đổi kiểu khó | LeRobot, F3.6 |

```
 Protobuf (TLV)        [tag=4|LEN][...Vec3...][tag=5|LEN][...][tag=7|LEN]"imu-01..."
                        ↑ reader lạ gặp tag 9 → giữ lại như unknown field, đọc tiếp
 CDR (vị trí cố định)  [encap 4][sec 4][nsec 4][len 4]"imu_link\0"[pad 3][quat 32][cov 72]...
                        ↑ chèn thêm 1 trường giữa → mọi byte phía sau đọc lệch, không lỗi nào báo
```

**File tự mô tả** (MCAP nhúng schema theo channel; Parquet nhúng schema ở footer) chuyển câu hỏi từ "reader có schema không" sang "**code của tôi**, viết theo schema X, đọc file mang schema Y có đúng nghĩa không". Schema nhúng giải quyết tầng bytes. Nó không mang theo đơn vị nếu bạn không ghi, không mang theo nghĩa của giá trị 0, không mang theo thư viện giải mã.

Hệ quả thực hành cho ROS 2: vì CDR không có câu chuyện tiến hóa, quy ước của repo là **không sửa message chuẩn; thứ chuẩn không có thì vào metadata channel hoặc topic riêng** (`CONVENTIONS.md` mục 4). rosbag (ROS 1) từng có "migration rules" để đọc bag cũ sau khi đổi message; rosbag2 không có cơ chế tương đương `[tự đo — kiểm tài liệu rosbag2 bản Jazzy]`.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Kafka + Confluent: message mang **schema ID** 5 byte, schema ở registry | MCAP mang **cả schema** trong file | Registry là dịch vụ phải sống; 10 năm sau có thể không còn. File tự mô tả sống độc lập nhưng không có ai chặn schema sai lúc ghi | Ghi schema ID thay vì schema vào file robot "cho gọn" → file mồ côi khi registry đổi |
| Protobuf trong gRPC: kích thước message ít quan trọng | Protobuf ghi 200 Hz × nhiều giờ | Kích thước **phụ thuộc giá trị**: trục bằng 0.0 đúng thì biến mất, `sequence` lớn tốn thêm byte | Tính dung lượng từ một message mẫu "đẹp" (nhiều số 0) → thiếu |
| Thêm giá trị enum mới vào API | Thêm trường enum vào message cảm biến | proto3: reader mới đọc dữ liệu cũ thấy **giá trị số 0** của enum. Nếu số 0 mang nghĩa thật, dữ liệu cũ bị gán nghĩa đó | Toàn bộ file cũ hiện là `clock_source = ESP32_TIMER` (bài tập mục 5) |
| JSON schema linh hoạt, thêm field tùy ý | CDR của ROS 2 | CDR không có tag; reader dùng schema khác writer đọc ra rác có hình dạng hợp lệ | Sửa `sensor_msgs/Imu` cục bộ "thêm 1 trường" → Foxglove/rosbag2 của người khác đọc lệch |

**Chấm mô hình:**

- *"Protobuf luôn nhỏ hơn CDR."* — **ĐÚNG MỘT PHẦN.** Với `ImuSample` của repo, một mẫu đầy đủ ~190 B so với 324 B của `sensor_msgs/Imu` CDR — nhưng hai message không mang cùng thông tin (`sensor_msgs/Imu` có quaternion và ba ma trận covariance). So sánh đúng phải cùng nội dung. Phản ví dụ: một message toàn `double` khác 0 và không có trường rỗng thì Protobuf tốn thêm 1 byte tag mỗi trường so với CDR.
- *"Schema nhúng trong file nên đọc được mãi mãi."* — **ĐÚNG MỘT PHẦN.** Bytes giải mã được nếu còn thư viện cho encoding đó. Gãy: schema `ros2msg` cần đủ định nghĩa phụ thuộc (MCAP nối chúng vào một chuỗi); nghĩa (đơn vị, frame, giá trị 0) không nằm trong schema; và code đọc theo tên trường vỡ khi tên đổi. Phản ví dụ: file năm 2026 có `clock_source` enum mà số 0 là "ESP32"; reader năm 2031 đọc đúng bytes, gán sai nghĩa cho mọi file trước khi trường đó tồn tại.

**Tên chuẩn của thứ bạn đã làm:** khi bạn chọn Avro + registry với chế độ `BACKWARD_TRANSITIVE` để consumer mới đọc được mọi bản cũ, bạn đang làm **schema evolution có kiểm ở thời điểm ghi**. Ở robot, cổng kiểm đó dời sang **CI của repo schema** (`buf breaking` cho `.proto`) và **ingest** (từ chối hoặc gắn cờ file mang schema chưa đăng ký). Còn thiếu: test tương thích *ngữ nghĩa* bằng golden file (K2 Bài 6) — không công cụ breaking-check nào làm thay.

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | Encoding / serialization | Cách biến cấu trúc thành bytes | Schema |
| 🟢 | Self-describing file | File mang schema của chính nó | File mang cả nghĩa |
| 🟢 | Varint, implicit presence (proto3) | Số nhỏ tốn ít byte; trường bằng mặc định không được ghi | Mọi trường luôn được ghi |
| 🟢 | Enum zero value | Giá trị mặc định khi trường vắng mặt | Một lựa chọn như mọi lựa chọn khác |
| 🟢 | CDR, căn lề (alignment) | Encoding vị trí cố định của DDS/ROS 2 | Có tag như Protobuf |
| 🟡 | Writer schema / reader schema (Avro) | Hai schema được phân giải lúc đọc | — |
| 🟡 | XCDR2, kiểu appendable/mutable (DDS-XTypes) | Biến thể CDR có hỗ trợ tiến hóa | ROS 2 mặc định đã dùng `[tự đo]` |
| 🔴 | Chi tiết wire format từng kiểu | Tra spec khi viết parser | — |

### 5. Bài tập dự đoán

Dùng `GỐC/src/proto/sensors/v1/imu.proto` (lớp đã sinh sẵn `imu_pb2.py`, cần `protobuf` cài trong Python; không cần `protoc`). Script dựng một bản v2 bằng code: thêm `ClockSource clock_source = 9` với enum *thiết kế vội* `ESP32_TIMER = 0, HOST_PTP = 1, HOST_UNSYNCED = 2`.

**Dự đoán** (ghi `prediction.md`, tính tay trước — mỗi trường Protobuf = tag 1 byte + giá trị; `double` 8 byte; chuỗi/message con = tag + độ dài + nội dung; varint 7 bit mỗi byte):

1. Một `ImuSample` đầy đủ (giá trị trong hàm `sample()`) dài bao nhiêu byte?
2. Nếu `ax` và `gz` đo được **đúng 0.0**, message ngắn đi bao nhiêu byte?
3. `sequence` = 1, 300, 2³²−1: kích thước đổi thế nào?
4. Đọc bytes v1 bằng lớp v2: `clock_source` ra giá trị nào?
5. v2 ghi `clock_source = HOST_PTP`; một service v1 parse rồi serialize lại (ví dụ một bước lọc cũ trong pipeline), v2 đọc lại: còn `HOST_PTP` không?
6. Dung lượng một giờ IMU 200 Hz bằng `ImuSample` (chưa tính overhead MCAP), so với con số "~50 byte/mẫu, 36 MB/giờ" của bản gốc K5 Bài 13.

```python
# [đã chạy] Kích thước Protobuf phụ thuộc giá trị; enum mới đọc dữ liệu cũ ra gì
import sys; sys.path.insert(0, "/home/user/robotics-lab/src")   # GỐC/src — sửa theo máy bạn
from proto.sensors.v1 import imu_pb2
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory, timestamp_pb2

def sample(ax=0.01, gz=-0.0005, seq=123456):
    m = imu_pb2.ImuSample(frame_id="imu_link", sequence=seq,
                          calibration_id="imu-01@2026-11-02-a", source_device_id="esp32-01")
    m.stamp.seconds, m.stamp.nanos = 1_791_504_000, 123_456_789
    m.linear_acceleration.x, m.linear_acceleration.y, m.linear_acceleration.z = ax, -0.02, 9.787
    m.angular_velocity.x, m.angular_velocity.y, m.angular_velocity.z = 0.001, 0.002, gz
    m.acceleration_covariance.extend([4e-4, 0, 0, 0, 4e-4, 0, 0, 0, 4e-4])
    return m

print("Q1 đủ trường            :", len(sample().SerializeToString()), "byte")
print("Q2 ax = gz = 0.0 đúng   :", len(sample(ax=0.0, gz=0.0).SerializeToString()), "byte")
for s in (1, 300, 2**32 - 1):
    print(f"Q3 sequence={s:<11d}:", len(sample(seq=s).SerializeToString()), "byte")

# v2: thêm enum clock_source số hiệu 9 — dựng descriptor bằng code, không cần protoc
fdp = descriptor_pb2.FileDescriptorProto()
imu_pb2.DESCRIPTOR.CopyToProto(fdp)
fdp.name = "imu_v2.proto"; fdp.package = "sensors.v2"
enum = fdp.enum_type.add(name="ClockSource")
for i, n in enumerate(["CLOCK_SOURCE_ESP32_TIMER", "CLOCK_SOURCE_HOST_PTP", "CLOCK_SOURCE_HOST_UNSYNCED"]):
    enum.value.add(name=n, number=i)                       # thiết kế VỘI: giá trị 0 mang nghĩa thật
msg = next(m for m in fdp.message_type if m.name == "ImuSample")
for f in msg.field:
    if f.type_name.startswith(".sensors.v1"): f.type_name = f.type_name.replace("v1", "v2")
msg.field.add(name="clock_source", number=9, type=descriptor_pb2.FieldDescriptorProto.TYPE_ENUM,
              type_name=".sensors.v2.ClockSource", label=descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL)
pool = descriptor_pool.DescriptorPool()
pool.AddSerializedFile(timestamp_pb2.DESCRIPTOR.serialized_pb)
V2 = message_factory.GetMessageClass(pool.Add(fdp).message_types_by_name["ImuSample"])

old_bytes = sample().SerializeToString()                  # file ghi năm 2026 bằng v1
v2 = V2.FromString(old_bytes)
enum_t = V2.DESCRIPTOR.fields_by_name["clock_source"].enum_type
print("Q4 v1 đọc bằng v2       :", enum_t.values_by_number[v2.clock_source].name)
new = V2.FromString(old_bytes); new.clock_source = 1      # v2 ghi HOST_PTP
back = imu_pb2.ImuSample.FromString(new.SerializeToString())
print("Q5 v2→v1→v2 giữ field 9 :", V2.FromString(back.SerializeToString()).clock_source)
```

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

Chạy với `protobuf` 7.36 (Python):

| Câu | Kết quả | Vì sao |
|---|---|---|
| 1 | **190 byte** | stamp 13 · frame_id 10 · sequence 4 · hai Vec3 29 mỗi cái · covariance packed 74 (số 0 trong mảng packed vẫn được ghi) · hai chuỗi ID 21 + 10 |
| 2 | **172 byte** (−18) | mỗi `double` bằng 0.0 không được ghi: mất 1 byte tag + 8 byte |
| 3 | 188 / 189 / 192 byte | varint: 1 → 1 byte, 300 → 2, 2³²−1 → 5 (so với 123456 → 3) |
| 4 | **`CLOCK_SOURCE_ESP32_TIMER`** | trường vắng → giá trị số 0 của enum. Mọi file trước v2 bị gán "đóng dấu bằng ESP32" |
| 5 | **Còn (=1)** | v1 giữ trường lạ số 9 như unknown field và ghi lại nguyên vẹn (proto3 từ bản 3.5 giữ unknown fields `[spec]`) |
| 6 | ≈ 190 × 200 × 3600 ≈ **137 MB/giờ** | gần 4 lần "36 MB/giờ"; `sensor_msgs/Imu` CDR trong MCAP ≈ 265 MB/giờ (K5 Bài 13) |

Sửa thiết kế: số 0 của mọi enum là `CLOCK_SOURCE_UNSPECIFIED`, và reader coi UNSPECIFIED là "không biết" (quy ước style guide của Protobuf/Buf `[spec]`). Câu 2–3 là lý do không lấy **một** message mẫu để ước dung lượng: lấy phân bố kích thước trên dữ liệu thật.

</details>

### 6. Lăng kính đánh giá

Checklist khi đọc một thay đổi schema hay một con số kích thước:

1. Thay đổi an toàn ở **tầng nào**: bytes, code (tên, JSON, đường dẫn Foxglove), hay nghĩa? Khẳng định không nói tầng là CHƯA RÕ.
2. Encoding nào? Quy tắc của Protobuf **không** áp cho CDR, và ngược lại.
3. Trường mới vắng mặt trong dữ liệu cũ thì reader thấy gì — và giá trị đó có trùng một giá trị vật lý hợp lệ không (0 °C, 0 m/s², enum 0)?
4. Con số "byte/message" đo trên dữ liệu thật hay một mẫu tay? Có tính overhead container không?
5. Thông tin mới là **theo message** (payload/topic riêng), **theo luồng, không đổi trong file** (metadata channel), hay **theo file** (Metadata record / Attachment)?
6. Có golden file cũ trong repo để test đọc lại không?

**Khẳng định mẫu để tự chấm:**

- (a) `robotics-data-infra-roadmap.md`, bảng thuật ngữ: *"Schema evolution / backward compatibility — Bạn đã biết. Đây là lợi thế."*
- (b) Gemini, K5 Bài 13: *"Các trường `calibration_id`, `clock_source`, `sequence` không nằm trong định dạng message ROS 2 chuẩn, do đó chúng phải được lưu vào trường metadata của channel MCAP."*
- (c) `khoa-5/m3-data-stack.md` (bản đã soạn), giải thích con số của bản gốc: *"…vì 50 byte là kích thước `ImuSample` Protobuf tự chế ở Khóa 2."*

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

- (a) **ĐÚNG MỘT PHẦN.** Lợi thế thật ở tầng bytes với Protobuf/Avro. Gãy ở ba chỗ người backend ít gặp: CDR của ROS 2 gần như không có tiến hóa (→ không sửa message chuẩn); không có registry chặn lúc ghi (robot offline); và tương thích ngữ nghĩa (đơn vị, enum 0, giá trị mặc định trùng giá trị vật lý) quan trọng hơn tương thích bytes vì dữ liệu sống nhiều năm.
- (b) **ĐÚNG MỘT PHẦN, sai với `sequence`.** `calibration_id`, `clock_source` không đổi trong suốt luồng → metadata channel là chỗ đúng (`CONVENTIONS.md` mục 4). `sequence` đổi **mỗi message**; metadata channel là một map tĩnh ghi một lần khi tạo channel, không chứa được giá trị theo message. Chỗ đúng: trường `sequence` của Message record MCAP (spec: *"Optional message counter to detect message gaps"*) hoặc topic chẩn đoán như `CONVENTIONS.md` quy định. Bản gốc K5 Bài 13 viết "`sequence` → metadata hoặc topic chẩn đoán": nửa đầu cùng lỗi.
- (c) **SAI theo số đo.** Mục 5: `ImuSample` đầy đủ là 190 byte, không phải 50. ~50 B chỉ khớp với **gói thô từ MCU** (6 × int16 + timestamp + header, như K2 Bài 1 viết) hoặc một `ImuSample` thiếu covariance và ID. Kết luận của K5 (bản gốc thiếu 7 lần so với `sensor_msgs/Imu`) vẫn đúng; chỉ lời giải thích nguồn gốc con số cần sửa — đã ghi vào ghi chú cho người điều phối.

</details>

### 7. Câu hỏi ngược

1. **[Nếu…thì]** Nếu firmware ESP32 gửi `ImuSample` Protobuf qua serial, còn host đổi sang `sensor_msgs/Imu` CDR để ghi, thì bước chuyển đó phải làm gì với trường vắng mặt (covariance chưa đo)?
   <details><summary>Hướng nghĩ</summary>

   CDR không có "vắng mặt": phải điền số. REP/`sensor_msgs/Imu` có quy ước: covariance toàn 0 = "không biết", phần tử [0] = −1 = "không có ước lượng" `[spec: comment trong Imu.msg]`. Đây là nơi presence của Protobuf phải được dịch sang một quy ước giá trị.

   </details>
2. **[Quy mô]** 100 robot chạy 4 bản firmware khác nhau, mỗi bản ghi schema hơi khác cùng tên `sensors.v1.ImuSample`. Ở bước ingest, bạn phát hiện bằng gì?
   <details><summary>Hướng nghĩ</summary>

   Hash nội dung schema nhúng (không phải tên) làm khóa; bảng đăng ký "hash schema → được chấp nhận / cần migration"; file mang hash lạ vào quarantine. Đây là registry, chỉ là chạy ở ingest thay vì ở producer.

   </details>
3. **[Failure mode]** Một bước pipeline đọc MCAP, sửa một trường, ghi file mới bằng lớp Protobuf **cũ** đã biên dịch. Trường mới v2 còn không? Với JSON thì sao?
   <details><summary>Hướng nghĩ</summary>

   Nhị phân: còn (unknown fields, câu 5 mục 5). Nếu bước đó đi qua JSON (`MessageToJson`) hoặc dựng message mới bằng tay từ các trường nó biết: mất âm thầm.

   </details>
4. **[Vì sao không]** Vì sao ROS 2 không dùng Protobuf trên dây để có tiến hóa schema miễn phí?
   <details><summary>Hướng nghĩ</summary>

   ROS 2 xây trên DDS, chuẩn OMG có CDR từ thời CORBA; vị trí cố định cho phép zero-copy và kích thước biết trước, hợp với hệ thời gian thực. Đánh đổi: tiến hóa bằng tên kiểu mới. Không phải ai đúng ai sai; là ưu tiên khác.

   </details>

### 8. Liên kết ra ngoài

- **HL7/DICOM trong y tế**: ảnh DICOM mang hàng trăm thẻ tự mô tả; bệnh viện vẫn gặp lỗi vì thẻ "private" mỗi hãng một nghĩa. Giống: tự mô tả không đủ nghĩa. Khác: có ủy ban chuẩn hóa từ điển thẻ.
- **FITS trong thiên văn**: file ảnh từ 1981 vẫn đọc được vì header văn bản mô tả trục và đơn vị (`BUNIT`, `CTYPE`). Giống: file tự mô tả sống lâu hơn phần mềm. Khác: FITS đặt đơn vị *vào chuẩn*, thứ Protobuf không làm.

### 9. Áp vào khóa chính

- **K2 Bài 6:** thêm vào bộ test một trường enum mới với golden file v1; kiểm enum 0 là `UNSPECIFIED`.
- **K2 Bài 8b, K5 Bài 13:** dùng mục 6 câu 5 để quyết định chỗ cho `clock_source` (metadata channel), `sequence` (Message record hoặc `/diagnostics`), `calibration_id` (metadata channel), bảng hiệu chuẩn (Attachment).
- **K5 Bài 13:** tính dung lượng/giờ từ phân bố kích thước message thật, không từ một mẫu.
- **K7 C7.4:** data contract cho robot ghi rõ encoding, hash schema và quy ước giá trị "không biết".

### 10. Độ tin cậy

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| Knight Capital: cờ dùng lại, một server không cập nhật, ~460 triệu USD, ~45 phút | `[chuẩn]` | SEC Administrative Proceeding 34-70694 (2013) |
| Không dùng lại số hiệu trường, dùng `reserved` | `[spec]` | protobuf.dev, "Updating A Message Type" |
| Kích thước 190/172/188–192 byte; enum vắng → 0; unknown field được giữ | `[đã chạy]` | Mục 5, protobuf Python 7.36 |
| `sensor_msgs/Imu` CDR = 324 B | `[đã chạy ở K5 Bài 13]` | `len(m.data)` trên MCAP thật |
| rosbag2 không có migration rule như rosbag1 | `[tự đo]` | Tài liệu rosbag2 bản Jazzy |

### 11. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** Protocol Buffers documentation — "Encoding" và "Updating A Message Type" (protobuf.dev).
- **Giải thích:** Kleppmann, *Designing Data-Intensive Applications*, chương 4 (Encoding and Evolution) — so Thrift/Protobuf/Avro theo đúng câu "schema nằm ở đâu".
- **Đào sâu:** MCAP Specification, mục Schema/Channel và phụ lục "Well-known encodings" (ros2msg, protobuf).
- **Tự kiểm tra:** (1) giải thích cho backend engineer trong 5 câu vì sao không sửa `sensor_msgs/Imu` dù "chỉ thêm một trường"; (2) vẽ lại bảng mục 2 cột "thông tin cấu trúc nằm ở"; (3) câu hỏi:

  Bạn thêm `optional double temperature_c = 9` (có presence). Đọc file cũ: `HasField` trả gì, giá trị đọc ra là gì, và vì sao cách này tốt hơn `double temperature_c = 9`?
  <details><summary>Đáp án</summary>

  `HasField("temperature_c")` = False, giá trị đọc ra 0.0. Có presence nên code phân biệt được "không đo" với "0 °C"; không có presence thì không (K2 Bài 6 Chấm mô hình 2).

  </details>

---

## F3.3 — Event time vs processing time: window, watermark, dữ liệu đến muộn (5h)

> **Dùng cho:** K2 Bài 2 · K5 Bài 7, 13 · K7 C7.2 · **Cần trước:** F3.1; nên có F4.1 (ppm, drift) và F4.6 (thời điểm của một phép đo) · **Sau viên nang này bạn đánh giá được:** một timestamp trong file là thời điểm của *cái gì*, đo bằng đồng hồ nào; một cửa sổ/watermark có đóng sớm quá không; và một tỉ lệ "dữ liệu muộn" là do mạng, do hàng đợi hay do **đồng hồ trôi**.

### 1. Câu chuyện

Tyler Akidau và nhóm ở Google viết *Streaming 101* (2015) và *The Dataflow Model* (VLDB 2015) sau nhiều năm vận hành MillWheel và FlumeJava. Ví dụ họ dùng: điểm số của một trò chơi di động. Người chơi trên máy bay, điện thoại offline, điểm được gửi lên khi hạ cánh vài giờ sau. Nếu bạn cộng điểm theo **giờ server nhận** (processing time), bảng xếp hạng của giờ 14:00 chứa điểm chơi lúc 9:00. Nếu cộng theo **giờ chơi** (event time), bạn phải trả lời câu khó: *khi nào thì chắc đã nhận đủ điểm của 9:00?* Câu trả lời của họ là **watermark** — một ước lượng (không phải bảo đảm) rằng "dữ liệu có event time trước T có lẽ đã tới hết" — cộng với **allowed lateness** và cơ chế phát lại kết quả khi dữ liệu muộn vẫn tới `[chuẩn]`.

Robot thêm một tầng mà điện thoại không có. Điện thoại đóng dấu bằng đồng hồ đã đồng bộ NTP. ESP32 đóng dấu bằng timer đếm µs từ lúc boot, chạy bằng thạch anh lệch vài chục ppm (→ F4.1). *Kịch bản:* một phiên ghi 3 giờ, host quy đổi `esp_timer` sang giờ host bằng offset đo lúc khởi động và không bù drift. Pipeline đóng cửa sổ 1 s theo đồng hồ host với dung sai 50 ms. Giờ đầu không có gì lạ. Từ phút thứ 20, tỉ lệ "dữ liệu muộn" tăng đều, không có sự cố mạng nào. Không ai đổi code. Đồng hồ trôi đã âm thầm biến thành độ muộn. Bài tập mục 5 dựng lại đúng kịch bản này.

### 2. Mô hình tư duy

Một mẫu IMU có ít nhất **bốn** thời điểm. Chỉ cái đầu tiên là sự thật; ba cái còn lại là ước lượng hoặc nhật ký:

```
 thời gian thật ─────●──────────────────────────────────────────────►
                     │ t_phys: lúc gia tốc kế lấy mẫu (giữa cửa sổ lọc của chip, → F4.6)
 đồng hồ ESP32  ─────●  esp_timer = t_phys·(1+ε) + θ   (ε ~ ±10–50 ppm, θ = gốc lúc boot)
                     │   ↓ mô hình quy đổi (offset + drift), có version = clock_source
 header.stamp   ─────●  ước lượng t_phys trên trục host  ← EVENT TIME (dùng để ghép, cửa sổ)
                     ╲
                      ╲ trễ USB + driver + hàng đợi (ms, đuôi dài, có lúc kẹt 100+ ms)
 publish_time   ───────────●  lúc node publish                 ┐
 log_time       ─────────────●  lúc writer ghi vào MCAP        ┘ PROCESSING TIME (nhật ký)
```

Định nghĩa trong MCAP: `log_time` là *"Time at which the message was recorded"*, `publish_time` là *"Time at which the message was published. If not available, must be set to the log time"* `[spec: MCAP, Message record]`. Không trường nào trong hai trường đó là thời điểm đo; thời điểm đo nằm trong payload (`header.stamp`).

**Window và watermark trong một hình:**

```
 event time (stamp) →  [ 9.0 ─────────── 10.0 )[ 10.0 ──────── 11.0 )
 watermark W(t) = "mọi mẫu có stamp < W đã tới"
 cửa sổ [9,10) đóng khi W ≥ 10.0;  mẫu stamp=9.97 tới sau đó = DỮ LIỆU MUỘN → bỏ / side output / phát lại kết quả
 Hai cách dựng W:
   (1) theo dữ liệu:   W = (stamp lớn nhất đã thấy của nguồn chậm nhất) − L    ← đúng khi mỗi nguồn tới theo thứ tự
   (2) theo đồng hồ host: W = now_host − L                                    ← phổ biến trên robot, NGẦM GIẢ ĐỊNH stamp và host cùng trục
```

Ba điều khác backend, mỗi cái là một quyết định:

1. **Watermark phải tính theo từng nguồn rồi lấy min.** Một nguồn kẹt 200 ms (camera USB) giữ watermark của cả pipeline lại. Lấy max thì nguồn kẹt thành "muộn".
2. **Độ muộn có ba thành phần cộng lại:** trễ truyền (đuôi dài), kẹt hàng đợi (→ F3.9), và **sai số mô hình đồng hồ** (lệch offset + drift chưa bù). Thành phần cuối *tăng theo thời gian phiên* nếu drift không được bù. L phải bao cả ba, và chỉ tự đo được: phân bố `log_time − header.stamp` (K2 Bài 2) theo từng luồng, theo thời gian.
3. **Event time có thể lùi.** ESP32 reboot (timer về 0), NTP/PTP bước đồng hồ host, đổi mô hình quy đổi giữa phiên. Đây không phải lỗi dữ liệu để xóa; là **sự kiện** cần ghi lại (đổi `clock_source`/epoch) và tách phiên.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Flink `BoundedOutOfOrdernessWatermarks(L)` | Dung sai muộn L cho luồng cảm biến | Trong Flink, L bao *out-of-order*; ở đây L còn phải bao **drift tích lũy**, thứ tăng tuyến tính theo giờ chạy | Chọn L từ một phiên 10 phút, ra hiện trường 3 giờ thì drop tăng dần |
| Kafka `CreateTime` (đồng hồ producer đã NTP) | `header.stamp` từ timer MCU | `CreateTime` cùng thang với giờ thế giới, sai số ms; timer MCU có gốc riêng và tốc độ riêng, phải qua mô hình quy đổi | Ghi thẳng µs-từ-boot vào `stamp` → mẫu nằm ở năm 1970 (đã chấm ở K5 Bài 13) |
| `LogAppendTime` do broker cấp, đơn điệu | `log_time` của writer | Không phải trọng tài cho thời điểm đo; nhiều thread ghi thì `log_time` có thể không đơn điệu giữa các channel | Sort/ghép theo `log_time` cho tiện, nhúng jitter USB vào dữ liệu |
| Dữ liệu muộn → side output, sửa kết quả sau | Mẫu muộn → không được bỏ âm thầm | Một mẫu bỏ vì muộn là phép đo mất vĩnh viễn (→ F3.9). Pipeline online (điều khiển) được phép bỏ; pipeline ghi dataset thì không | Writer ghi file áp chính sách cửa sổ của bộ điều khiển → lỗ trong dataset không ai đếm |

**Chấm mô hình:**

- *Mô hình của bạn ở K3 lượt 7: "mỗi thiết bị có khái niệm về clock, về thời gian của chúng … dù giới hạn tốc độ lại nhưng mọi thứ vẫn lệch clock nhau … nên phải có buffer, để các giao thức có nguồn để hoạt động."* — **ĐÚNG MỘT PHẦN.** Đúng: mỗi thiết bị có thời gian riêng, và chúng lệch nhau. Gãy: buffer hấp thụ **lệch tốc độ tức thời** (burst, jitter), không sửa **lệch đồng hồ**. Lệch đồng hồ cần một *mô hình* (offset + drift, ước lượng liên tục, → F4.4–F4.6) và một trường ghi lại mô hình nào đã dùng (`clock_source`). Phản ví dụ: mục 5 — buffer/dung sai 150 ms che được drift 40 ppm trong một giờ (144 ms) nhưng sang giờ thứ hai thì không; tăng buffer chỉ dời thời điểm hỏng.
- *"Sort theo timestamp là xong thứ tự."* — Đã chấm **SAI** ở K5 Bài 13 (hai đồng hồ khác gốc, khác tốc độ). Thêm: ngay cả trong một nguồn, sau reboot thứ tự theo `stamp` khác thứ tự thật.

**Tên chuẩn của thứ bạn đã làm:** khi bạn tính SLA "độ tươi dữ liệu" bằng `now − event_timestamp` trên dashboard, bạn đang đo **event-time skew** (Akidau gọi là *skew* giữa event time và processing time). Còn thiếu ở robot: tách skew thành phần truyền (đuôi, ổn định) và phần đồng hồ (trôi đều). Phần sau là tín hiệu để **sửa đồng hồ**, không phải để tăng L.

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | Event time / processing time | Lúc sự việc xảy ra / lúc hệ thống thấy nó | `publish_time` là event time |
| 🟢 | `header.stamp`, `publish_time`, `log_time` | Thời điểm đo (ước lượng) / publish / ghi | Ba tên một thứ |
| 🟢 | Watermark | Ước lượng "dữ liệu trước T đã tới hết" | Bảo đảm |
| 🟢 | Allowed lateness, late data | Độ muộn còn chấp nhận / mẫu tới sau khi cửa sổ đóng | Lỗi mạng |
| 🟢 | `clock_source`, mô hình quy đổi | Đồng hồ nào + công thức nào sinh ra stamp | Chi tiết triển khai không cần lưu |
| 🟡 | Tumbling / sliding / session window | Cửa sổ rời / chồng / theo khoảng lặng | — |
| 🟡 | Trigger, accumulation (Dataflow) | Khi nào phát kết quả, phát lại thì cộng dồn hay thay | — |
| 🔴 | Exactly-once window state trong Flink | Không cần cho robot một máy | — |

### 5. Bài tập dự đoán

Mô phỏng 1 giờ IMU 200 Hz. ESP32 chậm 40 ppm so với host; host quy đổi bằng offset lúc boot, **không bù drift**. Trễ USB 2 ms + jitter mũ trung bình 1 ms. Mỗi 10 s, USB/đĩa kẹt 120 ms vắt qua ranh giới cửa sổ. Cửa sổ 1 s theo `stamp`, đóng khi đồng hồ host vượt `cuối cửa sổ + L`.

**Dự đoán:**

1. Sau 1 giờ, `stamp` lệch thời gian thật bao nhiêu ms? Dấu nào?
2. Với L = 20 ms, 50 ms, 150 ms: tỉ lệ mẫu muộn tổng, và nó **đổi thế nào giữa 10 phút đầu và 10 phút cuối**?
3. Với L = 50 ms, khoảng phút thứ mấy drift bắt đầu tự gây muộn (không cần kẹt)?
4. Đếm mẫu trong mỗi cửa sổ 1 s theo processing time và theo event time: min/max mỗi cách? Cách nào cho thấy drift?
5. Với L = 150 ms, sau bao nhiêu giờ thì lại bắt đầu muộn?

Tham số cần tra cho máy thật: ppm của thạch anh ESP32 (`[spec]` datasheet module, thường ghi ±10 ppm tại 25 °C cho thạch anh 40 MHz; sống thật thì đo ở K5 Bài 10), phân bố trễ USB (K2 Bài 2 hoặc K5 Bài 8).

```python
# [đã chạy] Watermark theo đồng hồ host + đồng hồ nguồn trôi: dữ liệu "muộn" sinh ra từ đâu
import numpy as np
rng = np.random.default_rng(3)
T, F = 3600.0, 200                                   # 1 giờ IMU 200 Hz
t_true = np.arange(0, T, 1 / F)                      # thời điểm vật lý đo (không ai thấy trực tiếp)
DRIFT = -40e-6                                       # đồng hồ ESP32 chậm 40 ppm so với host
stamp = t_true * (1 + DRIFT)                         # header.stamp sau khi quy đổi offset LÚC BOOT, không bù drift
lat = 0.002 + rng.exponential(0.001, t_true.size)    # trễ USB + driver: 2 ms + jitter
ph = (t_true - 9.95) % 10.0                          # mỗi 10 s: USB/disk kẹt 120 ms, vắt qua
stall = ph < 0.12                                    # ranh giới cửa sổ (9.95 → 10.07 s)
lat[stall] += 0.12 - ph[stall]                       # mẫu dồn lại, xả một lượt khi hết kẹt
arrive = t_true + lat                                # host nhận (processing time)

def late_fraction(L):
    # cửa sổ 1 s theo event time (stamp); đóng khi đồng hồ host vượt (cuối cửa sổ + L)
    w_end = np.floor(stamp) + 1.0
    late = arrive > w_end + L
    blocks = late.reshape(6, -1).mean(axis=1)        # tỉ lệ muộn theo từng khối 10 phút
    return late.mean(), blocks

for L in (0.020, 0.050, 0.150):
    tot, blocks = late_fraction(L)
    print(f"L={L*1e3:4.0f} ms  muộn tổng {tot:7.2%}  theo 10 phút:", " ".join(f"{b:6.1%}" for b in blocks))

# cùng dữ liệu, đếm theo cửa sổ processing time (thời điểm host nhận)
cnt_proc = np.bincount(np.floor(arrive).astype(int))[:3599]
cnt_event = np.bincount(np.floor(stamp).astype(int))[:3599]
print("đếm/cửa sổ theo processing time: min", cnt_proc.min(), "max", cnt_proc.max())
print("đếm/cửa sổ theo event time    : min", cnt_event.min(), "max", cnt_event.max())
print("lệch stamp so với t_true sau 1 giờ (ms):", round((t_true[-1] - stamp[-1]) * 1e3, 1))
```

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

| L | muộn tổng | 10 phút đầu → 10 phút cuối |
|---|---|---|
| 20 ms | 6,27% | 0,7% → 12,2% |
| 50 ms | 4,17% | 0,6% → 9,5% |
| 150 ms | 0,00% | 0% suốt giờ đầu |

1. **144 ms**, `stamp` chậm hơn thật (40 ppm × 3600 s).
2. Tỉ lệ muộn **tăng tuyến tính theo thời gian phiên**. Phần nền ~0,5% ở 10 phút đầu là các mẫu bị kẹt 70 ms qua ranh giới (10 mẫu mỗi 10 s). Phần tăng dần là drift.
3. Drift + trễ nền ≈ 50 ms khi 40 ppm × t ≈ 47 ms → t ≈ **20 phút**. Mô phỏng: khối 10–20 phút còn 0,9%, khối 20–30 phút nhảy lên 2,3%.
4. Theo processing time: **190–210** mẫu/cửa sổ — đợt kẹt dồn mẫu sang cửa sổ sau, nhìn như tần số dao động ±5% dù cảm biến đều tuyệt đối. Theo event time: **200–201**; cửa sổ thỉnh thoảng có 201 là dấu vết của drift (đồng hồ nguồn chậm nên 1 s "theo nó" dài hơn 1 s thật). Đếm theo processing time là đo hàng đợi, không đo cảm biến.
5. Drift tự vượt ~150 ms sau ≈ 148 ms / 40 ppm ≈ 3 700 s, **khoảng 1 giờ 2 phút**; phiên 3 giờ sẽ hỏng ở giờ thứ hai. Sửa đúng: bù drift (ước lượng liên tục offset + tốc độ, → F4.6) và tăng `clock_source` version, không tăng L.

</details>

### 6. Lăng kính đánh giá

Checklist khi gặp một timestamp, một cửa sổ, hay một con số "dữ liệu muộn":

1. Timestamp này là **thời điểm của cái gì** (đo, publish, ghi, nhận)? Do **đồng hồ nào** đóng dấu, quy đổi bằng **mô hình nào**, mô hình có version không?
2. Cửa sổ/watermark dựng **theo dữ liệu** hay **theo đồng hồ host**? Nếu theo host: ngầm giả định stamp và host cùng trục — giả định đó được kiểm ở đâu?
3. Watermark tính **theo từng nguồn** rồi lấy min, hay gộp?
4. L được chọn từ **phân bố đo được** (đuôi nào, phiên dài bao nhiêu), hay từ cảm giác?
5. Tỉ lệ muộn **có xu hướng theo thời gian phiên** không? Có → nghi đồng hồ trước khi nghi mạng.
6. Mẫu muộn đi đâu: bỏ (có đếm?), side output, hay sửa kết quả? Pipeline này là điều khiển online hay ghi dataset?
7. Event time **lùi** thì sao: reboot, bước đồng hồ? Có tách phiên/epoch không?

**Khẳng định mẫu để tự chấm:**

- (a) Gemini, K5 Bài 13, bước 2: *"Ghi cả `publish_time` (timestamp lúc cảm biến đo) và `log_time` (timestamp lúc daemon host ghi)."*
- (b) Bản gốc K5 Bài 16, bảng rule: *"Timestamp đơn điệu tăng — Thời gian một chiều — Bất kỳ vi phạm nào."*
- (c) *"Đặt watermark đủ rộng thì không còn dữ liệu muộn."*

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

- (a) **SAI** ở định nghĩa. Theo spec MCAP, `publish_time` là lúc message được publish (không có thì bằng `log_time`); thời điểm đo nằm trong payload, `header.stamp`. Dùng `publish_time` làm thời điểm đo là nhúng trễ driver + node vào dữ liệu. Phần đúng: ghi cả hai thời gian processing để chẩn đoán hàng đợi.
- (b) **ĐÚNG MỘT PHẦN.** Đúng như một rule *cảnh báo* trên `header.stamp` **của một nguồn trong một epoch đồng hồ**. Sai nếu áp lên `log_time` gộp nhiều channel (có thể không đơn điệu hợp lệ), và sai nếu coi mọi vi phạm là dữ liệu hỏng: reboot ESP32 hay bước PTP tạo ra lùi thời gian hợp lệ, cần ghi thành sự kiện và tách epoch, không xóa. Bài tập F3.7 cho thấy rule này bắt được timestamp lùi 12 ms mà không rule nào khác bắt.
- (c) **SAI.** Watermark heuristic chỉ là ước lượng (Akidau). Với drift chưa bù, độ muộn tăng không giới hạn theo thời gian phiên (mục 5 câu 5). Với đuôi dài (USB kẹt, GC, swap), luôn có mẫu vượt mọi L hữu hạn. L càng rộng thì kết quả càng trễ — đánh đổi độ đầy đủ lấy độ tươi, không xóa được nó.

</details>

### 7. Câu hỏi ngược

1. **[Nếu…thì]** Nếu bạn bù drift bằng hồi quy tuyến tính trên các cặp (esp_timer, host_time) *sau khi phiên kết thúc*, cửa sổ online và dataset offline sẽ thấy hai event time khác nhau. Cái nào ghi vào `header.stamp`?
   <details><summary>Hướng nghĩ</summary>

   Một lựa chọn: ghi raw counter + mô hình online vào file; dataset là view dẫn xuất áp mô hình offline tốt hơn, có version (→ F3.8). Đây là "log là sự thật, view tái tạo được" áp vào thời gian.

   </details>
2. **[Quy mô]** 100 robot, mỗi robot 6 luồng, mỗi luồng một đồng hồ. Watermark toàn đội tính thế nào, và một robot mất mạng 3 ngày làm gì với nó?
   <details><summary>Hướng nghĩ</summary>

   Watermark per-robot, per-stream; xử lý theo phiên của từng robot thay vì cửa sổ toàn cục. Robot offline = trò chơi di động trên máy bay của Akidau: batch hóa theo phiên khi dữ liệu tới.

   </details>
3. **[Failure mode]** Host chạy NTP và bị bước đồng hồ lùi 300 ms giữa phiên. Những trường nào trong file bị ảnh hưởng, những trường nào không?
   <details><summary>Hướng nghĩ</summary>

   `log_time` (nếu lấy từ CLOCK_REALTIME) và mọi stamp quy đổi qua giờ host. Timer ESP32 thô không bị. Đây là lý do giữ raw counter và dùng CLOCK_MONOTONIC cho đo khoảng (→ F4.3).

   </details>
4. **[Liên ngành]** Thiên văn dùng thang thời gian TDB/TT và ghi rõ trạm nào, đồng hồ nào cho mỗi quan sát. Giống `clock_source` ở đâu, khác ở đâu?
   <details><summary>Hướng nghĩ</summary>

   Giống: thời điểm luôn đi kèm thang đo và phép quy đổi. Khác: thiên văn quy đổi có mô hình vật lý chuẩn hóa quốc tế; robot tự xây mô hình và phải tự version.

   </details>
5. **[Vì sao không]** Vì sao không đóng dấu tất cả ở host lúc nhận cho đơn giản, khỏi cần đồng hồ MCU?
   <details><summary>Hướng nghĩ</summary>

   Receive time = thời điểm đo + trễ USB có đuôi dài; jitter vài ms nhúng thẳng vào dữ liệu. Ước lượng sai số: ở 2 rad/s, 3 ms jitter = 0,006 rad sai lệch góc mỗi lần ghép (→ F3.4). Đóng dấu tại nguồn + mô hình quy đổi cho sai số nhỏ hơn và đo được.

   </details>

### 8. Liên kết ra ngoài

- **Tài chính:** sàn giao dịch đóng dấu lệnh theo đồng hồ của sàn (processing time của sàn) nhưng quy định MiFID II buộc đồng bộ đồng hồ tới 100 µs cho giao dịch tần số cao `[chuẩn — kiểm RTS 25]`. Giống: thời điểm là dữ liệu có sai số được quy định. Khác: có một trọng tài pháp lý; robot không có.
- **Mạng (RTP/VoIP):** gói RTP mang timestamp của nguồn theo đồng hồ lấy mẫu; bên nhận dùng jitter buffer (L) và báo cáo độ trôi qua RTCP. Đúng mô hình mục 2, đã chạy hàng tỉ cuộc gọi.

### 9. Áp vào khóa chính

- **K2 Bài 2:** vẽ `log_time − header.stamp` theo thời gian phiên; độ dốc khác 0 = drift chưa bù, không phải mạng.
- **K5 Bài 7, 13:** ghi `clock_source` + version mô hình quy đổi; chọn L từ phân bố đo được của luồng chậm nhất (K5 Bài 13 phần 2 đã dùng `L_max` để mở rộng truy vấn theo `log_time`).
- **K7 C7.2:** source time ESP32 vs host là câu hỏi của chính viên nang này trên robot thật; kiểm tỉ lệ muộn theo giờ chạy trong soak.

### 10. Độ tin cậy

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| Định nghĩa `log_time`, `publish_time` | `[spec]` | MCAP Specification, Message record |
| Watermark là heuristic; event time vs processing time | `[chuẩn]` | Akidau, Streaming 101/102; Dataflow Model, VLDB 2015 |
| Tỉ lệ muộn tăng theo phiên khi drift không bù; số trong bảng | `[đã chạy]` | Mục 5, mô hình đồ chơi |
| Thạch anh ESP32 ±10 ppm | `[spec — kiểm datasheet module bạn mua]` | Đo thật ở K5 |
| MiFID II 100 µs cho HFT | `[chuẩn — kiểm RTS 25]` | Không ảnh hưởng nội dung chính |

### 11. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** Akidau et al., *The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing* (VLDB 2015).
- **Giải thích:** Tyler Akidau, *Streaming 101* và *Streaming 102* (O'Reilly Radar, 2015–2016).
- **Đào sâu:** Kleppmann, *DDIA* chương 11, mục "Reasoning About Time".
- **Tự kiểm tra:** (1) giải thích cho backend engineer trong 5 câu vì sao "dữ liệu muộn" tăng dần mà mạng không đổi; (2) vẽ lại hình bốn thời điểm từ trí nhớ; (3) câu hỏi:

  Cửa sổ đếm theo processing time báo IMU "chỉ có 190 mẫu/s" trong một giây. Ba giả thuyết, và một phép kiểm phân biệt chúng?
  <details><summary>Đáp án</summary>

  (1) Cảm biến thật sự rớt mẫu; (2) hàng đợi kẹt, mẫu dồn sang giây sau; (3) đồng hồ host bị bước. Kiểm: đếm theo `header.stamp` và nhìn `sequence` — đủ 200 và `sequence` liên tục → (2) hoặc (3), không phải (1); nhìn cửa sổ kế bên có 210 không.

  </details>

---

## F3.4 — Ghép luồng khác tần số: as-of join, nội suy, resampling, sai số căn chỉnh (5h)

> **Dùng cho:** K2 Bài 1 (lướt), Bài 11 · K5 Bài 13 · K7 C7, C8.3 · **Cần trước:** F3.3; F4.6 (thời điểm của một phép đo); F5.5 (Nyquist, aliasing) nên đọc mục 2 · **Sau viên nang này bạn đánh giá được:** một bảng "đã đồng bộ" ghép camera với IMU bằng phương pháp nào, sai số căn chỉnh tới đâu (ms và đơn vị vật lý), có bịa dữ liệu trong lỗ hổng không, và có tạo ra tần số không tồn tại không.

### 1. Câu chuyện

Năm 1991, Charles Lee và Mark Ready công bố cách đoán một giao dịch chứng khoán là lệnh mua hay bán: so giá khớp với giá chào mua/bán **đang hiệu lực tại thời điểm khớp**. Đó là một as-of join: với mỗi giao dịch, lấy báo giá gần nhất *trước* nó. Vấn đề họ gặp: báo giá và giao dịch đi qua hai đường báo cáo khác nhau với độ trễ khác nhau, nên "báo giá gần nhất trước giao dịch" theo timestamp thường là báo giá *sai*. Họ đề nghị lùi báo giá 5 giây — quy tắc "5-second rule" — một hiệu chỉnh cho độ lệch đồng hồ giữa hai luồng `[chuẩn: Lee & Ready, Journal of Finance, 1991]`. Ba mươi năm sau, khi dữ liệu có timestamp mili giây rồi micro giây, giới nghiên cứu vẫn tranh luận độ lùi đúng là bao nhiêu. Phép join thì dễ; **sai số căn chỉnh** mới là nội dung.

Ghép IMU 200 Hz với camera 30 Hz là đúng bài toán đó với thêm hai cái bẫy mà tài chính ít gặp: tín hiệu **liên tục** (nên nội suy là hợp lệ, và cũng vì thế mà dễ bịa), và tín hiệu **có tần số** (nên lấy mẫu lại có thể sinh ra dao động không tồn tại).

### 2. Mô hình tư duy

```
 IMU 200 Hz   |    |    |    |    |    |    |    |    |    |    |    |    |    |   (5 ms)
 camera 30 Hz ├──── phơi sáng ────┤ stamp = giữa phơi sáng (→ F4.6)
                       ▲ t_cam
   as-of (backward):  lấy mẫu IMU cuối cùng ≤ t_cam      → nhân quả, trễ 0..5 ms, TB 2,5 ms
   nearest:           mẫu gần nhất                        → không nhân quả, lệch 0..2,5 ms
   linear interp:     nội suy giữa hai mẫu kề             → không nhân quả, sai số ≈ h²/8·|x''|
   interval join:     mọi mẫu IMU trong [t_cam−Δ, t_cam+Δ] → giữ phân bố, để downstream quyết
```

**Ngân sách sai số căn chỉnh** cho một đại lượng x(t) (ví dụ vận tốc góc):

| Nguồn | Độ lớn trên x | Giảm bằng |
|---|---|---|
| Lệch đồng hồ còn lại δ giữa hai luồng | ≈ \|dx/dt\| · δ | đồng bộ tốt hơn (F4.5, F4.6) |
| Phương pháp ghép | as-of: ≈ \|dx/dt\| · h/2 trung bình; nội suy: ≤ h²/8 · \|d²x/dt²\| | đổi phương pháp |
| Định nghĩa thời điểm camera sai (đầu phơi sáng thay vì giữa, rolling shutter) | ≈ \|dx/dt\| · t_exp/2, khác nhau theo hàng ảnh | đóng dấu đúng (F4.6) |
| Lỗ hổng trong luồng nhanh | không giới hạn nếu nội suy xuyên lỗ | tolerance, mask |

K5 Bài 13 đã có mô phỏng cho thấy khi δ vượt cỡ một chu kỳ IMU thì phương pháp ghép hết quan trọng. Viên nang này lo ba cái bẫy **không nằm trong công thức nội suy**:

1. **Resampling là lọc.** "Đưa IMU về 30 Hz cho gọn" là lấy mẫu lại ở 30 Hz; mọi thành phần trên 15 Hz (rung motor, rung khung) **gập** xuống dưới 15 Hz (aliasing, → F5.5). Hạ tần số đúng = lọc thông thấp trước, rồi mới lấy mẫu; hoặc đừng hạ, giữ cửa sổ mẫu IMU quanh mỗi frame.
2. **Nội suy xuyên lỗ là bịa dữ liệu.** `np.interp` vui vẻ nối thẳng qua một khoảng USB rớt 250 ms. Kết quả mượt, không NaN, sai.
3. **As-of không có tolerance trả về mẫu cũ bất kỳ.** `merge_asof` mặc định không giới hạn tuổi mẫu: frame trong lỗ hổng được gắn mẫu IMU từ trước lỗ.

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Stream–stream join theo khóa (Flink interval join, Kafka Streams `JoinWindows`) | Ghép theo **thời gian**, không có khóa | Join backend ghép sự kiện rời rạc; không ai nội suy giữa hai đơn hàng. Tín hiệu vật lý liên tục nên nội suy được — chỉ cho đại lượng liên tục (không cho cờ trạng thái, ảnh; quaternion phải slerp) | Nội suy cờ `range_status` ra 0,5; trung bình hai ảnh |
| SQL `ASOF JOIN` (DuckDB, kdb+ `aj`, `pd.merge_asof`) | Đúng công cụ | Mặc định không có giới hạn tuổi mẫu; chiều mặc định là *backward* (nhân quả). Phải đặt tolerance theo chu kỳ luồng nhanh | Lỗ hổng biến thành mẫu cũ hợp lệ |
| Downsample metrics (avg mỗi phút) cho dashboard | Downsample tín hiệu cảm biến | Metric backend hiếm khi có tần số tuần hoàn cao; rung cơ khí có. Lấy mẫu thưa không lọc = aliasing, trung bình theo khối là một bộ lọc thô có búp phụ | Thấy "dao động 10 Hz" trong dataset, đi tìm nguồn không tồn tại |
| Clock skew giữa hai service: chấp nhận vài ms | Lệch vài ms giữa camera và IMU | Ở 2 rad/s, 5 ms lệch = 0,01 rad ≈ 0,6° mỗi lần ghép `[ước lượng]`; với hiệu chuẩn camera–IMU hay fusion, đó là sai số hệ thống | Mô hình học được độ trễ cố định như một đặc trưng của robot |

**Chấm mô hình:**

- *"Cứ resample mọi luồng về một lưới chung 30 Hz rồi join theo chỉ số, đơn giản nhất."* — **SAI** cho luồng có thành phần trên 15 Hz. Phản ví dụ: bài tập mục 5 — rung 40 Hz biên độ 0,4 rad/s hiện thành đỉnh phổ ở 10 Hz trong chuỗi 30 Hz. Đúng khi: đã lọc thông thấp trước (và chấp nhận mất thông tin rung), hoặc tín hiệu vốn chậm (nhiệt độ, pin).
- *"`merge_asof` là as-of join, dùng là xong."* — **ĐÚNG MỘT PHẦN.** Đúng thuật toán. Thiếu ba tham số quyết định nghĩa: `direction` (backward = nhân quả, cho dữ liệu huấn luyện policy chạy online; nearest/forward = nhìn trước tương lai), `tolerance` (tuổi mẫu tối đa), và cả hai bảng phải **sort theo cùng một thời gian event đã quy đổi**. Phản ví dụ: mục 5 Bẫy 3.

**Tên chuẩn của thứ bạn đã làm:** khi bạn ghép log request với metric hạ tầng "theo phút gần nhất" để debug, bạn đang làm **as-of join với zero-order hold**. Còn thiếu ở robot: ghi **tuổi mẫu** (khoảng cách thời gian giữa hai bên ghép) thành một cột của bảng kết quả, để mọi người dùng sau biết sai số căn chỉnh của từng dòng — giống cách K5 Bài 15 biến sai số sync thành một trường dữ liệu.

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | As-of join | Ghép mỗi dòng với dòng gần nhất trước nó theo thời gian | Join bằng nhau theo timestamp |
| 🟢 | Tolerance / tuổi mẫu | Khoảng cách tối đa cho phép giữa hai bên ghép | Tùy chọn |
| 🟢 | Nội suy tuyến tính, slerp | Nối thẳng giữa hai mẫu; nội suy quaternion | Dùng được cho mọi kênh |
| 🟢 | Aliasing, lọc chống aliasing | Tần số cao gập xuống khi lấy mẫu thưa; lọc trước khi hạ tần số | Chỉ chuyện âm thanh |
| 🟢 | Sai số căn chỉnh (alignment error) | Sai lệch giá trị do ghép lệch thời điểm | Bằng nửa chu kỳ |
| 🟡 | Interval join | Ghép với *mọi* mẫu trong một khoảng | — |
| 🟡 | Zero-order hold | Giữ giá trị cũ tới mẫu sau | — |
| 🔴 | Resampling đa pha (polyphase) | `scipy.signal.resample_poly` làm hộ | — |

### 5. Bài tập dự đoán

IMU 200 Hz đo vận tốc góc = quay chậm 0,5 Hz biên độ 1 rad/s + rung motor **40 Hz** biên độ 0,4 rad/s. USB rớt 250 ms IMU tại t = 8 s. Camera 30 Hz, stamp giữa phơi sáng, **đã cùng đồng hồ** (để tách riêng ba bẫy khỏi lỗi đồng hồ).

**Dự đoán:**

1. Bẫy 1: nội suy IMU tại các mốc camera (30 Hz), không lọc trước. Trong phổ của chuỗi 30 Hz, đỉnh lớn nhất trên 2 Hz nằm ở tần số nào? (công thức: tần số gập = |f − k·f_s| nhỏ nhất)
2. Bẫy 2: bao nhiêu frame camera rơi vào lỗ? Sai số lớn nhất khi nội suy xuyên lỗ cỡ bao nhiêu (so với biên độ các thành phần)?
3. Bẫy 3: `merge_asof` backward không tolerance trả bao nhiêu NaN? Mẫu IMU được gắn cũ nhất là bao nhiêu ms? Với tolerance 7,5 ms (1,5 chu kỳ IMU) thì bao nhiêu NaN?

```python
# [đã chạy] Ghép IMU 200 Hz vào camera 30 Hz: ba cái bẫy không nằm ở công thức nội suy
import numpy as np, pandas as pd
rng = np.random.default_rng(5)
T = 20.0
def gyro(t):   # quay chậm 0.5 Hz + rung motor 40 Hz (rad/s)
    return 1.0 * np.sin(2*np.pi*0.5*t) + 0.4 * np.sin(2*np.pi*40*t)
t_imu = np.arange(0, T, 1/200)
x_imu = gyro(t_imu) + rng.normal(0, 0.01, t_imu.size)
gap = (t_imu > 8.0) & (t_imu < 8.25)                      # USB rớt 250 ms IMU
t_imu_g, x_imu_g = t_imu[~gap], x_imu[~gap]
t_cam = np.arange(0.01, T, 1/30)                         # mốc giữa phơi sáng, đã cùng clock

# Bẫy 1: "resample IMU về 30 Hz cho gọn" = nội suy tại mốc camera, không lọc trước
x30 = np.interp(t_cam, t_imu_g, x_imu_g)
spec = np.abs(np.fft.rfft((x30 - x30.mean()) * np.hanning(x30.size)))
f = np.fft.rfftfreq(x30.size, 1/30)
band = f > 2                                              # bỏ vùng quay chậm
print("B1 đỉnh phổ lớn nhất trên 2 Hz của chuỗi 30 Hz: %.1f Hz" % f[band][spec[band].argmax()])

# Bẫy 2: nội suy xuyên qua lỗ hổng — trông mượt, là dữ liệu bịa
in_gap = (t_cam > 8.0) & (t_cam < 8.25)
err = np.abs(np.interp(t_cam[in_gap], t_imu_g, x_imu_g) - gyro(t_cam[in_gap]))
print("B2 số frame camera rơi vào lỗ: %d, sai số max khi nội suy xuyên lỗ: %.2f rad/s" % (in_gap.sum(), err.max()))

# Bẫy 3: merge_asof không tolerance lặng lẽ gắn mẫu cũ
cam = pd.DataFrame({"t": t_cam}); imu = pd.DataFrame({"t": t_imu_g, "gyro": x_imu_g})
j0 = pd.merge_asof(cam, imu, on="t", direction="backward")
j1 = pd.merge_asof(cam, imu, on="t", direction="backward", tolerance=0.0075)
age = t_cam - imu["t"].to_numpy()[np.searchsorted(t_imu_g, t_cam, side="right") - 1]
print("B3 không tolerance: NaN =", j0.gyro.isna().sum(), "| tuổi mẫu max = %.0f ms" % (age.max()*1e3))
print("B3 tolerance 7.5 ms: NaN =", j1.gyro.isna().sum())
```

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

| Câu | Kết quả | Đọc |
|---|---|---|
| 1 | Đỉnh ở **10,0 Hz** | 40 − 30 = 10 Hz. Rung 40 Hz biến thành "dao động 10 Hz" với cùng biên độ; không bộ lọc nào phía sau tách ra được nữa |
| 2 | **8 frame**, sai số max ≈ **0,42 rad/s** | ≈ biên độ rung: nội suy xuyên lỗ xóa rung và trả về đường thẳng trông hợp lý |
| 3 | Không tolerance: **0 NaN**, mẫu cũ nhất **243 ms**. Tolerance 7,5 ms: **8 NaN** | Đúng 8 frame trong lỗ hiện ra như thiếu dữ liệu, thay vì dữ liệu cũ |

Hệ quả thiết kế: bảng ghép nên có cột `imu_age_ms` (tuổi mẫu) và cột cờ "nội suy/giữ/thiếu"; hạ tần số chỉ sau lọc thông thấp (`scipy.signal.decimate` hoặc `resample_poly` có lọc sẵn); với ứng dụng cần rung (phát hiện va chạm, chẩn đoán motor), giữ cửa sổ mẫu IMU gốc quanh mỗi frame thay vì một giá trị.

</details>

### 6. Lăng kính đánh giá

Checklist khi gặp một bảng/dataset "đã đồng bộ" hay một con số sai số căn chỉnh:

1. Hai luồng có được đưa về **cùng một trục event time** trước khi ghép không (F3.3)? Ghép theo `log_time` là CHƯA RÕ cho tới khi chứng minh trễ nhỏ hơn ngân sách.
2. Phương pháp: as-of, nearest, nội suy, interval? **Nhân quả** hay không, và ứng dụng có cần nhân quả không (train policy chạy online)?
3. Có **tolerance** không? Có cột tuổi mẫu không? Lỗ hổng hiện ra thế nào?
4. Có **hạ tần số** không? Nếu có, lọc trước chưa, và tín hiệu có năng lượng trên Nyquist mới không?
5. Thời điểm của camera là đầu, giữa hay cuối phơi sáng, hay lúc nhận frame?
6. Sai số căn chỉnh được báo bằng **ms và bằng đơn vị vật lý** (rad, m/s²) ở tốc độ thay đổi điển hình, hay chỉ "đã sync"?
7. Kênh nào được nội suy: chỉ đại lượng liên tục? quaternion có slerp?

**Khẳng định mẫu để tự chấm:**

- (a) `robotics-data-infra-roadmap.md`: *"Nội suy (interpolation) — Hai stream khác tần số → phải nội suy về cùng mốc thời gian. Đây là code bạn sẽ viết."*
- (b) Gemini, K5 Bài 17, bảng ưu tiên drop: luồng camera — *"Mất một khung nhìn, nhưng thuật toán thị giác có thể nội suy."*
- (c) *"Ghép bằng as-of với IMU 200 Hz thì sai số căn chỉnh là 2,5 ms."*

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

- (a) **ĐÚNG MỘT PHẦN.** Đúng là bạn sẽ viết code ghép. Sai ở chữ "phải nội suy": as-of (nhân quả) là lựa chọn đúng cho dữ liệu huấn luyện một policy chạy online, vì nội suy dùng mẫu tương lai; interval join giữ thông tin rung; và nội suy chỉ hợp lệ cho kênh liên tục, có tolerance. Thiếu hẳn: aliasing khi đưa về "cùng mốc" thưa hơn.
- (b) **ĐÚNG MỘT PHẦN.** Một bộ ước lượng trạng thái online có thể *dự đoán qua* frame thiếu. Nhưng trong **dataset**, frame thiếu phải được ghi là thiếu (mask, bản ghi drop, → F3.9), không được nội suy ảnh để lấp. Nội suy ảnh tạo dữ liệu không ai quan sát.
- (c) **ĐÚNG MỘT PHẦN.** 2,5 ms là sai số *trung bình của riêng phương pháp* (nửa chu kỳ, phân bố đều 0–5 ms). Sai số căn chỉnh tổng còn cộng lệch đồng hồ δ, định nghĩa thời điểm camera (giữa phơi sáng, rolling shutter), và phải đổi sang đơn vị vật lý. Ngoài ra, với tỉ số 200/30 = 20/3, mốc camera chỉ rơi vào ba pha cố định của chu kỳ IMU, nên sai số có cấu trúc lặp chứ không đều (K5 Bài 13).

</details>

### 7. Câu hỏi ngược

1. **[Nếu…thì]** Nếu camera có rolling shutter 30 ms từ hàng đầu tới hàng cuối, "thời điểm của frame" là gì khi ghép với IMU? Interval join giúp gì?
   <details><summary>Hướng nghĩ</summary>

   Mỗi hàng ảnh có thời điểm riêng (→ F4.6, K5 Bài 11). Một giá trị IMU cho cả frame là xấp xỉ; giữ cả cửa sổ IMU trong [đầu phơi sáng hàng đầu, cuối phơi sáng hàng cuối] cho phép downstream bù theo hàng.

   </details>
2. **[Quy mô]** 1 000 giờ dữ liệu, bạn đổi phương pháp ghép (as-of → nội suy). Phải tính lại cái gì, và nếu bảng ghép là "nguồn sự thật" thì sao?
   <details><summary>Hướng nghĩ</summary>

   Nếu bảng ghép là view dẫn xuất từ MCAP (F3.1, F3.8), chỉ chạy lại job. Nếu bảng ghép đã thay raw (raw bị xóa cho tiết kiệm), phương pháp ghép bị đông cứng vĩnh viễn. Đây là lý do không xóa raw.

   </details>
3. **[Failure mode]** Hai luồng ghép rất khớp trong lab, lệch rõ trên robot thật chạy 30 phút. Ba giả thuyết theo thứ tự nên kiểm?
   <details><summary>Hướng nghĩ</summary>

   Drift chưa bù (lệch tăng theo thời gian, F3.3); trễ thay đổi theo tải CPU (camera đóng dấu lúc nhận); nhiệt độ làm đổi tần số thạch anh. Vẽ độ lệch ước lượng (cross-correlation theo cửa sổ, F4.6) theo thời gian phiên.

   </details>
4. **[Liên ngành]** Y sinh ghép ECG 500 Hz với huyết áp 125 Hz và SpO₂ 1 Hz trên monitor ICU. Họ giải bài toán ghép thế nào, và cái gì giống robot?
   <details><summary>Hướng nghĩ</summary>

   Thiết bị cùng một máy dùng chung đồng hồ; ghép theo sự kiện (đỉnh R của ECG) thay vì theo lưới. Giống: neo vào một sự kiện vật lý chung (như TN-1 GPIO chung ở K5 Bài 8). Khác: thiết bị y tế được chứng nhận cùng đồng hồ; robot ghép từ linh kiện rời.

   </details>
5. **[Vì sao không]** Vì sao không nâng IMU lên 1 kHz để sai số as-of còn 0,5 ms?
   <details><summary>Hướng nghĩ</summary>

   Khi δ đồng hồ là vài ms thì sai số phương pháp đã không phải phần trội. Còn băng thông, CPU, và bộ lọc nội của chip (ODR cao thì nhiễu khác). Tối ưu thành phần nhỏ nhất của ngân sách là lãng phí.

   </details>

### 8. Liên kết ra ngoài

- **Tài chính (kdb+/q `aj`, TAQ):** as-of join là phép toán hạng nhất của cơ sở dữ liệu tick; câu chuyện Lee–Ready ở mục 1. Giống: bài toán lệch đồng hồ giữa hai luồng báo cáo. Khác: giá là bậc thang (zero-order hold là đúng nghĩa), không nội suy.
- **Âm thanh số:** chuyển 48 kHz → 44,1 kHz bắt buộc qua bộ lọc chống aliasing; đó là lý do "sample rate converter" là một khối có tên trong mọi DAW. Giống hệt bẫy 1. Khác: âm thanh có đồng hồ chung chính xác, robot thì không.

### 9. Áp vào khóa chính

- **K2 Bài 11:** lớp lỗi về đồng bộ cần oracle là sai số căn chỉnh *đo được*; dùng checklist mục 6 để viết định nghĩa lớp lỗi.
- **K5 Bài 13:** quyết định as-of hay nội suy theo ứng dụng (nhân quả hay không), đặt tolerance theo chu kỳ, ghi cột tuổi mẫu; không hạ tần số khi chưa lọc.
- **K7 C7, C8.3:** hợp nhất odometry 50 Hz với pose marker 30 Hz có trễ xử lý ảnh: thời điểm của pose là lúc chụp, không phải lúc tính xong; ghép bằng as-of trên lịch sử odometry (đây là cách bộ ước lượng trạng thái xử lý đo muộn).

### 10. Độ tin cậy

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| Lee & Ready 1991, quy tắc 5 giây | `[chuẩn]` | Journal of Finance 46(2), 1991 |
| Sai số nội suy tuyến tính ≤ h²/8·max\|x''\| | `[chuẩn]` | Giải tích số |
| Alias 40 → 10 Hz, 8 frame, 243 ms, 8 NaN | `[đã chạy]` | Mục 5; pandas 3.0, numpy |
| `merge_asof` mặc định `direction="backward"`, không tolerance | `[spec]` | Tài liệu pandas `merge_asof`; kiểm bản bạn cài |
| 0,6° sai lệch ở 2 rad/s, 5 ms | `[ước lượng]` | 2 × 0,005 = 0,01 rad |

### 11. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** Lee & Ready, *Inferring Trade Direction from Intraday Data*, Journal of Finance (1991) — đọc phần về độ lệch thời gian báo giá.
- **Giải thích:** tài liệu `pandas.merge_asof` và DuckDB `ASOF JOIN` — đọc kỹ tham số `direction`, `tolerance`, `by`.
- **Đào sâu:** Furgale, Rehder, Siegwart, *Unified Temporal and Spatial Calibration for Multi-Sensor Systems* (IROS 2013; công cụ Kalibr) — cách ước lượng độ lệch thời gian camera–IMU như một tham số.
- **Tự kiểm tra:** (1) giải thích cho backend engineer trong 5 câu vì sao "resample về 30 Hz" có thể tạo ra dao động không có thật; (2) vẽ lại hình mốc IMU/camera và bốn phương pháp; (3) câu hỏi:

  Một bảng ghép có cột `imu_age_ms`. Phân bố của nó cho as-of trên IMU 200 Hz đều đặn trông thế nào, và một đỉnh phụ ở ~100 ms nói gì?
  <details><summary>Đáp án</summary>

  Đều đặn: dồn trong 0–5 ms (với 200/30 thì chỉ ba giá trị lặp lại). Đỉnh ở ~100 ms: có lỗ hổng IMU (USB kẹt/rớt) và tolerance quá rộng hoặc không có — các frame đó đang mang mẫu cũ.

  </details>

---

## F3.5 — Idempotency, exactly-once, upload resumable, ngữ nghĩa object store (4h)

> **Dùng cho:** K3 Bài 14 · K5 Bài 14 · K6 Bài 9 · K7 C7.3 · **Cần trước:** F3.1; F2.5 (fault injection) nên có · **Sau viên nang này bạn đánh giá được:** một thiết kế upload có thật sự "không mất, không trùng" không, dưới những lỗi nào; điều kiện xóa file local có đủ chặt không; và một khẳng định về checksum/ETag có kiểm cái mình tưởng nó kiểm không.

### 1. Câu chuyện

Phần này đúng nghề bạn nhất; câu chuyện ngắn. Tới tháng 12/2020, Amazon S3 chỉ bảo đảm *eventual consistency* cho một số thao tác: một object vừa ghi có thể chưa hiện trong `LIST`. Các pipeline Hadoop/Spark ghi output lên S3 rồi liệt kê để đọc tiếp thỉnh thoảng thiếu file mà không báo lỗi. Netflix viết hẳn một công cụ (s3mper, 2014) chỉ để *phát hiện* listing không nhất quán `[chuẩn]`. Từ 12/2020, S3 bảo đảm strong read-after-write consistency cho mọi PUT/LIST `[spec: thông báo AWS 12/2020]`, và từ 8/2024 hỗ trợ ghi có điều kiện `If-None-Match: *` cho PutObject và CompleteMultipartUpload `[spec: AWS S3 User Guide, "conditional writes"]`. Ngữ nghĩa của object store **đổi theo thời gian và theo nhà cung cấp** (MinIO, GCS, R2 không giống hệt S3). Thiết kế upload của bạn dựa trên ngữ nghĩa nào phải được ghi ra và test, không được nhớ.

Phần robot thêm: đơn vị dữ liệu là **file nhiều GB vừa được ghi xong trên một ổ duy nhất**, đường mạng đứt là trạng thái bình thường, và bản local là bản sao duy nhất cho tới khi bản trên store được *chứng minh* đúng.

### 2. Mô hình tư duy

```mermaid
stateDiagram-v2
  [*] --> WRITING: writer mở file
  WRITING --> SEALED: finish() + fsync + sha256 + manifest
  WRITING --> RECOVER: crash (không có summary, F3.1)
  RECOVER --> SEALED: mcap recover → file mới, hash mới
  SEALED --> UPLOADING: tạo multipart, LƯU upload_id bền
  UPLOADING --> UPLOADING: part n xong → lưu (n, checksum) bền
  UPLOADING --> UPLOADED: Complete (If-None-Match: *)
  UPLOADED --> VERIFIED: checksum DO SERVER TÍNH == sha256 lúc SEALED
  VERIFIED --> [*]: được xóa local (khi cần chỗ)
  UPLOADED --> QUARANTINE: lệch checksum → giữ local, alert
```

Ba ý tưởng, mỗi cái đã có tên trong nghề bạn:

1. **Exactly-once không tồn tại trên đường truyền; effectively-once thì có**: at-least-once (retry tới khi chắc) + **thao tác idempotent** ở đích. Idempotent ở object store = cùng key, cùng nội dung, ghi lần hai không đổi gì.
2. **Key quyết định idempotency.** Key theo **nội dung** (sha256) thì retry vô hại và hai bản khác nội dung không bao giờ đè nhau. Key theo **tên** thì phụ thuộc chính sách ghi đè. Key **mới mỗi lần thử** (UUID) thì mọi response bị mất thành một bản trùng.
3. **Điểm commit phải đo được.** "Xóa local" là thao tác không đảo ngược, nên điều kiện của nó phải là một bằng chứng *do bên kia tạo ra* (checksum server tính trên bytes nó nhận), không phải một trạng thái *bên mình nghĩ* (đã gửi xong, HTTP 200).

Ngữ nghĩa object store cần nhớ (S3; kiểm lại với store bạn dùng `[tự đo]` cho MinIO):

| Thuộc tính | S3 | Hệ quả |
|---|---|---|
| PUT là nguyên tử cả object; không append, không ghi dở hiện ra | `[spec]` | Không có "object bị cắt" do mạng đứt giữa PUT — nhưng có object đúng bytes của một **file đã bị cắt từ trước** |
| Multipart: part 5 MiB–5 GiB (trừ part cuối), tối đa 10 000 part; object chỉ hiện khi Complete | `[spec]` | Resume = `ListParts` theo `upload_id`; part bỏ dở vẫn tính tiền tới khi Abort (đặt lifecycle rule) |
| ETag của object multipart **không phải MD5 của cả file** (dạng `md5-của-các-md5-N`) | `[chuẩn]` | So ETag với `md5sum` local luôn lệch; dùng checksum bổ sung (SHA-256/CRC) mà S3 tính và trả về, hoặc tải về băm lại |
| Cùng key: ghi sau thắng; `If-None-Match: *` → 412 nếu key đã có | `[spec]` | Key theo tên + không điều kiện = có thể đè; có điều kiện = bản đầu (có thể là bản hỏng) thắng mãi |
| Strong read-after-write từ 12/2020 | `[spec]` | `HEAD` ngay sau Complete là kiểm hợp lệ |

### 3. Cầu nối từ backend

| Backend bạn biết | Ở đây | Gãy ở chỗ | Nếu dùng nhầm thì |
|---|---|---|---|
| Idempotency key trên API thanh toán (Stripe-style), server nhớ key 24h | Key object = sha256 nội dung | Server thanh toán *nhớ* key và trả lại response cũ; object store không nhớ request, nó chỉ có trạng thái hiện tại của key. Idempotency phải nằm **trong cách đặt key**, không trong header | Gửi header `Idempotency-Key` lên S3 và tưởng được bảo vệ |
| Kafka EOS (KIP-98): producer idempotent + transaction, đọc–xử lý–ghi trong Kafka | Robot → object store qua mạng đứt | EOS chỉ bao phạm vi *bên trong Kafka*; hiệu ứng ra ngoài (gửi email, phát âm thanh, xóa file local) không quay lui được (đã chấm ở K3 Bài 14) | Coi "dùng hạ tầng có exactly-once" là xong cho cả bước xóa local |
| Outbox pattern: ghi DB + ghi outbox trong một transaction | Hàng đợi upload bền trên robot | Ở đây "transaction" cần cả **fsync file dữ liệu** và **fsync trạng thái hàng đợi**; thứ tự sai (ghi trạng thái SEALED trước khi file xuống đĩa) → mất điện để lại trạng thái nói dối | Sau mất điện, hàng đợi trỏ tới file 0 byte |
| Retry với backoff khi 5xx | Retry upload trên robot | Ổn; nhưng retry **sau khi mất response** của một PUT đã thành công là tình huống *phổ biến* trên Wi-Fi yếu, không phải hiếm | Key UUID → bản trùng tỉ lệ thuận với tỉ lệ mất response |

**Chấm mô hình:**

- *"Upload lại cùng file thì vô hại vì S3 ghi đè."* — **ĐÚNG MỘT PHẦN.** Vô hại nếu key xác định và nội dung giống. Gãy: (a) key sinh mới mỗi lần thử → trùng; (b) cùng key, nội dung khác (file được upload khi chưa SEALED, rồi upload lại bản đủ) → bản nào thắng phụ thuộc thứ tự và điều kiện ghi. Phản ví dụ: mục 5.
- Đã chấm ở nơi khác, không lặp: *"`upload_file()` trả về thành công thì xóa local được"* — **SAI** (K5 Bài 14); *"Exactly-once là bài toán đã có lời giải"* — **ĐÚNG MỘT PHẦN** (K3 Bài 14).

**Tên chuẩn của thứ bạn đã làm:** dedupe theo hash nội dung khi import dữ liệu là **content-addressable storage** (git, Docker registry, Bazel cache đều dựa trên nó). Còn thiếu ở robot: định nghĩa *nội dung* là file **đã niêm phong**, và hash được tính **một lần lúc SEALED** rồi đi kèm file như danh tính của nó suốt vòng đời (→ F3.8).

### 4. Thuật ngữ

| Mức | Thuật ngữ | Nghĩa trong một câu | Hay bị hiểu nhầm thành |
|---|---|---|---|
| 🟢 | At-least-once / at-most-once / effectively-once | Có thể trùng / có thể mất / trùng nhưng vô hại nhờ idempotent | "Exactly-once" end-to-end |
| 🟢 | Idempotent | Làm hai lần = làm một lần | Retry an toàn trong mọi trường hợp |
| 🟢 | Multipart upload, `upload_id`, `ListParts` | Upload theo phần, resume được | Tự resume |
| 🟢 | Conditional write (`If-None-Match`, `If-Match`) | Ghi chỉ khi key chưa có / đang đúng phiên bản | Khóa phân tán |
| 🟢 | Content addressing | Key = hash nội dung | Chỉ để dedupe |
| 🟢 | Seal / niêm phong | File đóng, fsync, hash xong, không đổi nữa | "Writer đã thoát" |
| 🟡 | ETag multipart, checksum bổ sung (SHA-256, CRC) | Định danh phiên bản / bằng chứng toàn vẹn | ETag = MD5 file |
| 🟡 | Lifecycle rule, abort incomplete multipart | Dọn part bỏ dở | — |
| 🔴 | Giao thức tus | Upload resumable qua HTTP chung | — |

### 5. Bài tập dự đoán

Một object store đồ chơi (dict) có ghi có điều kiện (`setdefault` ≈ `If-None-Match: *`). Mỗi lần PUT: 10% mất trước khi tới store, 5% **store đã ghi nhưng response mất**. Client retry tới khi thấy 200. 2 000 file; 5 file bị đẩy lên lần đầu khi writer **chưa đóng** (bản bị cắt một nửa), sau đó lượt chính đẩy toàn bộ bản đúng. Ba cách đặt key: UUID mỗi lần thử, tên file, sha256 nội dung.

**Dự đoán:**

1. Kỳ vọng số bản trùng với key UUID? (Gợi ý: mỗi lần thử có ba kết cục; số lần "đã ghi nhưng mất response" trước lần thành công đầu tiên có kỳ vọng p_after / p_success.)
2. Key theo tên + ghi có điều kiện: bao nhiêu file mất bản đúng? Nếu bỏ điều kiện (ghi sau thắng) thì sao?
3. Key sha256: số object? Có bản trùng không? Thứ gì còn thừa trên store và phát hiện bằng gì?

```python
# [đã chạy] Retry + cách đặt key quyết định trùng lặp và hỏng âm thầm
import hashlib, random, uuid
random.seed(11)
P_LOST_BEFORE, P_LOST_AFTER = 0.10, 0.05   # request mất trước khi tới store / store đã ghi, response mất

def put(store, key, body):
    r = random.random()
    if r < P_LOST_BEFORE: raise TimeoutError
    store.setdefault(key, body)             # ghi có điều kiện kiểu If-None-Match: * (key có rồi thì giữ bản cũ)
    if r < P_LOST_BEFORE + P_LOST_AFTER: raise TimeoutError
    return 200

def upload(store, name, body, key_of):
    n = 0
    while True:                              # retry tới khi thấy 200, cùng hàm sinh key
        n += 1
        try: put(store, key_of(name, body), body); return n
        except TimeoutError: pass

full = {f"robot01/2026-11-02/{i:05d}.mcap": f"mcap-{i}|".encode() * 50 for i in range(2000)}
early = [n for i, n in enumerate(full) if i % 400 == 399]   # 5 file bị đẩy lên khi writer CHƯA đóng

keys = {"uuid mỗi lần thử": lambda n, b: str(uuid.uuid4()),
        "tên file":         lambda n, b: n,
        "sha256 nội dung":  lambda n, b: hashlib.sha256(b).hexdigest()}
for label, key_of in keys.items():
    store, tries = {}, 0
    for n in early: tries += upload(store, n, full[n][: len(full[n]) // 2], key_of)   # bản bị cắt
    for n, b in full.items(): tries += upload(store, n, b, key_of)                    # lượt chính
    by_content = {}
    for v in store.values(): by_content[v] = by_content.get(v, 0) + 1
    dup = sum(c - 1 for c in by_content.values())
    lost = sum(1 for n, b in full.items() if b not in by_content)       # bản đúng không có trên store
    print(f"{label:17s}| lần thử {tries} | object {len(store)} | bản trùng {dup} | file mất bản đúng {lost}")
```

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

| Key | Lần thử | Object | Bản trùng | File mất bản đúng |
|---|---|---|---|---|
| UUID mỗi lần thử | 2 344 | 2 115 | **110** | 0 |
| Tên file | 2 386 | 2 000 | 0 | **5** |
| sha256 nội dung | 2 342 | 2 005 | 0 | 0 |

1. Kỳ vọng 2 005 × 0,05/0,85 ≈ **118**; ra 110 (dao động thống kê). Tỉ lệ trùng = tỉ lệ mất response / tỉ lệ thành công — nó không giảm khi bạn retry "cẩn thận hơn".
2. **5 file**: bản bị cắt tới trước, giành key, bản đúng bị 412 (ở đây: `setdefault` giữ bản cũ) mãi mãi, mọi request đều "thành công". Bỏ điều kiện thì lần này bản đúng đè lên — nhưng chỉ vì nó tới sau; đảo thứ tự (retry của bản cũ tới muộn) thì bản hỏng đè bản đúng. Key theo tên chỉ an toàn khi **chỉ file đã SEALED mới được vào hàng đợi** và có kiểm checksum sau Complete.
3. **2 005 object**, không trùng; 5 object thừa là bản bị cắt, **mồ côi** (không manifest nào trỏ tới). Phát hiện bằng đối soát store ↔ manifest (job gom rác), và chúng không bao giờ che bản đúng. Cách sửa gốc vẫn là cấm upload trước SEALED.

</details>

### 6. Lăng kính đánh giá

Checklist cho một thiết kế upload/ingest:

1. Đơn vị upload là gì, và **trạng thái nào** của nó được phép vào hàng đợi (SEALED hay "file tồn tại")?
2. Key đặt thế nào? Retry sau khi **mất response** tạo ra gì?
3. Ngữ nghĩa store giả định (ghi đè, điều kiện, consistency) có được **ghi ra và test** trên đúng store (S3/MinIO/khác) không?
4. Điều kiện xóa local là bằng chứng **do server tạo** (checksum server tính) hay trạng thái **phía mình** (200 OK, đã gửi đủ byte)?
5. Trạng thái hàng đợi và file được fsync theo **thứ tự** nào? Mất điện ở giữa hai bước để lại gì?
6. Phần bỏ dở (multipart chưa Complete, object mồ côi) được dọn bằng gì?
7. Lỗi nào đã được **tiêm thật** (mất mạng, mất response, mất điện, đĩa đầy) và mỗi lỗi bao nhiêu lần (→ F1.4: 10 lần thành công không chứng minh tỉ lệ hỏng nhỏ)?

**Khẳng định mẫu để tự chấm:**

- (a) Gemini, K5 Bài 14, "Nếu kết quả ra khác": *"[ETag multipart không khớp] → Tính toán và so sánh SHA-256 metadata bằng cách gắn custom header `x-amz-meta-sha256` lúc khởi tạo upload."*
- (b) Gemini, K5 Bài 14, "Số phải ra": *"Ngắt mạng giữa lúc upload: không bao giờ upload lại từ đầu; tiếp tục chính xác từ part chưa hoàn thành."*
- (c) *"Đặt key là `robot01/2026-11-02/00042.mcap` là idempotent rồi, retry bao nhiêu cũng được."*

<details><summary>🔒 MỞ SAU KHI COMMIT prediction.md</summary>

- (a) **SAI như một phép kiểm toàn vẹn.** `x-amz-meta-*` là user metadata: server lưu nguyên chuỗi client gửi, **không tính hay đối chiếu** gì. So "metadata sha256" với sha256 local là so client với chính nó. Phép kiểm thật: dùng checksum bổ sung mà S3 *tự tính* trên bytes nhận được (SHA-256/CRC32/CRC64NVME tùy loại; với multipart có dạng tổng hợp theo part hoặc full-object tùy thuật toán `[spec: S3 User Guide, "Checking object integrity" — kiểm theo SDK bạn dùng]`), hoặc tải về và băm lại. Ghi sha256 vào metadata vẫn hữu ích — làm *danh tính* để đối chiếu sau, không làm bằng chứng.
- (b) **ĐÚNG MỘT PHẦN.** Đúng là mục tiêu và làm được bằng `upload_id` lưu bền + `ListParts`. Gãy: part đã lên nhưng crash trước khi lưu trạng thái → upload lại part đó (vô hại, cùng số part ghi đè); `upload_id` có thể đã bị lifecycle rule abort nếu robot offline lâu → phải bắt đầu lại từ đầu, và thiết kế phải coi đó là hợp lệ, không phải lỗi. "Không bao giờ" là tiêu chí test cho kịch bản ngắt mạng ngắn, không phải bất biến.
- (c) **ĐÚNG MỘT PHẦN.** Idempotent khi nội dung dưới key đó không bao giờ đổi — tức chỉ file đã SEALED được upload, và tên không bị tái dùng (ví dụ bộ đếm file reset sau khi cài lại OS, hai robot cùng ID). Phản ví dụ: mục 5, 5 file mất bản đúng mà mọi request đều thành công. Thêm sha256 vào key hoặc kiểm checksum sau Complete để đóng lỗ này.

</details>

### 7. Câu hỏi ngược

1. **[Quy mô]** Robot ghi 24 GB/ngày, mất mạng 3 ngày, ổ còn trống 100 GB. Tính bằng định luật Little (→ F7.1) lượng dữ liệu trong hàng đợi và thời gian xả khi có mạng lại ở 20 MB/s. Cái gì gãy trước?
   <details><summary>Hướng nghĩ</summary>

   72 GB tồn sau 3 ngày; xả 72 GB ở 20 MB/s ≈ 1 giờ, *trong lúc* vẫn ghi thêm ~1 GB/giờ. Ổ chịu được ~4 ngày. Ngày thứ 5 cần chính sách drop/retention theo ưu tiên (F3.9), quyết định trước, không lúc 3h sáng.

   </details>
2. **[Failure mode]** Mất điện đúng lúc giữa "đổi trạng thái thành VERIFIED" và "xóa file". Khởi động lại thấy gì, làm gì? Ngược lại: xóa file rồi mới ghi trạng thái?
   <details><summary>Hướng nghĩ</summary>

   Thứ tự đúng: ghi VERIFIED bền → xóa → ghi DELETED. Crash ở giữa: thấy VERIFIED + file còn → xóa lại (idempotent). Thứ tự ngược: thấy file mất + trạng thái UPLOADED → không biết đã verify chưa. Đây là write-ahead logging cho một thao tác hệ thống file.

   </details>
3. **[Vì sao không]** Vì sao không dùng `rsync` hay `rclone` thay cho tự viết uploader?
   <details><summary>Hướng nghĩ</summary>

   Có thể, và thường nên. Câu hỏi đúng: công cụ đó có (a) chỉ lấy file đã SEALED, (b) kiểm checksum phía server, (c) báo trạng thái để bước xóa dựa vào không? `rclone` có `--checksum` và hỗ trợ hash theo backend `[tự đo]`. Tự viết chỉ khi không ghép được ba điều đó.

   </details>
4. **[Liên ngành]** Ngân hàng chuyển tiền liên ngân hàng dùng số tham chiếu duy nhất và đối soát cuối ngày. Giống quy trình robot→store ở đâu?
   <details><summary>Hướng nghĩ</summary>

   Key duy nhất (idempotency) + đối soát độc lập (reconciliation) giữa hai sổ = sha256 + job đối soát manifest ↔ store. Khác: ngân hàng có thể đảo giao dịch; robot không tạo lại được dữ liệu đã xóa.

   </details>

### 8. Liên kết ra ngoài

- **Docker registry / OCI:** layer định danh bằng digest sha256; push lại layer đã có là no-op. Giống content addressing ở đây. Khác: registry kiểm digest phía server khi nhận — đúng thứ bạn cần đòi hỏi ở bước VERIFIED.
- **Thư viện số (LOCKSS, "Lots Of Copies Keep Stuff Safe"):** nhiều bản ở nhiều nơi, định kỳ so hash để phát hiện mục nát bit. Giống: niềm tin vào dữ liệu đến từ đối chiếu độc lập. Khác: họ bảo quản hàng thập kỷ; robot chỉ cần tới khi bản trên store được xác minh.

### 9. Áp vào khóa chính

- **K3 Bài 14:** khóa dedupe là danh tính ổn định của *ý định* (confession ID), không phải hash nội dung có thể sửa; F3.5 cho bạn từ vựng để phân biệt hai trường hợp.
- **K5 Bài 14:** dùng sơ đồ trạng thái mục 2 làm thiết kế; test đủ bốn lỗi (mất mạng, **mất response**, mất điện, đĩa đầy); điều kiện xóa = checksum server tính khớp sha256 lúc SEALED.
- **K6 Bài 9:** output 10 000 episode đặt key theo hash nội dung, manifest trỏ tới; chạy lại job không nhân đôi artifact.
- **K7 C7.3:** sidecar trên robot thật; đo tỉ lệ mất response trên Wi-Fi văn phòng để biết UUID-key sẽ đẻ bao nhiêu bản trùng.

### 10. Độ tin cậy

| Khẳng định | Nhãn | Ghi chú / cách kiểm |
|---|---|---|
| S3 strong consistency từ 12/2020 | `[spec]` | Thông báo AWS "Amazon S3 now delivers strong read-after-write consistency" |
| `If-None-Match` cho PutObject/CompleteMultipartUpload, 412 khi key có | `[spec]` | AWS S3 User Guide, conditional writes (8/2024) |
| Giới hạn multipart 5 MiB/10 000 part | `[spec]` | AWS S3 User Guide, multipart upload limits |
| Checksum bổ sung, full-object CRC cho multipart | `[spec — kiểm theo SDK]` | AWS S3 User Guide, "Checking object integrity" |
| MinIO hỗ trợ đủ các ngữ nghĩa trên | `[tự đo]` | Test trực tiếp ở K5 Bài 14 |
| Số trong bảng mục 5 | `[đã chạy]` | Mô phỏng |

### 11. Đọc thêm và tự kiểm tra

- **Nguồn gốc:** AWS S3 User Guide — các mục *Uploading and copying objects using multipart upload*, *Checking object integrity*, *conditional writes*.
- **Giải thích:** Kleppmann, *DDIA* chương 11, mục "Fault Tolerance" (exactly-once, idempotence) và chương 12, mục "The end-to-end argument for databases".
- **Đào sâu:** Saltzer, Reed, Clark, *End-to-End Arguments in System Design* (1984) — vì sao kiểm toàn vẹn phải làm ở hai đầu cuối, đúng lý do bước VERIFIED tồn tại.
- **Tự kiểm tra:** (1) giải thích cho backend engineer trong 5 câu vì sao 200 OK không phải điều kiện xóa; (2) vẽ lại sơ đồ trạng thái từ trí nhớ; (3) câu hỏi:

  Mỗi lần thử PUT có 3% mất response sau khi store đã ghi, 87% thành công. Dùng key UUID cho 10 000 file, kỳ vọng bao nhiêu bản trùng?
  <details><summary>Đáp án</summary>

  10 000 × 0,03 / 0,87 ≈ **345**. Không phụ thuộc số lần retry tối đa, chỉ phụ thuộc tỉ lệ hai kết cục.

  </details>

---
