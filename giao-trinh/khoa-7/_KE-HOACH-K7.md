# KẾ HOẠCH THIẾT KẾ LẠI KHÓA 7 — hợp đồng cho người soạn K7 (và người soạn F khi liên kết sang K7)

Đọc sau `_QUY-CHUAN.md`. File này định nghĩa mã chặng, mã bài, giờ, tên file, ràng buộc phần cứng mặc định và khung một chặng. Người soạn được làm sâu hơn, sửa con số khi có lý do (ghi vào phần 11 của bài và vào báo cáo), nhưng **giữ nguyên mã chặng, mã bài và tên file**.

## 1. Vì sao thiết kế lại

K7 gốc (`khoa-7-robot-hoan-chinh.md` + `khoa-7-phu-luc.md`) mở đầu bằng "Cho: người đã PASS Khóa 1–6". Danh sách mua chỉ một dòng ("khung xe 2 bánh + caster… driver motor, pin 3S/4S + BMS"). Không có bước lắp ráp, đi dây, bring-up hay an toàn pin nào. Nó là bản đặc tả dự án cho người đã quen tay.

Người học thật là người đang **học bật tắt mỏ hàn**, đi từ thế giới digital. Với người này, chỉ khi tự tay dựng robot mới cảm được độ khó của thế giới vật lý, và đó cũng là chỗ mọi khóa K1–K6 và F1–F7 được dùng thật. Vì vậy K7 mới là:

1. **Khóa vừa build vừa học**, đi đúng thứ tự một người mới thực sự dựng robot: xưởng → nguồn → cơ khí → bring-up trên bàn → firmware → lắp hoàn chỉnh → odometry → cảm biến/dữ liệu → điều hướng → nhận người → an toàn/vận hành → sim/HIL/CI → sản phẩm.
2. **Đường ray song song** với K2–K6, không phải khóa cuối. Chặng C0–C6 chạy được ngay sau K1 + K3 M1 (bảng ở mục 4).
3. **Hai sản phẩm cùng lúc:** con robot (artifact vật lý) và hệ thống data infra quanh nó (artifact dữ liệu). Mỗi chặng sinh ra cả hai.

## 2. Nguyên tắc riêng của K7

- **Đo trước khi cấp điện.** Mọi bước lắp có một checkpoint: đo gì, bằng dụng cụ gì, số phải ra (gập 🔒 nếu là số người học có thể dự đoán; số an toàn thuần thì để mở, ví dụ "điện trở giữa + và − pin sau khi nối: không được gần 0 Ω").
- **Một khối mới một lần.** Không bao giờ cắm hai thứ chưa kiểm cùng lúc. Bench trước khung; nguồn bàn có giới hạn dòng trước pin.
- **Robot luôn chạy được ở phạm vi nhỏ hơn** sau mỗi chặng (giống trunk-based development: không có nhánh "đang lắp dở" kéo dài nhiều tuần).
- **Sổ build là bộ dữ liệu đầu tiên.** Ảnh trước/sau, số đo, lỗi gặp, thời gian. Mỗi bench test trở thành **hạt giống regression test** cho HIL ở C11.
- **An toàn không thương lượng.** Mọi chặng đụng pin hoặc motor có mục An toàn riêng; quy tắc cứng viết dạng "KHÔNG …". Không viết mơ hồ kiểu "cẩn thận".
- **Viết cho người mới thật:** giải thích từng dụng cụ, cầm thế nào, mối hàn tốt trông ra sao, ốc nào siết bao chặt, dây màu gì. Không giả định người học "biết rồi". Có thể dẫn video/hướng dẫn công khai đáng tin (chỉ khi chắc tồn tại).

## 3. Bảng chặng (mã cố định)

| Chặng | File | Giờ | Làm ra được (vật lý · dữ liệu) | Bài khái niệm (mã · tên) | Lấy từ K7 gốc |
|---|---|---|---|---|---|
| **C0** Xưởng, dụng cụ, an toàn | `c00-xuong-an-toan.md` | 20 | Bàn làm việc an toàn, bộ đồ nghề, 10 mối hàn/đầu bấm đạt · sổ build + quy ước dây | C0.1 Bàn làm việc và đồ nghề: mua gì, vì sao *(rút gọn)* · C0.2 Điện gây hại bằng cách nào: dòng, nhiệt, năng lượng pin · C0.3 Hàn dây, bấm đầu nối, co nhiệt · C0.4 Nguồn bàn giới hạn dòng (CV/CC) · C0.5 Sổ build và quy ước dây *(rút gọn)* | — (mới) |
| **C1** Hệ nguồn | `c01-he-nguon.md` | 35 | Bo phân phối nguồn: pin → công tắc chính → cầu chì → nhánh motor (qua điểm cắt E-stop) / buck-boost 12 V mini PC / buck 5 V logic · bảng power budget đo được, log dòng–áp | C1.1 Pin lithium: hóa học, S/P, C-rate, BMS làm gì và không làm gì · C1.2 Power budget là một bảng số đo · C1.3 Dây, đầu nối, cầu chì: tiết diện, sụt áp, nhiệt · C1.4 DC-DC: buck/boost/buck-boost, ripple, pin cạn · C1.5 Lắp bo nguồn và đo dòng đỉnh (INA226 hoặc shunt) · C1.6 Sạc, bảo quản, xử lý pin hỏng *(rút gọn)* | dòng mua 7A, bảng ràng buộc mini PC |
| **C2** Cơ khí | `c02-co-khi.md` | 30 | Khung có motor, bánh, caster, gá mini PC/pin, quản lý cáp · bảng thông số hình học đo được (khối lượng, trọng tâm, đường kính bánh, khoảng cách bánh) | C2.1 Lực, mô-men, chọn motor/tỉ số truyền bằng số · C2.2 Khung, bố trí khối lượng, trọng tâm, chống lật · C2.3 Gá lắp: vít, ốc khóa, rung, standoff, strain relief · C2.4 Đo và cân robot: tham số hình học đầu tiên cho sim | — (mới) |
| **C3** Bring-up trên bàn | `c03-bring-up-tren-ban.md` | 30 | Mỗi motor + driver + encoder chạy riêng trên bàn từ ESP32, có capture · đường cong PWM→vận tốc, dòng hãm đo được | C3.1 Motor, encoder, driver: ba thứ trong một vỏ · C3.2 H-bridge: PWM, DIR, brake/coast, back-EMF, dòng hãm · C3.3 Encoder quadrature trên logic analyzer · C3.4 Đường cong PWM → vận tốc và vùng chết · C3.5 Quy trình bring-up có kỷ luật *(rút gọn)* | Bài 1, 2 |
| **C4** Firmware ESP32 | `c04-firmware-esp32.md` | 40 | Firmware vòng điều khiển 100 Hz từ timer phần cứng, giao thức với host, failsafe · log jitter vòng lặp, test firmware tự động trên bàn | C4.1 Kiến trúc firmware: timer, ISR, task, MCPWM/LEDC, PCNT · C4.2 PID vận tốc bánh và jitter vòng lặp · C4.3 Giao thức host↔MCU: framing, CRC, sequence, heartbeat → hardware interface `ros2_control` · C4.4 Failsafe trong firmware: watchdog, timeout, kẹp tốc độ, trạng thái an toàn mặc định | Bài 3, một phần Bài 15 |
| **C5** Lắp hoàn chỉnh lần đầu | `c05-lap-hoan-chinh.md` | 30 | Robot chạy bằng pin, điều khiển tay, có E-stop tạm · ROS 2 trong Docker trên robot, `/odom` chuẩn | C5.1 Tích hợp cơ–điện: checklist lần cấp điện đầu, nhiễu motor lên logic, ground, decoupling · C5.2 ROS 2 trong Docker trên robot: `ros2_control` + `diff_drive_controller`, udev, USB passthrough · C5.3 Teleop an toàn: deadman, giới hạn tốc độ, E-stop tạm · C5.4 Vận hành không màn hình: auto power on, SSH, restart policy *(rút gọn)* | kiến trúc hệ thống, Bài 8 bước 1 |
| **C6** Odometry | `c06-odometry.md` | 25 | Robot đi hình vuông với sai số đã hiệu chuẩn · dataset UMBmark trước/sau | C6.1 Động học vi sai và odometry · C6.2 UMBmark: tách sai số đường kính và khoảng cách bánh · C6.3 Odometry không biết mình sai: trượt, va chạm | Bài 4 |
| **C7** Cảm biến và ghi dữ liệu | `c07-cam-bien-ghi-du-lieu.md` | 35 | IMU + camera gá trên robot, TF tĩnh đúng REP-105 · sidecar MCAP, upload resumable, audit, dashboard Foxglove | C7.1 Gá cảm biến: rung, frame, TF tĩnh, băng thông USB · C7.2 Timestamp trên robot: source time ESP32 vs host · C7.3 Sidecar MCAP, upload, audit · C7.4 Data contract cho robot của chính mình | Bài 5 |
| **C8** Định vị và điều hướng | `c08-dieu-huong.md` | 70 | Robot tự đi A→B 20 lần · bảng độ chính xác marker, session điều hướng có rule phát hiện bất thường | C8.1 Marker hay lidar *(rút gọn)* · C8.2 Hiệu chuẩn camera và pose từ marker · C8.3 Hợp nhất odometry và marker, cây TF `map→odom→base_link` · C8.4 Nav2 từ A tới B · C8.5 Ghi và phân tích session điều hướng | Bài 6–10 |
| **C9** Nhận người, privacy-first | `c09-nhan-nguoi-privacy.md` | 64 | Nhận diện on-device, hai lớp đồng ý, xóa dữ liệu · ROC/FAR/FRR có khoảng tin cậy, audit log | C9.1 Quyền riêng tư trước dòng code đầu tiên, hai lớp đồng ý · C9.2 Pipeline nhận diện và FAR/FRR · C9.3 Đăng ký, xóa dữ liệu, audit log · C9.4 Tích hợp nhận diện vào điều hướng | Bài 11–14, Phụ lục A |
| **C10** An toàn và vận hành | `c10-an-toan-van-hanh.md` | 60 (+16 tùy chọn) | E-stop cứng qua relay/contactor, bumper, watchdog độc lập, state machine · FMEA đã test bằng lỗi thật, soak 72h, dashboard vận hành | C10.1 An toàn là một tầng phần cứng: E-stop, relay, bumper, đo thời gian phản ứng · C10.2 State machine và FMEA · C10.3 Soak 72h trong văn phòng thật · C10.4 HRI đo được *(tùy chọn)* | Bài 15–17, Phụ lục C |
| **C11** Sim twin, HIL, CI, vòng đời dữ liệu | `c11-sim-hil-ci.md` | 92 (+20 tùy chọn) | Model sim từ số đo thật, cổng HIL, CI 1000 episode ba trạng thái · tương quan sim–thật, vòng fine-tune | C11.1 Model sim khớp robot thật · C11.2 HIL và CI cho hành vi robot · C11.3 Sim có dự đoán được thực tế không ★ · C11.4 Controller tầng giữa: đo MPC mua được gì · C11.5 Vòng đời dữ liệu đầy đủ và fine-tune · C11.6 Dự đoán quỹ đạo người *(tùy chọn)* | Bài 18–21, Phụ lục B, D |
| **C12** Sản phẩm: robot confession | `c12-san-pham-confession.md` | 30 | Chuỗi audio K3 trên robot, luồng sản phẩm đầu–cuối · bài viết tổng kết, demo | C12.1 Gắn chuỗi audio lên robot: amp chung pin, nhiễu motor vào audio, ground loop · C12.2 Luồng sản phẩm đầu–cuối và state machine sản phẩm · C12.3 Demo, bài tổng kết, câu chuyện phỏng vấn *(rút gọn)* | gate 7E tiêu chí 8, Phụ lục mục 4 |

**Tổng lõi: 561h** (C0–C12, không tính tùy chọn); có tùy chọn: 597h. K7 gốc: 340h (trần 450h).

**Đường lõi tối thiểu ≈ 340h** (bằng K7 gốc, nhưng đi từ xưởng thay vì từ đặc tả): C0–C7 trọn (245h) + C10.1–C10.2 (~34h) + C11.1–C11.3 (~60h). Nếu chỉ làm được đường này, robot vẫn đi được, an toàn, có dữ liệu, có sim và có câu trả lời "sim có dự đoán đúng thực tế không" — đúng tinh thần "nếu chỉ làm được một phần, làm 7A và 7E" của bản gốc.

**Tác động ngân sách toàn lộ trình** (phải ghi trong `00-tong-quan.md` và README): K1–K6 = 545h; + K7 mới lõi 561h = **1.106h**; ở 6,5h/tuần ≈ 170 tuần ≈ **3,3 năm**. Đường lõi tối thiểu: 545 + 340 = 885h ≈ 2,6 năm. Đây là quyết định của người học, ghi vào `decisions.md`, không giấu.

## 4. Đường ray song song — chặng nào bắt đầu được khi nào

| Chặng | Cần trước (khóa chính) | Cần trước (viên nang nền) | Chạy song song được với |
|---|---|---|---|
| C0 | K1 Phần B (dụng cụ) | F5.7 (đọc) | K2 |
| C1 | K1 trọn; tốt nhất sau K3 Bài 5–6 (amp, brownout) | F5.7, F1.1 | K2–K3 |
| C2 | C0 | F1.1 | K2–K3 |
| C3 | K1 Phần D (logic analyzer), K3 M1 (ESP-IDF, I2S) | F5.1, F5.2 | K3–K4 |
| C4 | C3; K3 M1 | F5.2, F5.3, F5.8 | K4 |
| C5 | C1, C2, C4 | F5.7 | K4 |
| C6 | C5 | F6.4, F1.1, F1.6 | K4–K5 |
| C7 | C6; K5 M1–M3 | F3.1, F3.4, F4.6 | K5 |
| C8 | C7 | F6.7, F6.8, F1.4 | K5–K6 |
| C9 | C8; K4 | F2.8, F1.4, F1.5 | K6 |
| C10 | C8 | F7.6, F5.3, F7.7 | K6 |
| C11 | C10; K6 trọn | F6.1–F6.6, F2.7, F2.6 | sau K6 |
| C12 | C10, C11.2; K3 trọn | F5.7, F7.4 | — |

Khi chặng K7 cần một kỹ thuật mà khóa chính tương ứng chưa học tới (ví dụ C4.2 đo jitter mà K5 Bài 8 chưa học), bài K7 phải **tự chứa phiên bản tối thiểu** của kỹ thuật đó (đủ để làm) và trỏ `→ K5 Bài 8` cho bản đầy đủ.

## 5. Ràng buộc phần cứng mặc định (người soạn kiểm lại, được đổi nếu có lý do)

Ghi nhãn đúng: hầu hết là `[ước lượng]` hoặc `[tự đo]` cho tới khi người học đo.

- **Robot:** vi sai 2 bánh + 1–2 caster, chở mini PC N100 + pin + ESP32 + camera + loa. Khối lượng mục tiêu ≤5 kg `[ước lượng]` (cân thật ở C2.4). Tốc độ cứng ≤0,5 m/s trong văn phòng, kẹp ở firmware (C4.4) chứ không chỉ ở Nav2.
- **Mini PC:** nguồn 12 V DC, công suất 6–25 W có đỉnh `[ước lượng, tự đo]`; cần BIOS Auto Power On. Không được để mini PC ăn trực tiếp từ pin không ổn áp.
- **Pin:** khuyến nghị cho người mới là **pack dựng sẵn có BMS tích hợp + sạc đúng hóa học**; không tự ghép cell ở lần đầu; không dùng LiPo RC trần cho người mới trừ khi có lý do và quy trình an toàn đầy đủ. Lựa chọn so sánh ở C1.1: 4S Li-ion (NMC) vs 4S LiFePO4 vs 3S. Hệ quả cần chỉ ra: điện áp pack trôi theo mức sạc (ví dụ 4S Li-ion ~12–16,8 V `[chuẩn]`) → mini PC cần **buck-boost** (hoặc buck nếu điện áp pack luôn > 12 V + headroom), không phải "cứ buck là được".
- **Phân phối:** pin → công tắc chính + cầu chì chính sát pin → (a) nhánh động lực motor qua điểm cắt E-stop (relay/contactor, cắt khi mất điện cuộn hút) → driver; (b) DC-DC 12 V cho mini PC; (c) buck 5 V cho ESP32/logic/cảm biến. E-stop **cắt động lực, không cắt compute**. Mỗi nhánh có cầu chì bảo vệ dây của nhánh. Mass/ground hình sao, tách đường dòng motor khỏi đường logic.
- **Motor:** DC giảm tốc 12 V có encoder Hall quadrature (họ JGB37-520 hoặc tương đương phổ biến ở VN) `[tự đo]` PPR, tỉ số truyền, dòng không tải, dòng hãm. Chọn bằng tính toán mô-men ở C2.1, không chọn theo cảm tính.
- **Driver:** dòng liên tục định mức ≥ dòng hãm đo được (hoặc có giới hạn dòng), điện áp ≥ điện áp pack đầy; ưu tiên loại MOSFET có current sense. Giải thích vì sao **không** dùng L298N (sụt áp BJT, tỏa nhiệt) `[chuẩn]` và vì sao TB6612 thường quá nhỏ cho motor cỡ này `[spec, kiểm datasheet]`.
- **Đầu nối:** XT60/XT30 cho nguồn, JST-XH/PH cho tín hiệu, ferrule cho cầu đấu vít, Dupont chỉ trên bàn. Màu dây thống nhất (đỏ +, đen GND, quy ước tín hiệu ghi trong C0.5).
- **Đo lường có sẵn:** UT33D+ (kiểm dải đo dòng và cầu chì trong manual `[spec]`; multimeter quá chậm cho dòng đỉnh), logic analyzer 24 MHz, INA219/INA226 qua I2C cho log dòng–áp. **Phải mua:** nguồn bàn có giới hạn dòng (ví dụ 30 V/5 A) — bắt buộc trước khi đụng pin.
- **ESP32:** lập bảng chân (pin budget) ở C4.1: encoder ×4, PWM/DIR ×4, bumper, E-stop sense, I2C (IMU, INA226), I2S (C12), relay. Kiểm chân strapping/USB của ESP32-S3 `[spec]`. FMEA (C10.2) cần đường cắt relay **độc lập** với ESP32 chính (watchdog phần cứng ngoài hoặc MCU thứ hai) — thiết kế ở C10.1.
- **Phần mềm:** ROS 2 Jazzy trong Docker, `ros2_control` + `diff_drive_controller` (hardware interface viết riêng qua serial) là mặc định; micro-ROS là phương án so sánh ở C4.3. Mọi API ghi `[tự đo]` theo phiên bản cài.

## 6. Khung một file chặng

```markdown
# Chặng N — <Tên> (<giờ>h)

> **Vị trí:** <chặng trước → chặng này → chặng sau> · **Cần trước:** <K… / F… / Cn> · **Chạy song song với:** <K…>
> **Làm ra được:** <artifact vật lý> · <artifact dữ liệu> · **Sau chặng này bạn quyết định được:** <…>

## 0. Bức tranh chặng
<Mermaid/ASCII: robot (hoặc bàn thử) sau chặng này trông thế nào; khối nào mới thêm; dòng điện/dữ liệu đi đâu.>

## 1. An toàn của chặng
<rủi ro cụ thể của chặng (bỏng, ngắn mạch pin, cháy, kẹp tay, bánh quay bất ngờ…); quy tắc cứng dạng "KHÔNG …"; làm gì khi sự cố xảy ra (ví dụ pin bốc khói).>

## 2. BOM chặng
| Món | Thông số phải chọn | Vì sao (bằng số) | Giá [ước lượng 10/2026] | Kiểm khi nhận hàng | Thay thế được bằng |
|---|---|---|---|---|---|

## 3. Dụng cụ và kỹ năng tay
<kỹ năng mới của chặng; bài luyện trên phế liệu trước khi làm thật; mối hàn/đầu bấm đạt trông ra sao, hỏng trông ra sao.>

## 4. Sơ đồ đi dây
<ASCII/Mermaid có ghi tiết diện dây, màu, cầu chì, đầu nối; bảng chân (pin table) nếu có MCU.>

## 5. Trình tự chặng
<danh sách đánh số xen kẽ "Học Bài Cn.m" và "Lắp bước k". Mỗi bước lắp:>
**Bước k — <tên>**
- Làm: …
- ✅ Checkpoint trước khi cấp điện: đo <gì> bằng <dụng cụ>, giữa <điểm A> và <điểm B>; phải ra <…> (số dự đoán được thì gập 🔒)
- Nếu sai: …

## 6. Lỗi người mới hay gặp
| Triệu chứng | Nguyên nhân khả dĩ | Kiểm bằng cách | Sửa |
|---|---|---|---|

## 7. Lăng kính data infra
<chặng này sinh dữ liệu gì (schema, tần số, đơn vị theo CONVENTIONS.md); ghi ở đâu; test tự động nào sinh ra từ chặng này (hạt giống HIL/CI cho C11); metric/SLI nào; liên hệ vai trò Data Platform / Test & Validation.>

## 8. Nhật ký build
<mẫu `build-log/cNN.md` để copy: ngày, giờ thực, ảnh, số đo, lỗi, quyết định, câu hỏi còn mở.>

## Bài CN.1 — <Tên> (<giờ>h)
<khung 12 phần của _QUY-CHUAN.md mục 4; bài *(rút gọn)* dùng khung rút gọn>

## Bài CN.2 — …

## Gate chặng N
<tiêu chí nhị phân, giữ tiêu chí gate gốc 7A–7E đã phân về chặng này (mục 7), FAIL action>
```

Giờ của chặng = tổng giờ các bài + giờ lắp. Ghi rõ phân bổ.

## 7. Phân gate gốc về chặng mới

| Gate gốc | Về chặng |
|---|---|
| GATE 7A (odometry, jitter, PWM, dữ liệu) | C3 (PWM, dòng hãm), C4 (jitter p99), C6 (UMBmark), C7 (ghi dữ liệu) |
| GATE 7B | C8 |
| GATE 7C (+ Phụ lục A) | C9 |
| GATE 7D (+ Phụ lục C tùy chọn) | C10 |
| GATE 7E — và gate Khóa 7 (+ Phụ lục B) | C11; tiêu chí bài viết chính → C12 |
| Mới | C0 (an toàn xưởng, kỹ năng tay), C1 (power budget đo được, bảo vệ), C2 (thông số hình học), C5 (lắp hoàn chỉnh, teleop an toàn) |

## 8. Phân công soạn

| Agent | File |
|---|---|
| K7-a | `00-tong-quan.md`, `c00-xuong-an-toan.md` |
| K7-b | `c01-he-nguon.md` |
| K7-c | `c02-co-khi.md`, `c03-bring-up-tren-ban.md` |
| K7-d | `c04-firmware-esp32.md`, `c05-lap-hoan-chinh.md` |
| K7-e | `c06-odometry.md`, `c07-cam-bien-ghi-du-lieu.md` |
| K7-f | `c08-dieu-huong.md` |
| K7-g | `c09-nhan-nguoi-privacy.md`, `c12-san-pham-confession.md` |
| K7-h | `c10-an-toan-van-hanh.md` |
| K7-i | `c11-sim-hil-ci.md` |

Các agent soạn song song, không đọc được file của nhau lúc viết. Vì vậy: dùng đúng mã bài ở mục 3 khi trỏ sang chặng khác, và **không giả định nội dung chi tiết** của chặng khác ngoài những gì bảng mục 3 và ràng buộc mục 5 nói.

`00-tong-quan.md` của K7 gồm: vì sao thiết kế lại (mục 1), bản đồ chặng (Mermaid), bảng mục 3 + 4, ngân sách giờ và tiền (tổng BOM theo chặng, ước lượng), tác động lên tổng lộ trình, đường lõi tối thiểu, gate tổng, "Cách học khóa này" cho người mới (tuần thường làm gì, tuần crunch làm gì — đọc bài khái niệm, không lắp khi mệt), quy tắc an toàn xuyên suốt, bản đồ vai trò (rút từ Phụ lục mục 4), danh sách sửa lỗi so với K7 gốc và bản Gemini K7.

## 9. Quyết định đã chốt khi soạn (cập nhật 2026-10-08, Claude)

- **Pin mặc định: 4S LiFePO4** (C1.1). Áp đầy 14,6 V gần định mức motor 12 V, ổn định nhiệt hơn NMC. Mini PC bắt buộc qua **buck-boost 12 V ≥5 A** (adapter EQ12 là 12 V 3 A = 36 W; chọn DC-DC theo 36 W + biên).
- Đo dòng: INA226 + **shunt rời 50 A/75 mV** (module bán sẵn shunt 0,1 Ω chỉ tới ~0,8 A).
- Cầu chì chính sát pin + cầu chì từng nhánh; cuộn relay E-stop lấy từ pack qua cầu chì 1 A.
- Màu dây (C0.5): đỏ VBAT, cam 12 V, tím 5 V, đen GND, I2C theo Qwiic (đỏ 3,3 V của Qwiic dán nhãn "3V3").
- Motor mặc định sau tính toán C2.1: **JGB37-520 tỉ số 1:56, bánh 85 mm** `[tự đo]` PPR/dòng. Driver: loại TB6612 (14,6 V > 13,5 V khuyến nghị, 1,2 A < dòng hãm), loại L298N.
- Thuật ngữ: **dòng hãm** = stall current (rotor bị giữ đứng); **dòng phanh** = braking (H-bridge brake). Định nghĩa ở C3.1/C3.2; C4, C10 dùng đúng.
- Lấy mẫu encoder: tiêu chí là chu kỳ lấy mẫu nhỏ hơn khe ngắn nhất giữa hai cạnh vài lần, không phải "trên Nyquist" (C3.3).
- Giới hạn gia tốc phanh (chống lật, C2.2) lưu vào `decisions.md`, firmware C4.4 kẹp theo đó.
