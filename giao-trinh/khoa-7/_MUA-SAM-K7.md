# Theo dõi mua sắm K7

Nơi tập trung các món đã chọn cho BOM từng chặng K7: link Shopee, phân loại cần chọn, giá lúc xem, việc phải hỏi shop hoặc kiểm khi nhận. BOM gốc (thông số phải chọn, vì sao, cách kiểm) nằm ở mục 2 của từng file chặng; file này chỉ ghi **mua ở đâu** và **đang ở trạng thái nào**.

- Giá là giá hiển thị trên Shopee ngày **2026-10-09**, chưa trừ voucher, chưa tính ship. Giá đổi theo ngày.
- Link dạng `shopee.vn/product/<shop>/<item>`. Khi bấm vào, chọn đúng **phân loại** ghi ở cột "Chọn".
- Bỏ qua mọi link có shop id `1506174776`: đó là listing ảo trong kết quả tìm kiếm, mở ra báo "sản phẩm không tồn tại".

**Trạng thái:** `đề xuất` (đã chọn, chưa mua) · `hỏi shop` (phải nhắn shop trước khi đặt) · `đã đặt` · `đã nhận` · `đạt` (qua phép kiểm khi nhận) · `trả` · `bỏ`.

Cập nhật cột Trạng thái khi mua/nhận. Món trượt phép kiểm thì ghi lý do vào cột Ghi chú.

**Đọc mục 0 trước.** Mục 0 là danh sách chốt cho **đường lõi tối thiểu** (`00-tong-quan.md` mục 6), đã trừ đồ bạn có thật. Các bảng C0–C12 phía dưới là danh mục đầy đủ theo chặng, giữ để tra link và ghi chú kiểm hàng.

---

## 0. Danh sách final — đường lõi tối thiểu, đã trừ đồ đã có (chốt 2026-10-09)

Đường lõi tối thiểu: C0–C7 trọn, C8 tối thiểu (Nav2 A→B chỉ bằng odometry), C10.1–C10.2, C11.1–C11.3. Robot làm ra: chạy pin, teleop có deadman, odometry đã hiệu chuẩn, tự đi A→B quãng ngắn, E-stop cứng, MCAP, sim có kiểm tương quan.

Giá: Shopee 2026-10-09, chưa voucher, chưa ship `[tự đo — giá đổi theo ngày]`. Phiên kiểm lại bằng Chrome dừng giữa chừng vì Shopee bật captcha chống bot; dòng nào ghi **(kiểm 10/09)** là đã mở lại listing trong phiên đó, các dòng khác dùng link đã chọn ở các bảng bên dưới cùng ngày.

### 0.1 Đồ đã có và nó gánh dòng nào của K7

| Đồ đã có | Gánh dòng K7 | Ghi chú |
|---|---|---|
| Mỏ hàn 926, mũi nhọn, thiếc, bọt biển, nhựa thông | C0 mỏ hàn | Thiếu mũi dẹt cho XT60/dây 14 AWG (mục 0.3). Trạm Yihua 926 dùng mũi họ 900M `[tự đo — xem chữ trên tay hàn]` |
| Đồng hồ vạn năng | C0–C10 (UT33D+ trong bài) | Model chưa rõ. Cần: V DC phân giải 0,01 V, Ω, thông mạch có còi, chế độ diode, thang 10 A **có cầu chì**. Thiếu một trong số đó → mua UT33D+ 280k (`khoa-1/_MUA-SAM-K1.md`) |
| Logic analyzer 24 MHz 8 kênh "ARM FPGA" (Lập Trình Nhúng A-Z [102]) | C3.3, C4.2, C10.1 | Listing không ghi chip (kiểm 10/09). **Kiểm ngay:** Linux `lsusb` ra `0925:3881` hoặc PulseView nhận driver `fx2lafw` → dùng được. Không nhận → mua loại có chip CY7C68013A trước C3 |
| Breadboard ×2, jumper đực–đực 65, đực–cái 10 | Bàn thử | Thiếu cái–cái (C11) |
| Adapter 9 V SM0920 + mạch MB102 5 V/3,3 V | Bài tập kit (phụ lục) | **Không thay được nguồn bàn giới hạn dòng**: không chỉnh áp, không có CC |
| USB tester KWS-X1 | K1 | — |
| ESP32-S3 N16R8 G182 ×1 | C4 con chính | C11.2 cần con thứ hai cùng model (mục 0.3) |
| VL53L1X ×1 | C8 (cần 2–3) | Mua thêm 1 |
| INMP441, PCM5102A, MAX98357A, TPA3110 2×15 W 8–18 V, loa 4 Ω 5 W 52 mm | K3, C12 | Ngoài đường tối thiểu. TPA3110 8–18 V bao trọn pack 4S LFP (10–14,6 V) `[spec — nhãn listing; tự đo dòng nghỉ]` |
| ICM-42688-P ×2 | **Chưa dùng được** | Listing ghi gói LGA-14: nhiều khả năng là chip trần 2,5×3 mm. Shopee không có đế chuyển LGA-14 sang DIP (kiểm 10/09). Không dùng cho K7. Xem mục 0.6 |
| Kit Arduino 36 món | Xem `phu-luc-kit-arduino.md` | RC522 + thẻ, LED đỏ thay dòng C9; LM35, relay 5 V, LED RGB, còi, LCD1602, 28BYJ-48, biến trở dùng cho bài tập phụ |

### 0.2 Sửa so với các bảng bên dưới (lỗi đã thấy khi rà)

1. **Bảng C0–C12 coi một số món là "có từ K1/K5" nhưng bạn chưa mua:** kính bảo hộ, kìm cắt, kit điện trở (kit Arduino chỉ 30 con), cáp USB-C dữ liệu, ESP32-S3 thứ hai, IMU, camera. Đã đưa vào mục 0.3.
2. **BOM gốc có nhưng bảng mua sắm thiếu:** bình chữa cháy ABC (C0, "không thay được"), ống co nhiệt + máy khò (C0), túi chống cháy pin (C1), bo đục lỗ + header (C10 Lắp bước 1). Đã thêm.
3. **MOSFET Q1 (C10):** sơ đồ C10 mục 4 ghi "AO3400 hoặc tương đương" cùng Zener 20 V. Khi Q1 tắt, cực D lên tới V_pack + V_Z + V_diode ≈ 14,6 + 20 + 0,7 ≈ 35 V `[chuẩn]`, vượt V_DS 30 V của AO3400 `[spec — datasheet AOS AO3400]`. Trên Shopee không có MOSFET SOT-23 ≥40 V ghi R_DS(on) ở 2,5 V mà có lượt bán (AO3422 55 V chỉ có listing 0 lượt bán, và V_GS(th) tối đa 2,0 V `[spec — datasheet AOS AO3422]`; IRLML0040 không ghi R_DS(on) ở 2,5 V). **Chốt: AO3400 + Zener 10 V** → đỉnh ≈ 25,3 V, còn ~16% dư so với 30 V. Relay nhả chậm hơn một chút so với Zener 20 V; C10.1 vẫn đo hai cấu hình như bài yêu cầu. Ghi lựa chọn vào `decisions.md`. Đã sửa sơ đồ C10 mục 4.
4. **Mạch chuyển mức (C4):** chỉ cần nếu cấp encoder JGB37 bằng 5 V. Listing ghi encoder chạy 3,3–5 V → cấp 3,3 V thì bỏ được `[tự đo — đo mức cao A/B]`. Vẫn cần nếu làm bài LCD1602 của phụ lục kit.

### 0.3 BẮT BUỘC — mua theo đợt

Mua đúng đợt, không mua trước: motor chờ C2.1, driver chờ C3.1. Mỗi dòng: lựa chọn khuyên dùng · thay thế (rẻ hơn hoặc cùng chức năng).

**Đợt A — trước C0 (xưởng, an toàn; gồm món K1 còn thiếu)** · ~3,07tr

| Món | Khuyên dùng | Giá | Thay thế |
|---|---|---|---|
| Nguồn bàn giới hạn dòng | DF-305DS 32 V/5 A, link C0 | 909k | DF-3010DS 1.144k (cùng link) nếu muốn dư cho dự án sau. 5 A đủ cho K7: C3.1 tự ghi "số đó > 5 A thì không làm". Cắm ổ 3 chấu có tiếp địa |
| Bình chữa cháy bột ABC | 2 kg, https://shopee.vn/product/84293778/25818632626 (4,8★/526) (kiểm 10/09) | 350k | 4 kg 485k https://shopee.vn/product/1023859954/24655005532 (4,9★, 6k+/tháng). Kiểm tem kiểm định, kim ở vùng xanh. **Không có thay thế** |
| Kính bảo hộ | 3M Tour-Guard V, link K1 | 78,5k | — |
| Kìm cắt chân linh kiện | Plato 170, link K1 | 25,5k | — |
| Kit điện trở 1/4 W 1% | Set 600 con 30 giá trị, link K1 | 59,8k | Kiểm có 4,7k, 10k, 20k, 47k, 100k (C3, C10) |
| Ống co nhiệt | Hộp 530 ống nhiều cỡ (Lisgovn) https://shopee.vn/product/78103492/20762312441 (20k+ đã bán) (kiểm 10/09) | 44k | — |
| Dây silicon 14/18/22 AWG đỏ+đen | Link C0 | 178k | — |
| Kìm tuốt dây | TOTAL THT15246, link C0 | 278k | Chưa tra loại rẻ hơn tuốt được dây silicon không rách vỏ |
| Kìm bấm JST + hộp đầu JST-XH | SN-01BM + hộp 230 chi tiết, link C0 | 360k | IWISS SN2549 650k (hàng hãng) |
| Kìm bấm ferrule + 1.200 ferrule | HSC8 6-4A, link C0 | 148,5k | — |
| XT60 ×3 cặp, XT30 ×3 cặp | Amass, link C0 | 192k | — |
| Mũi hàn dẹt | 900M-T-3.2D, link C0 | 31,9k | Chỉ mua khi tay hàn 926 dùng mũi 900M |
| Hộp kim loại + cát khô | Hòm tôn 25 cm https://shopee.vn/product/342892536/5397911679 + cát | 170k + 56k | Thùng 7 L 290k (link C0); cát xây dựng phơi khô (0đ) |
| Kìm cách điện cán dài | Total 200 mm, link C0 | 194k | Kẹp gắp than cán dài (chưa tra giá) |

**Đợt B — C1 (hệ nguồn)** · ~2,26tr

| Món | Khuyên dùng | Giá | Thay thế |
|---|---|---|---|
| Pack 4S LiFePO4 + sạc | "4s1p - 7Ah, Pin kèm sạc 2a", link C1, **hỏi shop BMS trước** | 500k | Không thay bằng LiPo RC trần |
| Cầu chì lưỡi + cầu chì 1 A + đế ×3 | Link C1 | 199k | — |
| Công tắc chính DC | "Ctắc Xoay", link C1 | 169k | — |
| Relay 5 chân + đế | Goldspy, link C1 | 58k | — |
| Nút E-stop tạm, diode 1N5819 | Link C1 | 32,4k | — |
| Buck-boost 12 V ≥5 A | SK120X, link C1 | 550k | Module 80 W 180k (link C1): rủi ro không giữ được 5 A liên tục, phải thử tải ở C1.4 |
| Buck 5 V ×2, INA226, shunt 50 A/75 mV, cầu đấu ×2 | Link C1 | 235k | — |
| Tải giả: P21W ×2 + đui, điện trở nhôm 10 Ω 50 W | Link C1 | 60,5k | — |
| Jack DC 5,5×2,5, dây 16 AWG | Link C1 | 107k | — |
| Tụ low-ESR 1000 µF 35 V ×3 | Rubycon ZLH, link C5 (mua luôn ở đây vì C1.4 đã cần) | 75k | iLinhkien 5 con 26,3k (không ghi low-ESR) |
| Nhiệt kế hồng ngoại | Deli, link C1 | 275k | UNI-T UT306S 330k; LM35 của kit + log (phụ lục kit P2), chậm hơn và phải dán vào điểm đo |

**Đợt C — C2 (cơ khí; motor, bánh chỉ đặt sau C2.1)** · ~2,99tr, ~2,29tr nếu mượn được máy khoan

| Món | Khuyên dùng | Giá | Thay thế |
|---|---|---|---|
| 2× motor JGB37-520 encoder + 2× gá | Link C2 | 683k | ĐứcHuy 285k/cái (link C2) |
| Bánh 85 mm ×2 + khớp nối ×2 | Link C2, **hỏi giá cặp hay chiếc** | 162k (tới 324k nếu giá chiếc) | — |
| Caster ×2 | Link C2 | 35k | — |
| Ván ép 6 mm | Tiệm gỗ/CNC gần nhà | ~100k `[ước lượng]` | — |
| Vít M3/M4 + nyloc + trụ đồng + keo khóa ren | Link C2 | 479k | Hộp vít 260k là khoản lớn nhất; dùng lâu dài nên giữ |
| Dây rút, đế dán, grommet, đai pin | Link C2 | 99k | — |
| 3× cân điện tử | METIS 10 kg, link C2 | 189k | 1 cân + 2 khối kê cùng cao (63k; chậm hơn, kém hơn) |
| Thước kẹp | BESTCHOICE, link C2 | 142k | — |
| Máy khoan pin có ly hợp + mũi khoan | Deli 12 V + Favi, link C2 | 824k | Mượn máy khoan (chỉ mua mũi 125k) |
| Lục giác, tuýp 5,5/7, đột tâm, giũa, kẹp chữ C ×2 | Link C2/C3 | 276k | — |

**Đợt D — C3, C4 (bring-up, firmware)** · ~0,6tr

| Món | Khuyên dùng | Giá | Thay thế |
|---|---|---|---|
| Driver ×2 (chờ C3.1) | DRV8871, link C3 | 111k | BTS7960 ×2 200k nếu dòng hãm > 3,6 A |
| Tụ bulk 470 µF 35 V | Link C3 | 25k | — |
| **ESP32-S3 thứ hai** | Cùng model con đang có: G182 https://shopee.vn/product/107147748/55161247435 (kiểm 10/09) | 210k | G23 220k (link K1): bảng chân phải làm lại |
| Bo đục lỗ 2 mặt | "1 Tấm 9X15CM 2 mặt" + "2 Mặt 7X9CM" https://shopee.vn/product/404478549/19750269236 (4,95★/595) (kiểm 10/09) | 55k | — |
| Header đực + cái 2,54 mm | https://shopee.vn/product/85716713/2325940113 (4,98★/187) (kiểm 10/09) | ~24k | — |
| Đế chuyển SOT-23 → DIP (cho AO3400, AO3401) | "SOT23 SOP10 to DIP 10PCS" https://shopee.vn/product/778834786/16670462528 (4,96★/206) (kiểm 10/09) | 26,3k | Hàn dây trực tiếp lên chân SOT-23 (khó cho người mới) |
| Opto PC817 2 kênh | Link C4 | 25,2k | — |
| Lõi ferrite 5 mm + 7 mm | Link C4/C5 | 57,2k | — |
| Cáp USB-A → C có dây dữ liệu | Ugreen 1 m, link K1 | 65k | Cáp điện thoại sẵn có nếu truyền được file |

Bo ra chân cầu đấu cho ESP32 (115k, link C4) **thay bằng** tự hàn header + JST-XH trên bo đục lỗ: rẻ hơn, và là bài luyện hàn trước C10 Lắp bước 1.

**Đợt E — C5, C6** · ~0,5tr

| Món | Khuyên dùng | Giá | Thay thế |
|---|---|---|---|
| Tay cầm 2,4 GHz | Link C5 | 186,2k | Logitech F710 1.209k (chắc chạy trên Linux hơn) |
| Tụ gốm 100 nF | Link C5 | 22,8k | — |
| Thước dây 10 m, thước lá 1 m | Link C6 | 189k | — |
| Ê-ke 300 mm | Loại rẻ https://shopee.vn/product/107238804/9239547941 | 24k | JCTOP 105k (link C6) |
| Băng keo giấy 2 màu, module laser chấm | Link C6 | 81,7k | Bút dạ trong ống trượt |

**Đợt F — C7** · ~0,62tr

| Món | Khuyên dùng | Giá | Thay thế |
|---|---|---|---|
| IMU | MPU6050 GY-521 (link K5): bài K5/K7 viết sẵn cho nó | 57,1k | LSM6DS3 49,5k https://shopee.vn/product/770245757/29669820437 (5★/28) (kiểm 10/09): có FIFO và lọc số cấu hình được, nhưng bài chưa viết cho nó, ghi `decisions.md`. MPU6500 58k (link K5) |
| Camera USB | Logitech C270 (link K5) | 461,2k | VOVOVA 94,1k (link K5): **chỉ giữ** nếu `v4l2-ctl` ra MJPEG 720p30 và không có autofocus |
| Đế giảm rung (băng xốp + đệm cao su) | Link C7 | 90,3k | Ruột xe đạp cắt miếng (một trong ba kiểu thử) |
| Dây I2C nhiều màu | Cáp bẹ, link C7 | 10k | — |

Có học K5 song song thì camera và IMU mua theo `khoa-5/_MUA-SAM-K5.md` (2 camera khác model, 2 IMU), **không mua lại ở đây**.

**Đợt G — C8 tối thiểu** · 106,5k: VL53L1X thêm 1 con (link C8), đủ 2 con. Con thứ ba: mục 0.4.

**Đợt H — C10.1, C10.2** · ~0,39tr

| Món | Khuyên dùng | Giá | Thay thế |
|---|---|---|---|
| Nút E-stop mở cưỡng bức + nền vàng | Schneider XA2ES542, link C10 | 125k | IDEC YW1B 112k |
| Q1 + Zener + 1N4007 | AO3400 (link C10) + Zener phân loại **"10V"** (https://shopee.vn/product/71427966/7246108342, kiểm 10/09) + 1N4007 | 37,7k | Xem mục 0.2 điểm 3 |
| Mạch xung giữ, TVS SMBJ18A, tiền nạp | Link C10 | 102,8k | — |
| Bumper: KW11 ×5 + tấm EVA | Link C10 | 50,3k | — |
| Nút RESET | IDEC YW1B xanh, link C10 | 76k | Nút 12 mm của kit trong hộp có nắp (chỉ trên bàn thử) |

**Đợt I — C11.1–C11.3** · ~0,21tr

| Món | Khuyên dùng | Giá | Thay thế |
|---|---|---|---|
| Adapter USB–UART | CP2102, link C11 | 75k | USB native của ESP32 #2 |
| Dupont cái–cái | Link C11 | 23,1k | — |
| Dây con lắc hai dây | Dây PE bện, link C11 | 116,6k | Dây dù 29,5k: giãn hơn, đo chiều dài lúc đã treo vật |

**Ngoài Shopee, bắt buộc từ C5:** mini PC N100 (`khoa-2/_MUA-SAM-K2.md`, ~3–4tr `[ước lượng]`).

**Tổng bắt buộc: ~10,8tr** (chưa ship, chưa mini PC) `[ước lượng — cộng các dòng trên]`. Bản tiết kiệm mà vẫn an toàn (mượn máy khoan, 1 cân, dây dù, LM35 thay nhiệt kế IR, nút RESET của kit): ~9,5tr. Thêm buck 80 W và camera VOVOVA thì ~8,8tr, nhưng hai món đó có rủi ro phải mua lại.

### 0.4 NÊN CÓ — tiện và an toàn hơn, dùng lâu dài

| Món | Link | Giá | Vì sao |
|---|---|---|---|
| Máy khò mini 220 V | https://shopee.vn/product/78103492/3804596554 (10k+ đã bán) (kiểm 10/09) | 98k | Co nhiệt đều. Bật lửa là phương án thay, cấm gần pin và IPA. Loại này thường không chỉnh nhiệt `[tự đo]` |
| Túi chống cháy pin | https://shopee.vn/product/27693865/27638110904 (4,8★) (kiểm 10/09) | 83k | Chỗ sạc riêng, hộp thép giữ cho pin hỏng. Đo pack trước khi chọn cỡ |
| Kẹp ba tay | Link C0 | 146k | Hàn dây 14 AWG vào XT60 cần hai tay rảnh |
| Bùi nhùi đồng, flux gel, dây hút thiếc, IPA | Link K1 | ~180k | Mũi sạch hơn bọt biển; sửa mối hàn hỏng |
| Quạt hút khói hàn | Link K1, hỏi lọc than | 226,8k | Khói flux gây mẫn cảm hô hấp |
| Dây bắp chuối–cá sấu 15 A | Link C0 | 95k | Dây kèm nguồn rẻ nóng ở 5 A |
| Cân hành lý | Link C0 | 99k | Kéo thử mối nối, lực kích bumper |
| Dây cá sấu, móc kẹp test | Link K1 | ~80k | Kẹp logic analyzer vào bo C10 |
| VL53L1X thứ ba | Link C8 | 106,5k | BOM C8 cho phép 2–3 con |
| Mạch chuyển mức BSS138 | Link C4 | 33k | Bắt buộc nếu encoder chạy 5 V hoặc làm bài LCD của phụ lục kit |
| Trụ nylon M3, mũi vát | Link C2 | 132k | — |
| Cáp USB 0,5 m Ugreen | Link C4 | 125k | Cáp ngắn trên robot (C5.1) |

### 0.5 Thay bằng đồ sẵn có hoặc tự làm

| Dòng trong bảng | Thay bằng |
|---|---|
| Bo ra chân cầu đấu ESP32 115k (C4) | Bo đục lỗ + header + JST-XH tự hàn |
| Cân hành lý (C0) | Can nước treo bằng dây: 1 L ≈ 9,8 N |
| Bút sơn đánh dấu ốc 63k (C2) | Sơn móng tay |
| Tấm xốp 65k (C6) | Gối |
| Khung chữ L (C6), vì nhôm 2020 là đồ C9 | Hai thanh gỗ vuông góc, kiểm bằng tam giác 3-4-5 |
| Giá camera 145k (C7) | Ke nhôm chữ L + **hai** vít |
| RC522 + thẻ, LED đỏ (C9) | Kit Arduino |
| Máy phát xung cho checkpoint C10 Lắp bước 1 | ESP32 #2 (đợt D) |

### 0.6 BỎ QUA trong đường tối thiểu (mua khi làm phần đó)

- **C8 trọn:** formex, keo Super 77, in tag, chân máy, thước thủy, máy đo laser, lidar (~1,2tr; lidar thêm 0,39–2,6tr).
- **C9:** camera OV9726, cáp USB có công tắc, nhôm 2020 + ke + ngàm, nút Qanba (~0,73tr).
- **C10.3:** biển báo, cảm biến vực.
- **C12:** amp và loa đã có; cầu chì FE, cáp audio (~0,08tr).
- **Không bao giờ mua trước khi đo chứng minh cần:** Coral, Hailo.
- **ICM-42688-P đã mua:** để sau K7. Muốn dùng thì đặt bo breakout tự vẽ (JLCPCB/PCBWay) rồi hàn reflow bằng kem hàn + bếp gia nhiệt hoặc khò. Đây là bài hàn SMD nâng cao, không thuộc đường tối thiểu.

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| Nguồn bàn giới hạn dòng | DF-3010DS 32 V/10 A (shop Đông Phương) | https://shopee.vn/product/1343835804/43605396400 | 1.144k | đề xuất | 4,96★/113. Màn 4 số, nút OUTPUT ON/OFF, nhớ V/A, khóa phím. Có báo cáo rò điện ra vỏ khi không nối đất → cắm ổ 3 chấu có tiếp địa. Bản rẻ: DF-305DS 32 V/5 A, 909k, cùng link |
| Dây bắp chuối–cá sấu | "Đỏ + Đen", 1 cặp, 1 m, kẹp mở 15 mm, 15 A (Fixpro) | https://shopee.vn/product/71427966/18469024289 | 95k | đề xuất | Shop không ghi AWG. Kiểm: nguồn bàn 5 A, sụt áp một sợi ≤ ~0,15 V; ≥0,3 V hoặc ấm rõ → trả |
| Dây silicon 14 AWG đỏ/đen | "Đỏ,14AWG (1mét)" ×2, "Đen,14AWG (1mét)" ×2 (shop Hưng) | https://shopee.vn/product/65877537/27985190123 | 4×22k | đề xuất | 4,91★/2.485. Đánh giá xấu chủ yếu là giao thiếu mét, cắt rời → ghi chú "giao nguyên cuộn"; đo chiều dài, đọc chữ AWG trên vỏ |
| Dây silicon 18 AWG đỏ/đen | "Đỏ,18AWG" ×2, "Đen,18AWG" ×2 (shop Hưng) | https://shopee.vn/product/65877537/27985190123 | 4×11,5k | đề xuất | như trên |
| Dây silicon 22 AWG đỏ/đen | "22awg 2met, Đỏ" ×1, "22awg 2met, Đen" ×1 (Pin247) | https://shopee.vn/product/1427783833/40568832989 | 2×22k | đề xuất | 4,90★/576. Có đánh giá giao nhầm cỡ → đọc chữ AWG trên vỏ |
| Kìm tuốt dây | TOTAL THT15246, "TOTAL: KÌM 3 IN 1" (Bảo Hộ Hùng Hạnh) | https://shopee.vn/product/282449885/22686484430 | 278k | đề xuất | 4,96★/1.115. Tuốt 10–24 AWG. Thử trên dây silicon phế liệu trước (vỏ mềm có thể rách) |
| Kìm bấm JST/Dupont | YTH SN-01BM, "sn-01bm" (Kamy Tools) | https://shopee.vn/product/29908710/22809700814 | 288,6k | đề xuất | AWG 28–20, có trợ lực. Mô tả không ghi "cóc": bóp thử, không nhả giữa chừng mới là có cóc. Thay thế hãng: IWISS SN2549 650k https://shopee.vn/product/19330305/9666703735 |
| Đầu JST-XH + vỏ 2–5P | Hộp 230 chi tiết (Aogry phần cứng) | https://shopee.vn/product/284379266/17494288220 | 71k | đề xuất | 2P/3P/4P/5P × 10 bộ + 150 lõi. Hàng tương thích, không phải JST chính hãng. **Không có 6P** |
| JST-XH 6P (nếu cần) | Vỏ "6P (50 cái)" + giắc thẳng "6P (50 cái)" (Tranzi) | https://shopee.vn/product/183902009/3558855594 · https://shopee.vn/product/183902009/6058783026 | 32,5k + 45k | đề xuất | Mua khi chốt encoder cần 6 chân |
| Kìm bấm ferrule + 1.200 ferrule | HSC8 6-4A, "Bộ kìm + cos 1200spc" (giadungtongkho6366) | https://shopee.vn/product/909235728/43625509045 | 148,5k | đề xuất | 4,91★/1.577. Một đánh giá chê ferrule trầy bẩn. 14 AWG → ferrule 2,5 mm²; 18 AWG → 0,75/1,0; 22 AWG: hộp không có 0,34 mm² (E0308), dùng tạm 0,5 và kéo thử. Dự phòng: https://shopee.vn/product/19330305/21674464030 (205k) |
| XT60 Amass có nắp | "1 cặp" × 3 (Thái Tuấn hobby-fpv) | https://shopee.vn/product/188773686/4612625406 | 3×32k | đề xuất | 4,92★/166, không có đánh giá xấu có chữ. Kiểm: chạm mỏ 2 s nhựa không mềm |
| XT30 Amass | "1 cặp đực + cái" × 3 (Thái Tuấn hobby-fpv) | https://shopee.vn/product/188773686/7309075490 | 3×32k | đề xuất | 4,97★/115 |
| Kẹp ba tay | Trạm 4 tay (Brisunto.vn) | https://shopee.vn/product/1434793543/41564958729 | 146k | đề xuất | 4,87★/87. Khối lượng đế không ghi; đánh giá 1★: khớp nhựa cứng; có người bị rơi đầu kẹp. Kiểm: kẹp 14 AWG không trượt, đế không lật |
| Mũi hàn dẹt cho 936 | 900M-T-3.2D | https://shopee.vn/product/61435118/28289353856 | 31,9k | đề xuất | Shop chưa có lượt bán; chưa tìm được nguồn dự phòng. Cốc XT60 cần ~380–400 °C với mũi 900M |
| Cân hành lý | 50 kg, "Thế hệ mới" (GUHOME) | https://shopee.vn/product/51362935/1568818284 | 99k | đề xuất | 4,76★/378, chia 10 g, có TARE. Không thấy chức năng giữ đỉnh → quay video màn hình khi kéo thử. Hãng: Deli 139k https://shopee.vn/product/1048223751/47955942709 |
| Hộp thép cách ly pin | Hộp sắt 7 L 30×15×19 cm, "Thùng 7L" (TRUNG KIÊN AUTO) | https://shopee.vn/product/68423141/7791186835 | 290k | đề xuất | 4,92★/1.091. **Có đệm cao su kín nước → gỡ đệm hoặc chỉ đặt nắp hờ, không cài khóa.** Rẻ hơn: hòm tôn 25 cm 170k https://shopee.vn/product/342892536/5397911679 |
| Cát khô | Cát vàng kim sa "1kg" × 3 (DebutAqua) | https://shopee.vn/product/87863906/19766309831 | 3×18,6k | đề xuất | Phơi/rang khô trước khi đổ vào hộp. Rẻ hơn: cát xây dựng phơi khô |
| Kìm cách điện cán dài | Total 8"/200 mm, "THTIP2381: mỏ dài" (BẢO HỘ THINKSAFE) | https://shopee.vn/product/7239997/25267970839 | 194k | đề xuất | Tay cầm 1000 V. Muốn bớt tiền: kẹp gắp than (chưa tra) |

**Tạm tính C0 (chưa ship):** ~3,2tr (thêm 77,5k nếu lấy JST 6P), trong đó nguồn bàn 1.144k.

---

## C1 — Hệ nguồn

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| Pack LiFePO4 4S 12,8 V | "4s1p - 7Ah, Pin kèm sạc 2a" (Energy.Lithium) | https://shopee.vn/product/1155027895/50862637380 | 500k (385k không sạc) | **hỏi shop** | ~90 Wh, cell 32700, "BMS 40A". Hỏi: 40 A liên tục hay đỉnh, ngưỡng cắt quá dòng, cỡ dây ra. Loại: SECKAM 10 Ah (shop ghi xả liên tục 10 A) |
| Cầu chì lưỡi 2–40 A | "Hộp 100 cái 3 loại" (DaTaAuTo21) | https://shopee.vn/product/593628278/13181412390 | 88k | **hỏi shop** | Không có 1 A. Hỏi cỡ: phải là Standard/ATO (~19 mm) để vừa đế |
| Cầu chì 1 A | "1A 32V(10 con)" (iLinhkien) | https://shopee.vn/product/67030960/22473418926 | 45k | **hỏi shop** | "chân nhỏ" — hỏi có phải ATO không |
| Đế cầu chì inline có nắp | "DÂY THẲNG (LOẠI 2ly)" × 3 (MinhKhang_AutoParts) | https://shopee.vn/product/43431206/45900619810 | 3×22k | **hỏi shop** | Dây 2 mm² ≈ 14 AWG. Hỏi cỡ cầu chì vừa đế |
| Công tắc chính | "Ctắc Xoay" (X3_Liqueur) | https://shopee.vn/product/87220060/26972903664 | 169k | đề xuất | Công tắc ngắt ắc quy ô tô 12/24 V, ghi 250 A. Cực bulông → cần đầu cos tròn cho 14 AWG |
| Relay ô tô 12 V 40 A 5 chân + đế | "5 CHÂN" (Goldspy) | https://shopee.vn/product/116745109/6332133507 | 58k | đề xuất | 4,89★/212. Dòng cuộn không ghi → đo ở phép kiểm |
| Nút E-stop nấm | LA38-STOP phi 22, 1NO+1NC (Điện Công Nghiệp MCE) | https://shopee.vn/product/1233132826/27428871438 | 17k | đề xuất | 4,96★/850. Kiểm: chưa bấm → NC thông; bấm → hở; xoay → thông lại |
| Diode | 1N5819 túi 10 | https://shopee.vn/product/404478549/22604046645 | 15,4k | đề xuất | Schottky 1 A/40 V |
| Buck-boost 12 V mini PC | SK120X, "Sk120x" (A-LIFETIME) | https://shopee.vn/product/1041315709/28360284685 | 550k | đề xuất | 4,92★/125. Vào 6–36 V, 6 A/120 W, có CC + màn hình. Kiểm: đầu ra tự bật khi cấp điện. Rẻ: module 80 W "5 A" 180k https://shopee.vn/product/891300093/16489471486 (3 đánh giá, thường ~4 A liên tục, phải thử tải ở C1.4) |
| Buck 5 V logic | Mini560 "5V PRO" × 2 (itcuaban) | https://shopee.vn/product/92737532/28628007297 | 2×29k | đề xuất | Đồng bộ, 5 A. **Vào tối đa 20 V** → lấy từ nhánh sau cầu chì, tách khỏi nhánh motor |
| INA226 | CJMCU-226 | https://shopee.vn/product/578443443/20058025715 | 42,9k | đề xuất | Shunt trên module chỉ đo ~0,8 A → dùng shunt rời |
| Shunt rời | FL-2 50 A/75 mV | https://shopee.vn/product/119714962/19581152284 | 62k | đề xuất | 75 mV < 81,92 mV của INA226 |
| Cầu đấu | Hanyoung HYT "20A 6 cực" × 2 (+ và GND) | https://shopee.vn/product/1353620562/28813522404 | 2×36k | đề xuất | **Không có nắp** → tự che bằng mica/hộp |
| Bóng P21W | OSRAM 1 tóc chân thẳng × 2 | https://shopee.vn/product/946109632/29266951539 | 2×9,5k | đề xuất | Đo R nguội, ghi lại |
| Đui bóng 1156 | phân loại 1156 một tóc | https://shopee.vn/product/151227902/24908316719 | 19,5k | đề xuất | |
| Điện trở nhôm 10 Ω 50 W | 50W-10R | https://shopee.vn/product/914563933/19579499564 | 22k | đề xuất | Bắt lên tản nhiệt (~16 W ở 12,8 V) |
| Nhiệt kế hồng ngoại | UNI-T UT306S | https://shopee.vn/product/595978369/22756438740 | 330k | đề xuất | Rẻ hơn: Deli 275k https://shopee.vn/product/521320189/26201224299 |
| Jack DC đực 5,5×2,5 | "Đực 5.5x2.5mm(5 cái)" bắt vít (iLinhkien) | https://shopee.vn/product/1046767853/14599400841 | 36,75k | đề xuất | Không có bản sẵn dây 18 AWG → tự nối dây silicon 18 AWG. Đo cực tính trước khi cắm |
| Dây 16 AWG đỏ/đen | "Đỏ,16AWG" ×2, "Đen,16AWG" ×2 (shop Hưng) | https://shopee.vn/product/65877537/27985190123 | 4×17,5k | đề xuất | |
| Dây 18 AWG cam, 22 AWG tím | — | — | — | **chưa tìm được** | Các shop có màu đều hết hàng. Tạm: dây đen + co nhiệt màu đánh dấu đầu, ghi quy ước vào sổ build (C0.5) |

**Tạm tính C1 (chưa ship):** ~2,2tr với SK120X; ~1,83tr với module 80 W.

---

## C2 — Cơ khí

Motor và bánh: **chỉ đặt sau khi chạy xong Bài C2.1** với số của listing thật (rpm, mô-men hãm, dòng hãm). Link dưới đây là listing để lấy số cho `cands`, chưa phải quyết định tỉ số.

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| 2× motor JGB37-520 12 V encoder | Phân loại theo C2.1: "Encoder JGB37 170RPM" (~1:56) hoặc "330RPM" (~1:30) (dientunhattung.com) | https://shopee.vn/product/1045034041/25385250216 | 2×307k | **chờ C2.1** | 5★/18. Trục 6 mm chữ D, encoder A/B 3,3–5 V, I0 100 mA. Listing **không ghi mô-men hãm, dòng hãm** → hỏi shop hoặc tự đo ở C3.1. Thay thế: ĐứcHuy 285k (176/333 RPM, I0 0,12 A) https://shopee.vn/product/1292561517/41076331755 |
| 2× gá motor JGB37 | "Gá đỡ Động cơ JGB37" (dientunhattung.com) | https://shopee.vn/product/1045034041/29459066674 | 2×34,5k | đề xuất | 4,98★/41. Nhôm 3 mm, kèm ốc. Mua cùng shop motor để khớp lỗ |
| 2× bánh 85 mm | "Bánh xe 85mm" (Điện Tử Nguyễn Hiền) | https://shopee.vn/product/104103144/4462381726 | 129k | **hỏi shop** | 4,98★/47. Khớp lục giác 12 mm. Mô tả không nói giá cho 1 bánh hay 1 cặp → hỏi |
| 2× khớp nối lục giác 6 mm | "Khớp nối trục 6mm" (cùng listing) | https://shopee.vn/product/104103144/4462381726 | 33k | **hỏi shop** | Hỏi đơn vị (1 cái/cặp); kiểm vít trí tì vào mặt phẳng chữ D |
| Caster | Bánh xe đẩy PVC 5 cm "5cm Càng Quay" (Cơ Khí Nemo) | https://shopee.vn/product/1342793933/28763016908 | 17,5k/cái | đề xuất | 4,91★/1.516, có bạc đạn. PVC cứng → ồn trên sàn gạch. Mua 2 nếu theo bố trí A (C2.2) |
| Tấm khung 2 tầng | Ván ép 6 mm | — | — | **chưa tìm** | Mua/cắt ở cửa hàng gỗ hoặc xưởng CNC gần nhà rẻ và đúng kích thước hơn đặt online. Shopee chỉ có MDF 5,5 mm khổ nhỏ (18,2k https://shopee.vn/product/900741451/22006359293), MDF kém chịu ẩm và giữ ren kém hơn ván ép |
| Vít, đai ốc, long đen M2/M3/M4 | Hộp 1.080 chi tiết vít lục giác chìm đầu trụ (skycitys0.vn) | https://shopee.vn/product/1723848595/49907320844 | 260k | đề xuất | 4,79★/1.792. M3 4–30 mm, M4 6–30 mm, có đai ốc + long đen. Tiêu đề ghi vừa "inox 304" vừa "cấp bền 12.9" (mâu thuẫn: 304 không đạt 12.9) → coi là inox 304, đừng tin con số 12.9. **Không có đai ốc nylon** → mua dòng dưới |
| Đai ốc khóa nylon M3, M4 | Inox 304, 10 con/gói, mỗi cỡ 2–3 gói | https://shopee.vn/product/822472456/22553825275 | ~10,5k/gói | đề xuất | Chọn phân loại M3 và M4 |
| Trụ đồng M3 | Combo hộp 6/10/15/20 mm, đực–cái + cái–cái (Lập Trình Nhúng A-Z) | https://shopee.vn/product/107147748/14594524208 | 150k | đề xuất | 5★/13. Chỉ tới 20 mm → mua lẻ 30/40 mm ở https://shopee.vn/product/404478549/21373929730 (5k+ lượt bán). Trụ nylon M3 đực–cái cách điện 6–50 mm: 22k https://shopee.vn/product/1046874499/22878203339 (4,89★/72) |
| Keo khóa ren cường độ trung bình | "Keo khoá ren 243" (hàng phổ thông) | https://shopee.vn/product/458354804/40200755755 | 26,9k | đề xuất | Không phải Henkel/Loctite. Hàng ghi "Loctite 243" giá ~450k https://shopee.vn/product/1267529118/27060234045 — chưa kiểm được hàng thật. Cẩn thận nhãn nhái "LOCTTLF/LOCTTLTE" |
| Đế dán dây rút + dây rút | 20 đế dán keo 3M + gói 100 dây rút | https://shopee.vn/product/1017705409/23381470602 · https://shopee.vn/product/316861304/4491319997 | 11,2k + 19k | đề xuất | Đế dán không giữ được lâu khi rung → chỗ chịu lực dùng đế bắt vít M3. Grommet luồn dây: combo 5 đệm cao su luồn dây tủ điện 12–40 mm, 17k https://shopee.vn/product/49292482/4935870333 (4,90★/234), chọn cỡ theo lỗ khoan |
| Đai giữ pin | Gemfan chống trượt 2×25 cm (Thái Tuấn hobby-fpv) | https://shopee.vn/product/188773686/17096769642 | 52k | đề xuất | Đo chu vi pack 7 Ah trước; 25 cm có thể ngắn → hỏi shop có bản dài hơn |
| 3× cân điện tử | METIS "SF400_1g-10kg_Ko_BH" ×3 (Beary Việt Nam) | https://shopee.vn/product/541665853/24522403881 | 3×63k | đề xuất | 4,84★/7.651. 10 kg/1 g. Kiểm: cân cùng một vật trên cả ba, lệch ≤ vài g |
| Thước kẹp điện tử 150 mm | BESTCHOICE inox | https://shopee.vn/product/22668243/5132715569 | 142k | đề xuất | 716 lượt bán/tháng. Kiểm: đóng ngàm về 0. Hãng: INSIZE 805k https://shopee.vn/product/184684406/27423969950 |
| Máy khoan/vặn vít pin | Deli 12 V, "Hộp Giấy+1 Mũi Khoan" (Deli Tools HCM Store) | https://shopee.vn/product/1021391020/28461711897 | 699k | **hỏi shop** | 4,89★/856. 30 N·m, 2 cấp tốc độ, đảo chiều. Mô tả **không nhắc vòng chỉnh lực (ly hợp)** → hỏi shop có nấc mô-men không |
| Mũi khoan HSS 3,2 / 4,5 mm | Favi "3.2 Ly (10 cái)" + "4.5 Ly (10 cái)" (TH.26TPP) | https://shopee.vn/product/449440052/19185448888 | 52k + 73k | đề xuất | 4,87★/322. Có thêm 3,5 mm (55k) nếu cần. Mũi vát mép 3 me 90° phủ TiN: 110k https://shopee.vn/product/43004625/18355518461 (4,95★/109) |
| Lục giác hệ mét | TOTAL THT106191, 9 chìa 1,5–10 mm | https://shopee.vn/product/1212715740/28408630820 | 96,5k | đề xuất | 5★, 2k+ lượt bán/tháng |
| Tuýp 5,5 mm | Kingtony 233555M đầu 1/4" (309627441) | https://shopee.vn/product/309627441/20990264611 | 40k | đề xuất | 4,93★/45. Cần cần siết/tay vặn 1/4" hoặc đầu chuyển lục giác cho máy khoan (chưa tra) |
| Tuýp 7 mm | Đầu tuýp 1/4" ngắn, phân loại 7 mm | https://shopee.vn/product/100111563/42453683414 | 17,2k | đề xuất | 4,91★/554 |
| Đột tâm | Đột tâm tự động lò xo | https://shopee.vn/product/1332358515/25584753278 | 25,6k | đề xuất | 4,90★/1.721 |
| Giũa | Bộ 5 giũa kim loại 8 inch | https://shopee.vn/product/1796165453/44331335626 | 34k | đề xuất | 4,94★/518 |
| Kẹp chữ C ×2 | Xem C3 (Kapusi 2 inch) | — | — | | |
| Bút sơn đánh dấu ốc | Combo 5 bút chấm ốc sơn dầu (Cơ Khí Hà Nội) | https://shopee.vn/product/1627278108/40723610783 | 63k | đề xuất | 4,92★/92. Vạch sơn ngang đầu vít để thấy vít tự nới |

**Tạm tính C2 (chưa ship, chưa có ván ép):** ~3,0tr, nếu bánh 129k là giá một cặp (kẹp chữ C tính ở C3).

---

## C3 — Bring-up trên bàn

Driver: **chưa đặt trước khi có số dòng hãm của Bài C3.1** (C3.1 bước 1–4 chỉ cần motor + nguồn bàn). Hai lựa chọn của BOM gốc (Pololu DRV8874, Cytron MDD10A) **không có trên Shopee**; hai dòng dưới là hàng thay thế gần nhất, chọn một.

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| Driver — thay lựa chọn A (DRV8874) | 2× module DRV8871 3,6 A (vngoodstore.vn) | https://shopee.vn/product/1456687807/26374043552 | 2×55,6k | **chờ C3.1** | 5★/30, 391 lượt bán. 6,5–45 V, 3,6 A đỉnh, giới hạn dòng đặt bằng điện trở ILIM `[spec — datasheet TI DRV8871, kiểm]`. **Không có chân current sense ra ngoài** → đo dòng bằng INA226 của C1. Chỉ hợp nếu dòng hãm C3.1 ≲ 3,6 A, hoặc chấp nhận giới hạn dòng cắt bớt mô-men khởi động. Hàng tương tự ở shop Lập Trình Nhúng A-Z 85k https://shopee.vn/product/107147748/51261042215 |
| Driver — thay lựa chọn B (MDD10A) | 2× module BTS7960 43 A, phân loại "1 cầu test ok" (Xe dò line) | https://shopee.vn/product/97386457/25172523765 | 2×100k | **chờ C3.1** | 4,94★/93, 902 lượt bán. Mỗi module là **một** cầu H → cần 2. 5,5–27 V, có chân IS (current sense) `[spec — Infineon BTS7960, kiểm]`. Mạch đệm 74HC244 trên board nuôi 5 V có ngưỡng mức cao ~3,5 V `[chuẩn — 74HC: V_IH ≈ 0,7·VCC]` → 3,3 V của ESP32 nằm dưới spec; nuôi chân VCC logic của module bằng 3,3 V rồi kiểm cạnh bằng logic analyzer `[tự đo]`. Cytron MDD3A (4–16 V, 417k) có bán nhưng **loại**: 16 V sát pack đầy 14,6 V |
| Tụ bulk VM 470 µF 35 V | "Tụ hóa 35V 470uF 10x17mm" combo 5 con (iLinhkien.Store) | https://shopee.vn/product/67030960/20090438711 | 25k | đề xuất | 4,96★/27. Đọc cực tính, 35 V trên vỏ |
| Cầu chì 3–5 A + đế | Hộp cầu chì + đế inline đã chọn ở C1 | — | 0 | có từ C1 | Nếu hộp C1 không có 3/5 A: combo 10 cầu chì chân nhỏ 5–30 A https://shopee.vn/product/259738960/21716333730 (16,7k). "Chân nhỏ" là cỡ mini: **kiểm vừa đế C1** trước khi mua |
| Đầu nối motor | XT30 của C0 (3 cặp) | — | 0 | có từ C0 | Thiếu thì mua thêm cùng link C0 |
| Dây encoder + chia áp 10k/20k | JST-XH của C0; điện trở trong kit K1 | — | 0 | có từ C0/K1 | Xem `khoa-1/_MUA-SAM-K1.md` |
| 2× kẹp chữ C | Kapusi K-6262B, phân loại "2inch" (Hack Nghề Mộc) | https://shopee.vn/product/1769243163/40729834621 | 2×31,4k | đề xuất | 4,95★/62. Đây cũng là món "kẹp chữ C ×2" còn thiếu ở C2. Cỡ 4 inch: 74k cùng link |

**Tạm tính C3 (chưa ship):** ~0,2tr với DRV8871; ~0,29tr với BTS7960.

---

## C4 — Firmware ESP32

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| ESP32-S3 DevKit thứ hai | **Chưa có** (K1 mới mua 1 con G182) → mục 0.3 đợt D | — | 210k | đề xuất | Xem `khoa-1/_MUA-SAM-K1.md`. Bản N16R8 dùng PSRAM octal → GPIO35–37 không dùng được `[spec — datasheet ESP32-S3, kiểm]`; ghi vào bảng chân |
| Bo ra chân cầu đấu | "Đế ra chân esp32 s3 n16r8 loại domino 3.81mm" (linhkien1993.com) | https://shopee.vn/product/1404458001/26033453771 | 115k | **hỏi shop** | 5★/2, 17 lượt bán. FR4 70×90 mm. Hỏi: đế khớp board 44 chân nào (khoảng cách hai hàng chân); phải khớp đúng DevKit đã mua ở K1. Rẻ hơn nhưng là header, không phải cầu đấu: đế 44 chân Lập Trình Nhúng A-Z 65k https://shopee.vn/product/107147748/29516361995 |
| Điện trở 10 kΩ, 1 kΩ, 100 Ω | Kit điện trở K1 | — | 0 | có từ K1 | |
| Opto cho E-stop sense | Module PC817, phân loại "PC817 - 2 Kênh" (Linh Kiện NtShop) | https://shopee.vn/product/1394580583/27076929359 | 25,2k | đề xuất | 4,96★/79. Shop ghi đầu vào 3,6–24 V → hợp đường 12–16 V. Đo điện trở hạn dòng trên board bằng UT33D+. Dùng lại ở C10.1 |
| Mạch chuyển mức (chỉ nếu encoder chạy 5 V) | "Mạch chuyển mức tín hiệu 4 kênh 2 chiều 3.3V <–> 5V" combo 5 cái | https://shopee.vn/product/227331197/3956805320 | 33k | đề xuất | 5★/3. Loại MOSFET kiểu BSS138 (đọc mã trên board). Tránh TXS0108E khi chưa đo tần số encoder |
| Dây USB ngắn 0,5 m | Ugreen USB-A → USB-C, phân loại "3.0-20881-0.5 mét" (vitinh123.) | https://shopee.vn/product/81256369/40167900821 | 125k | đề xuất | 4,91★/183. Dây USB 3.0, chạy được với thiết bị USB 2.0. Không có lõi ferrite → thêm dòng dưới. Mini PC dùng cổng USB-A |
| Lõi ferrite kẹp cho cáp USB | Ugreen, phân loại "5mm" (Topick Global) | https://shopee.vn/product/196261835/16198523857 | 20,9k | đề xuất | 4,82★/1.525. Mô tả không ghi số cái/gói |
| Đồ gá kẹp motor | Kẹp chữ C của C3 | — | 0 | | |

**Tạm tính C4 (chưa ship):** ~0,32tr.

---

## C5 — Lắp hoàn chỉnh

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| Nút E-stop tạm | LA38 của C1 | — | 0 | có từ C1 | C10 thay bằng nút mở cưỡng bức |
| Tay cầm có nút giữ | Tay cầm 2,4 GHz, phân loại "Cổng USB + Micro USB" (G.M Store) | https://shopee.vn/product/36462866/6352528872 | 186,2k | đề xuất | 4,77★/1.827, 7k+ lượt bán. Không rõ chip dongle → chạy `ros2 run joy joy_enumerate_devices` ngay khi nhận, Linux không thấy thì trả `[tự đo]`. Chắc ăn hơn: Logitech F710 1.209k https://shopee.vn/product/52679373/845827881 (4,92★/71) |
| Tụ gốm 100 nF 50 V | Phân loại "10 CON 104" × 2 túi (Linh Kiện Điện Tử LiKi) | https://shopee.vn/product/404478549/21161544154 | 2×11,4k | đề xuất | 4,89★/438 |
| Tụ bulk low-ESR cho VM driver | Rubycon ZLH 35 V 1000 µF × 3 (DB Dynamics) | https://shopee.vn/product/1855865463/48663152831 | 3×25k | đề xuất | 5★/4, 19 lượt bán. 2 cái cho hai driver, 1 cái cho amp C12. ZLH là dòng low-ESR của Rubycon `[spec — catalogue Rubycon, kiểm]`; hàng nhái Rubycon phổ biến → kiểm chữ ZLH trên vỏ. Thay thế (không ghi low-ESR): iLinhkien 35 V 1000 µF 26,3k/5 con https://shopee.vn/product/1046767853/23952516250 |
| Lõi ferrite cho dây motor | Ugreen, phân loại "7mm" | https://shopee.vn/product/196261835/16198523857 | 36,3k | đề xuất | Cùng listing C4 |
| Băng dính sàn, thước dây | Của C6 | — | 0 | | Mua đồ C6 trước C5 |
| Khối kê, bàn phím/màn hình | Đồ sẵn có | — | 0 | | |

**Tạm tính C5 (chưa ship):** ~0,32tr; ~1,34tr nếu lấy F710.

---

## C6 — Odometry

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| Thước dây thép 10 m | Deli, phân loại "Vàng 10mx25mm" (Deli Tools Official Store) | https://shopee.vn/product/521320189/22381846656 | 88,5k | **hỏi shop** | 4,91★/2.249. Listing **không ghi cấp chính xác** → hỏi hoặc xem ảnh vỏ có ký hiệu "II". Khi nhận: so vạch 1 m với thước lá dòng dưới |
| Thước lá thép 1 m | Phân loại "Dài 1000mm" (Cokhituanphuongchogioi) | https://shopee.vn/product/1046867314/25589934708 | 100,5k | đề xuất | 4,90★/302. Inox bản 38 mm, dày 1,2 mm, khắc chìm |
| Ê-ke 30 cm | JCTOP AY0300 (OBP Retail Space) | https://shopee.vn/product/1815412333/45162321037 | 105k | đề xuất | 5★/18. Kiểm bằng phép lật mặt ở mục BOM. Rẻ hơn: ke 300 mm 24k https://shopee.vn/product/107238804/9239547941 (4,84★/294) |
| Băng keo giấy 2 màu | Màu cam, phân loại "1 cuộn 20mm - GIAY20" (Đức Hiếu Shop) + màu trắng 2 cm (Tape Mall) | https://shopee.vn/product/27661858/24055631628 · https://shopee.vn/product/90749935/22462491313 | 19,5k + 5,4k | đề xuất | Không có đúng cỡ 24 mm; 20 mm đủ dùng. Dán thử 1 ngày lên sàn |
| Điểm tham chiếu | Module laser 5 mW 650 nm, phân loại "Đi-ốt laser chấm" (Thiết Bị Máy Sài Gòn) | https://shopee.vn/product/164688497/23304786971 | 56,8k | đề xuất | 4,89★/105. Có chỉnh tiêu cự. Không nhìn thẳng vào tia; chỉ chiếu xuống sàn |
| Khung chữ L | Nhôm 2020 + ke góc của C9 (nhờ shop cắt thêm 2 đoạn 40 cm), hoặc gỗ | — | 0 | | Đặt nhôm C9 sớm nếu dùng cho C6 |
| Tấm xốp 3 cm | Phân loại "1 tấm 3cmx50cmx100cm" (BÁCH HOÁ TỔNG HỢP 29) | https://shopee.vn/product/1192097406/24489220741 | 65k | đề xuất | 4,93★/198. Shop từ chối đơn đi GHN (đọc mô tả) |
| Thảm thử | Thảm sẵn có | — | 0 | | |

**Tạm tính C6 (chưa ship):** ~0,44tr.

---

## C7 — Cảm biến, ghi dữ liệu

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| IMU | Dùng lại MPU6050 mua ở K5 (chưa mua K5 → mục 0.3 đợt F) | — | 0 | có từ K5 | **Không có module breakout ICM-42688-P giá hợp lý trên Shopee**: chỉ thấy chip trần LGA-14 (210k), module "601N1" có MCU riêng nói UART (277k, không đọc thanh ghi trực tiếp được), hoặc module 880–960k. Muốn ICM-42688-P thì đặt AliExpress/Mouser. Dùng MPU6050 thì ghi vào `decisions.md` cái giá về nhiễu (BOM mục 2) |
| Đế giảm rung | Băng keo xốp 3M VBH "CUỘN XỐP 3 MÉT x 5MM" + 20 vòng đệm cao su chống rung M2/M3 (loại cho mạch FPV) | https://shopee.vn/product/81520581/26279272788 · https://shopee.vn/product/870173721/23907526776 | 22,9k + 67,4k | đề xuất | 4,78★/74; 4,96★/71. Tấm gel silicone: chưa tra |
| Dây I2C + INT nhiều màu | Cáp bẹ 7 màu loại 10 sợi, tách lấy 5 sợi | https://shopee.vn/product/1206802084/29308056948 | 10k | đề xuất | 4,97★/60. Cáp bẹ thường là 28 AWG (BOM muốn 24–26 AWG); chấp nhận được với dây ≤ 30 cm. Dây silicon 26 AWG ở các shop chỉ có đỏ/đen |
| Camera USB | Dùng lại Logitech C270 mua ở K5 (chưa mua K5 → mục 0.3 đợt F) | — | 0 | có từ K5 | UVC, 720p, lấy nét cố định `[spec — Logitech; kiểm MJPEG 720p30 bằng v4l2-ctl]`. **Không có ren 1/4"**, dây liền ~1,5 m (không thay ngắn được) → bó dây bằng dây rút |
| Giá camera | Giá đỡ webcam bằng thép, phân loại "Không có đầu bi,Trung: 35cm" (Cửa hàng giáo dục) | https://shopee.vn/product/135318102/5839377767 | 145k | **hỏi shop** | 4,89★/213. Hỏi cách bắt vào khung (cần **hai** vít). Phương án rẻ hơn: in 3D ngàm kẹp C270 |
| Cáp USB ngắn + kẹp | Dây rút + đế dán của C2 | — | 0 | | |

**Tạm tính C7 (chưa ship):** ~0,25tr khi dùng lại IMU và camera của K5; thêm 461k nếu mua C270 riêng cho robot.

---

## C8 — Điều hướng

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| Camera | C270 của C7 | — | 0 | | Kiểm `--list-ctrls` có exposure tay. C270 lấy nét cố định nên không có control focus |
| In tag, bàn cờ | In laser trắng đen, giấy mờ, "Actual size", ở tiệm photo | — | ~20k | | |
| Tấm bồi | Formex 5 mm, phân loại "DÀY 5MM,2tấm A4 (20x30cm)" + "DÀY 5MM,2 tấm 30cmx30cm" (Formex Cao su non Thái An) | https://shopee.vn/product/267106798/22414884224 | 29k + 33k | đề xuất | 4,89★/439. Tấm "A4" của shop là 20×30 cm, hẹp hơn A4 thật 1 cm. Bàn cờ 9×6 góc trong, ô 25 mm = 250×175 mm, vừa tấm 30×30 |
| Keo bồi | 3M Super 77, 375 g | https://shopee.vn/product/157594197/17340696635 | 225k | đề xuất | 4,93★/290. Băng keo hai mặt mỏng khổ rộng: chưa tìm được (chỉ có khổ 1–5 mm) |
| Thước dây | Thước 10 m của C6 | — | 0 | | |
| Máy đo laser *(tùy chọn)* | ATuMan LS-P 40 m (HaNoi_ Store) | https://shopee.vn/product/600892110/22667780095 | 590k | đề xuất | 4,88★/432. Shop ghi sai số **±3 mm** (BOM muốn ±2 mm) |
| Ê-ke, thước thủy | Ê-ke của C6 + thước thủy Deli phân loại "230mm DL290230" | https://shopee.vn/product/521320189/13115477943 | 77k | đề xuất | 4,91★/2.147 |
| Băng dính sàn, bút | Của C6 | — | 0 | | |
| Chân máy ảnh | TOPICK, phân loại "3366 (1M4)" (Phụ Kiện Topick) | https://shopee.vn/product/1599943659/40861809233 | 206,4k | đề xuất | 4,96★/1.377. Kiểm có ốc 1/4" khi tháo kẹp điện thoại |
| ToF VL53L1X × 2 (cộng cái của K5 = 3) | CJMCU-531 (SAMIORE.vn) | https://shopee.vn/product/578443443/23266524871 | 2×106,5k | đề xuất | 5★/36. Cùng shop INA226 ở C1. Kiểm: đọc khoảng cách tới bức tường đã đo bằng thước |
| Lidar *(chỉ khi chọn đường lidar ở C8.1)* | RPLIDAR C1M1 | https://shopee.vn/product/1419756587/45651899727 | 2.600k | đề xuất | 5★/1. Rẻ: LDRobot LD14 390k https://shopee.vn/product/18248080/45116934321 (shop ghi hỗ trợ ROS 1/2; cùng hãng với LD06/LD19 nhưng tầm ngắn hơn `[kiểm datasheet]`). LD06/LD19 đúng tên: không thấy trên Shopee |

**Tạm tính C8 (chưa ship):** ~0,8tr với đường marker + ToF; thêm 0,39–2,6tr nếu lidar, 0,59tr nếu máy đo laser.

---

## C9 — Nhận người, privacy

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| Camera nhận mặt USB | Module camera USB OV9726 1 MP, 70° (dinghingxi23c.vn) | https://shopee.vn/product/816451625/44560165157 | 198,1k | **hỏi shop** | 4,8★/5. 1280×720, ống kính 2,8 mm, module trần 30×25 mm. Hỏi: 70° là góc chéo hay góc ngang; có exposure tay qua UVC không. C270 (góc chéo 55° `[spec — Logitech]`) hẹp hơn mức 60–80° ngang bài cần |
| Cáp USB có công tắc | "Dây cáp USB 2.0 có công tắc", phân loại "1 meter" (doublebuy.vn) | https://shopee.vn/product/135041292/2193172816 | 80,3k | **hỏi shop** | 4,96★/92. Hàng quốc tế, giao 7–9 ngày. Shop ghi "truyền dữ liệu không lỗi" → hỏi công tắc cắt VBUS hay cắt cả D+/D−. Kiểm thông mạch VBUS khi bật/tắt |
| LED đỏ 5 mm + điện trở | LED của kit Arduino + kit điện trở (mục 0.3 đợt A) | — | 0 | có từ kit | |
| Cột gá | Nhôm định hình 2020, phân loại "Trắng/ 1 mét,2020" (PStore Linh Kiện CNC) | https://shopee.vn/product/370915692/18582419413 | 125k | đề xuất | 5★/26. Shop cắt theo yêu cầu: ghi chú 1 đoạn 60 cm + 2 đoạn 20 cm (hoặc 2×40 cm cho khung chữ L của C6; khi đó lấy thanh 2 m) |
| Ke góc + tán T + bulông | Ke góc "2020 Bạc(3 cái)" ×2 (SaGo Tool); tán T "2020 M5,10 Con" (PStore); bulông lục giác M5 inox | https://shopee.vn/product/59961430/21489197884 · https://shopee.vn/product/370915692/21191309242 · https://shopee.vn/product/1611132548/44115001947 | 2×16,5k + 22k + 32k | đề xuất | Bulông: chọn M5×10 trong listing |
| Ngàm camera | Đầu bi đôi Ulanzi R102, ren 1/4" (HL Studio) | https://shopee.vn/product/75197188/27670825238 | 130k | đề xuất | 4,94★/96. Siết xong lắc không tự xoay |
| Nút "nghe / từ chối" | Qanba 30 mm, phân loại "30mm màu đỏ" + "30mm Màu xanh lá cây" (qanba.vn) | https://shopee.vn/product/1136955831/26575806363 | 2×53k | đề xuất | 4,87★/47. Giá một nút |
| Đo ánh sáng | App lux trên điện thoại | — | 0 | | Lux kế nếu cần: BSIDE L1 254k https://shopee.vn/product/196261835/25718676160 (4,87★/420) |
| RC522 + thẻ *(chỉ khi kích hoạt FAIL action)* | Có trong kit Arduino (RC522, thẻ trắng, móc khóa) | — | 0 | có từ kit | 4,96★/579 |
| Coral / Hailo | **Không mua** tới khi C9.2 chứng minh cần | — | — | bỏ | |

**Tạm tính C9 (chưa ship):** ~0,73tr.

---

## C10 — An toàn vận hành

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| Nút E-stop mở cưỡng bức | Schneider XA2ES542, phân loại "Xoay nhả XA2ES542" (shop Schneider Electric) | https://shopee.vn/product/1103000849/24806292846 | 118k | đề xuất | 5★/28. Nấm Ø40, lỗ Ø22, 1NC, xoay nhả, IP65. **Kiểm ký hiệu ⊝ trên khối tiếp điểm** trước khi lắp. Thay thế: IDEC YW1B, phân loại "Nhấn Khẩn" 112k https://shopee.vn/product/1353620562/28041250430 |
| Nền vàng cho E-stop | Tem EMG PVC, phân loại "Phi 22-D60mm" (Autosup) | https://shopee.vn/product/1124609329/25405669625 | 7k | **hỏi shop** | 4,97★/30. Mô tả ghi "nền đỏ" → hỏi có bản nền vàng không; không có thì cắt formex sơn vàng |
| Relay K1 5 chân | Relay 5 chân của C1 | — | 0 | có từ C1 | Listing C1 không có datasheet thời gian nhả → đo ở C10.1 |
| Zener 10 V 1 W + 1N4007 | Zener phân loại **"10V"** (Linh kiện Fixpro; "20V" chỉ khi Q1 ≥40 V, mục 0.2) + 1N4007 túi 10 con | https://shopee.vn/product/71427966/7246108342 · https://shopee.vn/product/27117857/368931341 | 15k + 10,8k | đề xuất | 4,91★/550; 4,91★/1.183 |
| MOSFET Q1 | AO3400 (link dòng "Tiền nạp VM") + Zener 10 V | — | 11,9k | **chốt ở mục 0.2** | Không thấy MOSFET SOT-23 nào **vừa** V_DS ≥ 40 V **vừa** ghi R_DS(on) ở V_GS = 2,5 V mà có lượt bán (IRLML0040: chỉ có listing 0 lượt bán). AO3400 (11,9k/10 con https://shopee.vn/product/1710381006/46304074429) có R_DS(on) ở 2,5 V nhưng V_DS chỉ 30 V `[spec — datasheet AOS]` → chỉ dùng được nếu V_pack + V_Zener còn dư xa 30 V, tức Zener ≤ ~10 V (tính lại thời gian nhả relay ở C10.1) |
| Linh kiện mạch xung giữ | Tụ 1 µF (Linh kiện Bách Việt); Schottky dùng 1N5819 của C1; điện trở kit K1 | https://shopee.vn/product/498850430/11633363897 | 10k | đề xuất | Listing ghi "104P 1UF 100NF" → kiểm mã khắc trên tụ (105 = 1 µF) |
| Bumper | Công tắc hành trình KW11 có bánh xe, phân loại "5 CÁI Có bánh xe" (Linhkiengiasi247) + tấm EVA | https://shopee.vn/product/1032535693/16298091172 · https://shopee.vn/product/1293086412/50407308852 | 25,3k + từ 25k | đề xuất | 4,93★/1.057. KW11 3 chân, có chân NC. Đo lực kích bằng cân hành lý C0 |
| Cảm biến vực *(nếu khu soak có bậc)* | 2× VL53L0X GY-530 (SAMIORE.vn) | https://shopee.vn/product/578443443/26608179549 | 2×39,4k | đề xuất | 4,91★/109. Sharp GP2Y0A41: không tìm thấy trên Shopee |
| Nút RESET | IDEC YW1B, phân loại "Nhấn Xanh 1NO" (Thiết Bị Điện 2Q) | https://shopee.vn/product/1353620562/28041250430 | 76k | đề xuất | 5★/16. Đầu nhấn phẳng, khó chạm nhầm hơn đầu lồi |
| Cầu phân áp 47k/10k + tụ 100 nF | Kit điện trở K1, tụ gốm C5 | — | 0 | | |
| TVS trên VM | SMBJ18A, phân loại "SMBJ18A" (bộ 50 con, pauluo8885.vn) | https://shopee.vn/product/1274879032/26454707677 | 35,4k | đề xuất | 4,92★/52. Gói SMB (hàn dán) |
| Tiền nạp VM | P-MOSFET AO3401 (V_DS −30 V); NPN C1815; điện trở 100 Ω 3 W (20 con); 1N4007 dòng trên | https://shopee.vn/product/1710381006/46304074429 · https://shopee.vn/product/1022361603/21983245317 · https://shopee.vn/product/61439282/4338958753 | 12,4k + 5k + 40k | đề xuất | Phân loại "AO3401". Listing C1815 ghi nhầm "PNP": C1815 là NPN `[chuẩn]`, đo chế độ diode cho chắc |
| Biển báo | In A5 ép plastic ở tiệm photo | — | ~20k | | |

**Tạm tính C10 (chưa ship):** ~0,5tr.

---

## C11 — Sim, HIL, CI

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| ESP32-S3 #2 | Con mua ở đợt D (mục 0.3) | — | 0 | xem C4 | |
| Adapter USB–UART | Module CP2102 (có hóa đơn) | https://shopee.vn/product/225740638/6458925653 | 75k | đề xuất | 5★/21. CP210x không có "latency timer" kiểu FTDI nhưng vẫn gom gói theo cách riêng → đo trễ loopback bằng logic analyzer `[tự đo]`. FT232RL giá 12–60k trên Shopee gần như chắc là chip nhái |
| Dây Dupont cái–cái | Dây test board 20 cm, chọn loại cái–cái (PVN ĐIỆN TỬ) | https://shopee.vn/product/16504852/7050771926 | 23,1k | đề xuất | 4,91★/1.607 |
| Thước, băng dính, thước góc | Đồ của C6/C8; vạch 360° in giấy dán sàn | — | 0 | | Thước đo góc điện tử nếu muốn: 180k https://shopee.vn/product/1316297282/29430627079 |
| Dây con lắc hai dây | Dây câu PE bện X4 (ít giãn) | https://shopee.vn/product/1608604347/52106235017 | 116,6k | đề xuất | 4,78★/210. Cuộn 300 m, thừa nhiều. Rẻ hơn: paracord 4 mm 29,5k https://shopee.vn/product/38201633/27211604799 (giãn nhiều hơn). Móc treo trần: tiệm kim khí |
| Máy CI, GPU thuê | Không mua trên Shopee | — | — | | Ghi lựa chọn vào `decisions.md` |

**Tạm tính C11 (chưa ship):** ~0,21tr.

---

## C12 — Sản phẩm

| Món | Chọn | Link | Giá | Trạng thái | Ghi chú / phải kiểm |
|---|---|---|---|---|---|
| Amp class-D ăn từ pack | **Đã có:** TPA3110 2×15 W 8–18 V (ONE SHOP). Listing gợi ý trước đây: TPA3110 XH-A232 2×30 W, 8–26 V (SAMIORE.vn) | https://shopee.vn/product/578443443/10080426932 | 0 | có | 4,74★/1.631, 8k+ lượt bán. Đọc mã chip; **kiểm chân SD/MUTE có ra header không**, và đầu vào trên board là đơn cực hay vi sai (chip vi sai, board thường nối đơn cực) `[tự đo]`. Thay thế: TPA3110D2 2×15 W của Lập Trình Nhúng A-Z 60k https://shopee.vn/product/107147748/27244117229 |
| Loa có hộp | Loa cộng hưởng 4 Ω 3 W có hộp (Lập Trình Nhúng A-Z) | https://shopee.vn/product/107147748/55018157150 | 45k | đề xuất | Chưa có đánh giá. Hoặc dùng loa K3. Loa trần 4 Ω 5 W 52 mm 41,5k https://shopee.vn/product/742847634/20409332207 (4,83★/227) + tự làm hộp |
| Cầu chì FE + giá | Vỏ cầu chì ống 5×20 có dây + ruột phân loại "2A,5 x 20 mm" và "3A,5 x 20 mm (20 cái)" (Linh Kiện Điện Tử Tino) | https://shopee.vn/product/85716713/6749411184 · https://shopee.vn/product/315383150/4755821277 | 10k + 8,8k + 20,9k | đề xuất | Chốt định mức sau khi đo dòng đỉnh amp ở C12.1 |
| Tụ bulk sát amp | Rubycon ZLH thứ ba đã mua ở C5 | — | 0 | có từ C5 | |
| Cáp tín hiệu audio | Dây tín hiệu chống nhiễu 2 lõi + mass, UL2547 28 AWG, 5 m | https://shopee.vn/product/1206233404/24973097527 | 50k | đề xuất | 4,90★/204. Kiểm lưới không chạm lõi |
| Vòng ferrite | Ugreen của C5 | — | 0 | | |
| ESP32-S3 #2 *(tùy chọn)* | Con thứ hai từ K1 | — | 0 | | |
| Bộ cách ly ground loop *(tùy chọn)* | — | — | — | **chưa tìm được** | Chỉ thấy 1 listing 0 lượt bán. Sửa đi dây trước |

**Tạm tính C12 (chưa ship):** ~0,17tr.

---

## Tổng K7 C3–C12 (chưa ship, chưa voucher)

~3,9tr ở cấu hình rẻ nhất: DRV8871, tay cầm 2,4 GHz, dùng lại IMU và camera của K5, không lidar, không máy đo laser. Cộng thêm theo lựa chọn: BTS7960 +0,09tr · F710 +1,02tr · C270 riêng cho robot +0,46tr · máy đo laser +0,59tr · lidar LD14 +0,39tr hoặc RPLIDAR C1 +2,6tr.
