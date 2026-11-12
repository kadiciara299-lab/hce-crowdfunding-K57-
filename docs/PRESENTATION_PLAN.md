# KỊCH BẢN TRÌNH BÀY NHÓM (5 PHÚT) — CỔNG GÂY QUỸ HOÀN TIỀN K57

## 1. Phân công trình bày và Artifact phụ trách
| Thời lượng | Thành viên phụ trách | Nội dung trình bày | Bằng chứng mở trực tiếp |
| :--- | :--- | :--- | :--- |
| **0:00 – 1:15** | Nguyễn Nguyên Phương | Bài toán thực tế, quy tắc kinh tế hoàn tiền và kiến trúc hợp đồng `ProjectCore.sol`. | `README.md`, `docs/SPEC.md`, `docs/ECONOMIC_RULES.md` |
| **1:15 – 2:30** | Hoàng Mạnh Tường | Quy trình rà soát an toàn: chống tấn công Reentrancy và xử lý kết quả Cross-Audit. | `contracts/project/ProjectCore.sol`, `docs/AUDIT_REPORT.md` |
| **2:30 – 4:00** | Nguyễn Nguyên Phương | Demo trực tiếp DApp trên Sepolia: kết nối MetaMask, góp quỹ `0.002 ETH`, đối chiếu Etherscan và thử ca vi phạm. | URL GitHub Pages (`web/index.html`), Sepolia Etherscan |
| **4:00 – 5:00** | Hoàng Mạnh Tường | Tổng kết chi phí gas thực tế, các lỗi AI đã phát hiện và hướng mở rộng. | `docs/AI_JOURNAL.md`, `evidence/` |

## 2. Kịch bản Demo trực tiếp (Live Demo Checklist)
1. Mở đường dẫn công khai GitHub Pages trên trình duyệt.
2. Kết nối ví MetaMask mạng Sepolia (`0xaA08C...A54f7`), xác nhận mục tiêu `0.01 ETH` và thời hạn `48 giờ`.
3. Gửi giao dịch ủng hộ `0.002 ETH` $\rightarrow$ nhận mã băm giao dịch (`TxHash`) và kiểm tra số dư đã huy động tăng lên.
4. Thử bấm **Giải ngân (`claimFunds`)** khi chưa đạt mục tiêu $\rightarrow$ giao diện bắt và hiển thị rõ lỗi `GoalNotReached`.
