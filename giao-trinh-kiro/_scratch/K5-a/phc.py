import struct
PTP_MAX_SAMPLES = 25
SIZE = 16 + PTP_MAX_SAMPLES * 3 * 16
IOC = (3 << 30) | (SIZE << 16) | (ord("=") << 8) | 9
print(SIZE, hex(IOC))

def decode(buf, n):
    out = []
    for i in range(n):
        s0, n0, _, s1, n1, _, s2, n2, _ = struct.unpack_from("=qIIqIIqII", buf, 16 + i * 48)
        sys0, phc, sys2 = s0 * 10**9 + n0, s1 * 10**9 + n1, s2 * 10**9 + n2
        out.append((sys2 - sys0, phc - (sys0 + sys2) // 2))
    return out

buf = bytearray(SIZE)
struct.pack_into("=I", buf, 0, 2)
for i in range(2):
    struct.pack_into("=qIIqIIqII", buf, 16 + i * 48, 100, 1000, 0, 100, 3500, 0, 100, 5000, 0)
print(decode(buf, 2), struct.calcsize("=qIIqIIqII"))
