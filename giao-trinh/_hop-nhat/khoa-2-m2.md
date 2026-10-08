# Nhật ký hợp nhất — Khóa 2 · Module 2 (`khoa-2/m2-dataset-audit.md`), đơn vị m-k2b

Ngày: 2026-10-08. Nguồn: `khoa-2-du-lieu-robot-khong-can-robot.md` dòng 678–1155. Bản C = `giao-trinh/khoa-2/m2-dataset-audit.md` (Bài 9–12), bản K = `giao-trinh-kiro/khoa-2/m2-dataset-audit.md` (Bài 9–15 + Gate).

**Kiểm chung:** source `huggingface/lerobot` nhánh main (commit 40e47be, 10/2026) được clone thưa để kiểm format: `CODEBASE_VERSION = "v3.0"`; `DEFAULT_DATA_PATH`, `DEFAULT_VIDEO_PATH`, `DEFAULT_TASKS_PATH = meta/tasks.parquet` (`utils.py`); mặc định 100 MB data / 200 MB video / 1000 file mỗi chunk; `add_frame` luôn gán `timestamp = frame_index / fps` và docstring cấm người gọi truyền `timestamp` (`dataset_writer.py`); `tolerance_s = 1e-4` (`lerobot_dataset.py`), quá dung sai ném `FrameTimestampError` (`video_utils.py`); docs v3 vẫn ghi `meta/tasks.jsonl` (docs và code bất đồng). Blog/release: v3.0 công bố 09/2025, ra cùng `lerobot` 0.4.0 (10/2025). HF Hub bị chặn từ môi trường hợp nhất, nên các số đo trên `data/lerobotpusht`, `data/libero` (chỉ có trên máy Kiro, thư mục gitignore) **không chạy lại được**; giữ nhãn `[tự đo]`. Mọi khối `# [đã chạy]` của bản cuối (7 khối) đã chạy lại trong `_scratch/m-k2b/` trên Python 3 + numpy 2.5 + scipy 1.18 + pyarrow 25, dataset v3.0 giả (3 episode, mp4 libx264) tự sinh; số ra khớp bảng trong bài.

**Độ dài:** đếm từ có chữ (không tính ký hiệu bảng), không tính code Python: Bài 9 ≈ 4 120, Bài 10 ≈ 3 890, Bài 11 ≈ 4 340, Bài 12 ≈ 4 280, Bài 13 ≈ 3 430, Bài 14 ≈ 1 980, Bài 15 ≈ 1 270. Tính cả code, Bài 11 ≈ 4 700, Bài 12 ≈ 4 830. Bản C Bài 11 gốc ~8 000 từ đã phải rút gần một nửa.

---

## Đầu module
- Ghép: bảng Bài → giờ → viên nang → quyết định (K) vào phần mở đầu của C. Đổi mục "timestamp được tính" ở đầu module thành câu hỏi để không lộ đáp án Bài 9.
- Ghi chú về dữ liệu `data/` (gitignore, chưa ghim revision) và vai trò `lerobot/robomme`.

## Bài 9 — LeRobot dataset format từ zero
- **Bản nền: C.** Kiểm chứng source tốt hơn (`add_frame`, `tolerance_s`, ba mức đếm ffprobe), checker v3 có kiểm **tổng theo file** (bắt frame thừa), mô hình "ảnh tra bằng thời gian".
- **Ghép từ K:** bảng tham số `info.json` thật của pusht/libero; bảng dự đoán K1–K8; kết quả đo trên `data/` (file parquet 1/377, ba điều bất ngờ); bước float32 ($2^{-18}$ s ở 50 s); câu hỏi ngược "bộ chuyển đổi bị kill" (gộp vào câu Failure mode) và "fps int vs float"; liên kết BAM/BAI.
- **Mâu thuẫn:** (1) K: `add_frame` tính timestamp "khi không truyền"; C: luôn tính, cấm truyền. Source main 10/2026: C đúng; bản cũ có thể cho truyền → ghi `[tự đo]` theo phiên bản. (2) Video 200 MB (C, mặc định code) vs 500 MB (K, `info.json` thật): cả hai đúng ở tầng của mình; `info.json` thắng.
- **Lỗi kỹ thuật đã sửa:** checker C bổ sung lọc `N/A` khi đọc pts (K có, C thiếu; packet thiếu pts làm `float()` crash). Bỏ khối pyarrow của K để giữ độ dài (nội dung gộp vào bước 3).

## Bài 10 — Kiểm tra bằng tay trước khi tự động hóa
- **Bản nền: K.** Đúng hơn ở điểm then chốt: phải biết **action space** trước khi so action với state. Script khảo sát của C chồng `action[j]` lên `state[j]` mặc định cùng đại lượng (sai với libero, action delta EEF); script K tách `dt` theo episode.
- **Ghép từ C:** chấm mô hình K3 lượt 21 và mô hình "giao VLM xem video"; bước ghi LSB thực tế và vẽ `|diff(state)|`; bảng "thường gặp với robot thật" (gripper giữ, lag 1–3 frame); câu hỏi gripper 12 s, rule of three, Hanny's Voorwerp; liên kết Levey–Jennings. Script: của K + phần in LSB và chạy đứng yên dài nhất của C (đã chạy lại).
- **Mâu thuẫn:** không có về sự thật.
- **Lỗi kỹ thuật đã sửa:** C — script giả định action/state cùng số chiều, cùng đại lượng (thêm kiểm, nhánh `diff(state)`).

## Bài 11 — Bảy lớp lỗi: định nghĩa và toán
- **Bản nền: C** (oracle, ba trạng thái phán quyết, toán $P_\text{same}$, mô phỏng L2 rớt frame "vô hình" và L5 vị trí vs sai phân, ngưỡng Wilson). Rút từ ~8 000 xuống ~4 340 từ prose: bỏ câu hỏi ngược lồng trong từng lớp, bỏ chép lại `best_lag` gốc, gộp bảng L7.
- **Ghép từ K:** bài tập chạy **nguyên văn** bảy định nghĩa gốc trên `data/` và bảng kết quả (L1 báo giả đúng N − 1 vì quên tách episode; L5 chạm biên ở 1 693 episode libero; L6 báo ~15 % frame ở kênh kẹp); $g$ theo action space cho L5; kênh hai chế độ ở L6; `len(names)` vs `shape` ở L7; cột FP/FN trong bảng tóm tắt; câu hỏi camera trễ 66 ms ("lớp thứ tám"); tự kiểm tra tick encoder 4 096.
- **Mâu thuẫn:** L3 hậu quả frame thiếu ở giữa — C: "im lặng, sai nội dung"; K: "có thể chỉ lặp/nhảy cục bộ". Kiểm `video_utils.py`: phụ thuộc pts — nếu pts sau chỗ lệch vẫn đều trên lưới thì im lặng (C đúng); nếu pts có khoảng trống thì truy vấn vượt `tolerance_s` và ném lỗi. Ghi cả hai chế độ.
- **Lỗi kỹ thuật đã sửa (C):** bảng $P_\text{same}$ — cột phải ghi "giá trị thật nằm giữa hai mức" nhưng số (1,00/0,69/0,05) là của $x = 0$, tâm một mức (giữa hai mức cho ≈ 0; đã tính lại). Câu (a): lệch dt tối đa "0,34 %" → 0,39 % (chạy lại: dt ∈ [0,033203; 0,033447]). Script L3 của K chỉ đếm theo cửa sổ, **không** bắt frame thừa (đã thử trên dataset giả: 0 lệch dù file thừa 1 frame) → dùng checker Bài 9 có kiểm tổng theo file.

## Bài 12 — Viết detector và đo chính detector bằng lỗi tiêm vào
- **Bản nền: C** (quét $W$ của L4 so định nghĩa gốc và sửa, equivalent mutant, Kepler injection–recovery, EER, exit code 0/1/2, schema JSON). Hai bản gần ngang nhau.
- **Ghép từ K:** bảng ba tầng kiểm; công thức Wilson (C hẹn "hàm Wilson ở Bài 13" nhưng C không có Bài 13); mô phỏng L1/L2 TPR/FPR có CI (phát hiện "TPR lùi 10 ms ≈ FPR"); canary lỗi cố ý ở runtime; mutation testing trên code detector; test "không áp dụng"; tiêu chí chọn ngưỡng viết trước; bảng tiêu chí hoàn thành; phân bổ giờ; chấm mô hình "server mock + golden dataset là đủ".
- **Mâu thuẫn:** không về sự thật. Số chạy lại: quét L4 (seed 1) và bảng L1/L2 (seed 7) khớp từng ô; Wilson 0/50 = 7,1 %, 0/200 = 1,9 %, 0/30 = 11 %, 0/400 = 0,95 %, 47/50 = [0,84; 0,98], 2/300 = [0,2 %; 2,4 %].
- **Lỗi đã sửa:** C — chấm mô hình EER dẫn con số "EER ở W ≈ 0,75 s" ngoài khối 🔒 (lộ kết quả) → viết lại không có số. K — "FPR ≤ 1 % cần ~300 episode" đúng theo rule of three nhưng Wilson cần ~380 → ghi cả hai.

## Bài 13 — Chạy trên dataset thật (chỉ K)
- **Bản nền: K.** Kiểm và sửa theo A–H.
- Đã kiểm: E[FP] = 1 899 × 7 × 0,005 ≈ 66; Bonferroni 0,05/13 293 ≈ 3,8·10⁻⁶; đáp án tự kiểm tra E[FP] ≈ 20 [10; 40]; script reproduce `next.*` chạy trên dataset giả có cột `next.*` (in đúng vị trí done (−2, −1)). Dead salmon, GWAS 5·10⁻⁸, Reinhart *Statistics Done Wrong*, Gelman & Loken: có thật.
- **Đã sửa:** thêm khối tiêu chí hoàn thành của bản gốc (≥1 lỗi thật xác nhận, reproduce máy sạch, tỉ lệ dự đoán đúng) — K chỉ để ngầm; hạ "50–70 % dự đoán đúng là bình thường" xuống `[ước lượng]`; chấm mô hình trỏ "Northcutt (Bài 11)" nhưng Bài 11 bản cuối không còn Northcutt → viết đầy đủ trích dẫn tại chỗ; thêm F2.8 vào "Cần trước".

## Bài 14 — Report, publish, báo lỗi (chỉ K, khung rút gọn)
- **Bản nền: K.**
- **Đã sửa:** bỏ tên một repo prior art cụ thể (`lerobot-doctor`) không xác minh được (GitHub search bị chặn từ môi trường), thay bằng các hàm `validate_*` có thật trong `src/lerobot/datasets/feature_utils.py` làm phản ví dụ cho "tool đầu tiên"; thêm bảng tiêu chí hoàn thành của bản gốc (report tự chứa, README, link báo lỗi, gate 60 ngày); ghi gộp độ tin cậy và hợp nhất. Độ dài ~1 980 từ, vượt mục tiêu khung rút gọn (500–1 200) nhưng dưới trần đơn vị.

## Bài 15 — Bài viết tiếng Anh (chỉ K, khung rút gọn)
- **Bản nền: K.** Đã sửa: khôi phục tiêu đề gốc *Auditing LeRobot datasets: what breaks and how to detect it* (K đổi tiêu đề), giữ biến thể của K làm gợi ý; sửa liên kết Northcutt.

## Gate Module 2 (chỉ K)
- **Bản nền: K.** Đối chiếu đủ năm tiêu chí gốc, ngân sách 60h, trần 85h; FAIL action và "đã sửa" của K giữ nguyên; khớp với Bài 12–13 sau hợp nhất.

---

## Nhận xét hai bên
- **C mạnh:** kiểm chứng bằng source thật (đúng ở `add_frame`, `tolerance_s`), chiều sâu toán (oracle, $P_\text{same}$, prewhitening, Wilson theo cận), mô phỏng có ý nghĩa. **C yếu:** quá dài (Bài 11 ~8 000 từ), vài lỗi nhãn/số nhỏ, script Bài 10 mặc định cùng đại lượng, lộ một số ngoài khối 🔒.
- **K mạnh:** đo thật trên dữ liệu thật (`data/`), phát hiện thực nghiệm sắc (L1 = N − 1, action delta làm L5 vỡ, kênh hai chế độ, `next.*` của pusht), cấu trúc đo detector (ba tầng, canary, Wilson), đủ Bài 13–15 + Gate với giọng báo lỗi chuẩn. **K yếu:** khẳng định về API dựa trên quan sát dữ liệu thay vì source (`add_frame`), script L3 thiếu kiểm tổng theo file, một tên repo không xác minh, một số mốc không nhãn.
