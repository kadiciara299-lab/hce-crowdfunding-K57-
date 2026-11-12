# BÁO CÁO RÀ SOÁT CHÉO — Nhóm K57 Crowdfunding

## Tóm tắt
Đã rà soát tệp `contracts/project/ProjectCore.sol` (79 dòng) đối chiếu với `docs/SPEC.md`. Phát hiện 2 vấn đề: 0 nghiêm trọng, 1 trung bình, 1 nhẹ[cite: 6].

## Phát hiện 1 — Thiếu kiểm tra tham số đầu vào khi khởi tạo chiến dịch
- **Mức độ:** Trung bình[cite: 6]
- **Vị trí:** Dòng 31–35, hàm `constructor(uint256 _targetAmountWei, uint256 _durationSeconds)`[cite: 6]
- **Mô tả:** Hợp đồng không kiểm tra `_targetAmountWei > 0` và `_durationSeconds > 0` khi triển khai[cite: 6].
- **Tình huống gây thiệt hại:** Nếu người tạo chiến dịch vô tình truyền mục tiêu bằng 0 hoặc thời gian bằng 0, chiến dịch sẽ kết thúc ngay lập tức hoặc đạt mục tiêu ở mức 0 ETH, làm vô hiệu hóa cơ chế hoàn tiền `claimRefund()` cho người đóng góp[cite: 6].
- **Khuyến nghị:** Thêm điều kiện chặn `if (_targetAmountWei == 0 || _durationSeconds == 0) revert InvalidParameters();` ngay đầu `constructor`[cite: 6].
- **Ai phát hiện:** Thành viên nhóm rà soát chéo[cite: 6].

## Phát hiện 2 — Cho phép đóng góp thêm sau khi quỹ đã giải ngân
- **Mức độ:** Nhẹ[cite: 6]
- **Vị trí:** Dòng 37–48, hàm `contribute()`[cite: 6]
- **Mô tả:** Khi dự án đạt mục tiêu sớm và chủ dự án đã rút vốn (`fundsWithdrawn == true`), hàm `contribute()` vẫn nhận tiền nếu chưa hết `deadline`[cite: 6].
- **Tình huống gây thiệt hại:** Nếu người dùng gửi tiền sau thời điểm chủ dự án đã gọi `withdrawFunds()`, số tiền này sẽ bị khóa vĩnh viễn trong hợp đồng vì chủ dự án không thể rút lần hai và người gửi cũng không thể hoàn tiền do chiến dịch đã đạt mục tiêu[cite: 6].
- **Khuyến nghị:** Thêm chốt chặn `if (fundsWithdrawn) revert AlreadyWithdrawn();` trong hàm `contribute()`[cite: 6].
- **Ai phát hiện:** Công cụ AI kết hợp thành viên nhóm kiểm tra chéo[cite: 6].

## Phản hồi và xử lý của nhóm phát triển
- Nhóm đồng ý với cả 2 phát hiện trên và đã cập nhật mã nguồn vá lỗi trực tiếp trong `contracts/project/ProjectCore.sol`[cite: 6].
