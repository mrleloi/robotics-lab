# [đã chạy] Bù trừ nhiệt độ BME280 theo datasheet Bosch (mục 4.2.3) — hệ số là VÍ DỤ
import math

def comp_T_int32(adc_T, T1, T2, T3):
    """Bản số nguyên 32-bit, đúng thứ tự phép toán của datasheet (dùng >>)."""
    var1 = (((adc_T >> 3) - (T1 << 1)) * T2) >> 11
    var2 = (((((adc_T >> 4) - T1) * ((adc_T >> 4) - T1)) >> 12) * T3) >> 14
    t_fine = var1 + var2
    T = (t_fine * 5 + 128) >> 8          # đơn vị 0.01 °C
    return T, t_fine

def comp_T_float(adc_T, T1, T2, T3):
    """Bản dấu phẩy động (datasheet mục 8.1 / Bosch SensorAPI)."""
    var1 = (adc_T / 16384.0 - T1 / 1024.0) * T2
    var2 = (adc_T / 131072.0 - T1 / 8192.0) ** 2 * T3
    return (var1 + var2) / 5120.0

# Hệ số VÍ DỤ (mỗi con chip có bộ riêng — đọc từ 0x88..0x8D của chip bạn)
T1, T2, T3 = 27504, 26435, -1000
adc_T = 519888                            # 20-bit, ghép từ 0xFA/0xFB/0xFC

T, t_fine = comp_T_int32(adc_T, T1, T2, T3)
print("int32 : T =", T / 100, "°C, t_fine =", t_fine)
print("float : T = %.4f °C" % comp_T_float(adc_T, T1, T2, T3))

# Lan truyền: độ nhạy dT/d(adc_T) quanh điểm làm việc (đạo hàm số)
d = 16
sens = (comp_T_float(adc_T + d, T1, T2, T3) - comp_T_float(adc_T - d, T1, T2, T3)) / (2 * d)
print("dT/dLSB(20-bit) = %.6f °C" % sens)
for bits in (16, 17, 18, 19, 20):         # osrs_t x1..x16 -> 16..20 bit hiệu dụng
    q = sens * 2 ** (20 - bits)           # bước lượng tử theo °C
    print(f"{bits} bit: bước {q*1000:.2f} m°C, u_quant = q/sqrt(12) = {q/math.sqrt(12)*1000:.2f} m°C")
print("Bước của output int32: 10 m°C -> u =", round(10 / math.sqrt(12), 2), "m°C")

# Nếu dùng nhầm hệ số của chip khác (T2 lệch 1%):
print("T2 lệch +1%%: T = %.3f °C" % comp_T_float(adc_T, T1, int(T2 * 1.01), T3))
print("T1 lệch +1%%: T = %.3f °C" % comp_T_float(adc_T, int(T1 * 1.01), T2, T3))

# g địa phương ở Hà Nội (công thức trọng trường chuẩn 1980, mực nước biển)
phi = math.radians(21.03)
g = 9.780327 * (1 + 0.0053024 * math.sin(phi) ** 2 - 0.0000058 * math.sin(2 * phi) ** 2)
print("g(21.03°N) = %.4f m/s^2; lệch so với g0: %.3f %%" % (g, (g / 9.80665 - 1) * 100))
print("raw kỳ vọng ±2g khi nằm yên:", round(16384 * g / 9.80665), "LSB")
print("MPU6050 sai số độ nhạy ±3% -> |a| trong", round(g * 0.97, 3), "..", round(g * 1.03, 3))
