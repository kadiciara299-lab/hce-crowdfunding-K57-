# NHẬT KÝ LÀM VIỆC VỚI AI & RÀ SOÁT AN TOÀN HỢP ĐỒNG

- **Dự án:** Nền tảng gây quỹ có hoàn tiền (Topic #5: HCE Student Crowdfund)
- **Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)
- **Kho mã nguồn:** [`hce-crowdfunding-K57-`](https://github.com/kadiciara299-lab/hce-crowdfunding-K57-)
- **Thành viên thực hiện:**
  - **Hoàng Mạnh Tường** (23K4300042) — Phụ trách Kiểm thử an toàn, BA & Audit
  - **Nguyễn Nguyên Phương** (23K4300034) — Phụ trách Hợp đồng & Frontend DApp

---

## PHẦN 1: NHẬT KÝ LÀM VIỆC VỚI AI — LAB 8

### Lần 1: Phản biện mô hình kinh tế v0.1 (Prompt chuẩn I.6)
- **Prompt:**
  "Bạn là người dùng thận trọng. Chỉ dựa trên SPEC và ECONOMIC_RULES dưới đây, hãy nêu 5 cách một người có thể lạm dụng quy tắc hoặc làm người khác bị thiệt. Với mỗi cách, chỉ rõ quy tắc nào chưa đủ chặt. Không viết mã.
  [Dán nội dung SPEC.md và ECONOMIC_RULES.md]"

- **AI trả về (Tóm tắt 5 điểm):**
  1. *Lạm dụng 1:* Chủ dự án tự dùng ví phụ của mình nộp tiền vào phút cuối để ép dự án vượt chỉ tiêu, sau đó rút sạch tiền của những sinh viên khác (Self-pledge Rug Pull).
  2. *Lạm dụng 2:* Dự án đạt mục tiêu nhưng chủ dự án làm mất khóa ví hoặc bỏ mặc dự án, tiền bị kẹt vĩnh viễn không có cơ chế thoát hiểm (Fund Lockup).
  3. *Lạm dụng 3:* Không có trần tối đa (Hard cap) khiến số tiền nộp vượt mức quá lớn mà không có kế hoạch giải trình chi tiêu (Unlimited Oversubscription).
  4. *Lạm dụng 4:* Tiền được giải ngân toàn bộ một lần, chủ dự án ôm tiền biến mất mà không làm sản phẩm (Post-funding Abandonment).
  5. *Lạm dụng 5:* Nếu người đóng góp nạp tiền qua ví hợp đồng không có hàm `receive()`, khi gọi `claimRefund()` giao dịch sẽ bị Revert làm kẹt tiền (Smart Contract Incompatibility).

- **Đánh giá:** ✅ Dùng được rất tốt, chỉ ra đúng các lỗ hổng rủi ro kinh tế thực tế.
- **Cách sửa của nhóm:**
  - Khóa trần góp vốn mỗi ví tối đa 25% mục tiêu để ngăn một người tự thao túng.
  - Bổ sung điều khoản ân hạn 90 ngày sau hạn chót để mở cơ chế hoàn tiền thoát hiểm nếu chủ dự án bỏ rơi.
  - Cài đặt trần cứng Hard Cap 120% mục tiêu ban đầu.
  - Áp dụng mô hình Pull over Push và chuyển tiền bằng `call{value: ...}("")` có kiểm tra kết quả trả về.
  - Chấp nhận rủi ro số 4 cho bản v0.1 vì phạm vi bài Lab yêu cầu giữ đơn giản (dưới 150 dòng mã), đưa cơ chế Milestone Escrow vào lộ trình Lab 11–15.
- **Ai phát hiện:** Sinh viên định hướng câu hỏi, AI chỉ ra các kịch bản ngoại biên.

---

## PHẦN 2: NHẬT KÝ TƯƠNG TÁC AI & AUDIT HỢP ĐỒNG — LAB 10

### 1. Rà soát an toàn mẫu luyện tập `VaultBuggy.sol`
- **Prompt:**
  "Bạn là kiểm toán viên hợp đồng thông minh. Rà soát hợp đồng VaultBuggy dưới đây và liệt kê mọi lỗ hổng, xếp theo mức nghiêm trọng. Với mỗi lỗ hổng, nêu: dòng số mấy, khai thác thế nào, sửa ra sao.
  [Dán mã nguồn VaultBuggy.sol]"

- **Phản hồi của AI:**
  AI nhận diện được 2 lỗi:
  1. Dấu so sánh hàm `withdraw()` bị ngược: `block.timestamp <= unlockTime` (cho rút trước hạn, khóa sau hạn).
  2. Hàm `withdraw()` thiếu phân quyền (bất kỳ ai cũng gọi được).

- **Sinh viên đối chiếu & Bổ sung:**
  Sinh viên độc lập phát hiện thêm 2 lỗi mà AI ban đầu bỏ qua:
  3. Biến `emergencyPin` khai báo `private` ở ô nhớ thứ 2 (Slot 2) vẫn bị đọc trọn vẹn bằng lệnh RPC `eth_getStorageAt`.
  4. Lệnh `transfer()` giới hạn cứng 2.300 gas vi phạm quy ước `AGENTS.md`, gây lỗi DoS nếu ví người nhận là Smart Contract, đồng thời thiếu phát `event`.

---

### 2. Bảng phân loại 4 lỗi bắt buộc theo chuẩn Sổ tay thực hành ECO2432 (Trang 25)

| Lỗi | Mô tả lỗi | Ai phát hiện | Cách khắc phục |
| :-: | :--- | :---: | :--- |
| **1** | **Lộ mã PIN qua Storage Slot 2:** Biến `emergencyPin` khai báo `private` nhưng vẫn bị đọc trộm dạng bản rõ qua RPC `eth_getStorageAt(contract, "0x2", "latest")`. | **Sinh viên phát hiện** | Không lưu trữ bí mật dạng bản rõ on-chain. Dùng mã băm mật mã `keccak256(pin + salt)` nếu cần xác thực. |
| **2** | **Điều kiện thời gian khóa bị ngược:** `require(block.timestamp <= unlockTime)` làm két cho rút tiền trước hạn nhưng khóa vĩnh viễn sau hạn. | **AI phát hiện** | Sửa thành `block.timestamp >= unlockTime` và chuyển sang Custom Error `error StillLocked(...)`. |
| **3** | **Hàm rút tiền thiếu phân quyền:** Hàm `withdraw()` trong `VaultBuggy.sol` không kiểm tra `msg.sender == owner`, ai cũng rút cạn tiền được. | **AI phát hiện** | Thêm điều kiện kiểm tra chủ sở hữu: `if (msg.sender != owner) revert NotOwner();`. |
| **4** | **Lệnh `transfer` cứng 2.300 gas & Vi phạm CEI:** Dùng `transfer()` gây lỗi DoS với ví hợp đồng thông minh, không cập nhật trạng thái trước khi gửi và không phát `event`. | **Sinh viên phát hiện** *(Được cộng điểm)* | Đổi sang `call{value: balance}("")` kèm kiểm tra kết quả trả về, tuân thủ nghiêm ngặt Checks-Effects-Interactions và phát `emit Withdrawn(...)`. |

---

### 3. Rà soát và Vá lỗi hợp đồng chính `ProjectCore.sol`
- **Mục tiêu:** Kiểm tra chéo hợp đồng dự án của nhóm theo đặc tả `docs/SPEC.md`.
- **Phát hiện 1 (Logic thời gian trong `claimFunds`):**
  - *Hiện tượng:* Biểu thức `if (block.timestamp < deadline && totalRaised < fundingGoal)` cho phép Creator rút tiền TRƯỚC hạn chót nếu gom đủ vốn, tiềm ẩn rủi ro Early Rug Pull.
  - *Sửa đổi:* Khóa cứng `if (block.timestamp < deadline) revert CampaignStillActive(deadline - block.timestamp);`. Bắt buộc phải qua hạn chót mới được giải ngân.
- **Phát hiện 2 (Nguy cơ Deadlock cấu hình):**
  - *Hiện tượng:* Nếu `_goalInWei` quá nhỏ khiến `maxContributionPerWallet < minContribution`, không ai có thể nạp tiền được vì nạp tối thiểu đã vượt trần.
  - *Sửa đổi:* Bổ sung kiểm tra trong constructor: `if (maxContributionPerWallet < minContribution) revert InvalidGoal();`.
- **Ai phát hiện:** Sinh viên phát hiện khi đối chiếu ràng buộc toán học và quy tắc nghiệp vụ `SPEC.md`.

---

## KẾT LUẬN
Quá trình rà soát tại Lab 10 chứng minh tầm quan trọng của việc hiểu sâu bản chất EVM và logic nghiệp vụ. Công cụ AI hỗ trợ rất tốt trong việc quét cú pháp và lỗi thường gặp, nhưng các lỗi liên quan đến kiến trúc lưu trữ (`Storage Layout`) và rủi ro kinh tế tinh vi đòi hỏi sinh viên phải trực tiếp làm chủ và đối chiếu.
