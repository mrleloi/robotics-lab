# Mục lục bài gốc (trích tự động từ các file khoa-*.md, số dòng để đọc theo offset)

## khoa-1-tu-zero-den-do-duoc.md
```
1: # KHÓA 1 — TỪ ZERO ĐẾN ĐO ĐƯỢC
63: # PHẦN A — NỀN (6h, không cần mua gì, làm được ngay tối nay)
67: ## Bài 1 — Bốn đại lượng và một quy tắc
134: ## Bài 2 — Mạch kín, GND, và tại sao dây nối là một giả định
171: ## Bài 3 — Tín hiệu số, bus, và clock
230: # PHẦN B — DỤNG CỤ: MỖI MÓN LÀ GÌ VÀ CẦM THẾ NÀO (5h)
234: ## Bài 4 — Mua gì, và mỗi món để làm gì
269: ## Bài 5 — Multimeter: cầm thế nào cho đúng
349: ## Bài 6 — Breadboard: nó nối với nhau như thế nào
396: ## Bài 7 — Logic analyzer và PulseView
442: ## Bài 8 — Mỏ hàn (chỉ cần khi module chưa hàn sẵn chân)
479: # PHẦN C — ĐO THẬT (14h)
485: ## Bài 9 — Voltage divider: thí nghiệm đầu tiên có dự đoán
561: ## Bài 10 — LED và điện trở: tại sao, bằng số
630: ## Bài 11 — Đọc trọn một datasheet
679: # PHẦN D — NHÌN THẤY DỮ LIỆU TRÊN DÂY (10h)
683: ## Bài 12 — Cắm I2C và nhìn thấy ACK
783: ## Bài 13 — Nhìn thấy I2S
843: ## Bài 14 — Gate Khóa 1
864: # LỊCH 4 TUẦN
877: # NGUỒN HỌC KÈM THEO KHÓA 1
894: # SAU KHÓA 1
```

## khoa-2-du-lieu-robot-khong-can-robot.md
```
1: # KHÓA 2 — DỮ LIỆU ROBOT MÀ KHÔNG CẦN ROBOT
34: # MODULE 1 — MCAP VÀ CÔNG CỤ (20h)
40: ## Bài 1 — Một con robot sinh ra dữ liệu gì (2h)
93: ## Bài 2 — Timestamp trong robotics (3h)
153: ## Bài 3 — Frame và TF (1h)
182: ## Bài 4 — MCAP: cấu trúc file (2h)
271: ## Bài 5 — Viết file MCAP đầu tiên (4h)
329: # IMU đứng yên: trục z đọc ~g, cộng nhiễu Gaussian ~0.02 m/s²
333: # Gyro đứng yên: quanh 0, có bias nhỏ và drift chậm
425: ## Bài 6 — Schema versioning và contract (3h)
494: ## Bài 7 — Index, random access, và file bị cắt (3h)
519: # đọc toàn bộ
524: # đọc 10 giây ở giữa bằng start_time/end_time
534: # cắt bỏ 20% cuối
571: ## Bài 8 — Foxglove và Rerun (2h)
620: ## Bài 8b — Schema của tôi vs schema của ngành (2h)
662: ## GATE MODULE 1 (= M2 PASS)
678: # MODULE 2 — DATASET AUDIT TOOL (60h) ★
684: ## Bài 9 — LeRobot dataset format từ zero (6h)
779: ## Bài 10 — Kiểm tra bằng tay trước khi tự động hóa (6h)
815: ## Bài 11 — Bảy lớp lỗi: định nghĩa và toán (8h)
969: ## Bài 12 — Viết detector và test tổng hợp (20h)
1049: ## Bài 13 — Chạy trên dataset thật (8h)
1076: ## Bài 14 — Report, publish, và báo cáo ra ngoài (8h)
1125: ## Bài 15 — Bài viết tiếng Anh (4h)
1142: ## GATE MODULE 2 (= M3 PASS)
1156: # LỊCH 8 TUẦN
1174: # NGUỒN HỌC KÈM THEO
1189: # SAU KHÓA 2
```

## khoa-3-chuoi-audio.md
```
1: # KHÓA 3 — CHUỖI AUDIO: TỪ SỐ NGUYÊN ĐẾN ÁP SUẤT KHÔNG KHÍ
59: # MODULE 1 — CHUỖI PHÁT (32h)
63: ## Bài 1 — Audio số thực sự là cái gì (2h)
123: ## Bài 2 — Dựng mini PC, ESP32-S3 và DAC I2S (5h)
206: ## Bài 3 — TN-1: Nhìn thấy âm thanh trên dây (5h)
308: ## Bài 4 — DMA buffer, ring buffer, underrun: từ dưới lên (6h)
383: ## Bài 5 — DAC → amp → loa: trở kháng và công suất (4h)
438: ## Bài 6 — TN-3: Cố tình làm hỏng nó bằng nguồn (5h)
499: ## Bài 7 — TN-4: Từ không khí thành số nguyên, và ngược lại (7h)
577: # MODULE 2 — ĐO ĐỘ TRỄ THẬT (16h)
583: ## Bài 8 — Latency budget: dự đoán trước (3h)
616: ## Bài 9 — TN-2: Đo độ trễ từ phần mềm ra không khí (7h)
686: ## Bài 10 — Đường cong độ trễ vs underrun (6h)
742: # MODULE 3 — TTS VÀ QUYẾT ĐỊNH KIẾN TRÚC (14h)
746: ## Bài 11 — RTF: chỉ số quyết định kiến trúc (3h)
778: ## Bài 12 — Chạy TTS tiếng Việt và đo RTF (6h)
824: ## Bài 13 — Streaming chunk đầu: độ trễ cảm nhận vs độ trễ tổng (5h)
858: # MODULE 4 — HỆ THỐNG V1 (22h)
864: ## Bài 14 — Ingest, dedupe, state machine (6h)
908: ## Bài 15 — Moderation queue và kill switch (5h)
943: ## Bài 16 — Streamer daemon, firmware, watchdog hai tầng (5h)
971: ## Bài 17 — TN-5: 72 giờ không ai trông (6h người, 72h treo máy)
1004: # GATE KHÓA 3 (6h)
1036: # LỊCH 12 TUẦN
1057: # BẢY BẪY ĐÃ BIẾT TRƯỚC
1071: # NGUỒN HỌC KÈM KHÓA 3
1091: # SAU KHÓA 3
```

## khoa-4-benchmark-edge.md
```
1: # KHÓA 4 — ĐO HIỆU NĂNG INFERENCE TRÊN EDGE
54: # MODULE 1 — NỀN TẢNG (10h)
58: ## Bài 1 — VLA model là cái gì, ở mức tensor (3h)
107: ## Bài 2 — Đo cái gì, và những con số hợp lý trông như thế nào (3h)
162: ## Bài 3 — Methodology: phần quan trọng nhất của cả khóa (4h)
242: # MODULE 2 — HARNESS (14h)
246: ## Bài 4 — Thiết kế harness (5h)
316: ## Bài 5 — Đo model đầu tiên trên GPU thuê (5h)
369: ## Bài 6 — Cô lập nhiệt và chứng minh bằng số (4h)
397: # MODULE 3 — TRỤC CHẤT LƯỢNG (16h)
405: ## Bài 7 — LIBERO: đo chất lượng mà không cần robot (5h)
439: ## Bài 8 — Quantization: fp32 → 4-bit (6h)
497: ## Bài 9 — Đường cong Pareto và bẫy "nhanh nhưng hỏng" (5h)
527: # MODULE 4 — NHIỀU MODEL, NHIỀU TARGET (18h)
533: ## Bài 10 — Model thứ hai và thứ ba (6h)
573: ## Bài 11 — Target thứ hai: CPU N100, và con số gây sốc (6h)
630: ## Bài 12 — Roofline: nút thắt nằm ở đâu (6h)
670: # MODULE 5 — PUBLISH VÀ REPRODUCE (12h)
676: ## Bài 13 — Viết bài tiếng Anh (5h)
714: ## Bài 14 — Làm cho người khác chạy lại được (4h)
752: ## Bài 15 — Đi tìm người reproduce (3h)
785: # GATE KHÓA 4
819: # LỊCH 11 TUẦN
839: # NGUỒN HỌC KÈM KHÓA 4
859: # BA ĐIỀU MANG ĐI
869: # SAU KHÓA 4
```

## khoa-5-sensor-timesync-platform.md
```
1: # KHÓA 5 — CẢM BIẾN, ĐỒNG BỘ THỜI GIAN, DATA PLATFORM
24: # MODULE 0 — CHỌN PHẦN CỨNG (8h)
28: ## Bài 1 — Kiểm tra ràng buộc phần cứng trước khi mua gì (3h)
99: ## Bài 2 — Kế hoạch đo trước, platform sau (5h)
126: # MODULE 1 — CẢM BIẾN VÀ RAW REGISTER (32h)
130: ## Bài 3 — Quét bus và bắt tay với chip (5h)
177: ## Bài 4 — Raw register → đơn vị vật lý, tự tay (8h)
245: ## Bài 5 — Cảm biến thứ hai và thứ ba (7h)
283: ## Bài 6 — ESP32-S3 làm node cảm biến: USB-serial vs mạng (12h)
339: # MODULE 2 — ĐỒNG BỘ THỜI GIAN (50h)
345: ## Bài 7 — Ngân sách sai số thời gian (6h)
382: ## Bài 8 — TN-1: GPIO chung, sự kiện duy nhất (10h)
427: ## Bài 9 — TN-2: PTP, trước và sau (12h)
471: # cổng 1 làm master
473: # cổng 2 làm slave (terminal khác)
475: # system clock theo PHC của cổng 1
518: ## Bài 10 — TN-3: Clock drift theo nhiệt độ (8h)
551: ## Bài 11 — TN-4: Hardware trigger và rig 2 camera + IMU (14h)
634: ## Bài 12 — Tổng hợp ngân sách sai số (không tính giờ riêng, làm cùng Bài 7–11)
644: # MODULE 3 — DATA STACK (50h, trần cứng 55h)
650: ## Bài 13 — Ingest nhiều luồng khác tần số vào MCAP (14h)
696: ## Bài 14 — Upload resumable và object store (10h)
727: ## Bài 15 — Index và truy vấn (10h)
751: ## Bài 16 — Validation theo vật lý, không chỉ theo schema (10h)
801: ## Bài 17 — Backpressure và drop policy (6h)
831: # MODULE 4 — VẬN HÀNH (10h người, 7 ngày treo máy)
835: ## Bài 18 — Soak 7 ngày (6h)
862: ## Bài 19 — Bisect qua bốn tầng (4h)
898: # GATE KHÓA 5
932: # LỊCH 24 TUẦN
955: # NGUỒN HỌC KÈM KHÓA 5
975: # BA ĐIỀU MANG ĐI
985: # SAU KHÓA 5
```

## khoa-6-sim-eval-infra.md
```
1: # KHÓA 6 — SIMULATION & EVALUATION INFRASTRUCTURE
70: # MODULE 1 — DETERMINISM (24h)
76: ## Bài 1 — Vì sao determinism là điều kiện tiên quyết, không phải tính năng đẹp (4h)
124: ## Bài 2 — Dựng stack và chạy episode đầu tiên (6h)
155: ## Bài 3 — Săn nguồn phá determinism (8h)
179: # sai — dùng state toàn cục
182: # đúng — generator riêng, seed dẫn xuất
234: ## Bài 4 — Chốt determinism vào CI (6h)
262: # MODULE 2 — KỊCH BẢN LÀ DỮ LIỆU (20h)
266: ## Bài 5 — Kịch bản không phải script (8h)
326: ## Bài 6 — Sinh kịch bản có hệ thống (6h)
357: ## Bài 7 — Provenance: từ kết quả truy ngược về mọi thứ (6h)
393: # MODULE 3 — CHẠY Ở QUY MÔ (24h)
399: ## Bài 8 — Song song hóa và throughput thật (8h)
433: ## Bài 9 — Artifact management: output của 10.000 episode đi đâu (8h)
473: ## Bài 10 — Từ run tới báo cáo (8h)
490: # MODULE 4 — ĐÁNH GIÁ VÀ REGRESSION (26h)
494: ## Bài 11 — Định nghĩa thành công bằng toán (6h)
548: ## Bài 12 — Bao nhiêu episode là đủ (8h)
616: ## Bài 13 — Phát hiện regression tự động (6h)
655: ## Bài 14 — Domain randomization và đo xem nó mua được gì (6h)
687: # MODULE 5 — ĐO SIM-TO-REAL GAP (20h)
695: ## Bài 15 — Định nghĩa gap sao cho đo được (6h)
724: ## Bài 16 — Con lắc: ba đường phải gặp nhau (8h)
836: ## Bài 17 — Bảng gap theo kênh và giới hạn hiệu lực (6h)
875: # MODULE 6 — VÒNG KHÉP KÍN VÀ PUBLISH (6h)
879: ## Bài 18 — CI: đổi một thứ, nhận một phán quyết (3h)
916: ## Bài 19 — Publish (3h)
939: # GATE KHÓA 6
971: # LỊCH 19 TUẦN
996: # NGUỒN HỌC
1015: # BA ĐIỀU MANG ĐI
1025: # SAU KHÓA 6
```

## khoa-7-phu-luc.md
```
1: # PHỤ LỤC KHÓA 7
```

## khoa-7-robot-hoan-chinh.md
```
1: # KHÓA 7 — ROBOT DI ĐỘNG HOÀN CHỈNH
99: # 7A — CHASSIS, MOTOR, ENCODER, ODOMETRY (60h)
105: ## Bài 1 — Motor, encoder, driver: ba thứ phải hiểu trước khi cấp điện (8h)
164: ## Bài 2 — Đường cong PWM → vận tốc, và vùng chết (8h)
199: ## Bài 3 — PID vận tốc bánh xe và jitter vòng lặp (14h)
252: ## Bài 4 — Odometry và hiệu chuẩn UMBmark (16h)
325: ## Bài 5 — Ghi dữ liệu và nối vào hạ tầng Khóa 5 (14h)
354: ## GATE 7A
378: # 7B — ĐỊNH VỊ VÀ ĐIỀU HƯỚNG (80h)
384: ## Bài 6 — Chọn đường: marker hay lidar (6h)
412: ## Bài 7 — Hiệu chuẩn camera và độ chính xác pose từ marker (16h)
446: ## Bài 8 — Hợp nhất odometry và marker (20h)
486: ## Bài 9 — Nav2: từ A tới B (24h)
528: ## Bài 10 — Ghi và phân tích session điều hướng (14h)
551: ## GATE 7B
573: # 7C — NHẬN NGƯỜI ON-DEVICE, PRIVACY-FIRST (60h)
579: ## Bài 11 — Thiết kế quyền riêng tư trước khi viết dòng code nào (10h)
619: ## Bài 12 — Pipeline nhận diện và đo FAR/FRR (24h)
675: ## Bài 13 — Đăng ký, xóa dữ liệu, và audit log (12h)
696: ## Bài 14 — Tích hợp nhận diện vào điều hướng (14h)
716: ## GATE 7C
741: # 7D — TÍCH HỢP, AN TOÀN, STATE MACHINE (60h)
747: ## Bài 15 — An toàn là một tầng phần cứng (16h)
799: ## Bài 16 — State machine và phân tích chế độ hỏng (18h)
847: ## Bài 17 — Soak 72 giờ trong văn phòng thật (16h người, 72h treo máy)
869: ## GATE 7D
887: # 7E — FULL TEST FLOW (80h)
895: ## Bài 18 — Dựng mô hình sim khớp với robot thật (20h)
937: ## Bài 19 — HIL và CI cho hành vi robot (24h)
977: ## Bài 20 — Sim có dự đoán được thực tế không (16h)
1011: ## Bài 21 — Vòng đời dữ liệu đầy đủ và fine-tune (20h)
1052: ## GATE 7E — VÀ GATE KHÓA 7
1081: # NGÂN SÁCH
1097: # LỊCH 60 TUẦN
1114: # BA ĐIỀU MANG ĐI
```

## Bản Gemini (detail/) — tìm bài bằng grep 'Bài N'
```
Gemini-khóa 3-20261008-0956.md:44: ### 1. Mục đích của Bài 2 là gì?
Gemini-khóa 3-20261008-0956.md:147: ### 1. Ở Bài 1: Hiểu audio số ở mức byte
Gemini-khóa 3-20261008-0956.md:156: ### 2. Ở Bài 2: Mang sang ESP32 có còn tạo file WAV không?
Gemini-khóa 3-20261008-0956.md:894: ### 4. Cầu nối trực tiếp sang Bài 6 (TN-3)
Gemini-khóa 3-20261008-0956.md:1009: ### Ý nghĩa lớn nhất của Bài 6
Gemini-khóa 3-20261008-0956.md:1464: ### 3. Xác nhận hiểu như thế nào? (Tiêu chí PASS của Bài 8)
Gemini-khóa 3-20261008-0956.md:2477: ### Bước chuyển tiếp sang Bài 17
Gemini-khóa 4-20261008-0958.md:34: # Khóa 4 — Bài 1: VLA Model Là Cái Gì, Ở Mức Tensor?[cite: 5]
Gemini-khóa 4-20261008-0958.md:152: # Khóa 4 — Bài 2: Đo Cái Gì, Và Những Con Số Hợp Lý Trông Như Thế Nào? (3h)[cite: 5]
Gemini-khóa 4-20261008-0958.md:262: # Khóa 4 — Bài 3: Methodology — Phần Quan Trọng Nhất Của Cả Khóa (4h)[cite: 5]
Gemini-khóa 4-20261008-0958.md:386: # Khóa 4 — Bài 4: Thiết Kế Harness (5h)[cite: 5]
Gemini-khóa 4-20261008-0958.md:581: # Khóa 4 — Bài 5: Đo Model Đầu Tiên Trên GPU Thuê (5h)[cite: 5]
Gemini-khóa 4-20261008-0958.md:710: # Khóa 4 — Bài 6: Cô Lập Nhiệt Và Chứng Minh Bằng Số (4h)[cite: 5]
Gemini-khóa 4-20261008-0958.md:819: # Khóa 4 — Bài 7: LIBERO: Đo Chất Lượng Mà Không Cần Robot (5h)[cite: 5]
Gemini-khóa 4-20261008-0958.md:947: # Khóa 4 — Bài 8: Quantization: FP32 → 4-bit (6h)[cite: 5]
Gemini-khóa 4-20261008-0958.md:1070: # Khóa 4 — Bài 9: Đường Cong Pareto Và Bẫy "Nhanh Nhưng Hỏng" (5h)[cite: 5]
Gemini-khóa 4-20261008-0958.md:1198: # Khóa 4 — Bài 10: Model Thứ Hai Và Thứ Ba (6h)[cite: 5]
Gemini-khóa 4-20261008-0958.md:1310: # Khóa 4 — Bài 11: Target Thứ Hai: CPU N100, Và Con Số Gây Sốc (6h)[cite: 5]
Gemini-khóa 4-20261008-0958.md:1442: # Khóa 4 — Bài 12: Roofline: Nút Thắt Nằm Ở Đâu? (6h)[cite: 5]
Gemini-khóa 4-20261008-0958.md:1506: ### Bước 4: Kiểm chứng chéo với số đo thực nghiệm ở Bài 8
Gemini-khóa 4-20261008-0958.md:1574: # Khóa 4 — Bài 13: Viết Bài Tiếng Anh (5h)[cite: 5]
Gemini-khóa 4-20261008-0958.md:1696: # Khóa 4 — Bài 14: Làm Cho Người Khác Chạy Lại Được (4h)[cite: 5]
Gemini-khóa 4-20261008-0958.md:1816: # Khóa 4 — Bài 15: Đi Tìm Người Reproduce (3h)[cite: 5]
Gemini-khóa 5-20261008-0959.md:107: ## 4. Tiêu chí hoàn thành (Deliverable của Bài 1)
Gemini-khóa 5-20261008-0959.md:2632: # Khóa 6 Bài 1: Vì sao determinism là điều kiện tiên quyết, không phải tính năng đẹp (4h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:83: ## 4. Thực hành: Làm gì cho Bài 1?
Gemini-khóa 6-20261008-1000.md:144: # Khóa 6 — Bài 2: Dựng stack và chạy episode đầu tiên (6h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:272: # Khóa 6 — Bài 3: Săn nguồn phá determinism (8h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:414: # Khóa 6 — Bài 4: Chốt determinism vào CI (6h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:553: # Khóa 6 — Bài 5: Kịch bản không phải script (8h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:740: # Khóa 6 — Bài 6: Sinh kịch bản có hệ thống (6h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:885: # Khóa 6 — Bài 7: Provenance: Từ kết quả truy ngược về mọi thứ (6h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:1062: # Khóa 6 — Bài 8: Song song hóa và throughput thật (8h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:1184: # Khóa 6 — Bài 9: Artifact management: Output của 10.000 episode đi đâu (8h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:1325: # Khóa 6 — Bài 10: Từ run tới báo cáo (8h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:1461: # Khóa 6 — Bài 11: Định nghĩa thành công bằng toán (6h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:1621: # Khóa 6 — Bài 12: Bao nhiêu episode là đủ (8h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:1790: # Khóa 6 — Bài 13: Phát hiện regression tự động (6h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:1931: # Khóa 6 — Bài 14: Domain randomization và đo xem nó mua được gì (6h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:2066: # Khóa 6 — Bài 15: Định nghĩa gap sao cho đo được (6h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:2198: # Khóa 6 — Bài 16: Con lắc: Ba đường phải gặp nhau (8h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:2379: # Khóa 6 — Bài 17: Bảng gap theo kênh và giới hạn hiệu lực (6h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:2515: # Khóa 6 — Bài 18: CI: Đổi một thứ, nhận một phán quyết (3h)[cite: 7]
Gemini-khóa 6-20261008-1000.md:2650: # Khóa 6 — Bài 19: Publish & Gate Khóa 6 (3h)[cite: 7]
Gemini-khóa 7-20261008-1001.md:46: ## Bài 1 — Motor, encoder, driver: ba thứ phải hiểu trước khi cấp điện (Khóa 7A)[cite: 9]
Gemini-khóa 7-20261008-1001.md:172: ## Bài 2 — Đường cong PWM → vận tốc, và vùng chết (Khóa 7A)[cite: 9]
Gemini-khóa 7-20261008-1001.md:274: ## Bài 3 — PID vận tốc bánh xe và jitter vòng lặp (Khóa 7A)[cite: 9]
Gemini-khóa 7-20261008-1001.md:403: ## Bài 4 — Odometry và hiệu chuẩn UMBmark (Khóa 7A)[cite: 9]
Gemini-khóa 7-20261008-1001.md:533: ## Bài 5 — Ghi dữ liệu và nối vào hạ tầng Khóa 5 (Khóa 7A)[cite: 9]
Gemini-khóa 7-20261008-1001.md:673: ## Bài 6 — Chọn đường: marker hay lidar (Khóa 7B)[cite: 9]
Gemini-khóa 7-20261008-1001.md:796: ## Bài 7 — Hiệu chuẩn camera và độ chính xác pose từ marker (Khóa 7B)[cite: 9]
Gemini-khóa 7-20261008-1001.md:909: ## Bài 8 — Hợp nhất odometry và marker (Khóa 7B)[cite: 9]
Gemini-khóa 7-20261008-1001.md:1072: ## Bài 9 — Nav2: từ A tới B (Khóa 7B)[cite: 9]
Gemini-khóa 7-20261008-1001.md:1231: ## Bài 10 — Ghi và phân tích session điều hướng (Khóa 7B)[cite: 9]
Gemini-khóa 7-20261008-1001.md:1379: ## Bài 11 — Thiết kế quyền riêng tư trước khi viết dòng code nào (Khóa 7C)[cite: 9]
Gemini-khóa 7-20261008-1001.md:1513: ## Bài 12 — Pipeline nhận diện và đo FAR/FRR (Khóa 7C)[cite: 9]
Gemini-khóa 7-20261008-1001.md:1660: ## Bài 13 — Đăng ký, xóa dữ liệu, và audit log (Khóa 7C)[cite: 9]
Gemini-khóa 7-20261008-1001.md:1802: ## Bài 14 — Tích hợp nhận diện vào điều hướng (Khóa 7C)[cite: 9]
Gemini-khóa 7-20261008-1001.md:1977: ## Bài 15 — An toàn là một tầng phần cứng (Khóa 7D)[cite: 9]
Gemini-khóa 7-20261008-1001.md:2154: ## Bài 16 — State machine và phân tích chế độ hỏng (Khóa 7D)[cite: 9]
Gemini-khóa 7-20261008-1001.md:2319: ## Bài 17 — Soak 72 giờ trong văn phòng thật (Khóa 7D)[cite: 9]
Gemini-khóa 7-20261008-1001.md:2469: ## Bài 18 — Dựng mô hình sim khớp với robot thật (Khóa 7E)[cite: 9]
Gemini-khóa 7-20261008-1001.md:2624: ## Bài 19 — HIL và CI cho hành vi robot (Khóa 7E)[cite: 9]
Gemini-khóa 7-20261008-1001.md:2808: ## Bài 20 — Sim có dự đoán được thực tế không? (Khóa 7E)[cite: 9]
Gemini-khóa 7-20261008-1001.md:2969: ## Bài 21 — Vòng đời dữ liệu đầy đủ và fine-tune (Khóa 7E)[cite: 9]
```
