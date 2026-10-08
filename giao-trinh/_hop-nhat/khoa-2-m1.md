# Nhật ký hợp nhất — Khóa 2 · Module 1 + 00-tong-quan (đơn vị m-k2a)

Đầu vào: `giao-trinh/khoa-2/m1-mcap-cong-cu.md` (Claude: Bài 1–3), `giao-trinh-kiro/khoa-2/m1-mcap-cong-cu.md` (Kiro: Bài 1–8b + Gate), `giao-trinh-kiro/khoa-2/00-tong-quan.md`. Nguồn gốc: `khoa-2-du-lieu-robot-khong-can-robot.md` dòng 1–677, 1142–1199.

Môi trường kiểm: venv riêng `_scratch/m-k2a/venv` với mcap 1.5.0, mcap-protobuf-support 0.5.4, mcap-ros2-support 0.5.7, protobuf 7.36.2, rerun-sdk 0.38.1, grpcio-tools 1.84.0; MCAP CLI Rust 0.3.0 build từ `foxglove/mcap` (HEAD 7/10/2026). Mọi khối `# [đã chạy]` của bản cuối đã chạy lại; hai khối đọc `data/example-006-arm-gazebo.mcap` chạy trên một file ROS 1 tổng hợp cùng cấu trúc (file `data/` không có trong repo này), số liệu `example-006` giữ theo Kiro, ghi "đã đo (máy có `data/`)".

## Phần đầu file
- Nền: K (bảng requirements, bảng dữ liệu) + C (đối chiếu code của người học).
- Mâu thuẫn: C ghi CLI "build từ source `go/cli/mcap`"; K ghi CLI Rust. Kiểm repo: `go/` không còn `cli`, CLI ở `rust/cli` (mcap-cli 0.3.0), docs `cargo build -p mcap-cli`. → K đúng.
- Thêm: đường lui khi không có `data/` (gitignore).

## Bài 1
- Bản nền: C. Vì: overhead 31 B + 16 B mỗi message (đúng spec, đổi kết luận về luồng nhỏ), mô hình ngân sách chạy được, chấm `sequence` ≈ idempotency key.
- Ghép từ K: bước tùy chọn đo `example-006` (point cloud nặng nhất, 95 %/5 % đúng với ảnh raw), IMU gói thô vs `sensor_msgs/Imu` 324 B, "một topic nhiều channel", câu hỏi "vì sao không mỗi cảm biến một file", liên kết observability.
- Mâu thuẫn: không có mâu thuẫn số; hai bên dùng tham số khác nhau (C: IMU 1 kHz 50 B; K: 200 Hz 320 B) — giữ C, thêm ghi chú K.
- Lỗi kỹ thuật: K dùng đường dẫn Windows `r"data\..."` → `"data/..."`. Kiểm thêm: `mcap du src/imu.mcap` cho MessageIndex 25,1 % byte, khớp khẳng định của C.

## Bài 2
- Bản nền: C. Vì: thuật ngữ đồng hồ chuẩn (offset/skew/drift), mô phỏng ba bệnh, giả thuyết hàng đợi phình (Little), chấm mô hình K3 lượt 21.
- Ghép từ K: Patriot đủ chi tiết (687 m, 28 người), Cloudflare 2017/Go 1.9, phép tính 10 ms → 5 mm / 5,5 px, độ phân giải float32, bài đọc timestamp `example-006` (latched 48,7 s, 23 chỗ `log_time` không tăng, frame RGB mang tên depth), câu hỏi chunk overlap khi NTP step, câu hỏi `millis()` tràn 49,7 ngày, dòng cầu nối "timestamp dùng để ghép phép đo vật lý".
- Mâu thuẫn sự thật: K định nghĩa "skew = lệch hệ thống (offset), drift = tốc độ skew đổi (ppm)"; C theo Mills/NTP: offset = lệch pha, skew = lệch tần số, drift = thay đổi của skew. → Chọn C (khớp quy chuẩn F4.1, K5).
- Lỗi đã sửa: C ghi "số dt ≈ 3T: thỉnh thoảng 1" — chạy seed 1–5 ra 0–2 → sửa. C câu A1 "3 lần rớt đôi nhiều hơn kỳ vọng" thêm điều kiện "nếu tổng chỉ vài nghìn frame".
- Cắt chữ độn để giữ ~4.600 từ phần chữ: bỏ dòng cầu nối tracing/p99 trùng ý, câu hỏi cửa sổ watermark (đã nằm trong chấm mô hình), câu GPS, TrueTime, bước kiểm đồng hồ máy mình.

## Bài 3
- Bản nền: C. Vì: REP-145, chứng minh comment Protobuf không vào FileDescriptorSet (đã kiểm: `source_code_info` vắng), chấm "frame" của K3 lượt 7.
- Ghép từ K: đồ chơi transform 4×4 (đúng chuỗi / quên optical / nhân ngược — đã chạy, (2,1;0;0,2) / (0,1;0;2,2) / (2,2;−0,1;0)), dự đoán IMU gắn nghiêng 90°, `/tf_static` latched, `frame_id` như foreign key có thời gian, câu hỏi camera lệch 5°, sửa "`world` không thuộc REP-105".
- Mâu thuẫn: không. Ma trận optical→link của hai bản trùng nhau (kiểm bằng code).

## Bài 4 (chỉ K có)
- Bản nền: K. Kiểm: walk.py chạy đúng (2 chunk, 2 MessageIndex, 2 ChunkIndex, 6 SummaryOffset), Footer 29 B, "Schema/Channel MUST có trong summary" đúng spec dòng 242, overlap là dòng của CLI (`info.rs`).
- Sửa/ghép: viết lại chấm mô hình theo đề "MCAP chỉ là Kafka trong một file" (→ F3.1) với 4 chỗ gãy và phản ví dụ đo được; thêm kết quả CLI thật: % nén CLI in là **phần giảm** (61,57 %), `info` trên file cắt `Bad magic number` exit 1, `doctor` thiếu DataEnd/Footer.

## Bài 5 (chỉ K)
- Bản nền: K. Đã chạy lại: 12 000 msg, 3 chunk, 59,995 s, nén 3,17×, round-trip bằng từng bit; `src/imu.mcap` cũ 2,6×, `sequence` record = 0.
- Lỗi đã sửa: script K ghi `imu.mcap` từ `src/` → **ghi đè** `src/imu.mcap` mà bước 8 còn dùng làm đối chứng → đổi thành `imu_b5.mcap` (kéo theo Bài 8, 8b). Payload cũ 82–93 B (K ghi 82–89). Quy tắc gencode vs runtime protobuf ghi rõ (grpcio-tools 1.84 sinh 7.35.1, chạy với runtime 7.36.2).

## Bài 6 (chỉ K)
- Bản nền: K. Đã chạy 4 test + 2 canary + thí nghiệm phá vỡ bằng proto v2/v3/v4 tự sinh: `DecoderFactory` đọc `temperature_c = 31.5`; v1 đọc v2 giữ byte lạ; `HasField` không `optional` ném `ValueError`; int64 → uint32: `-1 → 4294967295`, `2**32+7 → 7`; `double → float`: v1 đọc `z = 0.0` không exception; JSON `calibrationId`. Tất cả khớp K. Không sửa.

## Bài 7 (chỉ K)
- Bản nền: K. Đã chạy: speedup 144× / 68× / 12×, cứu 80,0 / 77,4 / 59,0 %, `make_reader` ném `RecordLengthLimitExceeded`. Thêm số `mcap recover` thật (8 476/12 000, exit 3). Liên kết "K5 Bài 17" → `K5 Bài 14` + `K5 Bài 17`.

## Bài 8 (chỉ K, rút gọn)
- Thiếu "Chấm mô hình" trong phần 3 → thêm (chấm câu bản gốc "Foxglove hiện đúng → writer đúng": ĐÚNG MỘT PHẦN). Rerun 0.38.1 chạy được.

## Bài 8b (chỉ K)
- Đã chạy converter: 324 B CDR, file 0,94 MB < 1,0 MB, nén 5,73×, 5 khóa metadata, sai lệch 0. Thêm liên kết `→ K5 Bài 13`, `→ K7 C7.3`.

## Gate M1 (chỉ K)
- Giữ tiêu chí, giờ 22h/trần 32h. Sửa: đường dẫn parquet pusht; thêm lựa chọn (c) `lerobot/robomme` (đã có script tải của người học); nêu lệch câu chữ "≥2 nguồn" (file khóa) vs "≥2 dataset công khai" (`00-lo-trinh-tong.md` M2) và cách thỏa cả hai.

## 00-tong-quan
- Nền: K. Bảng Module 2 lấy tên bài, "Cần trước" và quyết định từ dòng Vị trí của bản Kiro `m2-dataset-audit.md` (bảng trong 00 của Kiro đã lệch tên với chính file m2 của Kiro). Sửa F-link Bài 2 (thêm F4.1), mermaid M2, CLI, dữ liệu `data/` là tùy chọn, ghi chú điều kiện song song K7 C0–C2, thêm dòng sửa lỗi của đợt hợp nhất.

## Nhận xét hai bản
- Claude mạnh ở bản chất và thuật ngữ chuẩn (overhead/message, offset/skew/drift, Little), dùng code của người học làm bằng chứng.
- Kiro mạnh ở thực nghiệm đo được trên file thật và ở bẫy API (reader cũ = golden file, `optional`, đổi kiểu sai âm thầm, `make_reader` ném lỗi), pin phiên bản. Yếu: đường dẫn Windows, script ghi đè file đối chứng, dùng dữ liệu `data/` không có trong repo, skew/drift lệch chuẩn.
