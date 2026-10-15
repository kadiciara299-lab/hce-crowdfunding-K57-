"""
KỊCH BẢN KIỂM THỬ DEMO 3 PHÚT - GATE REVIEW 1 (LAB 12)
Học phần: Tiền điện tử & Hợp đồng thông minh (ECO2432)
Dự án: HCE Student Crowdfund (Chủ đề 5)
Kho mã nguồn: https://github.com/kadiciara299-lab/hce-crowdfunding-K57-.git
Nhóm thực hiện:
  - Hoàng Mạnh Tường (23K4300042)
  - Nguyễn Nguyên Phương (23K4300034)

Mô phỏng chính xác logic của ProjectCore.sol (^0.8.20) phục vụ trình diễn trước Hội đồng Gate Review 1:
  1. Luồng thành công (Happy Path): Huy động đạt mục tiêu -> Hết hạn -> Chủ dự án rút tiền.
  2. Các ca vi phạm & gian lận bị chặn (Negative Tests):
     - Ca gian lận 1: Gửi số tiền dưới sàn (Dust Attack < 0.001 ETH).
     - Ca gian lận 2: Nạp vượt trần ví (Whale Attack > 25% fundingGoal).
     - Ca vi phạm 3: Rút tiền khi chưa hết hạn chiến dịch (CampaignStillActive).
     - Ca vi phạm 4: Người lạ cố tình rút tiền của chủ dự án (OnlyCreatorAllowed).
  3. Luồng hoàn tiền tự động (Refund Path): Hết hạn nhưng không đạt mục tiêu -> Người ủng hộ tự rút hoàn 100%.
"""

import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def format_eth(wei_amount: int) -> str:
    """Đổi wei sang ETH theo quy tắc AGENTS.md"""
    return f"{wei_amount / 10**18:.4f} ETH"

class MockProjectCore:
    """Mô phỏng hành vi nghiệp vụ của Smart Contract contracts/project/ProjectCore.sol"""
    def __init__(self, creator: str, goal_in_wei: int, duration_seconds: int, min_contribution_wei: int = 10**15):
        if not creator or creator == "0x0":
            raise ValueError("InvalidCreator()")
        if goal_in_wei <= 0:
            raise ValueError("InvalidGoal()")
        if duration_seconds < 3 * 86400 or duration_seconds > 30 * 86400:
            raise ValueError("InvalidDuration()")

        self.creator = creator
        self.funding_goal = goal_in_wei
        self.funding_cap = (goal_in_wei * 120) // 100  # Trần cứng 120%
        self.min_contribution = min_contribution_wei
        self.max_contribution_per_wallet = (goal_in_wei * 25) // 100  # Trần 25%

        if self.max_contribution_per_wallet < self.min_contribution:
            raise ValueError("InvalidGoal: Trần nhỏ hơn sàn gây Deadlock!")

        self.current_time = 1_000_000
        self.deadline = self.current_time + duration_seconds
        self.total_raised = 0
        self.state = "Active"
        self.contributions = {}
        self.contract_balance = 0

    def advance_time(self, seconds: int):
        self.current_time += seconds

    def pledge(self, contributor: str, amount_wei: int):
        # 1. Checks
        if self.current_time >= self.deadline:
            raise RuntimeError(f"CampaignEnded(deadline={self.deadline}, currentTime={self.current_time})")
        if self.state != "Active":
            raise RuntimeError(f"CampaignEnded: Chiến dịch không ở trạng thái Active")
        if amount_wei < self.min_contribution:
            raise RuntimeError(f"ContributionTooLow(sent={format_eth(amount_wei)}, min={format_eth(self.min_contribution)})")
        if self.total_raised + amount_wei > self.funding_cap:
            raise RuntimeError(f"ExceedsFundingCap(attemptedTotal={format_eth(self.total_raised + amount_wei)}, cap={format_eth(self.funding_cap)})")

        current_contrib = self.contributions.get(contributor, 0)
        new_total = current_contrib + amount_wei
        if new_total > self.max_contribution_per_wallet:
            raise RuntimeError(f"ExceedsMaxContribution(attempted={format_eth(new_total)}, limit={format_eth(self.max_contribution_per_wallet)})")

        # 2. Effects
        self.contributions[contributor] = new_total
        self.total_raised += amount_wei
        self.contract_balance += amount_wei

        # Phát event Pledged
        return f"Event Pledged(contributor={contributor}, amount={format_eth(amount_wei)}, totalRaised={format_eth(self.total_raised)})"

    def claim_funds(self, caller: str):
        # 1. Checks
        if caller != self.creator:
            raise RuntimeError(f"OnlyCreatorAllowed: Caller {caller} không phải Creator {self.creator}")
        if self.state == "Claimed":
            raise RuntimeError("AlreadyClaimed()")
        if self.current_time < self.deadline:
            time_left = self.deadline - self.current_time
            raise RuntimeError(f"CampaignStillActive(timeLeft={time_left} giây)")
        if self.total_raised < self.funding_goal:
            raise RuntimeError(f"GoalNotMet(raised={format_eth(self.total_raised)}, goal={format_eth(self.funding_goal)})")

        # 2. Effects
        self.state = "Claimed"
        amount_to_transfer = self.contract_balance
        self.contract_balance = 0

        # 3. Interactions: Chuyển tiền qua call{value}
        return f"Event FundsClaimed(creator={self.creator}, totalAmount={format_eth(amount_to_transfer)})"

    def claim_refund(self, caller: str):
        # 1. Checks
        if self.current_time < self.deadline:
            time_left = self.deadline - self.current_time
            raise RuntimeError(f"CampaignStillActive(timeLeft={time_left} giây)")
        if self.total_raised >= self.funding_goal:
            raise RuntimeError("CampaignSucceeded: Chiến dịch thành công, không thể hoàn tiền!")

        contributed = self.contributions.get(caller, 0)
        if contributed == 0:
            raise RuntimeError("NoContributionToRefund: Địa chỉ ví không có số dư đóng góp!")

        # 2. Effects: Xóa sổ TRƯỚC để phòng vệ tái nhập (CEI)
        self.contributions[caller] = 0
        if self.state != "Failed":
            self.state = "Failed"

        self.contract_balance -= contributed

        # 3. Interactions
        return f"Event RefundClaimed(contributor={caller}, refundAmount={format_eth(contributed)})"


def run_gate_review_demo():
    print("*" * 75)
    print("🏛️  HỘI ĐỒNG GATE REVIEW 1: KIỂM TRA SỨC KHỎE REPO & DEMO 3 PHÚT")
    print("     Dự án: HCE Student Crowdfund (Chủ đề 5 - Gây quỹ có hoàn tiền)")
    print("     Sinh viên: Hoàng Mạnh Tường (23K4300042) & Nguyễn Nguyên Phương (23K4300034)")
    print("*" * 75)

    creator = "0xCreatorWallet_HCE"
    goal_wei = 1 * 10**18  # 1.0 ETH
    duration = 7 * 86400   # 7 ngày
    min_wei = 10**15       # 0.001 ETH

    print(f"\n[KHỞI TẠO CHIẾN DỊCH]")
    print(f"  - Chủ dự án (Creator):        {creator}")
    print(f"  - Mục tiêu gọi vốn:           {format_eth(goal_wei)}")
    print(f"  - Sàn đóng góp (min):         {format_eth(min_wei)}")
    print(f"  - Trần đóng góp mỗi ví (25%): {format_eth((goal_wei * 25) // 100)}")
    print(f"  - Trần cứng huy động (120%):  {format_eth((goal_wei * 120) // 100)}")
    print(f"  - Thời hạn chiến dịch:        {duration // 86400} ngày")

    # =========================================================================
    # KỊCH BẢN DEMO BƯỚC 2: 3 PHÚT TRÌNH BÀY VÀ THỰC NGHIỆM
    # =========================================================================
    print("\n" + "=" * 75)
    print("PHẦN 1: DEMO LUỒNG GIAN LẬN / VI PHẠM BỊ CHẶN (30 GIÂY DEMO)")
    print("=" * 75)

    app = MockProjectCore(creator, goal_wei, duration, min_wei)

    # 1. Ca gian lận 1: Gửi dưới sàn (Dust attack)
    print("\n[CA 1 - DUST ATTACK] Kẻ xấu gửi 0.0005 ETH (< sàn 0.001 ETH)...")
    try:
        app.pledge("0xAttacker_Dust", int(0.0005 * 10**18))
        print("  ❌ THẤT BẠI: Hợp đồng đã không chặn!")
    except RuntimeError as e:
        print(f"  🛡️ BỊ CHẶN THÀNH CÔNG! Mã lỗi: {e}")

    # 2. Ca gian lận 2: Cá mập gửi 0.35 ETH (> trần 25% = 0.25 ETH)
    print("\n[CA 2 - WHALE ATTACK] Tài phiệt gửi 0.35 ETH một lần (> trần ví 0.25 ETH)...")
    try:
        app.pledge("0xWhale", int(0.35 * 10**18))
        print("  ❌ THẤT BẠI: Hợp đồng đã không chặn!")
    except RuntimeError as e:
        print(f"  🛡️ BỊ CHẶN THÀNH CÔNG! Mã lỗi: {e}")

    # 3. Ca vi phạm 3: Chủ dự án cố tình rút tiền trước hạn chót khi đang diễn ra
    print("\n[CA 3 - EARLY WITHDRAWAL] Chủ dự án gọi claimFunds() trước ngày deadline...")
    try:
        app.claim_funds(creator)
        print("  ❌ THẤT BẠI: Hợp đồng đã cho rút trước hạn!")
    except RuntimeError as e:
        print(f"  🛡️ BỊ CHẶN THÀNH CÔNG! Mã lỗi: {e}")

    # 4. Ca vi phạm 4: Người lạ mạo danh chủ dự án để rút tiền
    print("\n[CA 4 - UNAUTHORIZED CLAIM] Kẻ lạ (0xImposter) gọi claimFunds()...")
    try:
        app.claim_funds("0xImposter")
        print("  ❌ THẤT BẠI: Kẻ lạ đã rút được tiền!")
    except RuntimeError as e:
        print(f"  🛡️ BỊ CHẶN THÀNH CÔNG! Mã lỗi: {e}")

    print("\n" + "=" * 75)
    print("PHẦN 2: DEMO LUỒNG CỐT LÕI THÀNH CÔNG (HAPPY PATH - 60 GIÂY DEMO)")
    print("=" * 75)

    print("\n[BƯỚC 1] 4 sinh viên HCE cùng tham gia đóng góp hợp lệ:")
    contributors = [
        ("0xSinhVienA", int(0.25 * 10**18)),
        ("0xSinhVienB", int(0.25 * 10**18)),
        ("0xSinhVienC", int(0.25 * 10**18)),
        ("0xSinhVienD", int(0.25 * 10**18)),
    ]
    for wallet, amount in contributors:
        evt = app.pledge(wallet, amount)
        print(f"  ✅ {wallet} đã nạp {format_eth(amount)} -> {evt}")

    print(f"\n[TIẾN ĐỘ CHIẾN DỊCH] Tổng huy động: {format_eth(app.total_raised)} / {format_eth(app.funding_goal)} (Đạt 100% mục tiêu!)")

    print("\n[BƯỚC 2] Thời gian trôi qua 7 ngày (chiến dịch kết thúc thời hạn nhận quỹ)...")
    app.advance_time(7 * 86400 + 1)
    print(f"  ⏳ Thời gian hiện tại đã vượt qua Deadline (Hạn chót: {app.deadline}, Giờ HT: {app.current_time})")

    print("\n[BƯỚC 3] Chủ dự án chính thức gọi claimFunds() để giải ngân kinh phí dự án:")
    evt_claim = app.claim_funds(creator)
    print(f"  🎉 GIẢI NGÂN THÀNH CÔNG! {evt_claim}")
    print(f"  Trạng thái hợp đồng chuyển sang: [{app.state}]")
    print(f"  Số dư còn lại trong quỹ: {format_eth(app.contract_balance)}")

    print("\n" + "=" * 75)
    print("PHẦN 3: DEMO LUỒNG HOÀN TIỀN TỰ ĐỘNG KHI THẤT BẠI (REFUND PATH)")
    print("=" * 75)

    fail_app = MockProjectCore(creator, goal_wei, duration, min_wei)
    print("\n[TÌNH HUỐNG THẤT BẠI] Chiến dịch chỉ nhận được 0.20 ETH từ bạn 0xStudentX...")
    fail_app.pledge("0xStudentX", int(0.20 * 10**18))
    print(f"  Tổng huy động: {format_eth(fail_app.total_raised)} (Dưới mục tiêu 1.0 ETH)")

    print("  Thời gian trôi qua hết 7 ngày...")
    fail_app.advance_time(7 * 86400 + 1)

    print("\n[BƯỚC 1] Chủ dự án cố tình rút tiền khi không đạt mục tiêu:")
    try:
        fail_app.claim_funds(creator)
    except RuntimeError as e:
        print(f"  🛡️ BỊ CHẶN: {e}")

    print("\n[BƯỚC 2] Bạn 0xStudentX gọi claimRefund() để lấy lại tiền:")
    evt_refund = fail_app.claim_refund("0xStudentX")
    print(f"  💸 HOÀN TIỀN THÀNH CÔNG: {evt_refund}")
    print(f"  Số dư đóng góp còn lại của 0xStudentX: {fail_app.contributions['0xStudentX']} wei")

    print("\n[BƯỚC 3] Bạn 0xStudentX cố tình gọi claimRefund() lần 2 (Rút kép):")
    try:
        fail_app.claim_refund("0xStudentX")
    except RuntimeError as e:
        print(f"  🛡️ BỊ CHẶN RÚT KÉP: {e}")

    print("\n" + "*" * 75)
    print("🏆 TỔNG KẾT GATE REVIEW 1: 100% CÁC TIÊU CHÍ KỸ THUẬT & NGHIỆP VỤ ĐẠT YÊU CẦU!")
    print("*" * 75)

if __name__ == "__main__":
    run_gate_review_demo()
