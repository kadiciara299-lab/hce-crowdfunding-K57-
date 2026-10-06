# LAB 07: TÍNH CHI PHÍ VẬN HÀNH THỰC TẾ

## 1. Số liệu gas đo đạc thực tế từ Remix VM (Két TimeLockVault)
- Môi trường đo: Remix VM (Solidity ^0.8.20)
- Giả định tính toán: Gas Price = 20 Gwei, Giá ETH = 3,000 USD

| Thao tác | Lượng gas thực tế (Transaction Cost) | Chi phí (ETH) | Chi phí (USD) |
| :--- | :--- | :--- | :--- |
| **Triển khai hợp đồng** |  22840 gas | 0.0050 ETH | 15.00 USD |
| **Nạp tiền (`deposit`)** | 22840 gas | 0.0004568 ETH | 1.37 USD |
| **Rút tiền (`withdraw`)** | 34499 gas | 0.0006000 ETH | 1.80 USD |

---

## 2. Giải bài toán vận hành thẻ tích điểm CLB (1.000 lượt/tháng)
*Mỗi lượt cộng điểm là 1 giao dịch ghi dữ liệu (ước tính tương đương 1 lượt ghi ~22,840 gas).*

### a. Chi phí một tháng trên mạng Ethereum Mainnet:
- Phí 1 lượt ghi: 22840 gas × 20 × 10⁻⁹ × 3,000 USD = 1.37 USD
- Tổng chi phí 1 tháng (1.000 lượt): 1,000 × 1.37 USD = **1,370 USD/tháng** (tương đương khoảng 34 triệu VNĐ).

### b. Chi phí nếu chuyển sang mạng Layer 2:
- Mạng Layer 2 có phí rẻ hơn khoảng 100 lần.
- Chi phí 1 tháng: 1,370 USD ÷ 100 = **13.70 USD/tháng** (tương đương khoảng 340.000 VNĐ).

### c. Ai trả khoản này? Sinh viên có chấp nhận không?
- Nếu CLB trả: Trên Mainnet là bất khả thi với ngân sách sinh viên; trên Layer 2 thì nằm trong khả năng quỹ của CLB.
- Nếu sinh viên trả: Sinh viên không bao giờ chấp nhận trả 1.37 USD (~35.000 VNĐ) tiền phí gas chỉ để nhận vài điểm tích lũy thưởng.

### d. Kết luận tính khả thi:
- Mô hình này **hoàn toàn không khả thi trên mạng chính Ethereum (Layer 1)** vì phí giao dịch vượt xa giá trị kinh tế của thẻ tích điểm.
- Mô hình **chỉ khả thi khi triển khai trên Layer 2** (như Arbitrum, Optimism, Base).

---

## 3. Mở rộng cho ý tưởng của nhóm
- Đối với dự án của nhóm: Thao tác cốt lõi gồm [tên thao tác, ví dụ: nạp tiền/đặt cọc], tiêu tốn khoảng [...] gas.
- Nhóm quyết định lựa chọn mạng [Layer 2 cụ thể] để chi phí người dùng ở mức chấp nhận được (< 0.05 USD/giao dịch).