# MA TRẬN RÀ SOÁT BẢO MẬT 10 TIÊU CHÍ BẮT BUỘC (LAB 14)

- **Nhóm thực hiện kiểm toán:** Nhóm 5 (K57 Kinh Tế Số — HCE)
  - Hoàng Mạnh Tường (23K4300042)
  - Nguyễn Nguyên Phương (23K4300034)
- **Hợp đồng được kiểm toán:** [`EventTicketCore.sol`](./PEER_CONTRACT_CODE.sol) (Dự án Vé sự kiện của Nhóm 6)
- **Căn cứ pháp lý & quy chuẩn:** Danh mục kiểm tra bắt buộc tại Trang 32 Sổ tay thực hành ECO2432 và quy ước [AGENTS.md](../../AGENTS.md).

---

## BẢNG MA TRẬN 10 TIÊU CHÍ RÀ SOÁT BẮT BUỘC

| # | Hạng mục kiểm tra | Câu hỏi kiểm tra chuẩn | Kết quả đánh giá | Dòng mã nguồn minh chứng | Chi tiết đánh giá & Rủi ro phát hiện |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **1** | **Phân quyền** | Mọi hàm nhạy cảm có kiểm tra người gọi không? Có hàm nào quên kiểm tra không? | ⚠️ **Cảnh báo** | Dòng 74–77 (`refundTicket`) | Hàm `refundTicket` có kiểm tra `ownerOf(tokenId) != msg.sender` nhưng thiếu kiểm tra trạng thái vé đã bị hủy hay chưa trước khi thao tác. Các hàm quản trị `issueVipTicket`, `checkIn`, `setTicketPrice`, `withdraw` có modifier `onlyOwner`. |
| **2** | **Thứ tự thao tác (CEI)** | Có hàm nào chuyển tiền ra ngoài trước khi cập nhật biến trạng thái không? | ❌ **LỖI NGHIÊM TRỌNG** | **Dòng 81–86 (`refundTicket`)** | **VI PHẠM CEI TRẦM TRỌNG:** Lệnh chuyển ETH `payable(msg.sender).call{value: refundAmount}("")` được thực thi ở dòng 81–82 TRƯỚC KHI gọi `_burn(tokenId)` (dòng 85) và `hasPurchased = false` (dòng 86). Kẻ tấn công có thể lợi dụng hàm `receive()` để re-enter rút cạn toàn bộ quỹ vé của ban tổ chức! |
| **3** | **Điều kiện thời gian** | Dấu so sánh có đúng chiều không? Thử nghĩ trường hợp đúng bằng mốc. | ⚠️ **Cần bổ sung** | Hàm `refundTicket` | Hợp đồng thiếu ràng buộc thời hạn hoàn vé trước ngày diễn ra sự kiện (`deadline`). Người dùng có thể xem xong sự kiện rồi mới gọi `refundTicket` nếu ban tổ chức quên bấm `checkIn`. |
| **4** | **Phép chia số nguyên** | Có phép chia nào làm tròn xuống thành 0 với số nhỏ không? | ❌ **LỖI TRUNG BÌNH** | **Dòng 92 (`calculateResellFee`)** | Nhóm bạn dùng `(resellPrice * resellFeePercent) / 100`. Nếu bán lại vé mệnh giá nhỏ hoặc tỷ lệ phần trăm lẻ dưới 1%, phép chia làm tròn xuống thành 0. **Vi phạm AGENTS.md Điều 7**: Tỷ lệ phần trăm bắt buộc dùng basis point (1% = 100). |
| **5** | **Cách chuyển ETH** | Dùng `call` hay `transfer`? Có kiểm tra kết quả trả về không? | ✅ **Đạt** | Dòng 81 & Dòng 102 | Nhóm bạn đã dùng đúng cú pháp `(bool ok, ) = payable(...).call{value: ...}("")` và có kiểm tra `require(ok, ...)`, không dùng `transfer`. |
| **6** | **Dữ liệu riêng tư** | Có dữ liệu nào tưởng là bí mật nhưng thực ra đọc được không? | ✅ **Đạt** | Toàn bộ biến trạng thái | Không lưu trữ dữ liệu nhạy cảm hoặc bí mật on-chain. |
| **7** | **Vòng lặp không giới hạn** | Có vòng lặp nào chạy trên danh sách dài không giới hạn không? | ✅ **Đạt** | Toàn bộ hợp đồng | Hợp đồng không sử dụng vòng lặp `for/while` duyệt qua mảng động, phòng tránh triệt để lỗi Gas Limit DoS. |
| **8** | **Sự kiện (Event)** | Mọi thay đổi trạng thái có ghi lại sự kiện để tra cứu không? | ❌ **LỖI NHẸ** | **Dòng 97–99 (`setTicketPrice`)** | Hàm thay đổi giá vé `setTicketPrice` là thao tác quản trị kinh tế nhạy cảm nhưng hoàn toàn KHÔNG phát sự kiện `event`, làm mù thông tin trên Etherscan và giao diện Web3 DApp. |
| **9** | **Trường hợp số 0** | Nạp 0 đồng, rút khi số dư 0, danh sách rỗng — xử lý thế nào? | ⚠️ **Cảnh báo** | Dòng 49 (`buyTicket`) | Hàm `buyTicket` kiểm tra `msg.value != ticketPrice`, nếu ban tổ chức vô tình đặt `ticketPrice = 0` thì người dùng sẽ mint vé miễn phí không giới hạn. |
| **10** | **Địa chỉ rỗng (`address(0)`)** | Có kiểm tra tham số địa chỉ khác `address(0)` không? | ❌ **LỖI TRUNG BÌNH** | **Dòng 61–66 (`issueVipTicket`)** | Hàm phát hành vé VIP `issueVipTicket(address to)` hoàn toàn không kiểm tra `require(to != address(0))`. Nếu ban tổ chức gõ nhầm địa chỉ 0x0, vé sẽ bị đúc vào hố đen và tiêu tốn một suất trong `maxSupply`. |

---

## TỔNG KẾT RÀ SOÁT
- **Tổng số lỗi phát hiện:** **4 vấn đề** (1 Nghiêm trọng, 2 Trung bình, 1 Nhẹ).
- **Đánh giá tổng quan:** Hợp đồng có cấu trúc ERC-721 rõ ràng nhưng mắc lỗ hổng Reentrancy chết người trong luồng hoàn tiền và sai lệch quy ước tài chính basis point của `AGENTS.md`.
