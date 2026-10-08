# Brief cho agent KIỂM TRA CHÉO (reviewer độc lập)

Repo: `/home/user/robotics-lab` (GỐC). Một agent khác vừa soạn các file giáo trình của một đơn vị. Bạn là người kiểm độc lập: **không tin** người soạn, tìm lỗi và **sửa trực tiếp** trong file (Edit). Chỉ sửa đúng các file của đơn vị được giao. Không chạy git commit/push.

## Đọc trước
1. `GỐC/giao-trinh/_QUY-CHUAN.md` trọn vẹn (hợp đồng).
2. Các file của đơn vị (đọc trọn).
3. Phần nguồn tương ứng trong file khóa gốc `GỐC/khoa-*.md` (để kiểm không cắt mất bước/tiêu chí/giờ của bản gốc).

## Kiểm theo thứ tự ưu tiên, sửa ngay khi thấy
A. **Đúng kỹ thuật** (quan trọng nhất). Với mỗi con số, công thức, khẳng định về phần cứng/API/phiên bản/lịch sử: có đúng không? Nghi ngờ thì kiểm bằng tính toán, chạy Python, hoặc WebSearch/WebFetch (tải schema qua ToolSearch). Sai → sửa và ghi vào phần 11 (hoặc mục 10 của viên nang) dòng "Reviewer sửa: …". Không chắc → hạ nhãn xuống `[tự đo]` hoặc `[ước lượng]` kèm cách kiểm. Các lỗi mục 7 quy chuẩn phải đã được sửa nếu bài chạm tới.
B. **Nguồn và sự cố có thật.** Mọi tên paper/sách/bài nói/URL/sự cố: tồn tại thật không? URL nghi ngờ → WebFetch; không xác minh được → bỏ URL, giữ tên + tác giả nếu chắc, hoặc bỏ hẳn. Sự cố giả định phải ghi "kịch bản".
C. **Code chạy được.** Chạy mọi khối Python có `# [đã chạy]` trong thư mục scratchpad của bạn (dùng `MPLBACKEND=Agg`). Lỗi → sửa code. Khối ghi `[đã chạy]` mà thực ra cần phần cứng → đổi thành `[chưa chạy]`.
D. **Niêm phong.** Quét thân bài (ngoài `<details>`): có con số kỳ vọng/kết luận thí nghiệm/đáp án tự kiểm tra bị lộ không (kể cả trong tiêu đề, bảng thuật ngữ, câu chuyện, chấm mô hình)? Lộ → chuyển vào khối 🔒 hoặc thay bằng cách tính. (Các con số là *tham số đầu vào* cần tra — như sample rate cấu hình — thì được để ngoài.)
E. **Khung.** Mỗi bài đủ 12 phần đúng tiêu đề (hoặc khung rút gọn có ghi chú); viên nang F đủ 11 mục + đầu file + cuối file theo 4b. Mỗi cầu nối backend có "Gãy ở chỗ" + hậu quả. Có "Chấm mô hình" với nhãn ĐÚNG/ĐÚNG MỘT PHẦN/SAI + phản ví dụ. Câu hỏi ngược có ít nhất 1 [Quy mô] và 1 [Failure mode], mỗi câu có hướng nghĩ gập. Có ít nhất một dạng không phải chữ. Mermaid phải đúng cú pháp (không dùng ký tự gây lỗi như ngoặc chưa bọc trong nhãn node — bọc nhãn bằng "…").
F. **Văn phong.** Cấm `[cite`, câu kết "sẵn sàng sang bài…", lời khen người học, emoji trang trí. Grep và xóa.
G. **Không cắt xương sống.** So với bản gốc: còn đủ bước Làm, tiêu chí PASS/FAIL, FAIL action, giờ? Thiếu → bổ sung.
H. **Chiều sâu.** Nếu một bài chỉ là bản kẻ bảng lại của gốc, thiếu bản chất ("vì sao thứ này tồn tại"), câu hỏi ngược hời hợt, hoặc liên kết ra ngoài chung chung → viết lại phần đó cho sắc hơn. Đây không phải chỗ để cắt bớt; chỉ cắt chữ độn.

## Trả về (≤250 từ)
- KIỂM: file + số bài/viên nang đã kiểm
- LỖI KỸ THUẬT ĐÃ SỬA: mỗi dòng một lỗi (chỗ → sai → đúng)
- NGUỒN ĐÃ SỬA/BỎ
- CODE: số khối đã chạy, số khối đã sửa
- NIÊM PHONG / KHUNG / VĂN PHONG: số chỗ đã sửa
- CÒN NGHI NGỜ: điều bạn không kiểm được, để người điều phối biết
