Dưới góc nhìn của một **nhà đầu tư / người dùng thận trọng**, dựa trên nội dung tại [SPEC.md] và [ECONOMIC_RULES.md] **5 cách thức một người có thể lạm dụng quy tắc hoặc khiến người tham gia chịu thiệt hại nặng nề**:

---

### 1. Chủ dự án tự nạp tiền ảo phút chót để "hút cạn" tiền thật (Self-Funding to Rug Pull)
* **Kịch bản lạm dụng:** Dự án đặt mục tiêu 10 ETH. Đến sát thời hạn (`deadline`), cộng đồng sinh viên chỉ mới đóng góp 6 ETH. Theo luật All-or-Nothing, nếu hết giờ thì 6 ETH này phải hoàn trả cho sinh viên. Nhận thấy sắp mất trắng tiền tài trợ, chủ dự án dùng một ví phụ nạp nốt 4 ETH vào những giây cuối cùng để đẩy `totalRaised` chạm mốc 10 ETH. Ngay sau khi qua `deadline`, chủ dự án kích hoạt hàm rút toàn bộ 10 ETH — vừa thu hồi lại 4 ETH của mình, vừa chiếm đoạt trọn vẹn 6 ETH của sinh viên mà không cần có được sự tín nhiệm thật sự của cộng đồng.
* **Quy tắc chưa đủ chặt:** **Quy tắc R1 & R2 trong [SPEC.md]**. Hợp đồng chỉ kiểm tra tổng tiền (`totalRaised >= goal`) mà không có trần góp vốn tối đa trên từng ví cá nhân (Max Cap per Wallet) và không yêu cầu số lượng ví ủng hộ tối thiểu (Min Unique Backers), dẫn đến việc một cá nhân có thể tự thao túng trạng thái thành bại của cả dự án.

---

### 2. Dự án bị "bỏ rơi" hoặc mất khóa ví — Tiền của người góp bị giam cầm vĩnh viễn (Fund Lockup with No Escape Hatch)
* **Kịch bản gây thiệt hại:** Dự án gây quỹ thành công (đạt 10 ETH). Tuy nhiên, sau `deadline`, chủ dự án làm mất khóa ví cá nhân (Private Key), gặp sự cố cá nhân, hoặc nhóm sinh viên bất hòa và bỏ mặc dự án. Vì điều kiện `totalRaised >= goal` đã thỏa mãn, theo quy tắc R3, **người góp tiền bị cấm tuyệt đối không được hoàn tiền**. Kết quả là toàn bộ 10 ETH của sinh viên sẽ bị giam vĩnh viễn trong hợp đồng mà không một ai có thể lấy lại được.
* **Quy tắc chưa đủ chặt:** **Quy tắc R2 & R3 trong [SPEC.md][ECONOMIC_RULES.md]**. Thiếu quy tắc về **Thời hạn ân hạn rút tiền (Grace Period / Sunset Clause)**: Nếu sau một khoảng thời gian (ví dụ 30 ngày kể từ `deadline`) mà Admin không rút quỹ, hợp đồng cần tự động chuyển sang trạng thái "Bỏ rơi" để cho phép người góp được rút lại tiền.

---

### 3. Huy động vượt trần không giới hạn rồi ôm trọn gói tiền (Unlimited Oversubscription Exploitation)
* **Kịch bản lạm dụng:** Dự án ban đầu chỉ đăng ký làm một sản phẩm nhỏ với ngân sách dự kiến là 2 ETH. Tuy nhiên, quy tắc R1 cho phép bất kỳ ai nạp tiền không giới hạn trước hạn. Chủ dự án dùng các chiêu trò truyền thông thổi phồng để huy động lên tới 30 ETH (gấp 15 lần mục tiêu). Khi hết hạn, chủ dự án nghiễm nhiên rút sạch 30 ETH mà hoàn toàn không có kế hoạch ngân sách hay trách nhiệm giải trình tương xứng cho số tiền khổng lồ vượt mức đó.
* **Quy tắc chưa đủ chặt:** **Mục 1 [ECONOMIC_RULES.md](tắc về **Trần cứng tối đa (Hard Cap)**, ví dụ quy định quỹ tối đa chỉ được nhận không quá 120% hoặc 150% mục tiêu ban đầu để tránh tích tụ rủi ro tài chính quá lớn cho sinh viên.

---

### 4. Rút cạn 100% tiền trong một lần duy nhất mà không có ràng buộc tiến độ (Post-funding Abandonment)
* **Kịch bản gây thiệt hại:** Sau khi qua `deadline` và đạt mục tiêu, Admin rút ngay lập tức 100% số dư hợp đồng trong 1 giao dịch duy nhất. Sau khi tiền về ví cá nhân, Admin hoàn toàn "bốc hơi", không tổ chức sự kiện hay làm sản phẩm như cam kết. Cơ chế All-or-Nothing chỉ bảo vệ được nhà tài trợ *trước khi huy động*, nhưng hoàn toàn vô dụng *sau khi tiền đã được giải ngân*.
* **Quy tắc chưa đủ chặt:** **Quy tắc R2 trong [SPEC.md][ECONOMIC_RULES.md]**. Thiết kế giải ngân 1 cục (All-at-once) thiếu cơ chế chia tiền theo từng giai đoạn (Milestones) hoặc cơ chế biểu quyết đóng băng quỹ của cộng đồng khi phát hiện dự án có dấu hiệu gian lận sau khi gọi vốn thành công.

---

### 5. Kẹt tiền hoàn trả khi người đóng góp sử dụng ví Smart Contract (Smart Contract Incompatibility)
* **Kịch bản gây thiệt hại:** Một câu lạc bộ hoặc một nhóm sinh viên dùng ví dùng chung (ví đa chữ ký Multi-sig như Gnosis Safe, hoặc ví hợp đồng thông minh không có sẵn hàm `receive()` / `fallback()`) để đóng góp quỹ. Khi dự án thất bại, ví này gọi hàm `claimRefund()`. Do hợp đồng gửi ETH về địa chỉ người gọi, giao dịch chuyển tiền bị Revert do ví nhận không thể tiếp nhận native ETH trực tiếp, khiến khoản tiền hoàn trả của tập thể đó bị tắc nghẽn vĩnh viễn trong quỹ.
* **Quy tắc chưa đủ chặt:** **Quy tắc R3 & R4 trong [SPEC.md][ECONOMIC_RULES.md]. Chưa có cơ chế bảo vệ phân định rõ hoặc chuyển đổi sang mô hình ủy thác ký gửi (Escrow/Vault claim) đối với các địa chỉ hợp đồng không hỗ trợ nhận ETH trực tiếp.