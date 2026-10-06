# SPEC - [Tên bài]

## 1. Mục đích

  Yêu cầu “Viết chương trình phân tích ví.” là một ví dụ điển hình về ĐẶC TẢ CHƯA ĐỦ RÕ (Đặc tả sai). Nếu AI tự suy đoán để viết mã ngay ở bước này, chắc chắn sẽ suy đoán sai nghiệp vụ tài chính và vi phạm nguyên tắc cốt lõi của Lab 5 (KHÔNG VIẾT MÃ NGUỒN TRONG BUỔI NÀY).

## 2. Đầu vào

Địa chỉ ví mục tiêu: Chuỗi 42 ký tự dạng hex bắt đầu bằng 0x... (so sánh không phân biệt hoa thường với to/from).
Khóa API Etherscan: Đọc từ biến môi trường ETHERSCAN_API_KEY qua os.getenv (tuyệt đối không ghi trực tiếp vào mã nguồn theo quy ước 

AGENTS.md
).
Khoảng thời gian: 90 ngày tính ngược từ thời điểm hiện tại (timestamp >= now - 90 days).

## 3. Quy tắc nghiệp vụ

R1 (Dòng tiền vào): Nếu to == address và giao dịch thành công (isError == "0"), ghi nhận là Dòng tiền vào với giá trị = value (ETH).
R2 & R3 (Dòng tiền ra): Nếu from == address, ghi nhận là Dòng tiền ra. Số tiền thực trừ khỏi ví = value + transaction_fee (trong đó transaction_fee = gasUsed * gasPrice).
R4 (Giao dịch thất bại): Nếu from == address và giao dịch thất bại (isError == "1"), value = 0 nhưng ví vẫn phải chịu phí gas $\rightarrow$ Ghi nhận phí gas này vào Dòng tiền ra.
R5 (Đơn vị tính): Toàn bộ số liệu value, gasPrice từ Etherscan API trả về ở đơn vị wei, phải chia cho $10^{18}$ để chuyển đổi sang ETH trước khi tính toán và hiển thị.
R6 (Thứ tự thời gian): Sắp xếp toàn bộ giao dịch theo thứ tự thời gian tăng dần (timeStamp tăng dần) để tính đúng số dư lũy kế theo từng mốc.


## 4. Đầu ra

Bảng dữ liệu dòng tiền: Gồm các cột: Thời gian, Loại (Vào/Ra), Giá trị chuyển (ETH), Phí gas (ETH), Số tiền ròng ảnh hưởng (ETH), Số dư lũy kế (ETH).
Ba chỉ số tài chính tổng hợp:
Tổng dòng tiền vào (Total Inflow)
Tổng dòng tiền ra (Total Outflow, bao gồm cả phí gas)
Chênh lệch số dư ròng trong kỳ (Net Flow = Inflow - Outflow)
Biểu đồ đường (Line Chart qua matplotlib): Trục hoành là thời gian (ngày/tháng), trục tung là số dư lũy kế (ETH).
## 5. Trường hợp ngoại lệ

Ví không có giao dịch trong 90 ngày: In thông báo "Vi khong co giao dich trong ky" và dừng gọn gàng, không báo lỗi đỏ.
Khóa API sai hoặc lỗi mạng: Kiểm tra status_code HTTP và trường status của phản hồi API trước khi bóc tách dữ liệu; thông báo rõ lỗi nếu API từ chối.
Phân trang (Pagination): Xử lý lặp phân trang (page, offset) nếu số lượng giao dịch lớn.

## 6. Ngoài phạm vi


