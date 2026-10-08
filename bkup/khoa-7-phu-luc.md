# PHỤ LỤC KHÓA 7
## Sau khi đối chiếu với hai bản review

Tài liệu này **bổ sung**, không thay thế `khoa-7-robot-hoan-chinh.md`. Đọc sau khi đã đọc bản chính.

---

## 0. ĐÁNH GIÁ HAI BẢN REVIEW

Cả hai đều tốt, và cả hai nói đúng một điều: chúng phân rã **tổ chức** (ai làm gì, team nào tồn tại), còn tài liệu gốc phân rã **phép đo** (đo cái gì, ngưỡng nào là đạt). Hai trục khác nhau, không mâu thuẫn.

**Cái hai review làm tốt hơn bản gốc:**
- Bản đồ vai trò đầy đủ — bản gốc không có, và nó thực sự thiếu
- Nhấn mạnh predictive control / MPC như một tầng riêng — bản gốc chỉ dùng Nav2 mặc định mà không bàn
- Nêu HRI như một chuyên môn riêng — bản gốc coi nó là phụ
- Nhắc dự đoán quỹ đạo người — bản gốc chỉ có tránh vật cản phản ứng

**Cái cả hai bỏ sót, và là chỗ nghiêm trọng nhất:** không ai đặt câu hỏi về **thiết kế sản phẩm** của chính cái use-case. Chi tiết ở mục 3.

**Giới hạn chung của cả hai:** danh sách vai trò dài không tự động biến thành hành động cho một người. Điều hữu ích với bạn không phải "công ty có 20 vị trí" mà là **"bạn đóng vai nào, bỏ vai nào, và làm sao nói được về vai mình bỏ"**. Mục 4 làm việc đó.

---

## 1. BỔ SUNG CẦN THIẾT

Tổng thêm ~52h. Tôi xếp theo mức ưu tiên, không phải làm hết.

| # | Nội dung | Giờ | Gắn vào | Ưu tiên |
|---|---|---|---|---|
| A | Hai lớp đồng ý — sửa lỗi thiết kế sản phẩm | 4 | 7C | **Bắt buộc** |
| B | Predictive control: nằm ở đâu, và đo nó mua được gì | 12 | 7E | **Bắt buộc** |
| C | HRI đo được | 16 | 7D | Nên làm |
| D | Dự đoán quỹ đạo người | 20 | 7B/7E | Tùy chọn |

---

## A. HAI LỚP ĐỒNG Ý (4h, gắn vào 7C Bài 11) — BẮT BUỘC

### Vấn đề mà không review nào nêu

V1 ở Khóa 3 là một cái loa cố định đọc confession **ẩn danh**. Phiên bản Khóa 7 là một robot **tự tìm đến một người cụ thể được nhắc tên** và phát nội dung về người đó, trước mặt đồng nghiệp.

Đó không phải cùng một sản phẩm. Đó là một hành vi **nhắm vào cá nhân**, có khuếch đại, và có tính công khai cưỡng bức — người nhận không chọn thời điểm, không chọn khán giả, và không rời đi được vì robot đi theo.

Hai review đều mô tả rất kỹ cách làm nó chạy và không ai hỏi nó **nên** chạy không. Một team sản phẩm thật sẽ bắt được điều này ở buổi họp đầu tiên, và bắt được nó chính là thứ phân biệt kỹ sư với người viết code.

### Sửa: tách hai lớp đồng ý

Bản gốc mới có **một** lớp — đồng ý cho đăng ký sinh trắc học. Cần lớp thứ hai:

| Lớp | Đồng ý cái gì | Rút lại thế nào |
|---|---|---|
| **1 — Sinh trắc** | Cho phép lưu embedding khuôn mặt để nhận diện | Nút xóa dữ liệu (đã có) |
| **2 — Nhận tin** | Cho phép robot tìm đến tôi và phát nội dung | Bật/tắt bất cứ lúc nào, mặc định **TẮT** |

Cộng thêm ba cơ chế:

- **Trạng thái "không làm phiền"** — bật một chạm, có thời hạn, robot bỏ qua mọi task nhắm vào người đó
- **Giới hạn tần suất** — tối đa N tin mỗi người mỗi ngày. Không có nó, một người có thể bị nhắm liên tục
- **Robot rời đi khi bị từ chối** — người nhận nói "không" hoặc bấm nút thì robot dừng và đi, không hỏi lại

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Người chưa bật lớp 2 | Task bị từ chối **ở server**, robot không bao giờ nhận |
| Bật "không làm phiền" giữa lúc robot đang tới | Robot hủy task và quay về. Test bằng cách bấm lúc robot cách 2m |
| Vượt giới hạn tần suất | Task vào hàng đợi ngày hôm sau, hoặc bị từ chối, có log |

### Vì sao điều này làm hồ sơ **mạnh hơn**, không phải yếu đi

Một đoạn trong README như thế này nói nhiều hơn cả trang tính năng:

> Lần lặp đầu, robot tìm đến bất kỳ ai được nhắc tên. Chúng tôi nhận ra đây là một kênh nhắm-cá-nhân có khuếch đại, khác về bản chất với loa đọc ẩn danh. Thiết kế hiện tại đòi hai lớp đồng ý tách biệt, có trạng thái không-làm-phiền, và giới hạn tần suất. Robot có thể giao ít tin hơn; đó là đánh đổi có chủ đích.

Nhà tuyển dụng đọc đoạn đó biết ngay bạn từng nghĩ về hậu quả của thứ mình xây. Rất ít hồ sơ hobby có.

---

## B. PREDICTIVE CONTROL NẰM Ở ĐÂU (12h, gắn vào 7E) — BẮT BUỘC

### Làm rõ trước một hiểu nhầm

Một trong hai review có sửa đúng ý này, đáng nhắc lại cho rõ: **MPC không thay thế vòng lặp realtime.** Robot vẫn phải có vòng điều khiển cứng ở thang mili-giây để giữ ổn định vật lý. MPC ngồi **phía trên** nó.

Kiến trúc của bạn đã đúng sẵn, chỉ là bản gốc không gọi tên tầng giữa:

| Tầng | Chạy ở đâu | Chu kỳ | Tầm nhìn | Việc |
|---|---|---|---|---|
| **Điều khiển** | ESP32-S3 | 10 ms | 0 | PID vận tốc bánh. **Deterministic, jitter p99 <100µs** |
| **Local planner** | Pi 5 | 50–100 ms | **1.5–3 s** | Sinh chuỗi lệnh vận tốc, tránh va chạm dự đoán |
| **Global planner** | Pi 5 | khi cần | cả hành trình | Đường đi trên bản đồ tĩnh |

Tầng giữa là chỗ "tính toán trước tương lai" thật sự nằm. Và nó **không cần** viết MPC từ đầu — Nav2 có sẵn nhiều controller, trong đó có loại dựa trên mô phỏng cuốn chiếu (MPPI) bên cạnh các loại đơn giản hơn như pure pursuit hoặc DWB. Kiểm tra bản phân phối ROS 2 bạn cài để biết có những loại nào.

### Cái đáng làm không phải "dùng MPC", mà là "đo MPC mua được gì"

Đây là chỗ Khóa 6 vào việc, và nó biến một tính năng thành một phép đo.

**Làm:**

1. Cấu hình **3 controller** trong Nav2: một loại đơn giản (pure pursuit), một loại lấy mẫu (DWB), một loại dựa trên mô phỏng cuốn chiếu (MPPI nếu có).
2. Dựng bộ kịch bản gồm **chướng ngại động**: người đi cắt ngang ở các góc và tốc độ khác nhau, người đứng chắn rồi tránh, hành lang hẹp có hai người.
3. Chạy **1000 episode mỗi controller** qua CI của 7E.
4. Đo bốn trục, không chỉ tỉ lệ thành công:

| Trục | Vì sao |
|---|---|
| Tỉ lệ tới đích | Cơ bản |
| **Thời gian tới đích** | MPC thường mượt hơn nhưng có thể chậm hơn |
| **Gia tốc và jerk p95** | Định lượng "mượt". Jerk cao = giật cục = người xung quanh khó chịu |
| **Khoảng cách gần nhất tới người** | An toàn cảm nhận |
| **Tải CPU trên Pi 5** | MPPI nặng hơn nhiều. Có chạy nổi cùng perception không? |

5. Vẽ mặt Pareto như Khóa 6 Bài 9, chọn điểm vận hành, ghi lý do.
6. Xác nhận trên thật: 20 lần chạy mỗi controller, kiểm xem thứ hạng sim có đúng không — đúng phương pháp Bài 20.

### Số phải ra

| Kiểm tra | Kỳ vọng |
|---|---|
| Tỉ lệ thành công giữa 3 controller | Có thể **không khác nhau đáng kể** ở kịch bản dễ |
| Jerk p95 | **Khác rõ rệt.** Đây là chỗ MPPI thắng |
| Thời gian tới đích | Loại đơn giản có thể **nhanh hơn** |
| Tải CPU | MPPI cao hơn nhiều. Nếu >70% trên Pi 5, đó là một ràng buộc thật |
| Thứ hạng sim vs thật | Nên khớp. Nếu không, kiểm miền hiệu lực |

**Kết quả đáng nói nhất có thể là kết quả tiêu cực:** nếu ở tốc độ 0.5 m/s trong văn phòng nhỏ, controller đơn giản không thua kém mà lại nhẹ hơn nhiều, bạn vừa chứng minh bằng số rằng **MPC không đáng cho bài toán này**. Đó là một kết luận kỹ thuật trưởng thành hơn nhiều so với việc dùng MPC vì nó nghe hay.

---

## C. HRI ĐO ĐƯỢC (16h, gắn vào 7D) — NÊN LÀM

### Khái niệm

Cả hai review đều nhắc HRI — "khoảng cách xã hội", "hành vi lịch sự" — nhưng như một thuộc tính mềm. Nó **không mềm**; nó đo được, và proxemics có tài liệu nghiên cứu dày.

Điểm hay: nó đo được bằng đúng dữ liệu bạn đã ghi, cộng một khảo sát ngắn.

### Làm

**Phần A — hành vi robot, đo từ log.**
1. Khoảng cách gần nhất tới người, phân bố trên toàn bộ session
2. Tốc độ khi có người trong bán kính 2m
3. Có dừng hẳn khi người đi cắt ngang không, hay chỉ giảm tốc
4. Thời gian robot đứng chắn lối đi của người khác

**Phần B — phản ứng của người, đo từ camera (không lưu ảnh, chỉ trích xuất số).**
5. **Người có đổi hướng để tránh robot không?** Đây là chỉ số hay nhất — nếu người phải né robot, robot đang xâm phạm không gian của họ.
6. Tần suất người dừng lại vì robot

**Phần C — khảo sát, n ≥ 10 đồng nghiệp, sau 72h soak.**
7. Thang 1–5: thấy thoải mái hay khó chịu; robot có đoán được không; có muốn nó tiếp tục không
8. Một câu mở: "điều gì khiến bạn khó chịu nhất"

**Phần D — thử nghiệm A/B.**
9. Hai cấu hình: tốc độ 0.5 vs 0.3 m/s gần người; khoảng cách dừng 1.0 vs 1.5m
10. Đo lại cả ba phần. **Áp dụng Khóa 6 Bài 12** — với n=10 người, khảo sát của bạn có sức mạnh thống kê rất thấp; báo cáo khoảng tin cậy và đừng tuyên bố quá dữ liệu.

### Số phải ra

| Kiểm tra | Kỳ vọng |
|---|---|
| Tỉ lệ người đổi hướng tránh robot | **Nên giảm** khi robot chậm và dừng sớm hơn |
| Khảo sát n=10, thang 1–5 | Khoảng tin cậy **rất rộng**. Báo cáo trung thực, coi là tín hiệu định tính |
| Câu mở | Thường có giá trị hơn con số. Đưa nguyên văn vào báo cáo |

Việc nêu rõ "n=10 nên khảo sát này không kết luận được gì chắc chắn, nhưng đây là những gì người ta nói" là một đoạn rất mạnh — nó cho thấy bạn áp dụng cùng kỷ luật thống kê cho dữ liệu định tính lẫn định lượng.

---

## D. DỰ ĐOÁN QUỸ ĐẠO NGƯỜI (20h, gắn vào 7B/7E) — TÙY CHỌN

### Khái niệm

Bản gốc chỉ có tránh vật cản **phản ứng**: thấy người → né. Cả hai review nhắc tới dự đoán: *"trong 2 giây nữa người này sẽ ở đâu"*.

Đó là một năng lực khác thật, và nó là thứ làm chuyển động trông tự nhiên. Nhưng nó chỉ đáng làm nếu bạn **đo** được nó, và may mắn là bài toán này có metric chuẩn.

### Hai chỉ số chuẩn

| Chỉ số | Nghĩa |
|---|---|
| **ADE** (Average Displacement Error) | Sai số trung bình trên toàn bộ quỹ đạo dự đoán |
| **FDE** (Final Displacement Error) | Sai số tại thời điểm cuối của tầm dự đoán |

Cả hai đo bằng mét, ở các tầm dự đoán khác nhau (1s, 2s, 3s).

### Làm

1. **Thu dữ liệu ground truth từ chính văn phòng bạn.** Robot đứng yên, ghi lại quỹ đạo người đi qua trong nhiều giờ. Trích xuất **chỉ tọa độ theo thời gian**, không lưu ảnh — nhất quán với thiết kế privacy.
2. Ba mô hình dự đoán, từ đơn giản tới phức tạp:
   - **Vận tốc không đổi** — baseline, và nó mạnh hơn bạn tưởng
   - Vận tốc không đổi + ràng buộc bản đồ (người không đi xuyên tường)
   - Một mô hình học được, nếu dữ liệu đủ
3. Đo ADE/FDE ở tầm 1s, 2s, 3s cho cả ba, trên tập kiểm tra riêng.
4. **Đưa dự đoán vào local planner**, chạy lại thí nghiệm ở mục B, đo xem nó mua được gì.

### Số phải ra

| Kiểm tra | Kỳ vọng |
|---|---|
| FDE của baseline vận tốc không đổi ở 1s | **Nhỏ.** Người đi bộ khá dự đoán được trong thời gian ngắn |
| FDE ở 3s | Lớn hơn nhiều — người đổi hướng, dừng lại, nói chuyện |
| Mô hình phức tạp vs baseline | **Có thể không cải thiện đáng kể ở 1–2s.** Đây là kết quả rất đáng viết |
| Đưa vào planner | Đo bằng CI ở mục B. Có giảm jerk không? Có giảm khoảng cách gần nhất không? |

Dòng thứ ba lại là một kết quả tiêu cực có giá trị: trong văn phòng nhỏ ở tốc độ thấp, mô hình dự đoán tinh vi có thể không mua được gì so với giả định vận tốc không đổi. Biết và chứng minh được điều đó tốt hơn nhiều so với việc thêm một mô hình phức tạp vì nó nghe hiện đại.

---

## 2. BA CHỖ TÔI GIỮ NGUYÊN

**a) Không xây fleet management.** Một review đề xuất hệ MQTT quản lý đội robot với dashboard. Với **một** robot, đó là sân khấu — nó trông giống công việc thật mà không phải công việc thật.

Thay vào đó, tốn đúng **một trang**: thiết kế data contract và định danh sao cho N robot chạy được, rồi viết một đoạn trong README trả lời *"cái gì sẽ phải đổi ở N=10"* — tranh chấp bản đồ, phân phối task, băng thông upload, phiên bản model không đồng nhất giữa các robot. Trả lời được câu đó có giá trị phỏng vấn ngang với việc xây nó, và tốn 1/40 thời gian.

**b) Marker thay vì SLAM.** Một review đề xuất Visual SLAM hoặc lidar để tự vẽ bản đồ. Marker vẫn là lựa chọn đúng cho bạn: rẻ hơn, buộc học hiệu chuẩn camera (kỹ năng khan hiếm), và quan trọng nhất — **nó cho bạn ground truth**. Không có chân lý thì không chấm điểm được gì, kể cả SLAM sau này. Thêm lidar ở 7B nếu dư giờ, nhưng đừng thay thế.

**c) Không mua Jetson trước.** Một review đề xuất Jetson Orin Nano làm bộ não. Nguyên tắc giữ nguyên: **chỉ mua sau khi phép đo chứng minh Pi 5 không đủ.** Khóa 4 tồn tại để trả lời câu hỏi này bằng số. Mua trước rồi biện minh sau là đúng thói quen mà cả lộ trình được thiết kế để phá.

---

## 3. BA CHỖ HAI REVIEW SAI

Nêu ra không phải để bắt lỗi, mà vì cả ba đều là lỗi bạn có thể vô tình lặp lại.

**a) "Xác suất đúng mặt > 95%" — không phải xác suất.**

Đầu ra của bước match là **độ tương tự cosine** giữa hai embedding, một số trong khoảng [-1, 1]. Nó **không phải** xác suất và không được hiệu chuẩn. Ngưỡng 0.95 trên thang cosine là một ngưỡng rất chặt; "95% xác suất đúng người" là một phát biểu khác hẳn và cần hiệu chuẩn riêng (Platt scaling hoặc tương đương) mới nói được.

Đây chính xác là kiểu diễn đạt mà 7C Bài 12 được thiết kế để ngăn: **báo cáo ngưỡng và cặp FAR/FRR tại ngưỡng đó, không báo cáo "độ chính xác phần trăm".**

**b) "Thu thập hàng nghìn ảnh nhân viên để training model" — sai cả kỹ thuật lẫn privacy.**

Một review mô tả vai trò Data Labeler thu thập hàng nghìn ảnh nhân viên ở nhiều góc và ánh sáng để huấn luyện model nhận diện. Cách làm này đã lỗi thời khoảng một thập kỷ. Nhận diện khuôn mặt hiện đại dùng **embedding từ model đã huấn luyện trên tập công khai lớn**, rồi so khớp với vài ảnh đăng ký — không huấn luyện lại trên mặt nhân viên.

Và về privacy thì nó trực tiếp phá ràng buộc số 3 trong `PRIVACY.md` của bạn: không lưu ảnh thô. Một kho hàng nghìn ảnh nhân viên có nhãn là đúng thứ bạn thiết kế để không tồn tại.

Nếu cần cải thiện cho điều kiện văn phòng, cách đúng là **fine-tune trên dữ liệu tối thiểu, có đồng ý riêng cho việc đó, và xóa sau khi train** — đúng như 7E Bài 21.

**c) "Robot giờ không xử lý realtime mà xử lý trước tương lai" — một review đã tự sửa đúng, giữ nguyên bản sửa.**

Vòng lặp realtime không biến mất. Nó vẫn ở đó, ở thang mili-giây, và nó là thứ giữ robot không ngã. Cái thêm vào là một tầng lập kế hoạch dự đoán **phía trên** nó. Kiến trúc ba tầng ở mục B nói rõ điều này — và nó cũng chính là lý do bạn tách ESP32 khỏi Pi ngay từ Bài 1.

---

## 4. BẢN ĐỒ VAI TRÒ: BẠN ĐÓNG VAI NÀO

Đây là phần hữu ích nhất chắt ra từ hai review, nhưng viết lại cho một người thay vì cho một công ty.

**Nguyên tắc: biết mình KHÔNG làm vai nào cũng quan trọng ngang với biết mình làm vai nào.** Trong phỏng vấn, câu "tôi mua khung xe có sẵn vì thiết kế cơ khí không phải chỗ tôi tạo giá trị, và đây là thứ tôi sẽ cần từ một kỹ sư cơ khí nếu làm lại" mạnh hơn nhiều so với việc giả vờ đã làm tất cả.

### Vai bạn thực sự đóng

| Vai trong công ty | Bạn làm ở đâu | Bằng chứng |
|---|---|---|
| Systems / Robotics Architect | 3 quyết định kiến trúc đầu Khóa 7 | `decisions.md` |
| Embedded / Controls Engineer | 7A Bài 1–4 | Jitter p99, UMBmark, đường cong PWM |
| Localization & Navigation | 7B | Bảng độ chính xác marker, 20 lần A→B |
| Perception Engineer (applied) | 7C | ROC, FAR/FRR theo điều kiện |
| Safety & Reliability | 7D | FMEA 8 dòng đã test, thời gian phản ứng 4 tầng |
| Simulation & Evaluation | 7E + Khóa 6 | Tương quan sim–thật, bảng miền hiệu lực |
| **Data Platform Engineer** | Khóa 5 + 7A Bài 5 | MCAP, audit, Foxglove |
| **Test & Validation** | 7E Bài 19 | CI ba trạng thái, HIL |
| MLOps (nhẹ) | 7E Bài 21 | Vòng fine-tune khép kín |
| Privacy / Compliance | 7C Bài 11 | `PRIVACY.md`, test xóa dữ liệu |
| Technical Writer | Xuyên suốt | 6 bài viết |

### Vai bạn chạm nhẹ, đủ để nói chuyện

| Vai | Mức bạn chạm | Nói gì trong phỏng vấn |
|---|---|---|
| Mechanical Engineer | Mua khung sẵn, đo và hiệu chuẩn nó | "Tôi không thiết kế cơ khí. Tôi đo được hệ quả của nó lên odometry và biết cần yêu cầu gì về dung sai" |
| Electrical Engineer | Dùng module, đo dòng hãm, thiết kế mạch E-stop | "Tôi không vẽ PCB. Tôi biết dòng hãm quyết định chọn driver và nguồn, vì tôi đo nó" |
| ML Research | Dùng model pretrained, fine-tune | "Tôi không train model từ đầu. Tôi đo được model nào dùng được trên phần cứng nào, với đánh đổi gì" |
| HRI / UX | Phụ lục C nếu làm | "Tôi đo hành vi né tránh của người và khảo sát n=10, và tôi biết n=10 không kết luận được gì chắc" |

### Vai bạn cố tình bỏ

Fleet Operations, Field Support, Sales / Solution Architect, Legal. Với ba cái đầu, lý do là **quy mô** — chúng chỉ tồn tại khi có nhiều robot và nhiều khách hàng. Với Legal, bạn không bỏ hoàn toàn: bạn phải biết Nghị định 13/2023 áp vào đâu, và bạn đã biết.

### Và đây là lý do thật khiến Khóa 7 giúp cho việc xin việc

Vị trí bạn nhắm — robotics data infrastructure — trong bản đồ vai trò ở trên là bốn ô: **Data Platform + Test & Validation + Simulation & Evaluation + MLOps**.

Khóa 7 không làm bạn thành kỹ sư cơ khí hay chuyên gia control. Nó làm bạn thành người duy nhất trong phòng phỏng vấn **đã tự tay tạo ra dữ liệu mà mình xây hạ tầng để xử lý**. Khi team Controls nói "chúng tôi cần ghi joint state ở 1kHz mà không ảnh hưởng control loop", bạn không gật đầu theo lý thuyết — bạn đã tự đo jitter của chính vòng lặp đó và biết chính xác cái gì làm nó trôi.

Đó là toàn bộ luận điểm, và nó mạnh hơn "tôi làm được một con robot" rất nhiều.

---

## 5. NGÂN SÁCH GIỜ SAU KHI BỔ SUNG

| Phần | Gốc | Thêm | Mới |
|---|---|---|---|
| 7A | 60 | — | 60 |
| 7B | 80 | +20 (D, tùy chọn) | 80–100 |
| 7C | 60 | +4 (A) | 64 |
| 7D | 60 | +16 (C) | 60–76 |
| 7E | 80 | +12 (B) | 92 |
| **Tổng** | **340** | **+16 tới +52** | **356–392** |

**Nếu chỉ làm hai mục bắt buộc (A và B): +16h.** Đó là mức tôi khuyên. C và D là stretch, mở ra nếu tới 7D và 7E mà vẫn trong ngân sách.

Trần cứng giữ nguyên **450h**, và FAIL action giữ nguyên: chạm trần thì dừng ở khóa con đang làm, publish nguyên trạng, viết bài tổng kết nói rõ cái gì xong cái gì chưa.
