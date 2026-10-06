# SPEC - Cổng Gây Quỹ Sinh Viên Có Hoàn Tiền (Crowdfunding Vault)

## 1. Mục đích
Hệ thống giữ hộ tiền đóng góp cho dự án gọi vốn cộng đồng; tự động giải ngân cho chủ dự án nếu đạt mục tiêu trước hạn chót, hoặc cho phép từng người đóng góp tự rút lại tiền nếu hết hạn mà không đạt mục tiêu

## 2. Đầu vào
- `goal`: Số tiền ETH mục tiêu cần gọi (uint256, wei), thiết lập lúc khởi tạo[
- `duration`: Thời gian gọi vốn tính bằng giây (uint256), thiết lập lúc khởi tạo.
- `creator`: Địa chỉ ví của chủ dự án nhận tiền giải ngân (address)
- Tiền đóng góp của người ủng hộ: gửi kèm giao dịch thông qua hàm `contribute()` (msg.value > 0)

## 3. Quy tắc nghiệp vụ
- R1: Bất kỳ ai cũng có thể đóng góp ETH khi chiến dịch còn trong thời hạn và tổng tiền chưa đạt mục tiêu
- R2: Hệ thống ghi nhận chính xác số tiền tích lũy của từng ví (`contributions[msg.sender]`) và tổng tiền đã gọi (`totalRaised`)
- R3: Chỉ chủ dự án (`creator`) mới được phép rút toàn bộ quỹ (`claimFunds()`), và chỉ rút được khi `totalRaised >= goal`
- R4: Nếu đã qua thời hạn gọi vốn (`block.timestamp >= deadline`) mà `totalRaised < goal`, từng người ủng hộ được quyền tự gọi hàm rút lại (`refund()`) đúng số tiền mình đã góp
- R5: Sau khi rút tiền (giải ngân hoặc hoàn tiền), số dư ghi nhận của đối tượng đó phải lập tức đưa về 0 để chống rút lặp lại.
- R6: Mọi thao tác đóng góp, giải ngân và hoàn tiền đều phải phát ra sự kiện (`event`) tương ứng

## 4. Đầu ra
- Trạng thái chiến dịch: Đang gọi vốn (`Active`), Thành công (`Successful`), hay Thất bại/Hoàn tiền (`Failed`)[
- Số dư đóng góp cá nhân và tổng tiến độ gọi vốn hiển thị trên giao diện
- Chuyển giao ETH thành công về đúng ví người nhận
## 5. Trường hợp ngoại lệ
- E1: Người ủng hộ gửi 0 ETH -> Báo lỗi `ZeroContribution()`
- E2: Người ủng hộ cố đóng góp khi chiến dịch đã hết hạn hoặc đã đạt mục tiêu -> Báo lỗi `CampaignNotActive()`
- E3: Chủ dự án cố rút tiền khi chưa đủ mốc `goal` -> Báo lỗi `GoalNotReached()`
- E4: Người ủng hộ yêu cầu hoàn tiền khi chiến dịch chưa hết hạn hoặc đã gọi vốn thành công -> Báo lỗi `RefundNotAllowed()`
- E5: Người có số dư đóng góp bằng 0 yêu cầu hoàn tiền -> Báo lỗi `NoFundsToRefund()`

## 6. Ngoài phạm vi
- Không hỗ trợ rút một phần tiền đã góp (chỉ hoàn trả toàn bộ phần đã đóng khi chiến dịch thất bại)
- Không xử lý quy đổi tỉ giá sang VNĐ trên smart contract
- Không phân chia giai đoạn (milestone) giải ngân nhiều lần