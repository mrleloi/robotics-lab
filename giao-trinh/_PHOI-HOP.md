# PHỐI HỢP HAI NHÓM SOẠN — Claude (`giao-trinh/`) và Kiro (`giao-trinh-kiro/`)

> Cập nhật: 2026-10-08. Đọc file này trước khi soạn hoặc hợp nhất bất cứ thứ gì. Kiro và Claude đều đọc được (repo chung, đẩy qua git).

## 1. Hợp đồng chung

- **Quy chuẩn duy nhất:** `giao-trinh/_QUY-CHUAN.md`. Đây là bản quy chuẩn của Kiro (có mục 4c Khóa 7 cho người mới và mục 9 quy tắc agent), chỉ sửa đường dẫn để chạy được ở cả hai môi trường. `giao-trinh-kiro/_QUY-CHUAN.md` giữ nguyên làm lịch sử; nếu hai bản lệch nhau, **bản trong `giao-trinh/` thắng**.
- **Kế hoạch K7 duy nhất:** `giao-trinh/khoa-7/_KE-HOACH-K7.md` (bản Kiro, giữ nguyên mã chặng `C0–C12` và mã bài `Cn.m`).
- **Tên file giống hệt nhau ở hai cây** (theo mục 8 quy chuẩn). Claude đã đổi tên file của mình cho khớp Kiro (`a-nen.md` → `phan-a-nen.md`, `m2-do-do-tre.md` → `m2-do-tre.md`, `m3-tts.md` → `m3-tts-kien-truc.md`, `m3-chat-luong.md` → `m3-truc-chat-luong.md`, `m4-nhieu-model-target.md` → `m4-nhieu-target.md`, `m4-danh-gia.md` → `m4-danh-gia-regression.md`). Nhờ vậy, so hai bản của cùng một bài chỉ cần mở cùng đường dẫn ở hai thư mục.
- **Bản cuối cùng nằm ở `giao-trinh/`.** `giao-trinh-kiro/` là nguồn đầu vào cho bước hợp nhất, không ai sửa ngược vào đó ngoài Kiro.
- K7 cũ (7A–7E) của Claude đã chuyển vào `giao-trinh/khoa-7/_nguyen-lieu-cu/`. Chỉ dùng làm nguyên liệu cho bài khái niệm (PID, odometry, Kalman, FAR/FRR, FMEA, HIL, MPC).

## 2. Chia việc (tránh hai bên viết trùng)

| Phần | Ai viết mới | Ai kiểm chéo / hợp nhất |
|---|---|---|
| K1, K2, K3 | Kiro đã xong gần hết; Claude có một phần | **Claude hợp nhất** từng bài (đợt 1) |
| K4, K5 | **Kiro** đang viết (đã có scratch K4-a/b, K5-a/b/c). Claude **không viết thêm** bài K4/K5 | Claude hợp nhất khi Kiro đẩy bản đủ |
| K6 | **Claude** viết các bài còn thiếu (Bài 5–7, 12–14, 17–19, Gate) | Kiro kiểm chéo nếu còn quota |
| F1–F7 | **Claude** | Kiro kiểm chéo nếu còn quota |
| K7 C0–C12 (khóa build mới) | **Claude**, theo `_KE-HOACH-K7.md` | Kiro kiểm chéo, ưu tiên C0, C1 (an toàn pin, điện) |
| `00-tong-quan.md` các khóa, `README.md` tổng | Claude, viết sau khi khóa đủ bài | — |

Nếu Kiro muốn đổi phần việc (ví dụ đã lỡ viết F hoặc K6), ghi một dòng vào mục 4 bên dưới rồi đẩy lên; bên còn lại đọc trước khi bắt đầu đợt mới.

## 3. Quy trình hợp nhất một bài có hai bản

1. Đọc trọn cả hai bản của bài.
2. Chọn **bản nền** theo thứ tự: đúng kỹ thuật → chiều sâu bản chất (vì sao thứ này tồn tại, chấm mô hình có phản ví dụ) → niêm phong đáp án sạch → câu hỏi ngược thật sự mở → code chạy được → giữ đủ xương sống bản gốc.
3. **Ghép từ bản kia** những gì bản nền thiếu: câu chuyện thật tốt hơn, một lỗi bản kia đã phát hiện, một mô phỏng, một câu hỏi ngược sắc, một dòng "Nếu ra khác". Không ghép trùng ý. Bài sau hợp nhất có thể dài hơn mức mục tiêu một chút, nhưng không gấp đôi.
4. Hai bản **mâu thuẫn về sự thật** (con số, công thức, API): tự kiểm (tính, chạy Python, web), chọn bản đúng, ghi lại.
5. Ghi nhật ký vào `giao-trinh/_hop-nhat/khoa-N.md`: mỗi bài một mục gồm bản nền (C/K), phần đã ghép, mâu thuẫn và cách giải, lỗi tìm thấy ở từng bản. Nhật ký này cũng là phản hồi cho người học biết mỗi bên mạnh/yếu ở đâu.

## 4. Ghi chú qua lại giữa hai nhóm

- (Claude, 2026-10-08) Đã thống nhất quy chuẩn và tên file như mục 1. Đợt 1: hợp nhất K1–K3, viết K6 còn thiếu. Đợt 2: F1–F7. Đợt 3: K7 C0–C12. K4/K5 chờ Kiro.
