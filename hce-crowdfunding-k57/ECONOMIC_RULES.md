# ECONOMIC RULES
Quy tắc dòng tiền, quản trị và chống lạm dụng kinh tế (Phiên bản v0.1)

## 1. Dòng tiền và Quyền lợi
- **Mô hình kinh tế:** Cơ chế gom vốn cam kết nhị phân (All-or-Nothing Crowdfunding).
- **Quyền lợi của Nhà tài trợ (Backers):** 
  - Toàn bộ 100% vốn góp được hợp đồng thông minh bảo vệ trong thời gian gây quỹ.
  - Được đảm bảo thu hồi vốn 100% nếu dự án không đủ điều kiện tối thiểu để hoạt động (không đạt chỉ tiêu).
- **Quyền lợi của Chủ dự án (Creator):** 
  - Nhận được 100% nguồn vốn tài trợ nếu thuyết phục được cộng đồng đạt chỉ tiêu cam kết ban đầu trước khi hết hạn.
  - Được hưởng toàn bộ phần vượt mức chỉ tiêu (nếu có) để phục vụ mở rộng quy mô dự án.

## 2. Giới hạn chống lạm dụng
- **Giới hạn số tiền góp tối thiểu:** Mỗi giao dịch nộp tiền phải có giá trị lớn hơn 0 Wei để ngăn chặn spam giao dịch làm nghẽn mạng và rác dữ liệu sự kiện.
- **Cơ chế kéo tiền về phía người dùng (Pull over Push):** Hợp đồng không dùng vòng lặp tự động gửi tiền trả lại cho tất cả mọi người cùng lúc (dễ bị nghẽn gas và lỗi DOS). Thay vào đó, mỗi cá nhân tự chủ động gọi lệnh rút tiền của chính mình (`claimRefund`).
- **Mô hình Checks-Effects-Interactions (CEI):** Khi người dùng rút tiền hoàn trả, số dư trong hợp đồng phải được trừ về `0` trước khi lệnh chuyển tiền ETH thực hiện, triệt tiêu hoàn toàn khả năng tấn công tái nhập (Reentrancy) nhằm bòn rút tiền của dự án.

## 3. Quyền quản trị
- **Quyền hạn duy nhất của Admin:** Chỉ được phép gọi hàm rút toàn bộ tiền `withdrawFunds()` duy nhất 1 lần khi VÀ CHỈ KHI thỏa mãn đồng thời hai điều kiện: (1) Đã qua thời hạn `deadline` và (2) `totalRaised >= goal`.
- **Hạn chế quyền lực:** Admin KHÔNG có quyền thay đổi mục tiêu vốn (`goal`), không thể thay đổi thời hạn (`deadline`), và tuyệt đối KHÔNG có quyền đụng vào tiền của các nhà tài trợ nếu dự án không đạt chỉ tiêu.

## 4. Tình huống người dùng bị thiệt và Cách xử lý
- **Tình huống 1: Người dùng bị kẹt vốn nếu thời gian gây quỹ đặt quá dài**
  - *Mô tả:* Nếu Admin cài đặt thời hạn 1 năm, người góp tiền sẽ không thể rút lại tiền trước hạn dù thấy dự án không có triển vọng.
  - *Khắc phục:* Giới hạn thời gian gây quỹ tối đa trong mã nguồn (tối đa 30 ngày) tại hàm khởi tạo.
- **Tình huống 2: Admin mất khóa bí mật ví (Private Key)**
  - *Mô tả:* Khi dự án thành công nhưng Admin mất khóa ví, tiền sẽ bị khóa vĩnh viễn trong hợp đồng.
  - *Khắc phục:* Ở phiên bản nâng cao (Lab 11), xem xét bổ sung cơ chế Multi-sig (chữ ký ủy thác từ ban cán sự nhóm) hoặc cho phép giải cứu hoàn tiền sau một khoảng thời gian dự phòng mở rộng (ví dụ sau 60 ngày nếu Admin không rút).