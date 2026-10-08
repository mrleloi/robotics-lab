# Thay đổi lộ trình — 10/2026

Ba quyết định, áp dụng cho mọi file. Chi tiết đầy đủ ở **mục 0.7 của `00-lo-trinh-tong.md`**.

## 1. Mini PC x86 thay Raspberry Pi 5

Mua **Beelink EQ12 (Intel N100), 16GB + 500GB**. Tiêu chí: ≥2 cổng LAN Intel (PTP hardware clock), nguồn 12V DC, BIOS Auto Power On. Dùng xuyên suốt: dev box (Khóa 2–4) → LAN box (Khóa 3–6) → compute trên robot (Khóa 7). Không mua Pi 5.

Kiểm ngay khi nhận máy: `ethtool -T` cả hai cổng phải có `PTP Hardware Clock` và `hardware-transmit/receive`.

## 2. ESP32-S3 là I/O bridge cho mọi thứ cần chân phần cứng

Mini PC không có GPIO. I2S, GPIO đánh dấu, encoder, bumper đều ở ESP32, nói chuyện với host qua USB.

## 3. Dữ liệu theo chuẩn ngành

REP-103, REP-105, message chuẩn ROS 2, metadata ở channel MCAP, `ros2_control` cho MCU. Mẫu khởi đầu: `CONVENTIONS.md`.

## Thay đổi theo file

| File | Thay đổi chính |
|---|---|
| `00-lo-trinh-tong.md` | Thêm mục 0.7; đợt mua 2 tách thành 2a (mini PC) + 2b (audio); kiến trúc V1 thành mini PC → USB → ESP32 → I2S; TN-2/TN-3 đo trên ESP32; M6 target edge là N100; M7 PTP giữa hai cổng mini PC; danh sách mua và nguồn học cập nhật |
| `khoa-1` | Bản đồ 7 khóa; thói quen ghi đơn vị SI từ Bài 9 |
| `khoa-2` | Đọc REP-103/105 ở Bài 3; **Bài 8b mới (2h)**: converter `ImuSample` → `sensor_msgs/Imu`, metadata ở channel; gate thêm tiêu chí 3b; ngân sách 22h/trần 32h |
| `khoa-3` | Viết lại Bài 2 (ESP-IDF + DAC), Bài 4 (DMA buffer + USB flow control, ALSA thành bước tùy chọn), Bài 6 (brownout ESP32 thay `get_throttled`), Bài 9–10 (GPIO marker trên ESP32, hai kịch bản tải), Bài 12 (RTF trên N100), Bài 16 (watchdog hai tầng, BIOS auto power on); mic dùng bộ I2S thứ hai của ESP32 nên phát và ghi đồng thời được; bẫy và nguồn học cập nhật |
| `khoa-4` | Bài 11 viết lại: target edge là N100 với ba runtime (ONNX Runtime CPU, OpenVINO CPU, OpenVINO iGPU); thermal dùng `turbostat`/tần số thật |
| `khoa-5` | Bài 1 viết lại: tầng phần cứng dựa trên hai PHC của mini PC; Bài 9 viết lại: **PTP giữa hai cổng trong một hộp**, trọng tài đọc PHC trực tiếp (`PTP_SYS_OFFSET_EXTENDED`) thay GPIO; TN-1 dùng hai ESP32; Bài 13 dùng message chuẩn + metadata, micro-ROS tùy chọn |
| `khoa-6` | Không đổi |
| `khoa-7` | Mini PC lên khung xe; khung/pin/DC-DC 12V lớn hơn; `ros2_control` cho đường MCU; FMEA thêm dòng mất nguồn 12V và đường cắt relay độc lập; ngân sách giảm còn 4.5–11tr |
| `khoa-7-phu-luc` | Planner chạy trên N100; điều kiện mua Jetson đổi theo |

## Điều chưa kiểm chứng — kiểm khi có máy

- Hai cổng i225/i226 trên máy bạn mua thật sự có hai PHC riêng (`ls /dev/ptp*`).
- Hai instance `ptp4l` cùng máy chạy ổn với transport L2 — có thể cần file cấu hình riêng.
- Độ rộng "kẹp" khi đọc PHC qua `PTP_SYS_OFFSET_EXTENDED` trên máy bạn — đây là sai số trọng tài, phải tự đo.
- Khối lượng và công suất thật của mini PC — cân và đo, đưa vào power budget Khóa 7.
