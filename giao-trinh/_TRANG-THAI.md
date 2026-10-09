# TRẠNG THÁI CÔNG VIỆC — bàn giao cho phiên sau

> **CẬP NHẬT 2026-10-09 (session 3, dừng vì hết usage).** Đã merge `main` (K4 của Kiro). Viết thêm: `khoa-7/00-tong-quan.md`, `README.md`, K4 Bài 5, K5 Bài 5, Bài 10, Bài 16 (các bài này đủ khung, kết thúc gọn). Agent bị dừng giữa chừng — **còn thiếu chính xác:**
> - K4: Bài 6 (cuối `khoa-4/m2-harness.md`), Bài 12 (cuối `khoa-4/m4-nhieu-target.md`).
> - K5: Bài 6 (cuối `m1-cam-bien.md`); Gate Module 0 (port từ `giao-trinh-kiro/khoa-5/m0-chon-phan-cung.md`); Bài 11, 12 (cuối `m2-dong-bo-thoi-gian.md`; Bài 7 trỏ tới `b12_budget.py` của Bài 12); Bài 17 (cuối `m3-data-stack.md`) + hai sửa nhỏ m3 trong `_hop-nhat/ghi-chu-cho-K4-K5.md` (có thể agent đã áp một phần — kiểm `git diff`); `m4-van-hanh.md` (Bài 18, 19, Gate K5) chưa tạo; `khoa-5/00-tong-quan.md` chưa có.
> - Sau khi K5 đủ: cập nhật bảng trạng thái trong `README.md` (đang ghi K4/K5 "đang soạn").
> - Câu hỏi mới chờ người học: đường lõi tối thiểu K7 không có C8 nhưng C11.3 cần Nav2 → thêm C8 tối thiểu (~360–370h) hay đổi C11.3 (ghi trong `khoa-7/00-tong-quan.md`).
> - Lời giao mẫu cho từng việc còn thiếu: dùng lại prompt kiểu "w-k4 / w-k5a / w-k5b / w-k5c" — đọc `_ref/brief-writer.md`, nối bài vào cuối file, KHÔNG sửa bài đã có, áp `_hop-nhat/ghi-chu-cho-K4-K5.md` và quy chuẩn mục 7 (Bài 11 rolling shutter (t_pulse+t_exp)/t_row; Bài 12 N100 ~0,19–0,22 TFLOPS CPU, decode batch 1 memory-bound).

> Cập nhật: 2026-10-08, cuối session 2 (Claude). Branch: `claude/quirky-allen-21hvip`.
> Dừng chủ động vì gần hết credit cloud (còn ~20 USD / 250 USD). Đọc file này rồi `_PHOI-HOP.md` trước khi làm tiếp.

## 0. Bối cảnh ngắn

- Hợp đồng: `_QUY-CHUAN.md` (bản thống nhất với Kiro), kế hoạch K7: `khoa-7/_KE-HOACH-K7.md` (mục 9 = quyết định đã chốt khi soạn: pin 4S LiFePO4, buck-boost 12 V ≥5 A, shunt 50 A/75 mV, relay 5 chân có 87a, JGB37-520 1:56 bánh 85 mm, thuật ngữ dòng hãm/dòng phanh…).
- Chia việc với Kiro: `_PHOI-HOP.md`. Kiro viết K4, K5; Claude hợp nhất. Bản cuối nằm ở `giao-trinh/`.
- Briefs: `_ref/brief-writer.md` (có mục "Bổ sung sau đợt 1": cấm đổi ngưỡng gate, mọi "mô phỏng sẽ thấy" phải chạy thật…), `_ref/brief-merger.md`, `_ref/brief-reviewer.md`, `_ref/brief-F.md`.
- Nhật ký hợp nhất/review: `_hop-nhat/` (gồm `ghi-chu-cho-K4-K5.md` — lỗi K4/K5 do các agent F phát hiện, PHẢI áp khi hợp nhất K4/K5).
- Bài học vận hành: chạy ≤6 agent/lượt; một agent soạn ~250–600k token. Ngân sách session 2 (~230 USD) đủ cho khoảng 40 lượt agent.

## 1. Đã xong

| Phần | Trạng thái | Ghi chú |
|---|---|---|
| K1 (tổng quan + 4 phần, Bài 1–14) | ✅ hợp nhất C×K | `_hop-nhat/khoa-1.md` |
| K2 (tổng quan + m1 Bài 1–8b + Gate, m2 Bài 9–15 + Gate) | ✅ hợp nhất | số đo trên `data/` (pusht, libero) còn `[tự đo]` — chạy lại trên máy |
| K3 (tổng quan + m1–m4, Bài 1–17 + Gate) | ✅ hợp nhất | m4 Bài 14–17 dài 5,4–6,4k từ |
| K6 (tổng quan + m1–m6, Bài 1–19 + Gate) | ✅ viết + review độc lập (`_hop-nhat/review-khoa-6.md`) | Bài 13 & 18 cùng quy tắc verdict, CI Newcombe |
| F1–F7 (khóa nền, 245h) | ✅ viết xong | **chỉ F4 bị review dở** (vài sửa nhỏ, đã giữ). F1, F2, F3, F5, F6, F7 **chưa review độc lập** |
| K7 C0–C12 (khóa build mới) | ✅ viết xong cả 13 chặng | C0–C1 đã review an toàn (`_hop-nhat/review-khoa-7-c00-c01.md`). C2–C12 **chưa review** |

## 2. Còn lại — theo thứ tự ưu tiên

1. **K4, K5: chờ Kiro.** Kiểm `giao-trinh-kiro/khoa-4`, `khoa-5` trên `main`. Khi đủ: hợp nhất theo `_ref/brief-merger.md` (bản Claude có K4 m1, m3, m4 Bài 10, m5; K5 m0, m1 Bài 3–4, m2 Bài 7–9, m3 Bài 13–15), áp `_hop-nhat/ghi-chu-cho-K4-K5.md`. Mỗi module 1 agent. Còn thiếu `00-tong-quan.md` của K4, K5.
2. **Review an toàn K7 C2–C5** (motor quay lần đầu, cấp điện cả robot) — agent đã bị dừng trước khi sửa gì. Đề bài đầy đủ: xem lời giao `r-k7b` dưới đây (mục 3). Phải thống nhất với C10.1: chân RELAY_HOLD là GPIO đảo bằng phần mềm (KHÔNG LEDC); bảng chân C4.1 dành chân VM_SENSE, RELAY_FB (87a), RESET, PRECHARGE.
3. **Review K7 C8–C10** (robot tự đi gần người, dữ liệu khuôn mặt, E-stop) — bị dừng trước khi sửa gì.
4. **`khoa-7/00-tong-quan.md`** — chưa viết. Nội dung theo `_KE-HOACH-K7.md` cuối mục 8; trần giờ FAIL action K7 gốc 450h cần cập nhật theo ngân sách mới (C9 và C7 đã ghi đề xuất).
5. **`giao-trinh/README.md`** — mục lục tổng, ngân sách giờ: K1–K6 545h; K7 mới lõi 561h → 1.106h (≈3,3 năm ở 6,5h/tuần); đường lõi tối thiểu 885h; khóa nền F trọn 245h (học đúng lúc thì ít hơn).
6. **Review độc lập F1, F2, F3, F5, F6, F7, K7 C11–C12** + cắt độ dài (F6 ~39,6k từ là dài nhất; F6.3 ~6,2k).
7. **Kiểm liên kết chéo toàn bộ** (mã `→ Fx.y`, `→ K7 Cn.m`, `→ Kn Bài m` trỏ đúng chỗ có thật) — có thể làm bằng script grep, rẻ.

## 3. Lời giao mẫu cho các việc đang dở

- **r-k7b:** "Đọc `_ref/brief-reviewer.md`, `khoa-7/_KE-HOACH-K7.md` (mục 2,5,6,9), `_hop-nhat/review-khoa-7-c00-c01.md`. Kiểm AN TOÀN + kỹ thuật `khoa-7/c02…c05`: back-EMF khi quay tay motor, GND chung USB laptop–pack, chân strapping ESP32-S3 làm motor giật lúc boot/flash, PWM mặc định khi reset, phanh gấp lật xe; tính chọn motor C2.1, PCNT accum_count/watch point, chân DevKitC-1 N8R8; thống nhất với C10.1 (RELAY_HOLD không LEDC, 4 chân thêm). Ghi `_hop-nhat/review-khoa-7-c02-c05.md`."
- **r-k7c:** "… kiểm `c08`, `c09`, `c10`: mạch E-stop C10.1 (Vg xung giữ vs Vgs(th), công suất R tiền nạp 100 Ω, TPS3823 WDI), dừng loại 0/1/2 IEC 60204-1/ISO 13850, OpenCV ArUco API theo phiên bản, luật 91/2025 + NĐ 356/2025, giấy phép InsightFace/YuNet/SFace, sự cố Cruise 2023/Knightscope/Therac-25. Ghi `_hop-nhat/review-khoa-7-c08-c10.md`."

## 4. Câu hỏi đang chờ người học quyết

- Ghi rõ diễn giải `CONVENTIONS.md` mục 7 (vòng điều khiển trong ESP32; USB dùng giao thức tối thiểu có spec + test; ROS dùng `ros2_control`) và thêm màu dây INT vào quy ước — file gốc của người học, Claude không tự sửa.
- Độ dài: K6 mỗi bài ~4,7–5,1k từ tính cả code; muốn ≤4,5k phải bỏ một mô phỏng (vd. mô phỏng 3 Bài 6). Mặc định: giữ.
- Các quyết định agent tự đưa ra cần người học duyệt: K6 Bài 14 tạo policy ở mỗi λ bằng random search/CEM; C9 tốc độ thử gần người ≤0,3 m/s, cấm phát audio khi robot chạy; C11.5 ứng viên fine-tune mặc định là bộ dự đoán quãng dừng (không cần dữ liệu cá nhân).

## 5. Ghi chú kỹ thuật

- `giao-trinh/_scratch/` (gitignore) còn vài thư mục nháp rỗng/cũ — xóa tay được, không ảnh hưởng.
- `.gitignore` đã thêm `__pycache__/`.
