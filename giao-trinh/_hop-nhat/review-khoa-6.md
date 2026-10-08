# Review độc lập — Khóa 6, đơn vị r-k6

Ngày: 2026-10-08. Phạm vi: `khoa-6/m2-kich-ban.md` (Bài 5–7 + checklist), `khoa-6/m4-danh-gia-regression.md` (Bài 12–14 + checklist; Bài 11 không sửa), `khoa-6/m5-sim-to-real.md` (Bài 17), `khoa-6/m6-ci-publish.md` (Bài 18, 19, Gate). Nguồn đối chiếu: `khoa-6-sim-eval-infra.md` dòng 262–392, 548–1033. Không commit.

## 1. Nhất quán quy tắc phán quyết Bài 13 ↔ Bài 18
- Bài 18 trước đó minh họa verdict bằng CI **Wald**, Bài 13 dùng **Newcombe**: cùng quy tắc nhưng một PR ở biên có thể nhận hai verdict khác nhau. Đã thống nhất về **Newcombe** (ghép hai khoảng Wilson), dùng cùng một hàm ở cả hai bài. Quy tắc chung: FAIL nếu cận trên CI 95% của Δ < 0; PASS nếu không FAIL và cận dưới ≥ −δ (Bài 18: δ = MDE); còn lại INCONCLUSIVE; ERROR khi phép so không hợp lệ.
- Viết lại `b18_verdict.py` theo Newcombe và chạy lại: −MDE PASS 2.3% → 2.6%, −MDE/2 PASS 27.6% → 28.1%; các ô khác giữ nguyên trong ±0.5 điểm %. Kiểm thêm: N = 624 → A/A PASS 95.0% (khớp công thức z_β = 1.645).
- Bài 13: bỏ ghi chú "Bài 18 minh họa bằng Wald"; Bước 2 ghi rõ dùng cùng hàm Newcombe. Bài 18 phần Dự đoán A: N tính bằng công thức non-inferiority của Bài 13 câu 2 (code vẫn dùng đúng công thức đó), không phải "công thức hai tỉ lệ Bài 12".
- Lỗi mới phát hiện (Bài 18): "≈53% ít nhất một biến thể vô dụng báo cải thiện" chỉ đúng khi mỗi biến thể so với một lần chạy baseline riêng. Mô phỏng 30 biến thể so với **cùng** một baseline ra ≈26%. Đã thêm vào code, sửa phần 7 và Chấm mô hình.
- Bài 18: "12–19/20 lần PASS (Wilson)" → đây là khoảng 95% của Bin(20, 0.8), không phải Wilson.

## 2. Trích dẫn đã kiểm
- Henderson et al. 2018 (hai nhóm 5 seed cùng cấu hình khác nhau có ý nghĩa): đúng. Button et al. 2013 (power trung vị ~21%): đúng; thân bài đổi "khoảng 20%" → "khoảng 21%".
- Tan et al. RSS 2018 (Minitaur; system ID actuator + mô hình độ trễ, rồi randomize): đúng. Hwangbo et al. 2019, Science Robotics 4(26): đúng; thêm tên bài.
- Columbia/Crater: tra web, con số "tối đa ~640 lần" (≈1.920 vs 3 inch khối) và "ước lượng tốt nhất ~400 lần" được trích từ CAIB; thân bài ghi "hàng trăm lần (tối đa ~640, tốt nhất ~400)". Chưa mở được PDF CAIB (proxy chặn nasa.gov) để xác nhận chương/trang → ghi "tự kiểm" ở phần 11.
- VW: EPA NOV 18/9/2015, NOx tới ~40× giới hạn, WVU/ICCT 2014: đúng.
- Claude 3.7 Sonnet system card (2/2025, special-casing test trong môi trường lập trình agent) và METR *Recent Frontier Models Are Reward Hacking* (5/6/2025, sửa test/scoring code, lục call stack lấy đáp án): xác nhận qua web; thay "[chuẩn; kiểm lại nguồn bạn đọc]" bằng mô tả cụ thể.
- Hướng dẫn FDA non-inferiority 2016: không chắc văn bản dùng chữ "biocreep" → hạ giọng (biocreep là chủ đề của lĩnh vực, không gán cho văn bản FDA).
- Bài 12: câu "eval robot 20–50 episode đang ở đúng vùng power thấp" hạ thành [ước lượng].

## 3. Lỗi kỹ thuật khác đã sửa
- Bài 12, Số phải ra câu 1: cột "Tính lại" lệch 1 so với chính `n_indep` (93/387/905/434 → 94/388/906/435, làm tròn lên). Câu 5: CI Newcombe hiệu [−10, +23] → [−10, +24].
- Bài 17, Tự kiểm tra câu 1: đáp án ngụ ý đo góc (0.3, 0.5) cứu được kịch bản (0.45, 0.3); thực tế điểm đó vẫn cách 2.5 thang → sửa.
- Bài 5: Chấm mô hình 2 lộ đáp án dự đoán mục 2–3 (`1e-3` thành chuỗi, `012` thành 10, "dòng 3 hai hash") ở thân bài → chuyển thành chỉ dẫn "tự chạy sau khi dự đoán"; "Tham số cần tra" không còn nói sẵn "số thực bắt buộc dấu chấm".
- Bài 14: thân bài (Chấm mô hình) lộ "(đồ chơi, λ ≥ 1.5)" → bỏ.
- Bài 13: khối peeking chép lại `wilson`/`diff_ci` với chữ ký khác khối đầu → chạy tiếp sau khối `b13_gate`, dùng lại hàm (đã chạy ghép hai khối, số không đổi).

## 4. Độ dài (wc -w, tính cả code; tiếng Việt đếm theo âm tiết)
| Bài | Trước | Sau | Code |
|---|---|---|---|
| 5 | 5.908 | 4.840 | ~380 |
| 6 | 6.660 | 5.060 | ~800 |
| 7 | 5.508 | 4.728 | ~630 |
| 12 | 5.439 | 4.923 | ~1.000 |
| 13 | 5.915 | 5.056 | ~770 |
| 14 | 5.223 | 4.811 | ~650 |
| 17 | 5.437 | 5.096 | ~940 |
| 18 | 5.511 | 5.067 | ~870 |
Cắt: câu hỏi ngược thứ 5 (giữ 4, vẫn có [Quy mô] và [Failure mode]), liên kết thứ 3, câu tự kiểm tra thứ 2, hàng 🔴 không cần, hàng cầu nối trùng ý, rút gọn "Đã sửa", phần 11 và văn xuôi. Không cắt bước Làm, tiêu chí, khối 🔒, FAIL action. Phần chữ (trừ code) mọi bài ≤ ~4.300; tính cả code vẫn 4.7–5.1k, vì code là đối tượng chạy được.

## 5. Code
Chạy lại 18 khối `# [đã chạy]` trong phạm vi (m2: 7 gồm ba điều kiện a/b/c của `collect` và khối Gemini cố ý crash; m4: 5; m5: 3 + kiểm số MuJoCo rơi tự do không có trong code; m6: 1). Mọi số khớp bảng trong 🔒. Sửa 2 khối (Bài 18 Newcombe + mô phỏng baseline chung; Bài 13 peeking dùng lại hàm).

## 6. Còn nghi ngờ
- Số trang/chương CAIB cho Crater (640/400) chưa xác nhận bằng PDF.
- Độ dài: các bài nhiều code còn ~4.7–5.1k từ; muốn ≤ 4.5k cần bỏ một mô phỏng (ví dụ Bài 6 mô phỏng 3) — người điều phối quyết.
