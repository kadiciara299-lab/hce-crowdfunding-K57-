# BÁO CÁO KIỂM THỬ QUY TẮC KINH TẾ — LAB 11

## 1. Quy tắc đã cài đặt
- Tên quy tắc: Mức đóng góp tối thiểu (Minimum Contribution)
- Giá trị áp dụng: 0.001 ETH (10^15 wei)
- Mã lỗi tùy biến: `ContributionTooLow(uint256 sentAmount, uint256 minAmount)`

## 2. Kết quả kiểm thử trên Remix VM
| Ca kiểm thử | Giá trị gửi | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
| :--- | :--- | :--- | :--- | :--- |
| **Ca vi phạm** | 0.0000005 ETH | Revert với lỗi `ContributionTooLow` | Giao dịch bị chặn, thông báo đúng mã lỗi | ✅ Đạt |
| **Ca hợp lệ** | 0.05 ETH | Thành công, phát sự kiện `Contributed` | Giao dịch được xác nhận, số dư tăng | ✅ Đạt |
