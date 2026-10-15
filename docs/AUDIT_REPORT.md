# BÁO CÁO KIỂM TOÁN CHÉO BẢO MẬT HỢP ĐỒNG THÔNG MINH — LAB 14

- **Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)
- **Đơn vị đào tạo:** Khoa Hệ thống Thông tin Kinh tế — Trường Đại học Kinh tế, Đại học Huế (HCE)
- **Cơ chế ghép cặp:** Vòng tròn theo quy chế Sổ tay thực hành ECO2432 (Trang 32)
  - **Nhóm 5 (K57 Kinh Tế Số - Nhóm chúng ta)** tiến hành rà soát **Nhóm 6 (K57 EventTicket - Chủ đề 6)**.
  - **Nhóm 5** tiếp nhận báo cáo rà soát từ **Nhóm 4 (K57 Học bổng Minh bạch - Chủ đề 4)**.
- **Thông điệp Commit chốt:** `lab-14: xu ly ket qua audit cheo`

---

# PHẦN I: BÁO CÁO RÀ SOÁT — NHÓM 5 RÀ SOÁT NHÓM 6

## 1. Tóm tắt kiểm toán (Audit Summary)
- **Đối tượng rà soát:** Tệp [`contracts/peer/EventTicketCore.sol`](../evidence/lab-14/PEER_CONTRACT_CODE.sol) và tài liệu đặc tả `docs/SPEC.md` của Nhóm 6.
- **Quy mô hợp đồng:** 108 dòng mã nguồn Solidity `^0.8.20`.
- **Tổng số vấn đề phát hiện:** **4 vấn đề**, bao gồm:
  - **1 vấn đề Nghiêm trọng** (Critical - Rút cạn quỹ hợp đồng qua Reentrancy).
  - **2 vấn đề Trung bình** (Medium - Sai lệch phép chia số nguyên & Thiếu kiểm tra `address(0)`).
  - **1 vấn đề Nhẹ** (Low - Thiếu phát `event` khi thay đổi giá vé).

---

## 2. Chi tiết các phát hiện kiểm toán

### Phát hiện 1 — Lỗ hổng Tái nhập (Reentrancy) rút cạn quỹ vé trong `refundTicket()`
- **Mức độ:** **Nghiêm trọng (Critical)**
- **Vị trí:** Dòng 74–88, hàm `refundTicket(uint256 tokenId)`
- **Mô tả:**  
  Hàm `refundTicket` cho phép người mua trả lại vé trước sự kiện để nhận lại tiền cọc. Tuy nhiên, lệnh chuyển tiền ra bên ngoài `(bool ok, ) = payable(msg.sender).call{value: refundAmount}("");` được thực thi ở dòng 81–82 **TRƯỚC KHI** hợp đồng thực hiện lệnh hủy vé `_burn(tokenId)` (dòng 85) và trước khi cập nhật biến trạng thái `hasPurchased[msg.sender] = false` (dòng 86).
- **Tình huống gây thiệt hại thực tế:**  
  Kẻ tấn công sử dụng một Smart Contract độc hại để mua 1 vé giá $1 \text{ ETH}$. Khi gọi hàm `refundTicket()`, lệnh `call{value}` chuyển tiền sang hợp đồng tấn công. Hàm `receive()` của hợp đồng tấn công tự động kích hoạt và gọi ngược lại chính hàm `refundTicket(tokenId)`. Do vé chưa bị burn trên blockchain, bước kiểm tra `ownerOf(tokenId) == msg.sender` tiếp tục thỏa mãn. Quá trình tái nhập diễn ra liên tục cho đến khi rút cạn sạch toàn bộ quỹ bán vé của Ban tổ chức (đã được thực nghiệm chứng minh rút sạch $5 \text{ ETH}$ về $0 \text{ ETH}$ tại [`evidence/lab-14/test_output.log`](../evidence/lab-14/test_output.log)).
- **Khuyến nghị khắc phục:**  
  Áp dụng triệt để mẫu Checks-Effects-Interactions (CEI): Đưa lệnh `_burn(tokenId);` và `hasPurchased[msg.sender] = false;` lên TRƯỚC lệnh `call{value}`. Bổ sung modifier `nonReentrant` của OpenZeppelin.
- **Ai phát hiện:** Thành viên nhóm kiểm toán (Nguyễn Nguyên Phương - Red Team Lead).

---

### Phát hiện 2 — Phép chia làm tròn xuống 0 trong phí chuyển nhượng thứ cấp
- **Mức độ:** **Trung bình (Medium)**
- **Vị trí:** Dòng 91–93, hàm `calculateResellFee(uint256 resellPrice)`
- **Mô tả:**  
  Công thức tính phí của nhóm bạn là `(resellPrice * resellFeePercent) / 100`. Nhóm bạn sử dụng đơn vị phần trăm nguyên (`resellFeePercent = 2` tương ứng 2%).
- **Tình huống gây thiệt hại thực tế:**  
  Vi phạm Điều 7 của quy ước [`AGENTS.md`](../AGENTS.md): *"Tỷ lệ phần trăm dùng basis point, trong đó 1% = 100"*. Khi người dùng chuyển nhượng vé giá rẻ hoặc vé thanh lý có giá trị nhỏ, phép chia số nguyên của EVM làm tròn xuống thành 0. Ví dụ: Với giao dịch bán vé trị giá $0.005 \text{ ETH}$ và phí $2\%$, phí tính ra bị làm tròn thành 0, khiến ban tổ chức thất thoát toàn bộ phí hoa hồng điều tiết vé chợ đen.
- **Khuyến nghị khắc phục:**  
  Đổi biến `resellFeePercent` sang `resellFeeBps` (điểm cơ bản, ví dụ $2\% = 200 \text{ bps}$) và đổi công thức tính sang: `(resellPrice * resellFeeBps) / 10_000`.
- **Ai phát hiện:** Công cụ AI rà soát kết hợp thành viên Hoàng Mạnh Tường (BA Lead).

---

### Phát hiện 3 — Thiếu kiểm tra địa chỉ rỗng `address(0)` trong hàm phát hành vé VIP
- **Mức độ:** **Trung bình (Medium)**
- **Vị trí:** Dòng 61–67, hàm `issueVipTicket(address to)`
- **Mô tả:**  
  Hàm phát hành vé mời đặc cách cho khách VIP do chủ sở hữu gọi (`onlyOwner`) nhưng hoàn toàn không kiểm tra `to != address(0)`.
- **Tình huống gây thiệt hại thực tế:**  
  Nếu ban tổ chức thao tác nhầm trên giao diện hoặc dán địa chỉ rỗng `0x0000...0000`, vé NFT sẽ bị đúc trực tiếp vào địa chỉ hố đen. Biến đếm `nextTokenId` vẫn tăng lên, làm tiêu hao mất một suất vé trong hạn mức `maxSupply` mà không có cách nào thu hồi lại được.
- **Khuyến nghị khắc phục:**  
  Bổ sung dòng kiểm tra ở đầu hàm: `if (to == address(0)) revert InvalidRecipient();`.
- **Ai phát hiện:** Thành viên nhóm kiểm toán (Hoàng Mạnh Tường).

---

### Phát hiện 4 — Thiếu sự kiện `event` khi cập nhật giá vé
- **Mức độ:** **Nhẹ (Low)**
- **Vị trí:** Dòng 96–99, hàm `setTicketPrice(uint256 newPrice)`
- **Mô tả:**  
  Hàm cập nhật giá vé thay đổi biến trạng thái tài chính `ticketPrice` nhưng không phát ra sự kiện nào. Vi phạm Điều 1 của quy ước [`AGENTS.md`](../AGENTS.md): *"Mọi hàm làm thay đổi trạng thái phải phát event"*.
- **Tình huống gây thiệt hại thực tế:**  
  Giao diện Web3 DApp và các công cụ lắng nghe sự kiện on-chain không cập nhật kịp thời khi giá vé thay đổi, khiến người mua gửi nhầm số tiền cũ và bị hủy giao dịch hàng loạt.
- **Khuyến nghị khắc phục:**  
  Khai báo `event TicketPriceUpdated(uint256 oldPrice, uint256 newPrice);` và gọi `emit TicketPriceUpdated(...)` trong hàm.
- **Ai phát hiện:** Công cụ AI rà soát.

---

# PHẦN II: BÁO CÁO RÀ SOÁT NHẬN ĐƯỢC TỪ NHÓM 4 (NHÓM 4 RÀ SOÁT NHÓM 5)

## 1. Tóm tắt đánh giá từ Nhóm 4 về `ProjectCore.sol`
- **Hợp đồng được rà soát:** [`contracts/project/ProjectCore.sol`](../contracts/project/ProjectCore.sol) (149 dòng).
- **Kết luận chung của Nhóm 4:** Hợp đồng có cấu trúc bảo mật rất vững chắc, tuân thủ xuất sắc quy tắc CEI và có modifier `nonReentrant` bảo vệ hàm thanh toán; không sử dụng vòng lặp duyệt mảng. Tuy nhiên, Nhóm 4 nêu ra **3 điểm lưu ý cần tối ưu**:
  1. *Điểm 1 (Mức độ Nhẹ):* Thống nhất điều kiện so sánh mốc thời gian biên tại giây chính xác `block.timestamp == deadline`.
  2. *Điểm 2 (Mức độ Trung bình / Gợi ý kiến trúc):* Khi đóng góp vượt trần cứng `fundingCap`, hợp đồng từ chối toàn bộ giao dịch (`revert ExceedsFundingCap`) thay vì nhận vừa đủ và hoàn lại tiền thừa.
  3. *Điểm 3 (Mức độ Nhẹ / UX):* Sự kiện `CampaignCreated` nên phát thêm thông tin `minContribution` và `maxContributionPerWallet` để Frontend DApp không phải gọi thêm các hàm view.

---

# PHẦN III: PHẢN HỒI VÀ BIỆN PHÁP XỬ LÝ SỬA LỖI CỦA NHÓM 5 (BƯỚC 3)

Nhóm 5 đã họp nhanh và phản hồi chính thức từng điểm của Nhóm 4 như sau:

| STT | Vấn đề Nhóm 4 nêu | Phản hồi giải trình của Nhóm 5 | Quyết định xử lý mã nguồn |
| :-: | :--- | :--- | :--- |
| **1** | **Điều kiện biên thời gian:** Tại giây `block.timestamp == deadline`, `pledge()` từ chối nhưng `claimFunds()` cho phép rút. | **Hoàn toàn đồng thuận:** Đây là thiết kế chủ đích bảo đảm tính chuyển tiếp trạng thái tức thì: Ngay khi hết giờ nhận tiền, cổng giải ngân được mở ngay lập tức, không có "vùng xám" thời gian bị kẹt. | Giữ nguyên logic so sánh `block.timestamp >= deadline` trong `pledge` và `block.timestamp < deadline` trong `claim`, đồng thời bổ sung chú thích nghiệp vụ rõ ràng. |
| **2** | **Xử lý tiền thừa (Excess Refund):** Tại sao không hoàn lại phần dôi dư khi vượt `fundingCap`? | **Giải trình nghiệp vụ:** Nếu viết cơ chế nhận một phần và `call{value}` trả lại phần thừa ngay trong hàm `pledge()`, hợp đồng sẽ tự mở ra **bề mặt tấn công Reentrancy mới** trong quá trình nhận tiền, đồng thời tiêu tốn thêm gas cho tất cả sinh viên bình thường. Quy định trong `SPEC.md` là người nạp tự cân đối số tiền không vượt trần cứng. | Bảo lưu thiết kế an toàn: Từ chối toàn bộ giao dịch vi phạm trần cứng để bảo vệ tính đơn giản và an toàn tuyệt đối của hợp đồng. |
| **3** | **Bổ sung tham số Event `CampaignCreated`:** Giúp giao diện Web3 DApp dễ dàng bắt thông tin khởi tạo. | **Hoàn toàn tiếp thu:** Đề xuất này rất xác đáng, giúp tối ưu hóa hiệu năng cho bài Lab 15 khi xây dựng giao diện kết nối ví MetaMask. | Cập nhật định nghĩa `event CampaignCreated` bao gồm `(creator, fundingGoal, fundingCap, deadline, minContribution, maxContributionPerWallet)`. |

---

## BIÊN BẢN KÝ DUYỆT KIỂM TOÁN CHÉO

```text
       ĐẠI DIỆN ĐOÀN KIỂM TOÁN (NHÓM 5)               ĐẠI DIỆN NHÓM ĐƯỢC DUYỆT (NHÓM 6)
              (Lead Reviewer)                                  (Project Lead)
                  (Đã ký)                                          (Đã ký)


             Nguyễn Nguyên Phương                             Trưởng nhóm 6
```
