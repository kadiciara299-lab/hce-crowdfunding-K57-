# LAB 03 — BÁO CÁO PHÂN TÍCH ON-CHAIN TRÊN ETHERSCAN

**Transaction Hash:** `0xea02a3d7c76576fe56c8a87d5fc7bc77c7392bca7d3a5746b4646f8431756881`

## 1. Bảng giải thích chi tiết 10 trường giao dịch (Sepolia)

| Trường | Giá trị thực tế | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- |
| **Status** | Success (Thành công) | Xác nhận giao dịch đã ghi vào sổ cái. Giao dịch thất bại vẫn tốn phí |
| **Block** | 11772181 | Số thứ tự khối chứa giao dịch, dùng xác định thời điểm |
| **Timestamp** | Sep-24-2026 12:59:00 PM +UTC | Thời gian thực ghi nhận giao dịch (dùng hạch toán) |
| **From** | `0xaA08C3D4Cf35a9526268Fc53A9CE5724A9eA54f7` | Địa chỉ ví gửi |
| **To** | `0xb0aF0A8CF44113b0088E315f9f510464fC5060Bc` | Địa chỉ ví nhận |
| **Value** | 0.01 Sepolia ETH | Số tiền giao dịch |
| **Transaction Fee** | 0.000055009558485 ETH | Chi phí giao dịch thực tế trả cho thợ đào/validator |
| **Gas Price** | 2.619502785 Gwei | Đơn giá gas tại thời điểm gửi lệnh |
| **Gas Limit** | 31,500 | Mức gas tối đa cho phép tiêu thụ |
| **Gas Used** | 21,000 (66.67%) | Lượng gas thực tế đã sử dụng |
| **Nonce** | 40 | Số thứ tự giao dịch của ví gửi |

## 2. Phân tích Tab Contract (Đọc hợp đồng thông minh trên Etherscan)

| Thành phần | Đặc điểm & Khái niệm | Ý nghĩa nghiệp vụ & Lưu ý |
| :--- | :--- | :--- |
| **Bytecode** | Chuỗi mã máy thực thi (dạng opcode hex), con người không thể đọc trực tiếp được. | Là mã nhị phân được biên dịch và lưu trữ trực tiếp trên EVM (Ethereum Virtual Machine). |
| **Source Code (verified)** | Mã nguồn (Solidity) công khai do dự án đăng tải, đã được Etherscan xác thực khớp 100% với Bytecode. | Giúp kiểm toán logic và tính minh bạch của hợp đồng.<br>*(Lưu ý đối với USDC: Đây là mẫu **Proxy Contract (EIP-1967)**, cần xem ở tab con **Read as Proxy** / **Write as Proxy** để đọc đúng logic token gốc).* |
| **Tab Read Contract** | Chứa các hàm chỉ truy vấn/đọc trạng thái dữ liệu (view/pure functions như `totalSupply()`, `balanceOf()`). | **Không tốn phí gas** và **không cần kết nối ví Web3**. Bất kỳ ai cũng có thể đọc dữ liệu công khai trên blockchain (ví dụ: bấm gọi hàm `totalSupply()`). |
| **Tab Write Contract** | Chứa các hàm làm thay đổi trạng thái/dữ liệu trên blockchain (như `transfer()`, `approve()`). | **Tốn phí gas** và **bắt buộc phải kết nối ví Web3 & ký giao dịch** để thực hiện ghi dữ liệu lên mạng lưới. |

