# Review — các bài K4/K5 viết ở session 4 (2026-10-09)

**Loại review:** tự review của người soạn (Claude), cùng phiên, theo `_ref/brief-reviewer.md` mục A–H. **Không phải review độc lập.** Một reviewer khác vẫn nên đọc lại, ưu tiên các bài có công thức (K5 Bài 11, 12) và các định nghĩa đi vào gate (K5 Bài 17, 18).

**Phạm vi:** K4 Bài 6 (`m2-harness.md`), Bài 12 (`m4-nhieu-target.md`); K5 Gate Module 0 (`m0`), Bài 6 (`m1`), Bài 11, 12 (`m2`), Bài 17 (`m3`), Bài 18, 19, Gate K5 (`m4-van-hanh.md`), `00-tong-quan.md`; khối "C8 tối thiểu" ở đầu `khoa-7/c08-dieu-huong.md` và ghi chú FMEA trong `c10`.

## Cách kiểm

- Script `_scratch/review/check.py`: kiểm đủ phần khung (12 phần hoặc khung rút gọn), cụm từ cấm, có [Quy mô] và [Failure mode], nhãn Mermaid chứa ngoặc chưa bọc, số xuất hiện trong khối 🔒 mà cũng có ngoài khối, và chạy lại mọi khối `# [đã chạy]` lấy trực tiếp từ file markdown.
- Kiểm web ba khẳng định chưa chắc: EASA AD 2017-0129 (A350, 149 giờ), TjMax/base power của N100, RFC 3393 có bàn ước lượng skew.
- Đọc lại thủ công các bước Làm, các phép tính trong đáp án tự kiểm, và lập luận ở phần 2.

## Kết quả

| Mục | Kết quả |
|---|---|
| C. Code | 10/10 khối `[đã chạy]` chạy lại sạch, output khớp bảng 🔒 |
| E. Khung | Gate Module 0 thiếu khung rút gọn → **viết lại** đủ Vị trí, 1, 2, 3, 6, 8, 9, 12 (thêm Mermaid, cầu nối, 2 câu hỏi ngược). Các bài khác đủ. Script báo K4 Bài 6 "thiếu phần 7–12" là cảnh báo nhầm (dòng `##` nằm trong khối code mẫu `METHODOLOGY.md`); kiểm tay đủ 12 phần |
| F. Văn phong | 0 chỗ |
| Mermaid | 0 lỗi cú pháp |

## Lỗi đã sửa

**D. Niêm phong** (sửa ở lượt kiểm trước khi commit và ở lượt này):
- K4 Bài 6, 12; K5 Bài 6, 11, 17, 18, 19: số kết quả mô phỏng nằm trong phần "Chấm mô hình" ngoài khối 🔒 (đúng các số mà phần Dự đoán bắt đoán) → thay bằng tham chiếu "phần 7".
- K4 Bài 12: "Một pha đạt 6% trần" ở phần 2; ví dụ "6% hay 60%" ở mục sai số; nhãn "vision/expert" trên hình roofline phác thảo → bỏ số, đổi nhãn thành "pha A/pha B".
- K5 Bài 17: "tải trung bình 4%" trong một mô hình được chấm và ở phần 2 → "vài phần trăm".

**A. Kỹ thuật:**
- K5 Bài 11, Phần C bước 1: thứ tự vòng tròn (ước lượng β trước khi có t_on trên đồng hồ host) → đổi t_on sang đồng hồ host bằng mô hình ESP32 ↔ host trước, rồi β_k = T_k − (t_on − r*·t_row); ghi sai số ánh xạ cạnh β_k.
- K5 Bài 6, đáp án tự kiểm 2: "skew đổi 3 ppm khi phòng nguội là hợp lý" → quá dễ dãi với AT-cut; sửa: skew là hiệu của hai thạch anh, 3 ppm đòi nhiệt quanh board đổi đáng kể, kiểm bằng BME280.
- K5 Bài 6, phần 7: "mỗi lỗi giết đúng một khung" → thêm điều kiện "không có hai lỗi rơi vào cùng một khung".
- K5 tổng quan: "K6 Bài 15 (sim-to-real theo kênh)" → K6 Bài 15 là định nghĩa gap đo được, bảng theo kênh là Bài 17; sửa thành "K6 Bài 15, 17".

**B. Nguồn:**
- K5 Bài 18: EASA AD 2017-0129 đã xác minh (25/7/2017, A350-941, mất liên lạc avionics sau 149 giờ cấp điện liên tục) → thêm chi tiết 149 giờ, nâng ghi chú từ "kiểm số AD" thành "đã kiểm".
- K4 Bài 6, K5 Bài 18: TjMax 105 °C, base power 6 W của N100 khớp nguồn thứ ba trích ARK.
- K5 Bài 6: RFC 3393 §5.2 có bàn ước lượng skew tuyến tính và trừ nó khỏi IPDV, đúng như câu hỏi ngược 5.

## Còn nghi ngờ (chưa kiểm được ở đây)

- Cú pháp `turbostat --show Time_Of_Day_Seconds` (có thể cần `--enable`), cờ `ts-src-soe/eof` của uvcvideo, `FlopCounterMode` từ PyTorch 2.1, odometry của `diff_drive_controller` có về 0 khi kích hoạt lại không: đều đã gắn `[tự đo]` trong bài.
- Ngưỡng V_IH của ESP32-S3 và ngưỡng đầu vào của logic analyzer clone (K5 Bài 19, ý 1): `[tự đo]`.
- Kích thước SmolVLA trong mô phỏng K4 Bài 12 (720/1920 cho expert): `[ước lượng]`, người học in lại từ `config.json`.
