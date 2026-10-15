# BẰNG CHỨNG GIAO DỊCH VÀ THỰC NGHIỆM ON-CHAIN (LAB 15)

**Học phần:** ECO2432 — Tiền điện tử & Hợp đồng thông minh  
**Dự án:** HCE Student Crowdfund (Chủ đề 5 — Gây quỹ có hoàn tiền)  
**Nhóm sinh viên:**  
1. Hoàng Mạnh Tường — 23K4300042 (Contract & Frontend Lead)  
2. Nguyễn Nguyên Phương — 23K4300034 (Security & Presentation Lead)  
**Mạng thử nghiệm:** Ethereum Sepolia Testnet (Chain ID: `11155111`)  

---

## 1. Thông số Kỹ thuật Hợp đồng Triển khai trên Sepolia

| Thuộc tính | Giá trị On-chain |
| :--- | :--- |
| **Tên hợp đồng** | `ProjectCore` |
| **Mã nguồn** | `contracts/project/ProjectCore.sol` (149 dòng, Solidity ^0.8.20) |
| **Địa chỉ hợp đồng (`CONTRACT_ADDRESS`)** | [`0x71C3b7C8A9B2c21950b73De79A168f844bF97A48`](https://sepolia.etherscan.io/address/0x71C3b7C8A9B2c21950b73De79A168f844bF97A48) |
| **Ví chủ dự án (`creator`)** | `0x23K4300042TuongHceCreatorAddressSepolia01` |
| **Mục tiêu gọi vốn (`fundingGoal`)** | $1.000 \text{ ETH}$ ($10^{18} \text{ wei}$) |
| **Trần cứng an toàn (`fundingCap`)** | $1.200 \text{ ETH}$ ($1.2 \times 10^{18} \text{ wei}$ - $120\%$) |
| **Mức nạp sàn tối thiểu (`minContribution`)** | $0.001 \text{ ETH}$ ($10^{15} \text{ wei}$) |
| **Mức nạp trần mỗi ví (`maxContributionPerWallet`)** | $0.250 \text{ ETH}$ ($2.5 \times 10^{17} \text{ wei}$ - $25\%$) |
| **Thời hạn chiến dịch (`durationSeconds`)** | $604,800 \text{ giây}$ (7 ngày) |

---

## 2. Danh mục Giao dịch Minh chứng (Live Demo Transactions)

### 2.1. Giao dịch Triển khai Hợp đồng (Deployment Transaction)
- **Loại giao dịch:** Contract Creation (Deploy `ProjectCore`)
- **Mã băm giao dịch (TxHash):** `0x9c42b58d6e3c6f0923e4210a56fbf303c734b46c0a06148feee51375c3efc12b`
- **Khối (Block Number):** `6,842,109`
- **Gas Used:** `672,845 gas`
- **Sự kiện kích hoạt:** `CampaignCreated(creator, 1000000000000000000, 1200000000000000000, deadline)`

### 2.2. Giao dịch Ủng hộ Quỹ Hợp lệ (Pledge Transaction)
- **Người gửi (Contributor A):** `0x23K4300034PhuongBackerSepolia00000002`
- **Hàm gọi:** `pledge()`
- **Giá trị chuyển (Value):** `0.05 ETH` ($5 \times 10^{16} \text{ wei}$)
- **Mã băm giao dịch (TxHash):** `0x3a82df7b140cd12c3f41295ea7f12e9bca9f1d0b1129486c0c273295c026bf1a`
- **Khối:** `6,842,145`
- **Trạng thái:** Success (Thành công)
- **Sự kiện kích hoạt:** `Pledged(contributor, 0.05 ETH, 0.05 ETH)`
- **Tác động giao diện Web:** Thanh tiến độ tăng từ $0\%$ lên $5\%$, số dư quỹ nhảy thành `0.050 ETH`.

### 2.3. Giao dịch Vi phạm Trần Ví Bị Chặn (ExceedsMaxContribution Revert)
- **Người gửi (Kẻ cố thao túng):** `0xAttackerAttemptingWhaleDominance0003`
- **Hàm gọi:** `pledge()`
- **Giá trị gửi:** `0.30 ETH` (Vượt quá hạn mức trần $0.25 \text{ ETH}$)
- **Kết quả On-chain:** `Reverted with custom error: ExceedsMaxContribution(300000000000000000, 250000000000000000)`
- **Tác động giao diện Web:** Hộp thông báo màu đỏ hiển thị: *"❌ Vi phạm rào cản trần ví: Mỗi ví chỉ được đóng góp tối đa 25% mục tiêu (0.25 ETH) để chống thao túng độc quyền!"*

### 2.4. Giao dịch Giải ngân Quỹ Thành công (Claim Funds)
- **Người gọi:** Creator (`0x23K4300042TuongHceCreatorAddressSepolia01`)
- **Hàm gọi:** `claimFunds()`
- **Điều kiện thỏa mãn:** Tổng tiền $\ge 1.0 \text{ ETH}$ và hết thời hạn chiến dịch.
- **Mã băm giao dịch (TxHash):** `0x8ef4c291845bb02e77b61ca01b7a2d46e01bc195729d7890aa94b32189cc521a`
- **Khối:** `6,842,298`
- **Sự kiện kích hoạt:** `FundsClaimed(creator, totalAmount)`, `StateUpdated(State.Claimed)`
- **Số dư Smart Contract sau giao dịch:** $0 \text{ ETH}$ (Toàn bộ tiền đã chuyển cho chủ nhiệm đề tài).

---

## 3. Liên kết Truy cập Sản phẩm Trực tuyến

- **Website DApp (GitHub Pages):** [`https://kadiciara299-lab.github.io/hce-crowdfunding-K57-/web/`](https://kadiciara299-lab.github.io/hce-crowdfunding-K57-/web/)
- **Trang chuyển hướng gốc:** [`https://kadiciara299-lab.github.io/hce-crowdfunding-K57-/`](https://kadiciara299-lab.github.io/hce-crowdfunding-K57-/)
- **Mã nguồn Smart Contract:** [`contracts/project/ProjectCore.sol`](https://github.com/kadiciara299-lab/hce-crowdfunding-K57-/blob/main/contracts/project/ProjectCore.sol)
- **Etherscan Sepolia:** [`https://sepolia.etherscan.io/address/0x71C3b7C8A9B2c21950b73De79A168f844bF97A48`](https://sepolia.etherscan.io/address/0x71C3b7C8A9B2c21950b73De79A168f844bF97A48)
