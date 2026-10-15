# BẢNG ÁNH XẠ NỐI GIAO DIỆN DAPP VỚI SMART CONTRACT (LAB 15)

**Học phần:** ECO2432 — Tiền điện tử & Hợp đồng thông minh  
**Dự án:** HCE Student Crowdfund (Chủ đề 5 — Gây quỹ có hoàn tiền)  
**Tệp hợp đồng:** `contracts/project/ProjectCore.sol`  
**Tệp giao diện:** `web/index.html`  

---

## 1. Thông tin Cấu hình Chung

| Tham số | Giá trị trong DApp | Mô tả nghiệp vụ |
| :--- | :--- | :--- |
| **`CONTRACT_ADDRESS`** | `0x71C3b7C8A9B2c21950b73De79A168f844bF97A48` | Địa chỉ hợp đồng đã triển khai trên Ethereum Sepolia Testnet |
| **`SEPOLIA_CHAIN_ID`** | `11155111` (`0xaa36a7`) | ID mạng thử nghiệm Sepolia; DApp tự động phát hiện và nhắc chuyển mạng |
| **`CONTRACT_ABI`** | JSON ABI từ Remix Compiler 0.8.20 | Chứa 10 hàm view, 3 hàm ghi, 5 sự kiện và 15 mã lỗi tùy biến |
| **Thư viện Web3** | `ethers.umd.min.js` (Ethers v6.13.2) | Cung cấp `BrowserProvider`, `Contract`, `formatEther`, `parseEther` |

---

## 2. Bảng Ánh xạ Chi tiết: Giao diện Web $\leftrightarrow$ Smart Contract

### 2.1. Nhóm Hàm Đọc (View Functions — Miễn phí Gas)

| Tên phần tử trên HTML | ID phần tử | Hàm Smart Contract tương ứng | Kiểu dữ liệu trả về | Ý nghĩa hiển thị trên DApp |
| :--- | :--- | :--- | :--- | :--- |
| Số dư gây quỹ | `#vaultBalance` | `totalRaised()` | `uint256` (wei $\to$ ETH) | Hiển thị tổng số ETH mà các sinh viên đã nạp vào quỹ |
| Mục tiêu chiến dịch | `#fundingGoal` | `fundingGoal()` | `uint256` (wei $\to$ ETH) | Hiển thị mốc $1.000 \text{ ETH}$ cần đạt để thành công |
| Trần cứng an toàn | `#fundingCap` | `fundingCap()` | `uint256` (wei $\to$ ETH) | Mốc $1.200 \text{ ETH}$ ($120\%$) tối đa chiến dịch nhận |
| Mức nạp sàn | `#minContributionText` | `minContribution()` | `uint256` (wei $\to$ ETH) | Mức sàn $0.001 \text{ ETH}$ chống spam giao dịch rác |
| Mức nạp trần mỗi ví | `#maxContributionText` | `maxContributionPerWallet()` | `uint256` (wei $\to$ ETH) | Hạn mức $0.250 \text{ ETH}$ ($25\%$) chống thao túng |
| Thời gian còn lại | `#countdown` | `timeLeft()` / `deadline()` | `uint256` (timestamp) | Đồng hồ đếm ngược từng giây theo thời gian thực |
| Địa chỉ chủ nhiệm | `#creatorAddress` | `creator()` | `address` | Địa chỉ ví sinh viên đại diện khởi tạo đề tài |
| Trạng thái chiến dịch | `#stateBadge`, `#stateText` | `state()` | `enum State (0..3)` | $0$: Đang diễn ra, $1$: Thành công, $2$: Thất bại, $3$: Đã rút quỹ |
| Đóng góp của ví tôi | `#myContribution` | `contributions(userAddress)` | `uint256` (wei $\to$ ETH) | Số ETH ví hiện tại đã nạp; căn cứ để nhận hoàn tiền |

---

### 2.2. Nhóm Hàm Ghi (State-Changing Functions — Yêu cầu Ký Ví & Trả Gas)

| Tên nút trên HTML | ID phần tử | Hàm Smart Contract | Tham số / Value truyền vào | Xử lý trạng thái & Hiển thị |
| :--- | :--- | :--- | :--- | :--- |
| **Nạp Quỹ Vào Chiến Dịch** | `#btnPledge` | `pledge()` | `payable`: `msg.value` (từ `#amount`) | - Khóa nút, xoay spinner.<br>- Chờ `tx.wait()` thành công.<br>- Cập nhật thanh tiến độ và số dư ví. |
| **Chủ Dự Án Rút Tiền** | `#btnClaimFunds` | `claimFunds()` | Không tham số (`msg.sender == creator`) | - Chỉ sáng khi $state == Successful$ hoặc quá hạn đạt mục tiêu.<br>- Chuyển $100\%$ số dư quỹ về ví chủ nhiệm.<br>- Chuyển trạng thái sang `Claimed`. |
| **Rút Lại 100% Hoàn Tiền** | `#btnClaimRefund` | `claimRefund()` | Không tham số (`contributions[msg.sender] > 0`) | - Chỉ sáng khi chiến dịch thất bại ($state == Failed$).<br>- Reset số dư đóng góp về 0.<br>- Hoàn lại $100\%$ ETH về ví người ủng hộ. |

---

### 2.3. Bảng Ánh xạ Lỗi Tùy Biến (Custom Errors) $\leftrightarrow$ Thông báo Tiếng Việt Thân thiện

Smart Contract tuân thủ quy ước `AGENTS.md`, sử dụng `custom error` thay vì chuỗi `require` tốn gas. Giao diện DApp bắt các mã lỗi này qua `try / catch` và hiển thị thông báo rõ ràng:

| Lỗi On-chain (Solidity Custom Error) | Nguyên nhân kích hoạt | Thông báo hiển thị trên hộp `#statusNode` |
| :--- | :--- | :--- |
| `ContributionTooLow(sent, minRequired)` | Người dùng nhập số ETH $< 0.001 \text{ ETH}$ | ❌ **Số tiền gửi nhỏ hơn mức sàn quy định (Tối thiểu 0.001 ETH)!** |
| `ExceedsMaxContribution(attempted, limit)` | Tổng đóng góp của ví vượt quá $25\%$ mục tiêu ($> 0.25 \text{ ETH}$) | ❌ **Vi phạm rào cản trần ví: Mỗi ví chỉ được đóng góp tối đa 25% mục tiêu (0.25 ETH)!** |
| `ExceedsFundingCap(attemptedTotal, cap)` | Khoản nạp làm tổng quỹ vượt quá $120\%$ ($1.2 \text{ ETH}$) | ❌ **Vượt quá trần cứng an toàn (120% mục tiêu = 1.2 ETH). Chiến dịch từ chối nhận thêm quỹ!** |
| `CampaignEnded(deadline, currentTime)` | Nạp tiền khi chiến dịch đã hết hạn chót | ❌ **Chiến dịch đã kết thúc hạn chót nhận quỹ!** |
| `OnlyCreatorAllowed()` | Ví không phải Creator cố tình gọi `claimFunds()` | ❌ **Chỉ chủ nhiệm dự án (Creator) mới có quyền rút tiền giải ngân!** |
| `GoalNotMet(raised, goal)` | Gọi rút tiền khi chưa đạt mục tiêu $1.0 \text{ ETH}$ | ❌ **Chưa đạt mục tiêu tối thiểu (1.0 ETH), không thể giải ngân!** |
| `CampaignStillActive(timeLeft)` | Gọi giải ngân / hoàn tiền khi chiến dịch chưa hết hạn | ❌ **Chiến dịch vẫn đang mở tiếp nhận quỹ, chưa đến hạn chót giải ngân/hoàn tiền!** |
| `CampaignSucceeded()` | Đòi hoàn tiền khi chiến dịch đã thành công | ❌ **Chiến dịch đã thành công và tiền thuộc về dự án, không áp dụng hoàn tiền!** |
| `NoContributionToRefund()` | Ví chưa từng nạp tiền cố tình đòi rút hoàn tiền | ❌ **Ví này chưa đóng góp ETH nào vào quỹ để nhận hoàn tiền!** |
| `AlreadyClaimed()` | Rút quỹ lần 2 sau khi đã giải ngân | ❌ **Quỹ dự án đã được giải ngân hoàn tất trước đó!** |
| `User Rejected (Code 4001)` | Người dùng bấm Từ chối (Reject) trên MetaMask | ⚠️ **Bạn đã từ chối ký xác nhận giao dịch trên ví MetaMask.** |
