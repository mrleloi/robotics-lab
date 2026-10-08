# Brief cho agent HỢP NHẤT (Claude × Kiro)

Repo: `/home/user/robotics-lab` (GỐC). Hai nhóm đã soạn độc lập cùng một bộ giáo trình theo cùng quy chuẩn:
- Bản Claude: `GỐC/giao-trinh/khoa-N/<file>.md`
- Bản Kiro: `GỐC/giao-trinh-kiro/khoa-N/<file>.md` (cùng tên file)

Bạn tạo **bản cuối cùng** cho đơn vị được giao, ghi vào `GỐC/giao-trinh/khoa-N/<file>.md` (ghi đè bản Claude). Bạn vừa là người hợp nhất vừa là **reviewer độc lập của cả hai bản**: không tin bên nào.

## Đọc trước
1. TRỌN `GỐC/giao-trinh/_QUY-CHUAN.md` (hợp đồng) và `GỐC/giao-trinh/_PHOI-HOP.md` (mục 3 là quy trình hợp nhất).
2. `GỐC/giao-trinh/_ref/brief-reviewer.md`: các mục kiểm A–H áp dụng cho bản cuối của bạn.
3. `GỐC/giao-trinh/_ref/cau-hoi-cua-ban-trong-gemini.md` (giọng và mô hình của người học).
4. Phần nguồn trong file khóa gốc `GỐC/khoa-N-*.md` (số dòng ở `GỐC/giao-trinh/_ref/muc-luc-bai-goc.md`). Bản cuối phải giữ đủ bước Làm, tiêu chí PASS/FAIL, FAIL action, giờ của gốc.
5. Liên kết sang Khóa 7 phải dùng mã mới `K7 Cn.m` theo `GỐC/giao-trinh/khoa-7/_KE-HOACH-K7.md` (mục 3). Sửa mọi liên kết kiểu "K7 Bài N" trong hai bản sang mã mới.

## Làm từng bài, theo thứ tự trong file
- Bài chỉ có **một** bản → dùng nó, kiểm và sửa theo brief-reviewer A–H.
- Bài có **hai** bản → chọn bản nền, ghép phần mạnh của bản kia, giải mâu thuẫn về sự thật (theo `_PHOI-HOP.md` mục 3).
- Bài **không bên nào có** → soạn mới theo `GỐC/giao-trinh/_ref/brief-writer.md`.
- Chạy lại mọi khối Python `# [đã chạy]` của bản cuối (python3 có numpy/scipy/matplotlib; `MPLBACKEND=Agg`) trong scratchpad riêng `GỐC/giao-trinh/_scratch/<mã đơn vị>/` (đã gitignore).

**Cách ghi file lớn:** đừng giữ cả file trong một lần Write. Ghi ra file tạm `GỐC/giao-trinh/_scratch/<mã>/final.md` từng bài một (Write bài đầu, rồi nối thêm từng bài bằng Edit hoặc `cat >>`), cuối cùng copy đè lên file đích. Khi một bài của bản nền đã tốt và chỉ cần vài chỗ ghép/sửa, có thể trích nguyên đoạn bằng script (theo tiêu đề `## Bài N`) rồi Edit tại chỗ thay vì gõ lại.

## Nhật ký
Ghi `GỐC/giao-trinh/_hop-nhat/khoa-N-<mã đơn vị>.md`: mỗi bài một mục ngắn:
- Bản nền: C / K / mới. Vì sao.
- Đã ghép từ bản kia: …
- Mâu thuẫn sự thật và cách giải: …
- Lỗi kỹ thuật đã sửa (ghi bản nào mắc): …

## Không được
- Không sửa `giao-trinh-kiro/`, file gốc, `_ref/`, `_QUY-CHUAN.md`, file của đơn vị khác. Không git commit/push.

## Trả về (≤300 từ)
- FILES đã ghi (+ `wc -w`)
- Mỗi bài: bản nền C/K/mới, một dòng
- LỖI KỸ THUẬT đã sửa (bản nào, chỗ → sai → đúng)
- MÂU THUẪN giữa hai bản và cách giải
- CÒN NGHI NGỜ
- NHẬN XÉT ngắn: bên nào mạnh ở điểm gì (để người điều phối chỉnh brief cho đợt sau)
