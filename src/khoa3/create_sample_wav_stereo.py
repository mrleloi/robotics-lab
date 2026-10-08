import math
import struct

SAMPLE_RATE = 24000 #24khz
FREQUENCY = 440 #hz
DURATION = 1.0 #duration
AMPLITUDE = 32767 # biên độ voice

CHANNELS = 2 #stereo channel
BITS_PER_SAMPLE = 16 #16 bit

num_samples = int(SAMPLE_RATE * DURATION)

left_samples = []
right_samples = []

for n in range(num_samples):
    left = AMPLITUDE * math.sin(
        2 * math.pi * FREQUENCY * n / SAMPLE_RATE
    )
    right = AMPLITUDE * math.sin(
        2 * math.pi * 2 * FREQUENCY * n / SAMPLE_RATE
    )
    left_samples.append(int(left))
    right_samples.append(int(right))


# =========================
# WAV header
# =========================

bytes_per_sample = BITS_PER_SAMPLE // 8

block_align = CHANNELS * bytes_per_sample
byte_rate = SAMPLE_RATE * block_align
data_size = num_samples * block_align


riff_chunk_size = 36 + data_size


header = b""


# RIFF chunk
header += b"RIFF"
header += struct.pack("<I", riff_chunk_size)
header += b"WAVE"

# fmt chunk
header += b"fmt "
header += struct.pack("<I", 16)              # PCM fmt chunk size
header += struct.pack("<H", 1)               # audio format = PCM
header += struct.pack("<H", CHANNELS)
header += struct.pack("<I", SAMPLE_RATE)
header += struct.pack("<I", byte_rate)
header += struct.pack("<H", block_align)
header += struct.pack("<H", BITS_PER_SAMPLE)


# data chunk
header += b"data"
header += struct.pack("<I", data_size)


# =========================
# PCM data
# =========================

pcm_data = b""

for left, right in zip(left_samples, right_samples):
    pcm_data += struct.pack("<h", left)  # Left
    pcm_data += struct.pack("<h", right)  # Right


with open("tone_440_stereo.wav", "wb") as f:
    f.write(header)
    f.write(pcm_data)



print("num_samples =", num_samples)
print("data_size   =", data_size)
print("header_size =", len(header))
print("file_size   =", len(header) + len(pcm_data))

print("\nFirst 20 samples:")

