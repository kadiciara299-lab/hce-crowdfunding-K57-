# PROJECT PLAN
Nền tảng Gây quỹ có hoàn tiền cho Dự án Sinh viên (Student Refundable Crowdfunding)

## 1. Thành viên và vai trò
| Họ và tên | Mã sinh viên | Vai chính Lab 8-11 | Vai chính Lab 12-15 |
| :--- | :--- | :--- | :--- |
| Hoàng Mạnh Tường | 23K4300042 | Trưởng nhóm / Hợp đồng lõi | Kiểm thử an toàn & Hardening |
| Nguyễn Nguyên Phương | 23K4300034 | Đặc tả nghiệp vụ (BA) & Tài liệu | Giao diện Web DApp & Triển khai |

*(Quy ước: Các thành viên hoán đổi vai trò giữa 2 giai đoạn theo đúng yêu cầu sổ tay).*

## 2. Người dùng và vấn đề
- **Người dùng chính:** 
  1. *Chủ dự án (Admin / Sinh viên khởi xướng):* Cần huy động vốn ban đầu để tổ chức sự kiện, nghiên cứu khoa học hoặc sản phẩm khởi nghiệp.
  2. *Người đóng góp (Sinh viên / Nhà tài trợ):* Muốn ủng hộ vốn nhưng e ngại dự án không thu hút đủ tiền để triển khai và không được hoàn lại tiền.
- **Vấn đề cần giải quyết:** Loại bỏ rủi ro chủ dự án "ôm tiền" bỏ trốn khi không huy động đủ ngân sách thực thi. Hợp đồng thông minh giữ tiền độc lập và tự động hoàn trả.
- **Sản phẩm cuối nhìn thấy được:** Một DApp công khai (Web kết nối ví MetaMask) cho phép nộp ETH, theo dõi tiến độ thời gian thực, chủ dự án rút tiền khi thành công hoặc người góp bấm nút hoàn tiền khi hết hạn mà không đạt mục tiêu.

## 3. Mốc bắt buộc
- **Lab 8:** Khởi tạo codebase nhóm, chốt PROJECT_PLAN, SPEC v0.1, ECONOMIC_RULES v0.1.
- **Lab 9:** Contract lõi `ProjectCore.sol` biên dịch và chạy được chu trình trên Remix VM.
- **Lab 10:** Audit hợp đồng bằng AI và thủ công, sửa lỗi bảo mật.
- **Lab 11:** Cài đặt quy tắc kinh tế vào contract, kiểm thử luồng hợp lệ và vi phạm.
- **Lab 12:** Gate Review 1 (Duyệt codebase và bảo vệ phạm vi).
- **Lab 13:** Kiểm thử tấn công Reentrancy và hardening dòng lệnh theo CEI.
- **Lab 14:** Tham gia rà soát chéo (audit chéo) với nhóm bạn.
- **Lab 15:** Triển khai giao diện Web DApp lên GitHub Pages và công bố link trực tuyến.