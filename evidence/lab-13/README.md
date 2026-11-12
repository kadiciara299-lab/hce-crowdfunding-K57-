# BÁO CÁO THỰC NGHIỆM LAB 13 — REENTRANCY VÀ HARDENING

## 1. Kết quả thực nghiệm trên Remix VM
- Số dư ngân hàng trước tấn công: 6 ETH (3 tài khoản x 2 ETH).
- Số dư ngân hàng sau tấn công: 0 ETH (AttackBank rút sạch thông qua hàm receive).
- Kết quả sau khi vá (Checks-Effects-Interactions): Giao dịch attack() bị revert, bảo toàn số dư.

## 2. Ba câu giải thích khi vấn đáp
1. Lỗ hổng xảy ra do chuyển ETH bằng `.call` trước khi trừ số dư trên sổ sách, trao quyền điều khiển cho hàm `receive()` của kẻ tấn công.
2. Việc đặt dòng cập nhật số dư về 0 lên trước lệnh chuyển tiền giúp mọi lần gọi đệ quy sau đó đều bị chặn ngay ở bước kiểm tra số dư.
3. Trong `ProjectCore.sol`, hàm `claimRefund()` luôn đặt `contributions[msg.sender] = 0` trước khi gọi chuyển tiền để triệt tiêu hoàn toàn rủi ro tái nhập.
