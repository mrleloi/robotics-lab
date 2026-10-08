# Review K7 C0 + C1 (reviewer r-k7a, 2026-10-08)

Phạm vi: `khoa-7/c00-xuong-an-toan.md` (5 bài + gate), `khoa-7/c01-he-nguon.md` (6 bài + gate). Sửa trực tiếp, chưa commit.

## RỦI RO AN TOÀN ĐÃ SỬA

1. **Ngắn mạch pin qua đồng hồ vạn năng.** C0.4 bước 3 bảo "cắm que đỏ sang lỗ mA". Họ UT33+ không có lỗ mA riêng: mA dùng chung lỗ với V/Ω, chọn bằng núm (review lygte-info). Đã viết lại bước này. Thêm quy tắc cứng ở C0 mục 1 và C1 mục 1: không chạm que vào pin khi núm ở thang dòng hoặc que ở lỗ `10A`, đọc to "núm ở V, que ở VΩ" trước mỗi lần đo áp, và không bao giờ đo dòng pin bằng đồng hồ. Cầu chì thủy tinh 5×20 không được thiết kế để cắt dòng chập của pack; một teardown UT33D đời cũ (EEVblog) thấy dây đồng hàn vào chỗ cầu chì 10 A. Đã gắn câu kiểm tra vào các bước đo OCV (C1.1 bước 2, Lắp bước 8) và vào bước đối chứng 10 A (C1.5 bước 4).
2. **Gắn F0 + XT60 vào dây pin đang có điện (C1 Lắp bước 3).** Bản cũ chỉ ghi "pigtail pin" mà không có quy trình. Đã thêm Lắp bước 3a:
   - Ưu tiên làm dây chuyển, không cắt dây pin.
   - Nếu phải làm trên dây pin thì làm từng dây một: lắp đế F0 khi chưa cắm cầu chì → hàn dây + vào XT60 cái → dây − làm sau cùng → đo phải ra 0 V → mới cắm F0.
   - Với cọc vít: nối + trước, − sau; tháo − trước.
   - Thêm quy tắc cứng: không cắt hai dây pin cùng một nhát kìm.
3. **Dùng nguồn bàn làm bộ sạc LFP (BOM + C1.6).** Bản cũ ghi "đặt 14,6 V". Đã sửa thành: đặt 14,4 V khi đầu ra hở và kiểm bằng đồng hồ, vì sai số màn hình có thể đẩy cell quá 3,65 V. Nguồn bàn không tự ngắt, nên người học phải tự tháo pin khi dòng xuống dưới ~0,05C và đặt hẹn giờ. Không để pack nối vào nguồn bàn đang tắt (dòng ngược). Sờ hoặc đo IR vỏ pack mỗi 10 phút.
4. **Dây sense và VBUS của INA226 nối thẳng VBAT.** Bản cũ ghi "không cần cầu chì". Nếu dây 26 AWG cọ chạm GND, nó cháy trước khi F0 15 A kịp đứt. Đã thêm điện trở 10 Ω sát mép shunt trên mỗi dây (vừa làm phần tử hy sinh, vừa là giá trị lọc tối đa TI khuyên), và ghi rõ IN+ ở phía pin.
5. **Ba giới hạn của mạch E-stop C1** (mạch vẫn fail-safe: tiếp điểm NO + nút NC, mất cuộn hút = cắt):
   - Xoay nhả nút là động lực có lại ngay, không qua bước reset.
   - Diode dập song song cuộn làm relay nhả chậm hơn.
   - Relay đóng vào tụ 1000 µF có thể hàn dính tiếp điểm, tức E-stop hỏng ở trạng thái đóng mà không ai biết.
   - Cần kiểm dải áp cuộn 12 V từ 10 V đến 14,6 V.
   Ba điểm đầu đã chuyển sang C10.1.
6. **Cực tính XT60.** Bản cũ ghi "+ ở cạnh vát", ngược với quy ước phổ biến ("+" ở cạnh phẳng). Đã sửa: tin ký hiệu đúc trên vỏ, rồi đo lại bằng đồng hồ.
7. **Cháy khi đang sạc.** Thêm bước ngắt điện lưới trước khi dùng nước, nếu tới được ổ hoặc aptomat mà không phải đi qua lửa. Đã kiểm hướng dẫn: nước dùng được để làm mát pin Li-ion/LFP (FAA, các cơ quan cứu hỏa).

## Lỗi kỹ thuật khác đã sửa
- Bảng thời gian–dòng ATO (C1.3): hàng "100% ≥100 h" sửa thành "110% ≥100 h" theo datasheet Littelfuse 0257. Thêm cột cho cầu chì 1–2 A (min ở 350% là 0,02 s, ở 200% là 0,10 s), vì thí nghiệm dùng cầu chì 2 A. Đã sửa đáp án 🔒.
- Firmware INA226: `(Wire.read()<<8)|Wire.read()` có thứ tự tính không xác định trong C++, có thể đảo byte. Đã tách thành hai lần đọc riêng và ép kiểu `%lu`. Mã cấu hình 0x4097, bit CVRF và các LSB 2,5 µV / 1,25 mV đã kiểm và đều đúng.
- Lực kéo UL 486A: bổ sung giá trị cho 14 AWG (50 lbf ≈ 222 N). Ghi rõ bảng UL áp cho đầu bấm; mức 133 N cho mối hàn XT60 là quy ước của khóa.
- Cất pin LFP: "50% = 13,2 V" sửa thành xác định bằng đếm Ah. Áp nghỉ chỉ dùng để kiểm thô, vì đường OCV của LFP phẳng.
- Philae: bỏ cặp số "100 Wh còn / 80 Wh cần" vì không tìm được nguồn gốc. Đã xác minh bài E3S 2017 (06006) và con số 64 h.
- Mermaid erDiagram (C0.5): tách mỗi thuộc tính ra một dòng riêng.

## Đã kiểm, đúng
- **Ngưỡng IEC 60479-1:** 0,5 mA cảm nhận, let-go 5 mA (bản 2005), dòng DC không có ngưỡng let-go xác định.
- **Pin và linh kiện:**
  - Dải LFP 2,5–3,65 V/cell.
  - XT60 30 A, JST-XH 3 A.
  - ATO cắt được 1000 A ở 32 V DC.
  - INA226: ±81,92 mV; shunt 50 A/75 mV cho I_max ≈ 54 A, độ phân giải ≈ 1,7 mA.
  - Mini PC: buck-boost ≥5 A cho 36 W.
- **Sự kiện thật:**
  - 787: ngày tháng, NTSB 12/2014, DCA13IA037.
  - Note 7: lỗi pin A và pin B, công bố 1/2017.
  - Swissair 111: TSB A98H0003.
  - iPhone: iOS 10.2.1, giảm >80% số lần tắt trên 6s; thư xin lỗi 12/2017.
  - CPSC: 6/7/2016, 501.000 xe, 10 hãng, 99 sự cố.
- **Code:** 9/9 khối `[đã chạy]` đã chạy lại, số in ra khớp với các bảng 🔒. Scratch đã xóa.

## Còn nghi ngờ
- Cầu chì 10 A của UT33D+ có thật hay không còn tùy đời máy. Người học phải mở nắp kiểm (gate C0 tiêu chí 6 đã yêu cầu).
- Không lấy được manual UT33D+ và trang lygte (proxy chặn). Thông số lấy từ kết quả tìm kiếm.
- "Hersman: <100.000 giờ" khớp với Reuters. Chưa đối chiếu được văn bản gốc của NTSB.
