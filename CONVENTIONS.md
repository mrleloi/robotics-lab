# CONVENTIONS.md — quy ước dữ liệu của repo

> Mẫu khởi đầu. Copy vào gốc repo `robotics-lab/`, sửa theo thực tế, commit trước khi ghi bất kỳ dữ liệu nào.
> Mọi thay đổi ở đây ghi kèm lý do vào `decisions.md`.

## 1. Đơn vị và hệ trục — REP-103

- Đơn vị SI, không ngoại lệ: `m`, `s`, `kg`, `rad`, `m/s`, `m/s²`, `rad/s`, `K` hoặc `°C` (ghi rõ), `Pa`.
- Góc luôn là **rad** trong dữ liệu. Độ chỉ dùng khi hiển thị cho người đọc.
- Gia tốc là **m/s²**, không phải "g".
- Hệ tay phải. Thân robot: `x` tiến, `y` trái, `z` lên.
- Thời gian trong message: `header.stamp` (giây + nano giây). Thời gian trong MCAP: nano giây.

Nguồn: https://www.ros.org/reps/rep-0103.html

## 2. Frame — REP-105

```
map → odom → base_link → imu_link
                       → tof_link
                       → camera_<tên>_link → camera_<tên>_optical_frame
```

- `odom → base_link`: liên tục, trôi (odometry).
- `map → odom`: hiệu chỉnh nhảy bậc từ định vị tuyệt đối (marker, lidar).
- Frame quang học của camera theo quy ước REP-103 cho camera: `z` hướng ra trước ống kính, `x` sang phải, `y` xuống dưới.

Nguồn: https://www.ros.org/reps/rep-0105.html

## 3. Kiểu message

| Luồng | Message | Topic | Frame | Tần số | Ghi chú |
|---|---|---|---|---|---|
| IMU | `sensor_msgs/msg/Imu` | `/imu/data_raw` | `imu_link` | 200 Hz | Điền covariance từ số đo thật, không để 0 |
| ToF | `sensor_msgs/msg/Range` | `/tof/range` | `tof_link` | 30 Hz | `range` âm hoặc ngoài `[min_range, max_range]` = không hợp lệ |
| Nhiệt độ | `sensor_msgs/msg/Temperature` | `/env/temperature` | `env_link` | 1 Hz | |
| Áp suất | `sensor_msgs/msg/FluidPressure` | `/env/pressure` | `env_link` | 1 Hz | Đơn vị Pa |
| Độ ẩm | `sensor_msgs/msg/RelativeHumidity` | `/env/humidity` | `env_link` | 1 Hz | Giá trị 0–1, không phải % |
| Camera | `sensor_msgs/msg/CompressedImage` + `CameraInfo` | `/camera_<tên>/image/compressed` | `camera_<tên>_optical_frame` | 30 Hz | |
| Encoder | `sensor_msgs/msg/JointState` | `/joint_states` | — | 100 Hz | Từ `ros2_control` |
| Odometry | `nav_msgs/msg/Odometry` | `/odom` | `odom` → `base_link` | 50 Hz | Covariance từ UMBmark |
| Pin | `sensor_msgs/msg/BatteryState` | `/battery` | — | 1 Hz | |

(Bảng điền dần theo khóa. Thêm dòng trước khi thêm luồng.)

## 4. Metadata — thứ message chuẩn không có

**Nguyên tắc: payload dùng message chuẩn; thứ chuẩn không có thì đi vào metadata channel MCAP, không sửa message chuẩn.**

| Khóa metadata | Ví dụ | Bắt buộc |
|---|---|---|
| `metadata_version` | `1` | Có |
| `calibration_id` | `imu-01@2026-11-02-a` | Có, với mọi cảm biến có hiệu chuẩn |
| `clock_source` | `esp32_timer` · `host_ptp_synced` · `host_unsynced` · `estimated` | Có |
| `source_device_id` | `esp32-01` | Có |
| `firmware_version` | git hash firmware | Có |

Mất gói được phát hiện bằng số thứ tự ở tầng truyền (host ↔ ESP32), ghi vào topic chẩn đoán `/diagnostics`, không chèn vào message cảm biến.

## 5. Ghi log và công cụ

- Ghi bằng **rosbag2 → MCAP** (hoặc writer `mcap-ros2-support` khi không chạy ROS 2).
- Mọi file phải qua `ros2 bag info` và `mcap doctor` không lỗi.
- Xem bằng Foxglove; layout JSON commit trong repo.

## 6. Môi trường

- Ubuntu 24.04 LTS + ROS 2 Jazzy, chạy trong Docker.
- Image build **đa kiến trúc** (`docker buildx`, `linux/amd64` + `linux/arm64`) — mini PC là x86, Jetson là ARM64.
- Lockfile pin mọi phiên bản.

## 7. MCU ↔ host

- Khóa 3, 5: giao thức serial có số thứ tự, độ dài, và flow control dạng credit.
- Khóa 7: **`ros2_control` hardware interface** (hoặc micro-ROS). Không tự chế giao thức cho vòng điều khiển.
