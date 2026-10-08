# Brief chung cho agent soạn giáo trình

Repo: `/home/user/robotics-lab` (gọi là GỐC). Bạn là một trong nhiều agent soạn song song bộ giáo trình `GỐC/giao-trinh/`. Mỗi agent có một **đơn vị** riêng với danh sách file đầu ra riêng — **chỉ tạo/sửa đúng các file của đơn vị mình**, không đụng file khác, không chạy git commit/push (người điều phối sẽ commit).

## Thứ tự bắt buộc
1. Đọc TRỌN `GỐC/giao-trinh/_QUY-CHUAN.md`. Đây là hợp đồng. Mọi quy tắc trong đó là bắt buộc (khung 12 phần, niêm phong đáp án, "Gãy ở chỗ:", nhãn [spec]/[chuẩn]/[ước lượng]/[tự đo], chấm mô hình ĐÚNG/ĐÚNG MỘT PHẦN/SAI, dạng không phải chữ, cấm [cite: N], cấm lời khen/câu kết độn, không bịa nguồn/sự cố, mục 7 lỗi đã biết).
2. Đọc `GỐC/giao-trinh/_ref/cau-hoi-cua-ban-trong-gemini.md` để nắm giọng và các mô hình người học tự xây. Khi một mô hình của người học liên quan đến bài bạn soạn, chấm nó trong phần "Chấm mô hình" (trích ngắn, ghi "mô hình của bạn ở K3 lượt 7" chẳng hạn).
3. Đọc phần nguồn của đơn vị trong file khóa gốc (dùng Read với offset/limit, các file 50–75KB). Đọc lướt `GỐC/00-lo-trinh-tong.md` (grep phần liên quan khóa của bạn), `GỐC/CONVENTIONS.md`, `GỐC/THAY-DOI-10-2026.md`, và grep `GỐC/robotics-data-infra-roadmap.md` để lấy mức 🟢🟡🔴 của thuật ngữ.
4. Nếu khóa có bản Gemini (`GỐC/detail/Gemini-khóa N-*.md`, định dạng `## User:`/`## Gemini:`): Grep "Bài N" để tìm đoạn tương ứng, đọc theo offset/limit. Chỉ gặt ví dụ/câu hỏi tốt; mọi khẳng định kỹ thuật từ Gemini phải tự kiểm lại; ghi lỗi Gemini tìm thấy vào phần 11.
5. Soạn. Viết **dần**: Write file với tiêu đề + bài đầu tiên, rồi Edit/append từng bài tiếp theo. Không viết một lần khổng lồ.

## Chất lượng — những thứ người điều phối sẽ kiểm
- **Giữ đủ nội dung thực hành của bản gốc** (các bước, lệnh, tiêu chí PASS/FAIL, FAIL action, giờ). Bạn thêm chiều sâu, không cắt xương sống. Giờ mỗi bài giữ như gốc.
- **Không lộ đáp án ngoài khối 🔒**: con số kỳ vọng, kết luận "sẽ thấy X", đáp án tự kiểm tra đều nằm trong `<details>`. Ở phần Dự đoán chỉ có đề, tham số cần tra (tra ở đâu: datasheet nào, lệnh nào), công thức/phương pháp, và mẫu `prediction.md`.
- **Bản chất trước công cụ**: mỗi bài phải trả lời "vì sao thứ này tồn tại / người ta khổ vì gì mà phát minh ra nó" và "quyết định nào bạn ra được sau bài này".
- **Cầu nối backend luôn có chỗ gãy** và hậu quả nếu dùng nhầm. Tận dụng vốn của người học (hàng đợi, Kafka, proxy, retry, idempotency, SLO, CI, mock server, LLM-judge, test pass/fail/inconclusive, host yên tĩnh…). Khi chỉ ra một kết nối sâu (ví dụ công thức độ trễ buffer = định luật Little), nói thẳng ra.
- **Câu hỏi ngược** phải là câu hỏi thật sự mở, khiến người học tự trừu tượng hóa và liên kết; có [Quy mô] (ở 100 robot/1000 giờ dữ liệu cái gì gãy trước) và [Failure mode].
- **Liên kết ra ngoài**: ngành khác (mạng, DB, tài chính, hàng không, y sinh, thiên văn…), có chỗ giống và chỗ khác.
- **Dạng không phải chữ**: Mermaid, ASCII timing, bảng số, WaveDrom JSON, hoặc mô phỏng Python ≤60 dòng. Python đã cài sẵn numpy/matplotlib/scipy. **Mọi khối Python bạn đưa vào phải chạy thử** trong thư mục scratchpad riêng của bạn (đường dẫn trong đề bài đơn vị; tạo nếu chưa có), dùng `matplotlib.use("Agg")` và savefig thay show khi chạy thử (trong bài có thể để `plt.show()`). Dòng đầu khối: `# [đã chạy]` hoặc `# [chưa chạy]` (chỉ cho code cần phần cứng/thư viện không cài được, như ESP-IDF, ROS 2, LeRobot).
- **Kiểm sự thật**: con số datasheet, API/phiên bản, URL — nếu không chắc, dùng WebSearch/WebFetch (tải schema qua ToolSearch nếu cần) hoặc gắn `[tự đo]`/bỏ URL chỉ ghi tên tài liệu + tác giả. Không bịa.
- **Sửa lỗi gốc**: mục 7 của quy chuẩn là bắt buộc nếu chạm bài của bạn. Khi thấy thêm lỗi kỹ thuật trong bản gốc hoặc Gemini, sửa và ghi ở phần 11 của bài (dòng "Đã sửa so với bản gốc/Gemini").
- **Liên kết chéo** dùng mã cố định trong mục 6 quy chuẩn (`→ F4.5`, `→ K5 Bài 9`). Khóa 7 đã thiết kế lại: dùng mã chặng/bài `→ K7 C3.2` theo `giao-trinh/khoa-7/_KE-HOACH-K7.md` (đọc mục 3–5 của file đó nếu bài của bạn liên quan robot thật). Tên file đầu ra theo mục 8 quy chuẩn. Có bản Kiro cùng tên trong `giao-trinh-kiro/` thì đọc để tham khảo (xem `giao-trinh/_PHOI-HOP.md`). Ở dòng **Vị trí** của mỗi bài, ghi các viên nang nền cần trước.
- Bài thuần hậu cần (mua sắm, cài đặt, viết bài tiếng Anh, tìm người reproduce, gate) dùng **khung rút gọn**.
- Không viết lời mở đầu kiểu "Chào bạn", không tóm tắt lặp cuối file.

## Đầu ra trả về (câu trả lời cuối cùng của bạn)
Một báo cáo ngắn (≤300 từ), dạng:
- FILES: danh sách file đã viết + số từ ước lượng (dùng `wc -w`)
- BÀI: danh sách bài đã soạn, đánh dấu bài nào dùng khung rút gọn
- SỬA LỖI: các lỗi trong bản gốc/Gemini đã sửa (1 dòng mỗi lỗi)
- CHƯA KIỂM: các khẳng định quan trọng còn `[tự đo]`/chưa chắc
- GHI CHÚ CHO NGƯỜI ĐIỀU PHỐI: mâu thuẫn, thiếu nguồn, quyết định bạn đã tự đưa ra
