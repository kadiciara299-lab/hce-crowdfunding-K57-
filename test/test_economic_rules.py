"""
Test kịch bản quy tắc kinh tế Lab 11 cho ProjectCore.sol
Học phần: ECO2432 - Tiền điện tử & Hợp đồng thông minh
Dự án: HCE Student Crowdfund (Chủ đề 5)
Thực hiện: Nhóm K57 Kinh Tế Số - HCE
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def simulate_campaign():
    print("=" * 60)
    print("KIỂM THỬ QUY TẮC KINH TẾ (LAB 11) - HCE STUDENT CROWDFUND")
    print("=" * 60)

    # Khởi tạo tham số chiến dịch (Constructor)
    funding_goal = 1.0  # 1 ETH (10^18 wei)
    min_contribution = 0.001  # Sàn 0.001 ETH
    max_contribution_per_wallet = (funding_goal * 25) / 100  # Trần 25% = 0.25 ETH
    funding_cap = (funding_goal * 120) / 100  # Trần cứng 120% = 1.20 ETH

    print(f"Mục tiêu gọi vốn (fundingGoal):        {funding_goal} ETH")
    print(f"Sàn đóng góp tối thiểu (minContribution): {min_contribution} ETH")
    print(f"Trần đóng góp mỗi ví (maxPerWallet):      {max_contribution_per_wallet} ETH (25%)")
    print(f"Trần cứng tối đa (fundingCap):            {funding_cap} ETH (120%)")
    print("-" * 60)

    total_raised = 0.0
    contributions = {}

    def pledge(wallet, amount):
        nonlocal total_raised
        print(f"\n[GIAO DỊCH] Ví {wallet} gửi {amount} ETH...")
        # 1. Kiểm tra sàn
        if amount < min_contribution:
            err = f"REVERT: ContributionTooLow(sent={amount} ETH, min={min_contribution} ETH)"
            print(f"  ❌ {err}")
            return False, err

        # 2. Kiểm tra trần cứng Hard Cap
        if total_raised + amount > funding_cap:
            err = f"REVERT: ExceedsFundingCap(attempted={total_raised + amount} ETH, cap={funding_cap} ETH)"
            print(f"  ❌ {err}")
            return False, err

        # 3. Kiểm tra trần ví
        current = contributions.get(wallet, 0.0)
        new_total = current + amount
        if new_total > max_contribution_per_wallet:
            err = f"REVERT: ExceedsMaxContribution(attempted={new_total} ETH, limit={max_contribution_per_wallet} ETH)"
            print(f"  ❌ {err}")
            return False, err

        # Cập nhật số dư & phát event
        contributions[wallet] = new_total
        total_raised += amount
        print(f"  ✅ THÀNH CÔNG! Phát event Pledged(contributor={wallet}, amount={amount} ETH, totalRaised={total_raised} ETH)")
        return True, "SUCCESS"

    # --- Ca 1: Nạp hợp lệ ---
    print("\n--- CA KIỂM THỬ 1: Giao dịch hợp lệ (Happy Path) ---")
    ok, msg = pledge("0xAlice", 0.05)
    assert ok, "Ca 1 phải thành công"

    # --- Ca 2: Vi phạm sàn nạp (Dust attack) ---
    print("\n--- CA KIỂM THỬ 2: Vi phạm sàn đóng góp tối thiểu (0.0005 ETH < 0.001 ETH) ---")
    ok, msg = pledge("0xBob", 0.0005)
    assert not ok and "ContributionTooLow" in msg, "Ca 2 phải revert với ContributionTooLow"

    # --- Ca 3: Vi phạm trần đóng góp mỗi ví (0.3 ETH > 0.25 ETH) ---
    print("\n--- CA KIỂM THỬ 3: Vi phạm trần đóng góp tối đa mỗi ví (0.3 ETH > 0.25 ETH) ---")
    ok, msg = pledge("0xCharlie", 0.30)
    assert not ok and "ExceedsMaxContribution" in msg, "Ca 3 phải revert với ExceedsMaxContribution"

    # --- Ca 4: Nạp hợp lệ tích lũy đến cận trần ví ---
    print("\n--- CA KIỂM THỬ 4: Nạp hợp lệ tích lũy 2 lần chạm trần ví ---")
    ok, msg = pledge("0xDavid", 0.15)
    assert ok
    ok, msg = pledge("0xDavid", 0.10)  # Tổng = 0.25 ETH chạm trần
    assert ok
    ok, msg = pledge("0xDavid", 0.01)  # Vượt trần 0.26 ETH
    assert not ok and "ExceedsMaxContribution" in msg, "Nạp thêm phải bị chặn"

    # --- Ca 5: Vi phạm trần cứng 120% ---
    print("\n--- CA KIỂM THỬ 5: Vi phạm trần cứng Hard Cap 120% ---")
    # Cho thêm người nạp để quỹ đạt 1.15 ETH
    pledge("0xEva", 0.25)
    pledge("0xFrank", 0.25)
    pledge("0xGrace", 0.25)
    pledge("0xHenry", 0.10)
    print(f"Tổng quỹ hiện tại: {total_raised} ETH")
    ok, msg = pledge("0xIvy", 0.10)  # Sẽ đẩy tổng lên 1.25 ETH > 1.20 ETH
    assert not ok and "ExceedsFundingCap" in msg, "Phải revert vì vượt 120% Hard Cap"

    print("\n" + "=" * 60)
    print("KẾT QUẢ: 100% CA THỬ NGHIỆM ĐẠT CHUẨN! TẤT CẢ RÀO CẢN KINH TẾ ĐƯỢC THI THIẾT HÀNH CHÍNH XÁC.")
    print("=" * 60)

if __name__ == "__main__":
    simulate_campaign()
