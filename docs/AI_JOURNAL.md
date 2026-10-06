# NHẬT KÝ LÀM VIỆC VỚI AI - ECO2432

## Lab 4: Nhận diện hợp đồng có rủi ro

**Prompt:** Bạn là chuyên viên thẩm định rủi ro tài sản số. Dưới đây là mã nguồn một hợp đồng token. Hãy liệt kê mọi quyền đặc biệt mà chủ sở hữu hợp đồng có thể thực hiện, và với mỗi quyền, nêu rõ:
- Tên hàm và số dòng
- Người nắm giữ token chịu rủi ro gì
Chỉ trả lời dựa trên mã nguồn tôi cung cấp. Nếu không tìm thấy, nói là không tìm thấy.
[dán mã nguồn]

**AI trả về:** Phân tích và thẩm định rủi ro 3 hợp đồng trong `ClubTokens.sol`:
- **ClubTokenA:** An toàn — Không tìm thấy quyền đặc biệt nào của admin; hợp đồng không kế thừa `Ownable`, tổng cung 1.000.000 CTA cố định từ lúc khởi tạo.
- **ClubTokenB:** Rủi ro cao — Hàm `mint(address,uint256)` tại dòng 18–20 cho phép chủ sở hữu (`onlyOwner`) đúc token không giới hạn, gây nguy cơ lạm phát vô hạn và xả hàng (rug pull).
- **ClubTokenC:** Rủi ro cao — Hàm `setRestricted(address,bool)` tại dòng 30–32 kết hợp kiểm tra ở `_update` dòng 34–37 cho phép chủ sở hữu đưa ví vào danh sách đen/đóng băng chiều gửi đi, biến token thành bẫy không thể bán (honeypot).

**Đánh giá:** ✅ Dùng được

**Chỗ sai:** AI ban đầu chỉ ra hàm `setRestricted` nhưng cần chú ý cơ chế chặn thực tế nằm bên trong hàm ghi đè `_update` (dòng 34–37) theo chuẩn OpenZeppelin 5.x.

**Cách sửa:** Sinh viên đối chiếu lại số dòng và bổ sung phân tích hàm `_update` dòng 34–37 để làm rõ cơ chế chặn chuyển nhượng.

**Ai phát hiện:** Sinh viên phát hiện

---

## Lab 6: Sinh mã phân tích dòng tiền ví và kiểm tra kết quả

### Lần 1 — Kiểm tra phiên bản API Etherscan (Mục 6)
**Prompt:** Đọc tệp SPEC.md trong dự án và viết chương trình Python thực hiện đúng đặc tả đó. Tuân thủ các quy ước trong AGENTS.md.
**AI trả về:** Sinh mã chương trình `wallet_analyzer.py` sử dụng thư viện `requests` và endpoint Etherscan v1 truyền thống (`https://api.etherscan.io/api`).
**Đánh giá:** ⚠️ Phải sửa
**Chỗ sai:** 
1. Thư viện `requests` gây lỗi `ModuleNotFoundError: No module named 'requests'` trên môi trường Python mặc định của máy chưa cài gói ngoài.
2. Dùng endpoint v1 cũ thiếu tham số `chainid`, dẫn tới lỗi hoặc timeout khi truy vấn mạng Sepolia (mạng thực hành của môn học).
**Cách sửa:** 
1. Chuyển sang sử dụng thư viện chuẩn tích hợp sẵn `urllib.request` và `json` để chạy độc lập không phụ thuộc `pip`.
2. Chuyển sang chuẩn Etherscan API v2 đa chuỗi (`https://api.etherscan.io/v2/api?chainid=11155111`) theo đúng tài liệu Etherscan Developer API mới nhất.
**Ai phát hiện:** Sinh viên phát hiện

---

### Lần 2 — Kiểm tra xử lý phí gas cho giao dịch đến bị lỗi (Mục 4)
**Prompt:** Viết hàm tính toán biến động số dư cho các giao dịch vào và ra theo quy tắc R1-R4 trong SPEC.md.
**AI trả về:** Hàm xử lý kiểm tra `isError == "1"` nhưng ban đầu áp dụng trừ phí gas cho tất cả các giao dịch lỗi mà không phân biệt ví mục tiêu là người gửi (`from`) hay người nhận (`to`).
**Đánh giá:** ⚠️ Phải sửa
**Chỗ sai:** Khi có một giao dịch gửi tiền ĐẾN ví mục tiêu (`to == target`) bị thất bại, người phải trả phí gas là bên gửi (`from`), ví nhận không bị trừ tiền hay phí. Việc trừ phí gas của ví nhận là sai quy tắc hoạt động on-chain.
**Cách sửa:** Sinh viên sửa lại logic trong hàm `parse_and_calculate_cash_flow`: chỉ trừ phí gas khi `from == target`. Đối với `to == target` mà giao dịch lỗi thì ghi nhận `net_impact = 0`.
**Ai phát hiện:** Sinh viên phát hiện
