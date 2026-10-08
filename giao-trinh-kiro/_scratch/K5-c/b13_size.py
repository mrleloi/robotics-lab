# [đã chạy] Bài 13 — một sensor_msgs/Imu trong MCAP thật sự nặng bao nhiêu byte?
import os, numpy as np
from mcap_ros2.writer import Writer
from mcap.writer import CompressionType

SEP = "=" * 80 + "\n"
IMU_DEF = (
    "std_msgs/Header header\ngeometry_msgs/Quaternion orientation\nfloat64[9] orientation_covariance\n"
    "geometry_msgs/Vector3 angular_velocity\nfloat64[9] angular_velocity_covariance\n"
    "geometry_msgs/Vector3 linear_acceleration\nfloat64[9] linear_acceleration_covariance\n"
    + SEP + "MSG: std_msgs/Header\nbuiltin_interfaces/Time stamp\nstring frame_id\n"
    + SEP + "MSG: builtin_interfaces/Time\nint32 sec\nuint32 nanosec\n"
    + SEP + "MSG: geometry_msgs/Quaternion\nfloat64 x\nfloat64 y\nfloat64 z\nfloat64 w\n"
    + SEP + "MSG: geometry_msgs/Vector3\nfloat64 x\nfloat64 y\nfloat64 z\n"
)
rng = np.random.default_rng(0)
N = 200 * 600  # 10 phút ở 200 Hz
for comp in (CompressionType.NONE, CompressionType.ZSTD):
    path = f"imu_{comp.name}.mcap"
    with open(path, "wb") as f:
        w = Writer(f, compression=comp)
        sch = w.register_msgdef("sensor_msgs/msg/Imu", IMU_DEF)
        cov = [0.0004, 0, 0, 0, 0.0004, 0, 0, 0, 0.0004]
        for k in range(N):
            t_ns = k * 5_000_000
            msg = {"header": {"stamp": {"sec": t_ns // 10**9, "nanosec": t_ns % 10**9}, "frame_id": "imu_link"},
                   "orientation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0},
                   "orientation_covariance": [-1.0] + [0.0] * 8,   # -1: không ước lượng orientation
                   "angular_velocity": dict(zip("xyz", rng.normal(0, 0.005, 3))),
                   "angular_velocity_covariance": cov,
                   "linear_acceleration": dict(zip("xyz", [*rng.normal(0, 0.02, 2), 9.787 + rng.normal(0, 0.02)])),
                   "linear_acceleration_covariance": cov}
            w.write_message(topic="/imu/data_raw", schema=sch, message=msg, log_time=t_ns, publish_time=t_ns)
        w.finish()
    sz = os.path.getsize(path)
    print(f"{comp.name:5s}: {sz/N:6.1f} byte/msg → {sz/N*200*3600/1e6:6.1f} MB/giờ ở 200 Hz")
    os.remove(path)
