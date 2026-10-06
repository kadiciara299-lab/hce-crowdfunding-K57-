#!/usr/bin/env python3
"""
Bộ kiểm thử tự động cho wallet_analyzer.py
Tuân thủ quy ước AGENTS.md: Nêu tối thiểu 3 ca kiểm thử, gồm 1 trường hợp gian lận.
"""

from wallet_analyzer import parse_and_calculate_cash_flow


def test_case_1_normal_flow():
    """Ca 1: Luồng nghiệp vụ bình thường (nạp tiền và chuyển tiền thành công)"""
    my_wallet = "0x1111111111111111111111111111111111111111"
    mock_txs = [
        # Giao dịch 1: Nhận 1.0 ETH từ ví khác (R1: Tiền vào)
        {
            "timeStamp": "1700000000",
            "from": "0x2222222222222222222222222222222222222222",
            "to": my_wallet,
            "value": str(1 * 10**18),
            "gasUsed": "21000",
            "gasPrice": str(20 * 10**9),
            "isError": "0",
            "hash": "0xabc1"
        },
        # Giao dịch 2: Chuyển đi 0.4 ETH (R2, R3: Tiền ra = 0.4 + phí gas)
        # Phí gas = 21000 * 20 Gwei = 0.00042 ETH
        {
            "timeStamp": "1700001000",
            "from": my_wallet,
            "to": "0x3333333333333333333333333333333333333333",
            "value": str(int(0.4 * 10**18)),
            "gasUsed": "21000",
            "gasPrice": str(20 * 10**9),
            "isError": "0",
            "hash": "0xabc2"
        }
    ]

    res = parse_and_calculate_cash_flow(my_wallet, mock_txs)
    assert len(res["rows"]) == 2
    assert res["total_inflow"] == 1.0
    expected_gas = (21000 * 20 * 10**9) / 10**18  # 0.00042 ETH
    assert abs(res["total_outflow"] - (0.4 + expected_gas)) < 1e-8
    assert abs(res["net_flow"] - (1.0 - 0.4 - expected_gas)) < 1e-8
    print("[PASS] Ca kiểm thử 1: Luồng nạp/rút tiền bình thường thành công.")


def test_case_2_empty_transactions():
    """Ca 2: Trường hợp biên (Ví mới tạo hoặc không có giao dịch trong 90 ngày)"""
    my_wallet = "0x0000000000000000000000000000000000000000"
    mock_txs = []

    res = parse_and_calculate_cash_flow(my_wallet, mock_txs)
    assert len(res["rows"]) == 0
    assert res["total_inflow"] == 0.0
    assert res["total_outflow"] == 0.0
    assert res["net_flow"] == 0.0
    print("[PASS] Ca kiểm thử 2: Trường hợp ví không có giao dịch (xử lý danh sách rỗng an toàn).")


def test_case_3_fraud_and_failed_transactions():
    """
    Ca 3: Trường hợp gian lận / Thao túng thất bại (Fraud & Failed Execution)
    Kẻ tấn công gọi hàm rút tiền trái phép từ smart contract (hoặc bẫy phishing), 
    giao dịch bị REVERT (isError = '1').
    Quy tắc R4: Giá trị chuyển (value = 5 ETH) KHÔNG bị trừ, nhưng ví VẪN MẤT PHÍ GAS.
    """
    my_wallet = "0x9999999999999999999999999999999999999999"
    mock_txs = [
        # Giao dịch gian lận bị Revert: Thử rút 5 ETH nhưng thất bại
        {
            "timeStamp": "1700005000",
            "from": my_wallet,
            "to": "0xContractVulnerableBank",
            "value": str(5 * 10**18),
            "gasUsed": "80000",
            "gasPrice": str(50 * 10**9),
            "isError": "1",  # THẤT BẠI
            "hash": "0xexploit_fail"
        }
    ]

    res = parse_and_calculate_cash_flow(my_wallet, mock_txs)
    assert len(res["rows"]) == 1
    row = res["rows"][0]
    assert row["type"] == "OUT (FAILED)"
    assert row["value_eth"] == 5.0
    expected_gas_fee = (80000 * 50 * 10**9) / 10**18  # 0.004 ETH
    assert abs(row["gas_fee_eth"] - expected_gas_fee) < 1e-8
    assert abs(row["net_impact"] - (-expected_gas_fee)) < 1e-8
    assert res["total_inflow"] == 0.0
    # Tổng tiền ra CHỈ bằng phí gas vì lệnh chuyển bị chặn (value không bị mất)
    assert abs(res["total_outflow"] - expected_gas_fee) < 1e-8
    print("[PASS] Ca kiểm thử 3: Trường hợp giao dịch thất bại/gian lận được bảo toàn giá trị chuyển và trừ đúng phí gas.")


if __name__ == "__main__":
    print("--- CHẠY BỘ KIỂM THỬ CHO WALLET ANALYZER (LAB 6) ---")
    test_case_1_normal_flow()
    test_case_2_empty_transactions()
    test_case_3_fraud_and_failed_transactions()
    print("--- TẤT CẢ CÁC CA KIỂM THỬ ĐÃ ĐẠT CHUẨN 100% ---")
