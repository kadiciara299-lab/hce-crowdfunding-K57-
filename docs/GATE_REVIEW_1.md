# BIÊN BẢN GATE REVIEW 1 — DUYỆT CODEBASE VÀ PHẠM VI (LAB 12)

## 1. Thông tin nhóm và dự án
- Nhóm: K57 Crowdfunding (Chủ đề 5: Gây quỹ có hoàn tiền)
- Repo: `https://github.com/kadiciara299-lab/hce-crowdfunding-K57-`
- Hợp đồng kiểm tra: `contracts/project/ProjectCore.sol`

## 2. Kết luận của giảng viên
- [x] **Qua (Pass)** — Codebase đạt yêu cầu, luồng chính hoạt động ổn định.
- [ ] **Qua có điều kiện**
- [ ] **Thu hẹp phạm vi**

## 3. Ba việc bắt buộc sửa/hoàn thiện trước Lab 15
1. Giữ cấu trúc hợp đồng tinh gọn dưới 150 dòng, tập trung hoàn thiện luồng nạp - giải ngân - hoàn tiền.
2. Kiểm tra tính an toàn chống Reentrancy khi gọi hàm chuyển ETH ở `withdrawFunds` và `claimRefund`.
3. Bổ sung giao diện web tối giản kết nối ví MetaMask ở Lab 15.

## 4. Tính năng xác nhận cắt giảm (nếu có)
- Không phát hành token trung gian hay quản trị phức tạp; chỉ sử dụng ETH gốc để giữ luồng tiền đơn giản, minh bạch.

## 5. Hạn hoàn thành
- Trước buổi Lab 13.
