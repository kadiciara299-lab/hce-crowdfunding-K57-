# NHẬT KÝ LÀM VIỆC VỚI AI — Lab 8: Thiết kế Quy tắc Kinh tế cho Sản phẩm

**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Nhóm sinh viên:** K57 Kinh Tế Số — Trường Đại học Kinh tế, Đại học Huế  
**Chủ đề:** Gây quỹ dự án sinh viên có hoàn tiền ([`hce-crowdfunding-K57-`](https://github.com/kadiciara299-lab/hce-crowdfunding-K57-))

---

## Lần 1 — Khởi tạo Mô hình Kinh tế & Phát hiện Lỗi Push vs Pull Payment

**Prompt:**  
"Tôi đang thiết kế một hợp đồng gây quỹ cộng đồng cho sinh viên bằng Solidity 0.8.20. Khi chiến dịch thất bại (hết hạn mà không gom đủ mục tiêu), hãy viết một hàm để hợp đồng tự động gửi hoàn trả tiền lại cho tất cả những người đã từng đóng góp."

**AI trả về:**  
AI đã sinh một đoạn mã sử dụng một mảng `address[] public contributors` và trong hàm `refundAll()`, AI dùng vòng lặp `for (uint i = 0; i < contributors.length; i++)` để thực hiện lệnh chuyển ETH `payable(contributors[i]).transfer(...)` lần lượt cho từng người trong danh sách.

**Đánh giá:** ❌ Sai, bỏ (Phạm phải mẫu nguy hiểm nghiêm trọng trong lập trình Smart Contract)

**Chỗ sai:**  
1. **Lỗi vượt hạn mức Gas (Gas Limit DoS):** Nếu chiến dịch có số lượng người ủng hộ lớn (ví dụ: vài trăm đến hàng nghìn sinh viên), vòng lặp duyệt qua toàn bộ mảng sẽ tiêu tốn lượng gas vượt quá giới hạn gas của một block Ethereum (`Block Gas Limit` ~30M gas). Khi đó, giao dịch hoàn tiền sẽ **luôn luôn bị revert do hết gas (Out of Gas)**, dẫn tới toàn bộ số tiền bị kẹt vĩnh viễn trong hợp đồng và không ai nhận lại được tiền!
2. **Lỗi từ chối dịch vụ có chủ đích (DoS with Unexpected Revert):** Chỉ cần một địa chỉ ví người nhận trong mảng là một hợp đồng thông minh không có hàm `receive()` hoặc cố tình `revert`, toàn bộ giao dịch của vòng lặp sẽ bị dừng và hoàn tác, làm tê liệt việc hoàn tiền cho tất cả mọi người khác.
3. **Vi phạm quy ước `AGENTS.md`:** Dùng hàm cấm `transfer` thay vì cú pháp an toàn `call{value: ...}("")`.

**Cách sửa:**  
Sinh viên bác bỏ hoàn toàn thiết kế "Push Payment" của AI. Chuyển sang mô hình chuẩn công nghiệp **Pull over Push (Withdrawal Pattern)**: Hợp đồng KHÔNG bao giờ dùng vòng lặp để đẩy tiền. Thay vào đó, mỗi người ủng hộ tự chủ động kết nối ví và gọi hàm cá nhân `claimRefund()`. Ai gọi thì hợp đồng tính toán và hoàn tiền cho người đó. Phí gas của ai người đó trả, cô lập hoàn toàn rủi ro giữa các người dùng.

**Ai phát hiện:** Sinh viên phát hiện (Dựa trên kiến thức về Gas và giới hạn Block trong bài Lab 7).

---

## Lần 2 — Phản biện Mô hình Kinh tế (Sử dụng Prompt chuẩn I.6)

**Prompt (Mẫu I.6):**  
"Bạn là nhà đầu tư thận trọng đang xem xét dự án này. Dưới đây là mô tả quy tắc kinh tế của dự án HCE Student Crowdfund (Gây quỹ sinh viên có hoàn tiền). Hãy nêu 5 điểm yếu nghiêm trọng nhất, xếp theo mức rủi ro giảm dần. Với mỗi điểm, nêu một tình huống cụ thể mà người dùng bị thiệt hại. Không cần đề xuất giải pháp, tôi muốn nghe phần phê bình.  
[Nội dung SPEC.md và ECONOMIC_RULES.md]"

**AI trả về (Tóm tắt 5 phản biện):**  
1. *Rủi ro 1:* Chủ dự án tạo tài khoản phụ tự đóng góp phần còn thiếu sát giờ G để đạt 100% mục tiêu, sau đó rút sạch tiền của những người ủng hộ thật (Self-pledge Rug Pull).
2. *Rủi ro 2:* Chủ dự án cài đặt thời hạn chiến dịch quá dài (ví dụ: vài năm) khiến tiền của sinh viên bị phong tỏa, không thể kích hoạt hoàn tiền.
3. *Rủi ro 3:* Không có mức đóng góp sàn, kẻ phá hoại có thể gửi hàng nghìn giao dịch siêu nhỏ để spam rác dữ liệu on-chain.
4. *Rủi ro 4:* Nếu chiến dịch thất bại nhưng chủ dự án không kích hoạt kết thúc thì người dùng có bị giam tiền không?
5. *Rủi ro 5:* Lỗ hổng tái nhập (Reentrancy) khi người dùng gọi hàm rút tiền hoàn trả.

**Đánh giá:** ✅ Dùng được rất tốt (Cung cấp các góc nhìn phòng vệ kinh tế và bảo mật sâu sắc).

**Chỗ cần hoàn thiện và Quyết định của nhóm:**  
- **Về Rủi ro 1 (Self-pledge):** Nhóm chấp nhận đây là rủi ro kinh tế của mô hình All-or-Nothing. Tuy nhiên, kẻ gian phải chịu rủi ro chôn vốn thật của chính mình. Nhóm quyết định bổ sung cơ chế định danh Off-chain thông qua email sinh viên `@hce.edu.vn` để ràng buộc trách nhiệm pháp lý thực tế.
- **Về Rủi ro 2 (Thời hạn vô lý):** Nhóm bổ sung quy tắc khóa cứng trong hợp đồng: thời gian chiến dịch tối thiểu 3 ngày, tối đa 30 ngày. Không ai có thể thiết lập ngoài khoảng này.
- **Về Rủi ro 3 (Spam bụi):** Đặt ngưỡng `minContribution = 0.001 ETH`.
- **Về Rủi ro 4 (Chủ quan Creator):** Logic chuyển trạng thái hoàn tiền được viết dựa trên thời gian khối `block.timestamp > deadline` mà không cần phụ thuộc vào bất kỳ hàm bấm nút nào của Creator.
- **Về Rủi ro 5 (Reentrancy):** Áp dụng nghiêm ngặt mẫu Checks-Effects-Interactions (trừ số dư `contributions[msg.sender] = 0` trước khi `call{value: ...}("")`).

**Ai phát hiện:** Công cụ AI nêu phản biện sắc bén $\rightarrow$ Nhóm sinh viên thảo luận, quyết định chính sách kinh tế và giải pháp kỹ thuật cụ thể.

---

## Lần 3 — Rà soát Quy ước AGENTS.md khi thiết kế Hợp đồng lõi

**Prompt:**  
"Hãy viết khung hợp đồng Solidity cho dự án Gây quỹ có hoàn tiền theo đặc tả trên. Hãy dùng modifier `onlyOwner` và hàm `transfer` để chuyển tiền."

**AI trả về:**  
AI đã sinh mã sử dụng cú pháp cũ:
```solidity
payable(msg.sender).transfer(amount);
```
và sử dụng chuỗi lỗi dài:
```solidity
require(block.timestamp >= deadline, "Chien dich chua ket thuc, khong the rut tien");
```

**Đánh giá:** ❌ Sai, vi phạm quy ước nội bộ `AGENTS.md`

**Chỗ sai:**  
1. Vi phạm Điều 4 trong `AGENTS.md`: "Chuyển ETH bằng `call{value: ...}("")` và kiểm tra kết quả; không dùng `transfer`." Hàm `transfer` bị gán cứng giới hạn 2,300 gas, sẽ bị lỗi nếu ví nhận là Smart Contract Wallet (như Safe hoặc ví sinh viên dùng Account Abstraction).
2. Vi phạm Điều 5 trong `AGENTS.md`: "Dùng `error` tùy biến thay cho chuỗi thông báo dài trong `require`." Chuỗi lỗi string dài làm tăng kích thước bytecode của contract và tiêu tốn gas của người dùng khi deploy và revert.
3. Không phát sự kiện `event` khi thay đổi trạng thái theo Điều 1 của `AGENTS.md`.

**Cách sửa:**  
Sinh viên chủ động yêu cầu AI tuân thủ tuyệt đối `AGENTS.md`:
- Đổi toàn bộ chuỗi require sang `custom error` kèm tham số: `revert CampaignStillActive(deadline - block.timestamp);`.
- Đổi lệnh chuyển tiền sang: `(bool ok, ) = payable(recipient).call{value: amount}(""); require(ok, "Transfer failed");`.
- Bổ sung phát `emit RefundClaimed(...)` và `emit FundsClaimed(...)`.

**Ai phát hiện:** Sinh viên phát hiện (Đối chiếu trực tiếp với tệp quy ước `AGENTS.md`).

---

## Lần 4 — Rà soát An toàn Reentrancy theo Lối đặt Câu hỏi Dẫn dắt (Lab 13 - Mẫu I.4)

**Prompt (Mẫu I.4 chuẩn Sổ tay thực hành):**  
"Bạn là kiểm toán viên hợp đồng thông minh.  
Đừng đưa mã sửa ngay. Hãy giải thích từng bước điều gì xảy ra khi hàm withdraw() dưới đây được gọi bởi một hợp đồng có hàm receive().  
Sau đó nêu 2 cách khắc phục và so sánh ưu nhược điểm của từng cách.  
[Mã nguồn VulnerableBank.sol]"

**AI trả về (Tóm tắt):**  
1. **Phân tích cơ chế tái nhập (Reentrancy Callback Loop):**  
   - Bước 1: Kẻ tấn công gọi `withdraw()`, hàm kiểm tra `balance > 0` thành công.  
   - Bước 2: Hợp đồng gửi ETH bằng lệnh `call{value: balance}("")`. Khi địa chỉ nhận là contract, EVM tự động chuyển giao quyền điều khiển sang hàm `receive()` của hợp đồng nhận.  
   - Bước 3: Trong `receive()`, kẻ tấn công viết lệnh gọi ngược lại chính hàm `withdraw()` của ngân hàng.  
   - Bước 4: Do dòng cập nhật sổ sách `balances[msg.sender] = 0;` nằm ở phía sau lệnh `call`, số dư của kẻ tấn công vẫn còn nguyên vẹn trên sổ sách! Vòng lặp đệ quy tiếp tục diễn ra cho đến khi ngân hàng hết tiền hoặc hết gas.  
   - Bước 5: Cuối cùng, hàm mới hoàn tất các lệnh gán số dư về 0 trong call stack, nhưng ngân hàng đã trống rỗng!
2. **Hai cách khắc phục:**  
   - *Cách 1:* Checks-Effects-Interactions (CEI) — Đổi vị trí dòng `balances[msg.sender] = 0;` lên trước lệnh `call{value}`.  
   - *Cách 2:* Khóa chống gọi lại `nonReentrant` (ReentrancyGuard của OpenZeppelin).

**Đánh giá:** ✅ Dùng được rất tốt (Câu lệnh ép "Đừng đưa mã sửa ngay" đã buộc AI giải thích bản chất kế toán và luồng thực thi thay vì chỉ đưa code sửa).

**Chỗ cần chú ý và Quyết định của nhóm:**  
- **Vấn đáp trọng tâm:** Sinh viên nhận thức sâu sắc rằng: *"Thứ chặn được tấn công ở cách 1 là thứ tự các dòng lệnh (ghi sổ trước khi chi tiền), không phải bất kỳ một từ khóa hay thư viện nào"*.  
- **Quyết định cho đồ án:** Nhóm áp dụng **chiến lược phòng thủ hai lớp (Defense-in-depth)** cho hợp đồng cốt lõi `ProjectCore.sol`:  
  1. Luôn tuân thủ tuyệt đối quy tắc CEI trong `claimRefund()` và `claimFunds()`.  
  2. Bổ sung thêm modifier `nonReentrant` nội bộ để khóa cứng mọi nỗ lực callback đệ quy, đảm bảo an toàn tuyệt đối mà vẫn giữ kích thước contract dưới 150 dòng (149 dòng).

**Ai phát hiện:** Sinh viên chủ động dẫn dắt bằng Prompt I.4 $\rightarrow$ AI giải mã chi tiết luồng EVM $\rightarrow$ Sinh viên viết kịch bản thực nghiệm kiểm chứng thành công tại `test/test_lab13_hardening.py`.

---

## Lần 5 — Xử lý Báo cáo Audit Chéo (Lab 14)

**Prompt:**  
"Dưới đây là 3 điểm mà Nhóm 4 đã phản hồi về hợp đồng ProjectCore.sol của chúng tôi. Hãy phân tích xem điểm nào là hiểu nhầm về quy tắc kinh tế của mô hình All-or-Nothing, điểm nào là lỗi cần sửa, và đề xuất mã tối ưu sự kiện CampaignCreated mà không làm hợp đồng vượt quá 150 dòng."

**AI trả về:**  
AI phân loại chính xác:
1. Ý kiến của Nhóm 4 về việc 'cho phép rút tiền trước hạn khi đạt mục tiêu' là vi phạm nguyên tắc bảo chứng All-or-Nothing; nhóm cần giữ nguyên điều kiện qua hạn chót mới cho rút tiền để bảo vệ người ủng hộ.
2. Đề xuất bổ sung tham số `fundingCap` và `deadline` vào sự kiện `CampaignCreated` để DApp lắng nghe và hiển thị trực tiếp mà không cần nhiều cuộc gọi view.
3. Mã cập nhật vẫn giữ hợp đồng ở mức 149 dòng.

**Đánh giá:** ✅ Dùng được rất tốt. Nhóm đã tiếp thu và tối ưu hóa hợp đồng thành công.

---

## Lần 6 — Tích hợp Giao diện Web DApp và Bắt Lỗi Custom Error (Lab 15)

**Prompt:**  
"Tôi muốn tạo giao diện Web DApp kết nối MetaMask bằng Ethers.js v6 cho hợp đồng ProjectCore.sol. Làm thế nào để bắt các Custom Errors của Solidity ^0.8.20 (như ExceedsMaxContribution, ContributionTooLow, OnlyCreatorAllowed) và hiển thị thông báo tiếng Việt lịch sự, thân thiện thay vì chuỗi lỗi kỹ thuật khó hiểu?"

**AI trả về:**  
AI đề xuất hàm phân tích lỗi `parseCustomError(error)` dựa trên việc kiểm tra chuỗi `error.data` hoặc `error.message` chứa tên của Custom Error tương ứng. Đồng thời gợi ý cấu trúc trạng thái UI, nút chọn nhanh số tiền và cơ chế đếm ngược thời gian thực.

**Chỗ sinh viên hoàn thiện:**  
Sinh viên nhận thấy nếu mạng Sepolia bị quá tải hay nghẽn RPC trong lúc báo cáo 5 phút thì buổi thuyết trình sẽ gặp sự cố lớn. Vì vậy, sinh viên chủ động yêu cầu tích hợp thêm **Chế độ Demo 5 Phút (Offline Simulation)** trực tiếp trên giao diện để có thể chuyển đổi linh hoạt chỉ bằng một nút bấm.

**Ai phát hiện:** Sinh viên phát hiện rủi ro mạng và chủ động thiết kế chiến lược dự phòng rủi ro.

