# BẢNG TỰ KIỂM TRA SỨC KHỎE REPOSITORY (HEALTH CHECK) — LAB 12

- **Dự án:** HCE Student Crowdfund (Chủ đề 5)
- **Ngày kiểm tra:** 15/10/2026
- **Thực hiện bởi:** Hoàng Mạnh Tường & Nguyễn Nguyên Phương
- **Kết quả tổng kết:** **5/5 TIÊU CHÍ ĐẠT 100% (READY FOR GATE REVIEW 1)**

---

## BẢNG ĐỐI CHIẾU 5 TIÊU CHÍ BẮT BUỘC

| # | Tiêu chí đánh giá | Trạng thái | Bằng chứng kiểm tra thực tế | Nhận xét chi tiết |
| :-: | :--- | :---: | :--- | :--- |
| **1** | **`README.md` nói rõ bài toán, người dùng và cách chạy** | ✅ **ĐẠT** | Tệp [`README.md`](../../README.md) | - Có câu định vị 1 câu theo chuẩn.<br>- Mô tả rõ nỗi đau người dùng: thất thoát tiền gây quỹ sinh viên.<br>- Hướng dẫn chi tiết cách biên dịch trên Remix và chạy DApp. |
| **2** | **`PROJECT_PLAN.md`, `SPEC.md`, `ECONOMIC_RULES.md` còn khớp với mã** | ✅ **ĐẠT** | Các tệp trong [`docs/`](../../docs/) và [`contracts/project/ProjectCore.sol`](../../contracts/project/ProjectCore.sol) | - R1–R8 trong `SPEC.md` khớp hoàn toàn với logic của `ProjectCore.sol`.<br>- 4 rào cản kinh tế trong `ECONOMIC_RULES.md` được cài đặt đầy đủ: `minContribution` (0.001 ETH), `maxContributionPerWallet` (25%), `fundingCap` (120%), và thời hạn 3–30 ngày. |
| **3** | **`ProjectCore.sol` biên dịch được** | ✅ **ĐẠT** | [`contracts/project/ProjectCore.sol`](../../contracts/project/ProjectCore.sol) | - Mã nguồn Solidity `^0.8.20` sạch lỗi.<br>- Kích thước **144 dòng**, thỏa mãn điều kiện < 150 dòng của Bộ lọc duyệt phạm vi Phần N Sổ tay ECO2432.<br>- Áp dụng triệt để Checks-Effects-Interactions, Custom Errors và chuyển tiền bằng `call{value}`. |
| **4** | **Có một ca hợp lệ và một ca gian lận/vi phạm bị chặn** | ✅ **ĐẠT** | [`test/test_gate_review.py`](../../test/test_gate_review.py) và [`evidence/lab-12/test_output.log`](./test_output.log) | - Ca hợp lệ: 4 sinh viên nạp 1.0 ETH $\rightarrow$ Đạt mục tiêu $\rightarrow$ Hết hạn $\rightarrow$ Chủ dự án giải ngân 1.0 ETH thành công.<br>- 4 Ca gian lận bị chặn: Nạp dưới sàn (Dust), Nạp vượt trần ví (Whale), Rút trước hạn chót, Kẻ lạ mạo danh rút tiền, và Rút kép hoàn tiền. |
| **5** | **Lịch sử commit có đóng góp của tất cả thành viên** | ✅ **ĐẠT** | Lịch sử Git commit trên nhánh `main` | - Thành viên 1: Hoàng Mạnh Tường (`@23k4300042-lang`) tham gia commit khởi tạo, đặc tả BA, kiểm thử và tài liệu.<br>- Thành viên 2: Nguyễn Nguyên Phương (`@kadiciara299-lab`) tham gia commit hợp đồng lõi, quy tắc kinh tế và tối ưu gas. |

---

## KẾT LUẬN CỦA NHÓM
Kho mã nguồn đã sẵn sàng 100% cho buổi Gate Review 1, không có tệp thừa, không dùng tệp ẩn ngoài repo, toàn bộ tài liệu và mã nguồn đồng nhất tuyệt đối.
