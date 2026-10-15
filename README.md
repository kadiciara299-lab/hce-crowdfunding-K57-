# HCE Student Crowdfund — Nền tảng Gây quỹ Dự án Sinh viên có Hoàn tiền

> **Một câu định vị sản phẩm:**  
> *"Nhóm xây dựng Nền tảng gây quỹ dự án sinh viên có hoàn tiền tự động (HCE Student Crowdfund) cho cộng đồng sinh viên và các câu lạc bộ Trường Đại học Kinh tế - Đại học Huế (HCE) nhằm huy động vốn minh bạch cho các đề tài nghiên cứu khoa học, dự án khởi nghiệp và cam kết tự động hoàn trả 100% tiền cho người ủng hộ nếu dự án không đạt mục tiêu tài chính trước hạn chót."*

---

## 👥 1. Thông tin Nhóm Sinh viên thực hiện (K57 Kinh Tế Số - HCE)

Dự án thuộc học phần: **Tiền điện tử & Hợp đồng thông minh (ECO2432)**  
Mã chủ đề đồ án: **Chủ đề 5 — Gây quỹ có hoàn tiền (Refundable Crowdfunding)**  
Kho mã nguồn chính thức: [`https://github.com/kadiciara299-lab/hce-crowdfunding-K57-.git`](https://github.com/kadiciara299-lab/hce-crowdfunding-K57-)

| STT | Họ và tên | Mã sinh viên | Vai chính Lab 8–11 | Vai chính Lab 12–15 | GitHub Username |
| :-: | :--- | :---: | :--- | :--- | :--- |
| 1 | **Hoàng Mạnh Tường** *(Lead)* | **23K4300042** | Đặc tả nghiệp vụ (BA) & Thiết kế Kinh tế *(kiêm QA)* | Hợp đồng thông minh & Audit *(kiêm Web3 Lead)* | `@23k4300042-lang` |
| 2 | **Nguyễn Nguyên Phương** | **23K4300034** | Hợp đồng thông minh *(kiêm Giao diện Web/Gas)* | Đặc tả & Thuyết trình *(kiêm Red Team Security)* | `@kadiciara299-lab` |

---

## 📂 2. Cấu trúc Kho mã nguồn Chuẩn (Theo Phần B.6 Sổ tay)

```text
hce-crowdfunding-K57-/
├── README.md                      # Giới thiệu sản phẩm, thành viên và hướng dẫn chạy
├── AGENTS.md                      # Quy ước dự án bắt buộc cho công cụ AI
├── docs/
│   ├── PROJECT_PLAN.md            # Kế hoạch dự án, phân vai xoay vòng và 7 mốc bắt buộc
│   ├── SPEC.md                    # Bản đặc tả nghiệp vụ v0.1 có hiệu lực
│   ├── ECONOMIC_RULES.md          # Quy tắc dòng tiền, 4 rào cản chống lạm dụng & phản biện
│   ├── AI_JOURNAL.md              # Nhật ký làm việc với AI và các lỗi nghiêm trọng đã sửa
│   └── PRESENTATION_PLAN.md       # Kịch bản báo cáo và demo 5 phút phân công từng giây
├── contracts/
│   ├── training/                  # Hợp đồng mẫu học tập (TimeLockVault, VaultBuggy,...)
│   └── project/
│       └── ProjectCore.sol        # Hợp đồng thông minh cốt lõi của sản phẩm nhóm
├── test/                          # Ca kiểm thử tự động của sản phẩm nhóm
├── web/
│   └── index.html                 # Giao diện Web3 DApp kết nối MetaMask
└── evidence/
    └── lab-08/                    # Minh chứng commit, kiểm thử và biên bản từng lab
```

---

## 🚀 3. Hướng dẫn Chạy và Thử nghiệm

### 3.1. Biên dịch và Triển khai Hợp đồng trên Remix IDE
1. Truy cập [Remix Ethereum IDE](https://remix.ethereum.org).
2. Tải tệp `contracts/project/ProjectCore.sol` lên thư mục làm việc của Remix.
3. Trong tab **Solidity Compiler**, chọn phiên bản `0.8.20` trở lên và bấm **Compile ProjectCore.sol**.
4. Trong tab **Deploy & Run Transactions**:
   - Chọn môi trường: **Remix VM (Cancun / Shanghai)** để thử nghiệm tức thì miễn phí, hoặc **Injected Provider - MetaMask** để triển khai lên mạng thử nghiệm Sepolia.
   - Điền tham số Constructor:
     - `_goalInWei`: Ví dụ `1000000000000000000` (1 ETH).
     - `_durationSeconds`: Ví dụ `259200` (3 ngày tính bằng giây).
     - `_minContributionInWei`: Ví dụ `1000000000000000` (0.001 ETH).
   - Bấm **Deploy**.

### 3.2. Chạy Giao diện DApp Cục bộ
- Mở tệp `web/index.html` trực tiếp bằng trình duyệt Google Chrome hoặc Microsoft Edge đã cài đặt tiện ích MetaMask.
- Kết nối ví và chuyển mạng sang **Sepolia Testnet**.

---

## 📜 4. Cam kết Liêm chính và Quy ước Mã nguồn

- Toàn bộ mã nguồn tuân thủ nghiêm ngặt chỉ dẫn tại [`AGENTS.md`](./AGENTS.md):
  - Áp dụng nguyên tắc **Checks - Effects - Interactions** bảo vệ chống tấn công tái nhập.
  - Sử dụng lệnh chuyển tiền `call{value: ...}("")`, tuyệt đối không dùng `transfer`.
  - Khai báo lỗi tùy biến (`custom errors`) thay cho chuỗi ký tự lỗi dài trong `require`.
  - Đơn vị tính toán số học trên chuỗi luôn dùng `wei` và điểm cơ bản `basis points` ($1\% = 100 \text{ bps}$).

---

## 📁 5. Danh mục sản phẩm & Lộ trình triển khai Đồ án (Lab 8 – 15)

| Giai đoạn | Sản phẩm bàn giao | Mô tả nghiệp vụ & Kỹ thuật | Trạng thái |
| :---: | :--- | :--- | :---: |
| **Lab 8** | [`docs/PROJECT_PLAN.md`](./docs/PROJECT_PLAN.md)<br>[`docs/SPEC.md`](./docs/SPEC.md)<br>[`docs/ECONOMIC_RULES.md`](./docs/ECONOMIC_RULES.md)<br>[`docs/AI_JOURNAL.md`](./docs/AI_JOURNAL.md)<br>[`lab08.md`](./lab08.md)<br>[`contracts/project/ProjectCore.sol`](./contracts/project/ProjectCore.sol) | Khởi động đồ án Chủ đề 5 (**HCE Student Crowdfund**), chuẩn hóa cấu trúc repo Phần B.6; hoàn thiện đặc tả BA v0.1 (8 quy tắc R1–R8, 9 ngoại lệ); thiết kế kinh tế All-or-Nothing, sàn 0.001 ETH, trần 25% và 5 kịch bản phản biện lạm dụng | ✅<br>**Hoàn thành** |
| **Lab 9** | [`contracts/project/ProjectCore.sol`](./contracts/project/ProjectCore.sol)<br>[`contracts/training/TimeLockVault.sol`](./contracts/training/TimeLockVault.sol)<br>[`lab09.md`](./lab09.md) | Hiện thực hóa máy trạng thái gây quỹ (`Active`, `Successful`, `Failed`, `Claimed`), cơ chế bảo chứng cam kết (Assurance Escrow); chuyển ETH an toàn bằng `call{value}`, đo đạc bảng tiêu thụ gas trên Remix VM | ✅<br>**Hoàn thành** |
| **Lab 10** | [`lab10.md`](./lab10.md)<br>[`docs/AI_JOURNAL.md`](./docs/AI_JOURNAL.md)<br>[`contracts/training/VaultBuggy.sol`](./contracts/training/VaultBuggy.sol)<br>[`contracts/project/ProjectCore.sol`](./contracts/project/ProjectCore.sol) *(v2)* | Rà soát mã nguồn do AI sinh ra, giải mã Storage Layout & Slot 2 (VaultBuggy); nhận diện và sửa 3 lỗi tiềm ẩn (chống DoS lặp Push payment, triệt tiêu `transfer`); kiểm toán và tối ưu cấu trúc lưu trữ `ProjectCore` | ✅<br>**Hoàn thành** |
| **Lab 11** | [`contracts/project/ProjectCore.sol`](./contracts/project/ProjectCore.sol)<br>[`test/test_economic_rules.py`](./test/test_economic_rules.py)<br>[`lab11.md`](./lab11.md)<br>[`evidence/lab-11/`](./evidence/lab-11/) | Cài đặt 3 rào cản kinh tế vào hợp đồng (sàn 0.001 ETH, trần ví 25%, trần cứng 120%). Kiểm thử tự động 5 ca thử nghiệm toàn diện: luồng hợp lệ, vi phạm sàn, vi phạm trần ví và vi phạm trần cứng | ✅<br>**Hoàn thành** |
| **Lab 12** | [`test/test_gate_review.py`](./test/test_gate_review.py)<br>[`Do An/lab12.md`](./Do%20An/lab12.md)<br>[`docs/GATE_REVIEW_1.md`](./docs/GATE_REVIEW_1.md)<br>[`evidence/lab-12/`](./evidence/lab-12/) | Vượt qua cổng duyệt bắt buộc **GATE REVIEW 1**; kiểm tra sức khỏe repo 5/5 tiêu chí; demo 3 phút chứng minh luồng thành công và 4 ca gian lận/vi phạm; thống nhất thu hẹp phạm vi và chốt phân vai xoay vòng Lab 13–15 | ✅<br>**Hoàn thành** |
| **Lab 13** | [`contracts/training/VulnerableBank.sol`](./contracts/training/VulnerableBank.sol)<br>[`contracts/training/SafeBank.sol`](./contracts/training/SafeBank.sol)<br>[`contracts/project/AttackCrowdfund.sol`](./contracts/project/AttackCrowdfund.sol)<br>[`contracts/project/ProjectCore.sol`](./contracts/project/ProjectCore.sol)<br>[`test/test_lab13_hardening.py`](./test/test_lab13_hardening.py)<br>[`Do An/lab13.md`](./Do%20An/lab13.md)<br>[`evidence/lab-13/`](./evidence/lab-13/) | Thực nghiệm rút cạn $6 \text{ ETH}$ qua lỗ hổng Reentrancy; giải mã cơ chế bằng Prompt I.4; vá lỗi bằng 2 phương pháp CEI & ReentrancyGuard; gia cố phòng thủ hai lớp cho `ProjectCore.sol` (149 dòng); 8 ca Negative Tests đạt 100% | ✅<br>**Hoàn thành** |
| **Lab 14** | [`docs/AUDIT_REPORT.md`](./docs/)<br>[`lab14.md`](./lab14.md)<br>[`evidence/lab-14/`](./evidence/) | Kiểm toán chéo bảo mật (Peer Security Audit) Smart Contract nhóm bạn theo bộ 10 tiêu chí an toàn (Reentrancy, Arithmetic, Access Control, Gas Griefing); tiếp nhận phản hồi kiểm toán và tối ưu bảo mật cho `ProjectCore` | 🔄<br>**Sắp triển khai** |
| **Lab 15** | [`contracts/project/ProjectCore.sol`](./contracts/project/ProjectCore.sol) *(Sepolia)*<br>[`docs/PRESENTATION_PLAN.md`](./docs/PRESENTATION_PLAN.md)<br>[`lab15.md`](./lab15.md) | Triển khai hợp đồng chính thức lên Sepolia Testnet, xuất bản Web3 DApp lên GitHub Pages tương tác trên thiết bị di động; hoàn thiện slide & kịch bản thuyết trình demo sản phẩm 5 phút phân vai từng giây | 🔄<br>**Sắp triển khai** |

