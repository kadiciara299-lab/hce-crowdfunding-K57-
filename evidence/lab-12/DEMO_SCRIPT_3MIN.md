# KỊCH BẢN DEMO 3 PHÚT (180 GIÂY) — CỔNG DUYỆT GATE REVIEW 1 (LAB 12)

- **Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)
- **Dự án:** **HCE Student Crowdfund (Chủ đề 5 — Gây quỹ có hoàn tiền)**
- **Nhóm sinh viên:**
  - **Hoàng Mạnh Tường** (23K4300042) — Trình bày phần 1 & phần 3
  - **Nguyễn Nguyên Phương** (23K4300034) — Trình bày phần 2 & phần 4 & phần 5
- **Thời lượng chuẩn:** Đúng 180 giây (3 phút) · Không dùng slide PowerPoint · Thao tác trực tiếp trên repo GitHub và Terminal.

---

## BẢNG PHÂN BỔ THỜI GIAN VÀ NỘI DUNG CHI TIẾT TỪNG GIÂY

| Mốc giây | Phân đoạn | Người nói | Thao tác trên màn hình | Lời thoại thuyết minh thực tế |
| :---: | :--- | :---: | :--- | :--- |
| **00 – 30s**<br>*(30 giây)* | **1. Người dùng & Vấn đề** | **Hoàng Mạnh Tường** | Mở file [`README.md`](file:///c:/Users/Tuong/Downloads/hce-web3-starter/hce-web3-starter/README.md), trỏ chuột vào mục 1: *Thông tin dự án & Nỗi đau thực tế*. | *"Kính thưa Thầy và các bạn, nhóm chúng em phát triển **HCE Student Crowdfund** — nền tảng gây quỹ cộng đồng cho sinh viên và CLB Đại học Kinh tế Huế. Vấn đề thực tế là: sinh viên gây quỹ qua tài khoản ngân hàng cá nhân, nếu dự án chỉ gom được 20-30% mục tiêu rồi bị hủy thì tiền ủng hộ thường bị kẹt, người góp mất niềm tin. Nền tảng của chúng em giải quyết triệt để bằng Smart Contract khóa tiền bảo chứng: đạt mục tiêu mới giải ngân, không đạt thì tiền tự động hoàn trả 100%."* |
| **30 – 60s**<br>*(30 giây)* | **2. Quy tắc Kinh tế cốt lõi** | **Nguyễn Nguyên Phương** | Mở [`docs/ECONOMIC_RULES.md`](file:///c:/Users/Tuong/Downloads/hce-web3-starter/hce-web3-starter/docs/ECONOMIC_RULES.md) và [`docs/SPEC.md`](file:///c:/Users/Tuong/Downloads/hce-web3-starter/hce-web3-starter/docs/SPEC.md), trỏ vào bảng 4 rào cản. | *"Về mặt kinh tế, chúng em thiết kế 4 rào cản tự động trên chuỗi: Thứ nhất, mức đóng góp sàn 0.001 ETH chống bão bụi giao dịch (Dust Attack). Thứ hai, trần mỗi ví 25% chống cá mập thao túng chiến dịch. Thứ ba, thời hạn chiến dịch giới hạn từ 3 đến 30 ngày chống giam vốn. Thứ tư, nếu hết hạn mà không đủ mục tiêu, bất kỳ ai cũng có thể tự rút lại 100% tiền của mình mà không bị tính phí."* |
| **60 – 120s**<br>*(60 giây)* | **3. Demo Luồng Cốt lõi Thành công** | **Hoàng Mạnh Tường** | Mở [`contracts/project/ProjectCore.sol`](file:///c:/Users/Tuong/Downloads/hce-web3-starter/hce-web3-starter/contracts/project/ProjectCore.sol), sau đó chuyển sang Terminal chạy lệnh: `python test/test_gate_review.py`. | *"Bây giờ em xin demo luồng thành công. Hợp đồng `ProjectCore.sol` gồm 144 dòng. Ở kịch bản khởi tạo, mục tiêu gọi vốn là 1.0 ETH trong 7 ngày. Khi 4 sinh viên nạp mỗi người 0.25 ETH chạm đúng trần ví, tổng quỹ đạt 1.0 ETH (100%). Sau khi thời gian vượt qua deadline, chủ dự án gọi hàm `claimFunds()` — hệ thống lập tức kiểm tra và giải ngân thành công 1.0 ETH về ví chủ dự án, phát event `FundsClaimed` và chuyển trạng thái hợp đồng sang `Claimed`."* |
| **120 – 150s**<br>*(30 giây)* | **4. Demo Các Ca Vi phạm Bị Chặn** | **Nguyễn Nguyên Phương** | Chỉ vào phần log chặn gian lận trên Terminal (`test_output.log`). | *"Tiếp theo, hệ thống chứng minh độ an toàn khi đối mặt với 4 ca gian lận: 1) Kẻ xấu gửi 0.0005 ETH dưới sàn lập tức bị chặn với lỗi `ContributionTooLow`. 2) Cá mập gửi 0.35 ETH vượt trần ví bị chặn với lỗi `ExceedsMaxContribution`. 3) Chủ dự án cố rút tiền trước hạn bị từ chối với lỗi `CampaignStillActive`. 4) Kẻ lạ mạo danh chủ dự án bị chặn với lỗi `OnlyCreatorAllowed`. Tất cả đều dùng Custom Error tiết kiệm gas theo `AGENTS.md`."* |
| **150 – 180s**<br>*(30 giây)* | **5. Lộ trình Tiếp theo & Kết luận** | **Cả 2 thành viên** | Mở [`docs/PROJECT_PLAN.md`](file:///c:/Users/Tuong/Downloads/hce-web3-starter/hce-web3-starter/docs/PROJECT_PLAN.md), chỉ vào bảng mốc Lab 13–15. | *(Phương): "Về lộ trình tiếp theo, ở Lab 13 chúng em sẽ thực nghiệm viết contract tấn công Reentrancy và vá lỗi bằng CEI. Ở Lab 14 chúng em rà soát chéo hợp đồng nhóm bạn. Và Lab 15 sẽ đưa DApp lên mạng Sepolia và GitHub Pages."*<br>*(Tường): "Nhóm đã hoàn thành xoay vai trò và sẵn sàng cho các yêu cầu của Hội đồng. Xin trân trọng cảm ơn Thầy!"* |

---

## KẾT QUẢ ĐẦU RA KHI THỰC THI DEMO TRỰC TIẾP

```text
***************************************************************************
🏛️  HỘI ĐỒNG GATE REVIEW 1: KIỂM TRA SỨC KHỎE REPO & DEMO 3 PHÚT
     Dự án: HCE Student Crowdfund (Chủ đề 5 - Gây quỹ có hoàn tiền)
     Sinh viên: Hoàng Mạnh Tường (23K4300042) & Nguyễn Nguyên Phương (23K4300034)
***************************************************************************

[KHỞI TẠO CHIẾN DỊCH]
  - Chủ dự án (Creator):        0xCreatorWallet_HCE
  - Mục tiêu gọi vốn:           1.0000 ETH
  - Sàn đóng góp (min):         0.0010 ETH
  - Trần đóng góp mỗi ví (25%): 0.2500 ETH
  - Trần cứng huy động (120%):  1.2000 ETH
  - Thời hạn chiến dịch:        7 ngày

===========================================================================
PHẦN 1: DEMO LUỒNG GIAN LẬN / VI PHẠM BỊ CHẶN (30 GIÂY DEMO)
===========================================================================

[CA 1 - DUST ATTACK] Kẻ xấu gửi 0.0005 ETH (< sàn 0.001 ETH)...
  🛡️ BỊ CHẶN THÀNH CÔNG! Mã lỗi: ContributionTooLow(sent=0.0005 ETH, min=0.0010 ETH)

[CA 2 - WHALE ATTACK] Tài phiệt gửi 0.35 ETH một lần (> trần ví 0.25 ETH)...
  🛡️ BỊ CHẶN THÀNH CÔNG! Mã lỗi: ExceedsMaxContribution(attempted=0.3500 ETH, limit=0.2500 ETH)

[CA 3 - EARLY WITHDRAWAL] Chủ dự án gọi claimFunds() trước ngày deadline...
  🛡️ BỊ CHẶN THÀNH CÔNG! Mã lỗi: CampaignStillActive(timeLeft=604800 giây)

[CA 4 - UNAUTHORIZED CLAIM] Kẻ lạ (0xImposter) gọi claimFunds()...
  🛡️ BỊ CHẶN THÀNH CÔNG! Mã lỗi: OnlyCreatorAllowed: Caller 0xImposter không phải Creator 0xCreatorWallet_HCE

===========================================================================
PHẦN 2: DEMO LUỒNG CỐT LÕI THÀNH CÔNG (HAPPY PATH - 60 GIÂY DEMO)
===========================================================================

[BƯỚC 1] 4 sinh viên HCE cùng tham gia đóng góp hợp lệ:
  ✅ 0xSinhVienA đã nạp 0.2500 ETH -> Event Pledged(contributor=0xSinhVienA, amount=0.2500 ETH, totalRaised=0.2500 ETH)
  ✅ 0xSinhVienB đã nạp 0.2500 ETH -> Event Pledged(contributor=0xSinhVienB, amount=0.2500 ETH, totalRaised=0.5000 ETH)
  ✅ 0xSinhVienC đã nạp 0.2500 ETH -> Event Pledged(contributor=0xSinhVienC, amount=0.2500 ETH, totalRaised=0.7500 ETH)
  ✅ 0xSinhVienD đã nạp 0.2500 ETH -> Event Pledged(contributor=0xSinhVienD, amount=0.2500 ETH, totalRaised=1.0000 ETH)

[TIẾN ĐỘ CHIẾN DỊCH] Tổng huy động: 1.0000 ETH / 1.0000 ETH (Đạt 100% mục tiêu!)

[BƯỚC 2] Thời gian trôi qua 7 ngày (chiến dịch kết thúc thời hạn nhận quỹ)...
  ⏳ Thời gian hiện tại đã vượt qua Deadline (Hạn chót: 1604800, Giờ HT: 1604801)

[BƯỚC 3] Chủ dự án chính thức gọi claimFunds() để giải ngân kinh phí dự án:
  🎉 GIẢI NGÂN THÀNH CÔNG! Event FundsClaimed(creator=0xCreatorWallet_HCE, totalAmount=1.0000 ETH)
  Trạng thái hợp đồng chuyển sang: [Claimed]
  Số dư còn lại trong quỹ: 0.0000 ETH

===========================================================================
PHẦN 3: DEMO LUỒNG HOÀN TIỀN TỰ ĐỘNG KHI THẤT BẠI (REFUND PATH)
===========================================================================

[TÌNH HUỐNG THẤT BẠI] Chiến dịch chỉ nhận được 0.20 ETH từ bạn 0xStudentX...
  Tổng huy động: 0.2000 ETH (Dưới mục tiêu 1.0 ETH)
  Thời gian trôi qua hết 7 ngày...

[BƯỚC 1] Chủ dự án cố tình rút tiền khi không đạt mục tiêu:
  🛡️ BỊ CHẶN: GoalNotMet(raised=0.2000 ETH, goal=1.0000 ETH)

[BƯỚC 2] Bạn 0xStudentX gọi claimRefund() để lấy lại tiền:
  💸 HOÀN TIỀN THÀNH CÔNG: Event RefundClaimed(contributor=0xStudentX, refundAmount=0.2000 ETH)
  Số dư đóng góp còn lại của 0xStudentX: 0 wei

[BƯỚC 3] Bạn 0xStudentX cố tình gọi claimRefund() lần 2 (Rút kép):
  🛡️ BỊ CHẶN RÚT KÉP: NoContributionToRefund: Địa chỉ ví không có số dư đóng góp!

***************************************************************************
🏆 TỔNG KẾT GATE REVIEW 1: 100% CÁC TIÊU CHÍ KỸ THUẬT & NGHIỆP VỤ ĐẠT YÊU CẦU!
***************************************************************************
```
