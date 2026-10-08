import numpy as np

# Create sample data that make sense
fps = 200
duration = 60
n = fps * duration
t = np.arange(n) / fps

g = 9.81
## IMU đứng yên: trục z đọc ~g, cộng nhiễu Gaussian ~0.02 m/s²
az = g + np.random.normal(0, 0.02, n)
ax = np.random.normal(0, 0.02, n)
ay = np.random.normal(0, 0.02, n)
## Gyro đứng yên: quanh 0, có bias nhỏ và drift chậm
gz = np.random.normal(0, 0.001, n) + 0.002 + 1e-5 * t

# Save as Mcap file
from mcap_protobuf.writer import Writer
from proto.sensors.v1 import imu_pb2

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

