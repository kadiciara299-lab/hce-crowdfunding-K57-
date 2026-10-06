# NHẬT KÝ LÀM VIỆC VỚI AI - LAB 8

## Lần 1: Phản biện mô hình kinh tế v0.1
- **Prompt:**
  "Bạn là người dùng thận trọng. Chỉ dựa trên SPEC và ECONOMIC_RULES dưới đây, hãy nêu 5 cách một người có thể lạm dụng quy tắc hoặc làm người khác bị thiệt. Với mỗi cách, chỉ rõ quy tắc nào chưa đủ chặt. Không viết mã.
  [Dán nội dung SPEC.md và ECONOMIC_RULES.md]"

- **AI trả về (Tóm tắt):**
  1. *Lạm dụng số 1:* Chủ dự án tự dùng ví phụ của mình nộp tiền ảo vào phút cuối để ép dự án vượt chỉ tiêu, sau đó rút sạch tiền của những sinh viên khác.
  2. *Lạm dụng số 2:* Nếu một người nộp tiền thông qua hợp đồng trung gian không có hàm nhận tiền (hàm `receive()` hoặc `fallback()`), khi gọi `claimRefund()` giao dịch sẽ bị lỗi Revert vĩnh viễn làm kẹt tiền.
  3. *Lạm dụng số 3:* Không có trần tối đa (Hard cap) khiến số tiền nộp vượt mức quá lớn mà không có kế hoạch giải trình chi tiêu.
  4. *Lạm dụng số 4:* Người dùng nhập sai số tiền quyên góp quá lớn do không có chức năng xác nhận lại.
  5. *Lạm dụng số 5:* Dự án thành công nhưng chủ dự án không triển khai sản phẩm thực tế ngoài đời vì tiền đã được rút sạch một lần (thiếu cơ chế giải ngân theo mốc).

- **Đánh giá:** Rất hữu ích, chỉ ra đúng các lỗ hổng rủi ro kinh tế thực tế.
- **Cách sửa của nhóm:**
  - Chấp nhận rủi ro số 5 cho bản v0.1 vì phạm vi bài Lab 8 yêu cầu giữ đơn giản (dưới 150 dòng mã).
  - Bổ sung quy tắc Checks-Effects-Interactions và sử dụng `.call{value: ...}("")` có kiểm tra kết quả trả về để hạn chế lỗi kẹt giao dịch ở mục số 2.
  - Bổ sung vào kịch bản kiểm thử ở Lab 13 cho ca gian lận tự góp tiền để hợp thức hóa rút quỹ.
- **Ai phát hiện:** Sinh viên định hướng câu hỏi, AI chỉ ra các kịch bản ngoại biên.