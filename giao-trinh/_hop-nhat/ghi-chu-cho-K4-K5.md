# Ghi chú cho lượt hợp nhất K4/K5 (thu từ các agent F)

- K5 m3 (bản Claude) dòng ~224: "50 byte là kích thước ImuSample Protobuf tự chế" — đo thật 190 B khi đủ trường; kết luận "thiếu ~7 lần" vẫn đúng, sửa phần giải thích nguồn gốc con số. (w-F3)
- K5 Bài 15 bước 3: tên output extractor chỉ theo sha256 nguồn → sau khi sửa bug extractor, output mới trùng tên output lỗi. Thêm version extractor vào tên (→ F3.8). (w-F3)
- K5 Bài 16 gốc: "schema bắt được sai đơn vị" sai; rule |a|=g chỉ đúng khi đứng yên; "σ=0 trong 1 s là kênh đơ" báo nhầm khi host đọc nhanh hơn ODR. (w-F3, đã chấm ở F3.7)
- K5 Bài 17: quan hệ đúng là số lỗ audit thấy ≥ số drop đã khai, không phải "khớp hoàn toàn". (w-F3)
- K4 Bài 2: "1% số lần chậm = robot giật 1% thời gian" lẫn đếm theo lần với theo thời gian. K4 Bài 6: "không tương quan latency–nhiệt" không là bằng chứng khi nhiệt gần như không đổi. (w-F1)
