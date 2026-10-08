# KHÓA 6 — SIMULATION & EVALUATION INFRASTRUCTURE

**Cho:** người đã PASS Khóa 2 và Khóa 4. Khóa 5 nên xong trước Module 5 (cần dữ liệu thật để đo gap).
**Thời lượng:** ~120h · **Trần:** 160h. Khoảng 18–20 tuần ở nhịp 6–7h/tuần.
**Chi phí:** ~0đ. GPU thuê theo giờ nếu cần, khoảng 500k–1tr cho cả khóa.
**Thay cho:** Khóa 6 gốc (SO-101), nay đẩy thành Khóa 7.

**Xong khóa này bạn có:** một môi trường nơi bạn đổi một thứ, chạy một lệnh, và nhận lại **phán quyết có căn cứ thống kê** — cộng với một bảng đo khoảng cách giữa mô hình và thế giới thật.

---

## VÌ SAO KHÓA NÀY TỒN TẠI

Năm khóa đầu xây rất tốt tầng quan sát và tầng đo. Nhưng chúng không có **vòng lặp kín**: bạn phát hiện được dữ liệu hỏng, nhưng không có chỗ để hỏi *"nếu tôi đổi tham số này, hành vi tốt lên hay xấu đi, và chắc chắn đến mức nào"*.

Đây là khóa đóng vòng lặp đó. Và nó là điều kiện tiên quyết của Khóa 7 — không có nó, Khóa 7 chỉ là một con robot hobby nữa trên YouTube.

**Ba điều khóa này KHÔNG dạy:**
- Không dạy bạn viết physics engine
- Không dạy bạn train policy (đó là Khóa 7E, và bạn sẽ dùng thư viện)
- Không dạy bạn làm đồ họa đẹp

Nó dạy bạn xây **chỗ để chạy thí nghiệm và tin được kết quả**. Đó là một bài toán hạ tầng, và bạn đã làm nó tám năm — chỉ khác payload.

---

## MỘT LUẬN ĐIỂM ĐỂ MANG XUYÊN SUỐT

> **Simulator không dạy bạn vật lý. Nó dạy bạn mô hình vật lý của người viết simulator.**
>
> Khoảng cách giữa hai thứ đó là sim-to-real gap, nó **đo được**, và đo nó là một nghề.

Nếu bạn chỉ làm Module 1–4, bạn có một công cụ CI tốt. Nếu bạn làm cả Module 5, bạn có thứ rất ít người có. **Module 5 là moat, đừng cắt nó.**

---

## CẤU TRÚC

| Module | Nội dung | Giờ |
|---|---|---|
| **1** | Determinism — nền của tất cả | 24 |
| **2** | Kịch bản là dữ liệu | 20 |
| **3** | Chạy ở quy mô | 24 |
| **4** | Đánh giá và phát hiện regression | 26 |
| **5** | **Đo sim-to-real gap** | 20 |
| **6** | CI khép kín và publish | 6 |

Giữ nguyên định dạng sáu phần: **Câu hỏi · Khái niệm · Làm · Số phải ra · Nếu ra khác · Tự kiểm tra**.

---

## CHỌN CÔNG CỤ (đọc một lần, quyết một lần, đừng quay lại)

| Công cụ | Mạnh ở | Dùng cho khóa này |
|---|---|---|
| **MuJoCo** (+ MJX / MuJoCo Warp) | Contact physics chính xác, mặc định cho manipulation và đánh giá VLA | **Engine chính** |
| **robosuite** | Benchmark manipulation chuẩn: LIBERO, MimicGen, RoboMimic | **Tầng kịch bản** |
| Isaac Sim | Digital twin, dữ liệu perception tổng hợp, cầu ROS 2 | Không dùng ở khóa này |
| Isaac Lab | RL song song trên GPU | Không dùng |
| Newton | Engine GPU mã nguồn mở trên NVIDIA Warp | Theo dõi, không dùng |
| Genesis | Multi-physics (rigid + soft + fluid) | Theo dõi |
| Gazebo | Tích hợp ROS 2, multi-robot | Chỉ nếu Khóa 7 cần |

**Chọn MuJoCo + robosuite và không đổi.** Lý do: bạn đã chạm LIBERO ở Khóa 4 Bài 7, nên không bắt đầu từ số không; MuJoCo chạy tốt trên CPU nên phần lớn khóa này không cần GPU; và mục tiêu của bạn là **hạ tầng đánh giá**, không phải đồ họa hay locomotion.

Quy tắc chống rabbit hole: mỗi lần bạn thấy mình đang so sánh simulator thay vì chạy thí nghiệm, đó là dấu hiệu trốn việc. Ghi vào `later.md` và quay lại.

---

# MODULE 1 — DETERMINISM (24h)

Đây là module nền. Mọi thứ còn lại vô nghĩa nếu module này không xong.

---

## Bài 1 — Vì sao determinism là điều kiện tiên quyết, không phải tính năng đẹp (4h)

**Câu hỏi:** chạy hai lần ra hai kết quả khác nhau thì sao?

### Khái niệm

Bạn đổi một tham số, chạy 100 episode, được 62% thành công. Trước đó là 58%. **Cải thiện 4 điểm, hay nhiễu?**

Không có determinism, câu hỏi đó không trả lời được, và toàn bộ hạ tầng đánh giá sụp. Đây là lý do determinism đứng đầu khóa: nó không phải một thuộc tính đẹp của phần mềm, nó là **điều kiện để tồn tại một phép so sánh**.

**Hai loại determinism, phải phân biệt rõ và cam kết một loại:**

| Loại | Nghĩa | Khả thi ở đâu |
|---|---|---|
| **Bit-exact** | Cùng seed → từng float giống hệt, từng bit | CPU đơn luồng: khả thi. GPU song song: rất khó |
| **Thống kê tương đương** | Cùng seed → kết quả có thể lệch nhỏ, nhưng **trong ngưỡng đã nêu trước** | Khả thi ở mọi nơi, nếu bạn định nghĩa ngưỡng |

Nhiều người vô thức mong bit-exact, không đạt được, rồi bỏ cuộc và sống với sim không tin được. Cách đúng: **cam kết một loại, viết ngưỡng ra, và chứng minh bằng số.**

**Bảy nguồn phá determinism, theo thứ tự hay gặp:**

| # | Nguồn | Biểu hiện |
|---|---|---|
| 1 | **RNG toàn cục** — `numpy.random`, `random`, `torch` dùng chung một state | Đổi thứ tự gọi hàm → đổi kết quả |
| 2 | **Seed mỗi env không độc lập** | Chạy 4 env song song ≠ chạy 4 env tuần tự |
| 3 | **Float không có tính kết hợp** — `(a+b)+c ≠ a+(b+c)` | Reduction song song trên GPU cho kết quả khác nhau mỗi lần |
| 4 | **Chọn thuật toán động** — cuDNN benchmark mode, TF32 | Lần đầu chọn kernel này, lần sau kernel khác |
| 5 | **Thứ tự thread / atomics** | Không lặp lại được |
| 6 | **Thứ tự nạp asset, duyệt thư mục** | `os.listdir` không đảm bảo thứ tự |
| 7 | **Phụ thuộc đồng hồ treo tường** | Bất kỳ `time.time()` nào ảnh hưởng tới logic |

Nguồn số 3 đáng dừng lại vì nó là nguồn sâu nhất và không sửa được bằng cách "cẩn thận hơn": cộng số thực dấu phẩy động **không có tính kết hợp**. Khi GPU cộng 4096 số theo thứ tự khác nhau giữa hai lần chạy, tổng khác nhau ở bit cuối. Sai lệch cỡ 1e-16 đó đi qua hàng nghìn bước mô phỏng và trở thành một quỹ đạo hoàn toàn khác. Hệ tiếp xúc (contact) là hệ hỗn loạn — **sai số nhỏ khuếch đại theo hàm mũ**.

Đây chính là hiện tượng bạn đã gặp ở Khóa 4: sai số làm tròn nhỏ ở vision tower tích lũy qua các solver step và làm lệch hành động vật lý. Cùng một nguyên nhân, khác tầng.

### Làm

1. Viết `DETERMINISM.md` **trước khi code**. Nội dung: bạn cam kết loại nào, ngưỡng bao nhiêu, đo bằng gì.
2. Với mỗi nguồn trong bảng 7 mục, viết một câu: nó có xuất hiện trong stack của tôi không, và nếu có thì xử lý thế nào.
3. Dự đoán: bạn nghĩ nguồn nào sẽ làm khổ bạn nhất? Commit dự đoán.

### Tự kiểm tra

1. *Hai lần chạy cho 58% và 62% trên 100 episode. Kết luận được gì?* → Không gì cả. Sai số chuẩn của tỉ lệ với n=100, p≈0.6 là khoảng 4.9 điểm phần trăm, nên khoảng tin cậy 95% rộng gần ±10 điểm. Bài 12 sẽ làm rõ.
2. *Vì sao bit-exact khó trên GPU mà dễ trên CPU đơn luồng?* → Thứ tự phép cộng cố định khi đơn luồng.

---

## Bài 2 — Dựng stack và chạy episode đầu tiên (6h)

**Câu hỏi:** từ máy trắng tới một episode chạy xong mất bao lâu?

### Làm

1. Cài MuJoCo + robosuite. **Trong Docker**, không cài thẳng vào máy — bạn sẽ cần tái lập môi trường này trên máy khác ở Bài 4.
2. Chạy một task LIBERO có sẵn với policy ngẫu nhiên. Xem nó chạy.
3. In ra **shape và ý nghĩa** của mọi thứ trong observation dict. Ghi vào `notes/`.
4. Chạy một episode và lưu toàn bộ trajectory: state, action, reward, done, info.
5. Đo: một episode mất bao lâu trên CPU? Trên bao nhiêu core?
6. Ghi lockfile pin mọi phiên bản. **Bao gồm cả phiên bản MuJoCo và robosuite** — đây là hai thứ đổi hành vi giữa các bản minor.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Một episode manipulation ngắn trên CPU | Thang **giây**, không phải phút |
| Nhiều tiến trình song song trên n core | Throughput gần tuyến tính tới số core vật lý, rồi bão hòa |
| Docker image build lại từ đầu | Ra cùng phiên bản thư viện, chứng minh bằng `pip freeze` giống hệt |

### Nếu ra khác

| Triệu chứng | Nguyên nhân |
|---|---|
| Chậm hơn nhiều so với kỳ vọng | Đang render đồ họa trong lúc chạy. **Tắt render khi benchmark** — bạn không xem, chỉ máy chạy |
| Lỗi OpenGL / EGL trong Docker | Chạy headless, dùng `osmesa` hoặc `egl` backend. Ghi cách làm vào README, người khác sẽ vấp đúng chỗ này |
| Throughput không tăng khi thêm process | Bị bound bởi bộ nhớ hoặc GIL. Dùng process chứ không dùng thread |

---

## Bài 3 — Săn nguồn phá determinism (8h)

**Câu hỏi:** cái gì trong stack của tôi đang không lặp lại được?

### Khái niệm

Đây là bài điều tra, và nó dùng đúng kỹ năng bisect bạn đã học ở Khóa 5 Bài 19 — chỉ khác là tầng bây giờ là phần mềm.

**Cấu hình phải đặt, biết trước để đỡ mất thời gian:**

```bash
export PYTHONHASHSEED=0
export CUBLAS_WORKSPACE_CONFIG=:4096:8   # cần cho torch deterministic trên CUDA
```

```python
torch.use_deterministic_algorithms(True)
torch.backends.cudnn.benchmark = False    # tắt chọn kernel động
torch.backends.cuda.matmul.allow_tf32 = False
```

Và nguyên tắc quan trọng nhất: **mỗi env một RNG riêng, seed dẫn xuất từ seed gốc theo công thức xác định.** Không dùng RNG toàn cục ở bất kỳ đâu trong đường chạy episode.

```python
# sai — dùng state toàn cục
np.random.seed(42)

# đúng — generator riêng, seed dẫn xuất
rng = np.random.default_rng(seed_root + env_index)
```

### Làm

**Bước 1 — thiết lập phép đo.** Hàm `run_episode(seed) -> trajectory_hash`. Hash toàn bộ chuỗi state bằng SHA-256 sau khi làm tròn về một số chữ số cố định. Làm tròn là có chủ đích — nó cho bạn một nút vặn giữa bit-exact và thống kê tương đương.

**Bước 2 — đo baseline.** Chạy cùng một seed 20 lần. Bao nhiêu hash khác nhau?

**Bước 3 — bisect.** Với mỗi nguồn nghi ngờ, cô lập và loại trừ từng cái một. Ghi lại từng bước như lab notebook.

**Bước 4 — bốn kịch bản phải kiểm riêng**, vì chúng hỏng theo cách khác nhau:

| Kịch bản | Câu hỏi |
|---|---|
| Cùng seed, cùng tiến trình, chạy 2 lần | Có giống nhau không? |
| Cùng seed, 2 tiến trình khác nhau | Có giống nhau không? |
| Cùng seed, chạy tuần tự vs chạy song song 8 env | **Có giống nhau không?** ← chỗ hỏng nhiều nhất |
| Cùng seed, 2 máy khác nhau | Có giống nhau không? |

Kịch bản thứ ba là kịch bản hay hỏng nhất và ít ai kiểm. Nếu chạy song song cho kết quả khác chạy tuần tự, mọi benchmark quy mô của bạn không so được với kết quả nhỏ.

**Bước 5 — nếu không đạt bit-exact, đo độ phân kỳ.** Với cùng seed, hai lần chạy phân kỳ **sau bao nhiêu bước**? Vẽ khoảng cách giữa hai quỹ đạo theo thời gian, thang log. Với hệ tiếp xúc bạn sẽ thấy đường thẳng trên thang log — đó là phân kỳ hàm mũ, và nó có tên: hệ hỗn loạn.

### Số phải ra

| Kiểm tra | Mục tiêu |
|---|---|
| Cùng seed, cùng tiến trình, CPU | **Bit-exact.** Nếu không đạt được ngay cả ở đây, còn một RNG toàn cục đâu đó |
| Cùng seed, khác tiến trình, CPU | Bit-exact sau khi đặt `PYTHONHASHSEED` |
| Tuần tự vs song song | Bit-exact nếu seed dẫn xuất đúng |
| Khác máy (cùng Docker image, cùng kiến trúc CPU) | Bit-exact hoặc rất gần |
| Khác máy (khác kiến trúc CPU / có GPU) | Có thể lệch — **ghi rõ ngưỡng chấp nhận** |
| Đồ thị phân kỳ khi có nhiễu nhỏ | Đường thẳng trên thang log = phân kỳ hàm mũ |

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Hash khác nhau ngay lần 2 cùng tiến trình | RNG toàn cục | Tìm bằng cách monkey-patch `np.random` để raise khi bị gọi |
| Tuần tự ≠ song song | Seed phụ thuộc thứ tự khởi tạo env | Dẫn xuất seed từ `env_index`, không từ thứ tự gọi |
| Chỉ khác ở vài episode, đa số giống | Có một nhánh code hiếm dùng RNG toàn cục | Chạy nhiều seed, tìm seed nào hỏng, bisect vào |
| Giống nhau 1000 bước rồi phân kỳ | Tiếp xúc. Bình thường với hệ hỗn loạn | Chuyển sang tiêu chí thống kê tương đương, và **nêu rõ** |

### Tự kiểm tra

1. *Vì sao làm tròn state trước khi hash lại là một quyết định thiết kế chứ không phải ăn gian?* → Vì nó định nghĩa rõ ngưỡng nào bạn coi là "giống nhau". Ăn gian là làm tròn tới mức mọi thứ đều giống. Trung thực là nêu ngưỡng và chứng minh nó đủ chặt để phát hiện thay đổi thật.
2. *Hai quỹ đạo phân kỳ hàm mũ thì đánh giá bằng cách nào?* → Không đánh giá theo quỹ đạo, đánh giá theo **phân bố kết quả** trên nhiều episode. Đó là Module 4.

---

## Bài 4 — Chốt determinism vào CI (6h)

**Câu hỏi:** làm sao determinism không âm thầm hỏng lại sau ba tháng?

### Khái niệm

Bạn biết câu trả lời: viết test. Điểm mới duy nhất là **test cái gì**.

### Làm

1. Test 1 — **reproducibility**: chạy N seed cố định, so hash với hash đã lưu trong repo. Fail nếu khác.
2. Test 2 — **tuần tự vs song song**: chạy cùng bộ seed hai cách, so kết quả.
3. Test 3 — **cross-machine**: chạy trong CI (máy khác máy dev của bạn), so với hash gốc. Nếu không bit-exact, so theo ngưỡng thống kê đã cam kết ở Bài 1.
4. Test 4 — **canary phá hoại**: cố tình chèn một lời gọi `np.random` toàn cục vào một nhánh hiếm. **Test phải bắt được.** Nếu không bắt được, test của bạn chưa đủ chặt — đây là cùng nguyên lý với test case tổng hợp ở Khóa 2.
5. Chạy toàn bộ trên GitHub Actions. Thời gian chạy phải dưới 10 phút để nó thực sự được chạy.

### Số phải ra

| Kiểm tra | Ngưỡng |
|---|---|
| Test suite chạy trong CI | <10 phút |
| Canary phá hoại | **Bị bắt 100%** |
| Hash lưu trong repo | Có, và có script để cập nhật khi cố ý thay đổi |

Điểm cuối quan trọng về mặt vận hành: đôi khi bạn **cố ý** thay đổi hành vi (nâng bản MuJoCo chẳng hạn). Phải có quy trình cập nhật hash kèm ghi chú lý do, chứ không phải sửa lén. Đó là schema migration, đổi miền.

---

# MODULE 2 — KỊCH BẢN LÀ DỮ LIỆU (20h)

---

## Bài 5 — Kịch bản không phải script (8h)

**Câu hỏi:** "tôi đã test cấu hình nào" là một câu hỏi trả lời được hay không?

### Khái niệm

Đây là lỗi thiết kế phổ biến nhất trong hạ tầng đánh giá tự chế: kịch bản nằm trong code Python, hardcode, mỗi lần đổi thì sửa file. Hậu quả:

- Không biết một kết quả cũ được sinh bằng kịch bản nào
- Không sinh được biến thể một cách hệ thống
- Không so được kết quả giữa hai lần chạy cách nhau ba tuần
- Không ai ngoài bạn chạy lại được

**Cách đúng: kịch bản là một artifact dữ liệu có version**, giống hệt cách bạn đã đối xử với schema ở Khóa 2 và với config benchmark ở Khóa 4. Bạn đã biết mô hình này; ở đây chỉ là áp dụng lại.

Một định nghĩa kịch bản tối thiểu phải có:

```yaml
scenario_version: "1.2"
scenario_id: "pick_place_cube_baseline"
task: "libero_object/pick_up_the_alphabet_soup"
initial_state:
  object_pose: {x: 0.1, y: 0.0, z: 0.82, yaw: 0.0}
  robot_qpos: [...]
physics:
  timestep: 0.002
  solver_iterations: 50
  friction: {sliding: 1.0, torsional: 0.005, rolling: 0.0001}
episode:
  max_steps: 500
  success_criteria: "object_z > 0.9 for >= 10 consecutive steps"
seed_policy: "derive_from(seed_root, episode_index)"
```

**Ba trường đáng chú ý:**

`physics.timestep` và `solver_iterations` nằm trong kịch bản chứ không nằm trong code, vì chúng **thay đổi kết quả**. Một kết quả không kèm hai giá trị này là một kết quả không tái lập được.

`success_criteria` viết bằng biểu thức, không phải bằng lời. Bài 11 sẽ nói kỹ.

`seed_policy` khai báo cách dẫn xuất seed — nối trực tiếp với Module 1.

### Làm

1. Thiết kế schema kịch bản. Dùng JSON Schema hoặc Pydantic để validate.
2. Viết loader: đọc file → dựng env. **Không** cho phép tham số nào đi vòng qua loader.
3. Chuyển ≥5 task LIBERO thành file kịch bản.
4. Test: hai kịch bản có cùng nội dung nhưng khác thứ tự trường phải cho cùng kết quả (hash chuẩn hóa).
5. Version schema từ v1. Test backward compatibility như Khóa 2.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Mọi tham số ảnh hưởng kết quả đều nằm trong file kịch bản | Chứng minh bằng cách grep code tìm hằng số hardcode |
| Đổi một trường trong kịch bản | Kết quả đổi. Đổi trường không liên quan → kết quả không đổi |
| Kịch bản v1 chạy bằng loader v2 | Thành công |

---

## Bài 6 — Sinh kịch bản có hệ thống (6h)

**Câu hỏi:** làm sao phủ 500 biến thể mà không viết 500 file tay?

### Khái niệm

Bạn cần hai thứ khác nhau, đừng trộn:

| | Mục đích | Cách sinh |
|---|---|---|
| **Sweep** | Phủ có hệ thống một không gian tham số | Lưới, hoặc Latin hypercube |
| **Randomization** | Tạo đa dạng để test tính bền vững | Lấy mẫu từ phân bố, có seed |

Sweep dùng để trả lời *"tham số này ảnh hưởng thế nào"*. Randomization dùng để trả lời *"policy này có bền không"*. Trộn hai cái sẽ không trả lời được câu nào.

### Làm

1. Viết generator: kịch bản cơ sở + spec biến thiên → N kịch bản con.
2. Mỗi kịch bản con có `parent_scenario_id` và `variation_params` — đây là **lineage**, khái niệm bạn đã dùng ở Khóa 2.
3. Sinh 3 bộ: sweep ma sát (10 điểm), sweep vị trí vật (5×5 lưới), randomization 100 mẫu.
4. Lưu bộ kịch bản thành một artifact có hash. Kết quả sẽ tham chiếu tới hash này.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Sinh lại cùng spec | Ra **đúng cùng bộ kịch bản**, hash giống hệt |
| Mỗi kịch bản con | Truy ngược được về cha và về spec biến thiên |

---

## Bài 7 — Provenance: từ kết quả truy ngược về mọi thứ (6h)

**Câu hỏi:** nhìn một con số trong báo cáo, tôi truy về được những gì?

### Khái niệm

Nguyên tắc số 5 của lộ trình gốc: *dữ liệu không kèm calibration state và provenance là dữ liệu vô giá trị.* Ở đây "calibration state" đổi tên thành cấu hình sim, nhưng nguyên tắc y hệt.

**Mọi kết quả phải truy ngược về sáu thứ:**

| # | Truy về | Ghi bằng |
|---|---|---|
| 1 | Kịch bản | `scenario_id` + `scenario_hash` |
| 2 | Code | git commit hash, và cờ dirty nếu working tree bẩn |
| 3 | Môi trường | Docker image digest, lockfile hash |
| 4 | Policy / config được test | checkpoint hash hoặc version |
| 5 | Seed | seed gốc + công thức dẫn xuất |
| 6 | Phần cứng | CPU model, số core, có GPU không |

Thiếu một trong sáu, kết quả không tái lập được, và bạn sẽ phát hiện điều đó vào đúng lúc cần nhất — khi có người hỏi.

### Làm

1. Thêm cả sáu trường vào output. **Fail cứng nếu working tree bẩn** và không có cờ `--allow-dirty`.
2. Viết `reproduce.py`: đưa vào một run_id, script tự dựng lại đúng môi trường và chạy lại.
3. Test: lấy một kết quả từ 2 tuần trước, chạy `reproduce.py`, so kết quả.

### Số phải ra

| Kiểm tra | Ngưỡng |
|---|---|
| `reproduce.py` trên kết quả cũ | Ra kết quả trong ngưỡng determinism đã cam kết |
| Chạy với working tree bẩn | Bị chặn, trừ khi có cờ tường minh |

---

# MODULE 3 — CHẠY Ở QUY MÔ (24h)

Module này là sân nhà của bạn. Tôi sẽ nói ngắn ở chỗ bạn đã biết và nói kỹ ở chỗ khác biệt.

---

## Bài 8 — Song song hóa và throughput thật (8h)

**Câu hỏi:** chạy 10.000 episode mất bao lâu, và nút thắt ở đâu?

### Làm

1. Ba chiến lược, đo cả ba:
   - Nhiều process trên một máy (multiprocessing)
   - Vectorized env trong một process (MuJoCo hỗ trợ batch)
   - MJX / MuJoCo Warp trên GPU
2. Với mỗi chiến lược: đo throughput (episode/phút), CPU/GPU utilization, RAM peak.
3. Vẽ throughput theo số worker. Tìm điểm bão hòa.
4. **Kiểm tra lại determinism ở mỗi chiến lược** — Module 1 Bài 3 kịch bản 3. Song song hóa là nơi determinism hay chết.
5. Tính chi phí: 10.000 episode tốn bao nhiêu giờ CPU, và nếu thuê thì bao nhiêu tiền.

### Số phải ra

| Kiểm tra | Kỳ vọng |
|---|---|
| Throughput theo số worker | Gần tuyến tính tới số **core vật lý**, rồi bão hòa. Hyperthread cho lợi ích nhỏ |
| CPU utilization lúc bão hòa | Gần 100%. Nếu thấp hơn nhiều, bị bound bởi I/O hoặc khóa |
| GPU (MJX) vs CPU | Lợi thế lớn ở batch to; **có thể tệ hơn ở batch nhỏ** do overhead |
| Determinism sau song song hóa | Giữ nguyên, hoặc lệch trong ngưỡng đã nêu |

### Nếu ra khác

| Triệu chứng | Nguyên nhân |
|---|---|
| Throughput tăng rồi **giảm** khi thêm worker | Tranh chấp bộ nhớ hoặc cache thrashing. Tìm điểm tối ưu, đừng chạy max core |
| RAM tăng tuyến tính tới hết | Mỗi worker giữ một bản model đầy đủ. Dùng shared memory hoặc giảm worker |
| GPU utilization thấp | Batch quá nhỏ, hoặc đang copy qua lại host–device mỗi bước |

---

## Bài 9 — Artifact management: output của 10.000 episode đi đâu (8h)

**Câu hỏi:** chạy 10.000 episode sinh ra bao nhiêu dữ liệu, và giữ cái gì?

### Khái niệm

Đây là chỗ hạ tầng đánh giá tự chế chết lần thứ hai (lần thứ nhất là determinism). Người ta lưu toàn bộ mọi thứ, đĩa đầy sau hai tuần, rồi bắt đầu xóa bừa, và mất khả năng so sánh.

**Phân tầng lưu trữ, quyết định trước:**

| Tầng | Lưu gì | Giữ bao lâu | Kích thước |
|---|---|---|---|
| **Summary** | Một dòng mỗi episode: success, reward, số bước, lý do kết thúc | **Mãi mãi** | Rất nhỏ |
| **Aggregate** | Thống kê mỗi run: tỉ lệ, phân vị, khoảng tin cậy | Mãi mãi | Rất nhỏ |
| **Trajectory** | State/action đầy đủ | Chỉ episode thất bại + mẫu ngẫu nhiên episode thành công | Trung bình |
| **Video** | Render | Chỉ khi được yêu cầu tường minh | Lớn |

**Nguyên tắc: giữ mọi episode thất bại, lấy mẫu episode thành công.** Episode thất bại là nơi có thông tin; episode thành công giống nhau cả.

### Làm

1. Implement phân tầng trên.
2. **Ghi trajectory ra MCAP** — dùng lại toàn bộ schema và writer của Khóa 5. Sim là một nguồn dữ liệu như mọi nguồn khác; không có lý do gì dùng định dạng riêng.
3. Object store (MinIO) như Khóa 5 Bài 14.
4. Index vào DB như Khóa 5 Bài 15, trả lời được: *"mọi episode thất bại với ma sát > 0.8 trong tuần qua"*.
5. Đo: 10.000 episode sinh ra bao nhiêu GB ở mỗi tầng.
6. **Chạy tool audit của Khóa 2 lên MCAP sinh từ sim.** Nó có bắt được gì không?

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Summary của 10.000 episode | Vài MB |
| Truy vấn "episode thất bại theo điều kiện" | <2 giây |
| Tool Khóa 2 chạy trên dữ liệu sim | **Nên báo sạch.** Sim không rớt frame, không lệch timestamp |

Điểm cuối là một quan sát đáng viết vào bài: **dữ liệu sim sạch một cách phi tự nhiên.** Tool audit của bạn không tìm thấy gì, và đó chính là bằng chứng đầu tiên, định lượng, cho luận điểm "sim không dạy bạn vật lý". Nó nối thẳng vào Module 5.

---

## Bài 10 — Từ run tới báo cáo (8h)

**Câu hỏi:** một lệnh chạy xong, người đọc thấy gì?

### Làm

1. Report generator: HTML tự chứa, có biểu đồ, sinh tự động cuối mỗi run.
2. Nội dung bắt buộc: tỉ lệ thành công **theo từng task** (không chỉ trung bình — bài học Khóa 4 Bài 8), khoảng tin cậy, phân bố số bước, top lý do thất bại, provenance đầy đủ.
3. So sánh hai run: diff, đánh dấu chênh lệch có ý nghĩa thống kê và chênh lệch không.
4. Link tới video/trajectory của episode thất bại tiêu biểu.

### Số phải ra

Người khác mở báo cáo và trả lời được ba câu mà không hỏi bạn: *chạy cái gì*, *kết quả thế nào*, *khác lần trước ra sao và có đáng tin không*.

---

# MODULE 4 — ĐÁNH GIÁ VÀ REGRESSION (26h)

---

## Bài 11 — Định nghĩa thành công bằng toán (6h)

**Câu hỏi:** "robot làm được task" nghĩa là gì, chính xác?

### Khái niệm

Cùng loại kỷ luật với Khóa 2 Bài 11–14, nơi bạn định nghĩa từng lớp lỗi bằng công thức chứ không bằng lời. Ở đây đối tượng là thành công thay vì lỗi.

**Ba cách định nghĩa sai hay gặp:**

| Định nghĩa | Vấn đề |
|---|---|
| "Vật được nhấc lên" | Nhấc lên rồi rơi có tính không? |
| "Reward > ngưỡng" | Reward là đại lượng dùng để train, không phải để đánh giá. Reward hacking |
| Dùng cờ `success` có sẵn của môi trường | Bạn không biết nó định nghĩa thế nào. **Đọc source, đừng tin** |

**Định nghĩa đúng có ba phần:** điều kiện, thời lượng duy trì, và điều kiện loại trừ.

```
success = (object_z > 0.90) 
          AND (duy trì ≥ 10 bước liên tiếp)
          AND (không va chạm với chướng ngại trong toàn episode)
          AND (episode kết thúc trước max_steps)
```

Và mỗi lần thất bại phải được **phân loại**, không chỉ đánh dấu:

| Lý do thất bại | Ý nghĩa |
|---|---|
| `timeout` | Không xong trong giới hạn bước |
| `dropped` | Đã nắm được rồi làm rơi |
| `never_grasped` | Chưa từng nắm được |
| `collision` | Va chạm gây kết thúc |
| `sim_unstable` | **Vật lý nổ** — không phải lỗi policy, là lỗi sim |

Loại cuối cùng quan trọng và hay bị bỏ sót: nếu solver phân kỳ và vật bay ra vô cực, đó không phải policy kém, đó là kịch bản hỏng. Gộp nó vào tỉ lệ thất bại sẽ làm sai lệch mọi so sánh.

### Làm

1. Viết định nghĩa thành công cho ≥5 task, dạng biểu thức trong file kịch bản.
2. Implement phân loại thất bại với ≥5 loại, gồm `sim_unstable`.
3. Test từng loại bằng kịch bản tổng hợp cố ý kích hoạt nó.
4. Chạy trên dữ liệu cũ, xem phân bố lý do thất bại.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Mỗi loại thất bại | Kích hoạt được bằng test tổng hợp |
| Tỉ lệ `sim_unstable` | **Nên rất thấp.** Nếu >1%, cấu hình vật lý của bạn có vấn đề — sửa trước khi đi tiếp |
| So định nghĩa của bạn với cờ `success` mặc định | Có thể khác. Nếu khác, giải thích được vì sao |

---

## Bài 12 — Bao nhiêu episode là đủ (8h)

**Câu hỏi:** 50 episode có đủ để nói một thay đổi là cải thiện không?

**Đây là bài quan trọng nhất Module 4, và có lẽ là bài có giá trị khác biệt cao nhất cả khóa.**

### Khái niệm

Thành công/thất bại là biến nhị phân. Sai số chuẩn của một tỉ lệ:

```
SE = √( p(1−p) / n )
```

Khoảng tin cậy 95% ≈ ±1.96 × SE. Thay số:

| n episode | Nửa độ rộng CI 95% tại p = 0.5 |
|---|---|
| 50 | **±13.9 điểm phần trăm** |
| 100 | ±9.8 |
| 400 | ±4.9 |
| 1.000 | ±3.1 |
| 10.000 | ±0.98 |

**Đọc lại dòng đầu.** Với 50 episode — con số rất phổ biến trong các báo cáo đánh giá robot — bạn đo được tỉ lệ thành công với độ chính xác ±14 điểm. Nghĩa là 50% và 63% **không phân biệt được**.

Và để **so sánh hai cấu hình** thì tệ hơn nữa, vì sai số của cả hai cộng vào. Số episode cần mỗi nhóm để phát hiện một chênh lệch thật, với power 0.8 và α = 0.05:

| Từ p₁ | Tới p₂ | Chênh | n cần **mỗi nhóm** |
|---|---|---|---|
| 0.50 | 0.70 | 20 điểm | ~90 |
| 0.50 | 0.60 | 10 điểm | ~385 |
| 0.50 | 0.55 | 5 điểm | ~1.560 |
| 0.80 | 0.90 | 10 điểm | ~196 |
| 0.80 | 0.85 | 5 điểm | ~903 |

**Kết luận thực tế:** nếu muốn phát hiện cải thiện 5 điểm, bạn cần khoảng 1.500 episode mỗi nhóm. Đó là lý do Module 3 tồn tại — hạ tầng chạy quy mô không phải để khoe, nó là **điều kiện để có một kết luận**.

Và đây là đoạn đáng viết thành bài: phần lớn kết quả đánh giá robot công bố công khai dùng vài chục episode mỗi task, tức là chúng không có đủ sức mạnh thống kê để phân biệt những chênh lệch mà chúng đang tuyên bố. Bạn có thể chứng minh điều đó bằng số, bằng chính công cụ của mình.

**Một chi tiết kỹ thuật:** với n nhỏ hoặc p gần 0/1, xấp xỉ chuẩn sai. Dùng **khoảng Wilson score** thay vì công thức trên. Thư viện thống kê có sẵn; điều quan trọng là biết khi nào cần.

### Làm

1. Implement tính CI (Wilson) và kiểm định hai tỉ lệ trong harness.
2. Viết hàm **power analysis**: đưa vào p kỳ vọng và chênh lệch muốn phát hiện → trả về n cần thiết.
3. **Bắt harness từ chối kết luận** khi n không đủ. Thay vì in "62% vs 58%, cải thiện", in "62% [CI: 52–71] vs 58% [CI: 48–68], không phân biệt được ở n=100; cần n≈385 để phát hiện chênh lệch 10 điểm".
4. Thực nghiệm kiểm chứng: lấy **cùng một** policy, chạy hai lần với seed khác nhau, n = 50, 100, 400, 1000. Xem chênh lệch giả tạo giữa hai lần chạy giống hệt nhau lớn đến đâu.
5. Vẽ: chênh lệch quan sát được giữa hai run giống hệt, theo n.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Hai run cùng policy, n=50 | Chênh lệch quan sát có thể tới **10–15 điểm** dù không có khác biệt thật |
| Hai run cùng policy, n=1000 | Chênh lệch thu về vài điểm |
| Power analysis vs bảng trên | Khớp |
| Harness gặp n không đủ | **Từ chối kết luận**, không im lặng báo cáo |

Bước 4 là bước sẽ thay đổi cách bạn đọc mọi báo cáo robot từ nay về sau.

### Tự kiểm tra

1. *Báo cáo nói "phương pháp mới đạt 78% so với baseline 71%, n=50 mỗi bên". Tin được không?* → Không. Với n=50, CI mỗi bên khoảng ±12 điểm; hai khoảng chồng lên nhau rất nhiều. Cần khoảng 700 episode mỗi bên để phát hiện chênh lệch 7 điểm quanh mức đó.
2. *Vì sao phát hiện chênh lệch quanh p=0.8 dễ hơn quanh p=0.5?* → Vì phương sai `p(1−p)` cực đại tại p=0.5 và giảm về hai đầu.

---

## Bài 13 — Phát hiện regression tự động (6h)

**Câu hỏi:** làm sao biết thay đổi hôm nay làm hỏng thứ đã chạy được tháng trước?

### Khái niệm

Bạn biết regression testing. Điểm khác duy nhất: **verdict phải là thống kê, không phải so bằng**. `assert success_rate == 0.62` là vô nghĩa. `assert not significantly_worse_than(baseline)` mới đúng.

**Ba loại verdict, không phải hai:**

| Verdict | Nghĩa |
|---|---|
| **PASS** | Không tệ hơn baseline một cách có ý nghĩa |
| **FAIL** | Tệ hơn baseline một cách có ý nghĩa |
| **INCONCLUSIVE** | Không đủ episode để kết luận |

Loại thứ ba là loại hầu hết hệ CI thiếu, và thiếu nó thì hệ tự lừa mình: mọi thay đổi đều PASS chỉ vì n quá nhỏ để phát hiện bất cứ gì.

### Làm

1. Lưu baseline có version. Cập nhật baseline là hành động tường minh, có ghi lý do.
2. Verdict ba trạng thái, gồm INCONCLUSIVE.
3. Kiểm tra **theo từng task**, không chỉ tổng — bài học Khóa 4: trung bình giữ nguyên nhưng phân bố theo task dịch chuyển.
4. Hiệu chỉnh đa kiểm định: test 20 task cùng lúc thì ở α=0.05 bạn kỳ vọng ~1 task báo động giả. Dùng Bonferroni hoặc kiểm soát FDR, và **ghi rõ dùng cái nào**.
5. **Canary phá hoại:** chèn thay đổi làm giảm success rate đúng 5 điểm ở một task. CI phải bắt được — hoặc phải nói INCONCLUSIVE nếu n không đủ, chứ không được nói PASS.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Canary −5 điểm, n đủ | FAIL |
| Canary −5 điểm, n=50 | **INCONCLUSIVE**, không phải PASS |
| Không thay đổi gì | PASS, tỉ lệ báo động giả gần α sau hiệu chỉnh |
| Ngưỡng phát hiện tối thiểu | **Nêu bằng số trong README** |

Dòng cuối là một tiêu chí PASS của khóa. Một hệ CI không biết giới hạn phát hiện của chính nó là một hệ CI nguy hiểm.

---

## Bài 14 — Domain randomization và đo xem nó mua được gì (6h)

**Câu hỏi:** randomization làm policy bền hơn — bền hơn bao nhiêu?

### Khái niệm

Domain randomization là kỹ thuật chuẩn để thu hẹp sim-to-real gap: ngẫu nhiên hóa ma sát, khối lượng, ánh sáng, độ trễ, nhiễu cảm biến trong lúc train, để policy không bám vào một cấu hình cụ thể.

Phần lớn người dùng nó mà không đo. Bạn sẽ đo.

**Đánh đổi cần định lượng:** randomization mạnh thường làm giảm hiệu năng trên phân bố gốc để tăng hiệu năng ngoài phân bố. Cường độ tối ưu không phải "càng nhiều càng tốt", nó là một điểm trên đường cong — và đó là đúng loại đường cong bạn đã vẽ hai lần rồi, ở Khóa 3 Bài 10 và Khóa 4 Bài 9.

### Làm

1. Định nghĩa ≥4 trục randomization trong schema kịch bản, mỗi trục có cường độ chỉnh được: ma sát, khối lượng, độ trễ actuator, nhiễu quan sát.
2. Với mỗi mức cường độ (0%, 25%, 50%, 100%), đánh giá **hai** tập:
   - **In-distribution**: cùng phân bố đã dùng
   - **Out-of-distribution**: giá trị nằm ngoài dải train
3. n đủ theo Bài 12 — đây là chỗ bạn cần Module 3 thật sự.
4. Vẽ hai đường theo cường độ randomization. Tìm điểm cắt.
5. Ghi quyết định vào `decisions.md` kèm số.

### Số phải ra

| Kiểm tra | Kỳ vọng |
|---|---|
| In-distribution theo cường độ | Giảm dần khi randomization mạnh lên |
| Out-of-distribution theo cường độ | Tăng rồi có thể bão hòa hoặc giảm |
| Hai đường cắt nhau | **Có một điểm tối ưu.** Nếu không thấy, dải randomization của bạn quá hẹp |

---

# MODULE 5 — ĐO SIM-TO-REAL GAP (20h)

**Đây là moat. Nếu phải cắt scope, cắt Module 3 xuống MVP, không cắt module này.**

Bốn module đầu cho bạn một công cụ CI tốt — nhiều người xây được. Module này cho bạn thứ rất ít người có, và nó là cây cầu trực tiếp giữa Khóa 5 (thế giới thật) và Khóa 6 (mô hình).

---

## Bài 15 — Định nghĩa gap sao cho đo được (6h)

**Câu hỏi:** "sim không giống thật" — không giống ở chỗ nào, bao nhiêu?

### Khái niệm

Câu "sim-to-real gap" thường được dùng như một lời than, không phải một đại lượng. Bước đầu là biến nó thành số.

**Bốn mức độ đo, từ dễ tới khó:**

| Mức | Đo gì | Khi nào dùng |
|---|---|---|
| **1 — Đại lượng tất định** | Chu kỳ, tần số, thời gian rơi — thứ có công thức giải tích | Hiện tượng đơn giản. **Bắt đầu ở đây** |
| **2 — Quỹ đạo** | RMSE giữa quỹ đạo sim và quỹ đạo thật theo thời gian | Hệ không hỗn loạn, thời gian ngắn |
| **3 — Phân bố** | Khoảng cách giữa phân bố kết quả sim và thật (KS, Wasserstein) | Hệ hỗn loạn, nơi quỹ đạo đơn lẻ vô nghĩa |
| **4 — Chuyển giao hiệu năng** | Tương quan giữa success rate trong sim và ngoài thật | Cần robot thật — để Khóa 7 |

**Mức 2 có một cái bẫy quan trọng.** Với hệ tiếp xúc hỗn loạn, hai quỹ đạo phân kỳ hàm mũ ngay cả trong cùng một simulator (bạn đã thấy ở Module 1 Bài 3). So quỹ đạo sim với quỹ đạo thật sau 5 giây là vô nghĩa. Với hệ như vậy, **mức 3 là mức đúng** — so phân bố, không so đường đi.

Biết chọn mức nào cho hiện tượng nào chính là kỹ năng ở đây.

### Làm

1. Viết `GAP_METRICS.md`: với mỗi hiện tượng bạn định đo, mức nào phù hợp và tại sao.
2. Implement metric cho mức 1 và 3. Mức 2 chỉ dùng cho cửa sổ thời gian ngắn.
3. Định nghĩa **thời gian phân kỳ**: sau bao lâu thì sai lệch vượt ngưỡng. Đây là đại lượng hữu ích hơn RMSE tại một thời điểm.

---

## Bài 16 — Con lắc: ba đường phải gặp nhau (8h)

**Câu hỏi:** công thức nói một đằng, thực đo nói một nẻo, sim nói đằng thứ ba — ai đúng?

**Đây là thí nghiệm trung tâm của Module 5, và nó chỉ tốn một sợi dây, một quả nặng, và cái rig bạn đã có từ Khóa 5.**

### Khái niệm

Con lắc được chọn vì nó là hiện tượng vật lý hiếm hoi thỏa **cả ba** điều kiện: có công thức giải tích, đo được bằng thiết bị bạn có, và mô hình được trong MuJoCo trong 20 dòng.

Đây chính là **kiểm tra chéo ba đường** của Khóa 1, nâng lên tầng cao nhất: tính từ nguyên lý đầu, đo trực tiếp, và mô phỏng.

**Công thức, con lắc đơn (dây nhẹ, quả nặng tập trung), biên độ nhỏ:**

```
T = 2π √(L / g)
```

Với `g = 9.787 m/s²` ở Hà Nội (không phải 9.81 — bạn đã xác lập con số này ở Khóa 5 Bài 4):

| L | T tính được |
|---|---|
| 0.30 m | 1.100 s |
| 0.50 m | 1.420 s |
| 1.00 m | 2.008 s |

**Và đây là chi tiết đẹp nhất của bài này:** công thức trên **chỉ đúng ở biên độ nhỏ**. Ở biên độ lớn, chu kỳ dài hơn, xấp xỉ bậc hai:

```
T(θ₀) ≈ T₀ × (1 + θ₀²/16)
```

| Biên độ θ₀ | Sai lệch so với công thức nhỏ |
|---|---|
| 10° (0.175 rad) | +0.19% |
| 20° (0.349 rad) | +0.76% |
| 30° (0.524 rad) | **+1.7%** |
| 45° (0.785 rad) | +3.9% |

Với chu kỳ ~1.4s, +1.7% là **24 mili-giây** — hoàn toàn đo được bằng IMU 200Hz.

Nghĩa là: **bạn đo được chính xác điểm mà công thức sách giáo khoa bắt đầu sai.** Đó là sim-to-real gap thu nhỏ, vì một công thức cũng là một mô hình, và mọi mô hình đều có miền hiệu lực. Bài học này lớn hơn con lắc rất nhiều.

**Nếu dùng thanh cứng thay vì dây + quả nặng** (con lắc vật lý, thanh đều, quay quanh một đầu):

```
T = 2π √(2L / 3g)
```

L = 0.50 m → T = 1.160 s. Nếu bạn đo ra 1.16 mà mong 1.42, bạn không sai — bạn đang dùng sai mô hình. Đó cũng là một bài học.

### Làm

**Phần A — tính.** Chọn L, chọn loại con lắc, tính T cho 4 biên độ: 10°, 20°, 30°, 45°. Viết vào `prediction.md`. **Commit trước khi đo.**

**Phần B — đo thật.** Hai cách, làm cả hai:
1. **IMU gắn trên con lắc**, 200–500 Hz. Chu kỳ đọc ra từ tín hiệu gia tốc — dùng FFT hoặc đếm zero-crossing. Bạn đã làm FFT ở Khóa 3 Bài 7.
2. **Camera + LED**, dùng phương pháp hàng rolling shutter của Khóa 5 Bài 11 để có độ phân giải dưới mili-giây.

Đo ít nhất 20 chu kỳ mỗi biên độ và lấy trung bình — sai số giảm theo √n.

**Phần C — đo suy giảm.** Biên độ giảm theo hàm mũ: `A(t) = A₀ e^(−γt)`. Fit γ từ dữ liệu thật. Đây là ma sát không khí và ma sát trục — thứ **không có trong công thức lý tưởng**.

**Phần D — mô phỏng.** Dựng cùng con lắc trong MuJoCo. Chạy cùng 4 biên độ. Đo T bằng đúng phương pháp đã dùng cho dữ liệu thật (quan trọng: cùng phương pháp, nếu không bạn đang so hai thứ khác nhau).

**Phần E — bảng ba đường.**

| Biên độ | T công thức | T đo thật | T sim (damping mặc định) | T sim (damping đã fit) |
|---|---|---|---|---|
| 10° | | | | |
| 20° | | | | |
| 30° | | | | |
| 45° | | | | |

**Phần F — system identification.** Chỉnh hệ số damping trong MuJoCo cho tới khi đường cong suy giảm của sim khớp với thực đo. Ghi lại giá trị. **Bạn vừa làm system identification** — đó chính là công việc cốt lõi của "simulation realism", một trong năm kỹ năng khan hiếm nhất của physical AI.

**Phần G — kiểm tra chéo.** Sau khi fit damping ở biên độ 30°, **dự đoán** đường cong suy giảm ở biên độ 45° rồi mới đo. Khớp không? Nếu không, mô hình damping của bạn sai dạng (ví dụ ma sát thật phụ thuộc vận tốc bậc hai chứ không bậc một).

Phần G là phần phân biệt fit đường cong với hiểu hệ thống.

### Số phải ra

| Kiểm tra | Ngưỡng |
|---|---|
| T đo thật vs công thức, biên độ 10° | Lệch **<1%** |
| T đo thật vs công thức, biên độ 30° | Lệch **≈ +1.7%**, đúng chiều dự đoán |
| T sim vs T đo thật, sau khi fit | Lệch **<1%** |
| Đường cong suy giảm sim vs thật, sau khi fit γ | Khớp trong 10 chu kỳ đầu |
| Dự đoán ngoại suy sang 45° (phần G) | Lệch nhỏ nếu mô hình damping đúng dạng; **lệch lớn là một phát hiện** |

### Nếu ra khác

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| T đo lệch >3% ở biên độ nhỏ | Sai L (đo từ điểm treo tới **tâm khối**, không tới đầu quả nặng), hoặc là con lắc vật lý chứ không phải con lắc đơn | Đo lại L, hoặc đổi công thức |
| Không thấy hiệu ứng biên độ lớn | Biên độ chưa đủ lớn, hoặc độ phân giải đo chưa đủ | Lên 45°, tăng số chu kỳ đo |
| Sim không suy giảm chút nào | MuJoCo mặc định damping rất nhỏ | Đúng như dự đoán. Đó chính là gap bạn sắp đo |
| Fit được damping ở 30° nhưng sai ở 45° | Mô hình damping sai dạng — ma sát thật thường có thành phần bậc hai theo vận tốc | **Đây là kết quả tốt.** Viết nó vào bài |

### Vì sao bài này đáng 8 giờ

Nó chứa toàn bộ luận điểm của khóa trong một thí nghiệm rẻ tiền:

- Công thức là một mô hình, có miền hiệu lực, và bạn **đo được** ranh giới đó
- Simulator là một mô hình khác, với sai lệch khác, và bạn **đo được** sai lệch đó
- Hiệu chỉnh mô hình theo dữ liệu thật là một quy trình, không phải một phép màu
- Và cách duy nhất biết mô hình đúng là **dự đoán rồi kiểm**, không phải fit rồi khoe

Khi ai đó hỏi bạn "anh hiểu sim-to-real gap thế nào", bạn không định nghĩa. Bạn mở bảng này ra.

---

## Bài 17 — Bảng gap theo kênh và giới hạn hiệu lực (6h)

**Câu hỏi:** simulator của tôi đáng tin tới đâu, cụ thể?

### Khái niệm

Sau Bài 16 bạn có một hiện tượng đã đo. Bài này mở rộng thành một **bảng hiệu lực** — tài liệu nói rõ sim đúng ở đâu và sai ở đâu.

Đây là thứ mà đội sim ở công ty thật phải duy trì, và gần như không có bản công khai nào.

### Làm

1. Chọn thêm 2 hiện tượng đo được bằng rig của bạn:
   - **Vật rơi tự do**: `t = √(2h/g)`, đo bằng camera high-fps hoặc bằng va chạm trên IMU. h = 1.0 m → t = 0.452 s ở g Hà Nội
   - **Vật trượt trên mặt nghiêng**: đo góc bắt đầu trượt → suy ra hệ số ma sát tĩnh. Đây là cách đo trực tiếp một tham số bạn phải điền vào sim
2. Với mỗi hiện tượng, làm đủ ba đường như Bài 16.
3. Lập bảng hiệu lực:

| Hiện tượng | Miền đã kiểm | Gap đo được | Miền **chưa** kiểm |
|---|---|---|---|
| Con lắc | L 0.3–1.0 m, biên độ ≤45° | <1% sau fit | Biên độ >45°, có gió |
| Rơi tự do | h 0.5–1.5 m | ... | Vật nhẹ, sức cản lớn |
| Ma sát tĩnh | 3 loại bề mặt | ... | Bề mặt ướt, bụi |

4. Cột cuối cùng quan trọng nhất. **Nói rõ cái bạn chưa kiểm là hành vi kỹ thuật trưởng thành**, không phải thú nhận yếu kém.
5. Nối ngược vào Module 4: với mỗi kịch bản đánh giá, kịch bản đó nằm trong hay ngoài miền đã kiểm? Gắn cờ.

### Số phải ra

| Kiểm tra | Kết quả đúng |
|---|---|
| Mỗi hiện tượng có đủ ba đường | Có |
| Bảng hiệu lực có cột "chưa kiểm" | Có, và không rỗng |
| Kịch bản đánh giá được gắn cờ trong/ngoài miền | Có |

Điểm cuối là thứ biến bảng hiệu lực từ tài liệu thành cơ chế: khi harness chạy một kịch bản nằm ngoài miền đã kiểm, báo cáo phải nói ra điều đó.

---

# MODULE 6 — VÒNG KHÉP KÍN VÀ PUBLISH (6h)

---

## Bài 18 — CI: đổi một thứ, nhận một phán quyết (3h)

**Câu hỏi:** vòng lặp bạn mô tả từ đầu — đã đóng chưa?

### Làm

Ghép mọi thứ:

```
đổi policy / config / tham số vật lý
          ↓
CI tự chạy N episode (N tính từ power analysis, Bài 12)
          ↓
so với baseline có version
          ↓
verdict ba trạng thái: PASS / FAIL / INCONCLUSIVE
          ↓
báo cáo tự sinh, có provenance đầy đủ
          ↓
episode thất bại lưu ra MCAP, mở được trong Foxglove
          ↓
kịch bản ngoài miền đã kiểm → gắn cờ
```

Test toàn bộ bằng ba pull request giả: một cải thiện thật, một làm hỏng thật, một không thay đổi gì. Cả ba phải cho verdict đúng.

### Số phải ra

| PR | Verdict đúng |
|---|---|
| Cải thiện thật ≥ ngưỡng phát hiện | PASS + báo cải thiện có ý nghĩa |
| Làm hỏng thật ≥ ngưỡng | FAIL |
| Không thay đổi | PASS, không báo gì có ý nghĩa |
| Thay đổi nhỏ hơn ngưỡng phát hiện | **INCONCLUSIVE**, kèm số episode cần thêm |

---

## Bài 19 — Publish (3h)

**Tiêu đề gợi ý:** *"How many episodes do you need? Statistical power in robot policy evaluation"*

Đây là góc có khả năng lan xa nhất, vì nó không đòi người đọc quan tâm tới simulator của bạn — nó đặt một câu hỏi mà mọi người trong ngành đang trả lời sai.

**Cấu trúc:**

| Phần | Nội dung |
|---|---|
| TL;DR | Bảng n cần thiết ở Bài 12 |
| The problem | Hai run cùng policy lệch 15 điểm ở n=50 — đồ thị từ Bài 12 bước 4 |
| Determinism first | Vì sao không có nó thì không có phép so sánh |
| **Power analysis** | Bảng chính |
| Three-verdict CI | INCONCLUSIVE là verdict hạng nhất |
| **Sim-to-real** | Bảng con lắc ba đường — phần khiến bài không chỉ là bài thống kê |
| Limitations | Bảng hiệu lực, cột "chưa kiểm" |
| Reproduce | Một lệnh |

Đăng: r/robotics, Hacker News, LeRobot Discord, ROS Discourse, LinkedIn.

---

# GATE KHÓA 6

```
[ ] 1. DETERMINISM chứng minh bằng số:
       cùng seed → bit-exact HOẶC tương đương thống kê trong ngưỡng đã nêu trước,
       kiểm ở cả 4 kịch bản (cùng tiến trình / khác tiến trình / tuần tự vs song song / khác máy),
       có canary phá hoại và canary bị bắt

[ ] 2. ≥1.000 episode chạy bằng MỘT lệnh, có artifact management phân tầng,
       mọi kết quả truy ngược được về đủ 6 thứ (kịch bản, commit, môi trường,
       policy, seed, phần cứng)

[ ] 3. Harness từ chối kết luận khi n không đủ, có verdict INCONCLUSIVE,
       và NGƯỠNG PHÁT HIỆN TỐI THIỂU được nêu bằng số trong README

[ ] 4. Canary regression −5 điểm bị bắt khi n đủ,
       và cho INCONCLUSIVE (không phải PASS) khi n không đủ

[ ] 5. BẢNG SIM-TO-REAL: ≥1 hiện tượng vật lý đo đủ ba đường
       (công thức giải tích, thực đo, sim trước và sau khi fit),
       kèm bảng miền hiệu lực có cột "chưa kiểm"

[ ] 6. Bài viết tiếng Anh + repo public, ≥1 người ngoài chạy lại và xác nhận
```

**FAIL → action, cam kết trước:**
- Không đạt bit-exact sau 30h → chuyển sang tiêu chí thống kê tương đương, nêu ngưỡng rõ, đi tiếp. **Không đâm đầu vào determinism GPU.**
- Chạm 160h chưa xong → cắt Module 3 xuống MVP (bỏ object store và DB, giữ summary + MCAP), giữ nguyên Module 1, 4, 5. Publish nguyên trạng.
- Không đủ tài nguyên chạy 1.000 episode → giảm số task, giữ nguyên số episode mỗi task. **Thà đo kỹ 3 task còn hơn đo hời hợt 20 task** — đó là toàn bộ luận điểm của Bài 12.

---

# LỊCH 19 TUẦN

| Tuần | Giờ | Làm |
|---|---|---|
| 1 | 4 | Bài 1 · `DETERMINISM.md`, cam kết loại và ngưỡng |
| 2 | 6 | Bài 2 · dựng MuJoCo + robosuite trong Docker |
| 3–4 | 8 | **Bài 3 · săn nguồn phá determinism** |
| 5 | 6 | Bài 4 · chốt vào CI |
| 6–7 | 8 | Bài 5 · schema kịch bản |
| 8 | 6 | Bài 6 · sinh kịch bản |
| 9 | 6 | Bài 7 · provenance |
| 10 | 8 | Bài 8 · song song hóa |
| 11 | 8 | Bài 9 · artifact management |
| 12 | 8 | Bài 10 · report generator |
| 13 | 6 | Bài 11 · định nghĩa thành công |
| 14–15 | 8 | **Bài 12 · power analysis** ← bài quan trọng nhất |
| 16 | 6 | Bài 13 · regression detection |
| 17 | 6 | Bài 14 · domain randomization |
| 18 | 14 | **Bài 15–16 · con lắc ba đường** |
| 19 | 12 | Bài 17–19 · bảng hiệu lực, CI khép kín, publish |

**Tuần 3–4, 14–15, 18 là ba điểm không được bỏ.** Nếu có tuần crunch MDP, hy sinh tuần 10–12 (module quy mô — bạn làm nhanh được) chứ đừng hy sinh ba điểm này.

---

# NGUỒN HỌC

| Nguồn | Dùng cho |
|---|---|
| **MuJoCo docs** — mục Computation, Modeling, và **Determinism** | Module 1, 5. Đọc kỹ phần solver và contact |
| **MuJoCo Menagerie** | Model robot có sẵn, chất lượng cao |
| **robosuite docs** | Module 2. Cấu trúc task và environment |
| **LIBERO repo** | Đã dùng ở Khóa 4, dùng lại |
| **PyTorch — Reproducibility notes** | Danh sách chính thức các nguồn non-determinism và cách tắt |
| **`statsmodels` — proportion tests, power** | Module 4. Dùng thư viện, đừng tự viết |
| **Wilson score interval** — đọc một bài giải thích ngắn | Bài 12, khi n nhỏ hoặc p gần biên |
| **MuJoCo Playground** (RSS 2025) | Tham khảo cách tổ chức env cho sim-to-real |
| **Isaac Lab paper** (arXiv 2511.04831) | Đọc phần về evaluation ở quy mô và Newton backend |
| **System identification** — tài liệu nhập môn bất kỳ | Bài 16 phần F. Chỉ cần khái niệm |

Quy tắc ba nguồn vẫn giữ. Ở khóa này **docs của MuJoCo là datasheet của bạn** — mọi hành vi bất ngờ đều có lời giải ở đó trước khi có lời giải trên forum.

---

# BA ĐIỀU MANG ĐI

**1. Determinism không phải tính năng, nó là điều kiện tồn tại của phép so sánh.** Một hệ đánh giá không deterministic không đo gì cả — nó chỉ sinh ra những con số trông giống dữ liệu. Đây là lý do module đầu tiên chiếm 24 giờ.

**2. Phần lớn kết quả đánh giá robot công khai không đủ sức mạnh thống kê để chứng minh điều chúng tuyên bố.** Bạn sẽ chứng minh được điều đó bằng số, bằng công cụ của chính mình, ở Bài 12. Đó là một đóng góp thật cho ngành, và nó tốn đúng 8 giờ.

**3. Con lắc rẻ tiền dạy đúng bài học mà digital twin triệu đô dạy.** Công thức là một mô hình có miền hiệu lực. Simulator là một mô hình khác có sai lệch khác. Hiệu chỉnh theo dữ liệu thật là một quy trình đo được. Và cách duy nhất biết mô hình đúng là dự đoán trước rồi kiểm — nguyên tắc bạn đã dùng từ Khóa 1 Bài 1, giờ áp dụng ở tầng cao nhất.

---

# SAU KHÓA 6

Bạn có **bốn artifact ★**: audit tool (K2), VLA edge benchmark (K4), sensor platform có số đo sync (K5), evaluation infrastructure có bảng sim-to-real (K6). Cộng bốn bài viết tiếng Anh và một dataset mang tên bạn.

**Chạy M5 ngay.** Đây là điểm mà hồ sơ của bạn đủ mạnh nhất tính trên mỗi giờ đã bỏ ra, và Khóa 7 là dự án 340 giờ — tức 13 tháng ở nhịp hiện tại. Làm nó **trước** khi đi làm là đánh đổi 13 tháng lấy một thứ mà bốn artifact này đã mở cửa được rồi.

Đường tôi khuyên: **K6 xong → apply → có việc → K7 chạy nền.** Lúc đó bạn có thu nhập robotics trả cho phần cứng, có đồng nghiệp để hỏi, và có ngữ cảnh thật để thiết kế nó. Con robot đó sẽ tốt hơn nhiều so với phiên bản bạn làm trong cô lập.

Nhưng nếu bạn quyết làm K7 trước vì nó là dream product chứ không phải vì nó tối ưu cho việc xin việc — đó là một lý do hợp lệ. Chỉ cần ghi vào `decisions.md` rằng bạn chọn nó **có ý thức**, để sáu tháng nữa bạn không tự hỏi vì sao mình chưa đi làm.
