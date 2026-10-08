# TRẠNG THÁI CÔNG VIỆC — bàn giao cho session sau

> **CẬP NHẬT 2026-10-08 (session 2):** đã thống nhất với bản Kiro. Đọc `_PHOI-HOP.md` trước. Tên file đã đổi theo mục 8 quy chuẩn (bảng dưới còn tên cũ). K7 đã có kế hoạch chốt `khoa-7/_KE-HOACH-K7.md` (mục 3 dưới đây đã lỗi thời). Tiến độ mới ở mục 6 cuối file.

> Cập nhật: 2026-10-08 12:50 UTC. Branch: `claude/kind-newton-m2ocmb`.
> Đọc file này **trước tiên** khi mở session mới. Nó đủ để tiếp tục mà không làm lại phần đã xong.

## 0. Bối cảnh trong 10 dòng

- Người học: backend 8 năm chuyển sang robotics data infra. Lộ trình 7 khóa (`khoa-*.md` ở gốc repo) + bản detail cũ do Gemini viết (`detail/`, chất lượng thấp).
- Yêu cầu: **soạn lại toàn bộ bài detail** K1–K7 và **soạn mới 7 khóa nền F1–F7**, theo hợp đồng `giao-trinh/_QUY-CHUAN.md`. Hợp đồng gồm khung 12 phần, niêm phong đáp án, "Gãy ở chỗ", nhãn tin cậy, chấm mô hình ĐÚNG / ĐÚNG MỘT PHẦN / SAI, dạng không phải chữ, và danh sách lỗi đã biết ở mục 7.
- Cách làm: mỗi **đơn vị** (một phần của một khóa, hoặc một khóa F) do một subagent soạn theo `giao-trinh/_ref/brief-writer.md` (khóa F đọc thêm `_ref/brief-F.md`). Sau đó một **reviewer độc lập** kiểm và sửa tại chỗ theo `_ref/brief-reviewer.md`. Người điều phối viết `giao-trinh/README.md` ở cuối.
- `_ref/cau-hoi-cua-ban-trong-gemini.md`: câu hỏi thật của người học trích từ hội thoại Gemini. Giáo trình phải chấm các mô hình người học tự xây trong đó.
- Bài học vận hành:
  - Máy có 4 CPU nên Workflow tool chỉ chạy 2 agent song song. Agent tool cho tối đa 20.
  - Chạy 20 agent cùng lúc làm **hết usage của gói rất nhanh**: đã 2 lần bị rate limit, các agent chết giữa chừng.
  - **Khuyến nghị: chạy ≤5–6 agent một lượt.**
- Agent viết dần (Write rồi Edit nối thêm). Vì vậy file dở dang vẫn dùng được: **mọi bài đang có trong file đã đủ 12 phần** (đã kiểm bằng script lúc 12:50). Phần còn thiếu là các bài *chưa có*.

## 1. Bảng trạng thái theo đơn vị

Ký hiệu: ✅ xong · 🟡 dở (có bài, thiếu bài) · ⬜ chưa bắt đầu · ⏸ tạm dừng chờ quyết định.
"Nguồn" = dòng trong file khóa gốc ở gốc repo.

| Đơn vị | File đầu ra (trong `giao-trinh/`) | Đã có | **Còn thiếu** | Nguồn |
|---|---|---|---|---|
| k1a | `khoa-1/00-tong-quan.md` | — | **cả file** | khoa-1 dòng 1–62, 843–902 |
| k1a | `khoa-1/a-nen.md` | Bài 1–3 ✅ | — | khoa-1 dòng 63–229 |
| k1a | `khoa-1/b-dung-cu.md` | Bài 4–6 | **Bài 7, 8** | khoa-1 dòng 396–478 |
| k1b | `khoa-1/c-do-that.md` | Bài 9–11 ✅ | — | |
| k1b | `khoa-1/d-du-lieu-tren-day.md` | Bài 12 | **Bài 13, Bài 14 (Gate K1)** | khoa-1 dòng 783–863 |
| k2a | `khoa-2/00-tong-quan.md` | — | **cả file** | khoa-2 dòng 1–33, 1142–1199 |
| k2a | `khoa-2/m1-mcap-cong-cu.md` | Bài 1–3 | **Bài 4, 5, 6, 7, 8, 8b, Gate M1** | khoa-2 dòng 182–677 |
| k2b | `khoa-2/m2-dataset-audit.md` | Bài 9–12 | **Bài 13, 14, 15, Gate M2** | khoa-2 dòng 1049–1155 |
| k3a | `khoa-3/00-tong-quan.md` | — | **cả file** | khoa-3 dòng 1–58, 1004–1095 |
| k3a | `khoa-3/m1-chuoi-phat.md` | Bài 1–4 | **Bài 5, 6, 7** (Bài 7 phải sửa SNR theo mục 7 quy chuẩn; Bài 6 chấm mô hình K3 lượt 11–13) | khoa-3 dòng 383–576 |
| k3b | `khoa-3/m2-do-do-tre.md` | Bài 8–10 ✅ | — | |
| k3b | `khoa-3/m3-tts.md` | Bài 11, 12 | **Bài 13** | khoa-3 dòng 824–857 |
| k3c | `khoa-3/m4-he-thong-v1.md` | Bài 14–17 + Gate ✅ | — | |
| k4a | `khoa-4/00-tong-quan.md` | — | **cả file** | khoa-4 dòng 1–53, 785–875 |
| k4a | `khoa-4/m1-nen-tang.md` | Bài 1–3 ✅ | — | |
| k4a | `khoa-4/m2-harness.md` | — | **Bài 4, 5, 6** (Bài 6: N100 không có HT; chứng minh cô lập nhiệt bằng số) | khoa-4 dòng 242–396 |
| k4b | `khoa-4/m3-chat-luong.md` | Bài 7–9 ✅ | — | |
| k4b | `khoa-4/m4-nhieu-model-target.md` | Bài 10 | **Bài 11, 12** (Bài 12 bắt buộc sửa N100 FLOPS và "batch 1 compute-bound", mục 7) | khoa-4 dòng 573–669 |
| k4c | `khoa-4/m5-publish.md` | Bài 13–15 + Gate ✅ | — | |
| k5a | `khoa-5/00-tong-quan.md` | — | **cả file** | khoa-5 dòng 1–23, 898–993 |
| k5a | `khoa-5/m0-chon-phan-cung.md` | Bài 1–2 ✅ | — | |
| k5a | `khoa-5/m1-cam-bien.md` | Bài 3, 4 | **Bài 5, 6** | khoa-5 dòng 245–338 |
| k5b | `khoa-5/m2-dong-bo-thoi-gian.md` | Bài 7–9 | **Bài 10, 11, 12** (Bài 10 sửa hệ số thạch anh; Bài 11 sửa công thức rolling shutter, mục 7) | khoa-5 dòng 518–643 |
| k5c | `khoa-5/m3-data-stack.md` | Bài 13–15 | **Bài 16, 17** | khoa-5 dòng 751–830 |
| k5c | `khoa-5/m4-van-hanh.md` | — | **Bài 18, 19, Gate K5** | khoa-5 dòng 831–931 |
| k6a | `khoa-6/00-tong-quan.md` | — | **cả file** | khoa-6 dòng 1–69, 939–1033 |
| k6a | `khoa-6/m1-determinism.md` | Bài 1–4 ✅ | — | |
| k6a | `khoa-6/m2-kich-ban.md` | — | **Bài 5, 6, 7** | khoa-6 dòng 262–392 |
| k6b | `khoa-6/m3-quy-mo.md` | Bài 8–10 ✅ | — | |
| k6b | `khoa-6/m4-danh-gia.md` | Bài 11 | **Bài 12, 13, 14** | khoa-6 dòng 548–686 |
| k6c | `khoa-6/m5-sim-to-real.md` | Bài 15, 16 | **Bài 17** | khoa-6 dòng 836–874 |
| k6c | `khoa-6/m6-ci-publish.md` | — | **Bài 18, 19, Gate K6** | khoa-6 dòng 875–970 |
| F1 | `nen-tang/F1-do-luong-thong-ke.md` | — | **cả file** (F1.1–F1.7) | |
| F2 | `nen-tang/F2-kiem-thu-danh-gia.md` | — | **cả file** (F2.1–F2.8) | |
| F3 | `nen-tang/F3-du-lieu-xu-ly-luong.md` | — | **cả file** (F3.1–F3.9) | |
| F4 | `nen-tang/F4-thoi-gian-dong-ho.md` | — | **cả file** (F4.1–F4.8) | |
| F5 | `nen-tang/F5-nhung-thoi-gian-thuc-tin-hieu.md` | — | **cả file** (F5.1–F5.8) | |
| F6 | `nen-tang/F6-mo-hinh-mo-phong-vv.md` | — | **cả file** (F6.1–F6.8) | |
| F7 | `nen-tang/F7-hieu-nang-van-hanh.md` | — | **cả file** (F7.1–F7.7) | |
| K7 | `khoa-7/*` | 7a Bài 1–4, 7b Bài 6–9, 7c-7d Bài 11–15 + Gate 7C, 7e Bài 18, 19, 19b | ⏸ **chờ thiết kế lại** (mục 3) | |
| — | `giao-trinh/README.md` | — | **cả file**, viết cuối cùng | |
| Review | mọi file | — | ⬜ **chưa reviewer nào chạy** | `_ref/brief-reviewer.md` |

Đã viết tổng cộng khoảng 410 nghìn từ, 27 file. Chưa có file nào qua reviewer.

## 2. Cách tiếp tục (không làm lại phần đã xong)

Với mỗi dòng có **Còn thiếu**, giao một subagent với prompt mẫu sau:

```
Đọc trọn giao-trinh/_ref/brief-writer.md (khóa F: đọc thêm giao-trinh/_ref/brief-F.md) và làm đúng theo đó.
ĐƠN VỊ <mã> — chỉ soạn phần CÒN THIẾU: <danh sách bài>.
File đầu ra: <đường dẫn>. File đã có các bài <…>: ĐỌC để giữ giọng văn, cách đánh số và liên kết chéo,
KHÔNG sửa và KHÔNG viết lại các bài đó. Nối bài mới vào cuối file (hoặc tạo file nếu chưa có).
Nguồn: <file khóa gốc + dòng>. Bản Gemini (nếu có): detail/Gemini-khóa N-*.md, grep "Bài N".
Scratchpad: thư mục scratchpad riêng của bạn trong session.
<gợi ý riêng của đơn vị ở mục 4>
```

`00-tong-quan.md` của mỗi khóa: giao cho agent của phần đầu khóa, viết **sau khi** các bài của khóa đã đủ. Nhờ vậy bảng "Bài → giờ → viên nang → quyết định" và danh sách sửa lỗi lấy được từ phần 11 thật của từng bài.

Thứ tự đề xuất, mỗi lượt ≤5–6 agent:
1. Bài còn thiếu K1–K6 (16 việc nhỏ, mỗi việc 1–3 bài).
2. F1–F7.
3. `00-tong-quan.md` của K1–K6.
4. Reviewer theo đơn vị (`_ref/brief-reviewer.md`), mỗi reviewer chỉ sửa file của đơn vị mình.
5. README tổng.
6. K7, sau khi người học chốt mục 3.

## 3. Khóa 7 — đang chờ người học quyết định

Phản hồi của người học: K7 hiện rời rạc và vô dụng với beginner ("còn đang học cách bật tắt mỏ hàn"). Toàn bộ công đoạn thiết bị, tháo lắp, đi dây, setup và lưu ý đều bị bỏ qua; khái niệm được viết cho người đã quen việc. Người học muốn K7 thành **khóa thực hành vừa build vừa học**: dựng robot thật để hiểu sâu nội dung K1–K6 cộng lại. Họ chấp nhận K7 có thể lớn gấp nhiều lần.

Các file `khoa-7/*.md` hiện có viết theo **cấu trúc cũ** (7A–7E). Chỉ dùng làm **nguyên liệu** cho các bài khái niệm (PID, odometry, Kalman, FAR/FRR, FMEA, HIL…), không phải bản cuối.

Đề xuất đã gửi người học (chưa được duyệt):

| Chặng | Làm ra được | Khái niệm học kèm |
|---|---|---|
| 0. Xưởng và an toàn | Bàn làm việc, nguồn bàn giới hạn dòng, an toàn pin LiPo | K1, F5.7 |
| 1. Hệ nguồn | Bo nguồn: pin, BMS, cầu chì, DC-DC 12 V, đo dòng đỉnh | Ohm, sụt áp, tiết diện dây |
| 2. Cơ khí | Khung, gá motor, phân bố khối lượng, gá mini PC | Mô-men, trọng tâm |
| 3. Bring-up trên bàn | Từng motor/driver/encoder chạy riêng trước khi lên khung | F5.2, F1.1 |
| 4. Firmware ESP32 | PWM, PCNT, watchdog, giao thức sang `ros2_control` | F5.3, F5.8 |
| 5. Lắp hoàn chỉnh | Mini PC lên xe, ROS 2 trong Docker, teleop | K3 |
| 6. Odometry | Hiệu chuẩn UMBmark | F6.4, F1 |
| 7. Cảm biến và ghi dữ liệu | IMU, camera, MCAP | K2, K5 |
| 8. Điều hướng | Định vị bằng marker, Nav2 | F6.7 |
| 9. Nhận người | On-device, privacy | F2.8 |
| 10. An toàn và vận hành | E-stop, state machine, FMEA, soak 72 h | F7.6 |
| 11. Sim twin, HIL, CI | Vòng khép kín | K6, F2.7 |
| 12. Sản phẩm | Robot confession, chuỗi audio | K3 |

Mỗi chặng gồm:
- BOM chi tiết (thông số cần chọn và vì sao).
- Sơ đồ đi dây.
- Các bước lắp, có checkpoint "đo trước khi cấp điện".
- Lỗi người mới hay gặp.
- Mẫu nhật ký build.
- Các bài khái niệm theo khung 12 phần.

**Ba câu hỏi người học chưa trả lời. Phải hỏi trước khi soạn K7:**
1. Ngân sách giờ: chấp nhận 600–900 h, hay cắt chặng 9 và 11 thành tùy chọn?
2. Thời điểm: cho chặng 0–3 chạy song song từ K1 (học điện bằng chính robot), hay giữ K7 sau K6?
3. Khung xe: mua kit có sẵn, hay tự chế?

Tài liệu cần đọc khi thiết kế lại:
- `khoa-7-robot-hoan-chinh.md`: dòng 1–98 là quyết định và kiến trúc.
- `khoa-7-phu-luc.md`: phụ lục A–D và bản đồ vai trò.
- `docs/lo-trinh-edge-physical-ai-final.md`: mục 4 (robot confession V1) và mục 5 (mua sắm, nơi mua tại Hà Nội).
- `00-lo-trinh-tong.md`.

## 4. Gợi ý riêng theo đơn vị (cho phần còn thiếu)

- **K1 Bài 7–8:**
  - Bài 7 logic analyzer: giới hạn 24 MHz và Nyquist cho tín hiệu số (→ F5.5). Bài 8 mỏ hàn: khung rút gọn.
  - Gate K1 giữ tiêu chí gốc.
  - Tổng quan K1 ghi rõ tổng lộ trình 885 h so với ngân sách 650 h.
- **K1 Bài 13:** I2S, BCLK = fs × bits × channels. Logic analyzer 24 MHz bắt được BCLK ở cấu hình nào.
- **K2 Bài 4–8b:**
  - MCAP ↔ Kafka log/segment/index (→ F3.1). Schema evolution Protobuf (→ F3.2), dùng `src/proto/sensors/v1/imu.proto` và `src/imu.mcap` của người học.
  - Chấm mô hình "MCAP chỉ là Kafka trong một file".
  - Kiểm API thư viện `mcap` Python hiện hành.
- **K2 Bài 13–15:** chạy trên dataset thật, report/publish, bài tiếng Anh (Bài 14–15 khung rút gọn). Detector là một phép đo có FP/FN (→ F2.1), CI Wilson (→ F1.4).
- **K3 Bài 5–7:**
  - Chấm mô hình người học: K3 lượt 9 cho Bài 5, lượt 11–13 cho Bài 6.
  - Lượt 12–13 "AI thay tầng vật lý": phần đúng là estimation thay đo trực tiếp; phần sai là không vượt được Nyquist/Shannon và giả định "công thức vật lý gần như hằng số" sai khi ra ngoài phân bố.
  - Bài 6 brownout (→ F5.7). Bài 7 sửa SNR (mục 7), kèm mô phỏng lượng tử hóa.
- **K3 Bài 13:** time-to-first-audio vs tổng độ trễ. Cầu nối TTFB/streaming HTTP; chỗ gãy là audio phải liên tục.
- **K4 Bài 4–6:**
  - Tên chuẩn của thứ người học đã làm: warmup, coordinated omission (Gil Tene), A/A, active benchmarking (→ F1.3).
  - Bài 6: turbostat, tần số thật, N100 không có HT.
- **K4 Bài 11–12:**
  - Bài 11: OpenVINO/ONNX Runtime trên N100, `[tự đo]`.
  - Bài 12: tự tính peak CPU (4 × GHz × 16 FLOP/chu kỳ) và iGPU; mô phỏng roofline; decode batch 1 là memory-bound (mục 7).
- **K5 Bài 5–6:** USB-serial vs mạng, framing, CRC, sequence number đếm mất gói (CONVENTIONS mục 4).
- **K5 Bài 10–12:**
  - Bài 10: tuning-fork 32.768 kHz vs AT-cut, Allan deviation.
  - Bài 11: số hàng sáng ≈ (t_pulse + t_exposure)/t_row.
  - Bài 12: ngân sách sai số (RSS vs cộng tuyến tính); câu chuyện Patriot missile.
- **K5 Bài 16–19:**
  - Bài 16 validation theo vật lý (→ F3.7). Bài 17 drop policy (→ F3.9).
  - Bài 18 soak 7 ngày: completeness ≥99% là một SLO (→ F7.4). Bài 19 bisect (→ F7.7).
- **K6 Bài 5–7:** kịch bản là dữ liệu, sinh có hệ thống (pairwise, Latin hypercube), provenance (→ F3.8).
- **K6 Bài 12–14:**
  - Bài 12 power analysis cho success rate.
  - Bài 13 regression: FP/FN, bội so sánh, peeking, phán quyết ba trạng thái. Nối với script pass/fail/inconclusive của người học.
  - Bài 14 domain randomization.
- **K6 Bài 17–19:**
  - Bài 17 bảng gap theo kênh + miền hiệu lực (→ F6.5).
  - Bài 18 CI và Goodhart, test giữ kín (→ F2.8). Bài 19 và Gate: khung rút gọn.
- **F1–F7:**
  - Nguồn đọc thêm và bài tập gợi ý đã có trong `_ref/brief-F.md` và trong phần đánh giá ban đầu.
  - Tóm tắt nhanh:
    - F4.1: phân biệt tuning-fork và AT-cut.
    - F4.5: `ptp4l -p` là thiết bị PHC.
    - F5: dùng mô hình K3 của người học làm khẳng định mẫu.
    - F7.2: dùng hai khẳng định sai của Gemini K4 Bài 12 làm khẳng định mẫu.
    - F1: phân biệt "không bác bỏ được" với "chứng minh tương đương" (ví dụ Gemini K4: 73% vs 71%, N = 50).

## 5. Ghi chú từ các agent đã xong

- **k4c (`m5-publish.md`):**
  - File dài hơn chuẩn: Bài 13 và 15 dài hơn mức 500–1.200 từ của khung rút gọn. Khung rút gọn có thêm phần 11.
  - Cảnh báo cho reviewer K4 Bài 7: câu "cùng seed 3 lần → giống hệt" chỉ đúng trên cùng máy, cùng image, có bật cờ tất định.
  - Tiêu chí 4 của Gate K4 ("xác nhận công khai") được *diễn giải* là cần JSON + `env` + output `compare.py`, theo ACM badges v1.1.
- **Quy chuẩn chưa nói rõ:** khung rút gọn có phần 11 hay không. Brief bắt ghi sửa lỗi ở phần 11, nên các agent đã thêm phần 11 vào khung rút gọn. Giữ nguyên.

## 6. Session 2 — tiến độ

| Đợt | Việc | Trạng thái |
|---|---|---|
| 1 | Hợp nhất K1, K2 (m1, m2), K3 (m1, m2–m4); viết K6 m2 | đang chạy |
| 2 | K6 m4, m5–m6; F1–F7 | chờ |
| 3 | K7 C0–C12 | chờ |
| 4 | Hợp nhất K4, K5 (khi Kiro đẩy), tổng quan, README | chờ |
