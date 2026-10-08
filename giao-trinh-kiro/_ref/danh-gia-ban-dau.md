# Đánh giá ban đầu (trích phần dùng làm tham chiếu cho người soạn)

## A. Ví dụ mẫu: K3 Bài 4 (DMA buffer) — chỉ các phần mới so với bản gốc

**Cầu nối:** buffer DMA là một hàng đợi kích thước cố định; định luật Little cho ngay độ trễ: L = λW ⇒ W = L/λ (ví dụ 4800 frame ÷ 24 000 frame/s).

**Gãy ở chỗ:** trong backend, khi hàng đợi cạn thì consumer chờ. Ở đây consumer là phần cứng không biết chờ: thiếu dữ liệu thì nó phát lại khung cũ hoặc phát số 0. Lỗi không nằm trong log, nó thành tiếng "tách".

**Câu hỏi ngược:**
- Vì sao không dùng một buffer DMA thật lớn và một ring buffer nhỏ, thay vì ngược lại?
- Credit-based flow control ở đây giống và khác TCP window ở chỗ nào?
- Nếu host gửi theo burst 10 ms mà jitter p99 là 8 ms, ring buffer phía MCU tối thiểu phải chứa bao nhiêu? (bài toán dimensioning theo p99)

**Liên kết ra ngoài:** jitter buffer trong VoIP, bufferbloat trong router, playout buffer của streaming video. Cùng một đánh đổi độ trễ ↔ độ tin cậy, đơn vị khác nhau.

**Hình:** notebook mô phỏng producer có jitter log-normal, quét kích thước buffer, vẽ đường cong underrun theo độ trễ. Làm trước khi nạp firmware, rồi so với số đo thật ở Bài 10.

## B. Chấm các mô hình người học đã nêu trong hội thoại Gemini K3

- "RAM đời đầu bản chất là tạo vô số buffer cho các thiết bị chạy theo clock" — ĐÚNG MỘT PHẦN. RAM tồn tại chủ yếu vì cần bộ nhớ làm việc lớn hơn thanh ghi và nhanh hơn ổ đĩa, để chứa chương trình và dữ liệu. Nối hai miền clock thường do FIFO bất đồng bộ nhỏ ngay trên chip. Buffer có thể nằm trong RAM, nhưng RAM không sinh ra vì buffer. "Flash" là bộ nhớ không mất dữ liệu khi tắt nguồn, không phải RAM.
- "Mạch có thể chạy nhanh hơn 1000 lần nhưng người ta cố tình giới hạn" — SAI. Tần số tối đa bị chặn bởi độ trễ đường dẫn chậm nhất (critical path, setup time) và công suất (P ∝ C·V²·f). Chạy nhanh hơn thì mạch tính sai. Đánh đổi thật: thiết kế đồng bộ hy sinh tốc độ lý thuyết của mạch bất đồng bộ để đổi lấy khả năng ghép khối.
- Cầu nối bị bỏ lỡ: công thức độ trễ DMA `desc_num × frame_num / sample_rate` chính là định luật Little.
- Các lượt khác cần chấm (người soạn K3 tự chấm): lượt 3 (ESP32 chỉ là dispatcher), lượt 6 (không có realtime forward 100%, luôn có buffer; "latency sẽ giảm" — thực ra buffer làm latency **tăng**), lượt 9 (loa không nguồn "dữ liệu tự chạy qua"), lượt 11 (sụt nguồn khi chung nguồn), lượt 12–13 (AI thay thế tầng vật lý), lượt 21 (RTF như một "flag" vận hành).

## C. Những gì người học đã làm, gọi đúng tên

| Đã làm | Tên chuẩn | Còn thiếu |
|---|---|---|
| Môi trường local tái tạo backend | Hermetic test, môi trường tái lập | Lockfile + image digest làm provenance (K6 Bài 7) |
| Server mock tự tạo bộ test | Test double, golden dataset | Bộ "canary" phá hoại để chứng minh test bắt được lỗi |
| Pass / fail / inconclusive | Kiểm định ba trạng thái | Power analysis: vì sao inconclusive, cần thêm bao nhiêu mẫu |
| Model AI chấm review | LLM-as-judge | Đo đồng thuận model–người (Cohen's kappa) trên tập đã gán nhãn |
| Đo trên host yên tĩnh | Cô lập nhiễu, active benchmarking (Brendan Gregg) | Chứng minh bằng số đã cô lập được (nhiệt, tần số CPU, độ lệch giữa phiên) |
| Agent tự test, sửa, deploy | Closed-loop CI | Goodhart: agent tối ưu để qua test, không phải để đúng. Cần test giữ kín |

## D. Nguồn đọc gợi ý cho khóa nền (người soạn F kiểm lại tồn tại/URL trước khi đưa vào)

- **F1:** *Statistics Done Wrong* (Alex Reinhart, đọc miễn phí online); bài nói "How NOT to Measure Latency" (Gil Tene) về coordinated omission; NIST Technical Note 1297 (biểu diễn độ bất định); GUM (JCGM 100:2008).
- **F2:** các chương testing trong *Software Engineering at Google* (đọc miễn phí); Will Wilson, "Testing Distributed Systems w/ Deterministic Simulation" (Strange Loop 2014); TigerBeetle VOPR, Antithesis; metamorphic testing (T.Y. Chen và cộng sự); tài liệu Hypothesis về property-based testing.
- **F3:** *Designing Data-Intensive Applications* (Kleppmann) — encoding, phân tán, batch, stream; Tyler Akidau "Streaming 101/102"; Jay Kreps "The Log: What every software engineer should know about real-time data's unifying abstraction".
- **F4:** Lamport "Time, Clocks, and the Ordering of Events in a Distributed System" (1978); paper Spanner (TrueTime); blog Meta Engineering về PTP trong datacenter; IEEE 1588; linuxptp docs.
- **F5:** *Making Embedded Systems* (Elecia White); bản tường thuật của Glenn Reeves về Mars Pathfinder priority inversion; *Mastering the FreeRTOS Real Time Kernel* (miễn phí).
- **F6:** NASA-STD-7009 (Standard for Models and Simulations); ASME V&V 10/20; Russ Tedrake *Robotic Manipulation* / *Underactuated Robotics* (miễn phí); tài liệu MuJoCo mục Computation.
- **F7:** *Site Reliability Engineering* (Google, miễn phí) — SLO, monitoring, postmortem; Brendan Gregg — USE method, *Systems Performance*; Williams/Waterman/Patterson "Roofline" (CACM 2009).
